"""Build the implementation source register with pandas; no live API calls."""
from pathlib import Path
import csv
import hashlib
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'implementation-data-sources.csv'
apis = json.loads((ROOT / 'exchange-apis.json').read_text())['items']
needs = json.loads((ROOT / 'decision-data.json').read_text())['items']
phase1 = {x['endpoint_id']: x for x in json.loads((ROOT / 'langgraph-phase1-endpoints.json').read_text())['endpoints']}
spec = json.loads((ROOT / 'api-research/finmind/openapi.json').read_text())
fm_doc = (ROOT / 'api-research/finmind/llms-full.txt').read_text()
blocks = {m[0]: m[1] for m in re.findall(r'^### (\w+)([^\n]*\n.*?)(?=^###? |\Z)', fm_doc, re.M | re.S)}
rows = []
COLS = ['項目ID','紀錄類型','接入階段','優先序','資料名稱','來源或負責方','市場或標的','需求ID','用途',
        'HTTP方法','端點URL','URL類型','資料集或代碼','參數與查詢方式','必要欄位或完整schema','更新頻率',
        '目標歷史範圍','官方歷史保證','PIT與時點要求','權限與費用','目前狀態','驗證程度','驗證日期',
        '使用者需準備','Codex接入工作','啟用條件','缺少時處理','上游項目ID','備援或替代','限制與注意',
        '來源文件','實測證據','實作模組','準備狀態','安全存放位置或回覆','完成驗收證據']

def add(id, kind, stage, name, **kw):
    r = dict.fromkeys(COLS, '')
    r.update({'項目ID': id, '紀錄類型': kind, '接入階段': stage, '資料名稱': name,
              '優先序': 'P2', '目前狀態': '待接入', '驗證程度': '設計清單；未接通驗收',
              '驗證日期': '2026-10-14', '準備狀態': '待準備',
              'PIT與時點要求': '保留published_at、first_seen_at、fetched_at、available_at及修訂版本；cutoff後資料不進本次研究',
              '完成驗收證據': '待填：樣本檔位置、覆蓋率、時間／單位檢查與hash；勿填密鑰'})
    r.update(kw)
    rows.append(r)
    return r

