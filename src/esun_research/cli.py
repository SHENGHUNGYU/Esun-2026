"""Read-only collection and reproducible research commands."""
import argparse
import csv
import fcntl
import json
import os
from pathlib import Path
from .contracts import Source, RunRequest, now, instant
from .store import Store, digest, encoded
from .gateway import Gateway, RemoteGateway, ingest

PROJECT = Path(__file__).resolve().parents[2]

def settings():
    sources = [Source.model_validate(s) for s in json.loads((PROJECT/'config/sources.json').read_text()) if s['enabled']]
    with (PROJECT/'planning/units/U01/evidence/universe.csv').open() as f:
        rows = list(csv.DictReader(f))
    universe = {r['code']:r for r in rows}
    if len(rows)!=150 or len(universe)!=150:
        raise ValueError('Expected 150 unique competition securities')
    return sources, universe

def code_hash():
    files=sorted((PROJECT/'src/esun_research').glob('*.py'))+[PROJECT/'uv.lock']
    return digest(encoded({str(p.relative_to(PROJECT)):digest(p.read_bytes()) for p in files}))

def candidate_sources(include_research=False):
    from .risk import FEEDS
    return [Source.model_validate(s).model_copy(update={'kind':'market_index'}) if s['id']=='TWSE-067' else Source.model_validate(s)
        for s in json.loads((PROJECT/'config/sources.json').read_text())
        if s['id']!='TWSE-043' and (s['kind'] in {'quotes','valuation','revenue'} or s['id']=='TWSE-067' or s['id'] in FEEDS
        or (include_research and s['enabled'] and s['kind'] in {'rss','announcements'}))]

def benchmark_settings():
    from urllib.parse import urlparse
    with (PROJECT/'planning/units/U01/evidence/active-etfs.csv').open() as f:
        codes=[r['code'] for r in csv.DictReader(f)]
    if len(codes)!=30 or len(set(codes))!=30:raise ValueError('Expected 30 unique official benchmarks')
    inventory=json.loads((PROJECT/'planning/api-research/etf-source-inventory.json').read_bytes())
    hosts={urlparse(r['official_url']).hostname for r in inventory['items']}
    # Official files may be served by another documented issuer subdomain.
    hosts.update({'www.fhtrust.com.tw','vpx.fhtrust.com.tw','www.capitalfund.com.tw','www.kgifund.com.tw','www.megafunds.com.tw','sitc.sinopac.com','websys.fsit.com.tw','webapi.alliancebernstein.com'})
    return codes,hosts

