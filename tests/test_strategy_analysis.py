import copy
from decimal import Decimal
import pytest
from test_candidate import environment
from test_turnover import settled
from test_strategy_agent import proposal
from test_holding_ledger import pack
from esun_research.research_tools import ResearchWorkspace
from esun_research.strategy_analysis import asset_bridge
from esun_research.turnover import gradual_positions,check_positions,budget_errors,held_positions


def test_diagnostics_missing_does_not_mean_bearish(environment):
    *_,p,policy,schema,req,snapshot,settings=settled(environment)
    ws=ResearchWorkspace(snapshot,p,policy,settings)
    code=next(c for c in held_positions(p) if c in ws.rows);ws.rows[code]['values'].pop('revenue_yoy_pct')
    r=ws.evaluate(proposal('diagnostic'))
    row=next(x for x in r['diagnostics']['rows'] if x['code']==code)
    assert row['stage']=='missing_features' and row['missing_features']==['revenue_yoy_pct']
    assert row['rank'] is None and row['held']
    assert len(r['diagnostics']['rows'])==len(snapshot['coverage'])


def test_gradual_caps_basket_cash_and_missing_features(environment):
    *_,p,policy,schema,req,snapshot,settings=settled(environment)
    held=held_positions(p);codes=sorted(held)
    ranked=[{'code':c,'score':Decimal(i)/len(codes)} for i,c in enumerate(codes)]
    # A missing signal freezes this holding rather than causing liquidation.
    missing=codes[len(codes)//2];ranked=[r for r in ranked if r['code']!=missing]
    positions,reasons,suppressed=gradual_positions(ranked,p,snapshot,policy,settings,'rank_tilt')
    assert positions[missing]==held[missing] and set(positions)==set(held)
    orders,state,errors=check_positions(positions,p,snapshot,policy)
    assert orders and not errors and not budget_errors(orders,state,p,snapshot['prices'],settings)
    assert state['cash']>=p.account.cash
    assert len(orders)<=2*settings.maximum_resize_pairs
    for c in positions:
        assert positions[c]>=1000
        assert abs(positions[c]-held[c])*Decimal(snapshot['prices'][c])<=settings.maximum_resize_weight*p.account.nav_tradable
    assert all(o['ticker'] in reasons for o in orders)


def test_gradual_no_signal_or_budget_means_hold(environment):
    *_,p,policy,schema,req,snapshot,settings=settled(environment)
    ranked=[{'code':c,'score':Decimal('.5')} for c in held_positions(p)]
    positions,_,_=gradual_positions(ranked,p,snapshot,policy,settings,'rank_tilt')
    assert positions==held_positions(p)
    ranked=[{'code':c,'score':Decimal(i)/30} for i,c in enumerate(sorted(positions))]
    strict=settings.model_copy(update={'maximum_daily_cost':Decimal('0.00000001')})
    assert gradual_positions(ranked,p,snapshot,policy,strict,'rank_tilt')[0]==positions


def test_bridge_exact_and_not_trading_pnl():
    a=pack(price='10',cash='90000');b=pack(day='2026-10-28',shares=2000,price='12',cash='79000')
    r=asset_bridge(a,b)
    assert r['status']=='COMPLETE_BRIDGE'
    assert Decimal(r['price_effect'])==2000 and Decimal(r['quantity_at_close_effect'])==12000
    assert Decimal(r['cash_change'])==-11000 and Decimal(r['aum_change'])==3000
    assert Decimal(r['unexplained_residual'])==0
    assert 'realized_pnl' not in r


def test_exited_stock_requires_same_date_closing_evidence():
    a=pack(price='10',cash='90000');b=pack(day='2026-10-28',shares=0,cash='101000')
    assert asset_bridge(a,b)['status']=='PARTIAL_BRIDGE'
    r=asset_bridge(a,b,{'2330':'12'},'2026-10-28')
    assert r['status']=='COMPLETE_BRIDGE' and Decimal(r['price_effect'])==2000
    assert Decimal(r['quantity_at_close_effect'])==-12000
    with pytest.raises(ValueError,match='price_date'):asset_bridge(a,b,{'2330':'12'},'2026-10-27')
    with pytest.raises(ValueError,match='team'):asset_bridge(a,pack(day='2026-10-28',team='OTHER'))


def test_gradual_output_compiles_to_official_add_trim_without_new_names(environment):
    from esun_research.candidate import compile_document
    from esun_research.portfolio import Policy
    from esun_research.dplan import validate_plan
    store,sources,universe,p,policy,schema,req,snapshot,settings=settled(environment)
    ws=ResearchWorkspace(snapshot,p,policy,settings)
    result=ws.evaluate(proposal('gradual-test','lower',mode='gradual',weighting='rank_tilt'))
    assert not result['errors'] and result['orders']
    plan,_,projected=compile_document(snapshot,result['ranking'],result['targets'],p,policy,req.model_dump(mode='json'),sources)
    assert not validate_plan(plan,schema,p,snapshot['prices'],universe,req.cutoff_at,policy)
    assert set(projected['positions'])==set(held_positions(p))
    assert {d['action'] for d in plan['decisions']}=={'ADD','TRIM'}


def test_analysis_api_rejects_tampered_reports_and_unauthorized_generation(tmp_path):
    from esun_research.application import create_app
    from esun_research.store import encoded,digest
    from fastapi.testclient import TestClient
    ident='a'*16;folder=tmp_path/'strategy-analysis'/ident;folder.mkdir(parents=True)
    report={'id':ident,'source_run':'test','reference_date':'2026-10-28','trade_date':'2026-10-29','cutoff_at':'2026-10-28T23:00:00+08:00'}
    files={'report.json':encoded(report),'inputs.json':b'{}','snapshot.json':b'{}','report.md':b'# analysis'}
    for name,body in files.items():(folder/name).write_bytes(body)
    (folder/'manifest.json').write_bytes(encoded({'artifacts':{n:digest(b) for n,b in files.items()}}))
    client=TestClient(create_app(tmp_path,model_config=None))
    assert client.get('/api/strategy-analysis').json()['reports'][0]['id']==ident
    assert client.get('/api/strategy-analysis/'+ident).json()==report
    assert client.post('/api/strategy-analysis',json={'source_run':'test'}).status_code==403
    (folder/'report.json').write_bytes(b'{}')
    assert client.get('/api/strategy-analysis/'+ident).status_code==400
