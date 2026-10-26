"""Official-operation evidence is separate from decision qualification and sending."""
import json
from datetime import date
import pytest
from fastapi.testclient import TestClient
from esun_research.application import create_app
from esun_research.candidate import generate_candidate
from esun_research.operations import ReceiptEvent,record_receipt,receipts,operation_status,record_reconciliation
from esun_research.store import encoded,digest
from test_candidate import environment

DOCUMENT=b'%PDF-1.4 test strategy document'
SHA=digest(DOCUMENT)

def build(env,req=None):
    store,sources,universe,*_,original=env
    req=req or original
    result=generate_candidate(store,req,sources,universe)
    return store.json(result['plan'])['plan']

def event(stage,**extra):
    return ReceiptEvent(stage=stage,official_reference='official-history-reference',statement='操作人員已核對官方後台，此處僅記錄操作證據。',**extra)

def test_new_submission_invalidates_previous_confirmation_even_on_same_run(environment):
    store,*_,req=environment;plan=build(environment)
    record_receipt(store,req.run_id,event('upload_checked',validation='serious_error'))
    assert operation_status(store,req.run_id,SHA)['submission']['state']=='not_recorded'
    record_receipt(store,req.run_id,event('submitted'))
    record_receipt(store,req.run_id,event('orders_confirmed',orders=plan['orders']))
    before=operation_status(store,req.run_id,SHA)
    assert before['orders']['state']=='recorded' and before['upload']['event']['event']['validation']=='serious_error'
    assert before['release_blockers'] and not before['submission_performed_by_application']
    record_receipt(store,req.run_id,event('submitted'))
    assert operation_status(store,req.run_id,SHA)['orders']['state']=='invalidated'
    record_receipt(store,req.run_id,event('orders_confirmed',orders=plan['orders']))
    record_receipt(store,req.run_id,event('submission_unknown'))
    state=operation_status(store,req.run_id,SHA)
    assert state['submission']['state']=='unknown' and state['orders']['state']=='invalidated'


def test_last_submission_is_scoped_across_candidates_not_only_one_run(environment):
    store,*_,req=environment;plan=build(environment)
    record_receipt(store,req.run_id,event('submitted'))
    record_receipt(store,req.run_id,event('orders_confirmed',orders=plan['orders']))
    other=req.model_copy(update={'run_id':'other-version'});other_plan=build(environment,other)
    assert plan['orders']==other_plan['orders']
    record_receipt(store,other.run_id,event('submission_unknown'))
    with pytest.raises(ValueError,match='submitted_evidence'):record_receipt(store,req.run_id,event('orders_confirmed',orders=plan['orders']))
    record_receipt(store,other.run_id,event('submitted'))
    state=operation_status(store,req.run_id,SHA)
    assert state['submission']['state']=='superseded' and state['orders']['state']=='invalidated'
    record_receipt(store,other.run_id,event('orders_confirmed',orders=other_plan['orders']))
    assert operation_status(store,other.run_id,SHA)['orders']['state']=='recorded'


def test_other_team_submission_does_not_supersede_this_team(environment):
    store,sources,universe,pack,policy,schema,req=environment;plan=build(environment)
    record_receipt(store,req.run_id,event('submitted'))
    other_pack=pack.model_copy(update={'team_id':'OTHER_TEAM'})
    other=req.model_copy(update={'run_id':'other-team','team_id':'OTHER_TEAM','datapack_ref':store.put(other_pack.model_dump_json().encode(),'bin')})
    build(environment,other);record_receipt(store,other.run_id,event('submission_unknown'))
    record_receipt(store,req.run_id,event('orders_confirmed',orders=plan['orders']))
    assert operation_status(store,req.run_id,SHA)['orders']['state']=='recorded'


def test_strategy_receipt_is_exact_version_and_shared_by_team_not_trade_date(environment):
    store,sources,universe,pack,policy,schema,req=environment;build(environment)
    record_receipt(store,req.run_id,event('submitted'))
    value=event('strategy_submitted',document_sha256=SHA)
    with pytest.raises(ValueError,match='matching_document'):record_receipt(store,req.run_id,value,strategy_document=b'other PDF')
    record_receipt(store,req.run_id,value,strategy_document=DOCUMENT)
    other_pack=pack.model_copy(update={'trade_date':date(2026,10,28)})
    other=req.model_copy(update={'run_id':'next-candidate','trade_date':date(2026,10,28),'datapack_ref':store.put(other_pack.model_dump_json().encode(),'bin')});build(environment,other)
    record_receipt(store,other.run_id,event('submission_unknown'))
    assert operation_status(store,req.run_id,SHA)['submission']['state']=='recorded'
    assert operation_status(store,other.run_id,SHA)['strategy']['state']=='recorded'
    assert operation_status(store,other.run_id,digest(b'new strategy'))['strategy']['state']=='version_mismatch'
    with pytest.raises(ValueError):event('submitted',document_sha256=SHA)
    with pytest.raises(ValueError):event('strategy_submitted')


