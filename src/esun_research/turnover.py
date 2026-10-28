"""Position continuity, bounded turnover and explicit no-trade alternatives.

Rank gaps are dimensionless evidence thresholds, never expected returns.
"""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
from collections import defaultdict
from .portfolio import decimal,target_shares,estimate,breaches


def held_positions(pack):return {h.code:h.shares for h in pack.holdings if h.shares>0}


def weights_for_positions(positions,pack,prices):
    # Half a share inside the same lot interval prevents float round-down from
    # turning an exact retained lot into an unintended 1,000-share sell.
    result={c:float((Decimal(n)+Decimal('.5'))*decimal(prices[c])/pack.account.nav_tradable) for c,n in positions.items() if n>0}
    if any(target_shares(result[c],pack.account.nav_tradable,prices[c])!=n for c,n in positions.items() if n>0):
        raise ValueError('retained_lot_encoding_failed')
    return result


def orders_for_positions(positions,pack):
    held=held_positions(pack)
    return [{'ticker':c,'side':'BUY' if positions.get(c,0)>held.get(c,0) else 'SELL',
        'shares':abs(positions.get(c,0)-held.get(c,0)),'decision_ref':'D'+str(i+1)}
        for i,c in enumerate(sorted(set(positions)|set(held))) if positions.get(c,0)!=held.get(c,0)]


def industries(snapshot):
    import json
    result={c['code']:c['industry'] for c in snapshot['candidates']}
    for r in snapshot['records']:
        if r['kind']=='revenue' and r['security_id'] not in result:
            result[r['security_id']]=str(json.loads(r['raw_json']).get('產業別','unknown'))
    return result


def check_positions(positions,pack,snapshot,policy):
    orders=orders_for_positions(positions,pack);state=estimate(pack,orders,snapshot['prices'],policy)
    groups=industries(snapshot)
    errors=breaches(state,policy,{c:groups.get(c,'unknown') for c in positions})
    if not policy.cash_band[0]<=state['cash_ratio']<=policy.cash_band[1]:errors.append('cash_policy_band')
    if snapshot.get('trading_risk'):
        from .risk import order_errors
        errors+=order_errors(snapshot['trading_risk'],orders)
    return orders,state,sorted(set(errors))


def budget_errors(orders,state,pack,prices,settings):
    gross=sum((decimal(prices[o['ticker']])*o['shares'] for o in orders),Decimal(0))/pack.account.nav_tradable
    errors=[]
    if gross>settings.maximum_daily_turnover:errors.append('daily_turnover_budget_exceeded')
    if state['fees']/pack.account.nav_tradable>settings.maximum_daily_cost:errors.append('daily_cost_budget_exceeded')
    return errors


def repair_positions(pack,snapshot,policy):
    """Greedy constraint repair, not a proof of minimum turnover."""
    positions=held_positions(pack);prices=snapshot['prices'];groups=industries(snapshot);reasons={}
    for _ in range(80):
        orders,state,errors=check_positions(positions,pack,snapshot,policy)
        if not errors:return positions,reasons
        weights=state['weights'];nav=state['nav'];change=None
        if len(positions)>30:
            c=min(positions,key=lambda c:decimal(prices[c])*positions[c]);change=(c,0,'持股數超過限制，依最小名目部位修正。')
        else:
            sector_weights=defaultdict(lambda:Decimal(0))
            for c,w in weights.items():sector_weights[groups.get(c,'unknown')]+=w
            for c,w in sorted(weights.items(),key=lambda item:-item[1]):
                cap=policy.tsmc_cap if c=='2330' else policy.single_cap
                excess=max(w-cap,sector_weights[groups.get(c,'unknown')]-policy.industry_cap)
                if excess>0:
                    lots=int(((excess*nav/decimal(prices[c]))/1000).to_integral_value(rounding=ROUND_CEILING))+1
                    change=(c,max(0,positions[c]-lots*1000),'官方持股單股或產業集中度超過內部限制，減少超額部位。');break
        if change is None and state['cash_ratio']<policy.cash_band[0]:
            c=max(positions,key=lambda c:decimal(prices[c])*positions[c])
            amount=(policy.cash_band[0]+Decimal('.005'))*nav-state['cash']
            lots=int((amount/(decimal(prices[c])*(1-policy.sell_fee_tax))/1000).to_integral_value(rounding=ROUND_CEILING))
            change=(c,max(0,positions[c]-max(1,lots)*1000),'現金低於政策下限，補回現金緩衝。')
        if change is None and (len(positions)<20 or state['cash_ratio']>policy.cash_band[1]):
            for row in sorted(snapshot['candidates'],key=lambda r:(r['code'] in positions,-decimal(r['amount']),r['code'])):
                c=row['code']
                if len(positions)>=30 and c not in positions:continue
                if len(positions)<20 and c in positions:continue
                cap=policy.tsmc_cap if c=='2330' else policy.single_cap
                sector=sum(w for code,w in weights.items() if groups.get(code,'unknown')==groups.get(c,'unknown'))
                capacity=min(cap-weights.get(c,0),policy.industry_cap-sector)*nav
                needed=max(Decimal(0),state['cash']-policy.cash_target*nav)
                amount=min(capacity*Decimal('.98'),needed if needed>0 else decimal(prices[c])*1000)
                lots=int((amount/(decimal(prices[c])*(1+policy.buy_fee))/1000).to_integral_value(rounding=ROUND_FLOOR))
                if lots>0:
                    change=(c,positions.get(c,0)+lots*1000,'僅為修正現金過高或持股不足，使用已通過新買風險檢查的流動部位。');break
        if change is None:raise ValueError('no_verified_risk_repair_available')
        c,n,reason=change
        if n:positions[c]=n
        else:positions.pop(c,None)
        reasons[c]=reason
    raise ValueError('risk_repair_did_not_converge')


