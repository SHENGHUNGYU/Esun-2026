"""Event time semantics and enforcement at the candidate/order boundaries."""
import json
from datetime import date
from pathlib import Path
import pytest
from esun_research.contracts import Source
from esun_research.store import Store, encoded, digest
from esun_research.risk import FEEDS, RiskPolicy, assess, order_errors
from esun_research.candidate import generate_candidate
from test_candidate import environment

ROOT=Path(__file__).resolve().parents[1]
TIME='2026-10-24T08:00:00+08:00'

def setup_risk(tmp_path, payloads=None, cutoff=TIME, trade='2026-10-27'):
    store=Store(tmp_path);sources=[];captures={}
    for sid in FEEDS:
        provider='TWSE' if sid.startswith('TWSE') else 'TPEx'
        source=Source(id=sid,provider=provider,kind='raw',branch='events',url='https://openapi.twse.com.tw/test')
        sources.append(source)
        store.capture(sid,encoded((payloads or {}).get(sid,[])),fetched_at=TIME)
        captures[sid]=store.select(sid,cutoff)
    universe={'2330':{'market':'TWSE'},'3491':{'market':'TPEX'}}
    frozen={'request':{'cutoff_at':cutoff,'trade_date':trade,'as_of':'2026-10-22'},'captures':captures}
    policy=RiskPolicy.model_validate_json((ROOT/'config/trading-risk-policy.json').read_bytes())
    return store,sources,frozen,universe,policy

def test_split_halt_resume_and_duplicate_announcements(tmp_path):
    rows=[{'SecuritiesCompanyCode':'3491','Date':'115','DateOfSuspendedTrading':'1150715','TimeOfSuspendedTrading':'080000','DateOfResumedTrading':'','TimeOfResumedTrading':''},
        {'SecuritiesCompanyCode':'3491','Date':'115','DateOfSuspendedTrading':'','TimeOfSuspendedTrading':'','DateOfResumedTrading':'1150716','TimeOfResumedTrading':'080000'}]
    env=setup_risk(tmp_path,{'TPEx-004':rows+[rows[0]]})
    risk=assess(*env)
    assert risk['securities']['3491']['buy_allowed']
    assert not risk['errors']
    assert 'risk_snapshot_needs_trade_window_refresh' in risk['release_blockers']

def test_halt_future_resume_and_session_boundary(tmp_path):
    def check(resume,clock):
        rows=[{'Code':'2330','TradingHaltDate':'1151027','TradingHaltTime':'080000','TradingResumptionDate':resume,'TradingResumptionTime':clock}]
        return assess(*setup_risk(tmp_path,{'TWSE-063':rows}))['securities']['2330']
    assert not check('1151027','090001')['sell_allowed']
    assert check('1151027','090000')['buy_allowed']
    assert not check('','')['buy_allowed']
    assert not check('garbage','')['buy_allowed']

def test_attention_annotation_disposition_period_and_exdate(tmp_path):
    payload={'TWSE-116':[{'Code':'2330','Date':'1151022'}],
        'TPEx-021':[{'SecuritiesCompanyCode':'3491','Date':'1151016','DispositionPeriod':'115/10/19～115/10/23'}]}
    result=assess(*setup_risk(tmp_path,payload))
    assert all(v['buy_allowed'] for v in result['securities'].values())
    payload['TPEx-021'][0]['DispositionPeriod']='1151026~1151029'
    result=assess(*setup_risk(tmp_path,payload))
    assert not result['securities']['3491']['buy_allowed']
    assert result['securities']['3491']['sell_allowed']
    payload['TWSE-126']=[{'Code':'2330','Date':'1151026'}]
    result=assess(*setup_risk(tmp_path,payload))
    assert not result['securities']['2330']['sell_allowed']
    assert order_errors(result,[{'ticker':'2330','side':'BUY'}])
    payload['TWSE-126'][0]['Date']='1151021'
    assert assess(*setup_risk(tmp_path,payload))['securities']['2330']['buy_allowed']

def test_unknown_formats_never_clear_and_empty_is_distinct_from_error(tmp_path):
    env=setup_risk(tmp_path,{'TWSE-116':[{'Number':'0','Code':'','Name':'','Date':'','TradingInfoForAttention':''}],
        'TPEx-003':[{'Date':'20261024','SecuritiesCompanyCode':'','CompanyName':'','暫停交易':'','恢復交易':''}],
        'TPEx-016':[{'Date':'1151022','SecuritiesCompanyCode':'3491','AlteredTrading':'Ｙ','PeriodicTrading':'','ManagedStock':'','SuspensionOfTrading':'?'}]})
    result=assess(*env)
    assert not result['errors'] and not result['securities']['3491']['buy_allowed']
    assert sum(h['explicit_empty_rows'] for h in result['feeds'])==2
    env[2]['captures']['TWSE-063']['status']='error'
    assert 'risk_feed_unavailable:TWSE-063' in assess(*env)['errors']
    env=setup_risk(tmp_path,{'TWSE-063':[{'nonsense':0}]})
    assert assess(*env)['errors']

