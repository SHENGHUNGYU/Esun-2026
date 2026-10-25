# R02：試繳與首日正式參賽閉環

修訂：2026-10-26。取代原三日研究報告安排；舊案保留於 [研究支線](R02_RESEARCH_DEFERRED.md)，核心交付完成後再排。範圍為 U02／U03／U04／U05／U06／U09／U10／U13／U14 的必要切片，ML／JEV／RL 及大規模歷史研究延後。既有 U01–U14 狀態不自動完成，也不要求先完成研究支線才開始準備試繳。

## 目前狀態與時程基準

已有研究管線、9 項既有測試與 150 檔官方樣本驗證；已新增本地 DataPack adapter，使用者提供的實際首日資料通過本地帳戶檢查；已完成自主規則配置與完整v4.3 D-Plan候選，真實十八來源／首日帳戶的本地檢查通過；尚無官方上傳、送出或結算對帳的成功證據。六台主機 SSH 已接通，不代表遠端模型與競賽系統已驗收。

以下日期為使用者本次公告稽核提供，時區 Asia/Taipei；本輪重取公告頁尚未成功，須在實際後台核對。附件結構與 DataPack 語意已依本地封存副本重讀，不能把公告未重取解讀成時程可延後。

| 時點 | 必要結果 | 缺證據時的處理 |
|---|---|---|
| 10/24 | 封存 v4.3、核對 DataPack、完成最小自主決策及本地驗證 | 立即列阻礙，先處理實際帳戶／行情，不做模型擴充 |
| 10/25 23:59 前 | 完成官方試繳要求，保存檢核與必要送出證據 | 核對試繳頁要求；不能將本地驗證或只上傳當完成 |
| 10/26 | ETF 策略 PDF 在後台標示期限前完成提交；確切截止時間待後台核對 | PDF 產生、字數、畫面與繳交狀態均須驗證 |
| 10/26 19:30–10/27 08:55 | 首個正式收件窗：有效 DataPack → Agent → 檢核 → 送出 → 委託確認 | 使用官方指定首日行情基準 10/22；不得硬套一般前一交易日推算 |
| 10/27 結算產生後 | 官方結果對帳、違規／提示分流、建立次日輸入 | 結算未產生須等待重新下載，不得當空手重建 |

原 72 小時連續測試在首日截止前已無法假定完成。可立即開始累積穩定性證據，但未滿時數必須揭露；試繳通過不等於正式可運作，也不等於已驗收收益或完整穩定性。

## P0-1：新版規格與帳戶真值

- 封存 12 份附件及 hash，以 `docs/official-2026-10-24/manifest.json` 為版本證據。產出 D-Plan 4.3；schema 版本字串允許 4.x，不宣稱 4.2 字串必然拒收。
- 以 schema 驗證 sources≤50、observations≤100、inferences≤60、decisions≤60、orders≤60、no_trade_decisions≤30；source_ref≤10、decision.inference_refs≤8。持股檔數仍為 20–30。
- 實作 DataPack adapter，保存原始 bytes/hash、team_id、trade_date、as_of_date、generated_at、版本與 missing；DataPack 版本獨立於 D-Plan，不硬編碼必須 4.3。
- 首日有效 account＋holdings=[] 視為真實全現金；missing 有 prev_settlement 或 account／holdings=null 則阻擋建倉。prev_close／skipped 不可判為通過。
- nav_tradable 為權重／現金比／股數分母；aum 僅總資產，應收配息配股不可使用。持股檔數按 shares>0，與官方 holdings_count 核對。
- 驗收：至少涵蓋首日、待結算、正常持股、純應收配股、缺收盤價、錯隊號／交易日、未知版本或狀態等測試；有效與待結算兩種 null-as_of 必須分開。
- 輸入進度：實際隊伍代號與10/27首日 DataPack 已取得，初步確認版本3.0、有效全現金帳戶，試繳已由使用者於10/26確認成功，ETF策略PDF已產出但後台繳交待確認。帳戶明細保留本地。十八個決策來源與10/22行情已成功下載，DataPack已接入配置及文件流程；官方上傳與送出仍未驗收。

## P0-2：最小自主決策、配置與 D-Plan

