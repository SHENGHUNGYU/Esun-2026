# 跨市場研究與個股損益操作

## 入口

本機工作台 `http://127.0.0.1:8766/#context`：更新免金鑰資料、查看健康與原始證據、執行本地專員分析。需先在「今日工作」匯入 DataPack 才能執行帶帳戶的專員分析。正式每日流程另會自動建立跨市場事實包，不額外執行四次模型分析。

`#holdings`：逐股成本、未實現損益及報酬率、已實現損益、已收股息、交易損益及含息總損益。可搜尋、排序、回看快照、查看已退出股票與現金差額。

## 資料來源

| 來源 | 公開文件 | 使用方式 |
|---|---|---|
| 期交所 | https://openapi.taifex.com.tw/ | PutCallRatio、DailyMarketReportFut、MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate、OpenInterestOfLargeTradersFutures；免 key，保留交易日、盤別、契約月與交易人分類。 |
| 央行 | https://data.gov.tw/dataset/7232 | 銀行間美元臺幣日收盤，免 key，政府資料開放授權第 1 版。 |
| Fed | https://www.federalreserve.gov/feeds/feeds.htm | press_monetary.xml、speeches.xml；免 key，保留 item 發布時間。 |
| 美國財政部 | https://home.treasury.gov/treasury-daily-interest-rate-xml-feed | 當年名目及實質殖利率 XML；免 key，實際連線失敗會保留原始錯誤。 |
| FRED／ALFRED | https://fred.stlouisfed.org/docs/api/fred/ | 需個人 API key，本輪未啟用；不能用未授權替代途徑或把今日修訂值當過去值。 |

各來源免 key 不代表可任意重散布，預設本地研究。沒有接入美股／ADR 個股行情、完整國際商業新聞、市場預期共識，也沒有宣稱以上來源可替代這些資料。

## CLI

在專案根目錄使用 `.venv/bin/python -m esun_research.cli --root artifacts/llm-agent-20261027 collect-context` 更新。每個來源最多一次 bounded request，三個網路工作者，十二秒 timeout；六小時內成功回應可重用。失敗回應保留內容，不繞過網站拒絕。

若要帶帳戶與研究因子建立事實包，可另加 `--run-id <新版本> --datapack <原始JSON> --research-data <因子bundle>`。

取得回傳 `context_id` 後，用 `research-board --run-id <新版本> --context-id <id> --datapack <路徑> --research-data <路徑> --llm-config config/llm-local.json` 執行分析。正式策略不讀取此研究報告。

## 保存與恢復

- `objects/`：content-addressed 原始 HTTP、證據包、角色輸入及結果。
- `public-context/<hash>.json`：封存截止與 bundle reference。
- `research-board/<run-id>/`：request、每角色輸出／模型呼叫、report。
- `research-board-checkpoints.sqlite`：角色節點 checkpoint。
- 角色已完成或失敗均不在同版本無限重試；修正程式／提示後建立新 run。
- 時效依取得時間及資料觀測日期判定；政策 RSS 無新公告不自動當成來源故障。觀測日期、item 發布時間、first-seen 各自保留。

## 損益計算與可信度

買入成本＝成交金額＋買進手續費。賣出釋出成本＝賣前平均成本×賣出股數。已實現損益＝賣出金額－手續費－稅－釋出成本。未實現損益＝可交易股數×官方收盤價－剩餘成本；報酬率＝未實現損益／剩餘成本。沒有扣尚未發生的賣出費用。

交易損益＝未實現＋已實現；含股息總損益還需有完整已收股息證據。應收現金與應收股數仍由官方帳戶另列，不可動用或提前併入可交易股數。無法證明完整權益歷史時，總損益顯示未知，而交易損益仍可顯示。

重建估計僅在相鄰官方快照且 outcome=executed 時，用實際股數差與官方日成交金額／量推算，費稅按競賽費率估計。被排除股票、資料缺漏、權益股數異動與不連續快照不猜成本。逐日列現金變化及殘差；殘差可能包含費用取整、成交口徑、權益或未解釋事件，不能為湊帳回填個股價格。

已附證據也不自稱官方獨立驗證。歷史候選不是成交證明。人工成本只錨定該快照剩餘成本，不倒推未知已實現損益。

## 成交事件 JSON

在持股頁選定目標快照，匯入 JSON 並附原始成交／權益證據：

```json
{
  "team_id": "TEAM_11179",
  "as_of_date": "2026-11-03",
  "previous_snapshot_id": "前份相鄰官方快照完整識別碼",
  "authority": "user_supplied_evidence",
  "events": [
    {"code":"2330","kind":"BUY","shares":1000,"gross_twd":"1000000","fee_twd":"1425","tax_twd":"0"}
  ]
}
```

這只是格式範例，不能當實際成交輸入。事件支援 BUY、SELL、DIVIDEND（已收淨現金，shares=0）、SHARE_ADJUSTMENT（有證據新增可交易股數，零金額，原剩餘總成本保留）。複雜合併、分割減股、成本拆分尚未支援，需保留未知並人工核對。

逐筆套用後的股數必須與官方完整庫存一致。每快照事件不可覆寫；相同原始檔與證據再次匯入為冪等。若原始資料有誤，需建立明確修正版快照／更正流程，不能直接改舊紀錄。
