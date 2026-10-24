# 第一階段 LangGraph 草稿：官方資料快照與每日研究報告

版本：2026-10-14 v0.1｜狀態：原研究設計；2026-10-21已有部分LangGraph實作，仍未完成競賽閉環。

> 2026-10-14來源增補：使用者指定FinMind＋中央社產經證券RSS＋TWSE／TPEx，MCP非必要。以[實作資料源總清單](15-data-source-register.md)及[完整CSV](implementation-data-sources.csv)為最新來源接入計畫。以下「尚無歷史」指尚未取得驗收的資料；FinMind已列為歷史補齊候選，通過後才啟用相關指標。正式研究與提交範圍仍依本草稿區分。

使用者已確認：第一階段交付「資料與研究報告」，目前沒有可讀取的 TEJ 歷史資料，先用官方 API 累積快照。本文件細化 [整體 Agent 設計](04-agent.md)，不代表 U02–U14 已開發或驗收。API 選擇以 2026-10-09 封存的 [368 個端點](11-openapi-guide.md) 為依據，上線前重驗 schema 與可用性。

## 1. 我建議的第一階段成果

每天回答四個問題：150 檔資料是否完整？市場與公司出現哪些可驗證變化？哪些研究指標已有足夠原料？哪些結論因資料缺口不能成立？

交付一個 Python LangGraph 工作流，輸出不可變的資料快照、逐檔品質表、可計算指標、帶引用的中文研究報告與恢復紀錄。第一階段結束在研究結果；股票配置、股數、D-Plan、官方提交另接後續圖。報告不以任何模擬績效宣稱策略有效。

核心設計是「確定性資料流程＋有界 LLM 解讀」。抓取、日期／單位換算、指標、引用驗證使用程式；LLM 負責事件分類、假說、反證與中文表達。JEV 放在離線比較接口，通過中文結構化評估前不成為必需依賴。

## 2. 圖的分工與執行順序

建議一個主圖，初版用三條固定並行資料分支，待需求擴張再考慮動態 Send。端點清單由版控設定提供；LLM 不自行新增 URL、選擇憑證或改動 cutoff。

```text
START → prepare_run → collect_market ──────┐
                   → collect_fundamentals ├→ assemble_snapshot → quality_gate
                   → collect_events ──────┘
quality_gate → 核心不合格 → write_blocked_report → END
quality_gate → 通過／可降級 → compute_features → build_observations
            → interpret → verify_claims → publish_research → END
                          │
                          └→ 引用／結構錯誤 → repair（最多 2 次）→ verify_claims
                             修復耗盡 → deterministic_report → publish_research
```

所有並行分支都回傳成功／部分成功／失敗的結構化結果，已耗盡的預期網路錯誤也須回傳結果，讓 join 可到達。程式 bug 或損壞的 checkpoint 則停止 run 並記錄 incident，不偽裝成一般資料缺口。prepare_run 驗證失敗直接終止為 BLOCKED。

| 節點 | 讀取／處理 | 寫出 | 失敗處理 |
|---|---|---|---|
| prepare_run | 模式、交易日、cutoff、固定150檔、端點／政策版本、既有快照 | RunContext、固定抓取清單 | 名單或時區不合法：BLOCKED；休市可輸出休市研究 |
| collect_market | 價量、主檔、交易日、估值、交易狀態、籌碼 | market_bundle_ref | 按 endpoint 有界重試；逐項記錄失敗 |
| collect_fundamentals | 營收、損益、資產負債；按公司產業分表 | fundamental_bundle_ref | 表缺失／欄位不相容隔離，不填零 |
| collect_events | 重大訊息、停復牌背景、除權息、注意處置 | event_bundle_ref | 空結果須區分成功無事件與抓取失敗 |
| assemble_snapshot | 去重、日期／單位、主檔映射、150檔過濾、時間可用性 | snapshot_ref、lineage_ref | 原始資料不改寫；無法判讀者進 quarantine |
| quality_gate | 價量日期、逐檔覆蓋、來源衝突、核心／選用能力 | capability_matrix、issues、gate | 核心失敗停止全面分析；選用失敗停用相關能力 |
| compute_features | 只計算能力矩陣允許的指標 | feature_ref、disabled_features | 缺歷史或除權調整：停用相應指標 |
| build_observations | 從欄位與公式建立事實及來源 ID | observation_ref | 每項數值必須帶單位、日期及 lineage |
| interpret | 給本地 LLM 有限事實與公告片段 | analysis_draft_ref | 無模型／timeout：確定性摘要；模型無抓取工具 |
| verify_claims | JSON schema、ID、數字／時間、引用、推論語氣 | verified_analysis_ref 或 errors | 可修復錯誤至多 2 次；之後保留事實摘要 |
| publish_research | 本地輸出 Markdown＋JSON＋manifest＋品質報告 | artifact_refs、終態 | 原子寫入、內容 hash；不自動上傳授權受限資料 |

