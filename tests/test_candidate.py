import copy
import json
from datetime import date
from decimal import Decimal
from pathlib import Path
import pytest
from esun_research.candidate import DecisionRequest,generate_candidate
from esun_research.contracts import Source
from esun_research.store import Store,encoded,digest
from esun_research.portfolio import Policy,compile_orders,estimate,target_shares
from esun_research.datapack import DataPack
from esun_research.dplan import validate_plan

ROOT=Path(__file__).resolve().parents[1]
TIME='2026-10-24T08:00:00+08:00'

@pytest.fixture
def environment(tmp_path):
    universe={str(1000+i):{'name':f'公司{i}','market':'TWSE' if i<100 else 'TPEX'} for i in range(150)}
    sources=[];store=Store(tmp_path)
    for provider in ['TWSE','TPEx']:
        for kind in ['quotes','valuation','revenue']:
            source=Source(id=provider+'-'+kind,url=('https://openapi.twse.com.tw/v1/test' if provider=='TWSE' else 'https://www.tpex.org.tw/openapi/v1/test'),provider=provider,branch='fundamentals' if kind=='revenue' else 'market',kind=kind)
            rows=[]
            for i in range(150):
                if (i<100)!=(provider=='TWSE'):continue
                code=str(1000+i);price=100+i
                if kind=='quotes':
                    values=[str(v) for v in [price,price+10,price-10,price+2,1000000,(price+1)*1000000]]
                    keys=['OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','TradeVolume','TradeValue'] if provider=='TWSE' else ['Open','High','Low','Close','TradingShares','TransactionAmount']
                    row=dict(zip(keys,values));row.update(Date='1151022',**({'Code':code} if provider=='TWSE' else {'SecuritiesCompanyCode':code}))
                elif kind=='valuation':
                    row={'Date':'1151022',**({'Code':code,'PEratio':str(10+i%30),'PBratio':'2','DividendYield':'1'} if provider=='TWSE' else {'SecuritiesCompanyCode':code,'PriceEarningRatio':str(10+i%30),'PriceBookRatio':'2','YieldRatio':'1'})}
                else:row={'公司代號':code,'資料年月':'11509','產業別':'sector-'+str(i%10),'營業收入-去年同月增減(%)':str(5+i%60),'營業收入-上月比較增減(%)':'2'}
                rows.append(row)
            store.capture(source.id,encoded(rows),fetched_at=TIME);sources.append(source)
    pack=DataPack.model_validate({'schema_version':'3.0','doc_type':'DataPack','team_id':'TEST_TEAM','trade_date':'2026-10-27','as_of_date':None,'generated_at':'2026-10-24T07:00:00+08:00','missing':[],
        'prev_day_orders':{'outcome':'none','void_reasons':[],'excluded_codes':[]},
        'account':{'cash':1000000000,'nav_tradable':1000000000,'aum':1000000000,'receivable_cash':0,'cash_ratio_tradable':1,'holdings_count':0},'holdings':[],
        'compliance':{'violations':0,'notices':0,'incidents':[]}})
    policy=Policy.model_validate_json((ROOT/'config/baseline-policy.json').read_bytes())
    schema=json.loads((ROOT/'docs/official-2026-10-24/D-Plan.schema_v4.3.json').read_bytes())
    request=DecisionRequest(run_id='candidate-test',cutoff_at=TIME,as_of='2026-10-22',team_id=pack.team_id,trade_date=pack.trade_date,mode='fixture',
       datapack_ref=store.put(pack.model_dump_json().encode(),'bin'),policy_ref=store.put_json(policy.model_dump(mode='json')),schema_ref=store.put_json(schema),
       session_ref=store.put_json({'first_trade_date':'2026-10-27','first_reference_date':'2026-10-22'}),datapack_seen_at=TIME,
       universe_hash=digest(encoded(universe)),registry_hash=digest(encoded([s.model_dump() for s in sources])),code_hash='c')
    return store,sources,universe,pack,policy,schema,request

def run(env,**kw):
    store,sources,universe,*_,req=env
    return generate_candidate(store,req,sources,universe,**kw)

