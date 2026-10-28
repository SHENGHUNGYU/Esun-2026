"""Resumable daily preparation. Official account truth never depends on inferred submission."""
import fcntl
import json
import re
import subprocess
import sys
from pathlib import Path
from .contracts import now
from .datapack import DataPack
from .store import Store, digest, encoded, immutable
from .operations import candidate_bundle, _reconciliation_inputs, reconcile


def review_previous(store, pack):
    comparisons=[]; unreadable=[]
    if pack.as_of_date:
        for path in sorted((store.root/'candidates').glob('*/manifest.json')):
            try:
                manifest=json.loads(path.read_bytes());req=manifest['request']
                if req['team_id']!=pack.team_id or req['trade_date']!=str(pack.as_of_date) or req['mode']!='live':continue
                if not any(n.startswith('D-Plan_') for n in manifest['artifacts']):continue
                folder,manifest=candidate_bundle(store,path.parent.name)
                previous,plan=_reconciliation_inputs(store,folder,manifest)
                result=reconcile(previous,plan,pack)
                comparisons.append({'run_id':path.parent.name,'plan_sha256':next(sha for name,sha in manifest['artifacts'].items() if name.startswith('D-Plan_') and name.endswith('.json')),
                    'reconciliation':result,'official_submission_verified':False})
            except (ValueError,KeyError,OSError) as error:
                unreadable.append({'run_id':path.parent.name,'error':str(error)[:200]})
    return {'settlement_date':str(pack.as_of_date) if pack.as_of_date else None,
        'next_trade_date':str(pack.trade_date),'comparisons':comparisons,'unreadable_candidates':unreadable,
        'note':'Local candidate comparisons are not submission receipts. Official DataPack holdings remain authoritative; no P&L attribution is inferred.'}


def daily_context(pack, review):
    return {'official_account':pack.account.model_dump(mode='json'),
        'official_holdings':[h.model_dump(mode='json') for h in pack.holdings],
        'previous_order_outcome':pack.prev_day_orders.model_dump(mode='json'),
        'compliance':pack.compliance.model_dump(mode='json'),
        'settlement_date':str(pack.as_of_date) if pack.as_of_date else None,
        'matching_local_candidates':[r['run_id'] for r in review['comparisons'] if r['reconciliation']['status']=='RECONCILED_SHARES'],
        'submission_verified':False,'performance_attribution_verified':False}


def failure_detail(store,run_id,error):
    folder=store.root/'candidates'/run_id
    validation=folder/'validation.json'
    codes=json.loads(validation.read_bytes()).get('errors',[]) if validation.exists() else []
    calls=folder/'agent-call-evidence.json'
    evidence=json.loads(calls.read_bytes()) if calls.exists() else []
    if any('Connection refused' in (c.get('error') or '') for c in evidence):
        return '模型通道未連線（Connection refused）；資料已備妥，尚未進入策略評估。請恢復通道後建立新版本。'
    if codes:return '候選驗證未通過：'+', '.join(codes)
    if isinstance(error,subprocess.CalledProcessError):return '此階段工作失敗，請查看工作紀錄中的底層錯誤。'
    return str(error)[:500]


def run_daily(root, datapack, run_id, model_config, history_root, ssh_host=None, runner=None):
    from .cli import PROJECT, code_hash
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('invalid_run_id')
    store=Store(Path(root));body=Path(datapack).read_bytes();pack=DataPack.model_validate_json(body)
    if pack.decision_gate().startswith('BLOCKED'):raise ValueError(pack.decision_gate())
    session=json.loads((PROJECT/'config/competition-session.json').read_bytes())
    reference=str(pack.as_of_date) if pack.as_of_date else session['first_reference_date']
    folder=store.root/'daily-runs'/run_id;folder.mkdir(parents=True,exist_ok=True)
    request={'datapack_sha256':digest(body),'trade_date':str(pack.trade_date),'reference_date':reference,
        'code_hash':code_hash(),'model_config_sha256':digest(Path(model_config).read_bytes()),
        'history_root':str(Path(history_root).resolve()),'ssh_host':ssh_host}
    with (folder/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        immutable(folder/'request.json',encoded(request));immutable(folder/'datapack.json',body)
        if not (folder/'review.json').exists():
            review=review_previous(store,pack);immutable(folder/'review.json',encoded(review))
            immutable(folder/'context.json',encoded(daily_context(pack,review)))
        state_path=folder/'progress.json'
        state=json.loads(state_path.read_bytes()) if state_path.exists() else {'run_id':run_id,'completed_steps':[]}
        def save(status, **extra):
            from .application import atomic_write
            state.update(status=status,updated_at=now(),**extra);atomic_write(state_path,encoded(state))
            print(json.dumps(state,ensure_ascii=False),flush=True)
        def execute(args):
            subprocess.run([sys.executable,'-m','esun_research.cli','--root',str(store.root),*args],cwd=PROJECT,check=True)
        execute=runner or execute
        remote=['--ssh-host',ssh_host] if ssh_host else []
        steps=[('decision_data',['ingest','--profile','decision','--reference-date',reference,*remote]),
            ('news',['ingest','--profile','research',*remote]),
            ('research_factors',['collect-agent-data','--reference-date',reference,'--history-root',str(history_root)]),
            ('generate',['generate-dplan','--run-id',run_id,'--datapack',str(folder/'datapack.json'),
                '--team-id',pack.team_id,'--trade-date',str(pack.trade_date),'--reference-date',reference,'--mode','live',
                '--decision-engine','llm_agent','--llm-config',str(model_config),
                '--research-data',str(store.root/'agent-inputs'/('research-data-'+reference+'.json'))])]
        for name,args in steps:
            if name in state['completed_steps']:continue
            save('RUNNING',step=name,error=None)
            if name=='generate' and (store.root/'candidates'/run_id/'request.json').exists():
                args=['resume-dplan','--run-id',run_id]
            try:execute(args)
            except Exception as error:
                save('BLOCKED',error=failure_detail(store,run_id,error));raise
            state['completed_steps'].append(name);save('RUNNING')
        candidate_folder,manifest=candidate_bundle(store,run_id)
        if manifest['status']!='CANDIDATE_BLOCKED_EXTERNAL_CHECKS':
            save('BLOCKED',error='candidate_local_validation_failed');raise ValueError('candidate_local_validation_failed')
        save('LOCAL_CANDIDATE_READY',candidate_status=manifest['status'],official_submission_performed=False)
        return state
