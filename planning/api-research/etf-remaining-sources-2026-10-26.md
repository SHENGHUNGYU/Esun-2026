# 剩餘八檔 ETF 持股來源補完研究

研究／下載日：2026-10-26（UTC fetched_at 保留實際時間，部分為台北10/26對應UTC10/25）。本次依既有研究與 raw 接續，未重做已完成的22檔、未修改核心程式／網站／既有主研究筆記／全域 summarize.py。

**新增六份來源明示評價日的完整股票快照，另將台新00986A既有36股轉為日期仍待核實的條件式快照；國泰00400A持續受阻。** 本次七份 JSON 全通過 `src/esun_research/benchmarks.py` 的 `Benchmark.model_validate_json`，主 raw 與 NAV／身分／公開說明書 supporting hash 均核對存在且一致。型別及 hash 通過不是官方 Active Share 或日期政策認證。

補充機器清單：`artifacts/etf-acquisition-20261026/remaining-sources-manifest.json`。沒有改寫舊 `manifest.json`，避免混淆舊結論；使用本批資料時須一併讀補充清單。

| ETF | 完整股票筆數 | 原NAV權重相加 | 股票評價日 | PCF適用日 | 狀態／輸出 |
|---|---:|---:|---|---|---|
| 00981A 統一 | 50 | 0.9581 | 2026-10-22 | 未提供 | `normalized/00981A.json`；明示日期 |
| 00988A 統一 | 38 | 0.9666 | 2026-10-21 | 未提供 | `normalized-other-dates/00988A.json`；明示日期 |
| 00403A 統一 | 50 | 0.8933 | 2026-10-22 | 未提供 | `normalized/00403A.json`；明示日期 |
| 00986A 台新 | 36 | 0.905637 | **暫列2026-10-21，推導待核** | 2026-10-23 | `normalized-other-dates/00986A.json`；不能當正式日期驗收通過 |
| 00989A 摩根 | 69 | 0.974181 | 2026-10-21 | 2026-10-27 | `normalized-other-dates/00989A.json`；明示日期 |
| 00401A 摩根 | 56 | 0.920388 | 2026-10-22 | 2026-10-27 | `normalized/00401A.json`；明示日期 |
| 00400A 國泰 | — | — | — | — | 既有PCF與另一官方基金頁均403；沒有製造快照 |
| 00404A 聯博 | 51 | 0.90373617 | 2026-10-22 | 2026-10-27 | `normalized/00404A.json`；明示日期 |

所有輸出保留原始NAV權重，不重正規化；股數為全基金實際股票持有表，不以每基數申贖籃子替代。0%但正股數的列保留，期貨／選擇權等按官方分類排除。

## 統一：正常匿名初始化後取得三檔完整內嵌資料

