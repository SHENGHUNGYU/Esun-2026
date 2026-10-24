"""One catalog source feeds the reference Markdown and interactive site."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def build_catalog():
    c=json.loads((ROOT/'decision-data.json').read_text())
    ids=[x['id'] for x in c['items']]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate data id')
    cats={x['id']:x for x in c['categories']};sources={x['id']:x for x in c['sources']}
    md=['# 決策資料完整目錄（自動產生）',f"更新：{c['updated']}。共 {len(c['categories'])} 類、{len(c['items'])} 組。來源為 decision-data.json；每組包含多個候選欄位，不代表全部需實作。",'策略取捨與 Beta／時點方法見 [決策資料說明](09-decision-data.md)。', '## 優先序', '\n'.join(f'- {k}：{v}' for k,v in c['priorities'].items())]
    for cat in c['categories']:
        md += ['## '+cat['title'],cat['question']]
        for x in c['items']:
            if x['category']!=cat['id']:continue
            if x['priority'] not in c['priorities']:raise ValueError('invalid priority')
            refs=[]
            for sid in x['sources']:
                s=sources[sid];url=s['url'].removeprefix('#doc=');refs.append(f"[{s['title']}]({url})")
            md += [f"### {x['id']} · {x['name']} · {x['priority']}", '\n'.join(f'- **{label}**：{value}' for label,value in [('欄位／指標',x['fields']),('決策用途',x['use']),('頻率／歷史需求',x['cadence']),('取得現況',x['status']),('限制與偏誤',x['caveat']),('候選來源','、'.join(refs))])]
    if any(x['category'] not in cats for x in c['items']):raise ValueError('unknown category')
    md+=['## 來源與核對範圍']
    for s in c['sources']:md += [f"- [{s['title']}]({s['url'].removeprefix('#doc=')})：{s['note']}"]
    (ROOT/'10-data-catalog.md').write_text('\n\n'.join(md)+'\n')
    return c
