# 官方公開持股回應測試樣本

於2026-10-26台北時間下載的原始公開回應；每份`.meta.json`保留來源、實際UTC或帶時區抓取時間與SHA256。沒有匿名cookie、頁面session或私人登入資料。

- 安聯：[公開ETF頁](https://etf.allianzgi.com.tw/instant-estimated)正常匿名防偽初始化後的GetFundOverview及GetFundAssets；00984A與00993A評價10/22，00402A評價10/21。
- 野村：[每日資產查詢](https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets)，00980A評價10/22。
- 中信：[官方ETF頁](https://www.ctbcinvestments.com/ETF)公開API的基金代碼對照及完整股票回應，00995A評價10/22、00983A評價10/21。單次取得不代表新自動更新路徑已通過；最新自動流程HTTP403另有紀錄。
- 群益：[00982A官方持股頁](https://www.capitalfund.com.tw/etf/product/detail/399/buyback)公開CFWeb API的basic及buyback原回應；日期字串含斜線及中文時段，測試用來阻止把PCF適用日當股票評價日。

測試使用完整股票表，核對識別、列數、日期、披露權重、海外市場命名空間及失敗時阻擋舊資料。不得把這些今日取得的回應假造為歷史當時已公開可得的證據。