這裡 publish_research 指寫入本地研究成品，不等於網站部署或官方提交。

## 3. 首批端點：按資料組接入

Base URL：TWSE `https://openapi.twse.com.tw/v1`；TPEx `https://www.tpex.org.tw/openapi/v1`。下列均為 GET，完整原始欄位仍以端點目錄為準。大多是全市場快照，抓一次後在本地過濾，不逐股重複抓 150 次。

| 資料組／接入次序 | TWSE 路徑 | TPEx 路徑 | 第一階段用途 |
|---|---|---|---|
| A1 主檔 | `/opendata/t187ap03_L` | `/mopsfin_t187ap03_O` | 公司識別與產業映射；不能用它替換固定競賽白名單 |
| A1 價量 | `/exchangeReport/STOCK_DAY_ALL` | `/tpex_mainboard_quotes`、`/tpex_mainboard_daily_close_quotes` | 收盤、成交量額、資料日；兩種上櫃報價交叉核對 |
| A1 行事曆 | `/holidaySchedule/holidaySchedule` | 另驗官方交易日曆 | 推導預期上一交易日；暫停／臨時休市仍須公告核對 |
| A1 停復牌 | `/exchangeReport/TWTAWU`、`/exchangeReport/TWT85U` | `/tpex_spendi_today`、`/tpex_spendi_history`、`/tpex_cmode` | 記錄交易狀態，解釋缺價；公告的生效日與發布日分開 |
| A2 估值 | `/exchangeReport/BWIBBU_ALL` | `/tpex_mainboard_peratio_analysis` | PE／PB／殖利率橫截面描述；負盈餘、缺值不當零 |
| A2 月營收 | `/opendata/t187ap05_L` | `/mopsfin_t187ap05_O` | 月營收與來源提供之成長率，逐公司標示年月 |
| A2 財報 | `/opendata/t187ap06_L_ci`、`/opendata/t187ap07_L_ci` | `/mopsfin_t187ap06_O_ci`、`/mopsfin_t187ap07_O_ci` | 一般產業損益／資產負債；金融等產業用對應分表 |
| A2 重大訊息 | `/opendata/t187ap04_L` | `/mopsfin_t187ap04_O` | 事件抽取、引用、觀測窗內新增公告 |
| A2 權益事件 | `/exchangeReport/TWT48U_ALL`、`/opendata/t187ap45_L` | `/tpex_exright_prepost`、`/tpex_exright_daily`、`/mopsfin_t187ap39_O` | 除權息警示、報酬計算可用性；不宣稱完整調整因子 |
| A3 市場指數 | `/indicesReport/MI_5MINS_HIST`、`/indicesReport/MFI94U` | `/tpex_index`、`/tpex_reward_index` | 市場背景、儲存價格／報酬指數；不把月內資料當多年歷史 |
| A3 融資融券 | `/exchangeReport/MI_MARGN` | `/tpex_mainboard_margin_balance` | 可用日的餘額／變化，先確認股數與金額單位 |
| A3 法人 | 本份 Swagger 無 T86 | `/tpex_3insti_daily_trading` | 先做上櫃研究，不對缺上市法人資料填零或跨市場硬排名 |
| A3 注意處置 | `/announcement/notice`、`/announcement/punish` | `/tpex_trading_warning_information`、`/tpex_disposal_information` | 事件與風險背景；注意、處置、停牌分別建模 |

