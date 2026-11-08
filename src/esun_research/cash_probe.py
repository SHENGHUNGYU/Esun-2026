"""Bounded cash-funded recovery experiments, never an automatic risk-on switch."""
from decimal import Decimal,ROUND_FLOOR
from .portfolio import decimal
from .turnover import held_positions,check_positions,budget_errors


def market_state(risk_data):
    series=risk_data.get('series',{})
    if len(series)<20:return {'state':'unknown','reason':'insufficient_verified_panel','members':len(series)}
    def fraction(test):return sum(test(p) for p in series.values())/len(series)
    advance=fraction(lambda p:decimal(p['returns'][-1])>0)
    above=fraction(lambda p:decimal(p['closes'][-1])>sum(map(decimal,p['closes'][-5:]))/5)
    recovery=fraction(lambda p:decimal(p['closes'][-1])>decimal(p['closes'][-4]))
    state='recovering' if min(advance,above,recovery)>=.5 else 'stressed' if above<.25 and recovery<.25 else 'mixed'
    return {'state':state,'members':len(series),'last_session_advancing_fraction':round(advance,6),
        'above_ma5_fraction':round(above,6),'three_session_positive_fraction':round(recovery,6),
        'basis':'Current competition-pool price panel; heuristic research regime, not official index or confirmed bottom.'}


def recovery_gate(values):
    """Positive revenue, relative resilience, initial price stabilization and flow support.

    These are conservative experiment eligibility rules, not estimated alpha.
    At least one supported flow may be positive; the other is allowed to sell.
    """
    required=['revenue_yoy_pct','relative_pool_20','momentum_1','momentum_3','foreign_net_ratio_3','trust_net_ratio_3']
    missing=[f for f in required if values.get(f) is None]
    if missing:return ['missing:'+f for f in missing]
    v={f:decimal(values[f]) for f in required};failed=[]
    if v['revenue_yoy_pct']<=0:failed.append('nonpositive_revenue_growth')
    if v['relative_pool_20']<=0:failed.append('no_relative_resilience')
    if max(v['momentum_1'],v['momentum_3'])<=0:failed.append('no_initial_price_stabilization')
    if max(v['foreign_net_ratio_3'],v['trust_net_ratio_3'])<=0:failed.append('no_recent_institutional_support')
    return failed


def probe_positions(ranked,rows,pack,snapshot,policy,settings,cash_target):
    """Buy only, <=2 positions; exact lots/fees, spare cash and all existing gates.

    No held name is sold to force this alternative. Market weakness does not
    force spending. Selection among feasible alternatives belongs to the agent.
    """
    positions=held_positions(pack);reasons={c:'維持官方原股數；本方案只比較有限現金試探。' for c in positions}
    nav=pack.account.nav_tradable;floor=max(settings.minimum_probe_cash,policy.cash_band[0],decimal(cash_target))
    budget=min(settings.maximum_cash_deployment*nav,max(Decimal(0),pack.account.cash-floor*nav))
    initial=budget;suppressed=[];buys=0
    for r in ranked:
        if buys>=settings.maximum_probe_names or budget<=0:break
        c=r['code'];failed=recovery_gate(rows.get(c,{}).get('values',{}))
        if failed:
            suppressed.append({'code':c,'reason':'recovery_gate','details':failed});continue
        if c not in positions and len(positions)>=min(30,settings.maximum_holdings):
            suppressed.append({'code':c,'reason':'holding_count_limit'});continue
        price=decimal(snapshot['prices'][c]);amount=min(budget,settings.maximum_probe_weight*nav)
        lots=int((amount/(price*(1+policy.buy_fee))/1000).to_integral_value(rounding=ROUND_FLOOR))
        if lots<=0 or lots*1000*price<settings.minimum_trade_fraction*nav:continue
        trial={**positions,c:positions.get(c,0)+lots*1000}
        orders,state,errors=check_positions(trial,pack,snapshot,policy)
        errors+=budget_errors(orders,state,pack,snapshot['prices'],settings)
        if state['cash']/nav<floor:errors.append('probe_cash_floor')
        if errors:
            suppressed.append({'code':c,'reason':'risk_or_budget','errors':sorted(set(errors))});continue
        cost=lots*1000*price*(1+policy.buy_fee);positions=trial;budget-=cost;buys+=1
        reasons[c]='營收支撐、相對抗跌與初步價格及法人訊號通過試探條件；有限使用現金，尚非反轉或收益已證實。'
    return positions,reasons,suppressed,{'cash_floor_reference_nav':str(floor),
        'maximum_cash_deployment':str(settings.maximum_cash_deployment),
        'actual_cash_deployed_fraction':str((initial-budget)/nav),'changed_names':buys,
        'no_automatic_spending':True,'scope':'Conservative recovery experiment; positive revenue is not complete earnings-quality proof.'}
