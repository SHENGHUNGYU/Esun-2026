"""Loopback-only operator application; decisions run through the same audited CLI."""
import argparse
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from datetime import date
from pathlib import Path
from fastapi import FastAPI,Request,UploadFile,File,Form,HTTPException
from fastapi.responses import HTMLResponse,FileResponse,JSONResponse,Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel,ConfigDict
from .store import Store,encoded,digest,immutable
from .contracts import now
from .cli import PROJECT,candidate_sources,benchmark_settings
from .datapack import DataPack,load_datapack
from .operations import candidate_bundle,ReceiptEvent,record_receipt,receipts,reconcile
from .benchmarks import import_benchmark

def atomic_write(path,body):
    import tempfile
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as f:
        temporary=Path(f.name);f.write(body);f.flush();os.fsync(f.fileno())
    os.replace(temporary,path)

def process_identity(pid):
    result=subprocess.run(['ps','-p',str(pid),'-o','lstart=','-o','command='],capture_output=True,text=True)
    return result.stdout.strip() if result.returncode==0 else None

class RunInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    datapack_id: str
    llm: bool=True

class ETFCollectionInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    reference_date: date
    pcf_date: date

class Jobs:
    def __init__(self,root):
        self.root=root/'app-jobs';self.root.mkdir(exist_ok=True);self.live={};self.lock=threading.RLock()
    def list(self):
        result=[]
        for path in sorted(self.root.glob('*/job.json'),reverse=True):
            value=json.loads(path.read_bytes());proc=self.live.get(value['id'])
            if proc and proc.poll() is not None and value['state']=='running':
                value.update(state='succeeded' if proc.returncode==0 else 'failed',exit_code=proc.returncode,finished_at=now());atomic_write(path,encoded(value))
            if not proc and value['state']=='running':
                identity=process_identity(value['pid'])
                if identity!=value.get('process_identity') or not identity:
                    manifest=self.root.parent/'candidates'/str(value.get('run_id'))/'manifest.json'
                    value.update(state='completed_after_restart' if manifest.exists() else 'interrupted',finished_at=now())
                    atomic_write(path,encoded(value))
            result.append(value)
        return result
    def start(self,args,kind,run_id=None):
        with self.lock:
            if any(j['state'] in {'running','attention_after_restart'} for j in self.list()):raise ValueError('另一項工作仍在執行或需要確認，請先查看工作紀錄。')
            ident=uuid.uuid4().hex;folder=self.root/ident;folder.mkdir()
            with (folder/'log.txt').open('w') as output:
                proc=subprocess.Popen([sys.executable,'-m','esun_research.cli',*args],cwd=PROJECT,stdout=output,stderr=subprocess.STDOUT,env={**os.environ,'LANGSMITH_TRACING':'false'})
            value={'id':ident,'kind':kind,'run_id':run_id,'state':'running','started_at':now(),'pid':proc.pid,'process_identity':process_identity(proc.pid)}
            atomic_write(folder/'job.json',encoded(value));self.live[ident]=proc
            return value

async def limited(file,limit=25_000_000):
    body=await file.read(limit+1)
    if len(body)>limit:raise HTTPException(413,'檔案過大')
    return body