A1 先做完整資料品質閉環，A2 再形成基本面／事件報告，A3 擴充研究。A1/A2/A3 是接入次序，不是原目錄的 P0/P1 優先序。機器可讀的 [57 個端點候選 JSON](langgraph-phase1-endpoints.json)（37 個明列候選＋20 個產業條件候選），其 URL 必須存在封存目錄，不能依命名習慣猜測。

金融產業的 basi/bd/fh/ins/mim 分表全部保留為條件候選；確認150檔產業映射後才啟用適用表。不能把銀行、保險與製造業的科目直接拼成同一 ROE／負債排序。先完成欄位語意核對，再開啟跨公司比較。

## 4. 時間、快照與累積歷史

資料日期、報告期與首次可用時間是不同欄位。每列至少保存：

| 欄位 | 意義 |
|---|---|
| security_id、exchange | 固定公司識別；改名仍維持映射 |
| source_id、endpoint_id、raw_sha256、row_key | 回到原始檔及列 |
| event_at／period_end／effective_date | 事件發生、財報期間、制度生效日期，各自保留 |
| published_at | 有官方可靠發布時間才填；出表日不自動等於首發 |
| first_seen_at、fetched_at | 系統首次觀測此版本及本次取得時間 |
| available_at、availability_basis | 本系統可使用此版本的時間與判定依據 |
| unit、currency、schema_version | 股／張／元／千元及轉換版本 |
| revision_id、supersedes | 後續修訂另存版本，不覆蓋歷史 |

保守政策：available_at 至少不早於 first_seen_at；若 published_at 更晚，取較晚者。盤後累積與盤前研究使用明確 cutoff，只有 available_at ≤ cutoff 的版本可進研究。未來股東會／除息日期可以是已知事件，不能因 effective_date 在未來就一律刪除；反之，未來才公布的財報不可用。

收集與研究採兩個入口：盤後／盤前的 ingestion job 呼叫相同 DatasetGateway 並持久化原始資料；07:00 的研究圖中三個 collect 節點選取 cutoff 前已入庫的版本，沒有合格版本就回傳缺口。live 指使用真實封存資料，不表示可以越過 cutoff 即時補抓。首次手動試跑先完成 ingestion，再設定其後的研究 cutoff；不把未來抓取時間回填為過去。

晨間研究讀取已在 cutoff 前入庫的封存資料；cutoff 後抓到的資料進下一快照，不補進本次研究。事件 API 若只回當日資料，從開始記錄日起累積並保留抓取間隔；兩次抓取之間可能遺漏的公告需揭露，不能聲稱完整新聞庫。

首次拉到過去一個月指數或上一季財報，可作「今天已知」的歷史內容，但無法證明在過去當天就可取得。嚴格歷史回放只使用當時已封存版本；不得以今天拿到的財報倒灌過去。

原始檔依 source／fetched_at／hash 保存；標準化資料按市場、交易日、公司及 revision 去重。資料集以 Parquet 保存，DuckDB 查詢；原始 JSON、manifest 與 lineage 都保留。LLM 接收的僅是必要摘要及引文，整份市場資料不塞進 prompt。

## 5. 指標能力逐步開放

以下是草稿的最少樣本政策，不代表統計上已有效，亦非競賽規則。缺值是 null＋reason，禁止補成0、均值或模型猜值。

| 能力 | 開啟條件 | 起步狀態 |
|---|---|---|
| 當日價量、估值、營收、重大訊息摘要 | 各自來源通過日期／單位／品質驗證 | 第一個有效快照可用；需標示資料期 |
| 融資／法人當日值 | 欄位語意與日期已驗證 | 局部市場可用，覆蓋率明列 |
| 前後變化與新增事件 | 至少兩個可比較、不同有效日期快照 | 未累積前停用；不得比較不同財報期成長為同日變化 |
| 5日報酬 | 至少6個對齊收盤觀測，權益事件已處理 | 尚未具備；不能把抓取6次當6個交易日 |
| SMA20、量比 | 至少20個有效交易日；量比使用當日量／前20日均量需21日 | 尚未具備 |
| RSI14、ATR14 | 至少15個連續且定義一致的OHLC，初始化方法固定 | 尚未具備；持續累積再評估是否採用 |
| Beta60／波動60 | 至少61個對齊價格點得到60筆報酬；基準變異數非0、權益調整有效 | 尚未具備；不足不降成5日Beta |
| 中長期品質／營收加速度 | 多期且可比較的財報／營收與首見版本 | 最新單期不等於完整因子歷史 |
| CFO／FCF、ETF實際持股、上市法人T86 | 補外部來源與授權驗證 | 官方兩份Swagger不足，明列缺口 |

