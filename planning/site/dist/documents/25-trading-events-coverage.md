# 停止買賣及公司行動來源覆蓋研究

查閱／實測：2026-10-26。只用官方公開來源及其頁面實際引用的 GET／唯讀 POST；未登入、未取憑證、未繞過安全限制。原始 HTML、JSON、頁面引用 JS、URL／參數／HTTP／UTC fetched_at／SHA-256 位於 `artifacts/trading-events-research-20261026/`。機器可讀介面盤點是該目錄的 `endpoint-inventory.json`，下載證據為 `manifest.json`。

**結論：可補進上市財務異常正式停牌、上市櫃減資／面額變更的停止與恢復日期，以及終止上市櫃清單。但仍未取得涵蓋所有組織異動、分割、合併／股份轉換的完整事件與對價資料，不能移除整體 scope blocker。** 公告清單可作發現入口；結案／申報生效不等於實際換股／可交易日期。

## 1. 現況與新增來源範圍

已讀 `src/esun_research/risk.py` 及既有 API 研究。本程式已接 11 feeds：TWSE-063 暫停／恢復、072 變更交易、108 處置、116 注意、126 除權息；TPEx-003 當日暫停／恢復、004 歷史暫停／恢復、015 除權息、016 交易狀態、020 注意、021 處置。本研究不重新下載這些 feeds。

`assess()` 明確保留 `corporate_action_scope_incomplete`、`trading_status_scope_incomplete`；這是正確的現況陳述。短期訊息面暫停／恢復不等於長期正式停止買賣，除權息不含所有減資／面額變更／企業分割，注意或處置也不等於全面不可交易。