@pytest.mark.parametrize('damage',['body','middle_deletion','tail_deletion','proof'])
def test_receipt_chain_and_attachments_fail_closed(environment,damage):
    store,*_,req=environment;build(environment)
    first=record_receipt(store,req.run_id,event('submitted'),b'official screen evidence')
    record_receipt(store,req.run_id,event('submission_unknown'))
    if damage=='proof':(store.root/first['proof_ref']).write_bytes(b'changed attachment')
    else:
        with store.connect() as db:
            if damage=='body':db.execute("UPDATE receipt_events SET body=replace(body,'submitted','unknown') WHERE id=1")
            elif damage=='tail_deletion':db.execute('DELETE FROM receipt_events WHERE id=2')
            else:db.execute('DELETE FROM receipt_events WHERE id=1')
    with pytest.raises(ValueError):receipts(store)
    with pytest.raises(ValueError):operation_status(store,req.run_id,SHA)
    with pytest.raises(ValueError):record_receipt(store,req.run_id,event('submitted'))


def test_legacy_receipts_resolve_scope_from_frozen_candidate(environment):
    store,*_,req=environment;build(environment)
    record_receipt(store,req.run_id,event('submitted'))
    with store.connect() as db:
        body=json.loads(db.execute('SELECT body FROM receipt_events').fetchone()[0])
        for key in ['team_id','trade_date']:body.pop(key)
        body['event'].pop('document_sha256')
        db.execute('UPDATE receipt_events SET body=?,hash=?',(encoded(body).decode(),digest(encoded(body))))
        db.execute("DELETE FROM captures WHERE source_id='receipt-ledger-head'")
    assert operation_status(store,req.run_id,SHA)['submission']['state']=='recorded'


def test_reconciliation_keeps_raw_pack_recomputes_and_wait_overrides_old_success(environment):
    store,sources,universe,pack,policy,schema,req=environment;build(environment)
    data=pack.model_dump(mode='json');data.update(trade_date='2026-10-28',as_of_date='2026-10-27')
    data['prev_day_orders'].update(outcome='voided',void_reasons=['official test void'])
    record_reconciliation(store,req.run_id,encoded(data))
    state=operation_status(store,req.run_id,SHA)['settlement']
    assert state['state']=='RECONCILED_SHARES' and state['input_hash_verified']
    assert not state['matches_latest_recorded_submission']
    data['prev_day_orders'].update(outcome='unknown',void_reasons=[])
    record_reconciliation(store,req.run_id,encoded(data))
    assert operation_status(store,req.run_id,SHA)['settlement']['state']=='WAIT_OFFICIAL_OUTCOME'
    c=store.json(store.select('reconciliation:'+req.run_id,'2099-01-01T00:00:00+08:00')['ref'])
    (store.root/c['datapack_ref']).write_bytes(b'changed account input')
    with pytest.raises(ValueError):operation_status(store,req.run_id,SHA)


def test_application_exports_operations_and_downloads_only_bound_verified_proof(environment):
    store,*_,req=environment;build(environment)
    app=create_app(store.root,model_config=None);client=TestClient(app);url='/api/candidates/'+req.run_id
    state=client.get(url+'/operations').json();assert state['submission']['state']=='not_recorded'
    strategy=client.get('/api/documents/ETF_strategy.pdf').content
    value=event('strategy_submitted',document_sha256=digest(strategy))
    files={'event':(None,value.model_dump_json()),'proof':('receipt.txt',b'official portal screenshot','text/plain')}
    assert client.post(url+'/receipts',files=files).status_code==403
    assert client.post(url+'/receipts',files=files,headers={'x-esun-token':app.state.csrf_token}).status_code==200
    state=client.get(url+'/operations').json();assert state['strategy']['state']=='recorded'
    seq=state['strategy']['event']['sequence']
    assert client.get(url+f'/receipts/{seq}/proof').content==b'official portal screenshot'
    assert client.get(url+'/receipts/999/proof').status_code==404
    report=client.get(url+'/operations.json');assert report.status_code==200 and 'attachment' in report.headers['content-disposition']
    assert report.json()['release_blockers'] and report.json()['strategy']['event']['source']=='operator_uploaded_evidence'