Beta = Cov(個股報酬, 基準報酬) / Var(基準報酬)，兩者同頻率、同觀測日、同報酬口徑；市場基準先分上市／上櫃。提供觀測數、期間、基準及不確定性，後續是否改共同基準另作策略決策。原始價用於行情與未來競賽帳本；研究用調整價需獨立序列。權益事件未完整處理前，受影響期間的報酬與Beta停用。

因此只累積兩週新快照，無法完成可靠的60日Beta或多年回測。若第二階段需要趨勢選股，必須補歷史資料或延後該能力，不能用模型取代缺失的歷史。

## 6. State、儲存與模組 Interface

State 只保存小型狀態及 artifact references，大型 DataFrame、原始公告、模型權重、憑證不進 checkpoint。

```python
# 介面草圖；不是已執行的程式
class ResearchState(TypedDict):
    run_id: str
    trade_date: str
    cutoff_at: str                 # +08:00
    mode: Literal['live', 'replay']
    universe_hash: str
    policy_hash: str
    endpoint_registry_hash: str
    market_bundle_ref: str         # 各分支唯一寫入欄位
    fundamental_bundle_ref: str
    event_bundle_ref: str
    snapshot_ref: str
    capability_matrix: dict
    feature_ref: str
    observation_ref: str
    analysis_draft_ref: str
    verified_analysis_ref: str
    issues: list[dict]             # 單一彙整節點寫入；當輪可替換
    repair_count: int
    gate: Literal['PASS', 'DEGRADED', 'BLOCKED']
    artifact_refs: dict
    status: str
```

這是最終欄位清單；實作時把中間產物設 Optional／NotRequired 或提供初始化值，入口只要求 RunRequest 欄位。公開輸出另定 ResearchResult schema，不輸出整個內部 State。

