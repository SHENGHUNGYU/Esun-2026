import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from esun_research.application import create_app
from esun_research.daily import run_daily,review_previous
from esun_research.datapack import DataPack
from esun_research.candidate import generate_candidate
from test_candidate import environment


def test_daily_uses_official_dates_and_stops_then_resumes(environment,monkeypatch):
    store,sources,universe,pack,policy,schema,req=environment
    data=pack.model_dump(mode='json');data.update(trade_date='2026-11-02',as_of_date='2026-10-30')
    path=store.root/'pack.json';path.write_text(json.dumps(data))
    config=store.root/'model.json';config.write_text('{}')
    calls=[]
    def fail(args):
        calls.append(args)
        if args[0]=='collect-agent-data':raise RuntimeError('source unavailable')
    with pytest.raises(RuntimeError):run_daily(store.root,path,'daily-test',config,store.root/'history',runner=fail)
    state=json.loads((store.root/'daily-runs/daily-test/progress.json').read_bytes())
    assert state['status']=='BLOCKED' and state['completed_steps']==['decision_data','news']
    assert not any(a[0]=='generate-dplan' for a in calls)
    monkeypatch.setattr('esun_research.daily.candidate_bundle',lambda *a:(None,{'status':'CANDIDATE_BLOCKED_EXTERNAL_CHECKS'}))
    calls.clear()
    result=run_daily(store.root,path,'daily-test',config,store.root/'history',runner=calls.append)
    assert result['status']=='LOCAL_CANDIDATE_READY'
    assert [a[0] for a in calls]==['collect-agent-data','generate-dplan']
    args=calls[-1];assert args[args.index('--trade-date')+1]=='2026-11-02'
    assert args[args.index('--reference-date')+1]=='2026-10-30'
    assert '--llm-config' in args and '--research-data' in args
    calls.clear();run_daily(store.root,path,'daily-test',config,store.root/'history',runner=calls.append)
    assert calls==[]
    config.write_text('{"changed":true}')
    with pytest.raises(ValueError,match='Immutable'):run_daily(store.root,path,'daily-test',config,store.root/'history',runner=calls.append)


def test_daily_rejects_unknown_account_before_work(environment):
    store,sources,universe,pack,policy,schema,req=environment
    data=pack.model_dump(mode='json');data.update(as_of_date='2026-10-27',trade_date='2026-10-28')
    data['prev_day_orders']['outcome']='unknown'
    path=store.root/'pack.json';path.write_text(json.dumps(data))
    with pytest.raises(ValueError,match='UNKNOWN_ORDER'):
        run_daily(store.root,path,'blocked',Path('absent-model'),store.root,runner=lambda a:pytest.fail('should not run'))


def test_previous_candidate_review_does_not_claim_submission(environment):
    store,sources,universe,pack,policy,schema,req=environment
    # Fixture candidates must never be inferred as yesterday's live submission.
    generate_candidate(store,req,sources,universe)
    data=pack.model_dump(mode='json');data.update(as_of_date='2026-10-27',trade_date='2026-10-28')
    review=review_previous(store,DataPack.model_validate(data))
    assert review['comparisons']==[]


def test_daily_api_derives_dates_and_requires_llm(environment,monkeypatch):
    store,sources,universe,pack,policy,schema,req=environment
    app=create_app(store.root);client=TestClient(app);auth={'x-esun-token':app.state.csrf_token}
    loaded=client.post('/api/datapack',files={'file':('pack.json',pack.model_dump_json(),'application/json')},headers=auth).json()
    body={'datapack_id':loaded['id'],'decision_engine':'llm_agent','llm':True}
    monkeypatch.setattr(app.state.model_connection,'ensure',lambda:None)
    seen=[];monkeypatch.setattr(app.state.jobs,'start',lambda args,kind,run_id:seen.append((args,kind,run_id)) or {'run_id':run_id})
    response=client.post('/api/daily-cycle',json=body,headers=auth)
    assert response.status_code==200 and seen[0][1]=='daily_cycle'
    assert '--reference-date' not in seen[0][0] and '--trade-date' not in seen[0][0]
    assert client.post('/api/daily-cycle',json={**body,'llm':False},headers=auth).status_code==400
    assert client.post('/api/daily-cycle',json={**body,'datapack_id':'../bad'},headers=auth).status_code==400
