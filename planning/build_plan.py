"""Build the read-only plan site from DAILY_TODO.md. Never updates acceptance."""
from pathlib import Path
import json, re, shutil, subprocess
from build_data_catalog import build_catalog
from build_api_catalog import build_apis
ROOT=Path(__file__).resolve().parent
STATUSES={'待開始','待討論確認','進行中','受阻','待驗收','已完成'}
SECTIONS={'討論問題':'discussion','你的任務':'human','Codex 任務':'codex','機器任務':'machine','驗收條件':'acceptance','證據':'evidence','阻礙':'blockers','你需準備':'preparation','回覆欄位':'reply_fields'}
def public_doc_sources():
    # Server inventory and connection evidence stay local even on the private site.
    result=[(p.name,p) for p in sorted(ROOT.glob('*.md')) if not p.name.upper().startswith('SERVER')]
    result.append(('17-competition-readiness.md',ROOT/'rounds/R02_PLAN.md'))
    result.append(('20-etf-source-readiness.md',ROOT/'api-research/etf-holdings-readiness-2026-10-24.md'))
    result.append(('23-etf-acquisition.md',ROOT/'api-research/etf-acquisition-2026-10-26.md'))
    result.append(('24-history-feasibility.md',ROOT/'api-research/history-feasibility-2026-10-26.md'))
    return result

def parse_todo(text):
    blocks=re.split(r'^## (U\d{2}) (.+)\n',text,flags=re.M)
    tasks=[]
    for n in range(1,len(blocks),3):
        uid,title,body=blocks[n:n+3]
        meta=dict(re.findall(r'^- (階段|狀態|前置依賴|清單確認|驗收確認)：(.+)$',body,re.M))
        if set(meta)!={'階段','狀態','前置依賴','清單確認','驗收確認'}:raise ValueError(f'{uid}: missing metadata')
        task={'id':uid,'day':int(uid[1:]),'title':title,'phase':meta['階段'],'status':meta['狀態'],'deps':re.findall(r'U\d{2}',meta['前置依賴']),'list_confirmed':meta['清單確認'],'acceptance_confirmed':meta['驗收確認']}
        if task['status'] not in STATUSES:raise ValueError(f'{uid}: invalid status')
        sections=re.split(r'^### (.+)\n',body,flags=re.M)
        for i in range(1,len(sections),2):
            name=sections[i]
            if name not in SECTIONS:raise ValueError(f'{uid}: unknown section {name}')
            values=re.findall(r'^- (.+)$',sections[i+1],re.M)
            if not values:raise ValueError(f'{uid}: empty {name}')
            task[SECTIONS[name]]=values
        if not all(x in task for x in SECTIONS.values()):raise ValueError(f'{uid}: missing section')
        fields=[]
        for row in task['reply_fields']:
            parts=row.split('｜')
            if len(parts)!=3 or not re.fullmatch(r'[a-z][a-z0-9_]*',parts[0]) or not all(parts):raise ValueError(f'{uid}: invalid reply field')
            fields.append(dict(zip(['key','label','hint'],parts)))
        if len({f['key'] for f in fields})!=len(fields):raise ValueError(f'{uid}: duplicate reply field')
        task['reply_fields']=fields

        if task['status'] in {'進行中','受阻','待驗收','已完成'} and task['list_confirmed']=='未確認':raise ValueError(f'{uid}: list not confirmed')
        if task['status']=='已完成' and task['acceptance_confirmed']=='未確認':raise ValueError(f'{uid}: acceptance not confirmed')
        tasks.append(task)
    if [t['id'] for t in tasks]!=[f'U{i:02}' for i in range(1,15)]:raise ValueError('expected U01–U14 exactly once in order')
    lookup={t['id']:t for t in tasks}
    for t in tasks:
        if len(t['deps'])!=len(set(t['deps'])) or any(d not in lookup or lookup[d]['day']>=t['day'] for d in t['deps']):raise ValueError(f"{t['id']}: invalid dependency")
        if t['day']>1 and f"U{t['day']-1:02}" not in t['deps']:raise ValueError(f"{t['id']}: preceding unit required")
        if t['status'] in {'進行中','待驗收','已完成'} and any(lookup[d]['status']!='已完成' for d in t['deps']):raise ValueError(f"{t['id']}: dependency not accepted")
    return tasks