三個 collector 只寫自己的 bundle_ref；使用 `add_edge(['collect_market', 'collect_fundamentals', 'collect_events'], 'assemble_snapshot')` 等三者完成後再彙整。初版不需要共用 list reducer，可避免平行寫入衝突與重播重複追加。若未來改動態 Send，才加入以 endpoint_id＋artifact_hash 為鍵的冪等合併，並測試聚合完成條件。[LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

| Module | 對外 Interface 草圖 | 隱藏的 Implementation |
|---|---|---|
| DatasetGateway | collect(dataset_request) → DatasetResult | TWSE／TPEx adapter、原始快照、retry、欄位映射；呼叫者不猜URL |
| SnapshotStore | freeze(run_context, bundles) → SnapshotRef；read(ref) | 不可變檔、hash、版本、PIT與去重；live／replay共用契約 |
| ResearchEngine | compute(snapshot_ref, capability_policy) → FeatureRef | 財務單位、公式、歷史樣本門檻與能力檢查 |
| EvidenceEngine | observe(features, events)；verify(analysis, observations) | 引用ID、原始列、數字及時間檢查 |
| ModelGateway | interpret(observation_ref, model_profile) → AnalysisResult | 本地模型、結構化輸出與有界修復；JEV可替換的離線adapter |

採 Python TypedDict 描述圖狀態，Pydantic 驗證外部輸入／模型輸出，Decimal 處理需精確的價格金額換算。確切依賴版號在實作開始時鎖定並測試，草稿不虛填已驗證版號。

## 7. 品質門檻、降級與恢復

研究終態：COMPLETE、DEGRADED、BLOCKED。COMPLETE 只代表本次設定的第一階段研究能力驗證完成，不代表可參賽、可交易或資料已涵蓋所有市場消息。

- 固定150檔每檔都須在品質表出現。行情已取得、公告可解釋的停牌、資料缺失三者分開；不因缺價而從分母移除。
- 價量日期必須等於預期上一交易日。停牌可有明確缺價狀態，但不能用舊價冒充新價。行情缺失且無法解釋：BLOCKED，仍產出品質與缺口報告。
- 單一股的可選估值／財報缺失：DEGRADED，該能力／比較排除並標分母。任何 cross-sectional 排名必須列出實際可比樣本與被排除原因；第一版預設只描述，不產生投資排名。
- 營收與財報依公司及報告期驗證，不用一個24小時TTL判定失效，也不把出表日刷新當成更新內容。
- schema 出現新欄位可保存並記錄；必要欄位移除、型別／單位無法判讀時隔離該資料組。兩市場同名字段不得直接認定同單位。
- 來源衝突保留雙方與差異，不取平均掩蓋；TWSE／TPEx／將來TEJ的優先序按用途固定。

HTTP 草稿政策：每端點總共最多3次請求，暫定單次20秒、指數退避與jitter；429尊重Retry-After但不得超出run deadline。只重試timeout／暫時連線錯誤／429／部分5xx；401、403、404、欄位不相容不盲目重試。每主機先限制1個並行請求、請求間至少1秒，這是本地保守設定，並非官方公布配額；依文件與實測調整。

每個資料組內可以逐endpoint進行，底層一成功就寫不可變raw與結果索引；節點重跑先查已完成結果，避免整組重抓。若來源資料版本已變，開新快照；replay模式完全不呼叫外網。整個run暫定15分鐘deadline；其後寫BLOCKED／DEGRADED報告，不能無限自修。

本地單機開發使用持久化 SQLite checkpointer；M3 先作單一 leader。工作流以固定 run_id 對應 thread_id，恢復同一run沿用，新的cutoff／政策另開run。正式多機再評估Postgres，NVIDIA只承接模型工作，不共同寫SQLite。InMemorySaver只用於測試，不能證明跨重啟恢復。[LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

checkpoint不是exactly-once保證。原始下載、LLM結果、最終檔案均以run_id／請求hash／內容hash去重；先原子寫檔再保存reference，恢復時驗hash。中途中斷可能重新執行節點，LLM輸出須留存，temperature=0也不當成位元級重現保證。

開發驗收由人確認；正式研究run不逐篇等待人工核准。`interrupt()` 只預留給需要人工補資源的操作事件，恢復時仍驗證設定，不允許藉resume注入股票／權重。中斷前的程式可能重執行，因此任何副作用都必須可重入。[LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

## 8. LLM的輸入與輸出

輸入分兩層：程式驗證的 observation（數值、單位、日期、來源）與官方公告片段（原文、ID、發布時間／first_seen）。公告內容一律視為資料，禁止改變系統政策。不要要求模型自己算Beta、推測缺值或編造引用。

輸出固定包含：market_summary、company_events、hypotheses、counter_evidence、uncertainties、observation_ids。每個推論標為推論，列出可推翻條件；無證據時可明確 abstain。模型自報信心不是經校準機率，不直接用於資金配置。

數字只引用程式生成的 observation；新算式回到ResearchEngine計算後再引用。validator可檢查ID存在、數字吻合、來源時點與引文位置；不能保證每個語意推論都正確，因此離線另建人工標註案例評估支持／矛盾／無證據。JEV與一般本地模型共用案例，測中文事件分類、引用正確率、延遲與記憶體。

LLM故障時，輸出程式生成的事實表與「敘述模型不可用」狀態，仍保留資料快照；不把降級報告算作LLM驗收通過。

## 9. 每日輸出範本與排程草案

報告依序顯示：

1. Run日期、cutoff、來源／模型版本、COMPLETE／DEGRADED／BLOCKED。
2. 150檔品質總表、各資料組日期與覆蓋率、未啟用指標。
3. 市場價量與指數背景，明列各自資料日。
4. 公司營收、財報、估值與事件事實；區分事實、推論、反證。
5. 籌碼資訊的市場覆蓋缺口，及近期已知權益事件。
6. 可以進一步驗證的研究假說，不能確認的事項。
7. 來源索引、原始快照hash、公式版本、執行／恢復紀錄。

擬定的本地目錄：

```text
artifacts/research/<run_id>/
  manifest.json          # 輸入版本、cutoff、hash與狀態
  quality.json           # 150檔及各dataset品質
  capabilities.json      # 能力可用性與停用原因
  observations.json      # 事實及lineage
  analysis.json          # 驗證後推論或確定性摘要
  report.md              # 中文報告
  trace.jsonl            # 節點耗時、錯誤、重試；無密鑰
```

排程提案（Asia/Taipei，尚未建立自動化）：盤後19:30收集價量／基本面快照，06:45補公告，07:00凍結晨間研究cutoff、07:15前完成報告。這些是內部時間，官方更新時間須實測，不能保證06:45抓取即完整。事件若需更高覆蓋再討論盤間輪詢；研究第一階段不保證全量新聞即時性。

原始與標準化快照先不自動刪除，至少保留整個競賽及驗收期間，磁碟占用告警；後續依實際日增量訂保留策略。研究執行在本機／M3，私人網站只展示設計與經選擇的摘要，不承載排程、checkpoint或付費資料原文。

## 10. 實作順序與驗收案例

| 步驟 | 建議交付 | 驗收 |
|---|---|---|
| S1 契約與fixtures | RunRequest、DatasetResult、Snapshot、品質碼、端點設定 | 端點均對應封存目錄；原始空白欄名不丟失；未知單位拒絕 |
| S2 A1資料閉環 | 官方HTTP adapter、檔案快照、150檔品質表 | 同資料輸入產生相同標準化hash；缺價／停牌可分辨 |
| S3 A2/A3與研究 | 可用指標、公告觀察、本地模型接口、報告 | 第一日不輸出Beta60；所有數字回源；無模型也有事實報告 |
| S4 LangGraph恢復 | 並行join、SQLite checkpoint、節點事件 | 分支timeout仍join；重啟不重複追加；replay不外連 |
| S5 故障與樣本驗收 | 固定fixtures、至少連續3個交易日影子研究 | 每日狀態誠實、缺口可查、修復次數有界；人確認驗收 |

S1–S5是本草稿的實作分解，映射U02、U03、U08、U09的部分工作，不更改原14單元順序與完成狀態。跨3個交易日觀察只是第一階段資料驗收，不替代後期72小時soak。

必要案例：ROC／西元日期、千元與元、股與張、欄名頭尾空白；休市與停牌；空陣列與HTTP失敗；晚到公告、財報修訂、未來生效但已公布的除息；上市法人缺失；樣本數不夠；注入「忽略規則」的公告片段；虛構引用；兩分支失敗；下載完成checkpoint前崩潰；LLM完成寫檔前崩潰；相同run恢復；不同cutoff必須分開快照。

## 11. 待後續確認的選擇

已確認範圍與無TEJ歷史的起步方式。以下不阻擋草稿，實作前確認：

- 晨間報告是否接受07:00 cutoff／07:15產出？或改盤後研究為主？
- 本地模型服務與主機存取方式；未接通前可先完成確定性資料報告。
- 首版是否採全部150檔品質表＋重要事件詳述？建議如此，避免每檔生成長篇且無增量的文字。
- 第二階段要在兩週內啟用趨勢與Beta時，歷史資料從何取得？本草稿保留匯入Interface，尚無資料來源承諾。

## 12. 來源與證據界線

專案依據：[競賽規則](01-rules.md)、[自主Agent設計](04-agent.md)、[決策資料需求](09-decision-data.md)、[API接入指南](11-openapi-guide.md)。本次沒有重新逐一探測368端點，沿用2026-10-09規格與9個代表實測。

LangGraph官方文件於2026-10-14查閱：[Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)、[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)。節點劃分、時間政策、HTTP預算、樣本門檻及儲存選擇為本專案設計提案。

## 2026-10-24 範圍與優先序修訂

研究管線保留，但 [R02](rounds/R02_PLAN.md) 改以 DataPack → 自主決策／配置 → 完整v4.3 D-Plan → 上傳檢核 → 明確送出 → 當日委託 → 結算／合規為首日必要路徑。本文「第一階段結束於研究報告」是舊切分，不再作為延後競賽閉環的理由。
