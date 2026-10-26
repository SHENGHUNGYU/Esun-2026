# 六個月獨立交易日曆與TAIEX日資料驗證

研究／下載：2026-10-26。**2026-04至2026-09共124個交易日已由官方年度開休市表＋兩交易所額外休市公告獨立重建，並與官方TAIEX六份月日資料以及現有兩市場股票日期聯集完全一致。** 同時保存124筆TAIEX OHLC／收盤點數，供後續Beta資料工程；本次沒有計算Beta、績效或宣稱完成PIT回測。

所有資料、原始回應、官方頁／公開程式證據及manifest在 `artifacts/history-calendar-20261026/`。未修改核心程式、網站或既有歷史股票archive；沒有登入、使用憑證、代理或繞過拒絕。

## 先檢查既有TWSE-067，避免重抓

唯讀檢查 `artifacts/live-20261024/index.sqlite` 中最近成功TWSE-067 capture，原ref是 `objects/6800c13392d34ae27a0dc9327b88d28f92f2112e369bf266a819116122f27ee1.bin`，實際fetched_at=`2026-10-24T14:06:07.492495+08:00`。

該[OpenAPI](https://openapi.twse.com.tw/v1/indicesReport/MI_5MINS_HIST)舊raw只有15筆，日期1151001–1151022，全部屬2026-10，**不含本次六個月**。本次未重新呼叫或自行加日期參數至OpenAPI。既有內容複製為 `existing-TWSE-067.json`，保留原fetched_at／hash／原始ref，不冒充新下載。

## 端點及每一參數的官方依據

### TAIEX月歷史與年度日曆

- [TAIEX官方查詢頁](https://www.twse.com.tw/zh/indices/taiex/mi-5min-hist.html)原HTML明示 `data-api=/TAIEX/MI_5MINS_HIST`，表單`name=date`、`data-date=b:1999,e:0,f:M`；頁面文字明示自1999-01-05提供。沒有依第三方文章猜路徑。
- [開休市官方頁](https://www.twse.com.tw/zh/trading/holiday.html)明示 `data-api=/holidaySchedule/holidaySchedule`，`name=date`、`f:Y`。
- 兩頁實際引用的 `main.js` 設正式報表根`/rwd`；[web-report.js](https://www.twse.com.tw/res/js/web-report.js)的doQuery組成 `cfg.apiHost.rwd + /zh + data-api`，序列化正式表單、刪除顯示用yy/mm/dd，再加`response=json`與GET。日期控制程式將年月日組成 `YYYYMMDD`，月份／年份選擇以1月／1日作錨。已封存既有成功取得的官方web-report.js，保留原下載時間。
- 本次請求為 `GET https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?date=20260401&response=json`，依相同**公開月份表單**依次選20260501–20260901；年度日曆為 `GET https://www.twse.com.tw/rwd/zh/holidaySchedule/holidaySchedule?date=20260101&response=json`。全部HTTP200且合法JSON。

每月回應`stat=OK`、date等於請求月份、title含對應民國年月、fields為日期／開盤指數／最高指數／最低指數／收盤指數。六個月不是每日endpoint硬加未文件化日期參數，也不是OpenAPI最新資料假裝歷史。

### 額外休市：必須補年度日曆以外公告

年度日曆只有預定假期，不能直接當實際成交日全集。六個月131個平日，扣6個平日的預定休市後為125日；尚須扣**2026-07-10額外全日休市**。

- [TWSE新聞列表](https://www.twse.com.tw/zh/about/news/news/list.html)原HTML明示`data-api=/news/newsList`及`tag,startDate,endDate`表單，日期格式為年選擇`f:Y`。GET `/rwd/zh/news/newsList?startDate=20260101&endDate=20260101&tag=7月10日&response=json`返回真實zhId。此年選擇表示2026年度，不把start/end兩個0101誤解為僅1月1日。列表亦有另一篇非休市結果，因此按標題人工核對，不假設搜尋字串精確過濾。
- 跟隨實際回傳ID到[官方休市新聞頁](https://www.twse.com.tw/zh/about/news/news/content.html?8a8216d69ef76943019f46cb86bf0111)。其form明示`/news/newsDetail`；[web-news.js](https://www.twse.com.tw/res/js/web-news.js)明示把裸query轉成id。GET `/rwd/zh/news/newsDetail?id=8a8216d69ef76943019f46cb86bf0111&response=json`返回PDF路徑；同JS明示前綴`/staticFiles`，因此直接下載[原始休市新聞PDF](https://www.twse.com.tw/staticFiles/news/news/tsecnews/8a8216d69ef76943019f46cb86ae0110.pdf)，不是猜內部ID或檔名。
- PDF發文日期115/07/09，正文確認巴威颱風影響，115/07/10集中交易市場全日休市。JSON帶`date=202607092011`，頁面JS將它顯示為2026-07-09 20:11；這是來源發布欄位，與本次fetched_at不同，也不代表本系統當時曾觀測。
- [TPEx新聞列表](https://www.tpex.org.tw/zh-tw/about/company/press/list.html)明示action=`news/list`，公開API_PATTERN為`/www/zh-tw/`，tables.js採唯讀POST。表單參數`startDate=2026/07/01,endDate=2026/07/13,keyword=休市,response=json,paging-offset=0,paging-size=10`，回傳唯一新聞與真實ID22926。
- 跟隨[該官方新聞詳情頁](https://www.tpex.org.tw/zh-tw/about/company/press/detail.html?22926)，依頁面action=`news/detail`及通用template程式的裸query→id轉換，POST `/www/zh-tw/news/detail`、`id=22926`，取得完整正文。115/07/09發文，確認7/10上櫃、興櫃等證券及衍生市場停止交易一日。沒有猜ID。

兩個市場均有各自官方額外休市證據；不是僅因股票或指數缺7/10列就自行判斷休市。

## 核對結果

| 月份 | 獨立重建交易日／TAIEX列數 | 首日 | 末日 |
|---|---:|---|---|
| 2026-04 | 20 | 04-01 | 04-30 |
| 2026-05 | 20 | 05-04 | 05-29 |
| 2026-06 | 21 | 06-01 | 06-30 |
| 2026-07 | 22 | 07-01 | 07-31 |
| 2026-08 | 21 | 08-03 | 08-31 |
| 2026-09 | 20 | 09-01 | 09-30 |
| 合計 | **124** | 2026-04-01 | 2026-09-30 |

平日的年度預定休市：4/3、4/6、5/1、6/19、9/25、9/28。4/3與4/6的說明為「補假」，不能只搜尋「放假」關鍵字漏掉；週末4/4、4/5不重複扣平日。另扣7/10颱風，`131−6−1=124`。

唯讀核對既有18,481列股票Parquet，TWSE與TPEX各自日期聯集都與**獨立日曆及TAIEX日期**相等；兩市場missing／extra皆為空。`validation.json`記錄既有股票archive SHA-256及比較結果。此結論針對市場日期覆蓋，不代表每檔股票所有日期都有交易或已驗證公司行動。

3718／7828掛牌前缺列仍依原始股票研究的掛牌日期與`*`註記處理；本次沒有填補掛牌前119列、推造前身／原市場映射，或把個股缺列等同全市場休市。完整原歷史股票archive未改動。

## 可交付資料與界線

- `twse-taiex-202604.json`至`twse-taiex-202609.json`：6份原始官方月OHLC。
- `taiex-daily-202604-202609.csv`：124筆，date與OHLC點數，帶source_raw_file／row／sha256。指數單位是**點**；不是股票元價、不是報酬率、也不是含股息總報酬指數。
- `calendar-202604-202609.json`：官方預定假期、獨立額外休市證據、完整124日與每月分組。
- `validate_calendar.py`：驗證source月份、唯一日期、OHLC大小關係、獨立日曆與兩市場聯集完全相等。`validation.json`為結果，`derived-manifest.json`為派生檔hash。
- `manifest.json`記錄每個原回應URL、參數、HTTP、實際fetched_at與SHA-256。引用既有raw時保留原fetched_at並記reused_from，沒有把複製時間當新觀測。

本次歷史官方查詢回應不含每筆首次發布／版本修訂紀錄。雖新聞額外休市具來源發文時間，仍不能倒填本系統的歷史first_seen；指數資料亦不可標成當時即時快照。未計算Beta、策略績效、交易成本或收益；後續Beta研究還須明確收益口徑、股票公司行動及對齊／缺失規則。

## 失敗／無資料亦保留

TPEx既有公告表`bulletin/announcement`類別9，在7/1–7/13回合法`stat=ok, tables[0].data=[], totalCount=0`，因此未拿空表證明無休市，而改用官方新聞列表／全文查證。另由官方開休市頁實際action=`bulletin/tradingDate`與date表單做一次查詢，HTTP200但內容是404 HTML，已標`invalid_payload_html_404_page_not_calendar`，沒有作交易日證據或猜新參數反覆重試。整體結論由成功的TWSE年度表、兩市場休市新聞與六份指數原回應支持。
