# 30 檔主動 ETF 實際持股來源盤點（2026-10-24）

本次依競賽指定30檔逐筆核對。**已建立30筆來源盤點；實際封存的可計算持股快照為0檔，目標10/22日期通過驗證為0檔，Active Share全覆蓋仍受阻。** 本文件只盤點來源，沒有把名單當作持股，也沒有呼叫付費API、登入或尋找token。

## 閱讀結果

- 4檔官方頁可見至少15筆股票列：00986A、00987A、00996A、00410A。其中只有00410A在本次頁面明列10/22資料日期；台新同頁包含不同PCF／申贖日期，另需確認持股評價日。兆豐搜尋索引為舊日期，直接重抓403，未繞過限制。
- 3檔只見部分持股：00982A、00985A、00992A。群益頁面顯示10筆並提供展開全部；未展開取得第11–15筆前不能計算。野村部分索引為動態頁或前10筆。
- 23檔定位到官方產品／總覽／官方產品文件，但尚未驗證每日持股明細。這不代表該投信不公布持股，只表示本次有界盤點未完成下載驗收。
- 公開可閱讀不等於已確認批次抓取或再散布授權。正式接入須遵守站方使用條款、節流與下載介面；不繞過驗證與存取限制。

## FinMind 的權限與涵蓋限制

