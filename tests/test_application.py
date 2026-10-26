import copy
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from esun_research.application import create_app
from esun_research.operations import ReceiptEvent,record_receipt,receipts,reconcile
from esun_research.candidate import generate_candidate
from esun_research.datapack import DataPack
from test_candidate import environment


def test_loopback_application_imports_only_valid_pack_and_blocks_cross_origin(environment):
    store,sources,universe,pack,policy,schema,req=environment
    app=create_app(store.root,model_config=None);client=TestClient(app)
    page=client.get('/');assert page.status_code==200 and '本機' in page.text
    assert 'frame-ancestors' in page.headers['content-security-policy']
    body={'file':('account.json',pack.model_dump_json(),'application/json')}
    assert client.post('/api/datapack',files=body).status_code==403
    auth={'x-esun-token':app.state.csrf_token}
    response=client.post('/api/datapack',files=body,headers=auth);assert response.status_code==200
    assert response.json()['gate']=='INITIAL_CASH_ACCOUNT'
    assert client.post('/api/datapack',files=body,headers={**auth,'origin':'https://evil.test'}).status_code==403
    assert client.get('/',headers={'host':'evil.test'}).status_code==400
    assert client.get('/api/candidates/unknown').status_code==404
    assert client.get('/api/status').json()['model_configured'] is False
    assert client.post('/api/candidates',json={'datapack_id':'../../secrets'},headers=auth).status_code==400


def test_history_workspace_downloads_only_verified_aggregate_and_preserves_dataset(tmp_path,monkeypatch):
    from test_history import FixtureGateway
    from esun_research.history import collect_history,dataset_folder
    from esun_research.store import Store,digest
    history=Store(tmp_path/'history-data')
    result=collect_history(history,{'2330':{'market':'TWSE'}},'2026-09','2026-09',FixtureGateway())
    app=create_app(tmp_path/'app',model_config=None,history_root=history.root);client=TestClient(app)
    state=client.get('/api/history').json()
    assert state['dataset']['fixed'] and state['progress']['strict_pit_verified'] is False
    assert state['dataset']['start_month']=='2026-09' and '績效' in state['scope']
    response=client.get('/api/history/files/daily-prices.parquet')
    assert response.status_code==200 and digest(response.content)==result['parquet_sha256']
    assert client.get('/api/history/files/request.json').status_code==404
    auth={'x-esun-token':app.state.csrf_token}
    monkeypatch.setattr(app.state.jobs,'start',lambda *args:{'id':'new-period'})
    assert client.post('/api/history/collect',json={'start_month':'2026-08','end_month':'2026-09'},headers=auth).status_code==200
    (dataset_folder(history.root,'2026-09','2026-09')/'daily-prices.parquet').write_bytes(b'tampered')
    assert client.get('/api/history/files/daily-prices.parquet').status_code==400