[TWSE 停止買賣頁](https://www.twse.com.tw/zh/listed/violations/stop.html) 明示只列因財務業務異常停止買賣的公司；公司組織異動、改組、減資等原因須依 MOPS 重大訊息。**不得把此表空白解讀成所有上市股票都可買賣。** 本次 JSON 列 1589 永冠-KY，正式停牌開始 115/04/07；該頁標題的 115/10/26 是頁面資料日期，不是事件開始或首次公告時間。

## 2. 上市：實測成功的公開 JSON

官方頁面使用 `data-api`，引用的 `web-report.js` 以 `cfg.apiHost.rwd + /zh + data-api` 組成 GET，`main.js` 的正式根路徑是 `/rwd`。以下都是由此查證，沒有猜測內部 ID。公共 JS 其他無關設定未作認證使用。

| 事件／官方說明頁 | 可機讀 endpoint（GET，均帶 `response=json`） | 已驗證參數／內容 |
|---|---|---|
| [財務業務異常停止買賣](https://www.twse.com.tw/zh/listed/violations/stop.html) | `https://www.twse.com.tw/rwd/zh/violation/stop` | 無日期表單；回傳 `stat=ok, tables[]`；第一表 `fields/data`，另有空 `{}` 表物件，不能假設所有 table 都含欄位 |
| [終止上市公司](https://www.twse.com.tw/zh/listed/suspend-listing.html) | `https://www.twse.com.tw/rwd/zh/company/suspendListing` | `date=20260101` 選年；4 列，含終止上市日期／公司名稱／上市編號。此回應無 stat，不能強制套用其他報表的 envelope |
| [減資預告](https://www.twse.com.tw/zh/announcement/reduction/twtavu.html) | `https://www.twse.com.tw/rwd/zh/reducation/TWTAVU` | 路徑確為 **reducation**；無日期表單；2 列。停止買賣日期、代號、名稱、恢復日期、減資換股率、原因、每股退還股款、減資後現增配股率、現增認購價、詳細資料、恢復參考價、參考價試算 |
| [減資恢復價](https://www.twse.com.tw/zh/announcement/reduction/twtauu.html) | `https://www.twse.com.tw/rwd/zh/reducation/TWTAUU` | `startDate=20260101&endDate=20261231`，17 列；恢復日期、代號／名稱、停止前收盤、恢復參考價、漲跌停、開盤競價基準、除權參考價、原因、詳細資料 |
| [面額變更預告](https://www.twse.com.tw/zh/announcement/change/twtb7u.html) | `https://www.twse.com.tw/rwd/zh/change/TWTB7U` | 無日期表單；1 列；停止／恢復日期、代號／名稱、換股率、變更前／後面額、詳細資料、恢復參考價、試算 |
| [面額變更恢復價](https://www.twse.com.tw/zh/announcement/change/twtb8u.html) | `https://www.twse.com.tw/rwd/zh/change/TWTB8U` | `startDate/endDate=YYYYMMDD`，2026 全年 2 列；恢復日期、代號／名稱、停止前收盤、恢復參考價、漲跌停、競價基準、詳細資料 |
| [公文公告](https://www.twse.com.tw/zh/announcement/announcement/list.html) | `https://www.twse.com.tw/rwd/zh/announcement/announcement` | `startDate/endDate=YYYYMMDD, keyword`；2026 年 `keyword=合併` 僅 2 列，為證券商合併營業公告，**不足以證明完整涵蓋上市發行人合併事件**。欄位項次、發文日期、文號、主旨、實際回傳 id；不猜 ID |

回傳日期多為民國 `115/11/12`；公告發文日期另有 `中華民國115年03月31日`。價格／退款為元；換股率為新股數／原股數的比例，不是百分比。TWTAVU notes 定義減資換股率＝減資後股數／減資前股數；TWTB7U 定義面額換股率＝舊面額／新面額＝新股數／舊股數。兩者分開建模，不可一概使用 `1-ratio`。

樣本：1808 減資預告為 115/11/12 停止、11/23 恢復、換股率 0.79999999、退 2 元；6949 面額變更為 115/08/27 停止、09/07 恢復、10 元改 0.5 元、換股率 20。保留精確 decimal 字串；不要從近似展示值推造官方股數取整或退款支付日。

TWTAUU 日期查詢頁明示自 2011-01-01 提供，面額恢復頁日期元件起點是 2019；本次未逐年驗證。預告表無公開歷史日期表單，不能自行加 date 後就宣稱取得歷史預告版本；歷史恢復價也不是當時已公布的完整預告。

## 3. 上櫃：實測成功的公開 POST

官方 `tables.js` 明示使用唯讀 `$.post`，`API_PATTERN=/www/{LANG}/{ACTION}`。以下 path 均取自官方頁面 `tables.init(action:...)`；正式根 `https://www.tpex.org.tw/www/zh-tw/`，表單都帶 `response=json`。POST 是查詢，不是寫入操作。

| 官方頁面 | action／參數 | 已實測 envelope／欄位 |
|---|---|---|
| [終止上櫃](https://www.tpex.org.tw/zh-tw/mainboard/listed/delisted.html) | `company/deListed`；`code=, date=, reason=-1, paging-offset=0, paging-size=10` | `stat=ok, tables[0]`，7 列／totalCount=7；股票代號、公司名稱、終止上櫃日期、原因、公司資料網址。date 空白是本次預設，不代表所有年度；UI 有年度選擇，本次未驗證指定年序列化。reason -1 為全部，0 為被合併／股份轉換，1 為轉換設金控，2 為轉上市，其他依頁面 option |
| [減資預告](https://www.tpex.org.tw/zh-tw/announce/market/reduction.html) | `bulletin/decap`；無額外日期表單 | 4 列；代號、名稱、停止日期、換股率、每股退款、原因、恢復日期、現增配股率／認購價、恢復價。回應 date=20261023，是資料表日期 |
| [面額變更預告](https://www.tpex.org.tw/zh-tw/announce/market/change.html) | `bulletin/pvChgAnn`；無額外日期表單 | `stat=ok, tables[0].data=[], totalCount=0`；欄位仍存在：代號／名稱、停止日期、換股率、前後面額、恢復日期／價 |
| [減資恢復參考價](https://www.tpex.org.tw/zh-tw/announce/market/reduction/reference.html) | `bulletin/revivt`；`startDate=2026/01/01,endDate=2026/10/26` | 19 列；恢復日期、代號／名稱、最後日收盤、恢復價、漲跌停、開始交易基準、除權參考價、原因、詳細資料 HTML |
| [面額變更恢復參考價](https://www.tpex.org.tw/zh-tw/announce/market/change/reference.html) | `bulletin/pvChgRslt`；同上日期參數 | 5 列；恢復日期、代號／名稱、最後日收盤、恢復價、漲跌停、基準價、詳細資料 HTML。詳細 HTML 另含停止日期／換股率／前後面額 |
| [公告查詢](https://www.tpex.org.tw/zh-tw/announce/market/announce.html) | `bulletin/announcement`；`startDate=2026/10/01,endDate=2026/10/26,cate=2或4,txtKeyword=` | 類別2：除權息增減資換股，6 列；類別4：變更交易停止終止股票，4 列。項次、資料日期、文號、主旨、詳細資料 URL；也可能含興櫃，須另過濾市場 |
| 公告詳細頁（由上一表真實 URL 跟隨） | `bulletin/annDetail`；原樣使用 URL query 的 `content_file,docId` | `stat=ok,data{downHtml,date,number,subject,depend,content,notes,files}`；date 為發文日，content 是公告 HTML；只用伺服器實際提供的參數，不產生／猜測 ID |
| [減資、合併、受讓收購分割申報案件](https://www.tpex.org.tw/zh-tw/service/pi/statement/apply/company.html) | `announce/processStk`；`date=` | 34 列；代號、公司型態、結案類型、名稱、承銷商、案件類別、金額／幣別／發行價、收文／補正／停止生效／解除／生效／廢止／撤回／退件日、性質、備註。**這是申報處理進度，不是證券停止買賣或合併交割時程表** |

完整 JSON URL 與每次參數見 raw manifest／endpoint inventory。`revivt` 回復日期為民國 7 碼 `1150112`，詳細 HTML 為 `114/12/31`；終止上櫃用 `115-10-16`。日期解析需按欄位，不把 `Date` 統一當 published_at。

`revivt` 8093 詳細 HTML 明示每千股換 600 股，可補停止日；`pvChgRslt` 8932 詳細明示 115/02/25 停止、03/09 恢復，5 元改 2.5 元、換股率 2。表格「詳細資料」是有用資料，不可像網站展示流程那樣直接 splice 丟棄。

公告詳情成功樣本為 4207 環泰，文號證櫃監字第11500064011號、發文 115/10/20：每千股換 950 股、每股退 0.5 元；115/10/29–11/06 暫停櫃檯買賣；11/06 換發基準；11/09 新股開始換發／交易。**停止過戶日期 11/02–11/06 與停止交易日期不同**，不得取錯。詳情下載原文是 `https://www.tpex.org.tw/storage/eb_data/11510/11500064011.html`（由 API 真實回傳）；本次保存 annDetail JSON 已含正文。

額外可見入口：[股票增減資掛牌及 TDR 公告](https://www.tpex.org.tw/zh-tw/announce/market/reduction-tdr.html) 的 `bulletin/tdr`，表單 `sect,startDate,endDate,mkt,code`，其中 sect 21／22 是本國／第一上櫃公司減資新股。本次只保存頁面，**未呼叫該 JSON、未驗證空值與欄位**，不算已接通來源。

## 4. 空資料、時間與仍缺的事件

- 已觀察 TWSE TWTB8U 2026-10-25 至同日：HTTP 200、`stat=OK, fields完整, data=[]`。TPEx pvChgAnn 也有 `stat=ok,data=[],totalCount=0`（在 tables[0]）。終止上櫃 `code=2330` 查詢得到同樣明確零列。這些只表示該查詢範圍內無記錄，不表示全市場／全類事件無風險。
- HTTP 200 也能是安全拒絕 HTML：TWSE 預告表公開 notes 指向的 [MOPS MIS 公告](https://mops.twse.com.tw/server-java/t39sb01?quick=1) 本次回「因為安全性考量，您所執行的頁面無法呈現」。已保留 raw，停止該路徑；未登入或改 IP／代理繞過。不能當成合法無公告。
- 發文日／表格出表日不等於首次可見時間。沒有時間的發文日期不足以證明當日早晨 cutoff 前可用；前瞻系統採實際 first_seen/fetched，不回填。未來生效事件可在公告已捕獲時先進風險日曆；不因 effective_at 大於 cutoff 而丟棄。歷史回放不能把今日下載的事件整表視為當時已知。
- 終止日期不是最後交易日，不是公告日。預告停止日不是換發基準日，恢復參考價不是實際成交價或官方競賽結算價。退還股款欄位未給現金支付日；合併對價需現金／股票／比例／存續證券／零碎股處理／交割日，不可用停止或終止清單推算。
- 上市櫃面額變更涵蓋部分經濟上的股票拆分；**企業分割減資與 ETF 分割不是同一件事**。兩交易所另有 ETF 分割／反分割預告與恢復頁，官方選單可見；固定普通股 universe 不應把 ETF 事件當股票企業分割資料。分割減資 TWTAVU 官方亦指向 MOPS 詳細公告，故尚缺對價分配與新證券映射。
- 本次並未驗證一筆完整普通股合併／股份轉換的「公告→停止→換股→終止／新股上市」全鏈；TPEx processStk 的申報案件與終止原因只能找線索，不能作已完成合併交割。TWSE 公文查詢搜尋合併只得到券商營業公告亦不足。**合併與組織異動完整覆蓋仍是缺口。**

## 5. 實作前採用條件（本次未改核心程式）

1. 新來源逐一固定 envelope／欄位與合法空值 fixtures；讀取完整頁數並比較 totalCount，不能只抓前 10 筆。靜默缺欄／HTML／錯誤訊息均算 unknown，不能變成空集合。
2. 新事件以原始證據索引保留 `source_url,raw_ref,raw_row,fetched_at,first_seen_at,announcement_date,effective_start,resume_date,ratio,cash_per_old_share`；缺值保持 unknown，現有 sidecar 可承載，不增塞官方 D-Plan 自訂欄位。
3. 只有證明事件區間、參考價與股數／現金帳務處理後才解除該個股阻擋；unknown 事件禁止自動換股或當日買賣。資料捕獲新鮮不能證明全類事件齊全。保留既有兩個 scope blocker，直到補完缺口且獨立驗收。
4. 測試至少包括正式停牌跨日／恢復邊界、減資跨 reference→trade gap、20 倍面額轉換、換股率非整數、現金支付日未知、終止前最後可交易日、停過戶和停交易不同、部分頁數、合法零列、安全拒絕200、歷史公告僅日粒度。

官方頁面／實際請求證據均留於 raw；本地與核心程式／網站未修改，未使用遠端設備，未對完整可參賽覆蓋作保證。
