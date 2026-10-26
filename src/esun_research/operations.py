"""Receipt evidence and official settlement reconciliation, without a send transport."""
import json
import sqlite3
from pathlib import Path
from pydantic import BaseModel,ConfigDict,Field,StrictInt,model_validator
from typing import Literal
from .contracts import now,instant
from .store import encoded,digest

class ConfirmedOrder(BaseModel):
    model_config=ConfigDict(extra='forbid')
    ticker: str=Field(pattern=r'^[0-9]{4,6}$')
    side: Literal['BUY','SELL']
    shares: StrictInt=Field(gt=0)
    decision_ref: str | None=None

    @model_validator(mode='after')
    def whole_lot(self):
        if self.shares%1000:raise ValueError('official_order_requires_whole_lot')
        return self

class ReceiptEvent(BaseModel):
    model_config=ConfigDict(extra='forbid')
    stage: Literal['upload_checked','submitted','submission_unknown','orders_confirmed','strategy_submitted']
    validation: Literal['passed','warned','serious_error','failed','skipped'] | None = None
    official_reference: str = Field(min_length=1,max_length=200)
    statement: str = Field(min_length=10,max_length=1200)
    orders: list[ConfirmedOrder] | None = Field(default=None,max_length=60)
    document_sha256: str | None = Field(default=None,pattern=r'^[a-f0-9]{64}$')

    @model_validator(mode='after')
    def separate_axes(self):
        if self.stage!='orders_confirmed' and self.orders is not None:raise ValueError('orders_only_belong_to_confirmation')
        if (self.stage=='strategy_submitted')!=(self.document_sha256 is not None):raise ValueError('strategy_document_hash_required_only_for_strategy_receipt')
        return self

def candidate_bundle(store,run_id):
    import re
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('invalid_run_id')
    folder=store.root/'candidates'/run_id
    manifest=json.loads((folder/'manifest.json').read_bytes())
    for name,sha in manifest['artifacts'].items():
        path=folder/name
        if not path.resolve().is_relative_to(folder) or digest(path.read_bytes())!=sha:raise ValueError('candidate_artifact_hash_mismatch')
    return folder,manifest

def _receipt_rows(store,db):
    anchor=db.execute("SELECT ref FROM captures WHERE source_id='receipt-ledger-head' ORDER BY id DESC LIMIT 1").fetchone()
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='receipt_events'").fetchone():
        if anchor:raise ValueError('receipt_history_integrity_failed')
        return []
    rows=[];previous={}
    for ident,run_id,body,sha in db.execute('SELECT id,run_id,body,hash FROM receipt_events ORDER BY id'):
        value=json.loads(body)
        if digest(encoded(value))!=sha or value.get('run_id')!=run_id or value.get('previous_event_hash')!=previous.get(run_id):
            raise ValueError('receipt_history_integrity_failed')
        if value.get('proof_ref'):store.read(value['proof_ref'])
        previous[run_id]=sha;rows.append({**value,'event_hash':sha,'sequence':ident})
    if anchor:
        head=store.json(anchor[0])
        if not rows or (head['sequence'],head['event_hash'])!=(rows[-1]['sequence'],rows[-1]['event_hash']):
            raise ValueError('receipt_history_integrity_failed')
    return rows

def _scoped_rows(store,rows,request):
    """Use immutable candidate identity, including for receipts predating scope fields."""
    scopes={};result=[]
    for row in rows:
        rid=row['run_id']
        if rid not in scopes:
            _,manifest=candidate_bundle(store,rid);scopes[rid]=manifest
        manifest=scopes[rid];req=manifest['request']
        plans=[n for n in manifest['artifacts'] if n.startswith('D-Plan_') and n.endswith('.json')]
        if len(plans)!=1 or row['plan_hash']!=manifest['artifacts'][plans[0]]:raise ValueError('receipt_candidate_binding_mismatch')
        if row.get('team_id',req['team_id'])!=req['team_id'] or row.get('trade_date',req['trade_date'])!=req['trade_date']:
            raise ValueError('receipt_scope_mismatch')
        if req['team_id']==request['team_id']:result.append((row,req['trade_date']))
    return result