def test_history_progress_does_not_confuse_stale_file_with_live_writer(tmp_path,monkeypatch):
    import fcntl
    from esun_research.store import encoded
    archive=tmp_path/'archive';(archive/'history').mkdir(parents=True)
    (archive/'history/request.json').write_bytes(encoded({'start':'2026-04','end':'2026-09'}))
    (archive/'history/progress.json').write_bytes(encoded({'status':'RUNNING'}))
    app=create_app(tmp_path/'app',model_config=None,history_root=archive);client=TestClient(app)
    assert client.get('/api/history').json()['progress']['status']=='INTERRUPTED'
    monkeypatch.setattr(app.state.jobs,'start',lambda *a:pytest.fail('duplicate history worker started'))
    with (archive/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        state=client.get('/api/history').json();assert state['active_writer'] and state['progress']['status']=='RUNNING'
        response=client.post('/api/history/collect',json={'start_month':'2026-04','end_month':'2026-09'},headers={'x-esun-token':app.state.csrf_token})
        assert response.status_code==400


def test_receipt_states_do_not_send_or_claim_orders_confirmation(environment):
    store,sources,universe,pack,policy,schema,req=environment
    result=generate_candidate(store,req,sources,universe);plan=store.json(result['plan'])['plan']
    confirmed=ReceiptEvent(stage='orders_confirmed',official_reference='r1',statement='已逐筆核對官方當日委託股數與方向。',orders=plan['orders'])
    with pytest.raises(ValueError):record_receipt(store,req.run_id,confirmed)
    checked=ReceiptEvent(stage='upload_checked',validation='warned',official_reference='check',statement='已完成官方上傳檢核，尚未按下送出。')
    event=record_receipt(store,req.run_id,checked,b'official receipt screenshot')
    assert event['proof_ref'] and event['event']['stage']=='upload_checked'
    assert len(receipts(store,req.run_id))==1
    with pytest.raises(ValueError):record_receipt(store,req.run_id,confirmed)
    record_receipt(store,req.run_id,ReceiptEvent(stage='submitted',official_reference='submission1',statement='已在歷史紀錄確認本版正式繳交。'))
    record_receipt(store,req.run_id,confirmed)
    assert len(receipts(store,req.run_id))==3
    bad=ReceiptEvent.model_validate({**confirmed.model_dump(),'orders':plan['orders'][:-1]})
    with pytest.raises(ValueError):record_receipt(store,req.run_id,bad)
    record_receipt(store,req.run_id,ReceiptEvent(stage='submission_unknown',official_reference='timeout',statement='後續重新送出的結果尚未從後台確認。'))
    with pytest.raises(ValueError,match='submitted_evidence'):record_receipt(store,req.run_id,confirmed)


def test_order_confirmation_rejects_coerced_or_fractional_shares():
    base={'stage':'orders_confirmed','official_reference':'checked','statement':'已從官方當日委託畫面逐筆抄錄。'}
    for quantity in [True,'1000',1000.9,1001,-1000]:
        with pytest.raises(ValueError):ReceiptEvent(**base,orders=[{'ticker':'2330','side':'BUY','shares':quantity}])


def test_unknown_official_outcome_is_not_completed_reconciliation(environment):
    store,sources,universe,pack,policy,schema,req=environment
    result=generate_candidate(store,req,sources,universe);plan=store.json(result['plan'])['plan']
    data=pack.model_dump(mode='json');data.update(trade_date='2026-10-28',as_of_date='2026-10-27')
    data['prev_day_orders']['outcome']='unknown'
    report=reconcile(pack,plan,DataPack.model_validate(data))
    assert report['status']=='WAIT_OFFICIAL_OUTCOME' and report['outcome']=='unknown'


def test_partial_execution_reconciles_official_shares_and_distinguishes_notices(environment):
    store,sources,universe,pack,policy,schema,req=environment
    result=generate_candidate(store,req,sources,universe);plan=store.json(result['plan'])['plan'];projection=store.json(result['plan'])['projected']
    data=pack.model_dump(mode='json');excluded=plan['orders'][0]['ticker'];positions={c:int(n) for c,n in projection['positions'].items() if c!=excluded}
    prices=store.json(result['snapshot'])['prices'];nav=1000000000;value=sum(float(prices[c])*n for c,n in positions.items());cash=nav-value
    data.update(trade_date='2026-10-28',as_of_date='2026-10-27',holdings=[{'code':c,'shares':n,'receivable_shares':0,'close_price':prices[c]} for c,n in positions.items()])
    data['account'].update(cash=cash,nav_tradable=nav,aum=nav,cash_ratio_tradable=cash/nav,holdings_count=len(positions))
    data['prev_day_orders'].update(outcome='executed',excluded_codes=[excluded])
    data['compliance'].update(notices=2,violations=0)
    next_pack=DataPack.model_validate(data);report=reconcile(pack,plan,next_pack)
    assert report['status']=='RECONCILED_SHARES' and report['official_violations']==0 and report['official_notices']==2
    data['holdings'][0]['shares']-=1000;data['account']['cash']+=float(prices[data['holdings'][0]['code']])*1000
    assert reconcile(pack,plan,DataPack.model_validate(data))['status']=='REQUIRES_REVIEW'
    pending=next_pack.model_copy(update={'missing':['prev_settlement'],'as_of_date':None,'account':None,'holdings':None})
    assert reconcile(pack,plan,pending)['status']=='WAIT_OFFICIAL_INPUT'


def test_agent_mode_requires_model_and_research_inputs_before_launch(environment,monkeypatch):
    store,sources,universe,pack,policy,schema,req=environment
    app=create_app(store.root);client=TestClient(app);auth={'x-esun-token':app.state.csrf_token}
    loaded=client.post('/api/datapack',files={'file':('pack.json',pack.model_dump_json(),'application/json')},headers=auth).json()
    body={'datapack_id':loaded['id'],'decision_engine':'llm_agent','llm':False}
    assert client.post('/api/candidates',json=body,headers=auth).status_code==400
    body['llm']=True
    assert client.post('/api/candidates',json=body,headers=auth).status_code==400
    assert client.get('/api/research-inputs?reference_date=2026-10-22').json()['status']=='NOT_STARTED'
    folder=store.root/'agent-inputs';folder.mkdir();(folder/'research-data-2026-10-22.json').write_text('{}')
    seen=[]
    monkeypatch.setattr(app.state.jobs,'start',lambda args,kind,run_id:(seen.append(args) or {'run_id':run_id}))
    response=client.post('/api/candidates',json=body,headers=auth)
    assert response.status_code==200
    assert seen[0][seen[0].index('--decision-engine')+1]=='llm_agent'
    assert '--research-data' in seen[0] and '--llm-config' in seen[0]
