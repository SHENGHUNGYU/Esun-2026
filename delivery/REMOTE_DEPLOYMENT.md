# 私有遠端容器部署

## 拓樸

Linux 主機維持既有 Ollama；工作台以 Docker Compose 運行，應用只監聽主機 127.0.0.1:8766。使用者透過 SSH 本機轉送開啟原來的 localhost 工作台。容器不管理 GPU，也不掛入 SSH 私鑰。

Compose 使用 host networking，容器能存取主機 loopback 模型服務；不發布對外網路介面。工作台與歷史資料、輸出以 volume 分開保存。`ESUN_SERVER_MODEL_CONFIG` 指定已確認 digest、base_url 為 `http://127.0.0.1:11434` 的模型設定。

## 設定

`deploy/compose.yaml` 需要私有環境檔，範例：

```dotenv
ESUN_RELEASE=<release-id>
ESUN_PROJECT_DIR=<container-project-path>
ESUN_DATA_DIR=<host-private-data-path>
ESUN_SERVER_MODEL_CONFIG=<host-model-config-json>
ESUN_UID=<host-user-uid>
ESUN_GID=<host-user-gid>
```

私有環境檔、主機 IP 與實際路徑不發布到規劃網站。既有封存紀錄包含絕對路徑，因此首次搬移可將容器 PROJECT_DIR 設為原專案根目錄，讓歷史路徑在容器內仍可讀；主機本身使用一般 Linux 目錄。

```sh
docker compose --env-file <private-env> -p esun-agent-prod -f deploy/compose.yaml build
docker compose --env-file <private-env> -p esun-agent-prod -f deploy/compose.yaml up -d
```

## 備份與還原

1. 確認沒有執行中工作，建立 runtime 根目錄 `maintenance-readonly.json`，暫停所有工作台寫入及 CLI 工作。
2. 暫停工作台，再執行 `scripts/migration_snapshot.py`。它保存未提交原始碼、設定、資料與輸出，跳過虛擬環境、Git、快取、憑證及巢狀搬移備份。
3. SQLite 使用 backup API，逐庫 `PRAGMA quick_check`；不直接複製 WAL／SHM。產出逐檔 SHA-256 manifest 與壓縮包 checksum。
4. 還原前核對壓縮包，還原後驗證全部 manifest 檔案及 SQLite 完整性。資料移到持久化目錄，再建置 Linux 環境，不搬 macOS .venv。
5. 在唯讀狀態測試帳戶、報告、原始物件、PDF 及模型 digest。公開端點／模型呼叫等寫入測試使用獨立 smoke 根目錄。
6. 正式切換時只解除遠端維護標記，本機保留唯讀備份並停用原應用服務；同一資料集維持單一寫入者。

## 安全切換及恢復

保留原本機 launchd plist、原始備份、遠端 release、資料根目錄及 compose 環境。不可把本機舊資料立即當成回退後的最新真值：遠端若已產生新工作，回退前需重新暫停遠端、備份並同步增量後驗證。避免兩端各自產生正式版本。

工作台 `GET /api/health` 顯示執行位置與唯讀狀態。`maintenance-readonly.json` 存在時，非 GET／HEAD 操作回覆 423、Jobs.start 拒絕啟動、CLI 拒絕寫入。這是維護機制，不是跨多主機分散式鎖。

舊 run 的程式雜湊不會因搬移改寫；若程式版本已改變，舊受阻 run 仍需依原有規則另建修正版。完整物件可讀不代表每個舊進程能直接續跑。

## 驗收清單

- 壓縮包及逐檔 checksum、SQLite quick_check。
- Linux 容器完整測試、健康檢查及重啟後資料仍在。
- 最新帳戶與 25 檔持股、成本覆蓋及估計可信度一致。
- 已有 D-Plan 下載雜湊、PDF 中文字型與公開資料原始證據。
- 與既有 Ollama digest 一致、獨立結構化模型測試成功。
- 獨立來源收集與歷史資料回放；不向官方平台送出任何文件。
- 只監聽 loopback，本機 SSH 轉送可用，舊本機寫入端已停用。

## 首次部署驗收（2026-11-04）

Release：`20261104-r01`。完整備份 10,000 檔、1,099,117,755 bytes；壓縮包 256,590,369 bytes，SHA-256：`2bea9860fe5d41ec77c1fa0733fe8e2ed9a96c28c15776a9ba742478d8b1b4a2`。13 個 SQLite 庫通過一致性備份及還原檢查。

本機與遠端 Linux 容器皆為 185 tests passed。36 份候選 manifest 通過雜湊驗證；763 格因子回源重算；21,331 筆歷史資料可讀。既有 PDF 可產生；最新 D-Plan 雜湊維持 `f1714eebb9d6907f6a52f91d1a9930c93057a630658ac3968b610f75587d5e61`。

遠端模型 digest 一致，結構化 smoke call 成功；九個免金鑰跨市場端點及 TWSE-108、TPEx-004、指定日行情通過直接連線驗證。Docker 重啟後資料可讀，Docker systemd 已 enabled。這些屬搬移驗收，不代表已通過長時間 soak 或策略績效驗證。

21:21（Asia/Taipei）切換至遠端正式寫入端。本機工作台改為 SSH 存取；本機舊資料維持唯讀，原應用服務停用。請重新整理頁面取得遠端的新 CSRF token。

本機 `scripts/start-agent.sh` 在已搬移狀態下會恢復 SSH UI 通道並檢查遠端健康，不另啟動本機正式服務。若要開發獨立本機環境，須明確設定 `ESUN_LOCAL_DEVELOPMENT=1`、獨立資料根及不同連接埠。