# Explicit source requests: documents/portals are never mislabeled callable APIs.
EXT = [
 ('SRC-FINMIND','第一階段','FinMind 帳號、Token與配額','D07 D08 D19 D20 D21 D25 D53 D64','https://finmind.github.io/login/','FinMind',
  '提供現有會員等級、到期日與Token的安全存放位置；若沒有帳號先註冊免費方案；不預授權升級付費',
  '帳號等級、可用資料集、單次範圍、每小時配額、保存／研究使用權','依帳號與dataset實測','登入與配額文件已讀；帳號未驗證'),
 ('SRC-CNA','第一階段','中央社產經證券 RSS','D38 D39 D42 D60','https://feeds.feedburner.com/rsscna/finance','中央通訊社',
  '確認競賽使用符合RSS非商業使用條件；若需全文或其他用途另取得授權；無需提供RSS金鑰',
  'title、link、guid、pubDate、description及first_seen；保留中央社來源標示','從接入日起累積；RSS不保證完整歷史','官方RSS頁確認入口；尚未以程式解析驗收'),
 ('SRC-TEJ','後續備援','TEJ PRO 歷史與PIT補缺','D05 D08 D09 D19 D20 D21 D22 D24 D26 D27 D29 D30 D49 D51 D64','https://api.tej.com.tw/','TEJ',
  '若FinMind缺PIT／歷史／欄位，提供已購模組、表目錄、欄位字典、匯出能力與可用年份；不用先購新產品',
  '歷史價量、公司行動、首發／重編財報、股數、籌碼、共識（依現有授權）','建議3–5年；財報至少12季，依已授權範圍','使用者有TEJ PRO；API與PIT產品權限未確認'),
 ('SRC-MOPS','第一階段備援','公開資訊觀測站／公司IR原始文件','D05 D19 D20 D21 D22 D24 D29 D37 D39 D40 D49','https://mops.twse.com.tw/mops/','MOPS及150檔公司IR',
  '不需逐檔手動準備；僅在公開資料不足時提供已合法取得之財報／法說資料與來源',
  '公司代碼、公告ID、原文或授權片段、附件、發布時間、版本、財報科目與單位','最新公告先累積；歷史以可取得原件與發布證據為準','文件入口；不是通用JSON端點'),
 ('SRC-T86','第一階段備援','上市逐股三大法人日報','D25','https://wwwc.twse.com.tw/zh/trading/foreign/t86.html','TWSE',
  '無需新帳號；FinMind法人資料不足時由Codex核對官方下載方式',
  '外資、投信、自營商自行買賣／避險買賣股數、日期、代碼','建議3–5年；此網頁不保證批次API歷史','網頁已讀；不在TWSE OpenAPI的368端點中'),
 ('SRC-TDCC','後續研究','TDCC股權分散表','D27','https://www.tdcc.com.tw/portal/zh/smWeb/qryStock','臺灣集保',
  '先用公開週資料；超過公開歷史範圍時確認FinMind或TEJ既有權限',
  '日期、代碼、級距、人數、股數、占比、取得時間','研究目標1–3年；官方查詢頁說明保存1年','官方頁已讀；尚未批次下載驗收'),
 ('SRC-TAIFEX','後續研究','期交所衍生品市場觀測','D46','https://openapi.taifex.com.tw/','TAIFEX',
  '公開資料可先接入；長歷史若需付費另討論',
  '期貨／選擇權日行情、到期月、日夜盤、法人OI、PutCall、VIX相關原料','研究目標3–5年；不得把快照當長歷史','Swagger入口已核對；未逐資料集驗收'),
 ('SRC-FRED','後續研究','FRED／ALFRED總體與發布版本','D32 D45 D47','https://fred.stlouisfed.org/docs/api/fred/series_observations.html','St. Louis Fed',
  '若啟用美國總體資料，申請API key並提供安全存放位置與使用範圍',
  'series_id、observation date/value、vintage、realtime_start/end、發布日期','建議5–10年；逐序列驗證可用vintage','官方API文件已讀；未設定key與序列'),
 ('SRC-MACRO-TW','後續研究','台灣官方總體與事件日曆','D42 D45 D47 D50','https://www.stat.gov.tw/','主計總處／央行／經濟部／財政部',
  '不需預購；若希望使用特定宏觀序列再選定',
  'CPI、GDP、利率會議、出口／外銷訂單、實際發布時間、首次值與修訂','建議5–10年；保留各版本','來源機構候選；序列與下載路徑待核對'),
 ('SRC-CONSENSUS','選用研究','分析師與總體共識PIT資料','D41 D47 D51','https://api.tej.com.tw/databases.html','TEJ既有產品或其他已授權供應商',
  '提供是否已有共識資料授權、預測發布時間／歷史版本及樣本；沒有就停用預期差模型',
  '預測期、EPS／營收／宏觀預測、預測家數、分歧、當時版本','至少2–3年PIT；今日回修歷史不等於PIT','供應商表代碼與權限未確認'),
 ('SRC-INDUSTRY','選用研究','產業出貨、價格、供應鏈與IR','D40 D49 D50','https://mops.twse.com.tw/mops/','公司IR／官方統計／已授權產業資料商',
  '列出已有產業報告或資料庫與可用範圍；先不用購買DRAM、運價或逐字稿產品',
  '產能、訂單、庫存、出貨、產品價格、客戶／地區營收、關係生效日與證據','建議3–5年；依行業／發布頻率','來源待逐項核實，新聞提及不是供應鏈證明'),
 ('SRC-ALT','延後研究','社群／搜尋／替代數據','D52 D66','','合法平台或已授權供應商待選',
  '第一階段不需取得；有明確假說與現有權限才提供',
  '搜尋量、討論量、網站流量、招聘、衛星等；抽樣方法、授權及版本','未定，須有可重現歷史','可裁切，未取得'),
 ('SRC-ORGANIZER','首日閉環P0','官方DataPack帳戶真值與兩階段繳交','D02 D03 D04 D05 D06 D35 D53 D56','https://esun-ai-challenge.tw/api/events/fundaiagent/attachments/29/download/', '主辦方',
  '提供實際team_id、最新DataPack安全路徑、試繳及PDF現況；後台下載方式已定義，自動化許可及Active Share口徑另核對',
  'DataPack: account.nav_tradable/aum/cash/receivable_cash/holdings_count; holdings.shares/receivable_shares; missing; prev_day_orders.outcome/excluded_codes/void_reasons; compliance.violations/notices/incidents; trade_date/as_of_date/generated_at','每交易日與官方修訂版本','DataPack與後台規格已封存，實際隊伍資料與送出尚未驗收；上傳檢核不等於送出，skipped不是通過'),
 ('SRC-ETF','正式參賽前','30檔指定ETF每日實際持股','D53 D54','https://finmind.github.io/tutor/TaiwanMarket/Chip/','FinMind／各ETF發行投信',
  '確認是否已有FinMind Sponsor持股權限；沒有先查各投信公開持股，不直接購買；確認主辦方接受之基準日期',
  'ETF代碼、持股代碼／ISIN、市場、幣別、股數、權重、現金、基準日、公告時間、前15排序','競賽每日；上市前不得虛補歷史；30檔逐一驗證','文件有ActiveETFHolding；30檔覆蓋及海外成分未驗證'),
 ('SRC-UNIVERSE','第一階段','官方固定150檔名單與主檔','D01','planning/units/U01/evidence/universe.csv','主辦方本地文件',
  '僅需提供主辦方後續更正版；現有150檔名單可先使用',
  '代碼、名稱、上市／上櫃、名單版本、來源頁與hash','固定競賽版本，不用今日市值重算','U01已核對；主檔映射待實作'),
 ('SRC-RULES','第一階段','D-Plan schema與競賽文件','D02 D04 D06','docs/official-2026-10-24/D-Plan.schema_v4.3.json','主辦方本地文件',
  '12份附件已封存且6份與舊檔相同；實作v4.3並在實際後台核對公告期限',
  'v4.3 schema與指南、DataPack、後台兩階段繳交；決策與委託各60，持股仍20–30','保留版本與生效日期','本地文件已核對；歧義仍待官方答覆'),
 ('SRC-OPS','第一階段','本地模型與主機資料儲存','D60 D62 D63 D64 D65','','使用者／Codex',
  '提供M3存取方式、資料目錄、可用磁碟與常駐時段、本地模型服務位址；未接通前可先完成無LLM資料管線',
  'artifact目錄、備份、時鐘時區、checkpoint、模型版本、權限與運行日誌','原始與研究證據至少保留競賽及驗收期間','M3與模型服務尚未驗收'),
 ('SRC-EVAL','第一階段','LLM／JEV中文金融評測資料','D60','','Codex建立／使用者驗收',
  '審閱由Codex整理的事件、引用、矛盾與缺證據案例；不需先提供付費模型',
  '案例原文、標準答案、引文ID、錯誤類型、獨立測試集','接入日起累積；獨立封存測試案例','尚未建立'),
 ('SRC-INDEX','後續研究','市場指數、指數換股與基金事件','D43 D44 D55 D56','https://openapi.twse.com.tw/','交易所／指數編製機構／基金發行人',
  '提供已授權的美股指數資料（若有）；無授權先使用驗證後可取得之市場基準，不能擅自以ETF冒充指數',
  '台美指數代碼、價格／總報酬、成分、權重、換股公告／生效日期、基金成立／清算、時區','建議3–5年；換股以當時公告版本為準','來源角色已定；美股SP500／Nasdaq／SOX等代碼與授權需驗證'),
 ('SRC-COMMODITY','選用研究','原油／金以外的成本與運輸序列','D48 D50','','官方統計或已授權產業資料商待選',
  '若策略使用銅、天然氣、運價或記憶體價格，提供已有資料商與產品；無現有權限先停用',
  '序列代碼、現貨／期貨口徑、幣別單位、轉倉、發布時間與修訂','研究目標3–5年，實際範圍依供應商','FinMind部分原料不能代表全部商品與運價'),
 ('SRC-NEWSARCHIVE','後續研究','可回測的歷史新聞與事件原文','D38 D40 D41 D42','','中央社授權產品／既有TEJ或其他已授權新聞庫',
  '若需事件回測，確認是否已有新聞歷史與全文／摘要授權；RSS只能從接入日起累積，暫不需購買',
  '首發與更新時間、原始URL／ID、授權摘要或原文、公司實體、刪修版本','至少1–3年候選；用當時可得內容','RSS不保證完整歷史；FinMind新聞也須核對內容授權與保存深度'),
]
for id, stage, name, refs, url, supplier, action, fields, hist, status in EXT:
    add(id,'資料源取得任務',stage,name,來源或負責方=supplier,需求ID=refs.replace(' ',';'),端點URL=url,
        URL類型='來源／文件入口' if url.startswith('https:') else ('本地檔案' if url else '待取得，不猜測URL'),
        必要欄位或完整schema=fields,目標歷史範圍=hist,目前狀態=status,使用者需準備=action,
        Codex接入工作='讀取官方文件、取樣、驗證欄位／單位／時間／覆蓋／授權，建立adapter與缺口記錄',
        啟用條件='取得且驗證所需資料與使用權；供應商文件存在不等於本帳戶可用',
        缺少時處理='停用依賴能力並記錄缺口；正式參賽必需項缺失時阻擋發布',
        權限與費用='依現有授權；未授權新增付費採購',來源文件=url or 'planning/08-sources-questions.md',
        優先序='P0' if id in {'SRC-ORGANIZER','SRC-ETF','SRC-UNIVERSE','SRC-RULES','SRC-OPS'} else 'P1',
        實作模組='source_registry')
