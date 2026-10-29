# LLM 主導研究版操作指南

LLM 主導研究功能已合併至 `main`。LLM負責研究動作、因子方案、比較修訂及自主選擇；程式核對數值、配置與競賽限制。既有規則基線保留作對照。

## 每日整合入口

上傳官方 DataPack 後，可直接按「更新資料並產生下一交易日 D-Plan」，自動更新決策資料、新聞、技術與籌碼，再啟動 LLM。日期取自資料包，不直接加一天；詳見 [每日流程指南](DAILY_CYCLE_GUIDE.md)。以下手動步驟保留供排查與個別更新使用。

## 從工作台操作

1. 以Python 3.12或3.13安裝鎖定依賴：`uv sync --frozen`。
2. 使用獨立資料目錄啟動：`ESUN_DATA_ROOT=artifacts/llm-agent-20261027 ./scripts/start-agent.sh`。腳本沿用AGENTS.md已授權設備的本機模型通道，不提供付費API。
3. 開啟`http://127.0.0.1:8766`，匯入官方後台最新DataPack。
4. 更新官方決策資料；另以`ingest --profile research`取得已設定的新聞與重大訊息。DataPack的行情基準與資料時點仍須一致。
5. 在「資料與持股」選官方行情基準日，按「建立／更新研究因子」。已有可重用的歷史月份不重抓；缺失或公司行動邊界保留為缺口。這項作業不會產生委託。
6. 在「今日工作」選「LLM主導研究、比較及自主選擇」；此模式必須啟用模型。按執行後，由Agent自己研究、提出至少兩個不同方案、比較與修訂，再選擇合格方案。
7. 在「候選與報告」閱讀「Agent策略比較與自主選擇」、本地驗證與外部阻礙；下載D-Plan、模型／工具紀錄及交付包。
8. 「繳交紀錄與對帳」的策略PDF會依候選模式對應文件版本。LLM版是新的策略說明草案；若後台已收既有策略文件，須先核對官方是否允許更動以及實際投資主題的一致性。本程式不替你上傳、送出或變更官方文件。

全新Git複製沒有私人DataPack、原始快照、研究因子與模型權限。請重新取得所需資料；下載到的歷史行情不能回填成當時已取得，缺參考日估值等資料會阻擋。既有本機驗證資料不隨公開網站發布。

## 命令列

```sh
uv run esun-research --root artifacts/llm-agent-20261027 ingest --profile decision
uv run esun-research --root artifacts/llm-agent-20261027 ingest --profile research
uv run esun-research --root artifacts/llm-agent-20261027 collect-agent-data --reference-date 2026-10-22 --history-root artifacts/history-202604-202609
uv run esun-research --root artifacts/llm-agent-20261027 generate-dplan --run-id llm-research-001 --datapack /path/to/DataPack.json --team-id YOUR_TEAM --trade-date 2026-10-27 --reference-date 2026-10-22 --mode live --decision-engine llm_agent --llm-config config/llm-local.json --research-data artifacts/llm-agent-20261027/agent-inputs/research-data-2026-10-22.json
uv run esun-research --root artifacts/llm-agent-20261027 resume-dplan --run-id llm-research-001
```

上述日期是首日已封存的驗證案例；其他日期請依最新官方DataPack，不可把日期改成今天來冒充新行情。公開資料本機無法連線時，ingest可加`--ssh-host`指定AGENTS.md已允許的設備。模型使用僅綁定本機的Ollama通道，實際名稱與digest在config/llm-local.json。

## 成品與恢復

`candidates/<run-id>/`包含D-Plan、策略比較Markdown、agent-research.json、agent-call-evidence.json、逐檔理由的llm-call-evidence.json、lineage、排名／配置、壓力情境、Active Share及hash manifest。模型請求／回應、每個工具結果與checkpoint均保留。

相同run固定程式、設定、來源、資料與模型版本。恢復重用已完成呼叫；程式改版或資料更新須新run。全目錄備份才足以重建，不能只留PDF。任何失敗或研究額度耗盡均保留受阻結果，不自動冒充模型已選擇基線。

本地D-Plan通過不代表正式收件、全30檔Active Share通過、成交、結算或合規。原始歷史價格的邊界過濾不是完整還原；目前沒有嚴格PIT策略績效、Sharpe或勝率驗證。

策略PDF及操作手冊PDF均依候選的決策模式提供對應版本；新分支手冊補充研究因子準備、自主選擇、恢復及草案變更條件。

## 研究上下文與失敗診斷

研究工具的完整結果、歷史假說與官方帳戶仍保存在封存證據中。每次模型呼叫會按輸入上限壓縮目錄、同義歷史分組、工具展示筆數與方案表格；原始帳戶股數、方案可行性、成本、換手與失敗情境保持可核對。省略的展示筆數會明列，不能視為模型已閱讀。

每輪 `research-agent/context-XX.json` 記錄壓縮前後大小、各區塊大小與是否通過上限。此為保守的 UTF-8 輸入預算，不是精確 tokenizer 計數；模型回傳的實際 token 用量另存在 call 紀錄中。安全必要內容仍放不下時會停止，不會跳過風險檢查。舊的受阻版本保持原樣，程式修正後須建立新版本。