def create_app(root:Path,model_config:Path|None=PROJECT/'config/llm-local.json',ssh_host=None):
    store=Store(root);jobs=Jobs(store.root);token=uuid.uuid4().hex
    app=FastAPI(title='玉山 Agent 工作台',docs_url=None,redoc_url=None,openapi_url=None)
    app.state.store=store;app.state.jobs=jobs;app.state.csrf_token=token
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=['127.0.0.1','localhost','testserver'])
    @app.middleware('http')
    async def protect(request,call_next):
        if request.method not in {'GET','HEAD'}:
            if request.headers.get('x-esun-token')!=token:return JSONResponse({'detail':'請重新開啟本機工作台後再試。'},status_code=403)
            origin=request.headers.get('origin')
            if origin and origin not in {str(request.base_url).rstrip('/')}:
                return JSONResponse({'detail':'拒絕跨來源請求'},status_code=403)
        response=await call_next(request)
        response.headers['Cache-Control']='no-store'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        response.headers['X-Content-Type-Options']='nosniff'
        return response
    @app.exception_handler(ValueError)
    async def value_error(request,error):return JSONResponse({'detail':str(error)[:300]},status_code=400)
    @app.exception_handler(FileNotFoundError)
    async def missing_file(request,error):return JSONResponse({'detail':'找不到指定資料或執行版本'},status_code=404)
    @app.get('/',response_class=HTMLResponse)
    def home():
        return (Path(__file__).parent/'web/index.html').read_text().replace('__TOKEN__',token)
    @app.get('/api/status')
    def status():
        codes,_=benchmark_settings();sources=[]
        for source in candidate_sources():
            c=store.select(source.id,now());sources.append({'id':source.id,'kind':source.kind,'status':c['status'],'fetched_at':c.get('fetched_at'),'error':c.get('error')})
        runs=[]
        for p in sorted((store.root/'candidates').glob('*/manifest.json'),key=lambda p:p.stat().st_mtime,reverse=True) if (store.root/'candidates').exists() else []:
            m=json.loads(p.read_bytes());runs.append({'run_id':p.parent.name,'status':m['status'],'trade_date':m['request']['trade_date'],'mode':m['request']['mode'],'llm':bool(m['request'].get('llm_ref'))})
        from .issuer_holdings import SUPPORTED
        benchmarks=[]
        for code in codes:
            capture=store.select('ETF:'+code,now());value=store.json(capture['ref'])['benchmark'] if capture.get('status')=='ok' else None
            benchmarks.append({'code':code,'status':capture['status'],'fetched_at':value['fetched_at'] if value else None,
                'valuation_date':value['valuation_date'] if value else None,'equity_count':len(value['holdings']) if value else None,
                'auto_supported':any(code in group for group in SUPPORTED.values())})
        session=json.loads((PROJECT/'config/competition-session.json').read_bytes())
        return {'at':now(),'sources':sources,'source_expected':len(sources),'etf_imported':sum(b['status']=='ok' for b in benchmarks),'etf_expected':30,'benchmarks':benchmarks,
            'first_reference_date':session['first_reference_date'],
            'runs':runs,'jobs':jobs.list(),'receipts':receipts(store),'model_configured':bool(model_config and model_config.exists()),
            'notice':'本機資料與操作紀錄；正式上傳及送出由官方後台完成。'}
    @app.post('/api/datapack')
    async def upload_pack(file:UploadFile=File(...)):
        body=await limited(file,2_000_000);pack=DataPack.model_validate_json(body);key=digest(body)
        folder=store.root/'app-inputs';folder.mkdir(exist_ok=True);immutable(folder/(key+'.json'),body)
        return {'id':key,'team_id':pack.team_id,'trade_date':str(pack.trade_date),'as_of_date':str(pack.as_of_date) if pack.as_of_date else None,
            'gate':pack.decision_gate(),'holdings_count':pack.account.holdings_count if pack.account else None,'nav_tradable':str(pack.account.nav_tradable) if pack.account else None}
    @app.post('/api/collect')
    def collect():
        args=['--root',str(store.root),'ingest','--profile','decision']
        if ssh_host:args+=['--ssh-host',ssh_host]
        return jobs.start(args,'collect')
    @app.post('/api/benchmarks/collect')
    def collect_benchmarks(data:ETFCollectionInput):
        if data.reference_date>date.today() or data.pcf_date<data.reference_date:raise ValueError('請核對評價基準日與PCF適用日')
        args=['--root',str(store.root),'collect-etfs','--reference-date',str(data.reference_date),'--pcf-date',str(data.pcf_date)]
        if ssh_host:args+=['--ssh-host',ssh_host]
        return jobs.start(args,'collect_etfs')
    @app.get('/api/jobs/{ident}/log')
    def job_log(ident):
        if not re.fullmatch(r'[a-f0-9]{32}',ident):raise HTTPException(404)
        return FileResponse(jobs.root/ident/'log.txt',filename='job-log.txt')
    @app.post('/api/candidates')
    def generate(data:RunInput):
        if not re.fullmatch(r'[a-f0-9]{64}',data.datapack_id):raise ValueError('無效資料包識別')
        path=store.root/'app-inputs'/(data.datapack_id+'.json');pack=DataPack.model_validate_json(path.read_bytes())
        if pack.decision_gate().startswith('BLOCKED'):raise ValueError(pack.decision_gate())
        session=json.loads((PROJECT/'config/competition-session.json').read_bytes());reference=str(pack.as_of_date) if pack.as_of_date else session['first_reference_date']
        run_id='run-'+uuid.uuid4().hex[:16]
        args=['--root',str(store.root),'generate-dplan','--run-id',run_id,'--datapack',str(path),'--team-id',pack.team_id,
            '--trade-date',str(pack.trade_date),'--reference-date',reference,'--mode','live']
        if data.llm:
            if not model_config or not model_config.exists():raise ValueError('尚未設定本地模型')
            args+=['--llm-config',str(model_config)]
        return jobs.start(args,'candidate',run_id)
    @app.get('/api/candidates/{run_id}')
    def candidate(run_id):
        folder,manifest=candidate_bundle(store,run_id)
        result={'manifest':manifest,'files':list(manifest['artifacts'])+['manifest.json'],'receipts':receipts(store,run_id)}
        for name,key in [('validation.json','validation'),('active-share.json','active_share'),('projected-account.json','projection')]:
            if name in manifest['artifacts']:result[key]=json.loads((folder/name).read_bytes())
        result['report']=(folder/'report.md').read_text()
        return result
    @app.get('/api/candidates/{run_id}/files/{name}')
    def download(run_id,name):
        folder,manifest=candidate_bundle(store,run_id)
        if name not in manifest['artifacts'] and name!='manifest.json':raise HTTPException(404,'找不到交付檔案')
        return FileResponse(folder/name,filename=name)
    @app.get('/api/documents/{name}')
    def document(name):
        from .deliverables import strategy_pdf,operating_guide_pdf
        if name=='ETF_strategy.pdf':body=strategy_pdf(json.loads((PROJECT/'config/strategy-description.json').read_bytes()))
        elif name=='Operator_guide.pdf':body=operating_guide_pdf()
        else:raise HTTPException(404)
        return Response(body,media_type='application/pdf',headers={'Content-Disposition':'attachment; filename="'+name+'"'})
    @app.get('/api/candidates/{run_id}/handoff.zip')
    def handoff(run_id):
        from .deliverables import strategy_pdf,operating_guide_pdf,handoff_zip
        description=json.loads((PROJECT/'config/strategy-description.json').read_bytes())
        body=handoff_zip(store,run_id,{'ETF_strategy.pdf':strategy_pdf(description),'Operator_guide.pdf':operating_guide_pdf()})
        return Response(body,media_type='application/zip',headers={'Content-Disposition':'attachment; filename="handoff-'+run_id+'.zip"'})
    @app.post('/api/benchmarks')
    async def benchmark(file:UploadFile=File(...),raw:UploadFile=File(...),supporting:list[UploadFile]=File(default=[])):
        codes,hosts=benchmark_settings();extra={}
        if len(supporting)>5:raise HTTPException(413,'補充證據檔案過多')
        for proof in supporting:
            body=await limited(proof);extra[digest(body)]=body
        c=import_benchmark(store,await limited(file,2_000_000),await limited(raw),codes,hosts,extra)
        return {'source_id':c['source_id'],'status':c['status']}
    @app.post('/api/candidates/{run_id}/receipts')
    async def receipt(run_id,event:str=Form(...),proof:UploadFile|None=File(default=None)):
        return record_receipt(store,run_id,ReceiptEvent.model_validate_json(event),await limited(proof) if proof else None)
    @app.post('/api/candidates/{run_id}/reconcile')
    async def reconciliation(run_id,file:UploadFile=File(...)):
        folder,manifest=candidate_bundle(store,run_id);req=manifest['request']
        previous=load_datapack(store.read(req['datapack_ref']),req['team_id'],__import__('datetime').date.fromisoformat(req['trade_date']))
        next_pack=DataPack.model_validate_json(await limited(file,2_000_000))
        plans=[n for n in manifest['artifacts'] if n.startswith('D-Plan_')]
        if len(plans)!=1:raise ValueError('無完整候選可供對帳')
        result=reconcile(previous,json.loads((folder/plans[0]).read_bytes()),next_pack)
        ref=store.put_json(result);store.capture('reconciliation:'+run_id,encoded({'result_ref':ref}))
        return result
    app.mount('/static',StaticFiles(directory=Path(__file__).parent/'web'),name='static')
    return app

def main():
    parser=argparse.ArgumentParser(description='本機 Agent 操作工作台')
    parser.add_argument('--root',type=Path,default=PROJECT/'artifacts/runtime')
    parser.add_argument('--port',type=int,default=8766)
    parser.add_argument('--llm-config',type=Path,default=PROJECT/'config/llm-local.json')
    parser.add_argument('--ssh-host',choices=sorted(__import__('esun_research.gateway',fromlist=['RemoteGateway']).RemoteGateway.ALLOWED_HOSTS))
    args=parser.parse_args()
    import uvicorn
    uvicorn.run(create_app(args.root,args.llm_config,args.ssh_host),host='127.0.0.1',port=args.port,access_log=False)

if __name__=='__main__':main()