def document(env,result):return env[0].json(result['plan'])['plan']

def test_complete_autonomous_initial_portfolio(environment):
    result=run(environment);plan=document(environment,result)
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS'
    assert len(plan['decisions'])==len(plan['orders'])==25
    assert all(o['shares']%1000==0 for o in plan['orders'])
    verdict=environment[0].json(result['validation'])
    assert verdict['schema_and_semantics_pass']
    assert 'fixture_input_not_for_submission' in verdict['release_blockers']
    assert 'trading_status_and_corporate_actions_not_verified' in verdict['release_blockers']
    assert all(not x['errors'] for x in verdict['scenarios'])

def test_formula_and_direction_do_not_use_receivables(environment):
    *_,pack,policy,schema,req=environment
    assert target_shares('.1','1000000','37.5')==2000
    assert target_shares('.1','1000000','100')==1000
    decision={'decision_id':'D1','ticker':'1000','action':'BUY','target_weight':.1}
    assert compile_orders([decision],pack,{'1000':Decimal('100')})[0]['shares']==1000000
    decision['action']='TRIM'
    with pytest.raises(ValueError):compile_orders([decision],pack,{'1000':Decimal('100')})

def test_tampering_quotes_references_and_coverage(environment):
    result=run(environment);store,sources,universe,pack,policy,schema,req=environment
    original=document(environment,result);prices=store.json(result['snapshot'])['prices']
    def validate(plan):return validate_plan(plan,schema,pack,prices,universe,TIME,policy,original['observations'],original['sources'])
    assert not validate(original)
    plan=copy.deepcopy(original);plan['orders'][0]['shares']+=1000
    assert 'official_order_formula_mismatch' in validate(plan)
    plan=copy.deepcopy(original);plan['observations'][0]['values']['universe_count']=999
    assert 'observation_lineage_mismatch' in validate(plan)
    plan=copy.deepcopy(original);plan['decisions'][0]['inference_refs']=['I999']
    assert 'broken_reference_chain' in validate(plan)
    plan=copy.deepcopy(original);plan['market_view']['posture']['net_exposure_intent']='reduce'
    assert 'posture_mismatch' in validate(plan)

def test_future_capture_and_pending_account_block(environment):
    store,sources,universe,pack,policy,schema,req=environment
    future=req.model_copy(update={'run_id':'future','cutoff_at':'2026-10-24T07:30:00+08:00'})
    result=generate_candidate(store,future,sources,universe)
    assert result['status']=='BLOCKED_LOCAL_CHECKS'
    assert not list((store.root/'candidates/future').glob('D-Plan_*.json'))
    pending=pack.model_copy(update={'missing':['prev_settlement'],'account':None,'holdings':None})
    req=req.model_copy(update={'run_id':'pending','datapack_ref':store.put(pending.model_dump_json().encode(),'bin')})
    assert generate_candidate(store,req,sources,universe)['status']=='BLOCKED_LOCAL_CHECKS'

def test_resume_and_artifact_integrity(environment):
    partial=run(environment,interrupt_before=['compile']);assert 'report' not in partial
    result=run(environment);assert result['report']==run(environment)['report']
    Path(result['report']).write_text('corrupted')
    with pytest.raises(ValueError,match='hash mismatch'):run(environment)

def test_full_rotation_allows_sixty_orders(environment):
    store,sources,universe,pack,policy,schema,req=environment
    holdings=[{'code':str(1000+i),'shares':100000,'receivable_shares':0,'close_price':str(102+i),'tradable_weight':None} for i in range(30)]
    cash=Decimal(1000000000)-sum(Decimal(h['close_price'])*h['shares'] for h in holdings)
    data=pack.model_dump(mode='json');data.update(as_of_date='2026-10-22',holdings=holdings)
    data['account'].update(cash=str(cash),cash_ratio_tradable=str(cash/Decimal(1000000000)),holdings_count=30)
    changed=DataPack.model_validate(data)
    for source in sources:
        if source.kind!='revenue':continue
        capture=store.select(source.id,TIME);rows=store.json(capture['ref'])
        for row in rows:
            if int(row['公司代號'])<1030:row['營業收入-去年同月增減(%)']='-1'
        store.capture(source.id,encoded(rows),fetched_at=TIME)
    policy=policy.model_copy(update={'holdings':30})
    req=req.model_copy(update={'datapack_ref':store.put(changed.model_dump_json().encode(),'bin'),'policy_ref':store.put_json(policy.model_dump(mode='json'))})
    result=generate_candidate(store,req,sources,universe)
    plan=document((store,sources,universe,changed,policy,schema,req),result)
    assert len(plan['orders'])==len(plan['decisions'])==60
    assert store.json(result['validation'])['schema_and_semantics_pass']