FinMind官方文件將 `TaiwanStockActiveETFHolding` 與 `TaiwanStockActiveETFHoldingChange` 列為 **Sponsor**；`TaiwanStockActiveETFInfo` 才是 **Free**。持股提供日期、ETF代碼、成分代碼／名稱、資產類型、股數、權重、市值與幣別。文件說明整體起日2025-05-05，各ETF起日不同；未提供已驗證的指定30檔逐日完整性保證。不能只因基本名單有代碼就認定持股資料完整。Change含申贖造成的等比例股數變化，不能直接視為經理人買賣。[官方API與資料集文件](https://finmind.github.io/llms-full.txt)；本地封存 `planning/api-research/finmind/llms-full.txt` 的對應段落一致。

此次未呼叫Sponsor資料集，沒有推定使用者方案。可用路線是逐投信公開下載，或使用者另行確認既有FinMind權限及用途授權後小量驗證；此報告不預授權付費。

## 逐檔清單

日期為此次官方頁／索引觀察到的日期，不代表已下載驗證，空白表示未確認。代碼一律保留字串。

|代碼|投信|狀態|頁面觀察日期|已核對官方入口／缺口|
|---|---|---|---|---|
|00980A|野村投信|官方入口，未驗證明細|未確認|[官方來源](https://www.nomurafunds.com.tw/ETFWEB/product-description?fundNo=00980A&tab=Shareholding)：持股頁已定位；直接讀取只回傳動態頁殼，未驗證15筆與資料日期。|
|00982A|群益投信|只見部分持股|2026-10-22|[官方來源](https://www.capitalfund.com.tw/etf/product/detail/399/buyback)：公開頁可見10筆股票及權重、股數；展開全部／下載尚未驗證，不能替代前15大。|
|00981A|統一投信|官方入口，未驗證明細|未確認|[官方來源](https://www.ezmoney.com.tw/events/2025TGA/00981A-ezguide.pdf)：僅核對官方產品指南；主站目前讀取不可用，日持股入口未驗證。|
|00983A|中國信託投信|官方入口，未驗證明細|未確認|[官方來源](https://www.ctbcinvestments.com.tw/Product/List?Kind=1&ProductEtfNo=27)：官方基金總覽包含代碼；直接讀取要求JavaScript，日持股明細尚未驗證。|
|00984A|安聯投信|官方入口，未驗證明細|未確認|[官方來源](https://etf.allianzgi.com.tw/eventsite/00984A/)：由安聯官網連出產品頁；產品行銷頁不是每日持股明細。|
|00985A|野村投信|只見部分持股|2026-09-30|[官方來源](https://www.nomurafunds.com.tw/ETFWEB/product-description?fundNo=00985A&tab=Shareholding)：索引可見10筆股票與查看更多；日期欄空白，資產／淨值對應9/30，仍須下載確認實際持股基準日。|
|00986A|台新投信|可見至少15筆；未封存驗證|2026-10-21|[官方來源](https://www.tsit.com.tw/ETF/Home/ETFSeriesDetail/00986A)：再次直接讀取可見36筆跨國股票及90.5636%合計；10/22預估單位與10/21申贖差額同頁，持股基準日未獨立明示，須核對10/22實際評價日。|
|00989A|摩根投信|官方入口，未驗證明細|未確認|[官方來源](https://am.jpmorgan.com/tw/zh/asset-management/twetf/funds/jpmorgan-us-tech-leaders-etf/)：已確認官方產品入口；本次未取得每日完整投資組合。月報前十大不可替代。|
|00988A|統一投信|官方入口，未驗證明細|未確認|[官方來源](https://www.ezmoney.com.tw/events/00988A/00988A-trading-guide.pdf)：官方申購指南可定位產品；尚未驗證每日持股來源。|
|00991A|復華投信|官方入口，未驗證明細|未確認|[官方來源](https://vpx.fhtrust.com.tw/ETF/etf_data_scale)：官方規模與費用總表包含代碼；持股入口尚未驗證。|
|00990A|元大投信|官方入口，未驗證明細|未確認|[官方來源](https://www.yuantaetfs.com/product/detail/00990A/Basic_information)：官方基本資料可見持股比重分頁；未實際展開取得明細。|
|00987A|台新投信|可見至少15筆；未封存驗證|2026-10-12|[官方來源](https://www.tsit.com.tw/ETF/Home/Pcf/00987A?DataDate=2026-10-13&FundType=ALL)：官方PCF可讀28筆及99.1448%合計；URL查詢日10/13而申贖價差標10/12，不能把URL當持股日，需核對10/22。|
|00992A|群益投信|只見部分持股|2026-10-22|[官方來源](https://www.capitalfund.com.tw/etf/product/detail/500/buyback)：官方頁僅展開10筆（含重複視覺表格），有展開全部按鈕；未驗證下載或其餘持股。|
|00994A|第一金投信|官方入口，未驗證明細|未確認|[官方來源](https://www.fsitc.com.tw/act/202512_994AETF/article-list.html)：官方產品頁已核對；月報前十大不是每日前15大，日持股入口未驗證。|
|00995A|中國信託投信|官方入口，未驗證明細|未確認|[官方來源](https://www.ctbcinvestments.com.tw/Product/List?Kind=1&ProductEtfNo=27)：官方總覽包含代碼；日持股明細尚未驗證。|
|00993A|安聯投信|官方入口，未驗證明細|未確認|[官方來源](https://etf.allianzgi.com.tw/eventsite/00993A/)：由安聯官網核對的產品入口；日持股明細未取得。|
|00996A|兆豐投信|可見至少15筆；未封存驗證|2026-09-11|[官方來源](https://www.megafunds.com.tw/MEGA/etf/etf_product.aspx?id=23)：官方搜尋索引可見至少16筆及9/11日期；直接重抓返回403，未繞過限制，需公開下載或授權替代來源。|
|00400A|國泰投信|官方入口，未驗證明細|2026-09-10|[官方來源](https://www.cathaysite.com.tw/ETF/purchase?code=EA&name=Cathay+Taiwan+High+Dividend+Momentum+Active+ETF)：官方PCF顯示淨值及查看基金持股權重，但本次文字頁未呈現持股列。|
|00401A|摩根投信|官方入口，未驗證明細|未確認|[官方來源](https://am.jpmorgan.com/tw/zh/asset-management/twetf/funds/jpmorgan-tw-equity-high-income-etf/)：已核對官方產品入口；每日持股及衍生品分流尚未驗證。|
|00997A|群益投信|官方入口，未驗證明細|未確認|[官方來源](https://www.capitalfund.com.tw/ETF_Area/Product_en)：官方英文ETF總覽含代碼與名稱；每日持股明細未取得，不推造產品內碼。|
|00999A|野村投信|官方入口，未驗證明細|未確認|[官方來源](https://www.nomurafunds.com.tw/ETFWEB/overview)：官方ETF總覽含代碼；未驗證其個別日持股分頁。|
|00403A|統一投信|官方入口，未驗證明細|未確認|[官方來源](https://www.ezmoney.com.tw/events/2026elite50/00403A-ezguide.pdf)：僅核對官方產品指南；每日持股入口未驗證。|
|00402A|安聯投信|官方入口，未驗證明細|未確認|[官方來源](https://etf.allianzgi.com.tw/eventsite/00402A/)：由安聯官網核對產品入口；每日持股明細未取得。|
|00404A|聯博投信|官方入口，未驗證明細|未確認|[官方來源](https://www.abfunds.com.tw/zh-tw/funds/etf/active/equities/abitl-taiwan-momentum-equity-premium-income-50-active-etf.-.TW00000404A5.html)：核對官方基本資料；日持股明細與掩護買權等工具分流尚未驗證。|
|00405A|富邦投信|官方入口，未驗證明細|未確認|[官方來源](https://www.fubon.com/asset-management/ph/glory/index.html)：核對官方產品專頁；日持股下載入口未驗證。|
|00406A|中國信託投信|官方入口，未驗證明細|未確認|[官方來源](https://www.ctbcinvestments.com.tw/Product/List?Kind=1&ProductEtfNo=27)：官方基金總覽含代碼；需以JavaScript或公開下載取得每日持股。|
|00407A|凱基投信|官方入口，未驗證明細|未確認|[官方來源](https://www.kgifund.com.tw/Fund/Detail?fundID=J024)：官方產品頁ISIN為TW00000407A8；本次未取得日持股。|
|00408A|第一金投信|官方入口，未驗證明細|未確認|[官方來源](https://www.fsitc.com.tw/act/202606_408AETF/article1.html)：核對官方產品資料；每日持股入口未驗證。|
|00410A|永豐投信|可見至少15筆；未封存驗證|2026-10-22|[官方來源](https://sitc.sinopac.com/SinopacEtfs/Etfs/SinglePcf/00410A)：官方PCF可讀28筆股票代號、股數與NAV權重；頁面上方10/27為PCF日期，實際持股資料日期明列10/22，不能混用。|
|00409A|復華投信|官方入口，未驗證明細|未確認|[官方來源](https://www.fhtrust.com.tw/ETF/etf_detail/ETF26)：核對官方產品入口；每日跨國持股尚未取得。|

## 進入計算前的必要證據

1. 對30檔取得對應交易日的實際持股原始檔並封存hash、first_seen、來源與基準日。抓取日／PCF適用日／持股評價日分欄；00410A頁面同時有10/27與10/22，就是具體反例。
2. 核對至少完整前15大股票及NAV權重。PCF若只是申贖籃子，不可自動視為完整實際持股；須核對頁面標示。只有前10大月報不足。
3. 海外證券需要市場／ISIN或等價識別；`2330 TT` 與美國ADR不能僅憑公司名稱合併。現金、期貨、選擇權與其他資產需獨立型別，不能混入股票前15大。
4. 依本地規則文件保留兩種暫行口徑：前15大保留原NAV權重、以及前15大各自正規化；兩者都是內部研究，主辦方仍須確認正規化、日期及海外比較細節。缺任一benchmark標未驗證，不得判為通過。[本地規則與官方辦法來源](../01-rules.md)。
5. 「連續兩交易日低於15%」要持久化每日結果與官方交易日，單日資料不能證明連續條件；內部20%緩衝也不能替代官方認證。

## 本次邊界與可交付結果

機器可讀盤點：[30檔來源JSON](etf-source-inventory.json)（本地來源：`planning/api-research/etf-source-inventory.json`）（30筆、狀態分類、投信、驗證過的官方URL、日期／權限缺口及來源URL）。此JSON沒有實際成分股或權重，**不能直接當Active Share benchmark輸入**。此份來源盤點本身不代表介接程式或持股驗收已完成。

建議優先接入永豐及台新可讀的公開PCF，建立日期與海外識別驗證範例，再處理群益展開全部及其他投信下載。全30檔達日期與完整性門檻前，候選保留外部驗收阻礙。
