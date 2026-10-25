#!/usr/bin/env python3
"""Continuous local service monitoring; never submits or invokes inference.

This measures availability and restarts, not full decision quality or GPU load.
The journal contains counts and fingerprints only, never account/response data.
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import httpx

def stamp():
    return datetime.now(timezone.utc).isoformat()

def local_url(value):
    p=urlparse(value)
    if p.scheme!='http' or p.hostname not in {'127.0.0.1','localhost','::1'} or p.username or p.password or p.query or p.fragment or p.path not in {'','/'}:
        raise ValueError('Only loopback service origins are allowed')
    return value.rstrip('/')

def probe(client,app_url,model_url,model,digest):
    try:
        page=client.get(app_url+'/');page.raise_for_status()
        status=client.get(app_url+'/api/status');status.raise_for_status();body=status.json()
        match=re.search(r'<meta name="esun-token" content="([a-f0-9]{32})">',page.text)
        if not match or not isinstance(body['sources'],list) or not isinstance(body['runs'],list):
            raise ValueError('invalid_application_response')
        policy=page.headers.get('content-security-policy','')
        if "frame-ancestors 'none'" not in policy or page.headers.get('cache-control')!='no-store':
            raise ValueError('missing_application_protections')
        tags=client.get(model_url+'/api/tags');tags.raise_for_status()
        identities=[m for m in tags.json()['models'] if m.get('name')==model]
        if len(identities)!=1 or identities[0].get('digest')!=digest:
            raise ValueError('model_identity_mismatch')
        return {'healthy':True,'application_boot':hashlib.sha256(match[1].encode()).hexdigest(),
            'official_sources_ok':sum(r['status']=='ok' for r in body['sources']),
            'etfs_imported':body['etf_imported'],'candidate_count':len(body['runs']),
            'model_identity_verified':True}
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        return {'healthy':False,'error':'service_probe_failed','model_identity_verified':False}

def advance(state,result,delta,interval):
    state=dict(state);state['samples']+=1;state['monitored_seconds']+=delta
    restarted=bool(result.get('application_boot') and state.get('application_boot') and result['application_boot']!=state['application_boot'])
    if restarted:state['application_restarts']+=1
    if not result['healthy'] or delta>interval*2.5 or restarted:
        state['healthy_seconds']=0
    elif state.get('previous_healthy'):
        state['healthy_seconds']+=delta
    state['previous_healthy']=result['healthy']
    if not result['healthy']:state['failed_samples']+=1
    if result.get('application_boot'):state['application_boot']=result['application_boot']
    state['longest_healthy_seconds']=max(state['longest_healthy_seconds'],state['healthy_seconds'])
    return state

def save(path,state):
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as f:
        f.write(json.dumps(state,ensure_ascii=False,indent=2).encode());f.flush();os.fsync(f.fileno());tmp=Path(f.name)
    os.replace(tmp,path)

def main():
    parser=argparse.ArgumentParser(description='本機工作台與模型服務持續監測，不執行推論或送出')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--app-url',default='http://127.0.0.1:8766')
    parser.add_argument('--model-config',type=Path,default=Path(__file__).resolve().parents[1]/'config/llm-local.json')
    parser.add_argument('--hours',type=float,default=72)
    parser.add_argument('--interval',type=float,default=60)
    args=parser.parse_args()
    if not 0<args.hours<=168 or not 5<=args.interval<=300:parser.error('Invalid monitor duration or interval')
    app_url=local_url(args.app_url);config=json.loads(args.model_config.read_bytes());model_url=local_url(config['base_url'])
    binding={'app_url':app_url,'model_url':model_url,'model':config['model'],'digest':config['digest'],
        'hours':args.hours,'interval':args.interval,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    root=args.output.resolve();root.mkdir(parents=True,exist_ok=True);path=root/'progress.json'
    with (root/'monitor.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if path.exists():
            state=json.loads(path.read_bytes())
            if state['binding']!=binding:raise ValueError('Monitor configuration changed; use a new output directory')
            state.update(healthy_seconds=0,previous_healthy=False,monitor_restarts=state['monitor_restarts']+1)
        else:
            state={'binding':binding,'started_at':stamp(),'samples':0,'failed_samples':0,'application_restarts':0,
                'monitor_restarts':0,'monitored_seconds':0.,'healthy_seconds':0.,'longest_healthy_seconds':0.,'previous_healthy':False}
        state['scope']='Application availability + model identity; no inference, ingestion, submission or 72-hour decision-quality certification.'
        state['status']='RUNNING';previous=time.monotonic()
        try:
            with httpx.Client(timeout=10,follow_redirects=False,trust_env=False) as client, (root/'samples.jsonl').open('a') as journal:
                while state['healthy_seconds']<args.hours*3600 and state['monitored_seconds']<(args.hours+6)*3600:
                    result=probe(client,app_url,model_url,config['model'],config['digest']);current=time.monotonic()
                    state=advance(state,result,current-previous,args.interval);previous=current
                    sample={'at':stamp(),**result,'healthy_seconds':state['healthy_seconds']}
                    journal.write(json.dumps(sample,ensure_ascii=False)+'\n');journal.flush();os.fsync(journal.fileno())
                    state['last_sample_at']=sample['at'];save(path,state)
                    if state['healthy_seconds']>=args.hours*3600:break
                    time.sleep(args.interval)
            state['status']='PASSED_AVAILABILITY_ONLY' if state['healthy_seconds']>=args.hours*3600 else 'INCOMPLETE'
        except KeyboardInterrupt:
            state['status']='STOPPED'
        finally:
            state['updated_at']=stamp();save(path,state)
        print(json.dumps({'status':state['status'],'samples':state['samples'],'healthy_seconds':state['healthy_seconds']}))

if __name__=='__main__':main()
