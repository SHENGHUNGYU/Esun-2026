# 資料與計算資源配置

> 2026-10-24 P0修訂：官方後台 DataPack 為正式帳戶真值。nav_tradable 是權重／現金比／股數分母，aum 含不可動用應收權益；首日有效帳戶＋空持股與待結算 null 必須分開。送出、成交、合規分軸記錄。帳戶與閉環接入提升至下一輪首要工作，取代舊「研究後才接官方帳戶」安排，詳見 [R02](rounds/R02_PLAN.md)。取得規格不代表實際隊伍資料已驗收。

> 執行政策更新（2026-10-08）：[每日 TODO](DAILY_TODO.md) 為任務、順序、狀態及验收唯一來源。以下舊 D 日期／工時僅作背景；每日使用者 2–3 小時、本地模型優先、付費 API 未授權，依新版單元執行。
## 資料使用契約

| 資源 | 用途 | D1–4 應查證 | 備援及限制 |
|---|---|---|---|
| TEJ PRO | 財報、月營收、產業分類、價量、公司行動 | PRO 是否含 API、資料表、歷史深度、PIT 與重編版本、下載／模型訓練授權 | 未含 API 就先合法匯出；不可假設 PRO 等於所有 TEJ 權限 |
| TWSE／TPEx | 原始收盤、成交量額、證券主檔 | 上市／上櫃接口、成交單位、調整情形、歷史日期可取性 | TEJ 交叉比對；官方換算必須回到交易所前日價 |
| MOPS | 財報、營收、重大訊息 | 發布時間／更正公告、代碼映射 | 原文快照與 hash，不能只有抓取時間 |
| 新聞 API | 事件特徵與來源證據 | 首次發布、更新時間、歷史全文、原始 URL、授權 | 去重；無歷史 PIT 時只前瞻影子運作，不能做假回測 |
| 台美股 MCP | 輔助行情、ADR、產業資訊、探索查詢 | provider、schema、單位、時區、限流、穩定 endpoint | MCP 是 transport；底層 provenance 不清就不進交易主線 |
| 主動 ETF 持股 | Active Share 防複製驗證 | 全部指定 30 檔、披露／生效日、歷史持股、NAV 權重 | 缺資料標 unknown；不得沿用未知時效資料稱完全合規 |
| 主辦方庫存／NAV | 次日委託權威基準 | 是否提供下載／API、例外成交、結算時點 | 本地 ledger 與官方比較；差異未解決不冒認持股 |

TEJ 官方有 API 服務，但本帳戶可用表格與授權仍需實際確認。[TEJ API](https://api.tej.com.tw/)

資料列最低包含 `security_id, exchange, effective_at, published_at, first_seen_at, fetched_at, available_at, value, unit, source_url, content_hash, revision`。回測可用條件是 `available_at ≤ decision_cutoff`，且 cutoff 之前真的可取得；缺首發時間不能直接以內容日期替代。D-Plan 的 `content_as_of` 則按官方定義填內容描述時點，不等同抓取時間。

交易日使用 TWSE 官方日曆；美股使用 America/New_York，再轉 Asia/Taipei。政策與特徵 cutoff 初版建議 07:30，08:10 提交；不靠臨近 08:55 的消息提升績效。這是內部設計，需測資料到齊時間。

## 存儲與版本

原始資料 immutable → Parquet 標準層 → DuckDB 查詢／特徵 → 實驗結果／模型 → 每日稽核包。小型運行狀態可用 SQLite，若多機 takeover 或提交鎖需要跨機一致性，再用 PostgreSQL。資料、模型和研究文檔分開；以 manifest 記 hash、as-of、授權來源和產生程式版本。

TEJ 付費資料與新聞全文保存在授权環境；官方指南建議新聞 archive_url，但不能擅自把付費內容上傳公共存檔。優先存可公開原始文章，授權內容保留私有快照並向主辦方確認可用佐證方式。這次網頁只包含規劃，不含付費資料或金鑰。

## 硬體角色與容量

以下依硬體名稱的常見容量做預案，D1 必須實查 GPU 型號、可用 VRAM、OS／driver、PCIe／互連及是否同機。M3 的 unified memory 不能與 NVIDIA VRAM 合併成單一可用池。

| 機器 | 建議工作 | 容量／相容性策略 |
|---|---|---|
| M3 Ultra 512GB | 資料倉庫、CPU 特徵／回測、開發、模型離線對照 | 大記憶體利於資料與 offload；自訂 JEV head 在 MLX／MPS 是否支援須實測，不以能載入 backbone 當成功 |
| RTX A6000（通常 48GB） | CUDA 主實驗、時序模型、JEV 量化候選 | JEV 27B BF16 純權重約 54GB，單 48GB 卡裝不下完整權重；另有 KV／activation／adapter overhead |
| RTX 3090（通常 24GB） | 小型 LLM／embedding、RL seeds、備援推論 | 27B 4-bit 純權重理論約 13.5GB，實際更多；決策 head／logprob／量化相容需驗證 |
| RTX A5000（通常 24GB） | 影子模型、事件批次、故障演練備機 | 不讓長訓練搶占正式晨間推論資源 |

AutoTrust 發布約 54GB 權重，推薦 vLLM 路徑含 decision adapter／head。不同服務介面與 head 校準方式要按照模型卡實作，不能把一般文字生成當 decision API。[模型卡部署說明](https://huggingface.co/autotrust/JEV-27B)

若 A6000＋3090 同機且軟體支援，可測切片／offload；不同機不能僅加總 VRAM 宣稱可跑。先選 2–8K token 的短證據上下文與小 batch；不追求 256K 全長。量化前後比較選項機率與校準，最好有 BF16 參考（可在足夠記憶體或支援 offload 的環境離線跑），否則如實標明沒有數值等價驗證。

**兩週內優先本地模型**：AutoTrust 本地部署最多一個開發工作日；TypeSafe 僅在已確認存取及費用授權後做少量案例驗證，記錄首 token／完整決策延遲、吞吐、峰值記憶體、失敗率及 options 一致性。沒有存取或相容性就用標準 LLM 分類接口。JEV 不從零訓練，僅在評測顯示明確不足且尚有餘裕時研究小規模適配，不列 MVP 依賴。

## 排程與成本預算

D1–3 CPU ETL 與規則優先；D4–7 A6000 做單個模型實驗、3090 做事件抽取；D8–9 才允許短 RL／TSFM spike；D10 起凍結訓練環境，D12–14 跑穩定性測試。每日 05:00–08:45 保留推論與資料資源，正式線禁止被研究 job 驅逐。

先量測每 run token、工具費用、推論時間與存儲；本版本沒有預授權付費 API；確有必要再討論用途與總額上限。對每個實驗設定總額和 timeout；free credit 不當作可靠主預算。Google $20 credit 每隊一組、前 750 組，有課程與 10/19 證明截止，需人工處理帳號／寄送；本次未替你寄信。[領取方式](../docs/玉山挑戰賽%20Google%20Token%20Credit%20領取方式.pdf)