def build():
    catalog=build_catalog()
    apis=build_apis()
    tasks=parse_todo((ROOT/'DAILY_TODO.md').read_text())
    (ROOT/'plan.json').write_text(json.dumps({'source':'DAILY_TODO.md','units':14,'timezone':'Asia/Taipei','human_hours_per_day':'2–3','tasks':tasks},ensure_ascii=False,indent=2)+'\n')
    md='# 兩週工作單元路線圖（自動產生）\n\n內容、狀態及驗收以 [每日 TODO](DAILY_TODO.md) 為唯一來源；請修改來源後執行 build_plan.py。日期僅供參考，未通過時延續当前單元。每天使用者投入 2–3 小時，機器運算另計。\n\n| 單元 | 階段 | 狀態 | 依賴 | 完成條件 |\n|---|---|---|---|---|\n'
    for t in tasks:md+=f"| {t['id']} {t['title']} | {t['phase']} | {t['status']} | {', '.join(t['deps']) or '無'} | {'；'.join(t['acceptance'])} |\n"
    md+='\n未確認清單不得進入開發；使用者確認驗收後才能完成。官方接口未驗證仍屬發布阻礙；JEV／ML 未通過可裁切，核心驗收保留。U12 啟動 72 小時 soak，U14 須實際達到連續時數，單元間隔不足則順延。\n'
    (ROOT/'02-roadmap.md').write_text(md)
    dest=ROOT/'site/dist';(dest/'documents').mkdir(parents=True,exist_ok=True)
    for name in ('implementation-data-sources.csv','langgraph-phase1-endpoints.json'):
        if (ROOT/name).exists():shutil.copy2(ROOT/name,dest/name)
    shutil.copy2(ROOT/'api-research/etf-source-inventory.json',dest/'etf-source-inventory.json')
    pdf_root=ROOT.parent/'output/pdf'
    if pdf_root.exists():
        import hashlib
        checks=json.loads((pdf_root/'document-checks.json').read_bytes())
        if not checks.get('visual_reviewed'):raise ValueError('Document visual review required before website publication')
        (dest/'deliverables').mkdir(exist_ok=True)
        for name in ['ETF_strategy.pdf','Operator_guide.pdf']:
            body=(pdf_root/name).read_bytes()
            if hashlib.sha256(body).hexdigest()!=checks['pdf_hashes'][name]:raise ValueError('Reviewed PDF changed: '+name)
            shutil.copy2(pdf_root/name,dest/'deliverables'/name)
    node='/Users/nelson/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
    marked='/Users/nelson/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js'
    documents=[]
    for p in (dest/'documents').glob('*.md'):
        if p.name.upper().startswith('SERVER'):p.unlink()
    for name,p in public_doc_sources():
        s=p.read_text();shutil.copy2(p,dest/'documents'/name)
        code='import {marked} from '+json.dumps(marked)+";let s='';for await(const c of process.stdin)s+=c;process.stdout.write(marked.parse(s));"
        html=subprocess.run([node,'--input-type=module','-e',code],input=s,text=True,capture_output=True,check=True).stdout
        html=re.sub(r'<a href="\.\./docs/([^\"]+)">(.*?)</a>',r'<span class="source-ref" title="來源位於專案 docs/">\2〔本地來源〕</span>',html)
        html=html.replace('href="site/dist/index.html"','href="#roadmap"')
        html=html.replace('href="rounds/R02_PLAN.md"','href="#doc=17-competition-readiness.md"')
        html=html.replace('href="../18-candidate-implementation.md"','href="#doc=18-candidate-implementation.md"')
        html=html.replace('href="../19-trading-risk-gate.md"','href="#doc=19-trading-risk-gate.md"')
        html=html.replace('href="../21-application-and-llm.md"','href="#doc=21-application-and-llm.md"')
        html=html.replace('href="../01-rules.md"','href="#doc=01-rules.md"')
        html=re.sub(r'href="(?:\.\./)?api-research/etf-holdings-readiness-2026-10-24.md"', 'href="#doc=20-etf-source-readiness.md"',html)
        html=re.sub(r'href="(?:\.\./)?api-research/etf-acquisition-2026-10-26.md"', 'href="#doc=23-etf-acquisition.md"',html)
        html=re.sub(r'href="(?:\.\./)?api-research/history-feasibility-2026-10-26.md"', 'href="#doc=24-history-feasibility.md"',html)
        html=re.sub(r'<a href="R02_RESEARCH_DEFERRED.md">(.*?)</a>',r'\1（本地封存）',html)
        html=re.sub(r'href="([\w-]+\.md)"',r'href="#doc=\1"',html)
        documents.append({'id':name,'title':s.splitlines()[0][2:],'html':html})
    (dest/'data.js').write_text('window.PLAN='+json.dumps(tasks,ensure_ascii=False)+';\nwindow.DOCS='+json.dumps(documents,ensure_ascii=False)+';\nwindow.DATA_CATALOG='+json.dumps(catalog,ensure_ascii=False)+';\nwindow.EXCHANGE_APIS='+json.dumps(apis,ensure_ascii=False)+';\n')
    print(f'Generated {len(tasks)} units; {len(documents)} documents; completed {sum(t["status"]=="已完成" for t in tasks)}')
if __name__=='__main__':build()