def record_receipt(store,run_id,event,evidence=None,strategy_document=None):
    folder,manifest=candidate_bundle(store,run_id)
    plans=[n for n in manifest['artifacts'] if n.startswith('D-Plan_') and n.endswith('.json')]
    if len(plans)!=1:raise ValueError('a_locally_validated_candidate_is_required')
    plan=json.loads((folder/plans[0]).read_bytes());plan_hash=manifest['artifacts'][plans[0]]
    if event.stage=='upload_checked' and event.validation is None:raise ValueError('validation_result_required')
    if event.stage!='upload_checked' and event.validation is not None:raise ValueError('validation_axis_belongs_to_upload_event')
    if event.stage=='strategy_submitted' and (not strategy_document or digest(strategy_document)!=event.document_sha256):
        raise ValueError('strategy_receipt_requires_matching_document')
    if event.stage=='orders_confirmed':
        signature=lambda rows:sorted((str(r['ticker']),r['side'],int(r['shares'])) for r in rows)
        if event.orders is None or signature(event.model_dump()['orders'])!=signature(plan['orders']):raise ValueError('official_orders_do_not_match_candidate')
    proof_ref=store.put(evidence,'bin') if evidence else None
    with store.connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS receipt_events(id INTEGER PRIMARY KEY,run_id TEXT,body TEXT,hash TEXT UNIQUE)')
        db.execute('BEGIN IMMEDIATE')
        history=_receipt_rows(store,db);scoped=_scoped_rows(store,history,manifest['request'])
        previous=[h for h in history if h['run_id']==run_id]
        submissions=[h for h,d in scoped if d==manifest['request']['trade_date'] and h['event']['stage'] in {'submitted','submission_unknown'}]
        if event.stage=='orders_confirmed' and (not submissions or submissions[-1]['event']['stage']!='submitted' or submissions[-1]['run_id']!=run_id):
            raise ValueError('submitted_evidence_required_before_orders_confirmation')
        body={'at':now(),'run_id':run_id,'plan_hash':plan_hash,'team_id':manifest['request']['team_id'],'trade_date':manifest['request']['trade_date'],
            'event':event.model_dump(),'proof_ref':proof_ref,
            'source':'operator_uploaded_evidence' if evidence else 'operator_attestation','previous_event_hash':previous[-1]['event_hash'] if previous else None,
            'note':'This records evidence of a portal operation; no upload or submission was performed by this application.'}
        sha=digest(encoded(body));insert=db.execute('INSERT INTO receipt_events(run_id,body,hash) VALUES(?,?,?)',(run_id,encoded(body).decode(),sha))
        anchor=store.put_json({'sequence':insert.lastrowid,'event_hash':sha})
        db.execute('INSERT INTO captures(source_id,fetched_at,epoch,status,ref,error) VALUES(?,?,?,?,?,?)',
            ('receipt-ledger-head',body['at'],instant(body['at']).timestamp(),'ok',anchor,None))
    return {**body,'event_hash':sha}

def receipts(store,run_id=None):
    with store.connect() as db:
        db.execute('BEGIN')  # Read head and rows from one snapshot while another request appends.
        rows=_receipt_rows(store,db)
    return [r for r in rows if run_id is None or r['run_id']==run_id]

def operation_status(store,run_id,strategy_sha256):
    folder,manifest=candidate_bundle(store,run_id);request=manifest['request']
    rows=receipts(store);scoped=_scoped_rows(store,rows,request)
    own=[h for h,d in scoped if h['run_id']==run_id]
    checked=[h for h in own if h['event']['stage']=='upload_checked']
    submitted=[h for h,d in scoped if d==request['trade_date'] and h['event']['stage'] in {'submitted','submission_unknown'}]
    latest=submitted[-1] if submitted else None
    submit_state='not_recorded'
    if latest:submit_state='unknown' if latest['event']['stage']=='submission_unknown' else ('recorded' if latest['run_id']==run_id else 'superseded')
    confirmations=[h for h in own if h['event']['stage']=='orders_confirmed']
    confirmed=bool(submit_state=='recorded' and confirmations and confirmations[-1]['sequence']>latest['sequence'])
    strategies=[h for h,d in scoped if h['event']['stage']=='strategy_submitted']
    strategy=strategies[-1] if strategies else None
    strategy_state='not_recorded' if not strategy else ('recorded' if strategy['event']['document_sha256']==strategy_sha256 else 'version_mismatch')
    validation=json.loads((folder/'validation.json').read_bytes())
    settlement=None;capture=store.select('reconciliation:'+run_id,now())
    if capture['status']=='ok':
        envelope=store.json(capture['ref'])
        if envelope.get('schema')=='reconciliation-evidence-1':
            if envelope['run_id']!=run_id or envelope['request_hash']!=digest(encoded(request)):raise ValueError('reconciliation_candidate_binding_mismatch')
            previous,plan=_reconciliation_inputs(store,folder,manifest)
            from .datapack import DataPack
            expected=reconcile(previous,plan,DataPack.model_validate_json(store.read(envelope['datapack_ref'])))
            if envelope['result']!=expected:raise ValueError('reconciliation_evidence_mismatch')
            settlement={'state':expected['status'],'result':expected,'recorded_at':envelope['at'],'input_hash_verified':True,
                'matches_latest_recorded_submission':submit_state=='recorded' and confirmed}
    return {'at':now(),'run_id':run_id,'team_id':request['team_id'],'trade_date':request['trade_date'],
        'candidate_status':manifest['status'],'candidate_errors':validation.get('errors',[]),'release_blockers':validation.get('release_blockers',[]),
        'upload':{'state':'recorded' if checked else 'not_recorded','event':checked[-1] if checked else None},
        'submission':{'state':submit_state,'event':latest},
        'orders':{'state':'recorded' if confirmed else ('invalidated' if confirmations else 'not_recorded'),'event':confirmations[-1] if confirmations else None},
        'strategy':{'state':strategy_state,'document_sha256':strategy_sha256,'event':strategy},
        'settlement':settlement or {'state':'not_recorded','input_hash_verified':False},
        'receipts_integrity_verified':True,'submission_performed_by_application':False,
        'note':'Operator evidence is not independently verified portal acceptance. Frozen candidate blockers remain unchanged; recorded submission, order matching, execution and compliance are separate.'}

