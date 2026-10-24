# 遠端設備連線測試（2026-10-24）

## 公鑰安裝後重測

使用者執行公鑰安裝後，2026-10-24 重測以下兩台均成功；六台設備目前皆可使用 SSH 金鑰登入。

- `nelson@192.168.157.169`：GPU 0 為 RTX A5000，24564 MiB，預設 Python 3.10.14。
- `nelson@192.168.157.124`：GPU 0 為 RTX 4060 Ti，16380 MiB，預設 Python 3.10.14。

設備與使用限制已寫入專案根目錄 `AGENTS.md`。以下保留初次測試紀錄，無需再次執行公鑰安裝指令。

## 初次測試

依 SERVER.md 指定主機及 GPU 編號進行唯讀測試。帳號為本機 SSH 設定的 `nelson`；使用 BatchMode 與既有主機金鑰驗證，沒有修改遠端設定或啟動運算負載。

| 設備 | 位址 | 允許 GPU | SSH 金鑰登入 | 實測硬體／環境 |
|---|---|---|---|---|
| RTX A6000 | 192.168.157.165 | 0,1 | 成功 | 2 × A6000，各 49140 MiB；RAM 約 503 GiB；Python 3.10.14 |
| RTX A5000 | 192.168.157.161 | 1 | 成功 | A5000 24564 MiB；RAM 約 251 GiB；Python 3.10.14 |
| RTX A5000 | 192.168.157.169 | 0 | 金鑰認證失敗 | 尚無法驗證硬體 |
| RTX 4060 Ti | 192.168.157.124 | 0 | 金鑰認證失敗 | 尚無法驗證硬體 |
| RTX 3090 | 120.107.172.133 | 0 | 成功 | RTX 3090 24576 MiB；RAM 約 63 GiB；Python 3.12.3 |
| M3 Ultra | 192.168.157.135 | Apple GPU | 成功 | M3 Ultra、80 核 GPU、512 GiB 統一記憶體、32 核 CPU；預設 Python 3.9.6 |

## 請在你的本機終端機執行

以下兩台回覆 `Permission denied (publickey,password)`，代表網路與 SSH 服務可達，但本次沒有成功以現有金鑰認證。這不一定代表完全沒安裝過公鑰，也可能是帳號或遠端 authorized_keys 設定不同。

```sh
ssh-copy-id -i ~/.ssh/id_ed25519.pub nelson@192.168.157.169
ssh-copy-id -i ~/.ssh/id_ed25519.pub nelson@192.168.157.124
```

依提示輸入對應遠端帳號密碼；若帳號不是 nelson，先替換使用者名稱。完成後可驗證：

```sh
ssh -o BatchMode=yes nelson@192.168.157.169 'nvidia-smi -i 0 --query-gpu=index,name,memory.total --format=csv,noheader'
ssh -o BatchMode=yes nelson@192.168.157.124 'nvidia-smi -i 0 --query-gpu=index,name,memory.total --format=csv,noheader'
```

## 開發環境與資源注意事項

- 本專案需要 Python 3.12 或 3.13。165、161 與 M3 的預設 Python 版本不足；尚未檢查其他已安裝的 Python 或建立專案環境。
- A6000 測試時 GPU 0／1 已使用約 15.6／11.4 GiB；A5000 GPU 1 約使用 2.4 GiB；3090 約使用 88 MiB。使用量是當下快照，並非可用資源保留。
- NVIDIA 設備測試已確認驅動與指定 GPU 可查詢；尚未驗證 PyTorch、CUDA 運算、本地模型服務及長時間穩定性。
- 三台成功登入的 Linux 主機回報 locale 警告：`en_US.UTF-8export`。未影響本次查詢，之後建立執行環境時需檢查 shell 的 locale 設定。
- 後續使用 A5000 的 192.168.157.161 時，應設定 `CUDA_VISIBLE_DEVICES=1`；此時程式內的 `cuda:0` 對應實體 GPU 1。

完整唯讀查詢結果保存在 `artifacts/server-check/2026-10-24.json`。此份包含內網位址的紀錄只保存在本地，未上傳網站。
