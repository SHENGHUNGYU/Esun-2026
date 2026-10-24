"""Official v4.3 structural checks plus independent order and lineage checks."""
from collections import Counter
from decimal import Decimal
from jsonschema import Draft202012Validator, FormatChecker
from .contracts import instant,now
from .portfolio import compile_orders,estimate,breaches,decimal

def validate_plan(plan,schema,pack,prices,universe,cutoff,policy,expected_observations=None,expected_sources=None):
    Draft202012Validator.check_schema(schema)
    errors=['schema:'+('/'.join(map(str,e.absolute_path)) or '/')+':'+e.message for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(plan)]
    if errors:return errors
    if plan['team_id']!=pack.team_id or plan['trade_date']!=pack.trade_date.isoformat():errors.append('account_identity')
    if pack.decision_gate().startswith('BLOCKED'):errors.append('account_gate:'+pack.decision_gate())
    if instant(pack.generated_at)>instant(cutoff):errors.append('account_after_cutoff')
    if expected_observations is not None and plan['observations']!=expected_observations:errors.append('observation_lineage_mismatch')
    if expected_sources is not None and plan['sources']!=expected_sources:errors.append('source_lineage_mismatch')
    ids={}
    for collection,key,prefix in [('sources','source_id','S'),('observations','obs_id','O'),('inferences','inf_id','I'),('decisions','decision_id','D')]:
        actual=[r[key] for r in plan[collection]]
        if actual!=[prefix+str(i+1) for i in range(len(actual))]:errors.append('noncontinuous_ids:'+collection)
        ids[prefix]=set(actual)
    for s in plan['sources']:
        for key in ['content_as_of','published_at','fetched_at']:
            if key in s:
                try:
                    if instant(s[key])>instant(cutoff):errors.append('source_after_cutoff:'+s['source_id'])
                except ValueError:errors.append('invalid_source_timestamp')
        if not s['url'].startswith('https://'):errors.append('non_https_source')
        if 'example.com' in s['url']:errors.append('example_source')
    refs=[(r['source_ref'],'S') for r in plan['observations']]+[(r['premise_refs'],'O') for r in plan['inferences']]+[(r['inference_refs'],'I') for r in plan['decisions']]+[(r['reason_refs'],'I') for r in plan['no_trade_decisions']]+[(plan['market_view']['basis_refs'],'O')]
    if any(not set(values)<=ids[kind] for values,kind in refs):errors.append('broken_reference_chain')
    market_ids={r['obs_id'] for r in plan['observations'] if r.get('topic')=='tw_market'}
    if not set(plan['market_view']['basis_refs'])<=market_ids:errors.append('non_market_basis')
    changed=[r['ticker'] for r in plan['decisions']];unchanged=[r['ticker'] for r in plan['no_trade_decisions']]
    if len(changed)!=len(set(changed)) or len(unchanged)!=len(set(unchanged)) or set(changed)&set(unchanged):errors.append('duplicate_decision_coverage')
    held={h.code for h in (pack.holdings or []) if h.shares>0}
    if not held<=set(changed+unchanged) or not set(unchanged)<=held:errors.append('incomplete_holding_coverage')
    if not set(changed+unchanged)<=set(universe):errors.append('outside_universe')
    try:
        expected=compile_orders(plan['decisions'],pack,prices)
        signature=lambda orders:Counter((r['ticker'],r['side'],r['shares'],r['decision_ref']) for r in orders)
        if signature(expected)!=signature(plan['orders']):errors.append('official_order_formula_mismatch')
        if len({r['ticker'] for r in plan['orders']})!=len(plan['orders']):errors.append('duplicate_order_ticker')
        state=estimate(pack,plan['orders'],prices,policy)
        errors+=breaches(state,policy)
        lo,hi=map(decimal,plan['market_view']['posture']['target_cash_pct_range'])
        if not lo<=hi or not lo<=state['cash_ratio_previous_nav']<=hi:errors.append('declared_cash_range')
        net=state['net_flow'];intent=plan['market_view']['posture']['net_exposure_intent']
        if (intent=='increase' and net<=0) or (intent=='reduce' and net>=0) or (intent=='hold' and abs(net)>pack.account.nav_tradable*Decimal('.02')):errors.append('posture_mismatch')
        declared=[]
        by_id={d['decision_id']:d for d in plan['decisions']}
        for d in plan['decisions']:
            if 'funding_for' in d:
                declared.append(d['decision_id'])
                if d['action'] not in {'TRIM','SELL_ALL'} or any(x not in by_id or by_id[x]['action'] not in {'BUY','ADD'} for x in d['funding_for']):errors.append('invalid_funding_reference')
        if declared:
            removed=[o for o in plan['orders'] if o['decision_ref'] not in declared]
            counter=estimate(pack,removed,prices,policy)
            if counter['cash_ratio_previous_nav']>=lo:errors.append('funding_gap_not_real')
    except (ValueError,KeyError,TypeError) as e:errors.append('portfolio_validation:'+str(e))
    try:
        start=instant(plan['agent_metadata']['run_started_at']);end=instant(plan['agent_metadata']['run_completed_at'])
        if start>end or end>instant(now()):errors.append('invalid_run_timestamps')
    except ValueError:errors.append('invalid_run_timestamps')
    return sorted(set(errors))
