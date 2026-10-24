# 交易事件風險關卡：首版實作與證據

更新：2026-10-24。已接入11個官方交易事件來源，將決策來源由7個擴充為18個。這是內部風險篩選首版；完整交易狀態、公司行動與官方檢核仍未驗收，不代表可直接正式送出。

## 流程中的位置

```text
18來源快照＋官方DataPack＋凍結政策
→ 行情／帳戶檢查
→ 交易事件正規化、停復牌時間線及生效日檢查
→ 排除不適合新買的候選
→ 自主排序／配置／股數換算／D-Plan
→ 獨立核對委託是否違反風險政策
→ 本地候選、事件證據及發布阻礙
```

資料收集仍在LangGraph外部執行。圖中的prepare處理事件，rank與allocate只接收允許新買的候選，validate再次核對每筆BUY／SELL。遇到持有且不可賣出或事件未釐清的股票，整份候選阻擋，避免盲目出清；目前尚未實作鎖定這類持股後重新配置的政策。

研究profile仍為15個預設來源，決策profile為18個；不能把18來源驗收擴張稱全部端點皆已接通。這版仍是確定性規則，沒有呼叫LLM／ML／RL／JEV。

## 11個已接入的來源

| ID | 官方端點 | 檢查內容與日期意義 | 本次下載列數 |
|---|---|---|---:|
| TWSE-063 | [TWTAWU](https://openapi.twse.com.tw/v1/exchangeReport/TWTAWU) | 暫停／恢復交易的實際日期與時間，按交易時段判定 | 1 |
| TWSE-072 | [TWT85U](https://openapi.twse.com.tw/v1/exchangeReport/TWT85U) | 變更交易名單；沒有資料日欄，僅以取得時間表達快照 | 10 |
| TWSE-108 | [punish](https://openapi.twse.com.tw/v1/announcement/punish) | 公布日與處置起訖分開；不能以公布日代替生效區間 | 3 |
| TWSE-116 | [notice](https://openapi.twse.com.tw/v1/announcement/notice) | 注意股票；本次為官方空代碼的「無事件」列 | 1 |
| TWSE-126 | [TWT48U_ALL](https://openapi.twse.com.tw/v1/exchangeReport/TWT48U_ALL) | 預告除權息日；未來生效日可以是截止前已知消息 | 22 |
| TPEx-003 | [tpex_spendi_today](https://www.tpex.org.tw/openapi/v1/tpex_spendi_today) | 當日停復牌摘要；空代碼、空事件列為明確無事件 | 1 |
| TPEx-004 | [tpex_spendi_history](https://www.tpex.org.tw/openapi/v1/tpex_spendi_history) | 停牌與復牌可拆兩列；Date可能只有民國年，不能當公布日 | 362 |
| TPEx-015 | [tpex_exright_prepost](https://www.tpex.org.tw/openapi/v1/tpex_exright_prepost) | 使用原欄位ExRrightsExDividendDate，辨認除權息生效日 | 71 |
| TPEx-016 | [tpex_cmode](https://www.tpex.org.tw/openapi/v1/tpex_cmode) | 變更／分盤／管理／停止買賣，支援官方全形Ｙ | 21 |
| TPEx-020 | [tpex_trading_warning_information](https://www.tpex.org.tw/openapi/v1/tpex_trading_warning_information) | 注意資訊與資料日，預設只註記 | 20 |
| TPEx-021 | [tpex_disposal_information](https://www.tpex.org.tw/openapi/v1/tpex_disposal_information) | 公布日、處置期間與措施分開，支援民國連續日期區間 | 13 |

列數為整個API回應，不是150檔白名單內的事件數。已保存原始物件hash、列號、來源URL與取得時間。官方Swagger入口：[TWSE](https://openapi.twse.com.tw/)、[TPEx](https://www.tpex.org.tw/openapi/)。

## 內部政策與官方事實分開

| 情況 | 首版處理 | 限制 |
|---|---|---|
| 停牌區間與09:00–13:30交易時段重疊 | 阻擋買賣；已有持股時整份候選受阻 | 沒有復牌時間不得猜測恢復；不同列須合併成時間線 |
| 注意股票 | 附註，預設不排除新買 | 注意不等於官方禁止交易；可版控調整政策 |
| 交易日落在處置名義期間 | 依內部政策排除新買，允許其他檢查通過的賣出 | 不是宣稱交易所禁止買進；遇順延仍須新公告確認 |
| 變更／分盤／管理交易 | 依內部政策排除新買 | 官方限制與內部較保守選擇分開 |
| 除權息介於行情基準之後至交易日 | 排除新買並阻擋未驗證的賣出換算 | 不自行改官方庫存、不動用應收權益；價格調整尚未驗收 |
| 缺日期、未知旗標、無法解析的當日停復牌文字 | 對相關股票阻擋；無法辨認代碼時阻擋全份候選 | 不能把解析失敗當沒有事件 |
| 來源失敗、缺失或取得時間超過36小時 | 阻擋本地候選 | 最新一次失敗不能默默退回較舊的成功資料 |
| 取得快照早於交易日前一日19:30 | 保留「收件窗需更新」發布阻礙 | 這是內部最低更新門檻，不能保證之後沒有新消息；正式產出前仍應重抓 |

空陣列與已觀察的官方空白列可表示無事件；未認得的空白格式不接受。處置期間早於交易日，只記錄名義期間已過，不宣稱不可能順延。資本減少、分割、合併、終止上市、所有正式停止買賣等覆蓋未完整，仍保留範圍不足的發布阻礙。

## 本次真實資料結果

- 11項事件來源均完整下載並通過本次格式檢查；150檔行情有效，128檔滿足基線因子條件。
- 5檔白名單股票有注意資訊，依預設政策附註。1檔歷史停復牌以兩列配對後正確解除，不因缺少同列復牌欄而永久排除。
- 本次事件快照沒有觸發新買或賣出的阻擋；這不是保證正式交易日沒有風險。
- 自主產生25檔、25筆委託，D-Plan引用18來源，本地schema／語意及9組價格情境通過；沒有上傳、試繳或正式送出。
- 39項程式測試通過，新增涵蓋停復牌配對／重複列、盤中復牌、未來事件、注意與處置區分、除權息基準、未知格式、空白回應、時效、政策版本及持有停牌股阻擋。

個股清單、帳戶與實際配置保留本地。候選新增trading-risk.json、trading-risk-policy.json，連同原始引用、公司觀測的風險來源與manifest保存；風險政策也納入D-Plan code_version。相同run-id不能套用新政策或新程式，須建立新run。

## 下一步與發布阻礙

1. 依 [30檔ETF來源盤點](api-research/etf-holdings-readiness-2026-10-24.md) 接入實際持股。現有盤點不是benchmark，0／30封存快照，Active Share仍受阻。
2. 補足交易狀態／公司行動範圍，並於正式收件窗重抓；不能沿用10/24快照宣告10/27安全。
3. 完成官方試繳、明確送出及歷史／當日委託核對；Agent策略PDF、官方費用取整、結算對帳及樣本外績效仍待驗收。

本輪沒有更改U01–U14的驗收狀態，也沒有啟用任何提交傳輸。