rss=next(r for r in rows if r['項目ID']=='SRC-CNA')
rss.update({'HTTP方法':'GET','URL類型':'RSS feed','來源文件':'https://www.cna.com.tw/about/rss.aspx',
 '更新頻率':'建議15–30分鐘去重輪詢；遵循服務限制，非已建立排程',
 '權限與費用':'官方限定個人／非營利之非商業用途；僅RSS標題、前言、文章及首圖連結，不包含全文授權',
 '限制與注意':'保留中央通訊社署名；首圖僅存URL，不下載展示；未涵蓋全文與完整歷史，合法使用範圍需符合官方條款'})

# Preserve the exact complete exchange inventory; enrollment is a separate field.
for x in apis:
    chosen = phase1.get(x['id'])
    stage = ('條件啟用：產業分表' if chosen and chosen['enablement'].startswith('conditional') else
             '第一階段' if chosen else '後續候選' if x['priority'] in {'P0','P1','P2'} else '參考保留：預設停用')
    add(x['id'],'交易所API端點',stage,x['summary'],優先序=x['priority'],來源或負責方=x['exchange'],
        市場或標的='官方固定150檔中所屬市場；全市場回應本地過濾',需求ID=';'.join(x['data_refs']),用途=x['use'],
        HTTP方法=x['method'],端點URL=x['url'],URL類型='可呼叫端點',資料集或代碼=x['path'],
        參數與查詢方式='Swagger未宣告日期／代號／分頁參數；整表抓取後過濾',
        必要欄位或完整schema=json.dumps(x['fields'],ensure_ascii=False,separators=(',',':')),
        更新頻率='依資料組日／月／季／事件更新；精確完成時點待實測',目標歷史範圍='先累積每日不可變快照；長歷史另用FinMind／既有TEJ驗證',
        官方歷史保證=x['history'],權限與費用='公開OpenAPI；9個代表端點無key探測成功，其餘未逐項驗證；配額未知',
        目前狀態='已選候選；尚未實作adapter' if chosen else '已列目錄；尚未選用／接入',
        驗證程度=x['verification'],驗證日期='2026-10-09',使用者需準備='無需提供金鑰；公開來源由Codex處理',
        Codex接入工作='重驗schema、保留原始欄名空白、日期／單位映射、150檔覆蓋與原始hash',
        啟用條件='資料組契約驗收；產業表另需公司科目映射' if chosen else '有需求／增量證據才啟用，不預設全抓',
        缺少時處理='核心行情缺失阻擋研究；選用資料停用相關能力',上游項目ID='SRC-UNIVERSE;SRC-RULES',
        備援或替代='同資料組FinMind；PIT／缺欄位以MOPS或既有TEJ補',限制與注意=x['caveat'],
        來源文件=x['spec_url'],實測證據=json.dumps(x['probe'],ensure_ascii=False) if x['probe'] else '僅規格核對',
        實作模組='exchange_adapter',準備狀態='公開來源可開始接入')

