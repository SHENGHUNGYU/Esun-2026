"""Receipt evidence and official settlement reconciliation, without a send transport."""
import json
import sqlite3
from pathlib import Path
from pydantic import BaseModel,ConfigDict,Field,StrictInt,model_validator
from typing import Literal
from .contracts import now
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
    stage: Literal['upload_checked','submitted','submission_unknown','orders_confirmed']
    validation: Literal['passed','warned','serious_error','failed','skipped'] | None = None
    official_reference: str = Field(min_length=1,max_length=200)
    statement: str = Field(min_length=10,max_length=1200)
    orders: list[ConfirmedOrder] | None = Field(default=None,max_length=60)

def candidate_bundle(store,run_id):
    import re
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('invalid_run_id')
    folder=store.root/'candidates'/run_id
    manifest=json.loads((folder/'manifest.json').read_bytes())
    for name,sha in manifest['artifacts'].items():
        path=folder/name
        if not path.resolve().is_relative_to(folder) or digest(path.read_bytes())!=sha:raise ValueError('candidate_artifact_hash_mismatch')
    return folder,manifest

def record_receipt(store,run_id,event,evidence=None):
    folder,manifest=candidate_bundle(store,run_id)
    plans=[n for n in manifest['artifacts'] if n.startswith('D-Plan_') and n.endswith('.json')]
    if len(plans)!=1:raise ValueError('a_locally_validated_candidate_is_required')
    plan=json.loads((folder/plans[0]).read_bytes());plan_hash=manifest['artifacts'][plans[0]]
    if event.stage=='upload_checked' and event.validation is None:raise ValueError('validation_result_required')
    if event.stage!='upload_checked' and event.validation is not None:raise ValueError('validation_axis_belongs_to_upload_event')
    if event.stage=='orders_confirmed':
        signature=lambda rows:sorted((str(r['ticker']),r['side'],int(r['shares'])) for r in rows)
        if event.orders is None or signature(event.model_dump()['orders'])!=signature(plan['orders']):raise ValueError('official_orders_do_not_match_candidate')
    proof_ref=store.put(evidence,'bin') if evidence else None
    with store.connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS receipt_events(id INTEGER PRIMARY KEY,run_id TEXT,body TEXT,hash TEXT UNIQUE)')
        db.execute('BEGIN IMMEDIATE')
        previous=db.execute('SELECT body,hash FROM receipt_events WHERE run_id=? ORDER BY id DESC LIMIT 1',(run_id,)).fetchone()
        history=[json.loads(r[0]) for r in db.execute('SELECT body FROM receipt_events WHERE run_id=? ORDER BY id',(run_id,))]
        submissions=[h for h in history if h['event']['stage'] in {'submitted','submission_unknown'} and h['plan_hash']==plan_hash]
        if event.stage=='orders_confirmed' and (not submissions or submissions[-1]['event']['stage']!='submitted'):raise ValueError('submitted_evidence_required_before_orders_confirmation')
        body={'at':now(),'run_id':run_id,'plan_hash':plan_hash,'event':event.model_dump(),'proof_ref':proof_ref,
            'source':'operator_uploaded_evidence' if evidence else 'operator_attestation','previous_event_hash':previous[1] if previous else None,
            'note':'This records evidence of a portal operation; no upload or submission was performed by this application.'}
        sha=digest(encoded(body));db.execute('INSERT INTO receipt_events(run_id,body,hash) VALUES(?,?,?)',(run_id,encoded(body).decode(),sha))
    return {**body,'event_hash':sha}

def receipts(store,run_id=None):
    with store.connect() as db:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='receipt_events'").fetchone():return []
        rows=db.execute('SELECT body,hash FROM receipt_events'+(' WHERE run_id=?' if run_id else '')+' ORDER BY id', (run_id,) if run_id else ()).fetchall()
    return [{**json.loads(body),'event_hash':sha} for body,sha in rows]

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