本地實作已完成首版，57項程式測試通過；真實資料候選為25檔、25筆委託，本地結構／語意／價格壓力通過。Active Share與官方檢核仍待驗收，詳見 [實作進度](../18-candidate-implementation.md)。

- 從可驗證且截止前可用的因子自行排序與選股，使用版控策略與配置限制；人討論方法，不提供正式個股／權重名單。
- 僅用已成立的指標。缺歷史時停用趨勢與 Beta，缺品質財報時不得把估值或單月成長冒充完整品質因子；策略說明須誠實反映首版能力。
- 以品質成長／趨勢輪動作主題邊界，但本輪採最小可驗證實作。若僅有行情不足以支持既定策略，先修正範圍與說明，不編造證據。
- `target_shares = floor(target_weight * account.nav_tradable / reference_close / 1000) * 1000`；`order_shares = target_shares - official_shares`。只可賣 official shares，不含 receivable_shares。
- 費稅、淨額交割（含同日賣出款）、預期成交與收盤壓力、現金緩衝及整張取整後限制一併檢查。不將官方 account.cash 誤當絕對買進上限。
- D-Plan 完整 source→observation→inference→decision→order；覆蓋所有實際持股與新買入，ID、方向、股數、續抱、funding_for、posture 與宣告現金區間一致。
- Active Share 對全部指定 ETF 取得相應持股並檢查。正規化／比較日期仍待官方解釋；缺資料標未驗證，雙口徑內部緩衝不能冒充官方通過。
- 驗收：首日自主產生完整 20–30 檔組合與可驗證文件；另測完整換倉最多 60 筆委託。只有官方短樣例或兩筆委託不能當完整合規驗收。

## P0-3：試繳與兩階段送出

狀態採獨立軸記錄，避免把收件、成交與合規混為一談：

```text
artifact: generated → locally_validated → uploaded
validation: pending / passed / warned / serious_error / failed / skipped
submission: not_sent / ready / sending / unknown / submitted
orders: unconfirmed / confirmed
settlement: pending / none / unknown / voided / executed（另記 excluded_codes）
compliance: pending / verified（另記官方 violations、notices、incidents）
```

- 依官方後台：下載 DataPack → Agent 產出 → 上傳檢核 → 明確送出繳交 → 歷史紀錄確認 → 當日委託逐筆比對。
- 上傳／檢核不等於繳交；檢核不留存且不計每日 25 次，正式送出才計次，以截止前最後送出版本為準。
- 橘色警告與嚴重錯誤可能仍允許送出，但內部不得因按鈕可按就判安全；嚴重錯誤與 skipped 必須處理／揭露。
- 不杜撰官方 API。先以允許的後台方式試驗；是否允許自動化、人工搬運未修改檔案及操作授權另核對。試繳／正式環境分開，不以登入授權推定已授權正式送出。
- timeout 記 unknown，先查歷史及當日委託再判斷是否重送；單一提交者、hash 對應、版本與官方計數保存。
- 驗收：實際隊伍試繳證據、檢核內容、送出狀態／歷史與委託核對（依試繳頁可提供項目）；模擬成功不可代替。

## P0-4：ETF 策略 PDF

- Agent 產製名稱≤20 字、主題≤50 字、理念100–300 字，依正式模板再核對欄位要求；主題、已實作因子與自主決策一致。
- 轉為 PDF、檢查字型／排版／字數與檔案可讀性；後台實際收 PDF，不能只交 DOCX。
- 後台核對實際截止、檔案大小與狀態，保存提交證據。此項可與 P0-2 同步準備，但決策政策修改後須重新檢查說明一致性。

## P0-5：初始化、結算對帳與正式窗口