def test_staleness_future_publication_and_fresh_window(tmp_path):
    env=setup_risk(tmp_path,{'TWSE-116':[{'Code':'2330','Date':'1151025'}]})
    assert not assess(*env)['securities']['2330']['buy_allowed']
    env=setup_risk(tmp_path,cutoff='2026-10-26T20:00:00+08:00')
    assert len(assess(*env)['errors'])==11
    for sid in FEEDS:
        env[0].capture(sid,encoded([]),fetched_at='2026-10-26T19:31:00+08:00')
        env[2]['captures'][sid]=env[0].select(sid,'2026-10-26T20:00:00+08:00')
    assert 'risk_snapshot_needs_trade_window_refresh' not in assess(*env)['release_blockers']
    assert 'corporate_action_scope_incomplete' in assess(*env)['release_blockers']

def with_risk(env,affected):
    store,sources,universe,pack,policy,schema,req=env
    for sid in FEEDS:
        provider='TWSE' if sid.startswith('TWSE') else 'TPEx'
        sources.append(Source(id=sid,provider=provider,kind='raw',branch='events',url='https://openapi.twse.com.tw/test'))
        rows=([{'Code':affected,'TradingHaltDate':'1151027','TradingHaltTime':'080000','TradingResumptionDate':'','TradingResumptionTime':''}] if sid=='TWSE-063' else [])
        store.capture(sid,encoded(rows),fetched_at=TIME)
    risk=RiskPolicy.model_validate_json((ROOT/'config/trading-risk-policy.json').read_bytes())
    req=req.model_copy(update={'risk_policy_ref':store.put_json(risk.model_dump()),'registry_hash':digest(encoded([s.model_dump() for s in sources]))})
    return store,sources,universe,pack,policy,schema,req

def test_candidate_excludes_before_ranking_and_retains_evidence(environment):
    env=with_risk(environment,'1099');store,sources,universe,pack,policy,schema,req=env
    result=generate_candidate(store,req,sources,universe)
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS'
    plan=store.json(result['plan'])['plan']
    assert all(o['ticker']!='1099' for o in plan['orders'])
    assert store.json(result['validation'])['schema_and_semantics_pass']
    assert len(plan['sources'])==17
    assert (store.root/'candidates'/req.run_id/'trading-risk.json').exists()
    # Risk policy participates in the immutable release fingerprint.
    changed=RiskPolicy.model_validate_json((ROOT/'config/trading-risk-policy.json').read_bytes()).model_copy(update={'attention_blocks_buys':True})
    other=req.model_copy(update={'run_id':'risk-policy-change','risk_policy_ref':store.put_json(changed.model_dump())})
    r2=generate_candidate(store,other,sources,universe)
    assert plan['agent_metadata']['code_version']!=store.json(r2['plan'])['plan']['agent_metadata']['code_version']

def test_held_halt_is_blocked_instead_of_forced_sale(environment):
    env=with_risk(environment,'1000');store,sources,universe,pack,policy,schema,req=env
    data=pack.model_dump(mode='json');data.update(as_of_date='2026-10-22',holdings=[{'code':'1000','shares':1000,'close_price':102,'receivable_shares':0}])
    data['account'].update(cash='999898000',cash_ratio_tradable='.999898',holdings_count=1)
    req=req.model_copy(update={'datapack_ref':store.put_json(data)})
    result=generate_candidate(store,req,sources,universe)
    assert 'held_security_requires_risk_resolution:1000' in result['errors']
    assert not list((store.root/'candidates'/req.run_id).glob('D-Plan_*.json'))

def test_future_halt_disposition_and_unknown_daily_summary(tmp_path):
    payload={'TWSE-063':[{'Code':'2330','TradingHaltDate':'1151028','TradingHaltTime':'080000','TradingResumptionDate':'','TradingResumptionTime':''}],
        'TPEx-021':[{'SecuritiesCompanyCode':'3491','Date':'1151022','DispositionPeriod':'115年10月28日至115年11月02日'}]}
    result=assess(*setup_risk(tmp_path,payload))
    assert all(v['buy_allowed'] for v in result['securities'].values())
    payload['TPEx-003']=[{'Date':'20261024','SecuritiesCompanyCode':'3491','CompanyName':'測試','暫停交易':'今日暫停','恢復交易':''}]
    result=assess(*setup_risk(tmp_path,payload))
    assert not result['securities']['3491']['sell_allowed']
    payload['TPEx-003']=[];payload['TWSE-116']=[{'Number':'0','Code':''}]
    assert assess(*setup_risk(tmp_path,payload))['errors']

def test_cli_decision_profile_has_all_risk_feeds():
    from esun_research.cli import candidate_sources,settings
    decision=candidate_sources();research,_=settings()
    assert len(decision)==18 and set(FEEDS)<={s.id for s in decision}
    assert len(research)==15