# Dataset-specific FinMind rows. Keep documented exact IDs; no API key in CSV.
FM_MAP = {
 'TaiwanStockInfo':'D01 D09','TaiwanStockPrice':'D04 D07 D10 D13 D14 D15 D16 D17 D18 D31 D33 D34 D57',
 'TaiwanStockPriceAdj':'D08 D13 D31 D32 D33 D34','TaiwanStockPER':'D23',
 'TaiwanStockTradingDate':'D02','TaiwanStockSuspended':'D11','TaiwanStockPriceLimit':'D11',
 'TaiwanStockTotalReturnIndex':'D31 D32 D43 D56','TaiwanStockFinancialStatements':'D20 D24',
 'TaiwanStockBalanceSheet':'D20 D22 D24','TaiwanStockCashFlowsStatement':'D21 D22 D23',
 'TaiwanStockMonthRevenue':'D19','TaiwanStockDividend':'D05 D08 D23 D39',
 'TaiwanStockDividendResult':'D05 D08 D39','TaiwanStockCapitalReductionReferencePrice':'D05 D08',
 'TaiwanStockSplitPrice':'D05 D08','TaiwanStockParValueChange':'D05 D08',
 'TaiwanStockMarketValue':'D09','TaiwanStockMarketValueWeight':'D09 D35','TaiwanStockDelisting':'D01 D11',
 'TaiwanStockFinancialReportFile':'D20 D21 D22 D24 D37','TaiwanStockInstitutionalInvestorsBuySell':'D25',
 'TaiwanStockInstitutionalInvestorsBuySellWide':'D25','TaiwanStockTotalInstitutionalInvestors':'D25 D43',
 'TaiwanStockShareholding':'D26','TaiwanStockHoldingSharesPer':'D27',
 'TaiwanStockMarginPurchaseShortSale':'D28','TaiwanStockTotalMarginPurchaseShortSale':'D28 D43',
 'TaiwanStockSecuritiesLending':'D28','TaiwanDailyShortSaleBalances':'D28',
 'TaiwanStockMarginShortSaleSuspension':'D11 D28','TaiwanStockDispositionSecuritiesPeriod':'D11',
 'TaiwanStockNews':'D38 D42','TaiwanStockIndustryChain':'D49',
 'TaiwanStockActiveETFInfo':'D53','TaiwanStockActiveETFHolding':'D53 D54',
 'TaiwanStockActiveETFHoldingChange':'D54','TaiwanStockIndustryChainMoneyFlow':'D18 D49 D50',
 'TaiwanStockGovernmentBankBuySell':'D25 D30','TaiwanStockBrokerDailyConcentration':'D30',
 'TaiwanStockTradingDailyReport':'D30','TaiwanStockLoanCollateralBalance':'D28',
 'TaiwanStockMarginMaintenance':'D28','TaiwanTotalExchangeMarginMaintenance':'D28',
 'TaiwanStockDayTrading':'D10 D30','TaiwanStockDayTradingSuspension':'D11',
 'TaiwanStockDayTradingBorrowingFeeRate':'D28','TaiwanSecuritiesTraderInfo':'D30',
 'TaiwanStockBlockTrade':'D30','TaiwanStockBlockTradingDailyReport':'D30',
 'USStockInfo':'D44','USStockPrice':'D44','TaiwanExchangeRate':'D45',
 'ExchangeRate':'D45','InterestRate':'D45 D47','GovernmentBondsYield':'D45',
 'CrudeOilPrices':'D48','GoldPrice':'D48','TaiwanBusinessIndicator':'D47 D50',
 'TaiwanFuturesDaily':'D46','TaiwanOptionDaily':'D46','TaiwanOptionVix':'D46',
 'TaiwanFuturesInstitutionalInvestors':'D46','TaiwanOptionInstitutionalInvestors':'D46',
 'TaiwanFuturesInstitutionalInvestorsAfterHours':'D46','TaiwanOptionInstitutionalInvestorsAfterHours':'D46',
 'TaiwanFuturesOpenInterestLargeTraders':'D46','TaiwanOptionOpenInterestLargeTraders':'D46',
 'TaiwanFuturesFinalSettlementPrice':'D46','TaiwanOptionFinalSettlementPrice':'D46',
 'TaiwanStockPriceTick':'D12','TaiwanStockKBar':'D12','TaiwanStockStatisticsOfOrderBookAndTrade':'D12',
}
enum = spec['components']['schemas']['DataSetInputV4']['enum']
assert set(FM_MAP) <= set(enum), set(FM_MAP)-set(enum)
first = {'TaiwanStockInfo','TaiwanStockPrice','TaiwanStockPER','TaiwanStockTradingDate','TaiwanStockSuspended',
         'TaiwanStockFinancialStatements','TaiwanStockBalanceSheet','TaiwanStockCashFlowsStatement',
         'TaiwanStockMonthRevenue','TaiwanStockInstitutionalInvestorsBuySell','TaiwanStockNews'}