def main():
    os.environ['LANGSMITH_TRACING']='false'
    parser=argparse.ArgumentParser(description='第一階段：公開資料快照與離線研究')
    parser.add_argument('--root',type=Path,default=PROJECT/'artifacts')
    sub=parser.add_subparsers(dest='command',required=True)
    collection=sub.add_parser('ingest',help='抓取已啟用的官方端點與中央社 RSS')
    collection.add_argument('--ssh-host',choices=sorted(RemoteGateway.ALLOWED_HOSTS))
    collection.add_argument('--reference-date',help='官方DataPack指定的行情基準日 YYYY-MM-DD')
    collection.add_argument('--profile',choices=['research','decision'],default='research')
    pack=sub.add_parser('check-datapack',help='本地驗證官方帳戶資料包，不產生或送出委託')
    pack.add_argument('--file',type=Path,required=True)
    pack.add_argument('--team-id',required=True)
    pack.add_argument('--trade-date',required=True)
    bench=sub.add_parser('import-etf',help='驗證並匯入投信實際股票持股表及對應原始檔')
    bench.add_argument('--file',type=Path,required=True)
    bench.add_argument('--raw',type=Path,required=True)
    bench.add_argument('--supporting-raw',type=Path,action='append',default=[])
    issuer_collection=sub.add_parser('collect-etfs',help='更新已驗證的投信官方完整持股；不用FinMind')
    issuer_collection.add_argument('--reference-date',required=True)
    issuer_collection.add_argument('--pcf-date',required=True)
    issuer_collection.add_argument('--ssh-host',choices=sorted(RemoteGateway.ALLOWED_HOSTS))
    historical=sub.add_parser('collect-history',help='下載官方歷史價量並驗收單位／覆蓋；不宣稱歷史原始版本或策略績效')
    historical.add_argument('--start-month',required=True)
    historical.add_argument('--end-month',required=True)
    agent_data=sub.add_parser('collect-agent-data',help='收集並回源驗證LLM研究用歷史技術及逐股法人資料')
    agent_data.add_argument('--reference-date',required=True)
    agent_data.add_argument('--history-root',type=Path,default=PROJECT/'artifacts/history-202604-202609')
    run=sub.add_parser('research',help='使用截止時間以前已取得的快照')
    run.add_argument('--run-id',required=True)
    run.add_argument('--as-of',required=True,help='預期行情日 YYYY-MM-DD')
    run.add_argument('--cutoff',default=None,help='含時區的 ISO 時間，預設現在')
    run.add_argument('--model')
    run.add_argument('--model-url',default='http://127.0.0.1:8000/v1')
    decision=sub.add_parser('generate-dplan',help='自主產生本地 D-Plan 候選，不連線提交')
    decision.add_argument('--run-id',required=True)
    decision.add_argument('--datapack',type=Path,required=True)
    decision.add_argument('--team-id',required=True)
    decision.add_argument('--trade-date',required=True)
    decision.add_argument('--reference-date',required=True)
    decision.add_argument('--mode',choices=['live','fixture'],required=True)
    decision.add_argument('--cutoff')
    decision.add_argument('--policy',type=Path,default=PROJECT/'config/baseline-policy.json')
    decision.add_argument('--risk-policy',type=Path,default=PROJECT/'config/trading-risk-policy.json')
    decision.add_argument('--llm-config',type=Path,help='本地模型設定；啟用後必須通過模型與引用驗證')
    decision.add_argument('--decision-engine',choices=['baseline','llm_agent'],default='baseline')
    decision.add_argument('--agent-settings',type=Path,default=PROJECT/'config/strategy-agent.json')
    decision.add_argument('--research-data',type=Path,help='由資料工具建立並可回源驗證的研究因子bundle')
    resume=sub.add_parser('resume-dplan',help='依已封存參數恢復本地候選，不重抓資料')
    resume.add_argument('--run-id',required=True)
    daily=sub.add_parser('daily-cycle',help='依官方結算更新資料並產生下一交易日候選，不正式送出')
    daily.add_argument('--run-id',required=True)
    daily.add_argument('--datapack',type=Path,required=True)
    daily.add_argument('--llm-config',type=Path,required=True)
    daily.add_argument('--history-root',type=Path,required=True)
    daily.add_argument('--ssh-host',choices=sorted(RemoteGateway.ALLOWED_HOSTS))
    args=parser.parse_args()
    if args.command=='daily-cycle':
        from .daily import run_daily
        run_daily(args.root,args.datapack,args.run_id,args.llm_config,args.history_root,args.ssh_host)
        return
    sources,universe=settings()
    store=Store(args.root)
    with (store.root/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if args.command=='ingest':
            if args.profile=='decision':sources=candidate_sources()
            sources=[s for s in sources if s.id!='TWSE-DATED-QUOTES' or args.reference_date]
            gateway=RemoteGateway(args.ssh_host) if args.ssh_host else Gateway()
            try:result=ingest(store,sources,gateway,{'TWSE-DATED-QUOTES':{'reference_date':args.reference_date}} if args.reference_date else None)
            finally:gateway.close()
            print(json.dumps(result,ensure_ascii=False,indent=2))
        elif args.command=='check-datapack':
            from datetime import date
            from .datapack import load_datapack
            body=args.file.read_bytes()
            official=load_datapack(body,args.team_id,date.fromisoformat(args.trade_date))
            gate=official.decision_gate()
            print(json.dumps({'gate':gate,'schema_version':official.schema_version,
                'team_id':official.team_id,'trade_date':official.trade_date.isoformat(),
                'sha256':digest(body),'official_server_validation':False},ensure_ascii=False))
            if gate.startswith('BLOCKED'):raise SystemExit(2)
        elif args.command=='collect-agent-data':
            from .agent_data import collect_bundle
            path,result=collect_bundle(store,universe,args.reference_date,args.history_root)
            print(json.dumps({'file':str(path),'cells':len(result['cells']),'gaps':len(result['missing'])},ensure_ascii=False))
        elif args.command=='collect-history':
            from .history import HistoricalGateway,collect_history
            gateway=HistoricalGateway()
            try:result=collect_history(store,universe,args.start_month,args.end_month,gateway,
                progress=lambda row:print(json.dumps(row,ensure_ascii=False),flush=True))
            finally:gateway.close()
            print(json.dumps({'status':result['status'],'successful_months':result['successful_months'],
                'requests':result['expected_requests'],'rows':result['normalized_rows'],'strict_pit_verified':False}))
            if result['status']!='COMPLETE':raise SystemExit(2)
        elif args.command=='collect-etfs':
            from .issuer_holdings import collect
            codes,hosts=benchmark_settings()
            result=collect(store,args.reference_date,args.pcf_date,codes,hosts,args.ssh_host)
            print(json.dumps(result,ensure_ascii=False,indent=2))
            if any(x['status']=='error' for x in result):raise SystemExit(2)
        elif args.command=='import-etf':
            from .benchmarks import import_benchmark
            codes,hosts=benchmark_settings()
            supporting={digest(body):body for p in args.supporting_raw if (body:=p.read_bytes())}
            capture=import_benchmark(store,args.file.read_bytes(),args.raw.read_bytes(),codes,hosts,supporting)
            print(json.dumps({'status':capture['status'],'source_id':capture['source_id'],'ref':capture['ref']}))
        elif args.command in {'generate-dplan','resume-dplan'}:
            from .candidate import DecisionRequest,generate_candidate
            if args.command=='resume-dplan':
                # Validate the run identifier before joining it into a path.
                import re
                if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}',args.run_id):
                    raise ValueError('Invalid run identifier')
                saved=json.loads((store.root/'candidates'/args.run_id/'request.json').read_bytes())
                request=DecisionRequest.model_validate(saved['request'])
                sources=candidate_sources(request.decision_engine=='llm_agent')
                if request.code_hash!=code_hash():raise ValueError('Code changed; create a new candidate run')
            else:
                from .portfolio import Policy
                from .risk import RiskPolicy
                from .llm import ModelConfig
                sources=candidate_sources(args.decision_engine=='llm_agent')
                if args.decision_engine=='llm_agent' and not args.llm_config:raise ValueError('LLM主導流程必須指定本地模型設定')
                body=args.datapack.read_bytes()
                capture=store.capture('DataPack:'+args.team_id+':'+args.trade_date,body)
                cutoff=args.cutoff or now()
                if instant(cutoff)>instant(now()):raise ValueError('Cutoff cannot be in the future')
                available=store.select(capture['source_id'],cutoff)
                if available.get('ref')!=capture['ref']:raise ValueError('Requested DataPack was not captured before cutoff')
                policy=Policy.model_validate_json(args.policy.read_bytes())
                benchmark_codes,_=benchmark_settings()
                benchmark_refs=[c['ref'] for code in benchmark_codes if (c:=store.select('ETF:'+code,cutoff)).get('status')=='ok']
                previous_strategy_ref=None;holding_memory_ref=None
                if args.decision_engine=='llm_agent':
                    from .turnover import previous_strategy
                    from .datapack import load_datapack
                    from datetime import date
                    prior=previous_strategy(store,load_datapack(body,args.team_id,date.fromisoformat(args.trade_date)),cutoff)
                    previous_strategy_ref=store.put_json(prior)
                    from .holding_ledger import remember_pack,review_memory
                    pack_for_memory=load_datapack(body,args.team_id,date.fromisoformat(args.trade_date))
                    remember_pack(store,body,available['first_seen_at'])
                    holding_memory_ref=store.put_json(review_memory(store,pack_for_memory,cutoff))
                request=DecisionRequest(run_id=args.run_id,cutoff_at=cutoff,as_of=args.reference_date,
                    team_id=args.team_id,trade_date=args.trade_date,mode=args.mode,
                    datapack_ref=capture['ref'],datapack_seen_at=available['first_seen_at'],
                    policy_ref=store.put_json(policy.model_dump(mode='json')),
                    risk_policy_ref=store.put_json(RiskPolicy.model_validate_json(args.risk_policy.read_bytes()).model_dump(mode='json')),
                    llm_ref=store.put_json(ModelConfig.model_validate_json(args.llm_config.read_bytes()).model_dump(mode='json')) if args.llm_config else None,
                    benchmark_universe_ref=store.put_json(benchmark_codes),benchmark_refs=benchmark_refs,
                    decision_engine=args.decision_engine,
                    agent_settings_ref=store.put_json(__import__('esun_research.research_tools',fromlist=['AgentSettings']).AgentSettings.model_validate_json(args.agent_settings.read_bytes()).model_dump()) if args.decision_engine=='llm_agent' else None,
                    previous_strategy_ref=previous_strategy_ref,holding_memory_ref=holding_memory_ref,
                    research_data_ref=store.put_json(json.loads(args.research_data.read_bytes())) if args.research_data and args.decision_engine=='llm_agent' else None,
                    schema_ref=store.put_json(json.loads((PROJECT/'docs/official-2026-10-24/D-Plan.schema_v4.3.json').read_bytes())),
                    session_ref=store.put_json(json.loads((PROJECT/'config/competition-session.json').read_bytes())),
                    universe_hash=digest(encoded(universe)),registry_hash=digest(encoded([s.model_dump() for s in sources])),code_hash=code_hash())
            result=generate_candidate(store,request,sources,universe)
            print(json.dumps({'status':result['status'],'report':result['report']},ensure_ascii=False))
            if result['status']=='BLOCKED_LOCAL_CHECKS':raise SystemExit(2)
        else:
            from .workflow import research, LocalModel
            cutoff=args.cutoff or now()
            if instant(cutoff)>instant(now()):
                raise ValueError('Cutoff cannot be in the future')
            request=RunRequest(run_id=args.run_id,as_of=args.as_of,cutoff_at=cutoff,
                universe_hash=digest(encoded(universe)),
                registry_hash=digest(encoded([s.model_dump() for s in sources])),
                code_hash=code_hash(),model=args.model,model_url=args.model_url if args.model else None)
            result=research(store,request,sources,universe,LocalModel(args.model,args.model_url) if args.model else None)
            print(json.dumps({'status':result['status'],'report':result['report']},ensure_ascii=False))

if __name__=='__main__':
    main()
