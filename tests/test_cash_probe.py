from decimal import Decimal as D
import copy
import pytest
from esun_research.cash_probe import recovery_gate,market_state
from esun_research.research_tools import ResearchWorkspace
from esun_research.turnover import held_positions
from test_candidate import environment
from test_turnover import settled
from test_strategy_agent import proposal


def spare_cash(pack):
    invested=pack.account.nav_tradable-pack.account.cash
    nav=invested/D('.79');cash=nav-invested
    return pack.model_copy(update={'account':pack.account.model_copy(update={'cash':cash,'nav_tradable':nav,'aum':nav,'cash_ratio_tradable':D('.21')})})


def eligible(workspace):
    for i,(c,r) in enumerate(workspace.rows.items()):
        r['values'].update(revenue_yoy_pct='10',relative_pool_20='.05',momentum_1='.01',momentum_3='-.01',foreign_net_ratio_3='-.05',trust_net_ratio_3='.01')


def test_gates_require_resilience_price_and_flow_support_not_only_large_decline():
    v={'revenue_yoy_pct':'10','relative_pool_20':'.05','momentum_1':'.01','momentum_3':'-.1','foreign_net_ratio_3':'-.1','trust_net_ratio_3':'.02'}
    assert recovery_gate(v)==[]
    assert 'no_initial_price_stabilization' in recovery_gate({**v,'momentum_1':'-.2'})
    assert 'no_relative_resilience' in recovery_gate({**v,'relative_pool_20':'-.05'})
    assert recovery_gate({}) and all(x.startswith('missing:') for x in recovery_gate({}))


def test_cash_probe_spends_bounded_cash_without_selling_and_can_add_new_names(environment):
    *_,pack,policy,schema,req,snapshot,settings=settled(environment)
    pack=spare_cash(pack)
    w=ResearchWorkspace(snapshot,pack,policy,settings);eligible(w)
    result=w.evaluate(proposal('probe','lower',mode='cash_probe'))
    assert not result['errors'],result['errors']
    orders=result['orders'];assert 1<=len(orders)<=2 and all(o['side']=='BUY' for o in orders)
    assert any(o['ticker'] not in held_positions(pack) for o in orders)
    assert result['holdings']<=30
    spent=sum(D(snapshot['prices'][o['ticker']])*o['shares']*(1+policy.buy_fee) for o in orders)
    assert spent/pack.account.nav_tradable<=settings.maximum_cash_deployment
    assert all(D(snapshot['prices'][o['ticker']])*o['shares']/pack.account.nav_tradable<=settings.maximum_probe_weight for o in orders)
    assert D(result['cash_ratio'])>=settings.minimum_probe_cash


def test_probe_does_not_force_spending_or_bypass_buy_restrictions(environment):
    *_,pack,policy,schema,req,snapshot,settings=settled(environment)
    pack=spare_cash(pack)
    w=ResearchWorkspace(snapshot,pack,policy,settings)
    e=w.evaluate(proposal('none',mode='cash_probe'))
    assert not e['errors'] and e['orders']==[]
    eligible(w)
    from esun_research.cash_probe import probe_positions
    ranked=[{**r['candidate'],'score':D(1)} for r in w.rows.values()]
    snapshot=copy.deepcopy(snapshot)
    snapshot['trading_risk']={'securities':{c:{'buy_allowed':False,'sell_allowed':True,'flags':[]} for c in w.rows}}
    # Existing order guard must reject every prohibited addition, not just new names.
    positions,_,suppressed,detail=probe_positions(ranked,w.rows,pack,snapshot,policy,settings,D('.15'))
    assert positions==held_positions(pack) and detail['changed_names']==0
    assert suppressed


def test_stressed_and_recovering_regimes_are_descriptive_and_do_not_force_orders():
    assert market_state({})['state']=='unknown'
    panel={str(i):{'closes':['100','99','98','97','96'],'returns':['-.01']*4} for i in range(20)}
    assert market_state({'series':panel})['state']=='stressed'
    for p in panel.values():p.update(closes=['96','97','98','99','100'],returns=['.01']*4)
    assert market_state({'series':panel})['state']=='recovering'