for dataset, refs in FM_MAP.items():
    b = blocks.get(dataset, '')
    def meta(label):
        m=re.search(r'^- '+re.escape(label)+r': (.+)$',b,re.M)
        return m.group(1) if m else '未明示，需逐資料集核對'
    title = re.search(r'^ \(([^\n]+)\)',b)
    path = '/api/v4/taiwan_stock_trading_daily_report' if dataset=='TaiwanStockTradingDailyReport' else '/api/v4/data'
    params = 'dataset='+dataset+'; data_id依標的; start_date/end_date依資料集文件；Authorization Bearer由安全環境注入'
    if meta('Params')!='未明示，需逐資料集核對':
        params='官方參數範例（日期／代號須替換，不當成固定值）：'+meta('Params')+'；Authorization Bearer由安全環境注入'
    if 'Single day per request' in b: params+='；單日請求，不假設end_date有效'
    if dataset=='TaiwanStockTradingDailyReport': params='data_id或securities_trader_id; date單日；專用端點，不送通用/data'
    if dataset=='TaiwanStockIndustryChainMoneyFlow': params='dataset='+dataset+'; start_date單日；不帶data_id及end_date'
    stage = '第一階段' if dataset in first else '條件啟用：歷史補齊' if dataset in {'TaiwanStockPriceAdj','TaiwanStockTotalReturnIndex'} else '正式參賽前' if dataset.startswith('TaiwanStockActiveETF') else '選用研究'
    limitation='文件範圍不等於每個代碼皆完整；帳戶、欄位單位、歷史與PIT尚待取樣。'
    if dataset in {'TaiwanStockFinancialStatements','TaiwanStockBalanceSheet','TaiwanStockCashFlowsStatement','TaiwanStockMonthRevenue'}:
        limitation+=' 財報date/營收年月不直接等於發布時間；無首發版本證據時不做嚴格PIT回測。'
    if dataset=='TaiwanStockFinancialStatements': limitation+=' EPS跨季股數基準可能不同，不直接加總為TTM。'
    if dataset=='TaiwanStockIndustryChainMoneyFlow': limitation+=' 文件說明歷史使用目前產業分類，不能當歷史PIT產業映射。'
    if dataset=='TaiwanStockPriceAdj': limitation+=' 必須核對除權息／還原方法；不可拿調整價作競賽成交價。'
    if dataset=='TaiwanStockPrice': limitation+=' 原始未公布價格可能儲存為0，須轉missing/no-price而非0元或-100%報酬；僅成交量>0不足以判斷有效價格。'
    if dataset=='TaiwanStockPriceAdj': limitation+=' 供應商可能沿用無成交日前一調整價；需連同原始價辨識填補，不能當作當日有效成交。'
    if dataset=='TaiwanStockActiveETFHoldingChange': limitation+=' 持股增減可能含申贖，不等於經理人主動買賣量。'
    if dataset=='TaiwanStockNews': limitation+=' 供應商新聞metadata不授權任意全文保存；中央社RSS仍為首選新聞來源。'
    add('FM-'+dataset,'FinMind資料集',stage,title.group(1) if title else dataset,來源或負責方='FinMind',
        優先序='P1' if dataset in first else 'P0' if dataset=='TaiwanStockActiveETFHolding' else 'P2',
        市場或標的='固定150檔／30ETF／指定基準；以dataset實際覆蓋為準',需求ID=refs.replace(' ',';'),
        用途=';'.join(i['name'] for i in needs if i['id'] in refs.split()),HTTP方法='GET',
        端點URL='https://api.finmindtrade.com'+path,URL類型='可呼叫端點＋dataset',資料集或代碼=dataset,
        參數與查詢方式=params,必要欄位或完整schema=(json.dumps(spec['components']['schemas'][dataset]['properties'],ensure_ascii=False,separators=(',',':')) if 'properties' in spec['components']['schemas'].get(dataset,{}) else meta('Columns')),更新頻率='依資料集排程與實際資料日核對',
        目標歷史範圍='先驗證最近5個交易日／最新報告期；通過後依需求回補3–5年，最少61個對齊價格點才開Beta60',
        官方歷史保證='文件描述：'+meta('Data range')+'；非本帳戶實測保證',權限與費用='文件會員層級：'+meta('Tier')+'；現有帳戶未驗，未授權付費升級',
        目前狀態='使用者指定來源；資料尚未取得驗收',驗證程度='2026-10-14官方OpenAPI列名與官方資料集文件核對',
        使用者需準備='完成SRC-FINMIND帳戶與安全Token位置；付費表無既有權限則先停用',
        Codex接入工作='使用pandas正規化；查quota後按dataset分批；驗body.status／HTTP402；不以高併發繞過限制',
        啟用條件='Token／層級、資料覆蓋、單位、日期與授權驗證通過；歷史計算另驗樣本數',
        缺少時處理='使用對應TWSE／TPEx快照；歷史不足停用依賴指標；ETF持股缺失阻擋正式合規',
        上游項目ID='SRC-FINMIND;SRC-UNIVERSE',備援或替代='交易所／MOPS／TDCC／既有TEJ；ETF用發行投信',
        限制與注意=limitation,來源文件='https://api.finmindtrade.com/openapi.json ; https://finmind.github.io/llms-full.txt',
        實作模組='finmind_adapter')

