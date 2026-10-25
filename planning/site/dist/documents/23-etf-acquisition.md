# 指定30檔 ETF 持股實際取得與驗證（2026-10-26）

已實際下載並正規化 **13／30檔** 的10/22股票快照，合計602筆股票紀錄（12檔由來源明示日期、台新00987A由官方PCF公告時序推導）；另3檔保留真實10/21日期，共138筆。其餘14檔尚有日期、動態介面、下載定位或連線缺口。此結果供已覆蓋資料的內部Active Share計算，**不能宣稱全30檔通過**。本次不使用FinMind Sponsor資料或任何付費API，不尋找token，不繞過403、CAPTCHA或其他限制。

## 可接入的快照

|ETF|投信|股票數|NAV權重合計|評價日|PCF適用日|原始證據|
|---|---|---:|---:|---|---|---|
|00405A|富邦投信|47|0.952210|2026-10-22|不適用／未提供|[官方來源](https://websys.fsit.com.tw/FubonETF/Fund/Assets.aspx?stkId=00405A)|
|00407A|凱基投信|50|0.9448|2026-10-22|不適用／未提供|[官方來源](https://www.kgifund.com.tw/Fund/Detail?fundID=J024)|
|00408A|第一金投信|52|0.9221|2026-10-22|2026-10-23|[官方來源](https://www.fsitc.com.tw/WebAPI.aspx/Get_hd)|
|00410A|永豐投信|28|0.8808|2026-10-22|2026-10-27|[官方來源](https://sitc.sinopac.com/SinopacEtfs/Etfs/SinglePcf/00410A)|
|00980A|野村投信|50|0.9501|2026-10-22|不適用／未提供|[官方來源](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)|
|00982A|群益投信|57|0.970203|2026-10-22|2026-10-27|[官方來源](https://www.capitalfund.com.tw/CFWeb/api/etf/buyback)|
|00985A|野村投信|50|0.9107|2026-10-22|不適用／未提供|[官方來源](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)|
|00987A|台新投信|28|0.964549|2026-10-22|2026-10-23|[官方來源](https://www.tsit.com.tw/ETF/Home/Pcf/00987A?DataDate=2026-10-27&FundType=ALL)|
|00991A|復華投信|50|0.98767|2026-10-22|不適用／未提供|[官方來源](https://www.fhtrust.com.tw/api/assetsExcel/ETF23/20261022)|
|00992A|群益投信|43|0.960759|2026-10-22|2026-10-27|[官方來源](https://www.capitalfund.com.tw/CFWeb/api/etf/buyback)|
|00994A|第一金投信|40|0.9616|2026-10-22|2026-10-23|[官方來源](https://www.fsitc.com.tw/WebAPI.aspx/Get_hd)|
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

台新00987A依[官方公開說明書](https://www.tsit.com.tw/active/202512TSIT_00987A/pdf/TSIT_00987A_Prospectus.pdf)PDF第9頁／印刷第7頁，十四(二)1的公告時序：每營業日NAV結算後公告次營業日PCF。原HTML回PUB_DATE=10/23，價金欄10/22，因此內部將28股票推導為10/22；標valuation_date_basis=official_pcf_timing_inference，公開說明書原PDF及hash另綁。**不宣稱股票區獨立明示日期，也不是官方Active Share日期認證**。解析器normalize_taishin_inference.py。其他12份標explicit_source_date。

## 其他真實日期的完整快照

normalized-other-dates/00997A.json為群益47股、00990A.json為元大42股、00409A.json為復華49股，皆保留來源明示10/21，沒有升格10/22。元大HTML前台僅5筆，但Nuxt的完整StockWeights含42筆；解析器僅拆解靜態字面值與參數，不執行遠端程式。復華Excel A3明示10/21；所有市場命名空間保留。解析器normalize_other_dates.py、normalize_fh_other.py。

## 其餘逐檔狀態

|ETF|投信|阻礙與觀察|
|---|---|---|
|00981A|統一投信|統一官網首頁回302且Location指回相同URL，無可讀主頁；既有產品指南PDF不能替代每日持股。|
|00983A|中國信託投信|官方.tw入口504；官方.com SPA可讀；其公開程式包含home/AuthToken初始化與API token參數，依不找token限制未呼叫認證流程；匿名資料權限尚未驗證，未取得直接持股下載。|
|00984A|安聯投信|產品頁連線逾時；另公開ETF主程式可讀，唯讀總覽API以官網參數查詢回400，未取得資產資料。|
|00986A|台新投信|完整36股已封存，但頁內申贖結算日為10/21，PUB_DATE=10/23；不能把夾限的PCF日期當股票10/22評價日。|
|00989A|摩根投信|官方產品與基金頁需動態投資組合介面；尚未取得10/22實際股票明細。|
|00988A|統一投信|既有入口為申購指南PDF，非持股資料；未驗證當期日持股。|
|00990A|元大投信|已下載官方ratio與PCF完整回應；股票區明示交易日10/21，雖頁面上傳10/22、公告10/23，也不能改標10/22。|
|00995A|中國信託投信|官方.tw入口504；官方.com SPA可讀；其公開程式包含home/AuthToken初始化與API token參數，依不找token限制未呼叫認證流程；匿名資料權限尚未驗證，未取得直接持股下載。|
|00993A|安聯投信|產品行銷頁可讀；公開主程式查明GetFundAssets，但總覽查詢回400，未猜測內部識別或繞過驗證。|
|00400A|國泰投信|官方PCF回HTTP403，停止該路徑，未繞過。|
|00401A|摩根投信|官方portfolio頁下載成功但主要為動態介面，尚未解析出完整當期股票及NAV權重。|
|00997A|群益投信|官方完整唯讀API取得47股票；PCF適用10/27但評價date2=10/21，未作10/22通過證據。|
|00403A|統一投信|既有入口為產品指南PDF，非持股資料；未驗證當期日持股。|
|00402A|安聯投信|產品行銷頁可讀；公開資產API尚未接通。|
|00404A|聯博投信|官方產品頁已下載；其中PCF超連結指向其他基金ISIN，不能據此混用為00404A持股，仍缺正確下載。|
|00406A|中國信託投信|官方.tw入口504；官方.com SPA可讀；其公開程式包含home/AuthToken初始化與API token參數，依不找token限制未呼叫認證流程；匿名資料權限尚未驗證，未取得直接持股下載。|
|00409A|復華投信|官方基金資產頁可讀且下載入口明列ETF26/20261021，基準日10/21；不是10/22證據。|

## 不可忽略的限制

- 目前13份只證明這些股票表可取得，其中一份評價日依官方時序推導；並未驗證之後每日更新、服務可靠度或全部30檔同日完整性。
- 原始抓取與first_seen均為10/26，不能插入10/24截止的舊run、不能回填成10/22公開可得時間。
- 海外ETF常見10/21評價日、10/22上傳、10/27 PCF適用同時存在。這些欄位必須分開，未確認官方比較日期政策前不能硬改成10/22。
- Active Share正規化／前15大之外權重／海外比較方式仍依主辦方答覆；內部雙口徑及緩衝不等於官方認證。
- 輸出保留公開披露精度與可能的合計微差；不使用權重和為1假設來填補缺資料。
- 所有取得皆一手公開來源；沒有用搜尋摘要手抄權重作機器輸入、沒有以ETF基本名單代替持股。

## 下一步

將13檔原始hash與正規化JSON接入benchmark contract，並保留台新推導日期標籤，缺任何ETF保持未驗證。其餘優先取得統一／中信／安聯日持股公開下載、補齊聯博及摩根介面，以及海外基金評價日政策；若有主辦方提供的官方ETF benchmark檔，應優先使用並另行驗證。