def _reconciliation_inputs(store,folder,manifest):
    from datetime import date
    from .datapack import load_datapack
    req=manifest['request']
    previous=load_datapack(store.read(req['datapack_ref']),req['team_id'],date.fromisoformat(req['trade_date']))
    plans=[n for n in manifest['artifacts'] if n.startswith('D-Plan_') and n.endswith('.json')]
    if len(plans)!=1:raise ValueError('a_locally_validated_candidate_is_required')
    return previous,json.loads((folder/plans[0]).read_bytes())

def record_reconciliation(store,run_id,datapack_body):
    from .datapack import DataPack
    folder,manifest=candidate_bundle(store,run_id)
    previous,plan=_reconciliation_inputs(store,folder,manifest)
    result=reconcile(previous,plan,DataPack.model_validate_json(datapack_body))
    evidence={'schema':'reconciliation-evidence-1','at':now(),'run_id':run_id,'request_hash':digest(encoded(manifest['request'])),
        'datapack_ref':store.put(datapack_body),'result':result}
    store.capture('reconciliation:'+run_id,encoded(evidence))
    return result

def reconcile(previous_pack,plan,next_pack):
    if previous_pack.team_id!=next_pack.team_id:raise ValueError('reconciliation_team_mismatch')
    gate=next_pack.decision_gate()
    if gate.startswith('BLOCKED'):
        return {'status':'WAIT_OFFICIAL_OUTCOME' if gate=='BLOCKED_UNKNOWN_ORDER_OUTCOME' else 'WAIT_OFFICIAL_INPUT',
            'gate':gate,'outcome':next_pack.prev_day_orders.outcome}
    if next_pack.as_of_date!=previous_pack.trade_date:raise ValueError('next_pack_does_not_settle_candidate_trade_date')
    outcome=next_pack.prev_day_orders.outcome
    old={h.code:h.shares for h in previous_pack.holdings if h.shares>0};expected=dict(old)
    exclusions=set(next_pack.prev_day_orders.excluded_codes);order_codes={o['ticker'] for o in plan['orders']}
    problems=[]
    if not exclusions<=order_codes:problems.append('excluded_code_not_in_candidate')
    if outcome=='executed':
        for order in plan['orders']:
            if order['ticker'] not in exclusions:expected[order['ticker']]=expected.get(order['ticker'],0)+(1 if order['side']=='BUY' else -1)*order['shares']
    expected={c:n for c,n in expected.items() if n>0};actual={h.code:h.shares for h in next_pack.holdings if h.shares>0}
    differences=[{'code':c,'expected_shares':expected.get(c,0),'official_shares':actual.get(c,0)} for c in sorted(set(expected)|set(actual)) if expected.get(c,0)!=actual.get(c,0)]
    if differences:problems.append('share_difference_requires_corporate_action_or_order_review')
    if next_pack.compliance.violations<previous_pack.compliance.violations:problems.append('official_violation_counter_regressed')
    fail_days=sorted({i.date.isoformat() for i in next_pack.compliance.incidents if i.status=='fail'})
    return {'status':'RECONCILED_SHARES' if not problems else 'REQUIRES_REVIEW','outcome':outcome,'excluded_codes':sorted(exclusions),
        'void_reasons':next_pack.prev_day_orders.void_reasons,'differences':differences,'problems':problems,
        'official_account':next_pack.account.model_dump(mode='json'),'official_violations':next_pack.compliance.violations,
        'official_notices':next_pack.compliance.notices,'fail_incident_dates':fail_days,
        'note':'Official account/holdings remain truth. warn/notices do not add violation days; no assumed fill prices or fee rounding. Share reconciliation alone does not prove NAV attribution.'}
