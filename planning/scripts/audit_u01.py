"""Read-only U01 inventory. No credentials, trades, installs or model downloads."""
from pathlib import Path
import argparse, csv, hashlib, json, re, subprocess, shutil, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'units/U01/evidence'
def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--network',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(ZoneInfo('Asia/Taipei')).isoformat()
    sources=[]
    for p in sorted((ROOT.parent/'docs').iterdir()):
        if p.is_file() and not p.name.startswith('.'):
            sources.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    old=json.loads((ROOT/'source-manifest.json').read_text())
    assert {Path(x['path']).name:x['sha256'] for x in old}=={x['file']:x['sha256'] for x in sources}, 'source changed: review before updating manifest'
    stocks=[];market=None;page=0
    for line in (ROOT/'sources/玉山挑戰賽 投資組合 150檔清單.txt').read_text().splitlines():
        if line.startswith('--- PAGE'): page=int(re.search(r'\d+',line)[0])
        if '【上市】' in line:market='TWSE'
        if '【上櫃】' in line:market='TPEX'
        if re.match(r'^\d{4}\s',line):
            for code,name in re.findall(r'(\d{4})\s+([^\s]+)',line): stocks.append({'code':code,'name':name,'market':market,'source_page':page})
    assert len(stocks)==len({s['code'] for s in stocks})==150
    assert sum(s['market']=='TWSE' for s in stocks)==100
    assert sum(s['market']=='TPEX' for s in stocks)==50
    etfs=[{'code':m[1],'name':m[2].strip(),'source_page':1} for m in re.finditer(r'^(\d{5}A)\s+(.+)$',(ROOT/'sources/玉山挑戰賽 主動型ETF列表 v1.txt').read_text(),re.M)]
    assert len(etfs)==len({e['code'] for e in etfs})==30
    for filename,rows in [('universe.csv',stocks),('active-etfs.csv',etfs)]:
        with (OUT/filename).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    save('sources.json',{'checked_at':stamp,'unchanged':True,'files':sources,'stocks':150,'listed':100,'otc':50,'etfs':30})
    hardware={'checked_at':stamp}
    for key,cmd in [('architecture',['uname','-m']),('cpu',['sysctl','-n','machdep.cpu.brand_string']),('memory_bytes',['sysctl','-n','hw.memsize'])]:
        p=subprocess.run(cmd,capture_output=True,text=True);hardware[key]={'value':p.stdout.strip(),'returncode':p.returncode}
    hardware['tools']={t:bool(shutil.which(t)) for t in ['python3','uv','ollama','nvidia-smi','ssh','node']}
    try:
        with urllib.request.urlopen('http://127.0.0.1:11434/api/tags',timeout=3) as r:
            d=json.load(r);hardware['ollama']={'status':r.status,'models':[{'name':x.get('name'),'size':x.get('size')} for x in d.get('models',[])]}
    except Exception as e:hardware['ollama']={'error_type':type(e).__name__,'status':'unreachable'}
    save('hardware.json',hardware)
    if args.network:
        probes=[]
        for name,url in [('organizer','https://esun-ai-challenge.tw/'),('twse','https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'),('tpex','https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes'),('tej_docs','https://api.tej.com.tw/')]:
            item={'name':name,'url':url,'checked_at':stamp,'authenticated':False}
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'Esun-U01-resource-audit/1.0'})
                with urllib.request.urlopen(req,timeout=20) as r:
                    raw=r.read();item.update(status=r.status,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),content_type=r.headers.get('Content-Type'))
                    try:
                        d=json.loads(raw)
                        if isinstance(d,list):
                            item.update(records=len(d),fields=list(d[0]) if d else [],dates=sorted({str(x.get('Date','')) for x in d}))
                            codekey='Code' if name=='twse' else 'SecuritiesCompanyCode'
                            expected={s['code'] for s in stocks if s['market']==('TWSE' if name=='twse' else 'TPEX')}
                            if name in ('twse','tpex'): item['missing_whitelist_codes']=sorted(expected-{str(x.get(codekey,'')) for x in d})
                        else:item['json_type']=type(d).__name__
                    except ValueError:
                        item['html_title']=re.findall(r'<title[^>]*>(.*?)</title>',raw.decode('utf-8','replace'),re.S)[:1]
            except Exception as e:item.update(error_type=type(e).__name__,status=getattr(e,'code',None))
            probes.append(item)
        history=OUT/'public-connectivity.json'
        previous=json.loads(history.read_text()) if history.exists() else []
        save('public-connectivity.json',previous+probes)
    print(json.dumps({'sources':len(sources),'stocks':len(stocks),'etfs':len(etfs),'evidence':str(OUT)},ensure_ascii=False))
if __name__=='__main__':main()