def test_reference_date_and_code_identity_are_bound(environment):
    store,sources,universe,pack,policy,schema,req=environment
    req=req.model_copy(update={'mode':'live','as_of':date(2026,10,21)})
    result=generate_candidate(store,req,sources,universe)
    assert 'official_reference_date_mismatch' in result['errors']
    with pytest.raises(ValueError):generate_candidate(store,req.model_copy(update={'code_hash':'changed'}),sources,universe)

def test_cash_costs_and_zero_delta_are_independently_checked(environment):
    store,sources,universe,pack,policy,schema,req=environment
    state=estimate(pack,[{'ticker':'1000','side':'BUY','shares':1000000}],{'1000':Decimal('100')},policy)
    assert state['cash']==Decimal('899857500')
    assert state['fees']==Decimal('142500')
    updated=pack.model_dump(mode='json')
    updated.update(as_of_date='2026-10-22',holdings=[{'code':'1000','shares':1000000,'receivable_shares':999999,'close_price':100,'tradable_weight':.1}])
    updated['account'].update(cash=900000000,holdings_count=1)
    settled=DataPack.model_validate(updated)
    with pytest.raises(ValueError,match='zero delta'):
        compile_orders([{'decision_id':'D1','ticker':'1000','action':'TRIM','target_weight':.1}],settled,{'1000':100})

def test_percentile_ties_do_not_depend_on_input_order(environment):
    from esun_research.portfolio import rank_candidates
    policy=environment[4]
    rows=[{'code':c,'revenue_yoy_pct':n,'earnings_yield':n,'amount':n} for c,n in [('A','1'),('B','1'),('C','2')]]
    ranked=rank_candidates(rows,policy)
    assert ranked==rank_candidates(list(reversed(rows)),policy)
    assert ranked[0]['code']=='C' and ranked[0]['score']==1
    assert ranked[1]['score']==Decimal('.25')

def test_market_index_is_a_distinct_source(environment):
    store,sources,universe,pack,policy,schema,req=environment
    source=Source(id='index',url='https://openapi.twse.com.tw/v1/indicesReport/MI_5MINS_HIST',provider='TWSE',branch='market',kind='market_index')
    store.capture(source.id,encoded([{'Date':'1151021','OpeningIndex':'100','HighestIndex':'105','LowestIndex':'90','ClosingIndex':'100'},
        {'Date':'1151022','OpeningIndex':'100','HighestIndex':'105','LowestIndex':'90','ClosingIndex':'98'}]),fetched_at=TIME)
    sources=sources+[source]
    req=req.model_copy(update={'registry_hash':digest(encoded([s.model_dump() for s in sources]))})
    result=generate_candidate(store,req,sources,universe)
    plan=document(environment,result)
    assert plan['observations'][0]['values']['taiex_close_return']==-.02
    assert 'market_background_pool_proxy_only' not in store.json(result['validation'])['release_blockers']

def test_policy_changes_have_distinct_release_fingerprints(environment):
    first=run(environment);old=document(environment,first)['agent_metadata']['code_version']
    store,sources,universe,pack,policy,schema,req=environment
    policy=policy.model_copy(update={'cash_target':Decimal('.16')})
    req=req.model_copy(update={'run_id':'changed-policy','policy_ref':store.put_json(policy.model_dump(mode='json'))})
    second=generate_candidate(store,req,sources,universe)
    new=document(environment,second)['agent_metadata']['code_version']
    assert old!=new
