# 指定30檔 ETF 持股實際取得與驗證（2026-10-26）

已實際下載並正規化 **21／30檔** 的10/22股票快照，合計1056筆股票紀錄；另8檔封存10/21日期，共374筆，其中台新00986A仍屬日期推導待核，程式明確禁止比較。其餘1檔尚未取得完整快照。日期推導個案保留標籤，**不能宣稱全30檔通過**。本次不用FinMind或付費API；只沿公開網頁正常匿名流程，不讀取私人登入憑證，不繞過403或CAPTCHA。

## 可接入的快照

|ETF|投信|股票數|NAV權重合計|評價日|PCF適用日|原始證據|
|---|---|---:|---:|---|---|---|
|00401A|摩根投信|56|0.920388|2026-10-22|2026-10-27|[官方來源](https://am.jpmorgan.com/FundsMarketingHandler/product-data?cusip=TW00000401A1&country=tw&role=twetf&language=zh&userLoggedIn=false&version=9.18_1791879504)|
|00403A|統一投信|50|0.8933|2026-10-22|不適用／未提供|[官方來源](https://www.ezmoney.com.tw/ETF/Fund/Info?fundCode=63YTW)|
|00404A|聯博投信|51|0.90373617|2026-10-22|2026-10-27|[官方來源](https://webapi.alliancebernstein.com/v2/funds/tw/zh-tw/investor/TW00000404A5/holdings)|
|00405A|富邦投信|47|0.952210|2026-10-22|不適用／未提供|[官方來源](https://websys.fsit.com.tw/FubonETF/Fund/Assets.aspx?stkId=00405A)|
|00406A|中國信託投信|62|0.8554|2026-10-22|2026-10-27|[官方來源](https://www.ctbcinvestments.com.tw/API/etf/Buyback)|
|00407A|凱基投信|50|0.9448|2026-10-22|不適用／未提供|[官方來源](https://www.kgifund.com.tw/Fund/Detail?fundID=J024)|
|00408A|第一金投信|52|0.9221|2026-10-22|2026-10-23|[官方來源](https://www.fsitc.com.tw/WebAPI.aspx/Get_hd)|
|00410A|永豐投信|28|0.8808|2026-10-22|2026-10-27|[官方來源](https://sitc.sinopac.com/SinopacEtfs/Etfs/SinglePcf/00410A)|
|00980A|野村投信|50|0.9501|2026-10-22|不適用／未提供|[官方來源](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)|
|00981A|統一投信|50|0.9581|2026-10-22|不適用／未提供|[官方來源](https://www.ezmoney.com.tw/ETF/Fund/Info?fundCode=49YTW)|
|00982A|群益投信|57|0.970203|2026-10-22|2026-10-27|[官方來源](https://www.capitalfund.com.tw/CFWeb/api/etf/buyback)|
|00984A|安聯投信|80|0.9845|2026-10-22|2026-10-27|[官方來源](https://etf.allianzgi.com.tw/webapi/api/Fund/GetFundAssets)|
|00985A|野村投信|50|0.9107|2026-10-22|不適用／未提供|[官方來源](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)|
|00987A|台新投信|28|0.964549|2026-10-22|2026-10-23|[官方來源](https://www.tsit.com.tw/ETF/Home/Pcf/00987A?DataDate=2026-10-27&FundType=ALL)|
|00991A|復華投信|50|0.98767|2026-10-22|不適用／未提供|[官方來源](https://www.fhtrust.com.tw/api/assetsExcel/ETF23/20261022)|
|00992A|群益投信|43|0.960759|2026-10-22|2026-10-27|[官方來源](https://www.capitalfund.com.tw/CFWeb/api/etf/buyback)|
|00993A|安聯投信|50|0.9679|2026-10-22|2026-10-27|[官方來源](https://etf.allianzgi.com.tw/webapi/api/Fund/GetFundAssets)|
|00994A|第一金投信|40|0.9616|2026-10-22|2026-10-23|[官方來源](https://www.fsitc.com.tw/WebAPI.aspx/Get_hd)|
|00995A|中國信託投信|55|0.9722|2026-10-22|2026-10-27|[官方來源](https://www.ctbcinvestments.com.tw/API/etf/Buyback)|
|00996A|兆豐投信|53|0.9665|2026-10-22|不適用／未提供|[官方來源](https://www.megafunds.com.tw/MEGA/etf/etf_product.aspx?id=23)|
|00999A|野村投信|54|0.9469|2026-10-22|不適用／未提供|[官方來源](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)|

正規化JSON位於 `artifacts/etf-acquisition-20261026/normalized/`，原回應及下載metadata在 `raw/`。逐檔hash、股票筆數及其餘各檔阻礙統一列於 `manifest.json`。台股使用 `TW:代碼`，不把海外ADR與原股合併；`weight_nav`是小數NAV權重字串，不重新正規化。每份保留valuation_date、pcf_applicable_date、實際fetched_at及raw_sha256。

## 解析與日期證據

### 永豐00410A

[官方PCF頁](https://sitc.sinopac.com/SinopacEtfs/Etfs/SinglePcf/00410A)明列資料日期10/22、股票表頭「佔基金淨資產之權重(%)」及28股票。HTML同時含桌機與手機重複列，只解析桌機股票表。頁首10/27為PCF適用日；基金股票股數是總持有數，沒有使用每基數申贖籃子。原始檔 `raw/00410A.html`；解析器 `normalize_sinopac.py`。

### 群益00982A、00992A

[00982A官方頁](https://www.capitalfund.com.tw/etf/product/detail/399/buyback)與[00992A官方頁](https://www.capitalfund.com.tw/etf/product/detail/500/buyback)預設僅顯示10筆；官方公開程式的展開全部／Excel下載都使用完整stocks陣列。依頁面實際載入的runtime、main與494明細元件核對：公開設定apiUrl為`https://www.capitalfund.com.tw/CFWeb`，唯讀POST `/api/etf/buyback`，參數`{fundId:"399"或"500",date:null}`。basic API對應確認399=00982A、500=00992A。這是持股查詢，沒有登入或發送委託。

回應`pcf.date1=10/27`與`stocks[].date1=10/27`是公告／PCF適用日，`pcf.date2=10/22`是淨值與實際申購價金基準。`inKind=N`為現金申贖，stocks.share為全基金持股；weight保留API四位百分點精度，不用顯示用weightRound。完整股票分別57、43筆。原始檔 `raw/capital399-holdings.json`、`raw/capital500-holdings.json`；解析器 `normalize_capital.py`。單純呼叫主站/api/路徑會回HTML（雖HTTP200），已排除該錯誤回應，不把200當資料成功。

### 凱基00407A、兆豐00996A

[凱基官方持股比重](https://www.kgifund.com.tw/Fund/Detail?fundID=J024)明列10/22、NAV及完整50股票；桌機與手機各一份同表，逐筆比對一致後去除重複。[兆豐官方持股比重](https://www.megafunds.com.tw/MEGA/etf/etf_product.aspx?id=23)本次直接HTTP200，明列「資料來源：兆豐投信，2026/10/22」、NAV及53股票；本次成功不是繞過前次403。兩者股數與NAV權重保留原值。原始檔 `raw/00407A.html`、`raw/00996A.html`；解析器 `normalize_mega_kgi.py`。

### 復華00991A

[官方基金頁](https://www.fhtrust.com.tw/ETF/etf_detail/ETF23)預設顯示前10筆，其「檔案下載」直接連至[完整資產Excel](https://www.fhtrust.com.tw/api/assetsExcel/ETF23/20261022)。Excel A3明列10/22、基金淨值資產68,178,935,634及50股票；每筆金額/NAV與公開權重在三位百分點四捨五入誤差內一致。少量股票顯示0.000%但股數大於0，保留零權重與正股數，不刪除此類股票或虛增權重精度。原始檔 `raw/fh-00991A-assets.xlsx`；解析器 `normalize_fh.py`。

## 下一批新增：富邦、野村、第一金與台新日期推導

[富邦官方資產頁](https://websys.fsit.com.tw/FubonETF/Fund/Assets.aspx?stkId=00405A)由官方行銷頁直接連出，明示10/22、NAV、47股票與金額，逐筆金額/NAV與權重符合披露精度。解析器normalize_fubon.py。

野村官方main.7ecbffde18d5367d.js明示[公開Fund/GetFundAssets查詢](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)，POST參數為FundID及SearchDate。FundID直接取已驗證官方fundNo，指定10/22後，00980A、00985A、00999A回應NavDate都明示10/22，股票表分別50、50、54股。沒有取用登入或Captcha流程。解析器normalize_nomura.py。

[第一金首頁](https://www.fsitc.com.tw/)明示00994A產品ID182、00408A產品ID183；其[基金頁](https://www.fsitc.com.tw/FundDetail.aspx?ID=182)公開Get_hd查詢（WebAPI.aspx/Get_hd）逐股sdate明示10/22，group=1為股票，分別40與52筆；NAV另綁Get_BuySellA原回應hash，摘要10/23是PCF適用日。解析器normalize_firstgold.py。

台新00987A依[官方公開說明書](https://www.tsit.com.tw/active/202512TSIT_00987A/pdf/TSIT_00987A_Prospectus.pdf)PDF第9頁／印刷第7頁，十四(二)1的公告時序：每營業日NAV結算後公告次營業日PCF。原HTML回PUB_DATE=10/23，價金欄10/22，因此內部將28股票推導為10/22；標valuation_date_basis=official_pcf_timing_inference，公開說明書原PDF及hash另綁。**不宣稱股票區獨立明示日期，也不是官方Active Share日期認證**。解析器normalize_taishin_inference.py。其餘快照的日期依各自來源明示欄位，逐檔標記於manifest。

## 其他真實日期的完整快照

normalized-other-dates/00997A.json為群益47股、00990A.json為元大42股、00409A.json為復華49股，皆保留來源明示10/21，沒有升格10/22。元大HTML前台僅5筆，但Nuxt的完整StockWeights含42筆；解析器僅拆解靜態字面值與參數，不執行遠端程式。復華Excel A3明示10/21；所有市場命名空間保留。解析器normalize_other_dates.py、normalize_fh_other.py。

## 其餘逐檔狀態

|ETF|投信|阻礙與觀察|
|---|---|---|
|00983A|中國信託投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|
|00986A|台新投信|已取得完整股票表，日期仍待獨立核實，禁止比較|
|00989A|摩根投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|
|00988A|統一投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|
|00990A|元大投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|
|00400A|國泰投信|官方PCF回HTTP403，停止該路徑，未繞過。|
|00997A|群益投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|
|00402A|安聯投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|
|00409A|復華投信|已取得完整股票表，來源評價日2026-10-21，未升格指定10/22|

## 中信與安聯公開查詢補充

[中信官方公開ETF頁](https://www.ctbcinvestments.com/ETF)的Buyback程式指向`.com.tw/API`；正常匿名home/AuthToken初始化後，ETFCNOList明確對應基金代碼與FID，再查etf/Buyback。匿名session僅在記憶體，不寫入原始檔、URL metadata或日誌。00995A為55股、00406A為62股，淨值日期10/22；00983A為43股，淨值日期10/21，未硬改日期。台股金額/NAV逐筆核對披露權重；海外資料保留原權重，不虛構匯率精度。

[安聯官方ETF頁](https://etf.allianzgi.com.tw/instant-estimated)主程式的正常初始化先呼叫AntiForgery/GetAntiForgeryToken，使用匿名cookie配對X-XSRF-TOKEN，並非登入。GetFundOverview提供基金代碼與CFundNo對照；GetFundAssets取得完整股票表。00984A為80股、00993A為50股，NavDate明示10/22；00402A為50股，NavDate明示10/21。PCFDate獨立為10/27。已封存匿名查詢的持股／識別回應，未保存cookie或防偽值。

## 每日更新實作

應用已加入collect-etfs與本機「資料與持股」更新功能，首批支援野村3、安聯3、中信3、群益2共11檔。來源失敗會覆蓋最新狀態為失敗，不能悄悄沿用舊快照；評價日不符會保留真實資料並標date_mismatch，候選比較仍阻擋。來源與對照原回應hash均綁定封存。其餘完整快照仍可由檔案匯入，不把已手工取得視為自動每日覆蓋。

## 不可忽略的限制

- 目前已取得的快照只證明這些股票表可取得，其中一份評價日依官方時序推導；並未驗證之後每日更新、服務可靠度或全部30檔同日完整性。
- 原始抓取與first_seen均為10/26，不能插入10/24截止的舊run、不能回填成10/22公開可得時間。
- 海外ETF常見10/21評價日、10/22上傳、10/27 PCF適用同時存在。這些欄位必須分開，未確認官方比較日期政策前不能硬改成10/22。
- Active Share正規化／前15大之外權重／海外比較方式仍依主辦方答覆；內部雙口徑及緩衝不等於官方認證。
- 輸出保留公開披露精度與可能的合計微差；不使用權重和為1假設來填補缺資料。
- 所有取得皆一手公開來源；沒有用搜尋摘要手抄權重作機器輸入、沒有以ETF基本名單代替持股。

## 下一步

將已取得快照的原始hash與正規化JSON接入benchmark contract，並保留台新推導日期標籤，缺任何ETF保持未驗證。其餘優先取得統一／中信／安聯日持股公開下載、補齊聯博及摩根介面，以及海外基金評價日政策；若有主辦方提供的官方ETF benchmark檔，應優先使用並另行驗證。

## 本批補完來源

統一3檔、摩根2檔、聯博1檔均取得完整持股；台新00986A日期仍待核實，已設valuation_date_usable=false並在比較器阻擋。完整來源、參數、幣別及日期證據見[剩餘來源研究](etf-remaining-sources-2026-10-26.md)。目前只剩國泰00400A沒有完整股票表；29份可取得持股不等於全30檔同日通過。
