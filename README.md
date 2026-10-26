# Esun 自主研究與 D-Plan 候選 Agent

目前有可操作的本機工作台，能從官方快照與 DataPack 自主產生本地 D-Plan v4.3 候選，並已接上真實本地LLM。已具備資料、規則基線、配置、股數換算、引用與驗證；尚未實作官方上傳／送出，外部合規與策略文件仍待驗收。

## 操作工作台

執行 `./scripts/start-agent.sh`，會建立需要的本機模型通道並啟動工作台；瀏覽器開啟 `http://127.0.0.1:8766`。僅使用已授權主機與既有金鑰；原始碼與依賴可重建，私人帳戶與執行快照不隨Git提供。

工作台有今日工作、候選與報告、資料與持股、繳交紀錄與對帳、研究驗證。完整說明見 [操作指南](delivery/APP_USER_GUIDE.md)，目前未完成條件見 [參賽驗收](delivery/READINESS.md)。

## 安裝

使用 Python 3.12 或 3.13，執行 `uv sync` 安裝鎖定依賴。遠端主機與允許 GPU 見 AGENTS.md；不要把 SSH 已接通當成模型環境已驗收。

## 決策資料與候選

```sh
uv run esun-research --root artifacts/live ingest --profile decision
uv run esun-research --root artifacts/live check-datapack --file /path/to/datapack.json --team-id YOUR_TEAM --trade-date 2026-10-27
uv run esun-research --root artifacts/live generate-dplan --run-id first-candidate --datapack /path/to/datapack.json --team-id YOUR_TEAM --trade-date 2026-10-27 --reference-date 2026-10-22 --mode live
uv run esun-research --root artifacts/live resume-dplan --run-id first-candidate
```

本機公開 API 下載受阻時，可在 ingest 增加 `--ssh-host`，指定 AGENTS.md 中已授權且可達的主機 IP。下載使用現有金鑰、既有主機指紋驗證及節流；不轉送憑證、不遠端運算，不支援透過此入口存取 FinMind 私有資料。10/24 實測 M3 連線逾時，3090 備援路徑成功完成25個決策來源下載。

首日參考日期依本次公告稽核為10/22，設定封存在 config/competition-session.json；其他日期用實際官方 DataPack 的 as_of_date，後台仍需核對。CLI 不接受未來 cutoff，DataPack 必須在 cutoff 前已被本地捕獲，來源也只選截止以前的快照。

使用 `--mode fixture` 只能產生測試候選，manifest 明確阻擋正式使用；禁止將舊樣本改日期冒充正式行情。相同 run-id 不接受新的資料／程式／政策；用 resume-dplan 讀取已封存參數，程式改版則建立新 run。

輸出在 `<--root 指定目錄>/candidates/<run-id>/`，包括：

- D-Plan JSON、引用 lineage、完整排名與排除原因。
- 官方帳戶基準、目標配置與參考收盤價情境下的 projected-account。
- schema／語意驗證、9組執行價／收盤價壓力情境，以及逐筆排除的結果。
- Markdown 報告、配置／交易風險政策、trading-risk.json、原始快照引用與檔案 hash manifest。

`CANDIDATE_BLOCKED_EXTERNAL_CHECKS` 表示本地候選成功產生，尚不能視為可送出；CLI 正常結束只代表本地產生成功。`BLOCKED_LOCAL_CHECKS` 會以非零狀態結束，不產生正式名稱的 D-Plan。驗收失敗的文件另存 rejected-plan.json。沒有任何命令會替你上傳或送出。

## 目前策略與邊界

首版為「營收成長與估值分散基線」，政策在 config/baseline-policy.json。對正營收成長、正本益比及足夠流動性的候選，以成長／盈餘殖利率／成交金額的百分位作60%／20%／20%排序，限制產業集中，選25檔等權，目標現金15%。參數是可重現的工程起點，沒有績效優勢證據；尚未宣稱完整品質成長、歷史趨勢、Beta或ML已驗收。