for name,path,fields in [('quota','https://api.web.finmindtrade.com/v2/user_info','user_count;api_request_limit'),
                         ('datalist','https://api.finmindtrade.com/api/v4/datalist','dataset;data_id清單'),
                         ('translation','https://api.finmindtrade.com/api/v4/translation','dataset;中英欄位映射')]:
    add('FM-SUPPORT-'+name,'FinMind支援端點','第一階段',name,來源或負責方='FinMind',HTTP方法='GET',端點URL=path,
        URL類型='可呼叫端點',需求ID='D64',必要欄位或完整schema=fields,上游項目ID='SRC-FINMIND',
        使用者需準備='僅Token安全位置；不要在CSV填Token',來源文件='https://finmind.github.io/llms-full.txt',
        啟用條件='登入權限可用；先讀quota再排程抓取',實作模組='finmind_adapter')

# Exactly one row for each of the 66 agreed requirements, including computed data.
derived=set(range(10,11))|set(range(13,19))|set(range(31,37))|{41,56,57,58,59,60,61,62,63,65}
derived_deps={10:[7,9],13:[7,8,43],14:[7,8],15:[7,8],16:[7,8],17:[7],18:[7,9,49],
 31:[7,8,43],32:[31,45,49],33:[7,8],34:[7,8,49],35:[3,9,31,34,49],36:[3,31,33,34,35],
 41:[19,20,38,51],56:[3,7,43],57:[4,7,8],58:[7,19,20,57],59:[57,58],60:[37,38],61:[57,58,59],
 62:[64],63:[7,62],65:[62,63]}
