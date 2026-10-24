# 待確認事項與來源索引

> 執行政策更新（2026-10-08）：[每日 TODO](DAILY_TODO.md) 為任務、順序、狀態及验收唯一來源。以下舊 D 日期／工時僅作背景；每日使用者 2–3 小時、本地模型優先、付費 API 未授權，依新版單元執行。
## 使用者已確認

- 計畫是 **兩週**，不是一個月；14 天內需要可參賽版本。
- JEV 指 [autotrust/JEV-27B](https://huggingface.co/autotrust/JEV-27B) 或 TypeSafe Jev。
- 已有 M3 Ultra 512GB、RTX A6000、3090、A5000；外部資源包含 TEJ PRO、新聞 API、台美股資料 MCP。

## D1–2 向你收集，尚不影響本次規劃交付

1. 每日可投入時間、隊伍人數／組別、team_id 與是否完成報名。
2. TEJ 是否可用 API、可用資料表／歷史範圍、PIT 財報／下市資料；新聞 API 供應商與歷史權限；MCP 名稱及來源。
3. GPU 是否同機、OS、VRAM、遠端連線與可用時段；常駐主機／備援主機誰負責。
4. TypeSafe 存取資格、每日 API 預算、是否允許授權資料送外部模型；不要在聊天貼明文金鑰。
5. 策略偏好：跨產業品質成長是否接受、可容忍回撤與換手。方法偏好可以討論，但不人工指定正式當日持股。

## 給主辦方的問題草稿（未發送）

| 優先 | 問題 | 未釐清前處理 |
|---|---|---|
| P0 D2 | Active Share 的前 15 大聯集、正規化、現金、基準持股日期及海外 ETF 怎麼計？是否所有 30 檔都需比較？ | 雙口徑檢查、≥20% 緩衝，缺資料標未驗證 |
| P0 D2 | D-Plan 上傳／回執／庫存下載 API 或官方測試入口？是否允許自動網頁上傳？ | mock adapter；無 endpoint 不杜撰 |
| 已有答案，待實際帳戶驗證 | DataPack 已定義 outcome、excluded_codes、void_reasons 與官方 account／holdings；剩餘問題為實際結算可下載時點及費用取整等例外 | 依官方資料包對帳，不再把部分／整批結果全部列未知 |
| P0 D2 | `verify_dplan.py` 或完整 C 檢查表何時釋出？反例註解與 schema 的警示／拒收及 C 編號差異以何為準？ | 全部不一致均內部擋下，不倚賴容錯 |
| P0 D3 | 比賽中可否換模型、修 prompt、重新訓練？人搬運未修改報告是否允許？自主性稽核需要哪些證據？ | 凍結政策、只留研究影子版 |
| P1 D3 | 除權息期末入帳、分割、併股、零股、未成交及手續費取整的確切演算法？ | 專用 fixtures，未確定項不能標精確等價 |
| P1 D3 | 對無交易日、首日建倉、target floor 後零股差是否有額外語意要求？ | 首日強制建倉；0 異動轉續抱 |
| P1 D3 | 新聞／TEJ 付費內容不能公開存檔時，接受私有快照 hash 或其他佐證嗎？ | 只公開可公開來源，私有資料不外流 |
| P1 D3 | 24 日交易日曆、盤後更新 19:00 與下午說法是否最新？同日最後送出檔為準已由後台說明確認；剩餘核對首日指定日期與資料可取得時點。 | 系統回執＋官方日曆為準 |

P0 不表示本次規劃要停下，而是正式上線前必須取得答案或明確風險接受；不能以內部猜測冒稱官方合規。

## 本地文件清單及使用範圍

| 來源 | 計畫採用重點 |
|---|---|
| [競賽辦法 更新.pdf](../docs/玉山%20AI%20競技場%20比賽辦法%20更新.pdf) | P1 本金／credit；P2–5 資格／時程；P6–7 評分；P7–10 規則／例外；P11–12 日程；其餘行政條款已抽取供查閱 |
| [D-Plan 撰寫指南 v4.3](../docs/official-2026-10-24/D-Plan_撰寫指南_v4.3.md) | 全鏈追溯、posture、庫存、官方取整、提交檢查 |
| [D-Plan schema v4.3](../docs/official-2026-10-24/D-Plan.schema_v4.3.json) | 正式結構／型別／數量／字串限制；schema 不取代語意驗證 |
| [正例 TEAM_042](../docs/D-Plan_TEAM_042_2026-10-27.json) | 正向結構 fixture；樣例資料不可當實際市場資料 |
| [反例 TEAM_043](../docs/D-Plan_TEAM_043_2026-10-27.json) | 缺引用、委託不一致、宣告不一致的語意負例 |
| [150 檔清單](../docs/玉山挑戰賽%20投資組合%20150檔清單.pdf) | 固定白名單及上市／上櫃映射 |
| [主動 ETF 列表](../docs/玉山挑戰賽%20主動型ETF列表%20v1.pdf) | 2026/9/11 列表，共 30 檔；不是最新持股表 |
| [策略說明 DOCX](../docs/玉山挑戰賽%20ETF%20投資策略說明.docx) | 名稱 20 字、主題 50 字、理念 100–300 字 |
| [策略範例 PDF](../docs/玉山挑戰賽%20ETF%20投資策略範例.pdf) | 可用因子與主題一致性要求 |
| [Google credit 領取](../docs/玉山挑戰賽%20Google%20Token%20Credit%20領取方式.pdf) | 課程、10/19 證明、兌換／失效日期 |

`sources/` 是本次從全部 PDF／DOCX 抽取的本地查閱文字；原文件是證據來源，抽取文字不能取代排版或更新版本。規則 P8 已做視覺核對。來源文件雜湊記在 `source-manifest.json`，日後可比對版本變動。

## 外部一手來源（查閱日 2026-10-07）

| 來源 | 支持的事實／限制 |
|---|---|
| [AutoTrust JEV-27B 模型卡](https://huggingface.co/autotrust/JEV-27B) | 模型來源、typed decision、vLLM head、權重與作者自報評測；非中文金融驗證 |
| [TypeSafe Jev 官方介紹](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | 原廠 System One 決策服務定位；行銷「無幻覺」不代表判斷永遠正確 |
| [TypeSafe 快速入門](https://docs.typesafe.ai/introduction/quickstart) | API／SDK 接入依據，實作時固定版本 |
| [TypeSafe 模型列表](https://docs.typesafe.ai/models) | 可用型號、alias 等資訊需在實作時再核對 |
| [TypeSafe 已知弱點](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | 應加入失敗案例評測，不能只看宣傳分數 |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | checkpoint／store 與重啟持久化 |
| [LightGBM LambdaRank](https://github.com/lightgbm-org/LightGBM/blob/main/examples/lambdarank/README.md) | 排序模型官方示例 |
| [Microsoft Qlib](https://github.com/microsoft/qlib) | 可參考量化研究架構與 ML／RL 管線 |
| [Amazon Chronos](https://github.com/amazon-science/chronos-forecasting) | Chronos-2 支援多變量／協變量 |
| [Google TimesFM](https://github.com/google-research/timesfm) | TimesFM 3.0 與自架權重授權區別 |
| [TEJ API](https://api.tej.com.tw/) | API 存在；不證明本帳戶已購買接口或 PIT 資料 |

官方競賽網站本次讀取失敗，競賽日期與規則依使用者本地文件整理；D1 務必登入確認最新公告。模型最新狀態僅指本次官方頁面查證結果，不表示已遍歷所有市場模型。

## 2026-10-24 來源增補

12份官方附件已依使用者稽核副本封存於 `docs/official-2026-10-24/`，本地hash核對其中6份與既有檔案相同。新增DataPack規格與後台操作PDF；schema／指南及兩個範例更新。manifest保留來源與hash；公告時程依使用者稽核，本輪公開頁未成功重取。Active Share正規化／比較日期、自動化與人工搬運許可、金額取整仍需確認；已明確定義的DataPack語意與兩階段繳交不再視為全然未知。