- 使用正式首日 DataPack 的初始資金，不沿用封測庫存或本地舊帳。保留封測資料供測試但隔離正式輸入。
- 依 prev_day_orders.outcome 區分 none／unknown／voided／executed。executed 仍可能有 excluded_codes；voided 保存全部 void_reasons。以官方新 holdings/account 覆蓋正式決策基準，本地帳本只作模擬與差異核對。
- compliance.violations 是累計違規天數，notices 是提示列數；同日多項 fail 不重複計天，warn 不計取消資格。畫面檢核警告、正式違規與成交結果分開記錄。
- 缺結算／價格、對帳不符或團隊／交易日不一致，阻擋錯誤自動決策；不得假定全成交、也不得因個別 excluded 就整批回滾。
- 10/26 晚間完成候選與檢核；10/27 08:10 首送、08:30 確認歷史／當日委託為內部目標；08:55 是官方截止，不能把本地產生時間當送達時間。
- 驗收：實際 DataPack 解析、首日交易基準、四種 outcome 與部分排除案例、累計違規對帳、未知回執恢復；實際結算尚未產生的部分列為待外部驗證。

## 執行與驗收分工

你負責：實際隊伍／後台存取、最新 DataPack、試繳與策略 PDF 的現況、主辦方歧義確認及必要的後台操作；不手改 Agent 的正式個股與權重。Codex 負責：新版 adapter、配置與文件編譯、語意驗證、測試、可重建成品與證據。

主機先使用能最快完成重建與完整資料下載者，依 AGENTS.md 限制 GPU。模型不是閉環前置條件；優先版控且可解釋的自主規則，付費 API 未預授權。小型本地模型能立即使用才接入，JEV／RL／模型比較全部移出本輪關鍵路徑。

P0-1 的本地adapter已通過首批測試，官方帳戶／整合驗收未完成；依序驗收 P0-1→P0-2→P0-3；P0-4 同步；P0-5 跨首日窗口及後續結算驗證。修訂計畫不等於上述工作已完成。若到試繳期限仍缺有效 DataPack、核心行情、完整文件或後台證據，明確判定尚未正式就緒，不能用研究報告代替。

## 來源與證據

- 本輪封存：`docs/official-2026-10-24/`，12 份附件及 manifest。
- [v4.3 schema](https://esun-ai-challenge.tw/api/events/fundaiagent/attachments/27/download/)、[指南](https://esun-ai-challenge.tw/api/events/fundaiagent/attachments/28/download/)、[DataPack](https://esun-ai-challenge.tw/api/events/fundaiagent/attachments/29/download/)、[後台說明](https://esun-ai-challenge.tw/api/events/fundaiagent/attachments/30/download/)。本輪依使用者已下載副本核對，不聲稱重新下載成功。
- [公告頁](https://esun-ai-challenge.tw/events/fundaiagent)：時程依使用者稽核提供，後台再次確認。

## 本輪實作證據更新

已新增generate-dplan／resume-dplan及可重現的SSH公開資料下載入口，帳戶→自主排名→配置→官方股數換算→完整D-Plan→本地驗證可運作。來源、排名、目標、證據、壓力結果與hash保存在私有artifacts；網站不發布原始帳戶或投組。14單元不自動完成，試繳已由使用者確認成功，策略PDF已產出，本版正式送出仍待核對。

## 交易風險與ETF盤點增補

已接入11個官方事件來源，決策profile共18來源。停復牌時間線、注意註記、處置／變更交易內部排除、除權息基準及委託二次檢查已實作；39項測試與真實資料重跑通過。仍保留交易狀態／公司行動範圍不足及正式收件窗更新阻礙。30檔ETF逐筆盤點完成，但可計算持股快照0／30；FinMind Holding／Change為Sponsor，不預設已有權限。詳見 [風險關卡](../19-trading-risk-gate.md) 與 [ETF來源盤點](../api-research/etf-holdings-readiness-2026-10-24.md)。試繳、策略PDF及官方送出仍未完成。

## 2026-10-26 應用與模型證據

已完成真實本地模型與工作台端到端候選產生，57項程式測試通過；已由本機應用下載並核對交付ZIP。ETF完整表取得16檔，其中13檔有效日期比較，本輪仍未達全30檔。策略PDF一頁與操作手冊兩頁已逐頁檢查；使用者確認試繳成功，未獨立讀取後台回執，本版正式繳交及PDF官方狀態另核對。詳見 [應用與模型驗收](../21-application-and-llm.md)。前段10/24的0／30與尚未啟用模型紀錄由本段更新，不能用舊狀態誤判新證據。