internal={3,6,35,56,57,58,59,60,61,62,63,65}
for n in needs:
    num=int(n['id'][1:]);rid='REQ-'+n['id']
    upstream=[r['項目ID'] for r in rows if n['id'] in r['需求ID'].split(';')]
    upstream += ['REQ-D%02d'%i for i in derived_deps.get(num,[])]
    stage='第一階段' if num in {1,2,7,11,19,20,21,22,23,25,37,38,39,49,60,62,63,64,65} else '正式參賽前' if n['priority']=='P0' else '條件啟用：歷史或研究驗收'
    source='內部計算／驗證產物' if num in derived else '來源取得任務與端點詳見上游項目ID'
    add(rid,'衍生或內部需求' if num in derived or num in internal else '原始資料需求',stage,n['name'],
        優先序=n['priority'],來源或負責方=source,需求ID=n['id'],用途=n['use'],必要欄位或完整schema=n['fields'],
        更新頻率=n['cadence'],目標歷史範圍=n['cadence'],官方歷史保證='需求目標，不代表供應商保證',
        目前狀態='資料需求已列；依上游逐項驗收',使用者需準備='先完成上游SRC任務；若為程式衍生，由Codex建立，無需購買指標',
        Codex接入工作='驗證上游原料後計算／產生' if num in derived else '選擇上游主來源與備援；逐欄確認需求是否滿足',
        啟用條件='所有必要欄位、時點、單位、覆蓋與歷史窗口達標；有端點映射不代表全欄位已覆蓋',
        缺少時處理='停用依賴能力；P0正式合規缺失不得標完成',上游項目ID=';'.join(upstream),
        備援或替代='按上游各來源列處理',限制與注意=n['caveat'],來源文件='planning/decision-data.json#'+n['id'],
        實作模組='feature/evidence/quality' if num in derived else 'dataset_gateway')