[統一官方首頁](https://www.ezmoney.com.tw/)直接無cookie請求會302自我迴圈；採標準 `http.cookiejar.CookieJar` 與 `HTTPCookieProcessor` 的普通匿名初始化後，首頁200。沒有改UA／IP、輸入私人憑證或破解安全檢查；匿名cookie只留記憶體，不保存cookie jar或回應認證header。

首頁直接明示：49YTW＝00981A、61YTW＝00988A、63YTW＝00403A，依實際 href 取得：

- [00981A官方基金投資組合頁](https://www.ezmoney.com.tw/ETF/Fund/Info?fundCode=49YTW)
- [00988A官方基金投資組合頁](https://www.ezmoney.com.tw/ETF/Fund/Info?fundCode=61YTW)
- [00403A官方基金投資組合頁](https://www.ezmoney.com.tw/ETF/Fund/Info?fundCode=63YTW)

三頁皆200，原檔為 `raw/ezmoney-{code}-info.html` 及 `.html.meta.json`。來源頁自身 Vue 程式明示讀取 `DataFund`、`DataAsset`、`DataAssetDetailSchema` 的 `data-content` JSON；只解析HTML字面內容，不執行遠端程式。`DataFund.sStockNo/sFundCode`再次核對身分，`DataAsset[AssetCode=ST].Details` 是全股票表。

評價日用**每一股票列的 TranDate**，不是 EditTime、DataAsset.EndDate 或今日抓取日。00981A／00403A全部逐股明示10/22；00988A全部10/21。後者後台EditTime是10/22，仍保留股票評價日10/21。NAV用同頁 `AssetCode=NAV` 的 Value；權重用欄位schema明示「持股權重」的 NavRate 百分點。Info頁沒有獨立PCF適用日，所以設 null，沒有猜日期。

00981A及00403A逐股Amount/NAV核對均在0.005百分點披露誤差內。00988A跨國股票原Amount包含多幣別，USD_EXRATE部分非USD為1且USD換算也有小差，**未以不完整匯率重造權重、未宣稱完整FX等價驗證**；直接保存官方NavRate。市場映射保留 TW、US、JP、KR、DE、HK、CN，依官方DetailCode字尾及MoneyType交叉核對，不把原股與ADR混合。

解析器：`normalize_remaining_ezmoney.py`。另外保存 `ezmoney-{code}-embedded-assets.json` 作可讀的衍生檢查檔；Benchmark 主hash仍指官方原HTML，衍生JSON沒有被冒充新的官方HTTP回應。

## 摩根：公開產品資料介面含完整PCF股票表

先前原始產品頁已存在。其[00401A官方產品頁](https://am.jpmorgan.com/tw/zh/asset-management/twetf/products/jpmorgan-taiwan-taiwan-equity-high-income-active-etf-tw00000401a1)及由[00989A官方入口](https://am.jpmorgan.com/tw/zh/asset-management/twetf/funds/jpmorgan-us-tech-leaders-etf/)實際列出的[00989A產品頁](https://am.jpmorgan.com/tw/zh/asset-management/twetf/products/jpmorgan-taiwan-u-s-tech-leaders-active-etf-tw00000989a5)，提供ISIN與公開 `FundsMarketingHandler` 載入程式。

兩產品頁直接明示的content/dam Excel連結本次各403，已停止該下載路徑。另依同頁正常產品應用的 `getUSFundData`，讀取公開投資組合顯示接口；沒有以任何身分登入，也沒有對受阻路徑改UA、IP或加憑證重試：

`GET https://am.jpmorgan.com/FundsMarketingHandler/product-data`

參數由公開程式取得：`cusip=TW00000401A1`或`TW00000989A5`，`country=tw,role=twetf,language=zh,userLoggedIn=false,version=9.18_1791879504`。兩者均HTTP200、`error=null`。公開bundle與loader皆保留raw與hash。

完整股票位於 `fundData.holdings.pcfEquityHoldings.data`，effectiveDate與**所有逐股navDate**一致，00401A為10/22、00989A為10/21；`breakdowns.m12Details`另明示同日基金NAV與10/27 PCF適用日。股權權重用 `marketValuePercent/100`，逐股 `marketValueBase/NAV`與權重在原披露精度內一致。沒有把兩個欄位中的「Percent」誤讀成已是小數。

00989A保留69筆（含DepRec／美國存託憑證與New York Registered Shares），使用美國交易市場命名空間；例如 `US:TSM`與`TW:2330`分開。00401A為56筆台股。股票筆數以完整pcfEquityHoldings陣列驗證，不用可能月頻／空的numberOfHoldings或只取前十大。

原檔 `raw/jpm-{code}-product-data.json`、解析器 `normalize_remaining_jpm.py`；身分supporting hash分別綁既有00401A官方產品HTML與新取00989A產品HTML。URL query參數只有公開查詢設定，沒有認證資訊。

## 聯博：正確ISIN的完整持股與NAV介面

[00404A官方產品頁](https://www.abfunds.com.tw/zh-tw/funds/etf/active/equities/abitl-taiwan-momentum-equity-premium-income-50-active-etf.-.TW00000404A5.html)的共用PCF選單會連到其他基金，這只是共用入口，**沒有拿其他基金的持股冒充00404A**。該[公開PCF介面](https://www.abfunds.com.tw/zh-tw/etfs/pcf.TW00000980D8.html)的React程式明示 fundApiUrl、countryCode、lang、currentSegmentName 與可選基金ISIN如何組成個別查詢。使用產品頁已確認的00404A ISIN，依程式呼叫：

- [正確00404A完整持股](https://webapi.alliancebernstein.com/v2/funds/tw/zh-tw/investor/TW00000404A5/holdings)
- [正確00404A NAV與PCF資訊](https://webapi.alliancebernstein.com/v2/funds/tw/zh-tw/investor/TW00000404A5/basket)
- [正確00404A身分對照](https://webapi.alliancebernstein.com/v2/funds/tw/zh-tw/investor/TW00000404A5/shareclasses)

三者皆200，shareclasses明示fundNumber=00404A／isin=TW00000404A5。持股 `domesticHoldings` 的 equity分類51筆，asOfDate=10/22/2026；期貨1列、選擇權2列保留在raw但不列equity。holdingPerc是NAV百分點，逐股holdingValue/NAV差小於0.0000005百分點；basket的aum=3,890,457,172、navAsOfDate=asOfDate=10/22，announcementDate=10/27單獨保留。

數筆holdingShares帶JSON浮點尾差（例如1294499.9999999998），僅在距整數小於0.000001股時轉整數，原值永久留raw。解析器 `normalize_remaining_ab.py`；兩份supporting hash綁basket與shareclasses。

## 台新00986A：完成格式，但日期仍是條件式

沿用既有 `raw/00986A-pcf-20261027.html`（[原請求](https://www.tsit.com.tw/ETF/Home/Pcf/00986A?DataDate=2026-10-27&FundType=ALL)），不重新下載該成功raw。36股票全表、全基金NAV537,463,447及原股數／NAV權重可讀；逐股加總90.5637%，表內股票合計90.5636%，保留披露微差。

日期衝突保留：PUB_DATE=DATA_DATE=MAX_DATE為10/23；「實際申購總價金／差額」10/21；「預估發行受益權單位數」10/22；**股票表沒有獨立日期標籤**。因而將10/21只作條件式研究封存，`valuation_date_basis=official_pcf_timing_inference`，不可標10/22通過，亦不可說10/21已獨立證實。

從[00986A官方基金頁](https://www.tsit.com.tw/ETF/Home/ETFSeriesDetail/00986A)實際href下載[本基金公開說明書](https://www.tsit.com.tw/ETF/Images/ETF_ASSET/Open/638887127859141633.pdf)。PDF第10頁／印刷第8頁十四(二)1規範NAV結算後公告次營業日現金申購買回清單，已綁PDF hash；該通則**仍不足以獨立證明跨國股票表評價日**，此限制明寫在快照provenance_notes。

解析器 `normalize_remaining_taishin.py`，市場TW/US/JP/GB/NL/FR/DE依原始Bloomberg字尾分開，NBIS UW亦是美股。此檔型別通過只是格式完成，納入正式比較前仍需投信／主辦方釐清股票日期。

## 國泰00400A：持續阻擋與停止條件

既有[官方PCF路徑](https://www.cathaysite.com.tw/ETF/purchase?code=EA&name=Cathay+Taiwan+High+Dividend+Momentum+Active+ETF)已403，沒有重試。另查官方搜尋明示的獨立[基金投資組合頁](https://www.cathaysite.com.tw/fund-details/EEA)，直接HTTP亦403，將失敗metadata寫 `raw/cathay-00400A-details.html.meta.json` 並停止；未透過其他機器、UA或登入繞過。

搜尋／閱讀工具能讀到官方基本資訊與淨值摘要，但沒有完整當期股票全表與可驗證公開下載，不能拿摘要、月報或第三方持股代替。未猜cwapi內部ID、未建立00400A正規化檔。仍需投信官方公開完整匯出、正常可讀頁面或主辦方提供的benchmark資料。

## 驗證與交接限制

- 七檔均以專案`.venv`執行Benchmark型別驗證；原始內容SHA-256與全部supporting hashes檢查通過，補充manifest記錄正規化檔hash、原始路徑、日期與持股數。
- 原HTTP回應metadata緊接下載寫入，包含實際fetched_at；沒有將10/26取得的資料回填為10/22 first_seen，不能插入先前cutoff的run。
- 完整資料不等於同日覆蓋；本批新增4份10/22來源明示快照（統一2、摩根1、聯博1），另2份來源明示10/21（統一1、摩根1），以及台新1份日期待核的條件式10/21檔。原有跨日與00987A推導日期限制繼續有效。
- 本次只建立可重現解析與封存證據，尚未建立這些新來源的每日自動更新／可靠度驗收，也沒有擅自解除30檔同日覆蓋或官方Active Share日期／算法阻擋。