def continuity_positions(ranked,desired,pack,snapshot,policy,settings):
    held=held_positions(pack);positions=dict(held);reasons={};suppressed=[]
    rank={r['code']:i+1 for i,r in enumerate(ranked)};score={r['code']:r['score'] for r in ranked}
    # Missing current factor data does not, by itself, justify a sale.
    exits=sorted([c for c in held if c in score and rank[c]>policy.holdings+settings.retention_rank_buffer],key=lambda c:score[c])
    entrants=[r['code'] for r in ranked[:policy.holdings] if r['code'] not in held and r['code'] in desired]
    replacements=0
    for new in entrants:
        if not exits or replacements>=settings.maximum_replacements:break
        old=exits[0];gap=score[new]-score[old]
        if gap<settings.minimum_rank_score_gap:continue
        if decimal(snapshot['prices'][old])*positions[old]/pack.account.nav_tradable<settings.minimum_trade_fraction:continue
        cash=decimal(snapshot['prices'][old])*positions[old]*(1-policy.sell_fee_tax)
        n=int((cash/(decimal(snapshot['prices'][new])*(1+policy.buy_fee))/1000).to_integral_value(rounding=ROUND_FLOOR))*1000
        if n<=0:continue
        proposal={c:n0 for c,n0 in positions.items() if c!=old};proposal[new]=n
        orders,state,errors=check_positions(proposal,pack,snapshot,policy)
        if errors or budget_errors(orders,state,pack,snapshot['prices'],settings):continue
        positions=proposal;exits.pop(0);replacements+=1
        reasons[old]='排名已超出續抱區間，替代標的分數差通過門檻，成對換股且通過風險與成本預算。'
        reasons[new]=reasons[old]
    # Within-name re-equalisation is not a trade trigger. Record the suppressed
    # small proposals; material limit violations belong to the repair comparison.
    for c in sorted(set(held)&set(desired)&set(positions)):
        wanted=target_shares(desired[c],pack.account.nav_tradable,snapshot['prices'][c]);delta=wanted-positions[c]
        drift=abs(Decimal(delta)*decimal(snapshot['prices'][c])/pack.account.nav_tradable)
        if delta and (drift<=settings.weight_deadband or drift<settings.minimum_trade_fraction):
            suppressed.append({'code':c,'reason':'weight_deadband_or_minimum_trade','suppressed_delta_shares':delta})
    for c in positions:
        reasons.setdefault(c,'維持官方實際股數；未有通過續抱區間、替代訊號、風險及成本門檻的必要交易。')
    return positions,reasons,suppressed


def previous_strategy(store,pack,cutoff):
    """Freeze only a unique same-day local strategy with reconciled share evidence."""
    import json
    from .research_tools import StrategyProposal
    from .daily import review_previous
    from .contracts import instant
    review=review_previous(store,pack);matches=[]
    for item in review['comparisons']:
        if item['reconciliation']['status']!='RECONCILED_SHARES':continue
        folder=store.root/'candidates'/item['run_id'];manifest=json.loads((folder/'manifest.json').read_bytes())
        if instant(manifest['request']['cutoff_at'])>instant(cutoff):continue
        if 'agent-research.json' not in manifest['artifacts']:continue
        research=json.loads((folder/'agent-research.json').read_bytes())
        if research.get('status')=='SELECTED':matches.append({'run_id':item['run_id'],'plan_sha256':item['plan_sha256'],'proposal':research['selected_evaluation']['proposal']})
    hashes={StrategyProposal.model_validate(m['proposal']).economic_hash() for m in matches}
    if len(hashes)!=1:return {'proposal':None,'reason':'missing_or_ambiguous_reconciled_previous_strategy','submission_verified':False}
    return {**matches[0],'equivalent_local_matches':[m['run_id'] for m in matches],'submission_verified':False}