# All 30 competition ETFs, preserving text IDs and distinct coverage obligations.
etfs=pd.read_csv(ROOT/'units/U01/evidence/active-etfs.csv',dtype=str,keep_default_na=False)
for e in etfs.to_dict('records'):
    add('ETF-'+e['code'],'逐檔持股取得任務','正式參賽前',e['name'],優先序='P0',來源或負責方='FinMind／該ETF官方發行投信',
        市場或標的=e['code'],需求ID='D53;D54',資料集或代碼=e['code'],HTTP方法='GET',
        端點URL='https://api.finmindtrade.com/api/v4/data',URL類型='候選端點；逐檔覆蓋未驗證',
        參數與查詢方式='dataset=TaiwanStockActiveETFHolding; data_id='+e['code']+'; start_date/end_date依文件與實測',
        必要欄位或完整schema='ETF代碼、持股代碼／ISIN、名稱、市場、幣別、股數／權重、現金、基準日、公告時間、前15名',
        更新頻率='每個競賽交易日；確認持股資料日與公告日',目標歷史範圍='上市後可得資料；競賽期間每日保存',
        官方歷史保證='此基金在資料集是否存在、起始日、海外成分與權重欄位均待驗',
        權限與費用='FinMind文件要求Sponsor；未授權升級；投信公開持股為備援',
        目前狀態='競賽名單已核對；實際持股未取得',使用者需準備='確認既有Sponsor權限或協助取得投信公開持股／主辦方基準；不需提供人工選股',
        Codex接入工作='逐ETF核對持股日期、15大排序、跨市場識別與官方Active Share口徑',
        啟用條件='本ETF資料與主辦方口徑均驗證',缺少時處理='該ETF合規未驗證；不能當通過',
        上游項目ID='SRC-ETF;SRC-ORGANIZER;FM-TaiwanStockActiveETFHolding',備援或替代='該ETF發行投信每日實際持股；精確持股URL待查證，不猜網址',
        限制與注意='基金名稱／代碼按本地競賽名單；不得以指數成分、ETF基本資料或今日權重回填歷史',
        來源文件='planning/units/U01/evidence/active-etfs.csv ; https://finmind.github.io/tutor/TaiwanMarket/Chip/',實作模組='etf_holdings_adapter')

# Provider-independent, known gaps must remain visible even if many endpoints map to a requirement.
assert len({r['項目ID'] for r in rows})==len(rows)
assert {r['項目ID'] for r in rows if r['紀錄類型']=='交易所API端點'}=={x['id'] for x in apis}
assert {r['需求ID'] for r in rows if r['項目ID'].startswith('REQ-')}=={n['id'] for n in needs}
ids={r['項目ID'] for r in rows}
for r in rows:
    assert all(x in ids for x in r['上游項目ID'].split(';') if x),(r['項目ID'],r['上游項目ID'])
    assert not any(str(v).startswith(('=','+','-','@','\t','\r')) for v in r.values()),r['項目ID']
    if r['項目ID'].startswith('REQ-'): assert r['上游項目ID'],r['項目ID']
df=pd.DataFrame(rows,columns=COLS)
rank={'資料源取得任務':0,'原始資料需求':1,'衍生或內部需求':1,'逐檔持股取得任務':2,'FinMind支援端點':3,'FinMind資料集':4,'交易所API端點':5}
df=df.assign(_rank=df['紀錄類型'].map(rank)).sort_values(['_rank','項目ID'],kind='stable').drop(columns='_rank').reset_index(drop=True)
df.to_csv(OUT,index=False,encoding='utf-8-sig',quoting=csv.QUOTE_ALL,lineterminator='\n')
read=pd.read_csv(OUT,dtype=str,keep_default_na=False,encoding='utf-8-sig')
pd.testing.assert_frame_equal(df,read)
assert set(read.loc[read['紀錄類型']=='逐檔持股取得任務','資料集或代碼'])==set(etfs['code'])
summary={'created_on':'2026-10-24','generator':'pandas '+pd.__version__,'rows':len(df),'columns':len(df.columns),
         'record_types':df['紀錄類型'].value_counts().to_dict(),'phase1_exchange_candidates':len(phase1),
         'requirements':len(needs),'etfs':len(etfs),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
         'checks':['unique IDs','368 exact exchange operation IDs','all 57 first-phase candidates','all 66 requirements','all 30 ETF codes preserved','FinMind dataset IDs in current official enum','all upstream IDs resolve','UTF-8 BOM pandas roundtrip exact','formula-prefix scan'],
         'scope_limit':'Catalog completeness is against the agreed requirements; entitlement, data quality, PIT and exact ETF coverage remain unverified.'}
(ROOT/'qa/implementation-data-sources-checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
