"""Extract the observed TPEx OAS snapshot; classifications are research judgments."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
SPEC = json.loads((ROOT / 'swagger.json').read_text())
BASE = SPEC['servers'][0]['url']
PROBES = {x['path']: x for x in json.loads((ROOT / 'probe-results.json').read_text())}

# Exact-path groups, reviewed against all 225 official operations.
GROUPS = [
    ('P0', 'price', ['D04', 'D07', 'D09', 'D10', 'D31', 'D33', 'D34', 'D57'], '官方成交均價、日價量、估值及研究序列的原始輸入；先限定固定 150 檔宇宙中的上櫃股。', ['tpex_mainboard_quotes', 'tpex_mainboard_daily_close_quotes']),
    ('P0', 'price', ['D11'], '暫停、恢復、變更交易及處置狀態檢查。', ['tpex_spendi_today', 'tpex_spendi_history', 'tpex_cmode', 'tpex_disposal_information']),
    ('P0', 'rules', ['D05', 'D08', 'D39'], '除權息與公司行動預告、計算結果，對照競賽權益帳；公告中的理論值不能直接取代官方結算。', ['tpex_exright_daily', 'tpex_exright_prepost']),
    ('P0', 'rules', ['D01', 'D09', 'D49'], '證券識別、發行股數、產業、上市櫃日期與基本資料映射。', ['mopsfin_t187ap03_O']),
    ('P1', 'fundamental', ['D19', 'D50'], '月營收年增、累計與加速度，保留各次發布快照。', ['mopsfin_t187ap05_O', 'mopsfin_t187ap05_OA', 'mopsfin_t187ap05_OB']),
    ('P1', 'fundamental', ['D23'], '估值比較與殖利率，核對盈餘分母、年度及不適用值。', ['tpex_mainboard_peratio_analysis']),
    ('P1', 'flows', ['D25'], '三大法人逐股買賣股數與淨額；區分自營商自行買賣及避險。', ['tpex_3insti_daily_trading']),
    ('P1', 'events', ['D37', 'D38', 'D39', 'D40', 'D41'], '重大訊息與事件證據，分別保留發言日期時間、事實發生日、出表與首見時間。', ['mopsfin_t187ap04_O']),
    ('P1', 'macro', ['D18', 'D31', 'D32', 'D43', 'D56'], '櫃買市場與總報酬基準，估 Beta、相對強弱與績效歸因。', ['tpex_index', 'tpex_index_consti', 'tpex_reward_index', 'tpex_mainborad_highlight', 'tpex_daily_trading_index']),
    ('P2', 'flows', ['D25', 'D26'], '法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。', ['tpex_3insti_qfii', 'tpex_3insti_qfii_industry', 'tpex_3insti_dealer_trading', 'tpex_3insti_summary', 'tpex_3insti_trading', 'tpex_3insti_qfii_trading']),
    ('P2', 'flows', ['D28'], '融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。', ['tpex_mainboard_margin_balance', 'tpex_margin_sbl', 'tpex_margin_trading_term', 'tpex_margin_trading_adjust', 'tpex_margin_trading_marginspot', 'tpex_margin_trading_margin_mark', 'tpex_margin_trading_margin_used', 'tpex_margin_trading_short_sell', 'tpex_short_sell']),
    ('P2', 'price', ['D10', 'D11', 'D16', 'D18'], '行情、交易風險、成交活躍度及流動性輔助檢查。', ['tpex_trading_warning_information', 'tpex_trading_warning_note', 'tpex_ceil_non_trading', 'tpex_active_dollar_volume', 'tpex_active_advanced', 'tpex_active_declined', 'tpex_daily_market_value', 'tpex_daily_turnover', 'tpex_trading_volumes_avg', 'tpex_trading_amount_avg', 'tpex_trading_volume_ratio', 'tpex_pe_ratio_top10', 'tpex_volume_rank', 'tpex_amount_rank', 'tpex_delayed_stock_open', 'tpex_delayed_stock_close', 'tpex_ipo_no_limit']),
    ('P2', 'events', ['D05', 'D23', 'D39'], '董事會股利方案與股東會日曆，提案不等於最終實施或可用現金。', ['mopsfin_t187ap39_O', 't187ap41_O']),
    ('P2', 'flows', ['D29', 'D24'], '董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。', ['mopsfin_t187ap02_O', 'mopsfin_t187ap08_O', 'mopsfin_t187ap09_O', 'mopsfin_t187ap10_O', 'mopsfin_t187ap11_O', 'mopsfin_t187ap12_O', 'mopsfin_t187ap13_O']),
    ('P2', 'events', ['D24', 'D37', 'D42'], '經營權變動、裁罰與資訊申報違規，作公司事件風險。', ['mopsfin_t187ap22_O', 'mopsfin_t187ap23_O', 'mopsfin_t187ap24_O', 'mopsfin_t187ap25_O', 'mopsfin_t187ap26_O', 'mopsfin_t187ap27_O']),
    ('P2', 'fundamental', ['D20', 'D40', 'D41'], '公司／產業 EPS 及財測達成與差異，樣本數、有效期及實際發布時點須另核。', ['mopsfin_t187ap14_O', 'mopsfin_t187ap15_O', 'mopsfin_t187ap16_O', 'mopsfin_187ap17_O']),
    ('P3', 'price', ['D10', 'D12', 'D30'], '當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。', ['tpex_securities', 'tpex_intraday_trading_statistics', 'tpex_active_broker_volume', 'tpex_odd_stock', 'tpex_off_market', 'tpex_daily_broker1', 'tpex_intraday_fee', 'tpex_intraday_trading_pre', 'tpex_intraday_trading_his', 'tpex_daily_qutoes_block', 'tpex_daily_trading_block', 'tpex_daily_trading_summary_odd', 'tpex_monthly_trading_summary_block', 'tpex_yearly_trading_summary_block', 'tpex_prvol', 'tpex_daily_trade_block_day', 'tpex_daily_broker2', 'mopsfin_t187ap19_O', 'tpex_margin_trading_lend']),
]
MAP = {}
for priority, category, refs, use, names in GROUPS:
    for name in names:
        assert '/' + name in SPEC['paths'], name
        assert '/' + name not in MAP, name
        MAP['/' + name] = (priority, category, refs, use)

def classify(path, summary, tags):
    if path in MAP:
        return MAP[path]
    # Off-universe markets remain in the full inventory; no planned stock orders.
    if '興櫃' in summary or '創櫃' in tags or path == '/tpex_esb_applicant_companies':
        return ('非本賽主線', 'industry', [], '興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。')
    if '權證' in tags:
        return ('P3', 'flows', ['D46'], '權證及牛熊證可作情緒／避險需求候選代理；不列入競賽股票委託，先驗證樣本外增量。')
    if '債券' in tags:
        return ('P3', 'macro', ['D45'], '債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。')
    if '黃金現貨' in tags:
        return ('P3', 'macro', ['D48'], '台灣黃金現貨價格背景；需另核單位與國際金價基差。')
    if '開放式基金' in tags:
        return ('非本賽主線', 'funds', [], '開放式基金行情及造市商，不是指定 30 ETF 的每日前 15 持股。')
    if '券商資料' in tags:
        return ('非本賽主線', 'flows', [], '券商人員數等營運資料，與每日選股沒有已驗證直接關係。')
    if '指數系列' in tags:
        return ('P2', 'macro', ['D18', 'D32', 'D43', 'D55', 'D56'], '風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。')
    if '財務報表' in tags:
        priority = 'P1' if path in ('/mopsfin_t187ap07_O_ci', '/mopsfin_t187ap06_O_ci', '/mopsfin_t187ap06_O_ciA') else 'P2'
        refs = ['D22'] if '資產負債表' in summary else ['D20', 'D23']
        return (priority, 'fundamental', refs, '財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。')
    if '公司治理' in tags:
        return ('P2' if '供應鏈' in summary or '產品品質' in summary or '風險管理' in summary or '資訊安全' in summary else 'P3', 'fundamental', ['D24', 'D49'] if '供應鏈' in summary else ['D24'], '治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。')
    raise ValueError((path, summary, tags))

def resolve(schema):
    if '$ref' in schema:
        obj = SPEC
        for key in schema['$ref'][2:].split('/'):
            obj = obj[key]
        return obj
    return schema

operations = []
for path, path_item in SPEC['paths'].items():
    for method, operation in path_item.items():
        if method.lower() not in ('get', 'post', 'put', 'patch', 'delete', 'head', 'options'):
            continue
        response = operation['responses']['200']
        media = response.get('content', {})
        schema = resolve(media.get('application/json', next(iter(media.values())))['schema'])
        priority, category, refs, use = classify(path, operation['summary'], operation['tags'])
        probe = PROBES.get(path)
        fields = [{'name': name, 'type': value.get('type'), 'description': value.get('description', ''), 'required': name in schema.get('required', [])} for name, value in schema.get('properties', {}).items()]
        operations.append({
            'exchange': 'TPEx', 'method': method.upper(), 'path': path,
            'url': BASE + path, 'summary': operation.get('summary', ''),
            'description': operation.get('description', ''), 'tags': operation.get('tags', []),
            'parameters': path_item.get('parameters', []) + operation.get('parameters', []),
            'fields': fields, 'response_schema_ref': media.get('application/json', next(iter(media.values())))['schema'].get('$ref'),
            'response_shape': schema.get('type'), 'media_types': list(media),
            'security': operation.get('security', SPEC.get('security', [])),
            'priority': priority, 'category': category, 'data_refs': refs,
            'use': use, 'caveat': 'Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。' + ('名稱雖含「歷史」，仍須確認實際保留期間。' if '歷史' in operation.get('summary', '') else ''),
            'history': '未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。',
            'verification': '代表實測 HTTP 200' if probe else '僅核對官方 Swagger schema，未實測',
            'probe': probe,
        })

(ROOT.parent / 'tpex-operations.json').write_text(json.dumps(operations, ensure_ascii=False, indent=2) + '\n')
metadata = {
    'exchange': 'TPEx', 'retrieved_date': '2026-10-09',
    'entry_url': 'https://www.tpex.org.tw/openapi/',
    'spec_url': 'https://www.tpex.org.tw/openapi/swagger.json',
    'api_base_url': BASE, 'openapi_version': SPEC['openapi'],
    'api_info_version': SPEC['info']['version'], 'operation_count': len(operations),
    'path_count': len(SPEC['paths']), 'schema_count': len(SPEC['components']['schemas']),
    'spec_sha256': hashlib.sha256((ROOT / 'swagger.json').read_bytes()).hexdigest(),
    'tag_counts': dict(collections.Counter(tag for x in operations for tag in x['tags'])),
    'priority_counts': dict(collections.Counter(x['priority'] for x in operations)),
    'parameters_operation_count': sum(bool(x['parameters']) for x in operations),
    'pagination': '未宣告', 'security': '規格未宣告 security 或 securitySchemes；四個代表端點未帶 key 回傳 HTTP 200。',
    'rate_limit': '規格未提供；不宣稱無限制。',
    'updated_at': '規格未逐表提供排程；HTTP Last-Modified 是檔案版本資訊，不能當公司公告時點。',
    'sources': [
        {'url': 'https://data.gov.tw/dataset/11371', 'role': '上櫃股票收盤行情：每 1 日更新、免費、政府開放授權；不可推論每張表同頻率。'},
        {'url': 'https://data.gov.tw/dataset/11370', 'role': '上櫃股票行情：含均價、次日參考價，股票／ETF／ETN；與收盤行情含權證之範圍不同。'},
        {'url': 'https://data.gov.tw/dataset/11387', 'role': '融資融券餘額：每日、政府開放授權。'},
        {'url': 'https://data.gov.tw/dataset/11369', 'role': '市場現況：官方資料集標示不定期更新，勿全表假設每日。'},
        {'url': 'https://eshop.tpex.org.tw/en/product/list/31', 'role': '另有盤後訂閱產品 API 文件，與本 OpenAPI 不同。'},
    ],
}
(ROOT / 'metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:metadata[k] for k in ('operation_count','tag_counts','priority_counts','parameters_operation_count')}, ensure_ascii=False, indent=2))
