# 專案開發與運算設備

本檔適用於本專案及其子目錄；同時遵循上層 AGENTS.md。設備清單來源為 `planning/SERVER.md`。

## 可使用的遠端設備

SSH 帳號均為 `nelson`，連接埠為 `22`。截至 2026-10-24，以下六台均已實測通過 SSH 金鑰登入與硬體查詢；169、124 已在使用者安裝公鑰後重測成功。當日後續實作時 M3 的 SSH 連線逾時，3090 備援仍可達且成功抓取七個官方資料源；連線狀態每次工作前重查，不把早先成功當永久可用。

| 設備 | SSH 目的地 | 允許使用的實體 GPU 編號 | 實測 GPU 記憶體／統一記憶體 | 預設 Python |
|---|---|---|---|---|
| NVIDIA RTX A6000 ×2 | `nelson@192.168.157.165` | `0,1` | 每張 49140 MiB（約 48 GiB） | 3.10.14 |
| NVIDIA RTX A5000 | `nelson@192.168.157.161` | **僅 `1`** | 24564 MiB（約 24 GiB） | 3.10.14 |
| NVIDIA RTX A5000 | `nelson@192.168.157.169` | **僅 `0`** | 24564 MiB（約 24 GiB） | 3.10.14 |
| NVIDIA GeForce RTX 4060 Ti | `nelson@192.168.157.124` | **僅 `0`** | 16380 MiB（約 16 GiB） | 3.10.14 |
| NVIDIA GeForce RTX 3090 | `nelson@120.107.172.133` | **僅 `0`** | 24576 MiB（24 GiB） | 3.12.3 |
| Apple M3 Ultra，80 核 GPU、32 核 CPU | `nelson@192.168.157.135` | Apple GPU，使用 Metal／MPS／MLX | 512 GiB 統一記憶體 | 3.9.6 |

## 使用方式與資源限制

- 優先以完整 `nelson@IP` 連線，避免依賴某台本機才有的 SSH alias。自動化使用 `BatchMode=yes`、有限的連線逾時與既有主機金鑰驗證；不要關閉主機金鑰驗證。
- 僅使用表格中允許的實體 GPU。啟動任務前查詢該 GPU 的使用量與剩餘記憶體，依當下容量安排；不能把一次查詢的空閒量當成資源預留，也不要停止其他人的程序。
- NVIDIA 任務須在程序啟動前限制 `CUDA_VISIBLE_DEVICES`。例如 161 必須使用 `CUDA_VISIBLE_DEVICES=1`，此時程序內的 `cuda:0` 對應實體 GPU 1；165 可選 `0`、`1` 或 `0,1`，其餘 NVIDIA 主機只能選 `0`。
- 如需嚴格對應 `nvidia-smi` 的實體編號，可先以 `nvidia-smi -i <允許編號> --query-gpu=uuid --format=csv,noheader` 取得 UUID，再將這些 UUID 指定給 `CUDA_VISIBLE_DEVICES`，避免 CUDA 裝置列舉順序造成誤用。
- M3 Ultra 使用統一記憶體，沒有 CUDA；不得套用 NVIDIA 的 GPU 編號與 CUDA 設定。模型與後端需依 MLX／MPS 支援情況實測。
- 本專案 Python 版本要求以 `pyproject.toml` 為準，目前為 3.12 或 3.13。除 3090 主機外，各機的預設 Python 都不足，執行前先確認是否有相容版本，並使用獨立專案環境及鎖定依賴。
- SSH 與硬體查詢成功，不代表 PyTorch／CUDA／MLX、本地模型服務或長時間任務已通過驗收。實際工作前須核對執行環境；長時間任務保留日誌、任務識別與可恢復的輸出。
- 不將 SSH 私鑰、密碼或 API token 寫入專案、報告或網站；沿用本機 SSH 金鑰與遠端已有的授權。
- 多台 Linux 主機有 `LC_ALL=en_US.UTF-8export` 的 locale 警告，建立環境時需確認 locale。不要為了消除警告而直接覆寫使用者的 shell 設定。

## 連線範例

```sh
ssh -o BatchMode=yes -o ConnectTimeout=8 nelson@192.168.157.165 'nvidia-smi -i 0,1'
ssh -o BatchMode=yes -o ConnectTimeout=8 nelson@192.168.157.161 'nvidia-smi -i 1'
ssh -o BatchMode=yes -o ConnectTimeout=8 nelson@192.168.157.169 'nvidia-smi -i 0'
ssh -o BatchMode=yes -o ConnectTimeout=8 nelson@192.168.157.124 'nvidia-smi -i 0'
ssh -o BatchMode=yes -o ConnectTimeout=8 nelson@120.107.172.133 'nvidia-smi -i 0'
ssh -o BatchMode=yes -o ConnectTimeout=8 nelson@192.168.157.135 'sysctl -n hw.memsize; python3 --version'
```

## 設備紀錄

- 原始清單：`planning/SERVER.md`。
- 初次測試與公鑰安裝指令：`planning/SERVER_TEST_2026-10-24.md`；該文件中的認證失敗是初次測試結果，後續重測狀態以本檔及該文件的重測紀錄為準。
- 內網位址、設備使用量與連線紀錄留在本地文件；不要隨一般網站規劃文件自動發布。
