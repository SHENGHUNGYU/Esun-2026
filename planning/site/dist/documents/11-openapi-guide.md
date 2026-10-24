# TWSE／TPEx OpenAPI：參賽端點選擇與接入指南

研究日期：2026-10-09。已讀取官方 Swagger 入口、入口引用的完整規格及相關官方資料集說明；本次保存 **TWSE 143＋TPEx 225＝368 個 GET operation**，沒有只挑常見端點。優先序與決策用途為本專案判斷，方法、路徑、官方名稱與欄位來自規格快照。只對 **9 個代表端點**作唯讀實測，完整端點索引不等於全部已接通驗收。

完整清單：[TWSE 143 個端點與欄位](12-twse-endpoints.md)、[TPEx 225 個端點與欄位](13-tpex-endpoints.md)。資料需求對照：[決策資料目錄](10-data-catalog.md)。網站提供同一份目錄的搜尋、優先序／交易所篩選及 JSON／Swagger 下載。

## 官方來源、方法與 Base URL

| 交易所 | 官方規格 | 格式／服務版號 | Base URL | 操作 |
|---|---|---|---|---|
| TWSE | [Swagger JSON](https://openapi.twse.com.tw/v1/swagger.json)；[UI](https://openapi.twse.com.tw/) | Swagger 2.0／info.version 1.0 | `https://openapi.twse.com.tw/v1` | 143 GET |
| TPEx | [Swagger JSON](https://www.tpex.org.tw/openapi/swagger.json)；[UI](https://www.tpex.org.tw/openapi/) | OpenAPI 3.0.0／info.version 1.0.0 | `https://www.tpex.org.tw/openapi/v1` | 225 GET |

兩份規格所有 operation 都未宣告查詢參數與安全設定，也未宣告分頁、限流、長歷史查詢與 SLA。**「未宣告」表示沒有文件化保證，不表示伺服器必然拒絕所有 query。** 不自行加上 `date`／`stockNo` 並假設生效，也不把「依日期查詢」「歷史」等表名當成參數契約。需指定歷史日期時，另核對官方歷史服務或 TEJ 權限。

兩份規格都宣告 JSON／CSV，200 schema 為 object；本次 9 個 JSON 實測均為 array of objects。TWSE 欄位均宣告 string；TPEx 3,254 個欄位中 3,250 string，四個標借欄位為 number。正式接入須做型態與缺值檢查，而不能把 Swagger 型別視為完全可靠。[TWSE 規格](https://openapi.twse.com.tw/v1/swagger.json)、[TPEx 規格](https://www.tpex.org.tw/openapi/swagger.json)

## 我會先使用的完整功能集合

下面列出功能主入口與必要的互補表；同一功能的表通常不能全部合併或視為可替換。財報的多個產業分表都保留在完整目錄，按固定 150 檔實際產業選用。

| 用途 | TWSE Path（接 Base URL） | TPEx Path（接 Base URL） | 實作判斷與限制 |
|---|---|---|---|
| 原始價量／官方日均價／技術與風險原料 | `/exchangeReport/STOCK_DAY_ALL` | `/tpex_mainboard_quotes`、`/tpex_mainboard_daily_close_quotes` | 核對金額／股數單位、日資料完成時間與150檔覆蓋；TPEx後者另有Average／NextReferencePrice，均價仍須交叉核對。 |
| 證券主檔／產業／股數 | `/opendata/t187ap03_L` | `/mopsfin_t187ap03_O` | 主檔全市場需過濾競賽名單；股本、發行股數與自由流通不同。 |
| 開休市 | `/holidaySchedule/holidaySchedule` | 本規格未找到相對應日曆端點 | 上櫃與臨時停市仍需官方日曆／公告核對。 |
| 停復牌／變更交易 | `/exchangeReport/TWTAWU`、`/exchangeReport/TWT85U` | `/tpex_spendi_today`、`/tpex_spendi_history`、`/tpex_cmode` | 無法估值／成交時按競賽例外處理；「history」未宣告指定日期參數。 |
| 處置／注意／首五日制度 | `/announcement/punish`、`/announcement/notice`、`/announcement/notetrans`、`/exchangeReport/TWT88U` | `/tpex_disposal_information`、`/tpex_trading_warning_information`、`/tpex_trading_warning_note`、`/tpex_ipo_no_limit` | 注意／處置與停牌含義不同；不可一律當成禁買。 |
| 除權息／股利 | `/exchangeReport/TWT48U_ALL`、`/opendata/t187ap45_L` | `/tpex_exright_prepost`、`/tpex_exright_daily`、`/mopsfin_t187ap39_O` | 預告、計算結果、決議三種時點分開；仍不完整覆蓋分割、減資與權益支付。 |
| 月營收與成長 | `/opendata/t187ap05_L` | `/mopsfin_t187ap05_O`；補充`/mopsfin_t187ap05_OA`、`/mopsfin_t187ap05_OB` | 當次兩市場都只取得11508快照；不是到查詢日全部公司都已更新。 |
| 損益／EPS／品質原料 | `/opendata/t187ap06_L_ci`及同族`basi/bd/fh/ins/mim` | `/mopsfin_t187ap06_O_ci`及同族`basi/bd/fh/ins/mim`；財報摘要`..._ciA`等 | 須核對單季／累計與產業科目；沒有 CFO／FCF 全表，也沒有首發／重編歷史保證。 |
| 資產負債 | `/opendata/t187ap07_L_ci`及同族產業表 | `/mopsfin_t187ap07_O_ci`及同族產業表 | 可支援負債與資本分析的一部分；現金餘額不是營業現金流。 |
| 盈餘／營益摘要 | `/opendata/t187ap14_L`、`/opendata/t187ap17_L` | `/mopsfin_t187ap14_O`、`/mopsfin_187ap17_O` | 後者Path真的沒有`t`，不得按命名習慣修正；以實際科目與單位對齊。 |
| 估值 | `/exchangeReport/BWIBBU_ALL`、`/exchangeReport/BWIBBU_d` | `/tpex_mainboard_peratio_analysis` | PE／PB／殖利率；不等於預估PE、完整EV倍數或可用股利現金。 |
| 市場／報酬基準、Beta | `/indicesReport/MI_5MINS_HIST`、`/indicesReport/MFI94U`；對照`TAI50I/FRMSA` | `/tpex_index`、`/tpex_reward_index`；成分`/tpex_index_consti` | 市場價格指數與總報酬分清；Beta需足夠個股／基準歷史自行計算。 |
| 廣度／市場狀態 | `/exchangeReport/MI_INDEX`、`/exchangeReport/FMTQIK`、`/exchangeReport/MI_INDEX4`、`/opendata/twtazu_od` | `/tpex_mainborad_highlight`、`/tpex_daily_trading_index` | TPEx Path 為`mainborad`；全市場統計不等於150檔廣度。 |
| 三大法人 | 此Swagger沒有T86逐股買賣超端點 | `/tpex_3insti_daily_trading`；補充`/tpex_3insti_summary`、`/tpex_3insti_trading`、`/tpex_3insti_qfii_trading`、`/tpex_3insti_dealer_trading` | 上市法人需官方另服務／TEJ；上櫃各表互補，避免重複總額與分項。 |
| 外資持股結構 | `/fund/MI_QFIIS_cat`、`/fund/MI_QFIIS_sort_20` | `/tpex_3insti_qfii`、`/tpex_3insti_qfii_industry` | TWSE是產業與前20，不是全體逐股持股；TPEx排名表覆蓋仍需驗證。 |
| 融資融券 | `/exchangeReport/MI_MARGN`、`/exchangeReport/BFI84U` | `/tpex_mainboard_margin_balance`及`/tpex_margin_trading_*`相關表 | TWSE MI_MARGN schema含逐股資料；兩市場都需單位與日期驗收。 |
| 借券／融券賣出 | `/SBL/TWT96U` | `/tpex_margin_sbl`、`/tpex_short_sell` | TWSE是可借券賣出股數；不是實際借券餘額／成交。 |
| 大股東／內部人／質押 | `/opendata/t187ap02_L`、`09_L/11_L/12_L/13_L`等同族表 | `/mopsfin_t187ap02_O`、`09_O/11_O/12_O/13_O`等同族表 | 申報與實際轉讓分開；多表均已列入完整目錄。 |
| 重大訊息／事件 | `/opendata/t187ap04_L`；`/news/newsList` | `/mopsfin_t187ap04_O` | 原始公告可供LLM抽取；交易所新聞不是全市場媒體新聞。 |
| 股東會／財測／裁罰／經營權 | `t187ap38_L/41_L/15_L/16_L/22_L/23_L/24_L/25_L/26_L/27_L`等 | `t187ap41_O/15_O/16_O/22_O/23_O/24_O/25_O/26_O/27_O`等 | 這列為端點族識別，完整可執行URL以全目錄為準；財測差異不是分析師共識。 |
| ETF身分／風格指數 | `/opendata/t187ap47_L`；`/ETFReport/ETFRank` | 風格指數與`*_constituents`各表 | 基金身分、定期定額戶數、指數成分都不能代替ETF每日實際持股。 |
| ESG／供應鏈與治理背景 | `/opendata/t187ap46_L_*`、治理各表 | `/t187ap46_O_*`、治理各表 | 慢頻補充，保留公開日期，不先假定有短期績效增量。 |

上表的省略寫法只是便於討論；只有完整目錄中的原始 Path 才用於實作，不組合猜測 URL。優先採 P0／P1，P2須測增量；P3及參考仍完整列出，供核對「是否漏了資料能力」。

## 9 個代表實測與時間差異

2026-10-09 約14:26–14:31台北時間，各完整 URL 呼叫一次，未提供 key。這些是觀測快照，不是每日排程或長期穩定性的保證。原始結果與 SHA-256 封存在專案 `planning/api-research/`，端點目錄提供 HTTP、列數、日期與型態證據。

| 交易所／端點 | HTTP／列數 | 實際時間範圍或現象 | 影響 |
|---|---|---|---|
| TWSE STOCK_DAY_ALL | 200／1380 | Date1151008 | 當次只有前一交易日，不能直接取得3–5年。 |
| TWSE t187ap05_L | 200／1086 | 出表1150917、資料年月11508 | 營收月份與可用時間不同；九月資料還需另驗。 |
| TWSE MFI94U | 200／6 | 1151001–1151008 | 當次有限歷史集合；不證明可指定年月。 |
| TWSE t187ap06_L_ci | 200／1049 | 出表1151009、年度115、季別2 | 新出表不等於新發布財報，也不等於當日已公布Q3。 |
| TPEx mainboard_quotes | 200／1011 | Date1151008 | 標的包含非白名單證券，需過濾。 |
| TPEx index | 200／6 | 20261001–20261008 | 此表為西元日期，與行情民國格式不同。 |
| TPEx t187ap05_O | 200／892 | 出表1150917、資料年月11508 | 與TWSE同樣需檢查時效。 |
| TPEx t187ap04_O | 200／63 | 出表1151009、發言日期1151008 | 出表、發言、事實發生、抓取四種時點不能混用。 |
| TPEx 3insti_daily_trading | 200／892 | 20個欄位與schema一致，含前導空白鍵 | 避險買進等完整拆分不足；不補造缺欄。 |

上述行情資料的政府資料集標示每日收盤後、每1日更新及免費，但市場現況資料集標示不定期更新。每張表逐表驗收，不能把某張行情表的排程套到全部368端點。[收盤行情](https://data.gov.tw/dataset/11371)、[含均價的股票行情](https://data.gov.tw/dataset/11370)、[市場現況](https://data.gov.tw/dataset/11369)

## 這兩份規格仍無法完整滿足的需求

| 缺口 | 現有端點為何不足 | 應補方向 |
|---|---|---|
| 指定30 ETF前15大每日實際持股 | 基金主檔與指數成分不是基金真實持倉；沒有每檔完整日持股權重表 | 基金公司／官方比較資料／TEJ；同時確認Active Share算法 |
| 多年日行情及PIT公告／財報修訂 | 未文件化指定日期參數；本次多為最新或當月 | TEJ既有權限、官方歷史服務、每日快照；保留版本 |
| 完整CFO／FCF與ROIC原料 | 損益／資產負債／摘要不足以替代完整現金流量表及科目明細 | MOPS正式財報、TEJ財務表 |
| 上市逐股三大法人完整交易 | TWSE此Swagger未列T86，外資持股表也不能代替交易流 | [TWSE官方T86頁](https://wwwc.twse.com.tw/zh/trading/foreign/t86.html)、核實其另服務或TEJ |
| 集保股權級距 | 兩交易所無TDCC級距資料 | [TDCC](https://original-www.tdcc.com.tw/portal/zh/smWeb/qryStock)、TEJ授權 |
| 完整分點、自由流通股／因子調整 | TPEx熱門排行與券商營業金額僅部分代理；主檔／除權息仍不完整 | TEJ表、公司行動與相關供應商；欄位逐項確認 |
| 媒體新聞全文／歷史共識預估 | 重大訊息有價值，但不是全部媒體及分析師PIT共識 | 新聞API、公司IR、TEJ或授權共識來源 |
| 海外市場、匯率、美債利率、總體vintage | 台灣債券／黃金表不等於完整海外與總體序列 | 台美股MCP底層來源、央行／ALFRED等 |
| Beta、RSI、MACD、協方差／ML標籤 | 兩份規格無本計畫整套衍生特徵服務 | 由足夠歷史原料、明確公式與成本帳本自行算 |
| 競賽庫存、NAV、提交及回執 | 市場公開資料不是個人競賽帳戶接口 | 主辦方接口與例外公式確認 |

## 接入契約與建議排程

先收集**整張表快照**，再按官方固定150檔過濾；不為每檔股票猜一個未宣告參數。保留原始 JSON、HTTP取得時間、來源、雜湊、解析版本、資料日期與公布時間。名稱有 typo 或空白也保留原始鍵，另建立明確對應；禁止靜默改鍵造成碰撞。

- 價量、交易狀態、公司行動、法人：盤後取得並隔晨驗證資料日期與覆蓋；具體更新時刻先觀測，不預設交易所固定幾點完成。
- 重大訊息：決策截止前增量取得、去重與版本化；每日表可能有限保留，歷史需另源，不為了即時性無限輪詢。
- 月營收／財報：定期檢查版本；出表日與年季保留，若沒有可靠公司首發時間，就不能當高精度事件訊號。
- 治理／ESG／主檔／日曆：按變更與低頻核對，避免不必要重抓。
- 建議本地每日快照＋適量重試／退避＋TEJ或其他已驗證備援；這是我們的工程方案，並非官方公布的配額或SLA。

數值解析使用Decimal／明確比例定義，處理逗號、負號、空白、`--`與不適用；日期各表按民國／西元／季別解析。金額與股數單位需資料集說明或可驗證案例，不能只憑欄位名字猜。原始價留給競賽帳本，調整價與總報酬用於研究；晨間只能讀截止前已完成且可得的版本。

## 官方文件、授權與歷史服務的邊界

TWSE Swagger 本身歡迎介接且連結[使用條款](https://www.twse.com.tw/zh/terms/use.html)及[政府資料開放授權](https://data.gov.tw/license)；公開API與任意抓取其他網頁是不同範圍。TPEx上述官方資料集明列開放授權，但不能據此推定所有其他資料商品或多年歷史免費。

TWSE另有[盤後／歷史資訊商店](https://eshop.twse.com.tw/zh/)，TPEx另有[盤後API使用說明](https://eshop.tpex.org.tw/zh/product/list/29)。它們是另服務，不能套用本次OpenAPI的URL、免key現象或欄位契約。本次未訂閱、付費或取得受限資料。

原始規格依官方快照完整封存；metadata的SHA-256用於偵測變更，不是資料值正確性的證明。更新規格後應做端點／欄位diff，核對新增、刪除、改名及型別，重新驗收受影響adapter。
