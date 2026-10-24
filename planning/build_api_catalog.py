"""Generate reference documents and site data from sealed official specifications."""
import json,shutil,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R=ROOT/'api-research'

def build_apis():
    tw=json.loads((R/'twse-operations.json').read_text());tp=json.loads((R/'tpex-operations.json').read_text())
    extra=json.loads((R/'tpex/extra-probe.json').read_text())
    for n,x in enumerate(tp,1):
        x['id']=f'TPEx-{n:03}';x['spec_url']='https://www.tpex.org.tw/openapi/swagger.json'
        if x['priority']=='非本賽主線':x['priority']='參考';x['category']='other'
        if x['path']=='/tpex_daily_market_value':x.update(category='price',data_refs=['D09'],use='發行股數、收盤價與市值排名；規模與流通分析的部分原料。')
        if x['path']=='/tpex_pe_ratio_top10':x.update(category='fundamental',data_refs=['D23'],use='本益比排行的部分估值觀測；全體股票估值優先用 peratio_analysis。')
        if x['path']=='/tpex_active_broker_volume':
            x.update(category='flows',data_refs=['D30'],use='熱門股券商進出排行，作為可延後的部分分點代理資料。');x['caveat']+=' 熱門排行不是全部個股完整分點流，也不識別最終受益人。'
        if any(z in x['summary'] for z in ['權證','牛熊']):x.update(category='other',data_refs=[],priority='參考',use='固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。')
        if x['path']=='/mopsfin_t187ap39_O':x.update(priority='P0',category='rules',data_refs=['D05','D39'],use='董事會通過股利分派，與除權息預告／結果交叉核對。')
        if x['path']=='/tpex_mainborad_highlight':x.update(data_refs=['D18','D43'],use='市場家數、漲跌廣度、成交量值與當前收市指數；非長歷史序列。')
        if x['path']=='/tpex_mainboard_daily_close_quotes':x['caveat']+=' 多 Average／NextReferencePrice；Average 必須以成交金額／股數核對競賽公式；正式收盤時間前不採用未完成日資料。'
        if x['path']=='/tpex_mainboard_quotes':x['caveat']+=' 與 daily_close_quotes 的標的範圍不同，含權證等；按150檔白名單過濾。'
        if x['path']=='/tpex_3insti_daily_trading' and extra.get('http_status')==200:
            x['probe']=extra;x['caveat']+=' 實測同樣只有此規格的20欄；避險買進等完整拆分不足，不得由缺欄推造值。含前導空白鍵，需明確映射。'
        if x.get('probe'):
            p=x['probe'];x['probe']={'http_status':p.get('http_status'),'rows':p.get('rows',p.get('row_count')),'actual_shape':p.get('actual_shape',p.get('response_type')),'fetched_at':p.get('fetched_at'),'sha256':p.get('sha256'),'date_ranges':p.get('date_ranges',p.get('sample_dates',{})),'observed_fields':p.get('observed_fields',[])}
    items=tw+tp
    categories=json.loads((ROOT/'decision-data.json').read_text())['categories']+[{'id':'other','title':'完整索引／本賽延後參考','question':'保留全部官方操作，但不直接當作固定股票策略的必要資料。'}]
    sources=[{'exchange':'TWSE','entry_url':'https://openapi.twse.com.tw/','spec_url':'https://openapi.twse.com.tw/v1/swagger.json','base_url':'https://openapi.twse.com.tw/v1','oas':'Swagger 2.0','info_version':'1.0','count':len(tw),'sha256':json.loads((R/'twse/manifest.json').read_text())['sha256']},{'exchange':'TPEx','entry_url':'https://www.tpex.org.tw/openapi/','spec_url':'https://www.tpex.org.tw/openapi/swagger.json','base_url':'https://www.tpex.org.tw/openapi/v1','oas':'OpenAPI 3.0.0','info_version':'1.0.0','count':len(tp),'sha256':json.loads((R/'tpex/metadata.json').read_text())['spec_sha256']}]
    assert len({x['id'] for x in items})==len({(x['exchange'],x['method'],x['path']) for x in items})==len(items)
    data_ids={x['id'] for x in json.loads((ROOT/'decision-data.json').read_text())['items']}
    for x in items:
        assert set(x['data_refs'])<=data_ids
        assert x['category'] in {c['id'] for c in categories}
        assert x['url']==next(s['base_url'] for s in sources if s['exchange']==x['exchange'])+x['path']
        x['verification']='代表實測 HTTP '+str(x['probe']['http_status']) if x.get('probe') and x['probe'].get('http_status') else '已核對 Swagger；未逐端點實測'
    catalog={'title':'TWSE／TPEx 官方 API 端點','updated':'2026-10-09','sources':sources,'categories':categories,'priorities':{'P0':'參賽與可信資料必備','P1':'兩週基線候選','P2':'增量候選','P3':'可延後研究','參考':'完整索引，非本賽主線'},'items':items}
    (ROOT/'exchange-apis.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    for source in sources:
        exchange=source['exchange'];rows=[x for x in items if x['exchange']==exchange];filename='12-twse-endpoints.md' if exchange=='TWSE' else '13-tpex-endpoints.md'
        md=[f'# {exchange} OpenAPI 全端點與欄位目錄',f"盤點：2026-10-09，共 {len(rows)} 個 operation。官方來源：[Swagger]({source['entry_url']})、[完整規格]({source['spec_url']})。Base URL：`{source['base_url']}`。\n\n優先序、用途與需求關聯為本專案研究判斷；官方名稱、方法、path、參數與欄位依封存規格。需求關聯表示可支持的部分原料，不代表完整滿足該資料群。接入限制與建議見 [使用指南](11-openapi-guide.md)。",'## 完整索引','| ID | 優先序 | 官方名稱 | 方法與 Path |\n|---|---|---|---|']
        for x in rows:md.append(f"| {x['id']} | {x['priority']} | {x['summary']} | `{x['method']} {x['path']}` |")
        for x in rows:
            md += [f"## {x['id']} · {x['summary']}",f"- **方法／URL**：[{x['method']} {x['path']}]({x['url']})\n- **官方 tags**：{'、'.join(x['tags'])}\n- **決策分類／優先序**：{next(c['title'] for c in categories if c['id']==x['category'])}／{x['priority']}\n- **可支持需求**：{'、'.join(x['data_refs']) or '非目前主線'}\n- **用途**：{x['use']}\n- **參數**：{json.dumps(x['parameters'],ensure_ascii=False) if x['parameters'] else '規格未宣告；沒有已文件化的日期／代號／分頁參數。'}\n- **歷史限制**：{x['history']}\n- **回應**：規格根型別 `{x['response_shape']}`；媒體型態 {'、'.join(x['media_types'])}；{x['verification']}\n- **授權設定**：{'規格未宣告 security' if not x['security'] else json.dumps(x['security'],ensure_ascii=False)}，不等於服務無限制或可任意再散布。\n- **接入注意**：{x['caveat']}"]
            if x.get('probe'):md.append('**代表探測證據**：`'+json.dumps(x['probe'],ensure_ascii=False).replace('`','\\`')+'`')
            md.append('| 原始欄位名稱（保留空白） | 型別 | 官方描述 |\n|---|---|---|')
            for f in x['fields']:md.append(f"| `{json.dumps(f['name'],ensure_ascii=False)}` | {f['type']} | {f['description'].replace('|','／').replace(chr(10),' ')} |")
        text='\n\n'.join(md)+'\n'
        text=re.sub(r'(\|[^\n]*\|)\n\n(?=\|)',r'\1\n',text)
        (ROOT/filename).write_text(text)
    out=ROOT/'site/dist';(out/'api-specs').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'exchange-apis.json',out/'api-specs/exchange-apis.json')
    for ex in ['twse','tpex']:shutil.copy2(R/ex/'swagger.json',out/f'api-specs/{ex}-swagger.json')
    print('API catalog:',len(items),'operations; priorities',dict(Counter(x['priority'] for x in items)))
    return catalog
if __name__=='__main__':build_apis()