啟用 `--llm-config config/llm-local.json` 後，本地LLM補充市場與逐檔推論／反證，每次核對模型完整digest，D-Plan記錄實際版本與token用量，保留請求／回應。沒有啟用模型的版本明確標示 deterministic-no-llm，不能當作LLM驗收。模型輸出不能改動正式股數、權重及硬限制。人可討論政策與驗收；正式個股、權重與委託由規則自主產生，不提供人工覆寫欄位。

權重與目標股數使用官方 nav_tradable；本地帳本僅模擬及對帳，不動用應收權益。千股取整、費稅、動作方向、全持股覆蓋、引用、posture與現金區間均檢查。原始價格與政策使用Decimal，D-Plan數字序列化後再以官方公式重算。

18個官方事件來源已接入：停復牌按時間線合併，注意股票預設只註記，處置／變更交易依內部政策排除新買；跨行情基準的除權息暫停未驗證換算。未知事件阻擋相關買賣，持有且不可賣出時阻擋整份候選。政策在 config/trading-risk-policy.json，以 --risk-policy 指定並凍結到run；36小時取得時效及收件窗更新門檻不代表消息完整。詳見 [風險關卡](planning/19-trading-risk-gate.md)。

外部阻礙保留：完整交易狀態／公司行動範圍、正式收件窗更新、30檔ETF Active Share、官方檢核／送出、費用取整、策略PDF及樣本外績效驗證。部分未成交模擬只揭露風險，不能保證任意多檔排除或跳空後仍合規；實際結果須依次日官方資料包對帳。每日等權再平衡可能產生換手，低換手政策仍需後續驗證。

## 研究管線

`uv run esun-research ingest` 抓取預設15來源；`uv run esun-research research --run-id research-001 --as-of 2026-10-22` 生成研究報告，另存 research/。可用 `--model` 與 `--model-url http://127.0.0.1:8000/v1` 接入本地相容服務，此research命令的相容模型路徑未另作真實模型驗收；D-Plan使用Ollama的路徑已有8次呼叫全鏈證據。

原始資料存放objects/，SQLite保存索引及LangGraph checkpoint；請備份整個 --root 目錄，不能只留報告。FinMind只有認證transport，歷史adapter與相關因子未接通；不把token貼入程式、報告或網站。

## 驗證

執行 `uv run pytest -q`，本輪103項通過。涵蓋時間截止、帳戶null與首日、應收權益、官方股數公式、手算費用、60筆完整換倉、引用／股數竄改、單次快照重啟恢復、輸出完整性、來源限制及資料缺失阻擋。

D-Plan的code_version結合程式、政策、schema、競賽時程、來源設定及白名單hash；調整政策會改變識別，不依賴可變的模型alias。

## 參賽文件與最新驗證

已完成從工作台匯入實際DataPack、啟動LLM、產生25檔候選及下載驗證交付ZIP；103項測試通過。策略PDF與操作手冊在output/pdf，已逐頁檢查。使用者已確認試繳成功，但本版正式送出／策略PDF繳交仍需核對。ETF公開來源已取得29檔完整表，其中21檔可用於當前10/22比較日期；全30檔仍未完成。

不使用FinMind亦可繼續官方資料路線；歷史營收缺原始申報／更正時點時不冒充嚴格PIT回測。模型、持股及官方程序的詳細驗證範圍見planning/21-application-and-llm.md。

## 六個月歷史價量

研究驗證頁已接入官方月日行情收集與可恢復快取，使用獨立歷史目錄；2026-04至09完成150檔、900／900月份、18,481筆日紀錄。另以官方日曆與TAIEX核對124個交易日。這不代表已完成價格還原、營收／估值PIT或策略績效驗收。詳見[歷史資料驗收](planning/27-historical-prices.md)。

工作台已提供[官方流程進度](planning/30-submission-evidence.md)：分開顯示上傳、送出、委託確認、策略PDF與結算，跨版本重送使舊確認失效，操作紀錄與原始結算資料保留完整性檢查。進度為本地證據紀錄，未代替官方驗收。
