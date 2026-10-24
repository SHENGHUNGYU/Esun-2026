# TPEx OpenAPI 全端點與欄位目錄

盤點：2026-10-09，共 225 個 operation。官方來源：[Swagger](https://www.tpex.org.tw/openapi/)、[完整規格](https://www.tpex.org.tw/openapi/swagger.json)。Base URL：`https://www.tpex.org.tw/openapi/v1`。

優先序、用途與需求關聯為本專案研究判斷；官方名稱、方法、path、參數與欄位依封存規格。需求關聯表示可支持的部分原料，不代表完整滿足該資料群。接入限制與建議見 [使用指南](11-openapi-guide.md)。

## 完整索引

| ID | 優先序 | 官方名稱 | 方法與 Path |
|---|---|---|---|
| TPEx-001 | P1 | 上櫃股票市場現況 | `GET /tpex_mainborad_highlight` |
| TPEx-002 | P3 | 上櫃股票現股當沖交易標的資訊 | `GET /tpex_securities` |
| TPEx-003 | P0 | 上櫃當日公布暫停/恢復交易股票 | `GET /tpex_spendi_today` |
| TPEx-004 | P0 | 上櫃歷史公布暫停/恢復交易股票 | `GET /tpex_spendi_history` |
| TPEx-005 | P0 | 上櫃股票行情 | `GET /tpex_mainboard_daily_close_quotes` |
| TPEx-006 | P0 | 上櫃股票收盤行情 | `GET /tpex_mainboard_quotes` |
| TPEx-007 | P1 | 上櫃股票個股本益比、殖利率、股價淨值比 | `GET /tpex_mainboard_peratio_analysis` |
| TPEx-008 | P2 | 上櫃股票融資融券餘額 | `GET /tpex_mainboard_margin_balance` |
| TPEx-009 | P1 | 櫃買指數歷史資料 | `GET /tpex_index` |
| TPEx-010 | P2 | 富櫃50指數歷史收盤指數 | `GET /tpex50_index` |
| TPEx-011 | P3 | 上櫃股票現股當沖交易統計資訊 | `GET /tpex_intraday_trading_statistics` |
| TPEx-012 | P3 | 上櫃股票熱門股證券商進出排行 | `GET /tpex_active_broker_volume` |
| TPEx-013 | P2 | 上櫃股票融券借券賣出餘額 | `GET /tpex_margin_sbl` |
| TPEx-014 | P0 | 上櫃股票除權除息計算結果表 | `GET /tpex_exright_daily` |
| TPEx-015 | P0 | 上櫃股票除權除息預告表 | `GET /tpex_exright_prepost` |
| TPEx-016 | P0 | 上櫃股票變更交易、分盤交易、管理股票與停止交易資訊 | `GET /tpex_cmode` |
| TPEx-017 | P3 | 上櫃股票零股交易資訊 | `GET /tpex_odd_stock` |
| TPEx-018 | P3 | 上櫃股票盤後定價行情 | `GET /tpex_off_market` |
| TPEx-019 | 參考 | 申請上櫃公司 | `GET /tpex_esb_applicant_companies` |
| TPEx-020 | P2 | 上櫃公布注意股票資訊 | `GET /tpex_trading_warning_information` |
| TPEx-021 | P0 | 上櫃處置有價證券資訊 | `GET /tpex_disposal_information` |
| TPEx-022 | P2 | 上櫃公布注意累計次數異常資訊 | `GET /tpex_trading_warning_note` |
| TPEx-023 | P2 | 上櫃融資融券暫停融券賣出預告表 | `GET /tpex_margin_trading_term` |
| TPEx-024 | P2 | 上櫃融資融券調整成數 | `GET /tpex_margin_trading_adjust` |
| TPEx-025 | P3 | 上櫃融資融券標借 | `GET /tpex_margin_trading_lend` |
| TPEx-026 | P2 | 上櫃信用交易餘額概況表 | `GET /tpex_margin_trading_marginspot` |
| TPEx-027 | P2 | 上櫃平盤下得融(借)券賣出之證券名單 | `GET /tpex_margin_trading_margin_mark` |
| TPEx-028 | P2 | 上櫃融資融券使用率報表 | `GET /tpex_margin_trading_margin_used` |
| TPEx-029 | P2 | 上櫃融資融券增減排行表 | `GET /tpex_margin_trading_short_sell` |
| TPEx-030 | P2 | 上櫃僑外資及陸資持股比例排行表 | `GET /tpex_3insti_qfii` |
| TPEx-031 | P2 | 上櫃各類股僑外資及陸資持股比例表 | `GET /tpex_3insti_qfii_industry` |
| TPEx-032 | P1 | 上櫃股票三大法人買賣明細資訊 | `GET /tpex_3insti_daily_trading` |
| TPEx-033 | P2 | 上櫃股票自營商買賣超彙總表 | `GET /tpex_3insti_dealer_trading` |
| TPEx-034 | P2 | 上櫃漲跌停未成交資訊 | `GET /tpex_ceil_non_trading` |
| TPEx-035 | P1 | 上櫃日成交量值指數 | `GET /tpex_daily_trading_index` |
| TPEx-036 | P2 | 上櫃當日融券賣出與借券賣出成交量值 | `GET /tpex_short_sell` |
| TPEx-037 | P3 | 上櫃各券商當日營業金額統計表 | `GET /tpex_daily_broker1` |
| TPEx-038 | P2 | 上櫃盤中個股成交金額排行 | `GET /tpex_active_dollar_volume` |
| TPEx-039 | P2 | 上櫃盤中個股漲幅排行 | `GET /tpex_active_advanced` |
| TPEx-040 | P2 | 上櫃盤中個股跌幅排行 | `GET /tpex_active_declined` |
| TPEx-041 | P3 | 上櫃應付現股當日沖銷券差借券費率 | `GET /tpex_intraday_fee` |
| TPEx-042 | P3 | 上櫃暫停先賣後買當日沖銷交易標的預告表 | `GET /tpex_intraday_trading_pre` |
| TPEx-043 | P3 | 上櫃暫停先賣後買當日沖銷交易歷史查詢 | `GET /tpex_intraday_trading_his` |
| TPEx-044 | P2 | 上櫃歷史個股市值排行 | `GET /tpex_daily_market_value` |
| TPEx-045 | P2 | 上櫃歷史個股週轉率排行 | `GET /tpex_daily_turnover` |
| TPEx-046 | P2 | 上櫃歷史個股日均量排行 | `GET /tpex_trading_volumes_avg` |
| TPEx-047 | P2 | 上櫃歷史個股日均值排行 | `GET /tpex_trading_amount_avg` |
| TPEx-048 | P2 | 上櫃歷史類股成交價量比重 | `GET /tpex_trading_volume_ratio` |
| TPEx-049 | P2 | 上櫃歷史個股本益比排行 | `GET /tpex_pe_ratio_top10` |
| TPEx-050 | P3 | 上櫃鉅額交易日成交資訊 | `GET /tpex_daily_qutoes_block` |
| TPEx-051 | P3 | 上櫃個股單一證券鉅額交易日成交資訊 | `GET /tpex_daily_trading_block` |
| TPEx-052 | P3 | 上櫃鉅額交易日成交量值統計 | `GET /tpex_daily_trading_summary_odd` |
| TPEx-053 | P3 | 上櫃鉅額交易月成交量值統計 | `GET /tpex_monthly_trading_summary_block` |
| TPEx-054 | P3 | 上櫃鉅額交易年成交量值統計 | `GET /tpex_yearly_trading_summary_block` |
| TPEx-055 | P2 | 上櫃歷史個股成交量排行 | `GET /tpex_volume_rank` |
| TPEx-056 | P2 | 上櫃歷史個股成交值排行 | `GET /tpex_amount_rank` |
| TPEx-057 | P3 | 上櫃股票等價系統成交分價表 | `GET /tpex_prvol` |
| TPEx-058 | P2 | 上櫃股票三大法人買賣金額彙總表 | `GET /tpex_3insti_summary` |
| TPEx-059 | P2 | 上櫃股票投信買賣超彙總表 | `GET /tpex_3insti_trading` |
| TPEx-060 | P3 | 鉅額交易歷史成交資訊 | `GET /tpex_daily_trade_block_day` |
| TPEx-061 | P2 | 上櫃每日暫緩開盤股票 | `GET /tpex_delayed_stock_open` |
| TPEx-062 | P2 | 上櫃每日暫緩收盤股票 | `GET /tpex_delayed_stock_close` |
| TPEx-063 | P2 | 上櫃首五日無漲跌幅資訊 | `GET /tpex_ipo_no_limit` |
| TPEx-064 | 參考 | 本國興櫃公司EPS排名 | `GET /tpex_esb_eps_rank` |
| TPEx-065 | 參考 | 興櫃公司資本額排名 | `GET /tpex_esb_capitals_rank` |
| TPEx-066 | P2 | 櫃買「富櫃200指數」當日收盤指數 | `GET /tpex200_change` |
| TPEx-067 | P2 | 上櫃公司治理指數當日成分股資訊 | `GET /tpcgi_constituents` |
| TPEx-068 | P2 | 上櫃公司治理指數歷史收盤指數 | `GET /tpcgi_reward_index` |
| TPEx-069 | P2 | 上櫃公司治理指數當日收盤指數 | `GET /tpcgi_change` |
| TPEx-070 | P1 | 櫃買指數成分股 | `GET /tpex_index_consti` |
| TPEx-071 | P1 | 櫃買指數與報酬指數之收市指數 | `GET /tpex_reward_index` |
| TPEx-072 | P2 | 櫃買「富櫃50指數」當日成分股 | `GET /tpex50_constituents` |
| TPEx-073 | P2 | 櫃買「富櫃50指數」當日收盤指數 | `GET /tpex50_change` |
| TPEx-074 | P2 | 櫃買「高殖利率指數」當日成分股 | `GET /tphd_constituents` |
| TPEx-075 | P2 | 櫃買「高殖利率指數」當日收盤指數 | `GET /tphd_change` |
| TPEx-076 | P2 | 櫃買「薪酬指數」當日成分股 | `GET /tpci_constituents` |
| TPEx-077 | P2 | 櫃買「薪酬指數」當日收盤指數 | `GET /tpci_change` |
| TPEx-078 | P2 | 櫃買「薪酬指數」歷史收盤指數 | `GET /tpci_reward_index` |
| TPEx-079 | P2 | 櫃買「勞工就業88指數」當日成分股 | `GET /tpex_emp88_constituents` |
| TPEx-080 | P2 | 櫃買「勞工就業88指數」當日收盤指數 | `GET /tpex_emp88_change` |
| TPEx-081 | P2 | 櫃買「勞工就業88指數」歷史收盤指數 | `GET /tpex_emp88_reward_index` |
| TPEx-082 | P3 | 可轉債資產交換ASO及ASW銀行承作餘額 | `GET /tpex_dpsp_monthly_CBmcs007` |
| TPEx-083 | P3 | 國際債券當日盤中報價行情表(含寶島債) | `GET /tpex_international_bond_quotes` |
| TPEx-084 | P3 | 國際債券當日盤中成交行情表(含寶島債) | `GET /tpex_international_bond_trade` |
| TPEx-085 | P3 | 國際債券(一般投資人) | `GET /tpex_international_bond_issue_investor` |
| TPEx-086 | P3 | 國際債券(僅售予專業投資人者) | `GET /tpex_international_bond_issue_org` |
| TPEx-087 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-職業安全衛生 | `GET /t187ap46_O_21` |
| TPEx-088 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-功能性委員會 | `GET /t187ap46_O_9` |
| TPEx-089 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-氣候相關議題管理 | `GET /t187ap46_O_8` |
| TPEx-090 | 參考 | 興櫃處置有價證券資訊 | `GET /tpex_esb_disposal_information` |
| TPEx-091 | 參考 | 興櫃公布注意有價證券資訊 | `GET /tpex_esb_warning_information` |
| TPEx-092 | 參考 | 興櫃推薦證券商與推薦之股票 | `GET /tpex_esb_recommended_dealer` |
| TPEx-093 | 參考 | 黃金現貨權證發行基本資料 | `GET /tpex_warrant_gold` |
| TPEx-094 | 參考 | 黃金現貨權證收盤行情 | `GET /tpex_warrant_gold_quts` |
| TPEx-095 | 參考 | 上櫃權證收盤行情日報表 | `GET /tpex_warrant_daily_quts` |
| TPEx-096 | 參考 | 上櫃權證收盤行情月報表 | `GET /tpex_warrant_monthly_quts` |
| TPEx-097 | 參考 | 上櫃權證發行基本資料 | `GET /tpex_warrant_issue` |
| TPEx-098 | 參考 | 上櫃牛熊證收盤行情(不含展延型牛熊證)日報表 | `GET /tpex_warrant_wcb_daily_quts` |
| TPEx-099 | 參考 | 上櫃牛熊證收盤行情(不含展延型牛熊證)月報表 | `GET /tpex_warrant_wcb_monthly_quts` |
| TPEx-100 | 參考 | 上櫃牛熊證發行基本資料(不含展延型牛熊證) | `GET /tpex_warrant_wcb_issue` |
| TPEx-101 | 參考 | 上櫃展延型牛熊證收盤行情日報表 | `GET /tpex_warrant_wxy_daily_quts` |
| TPEx-102 | 參考 | 上櫃展延型牛熊證收盤行情月報表 | `GET /tpex_warrant_wxy_monthly_quts` |
| TPEx-103 | 參考 | 上櫃展延型牛熊證發行基本資料 | `GET /tpex_warrant_wxy_issue` |
| TPEx-104 | 參考 | 單筆權證成交資料 | `GET /tpex_warrant_quts` |
| TPEx-105 | 參考 | 每日權證交易人數(上櫃) | `GET /tpex_warrant_statistics` |
| TPEx-106 | 參考 | 上櫃股票權證資訊 | `GET /tpex_warrant` |
| TPEx-107 | 參考 | 上櫃權證當日暫停/恢復交易資訊 | `GET /tpex_warrant_suspend_today` |
| TPEx-108 | 參考 | 上櫃權證歷史暫停/恢復交易資訊 | `GET /tpex_warrant_suspend_history` |
| TPEx-109 | 參考 | 開放式基金當日行情表 | `GET /tpex_opfund_latest` |
| TPEx-110 | 參考 | 開放式基金受益憑證造市商與造市之基金 | `GET /tpex_opfund_recommended_dealer` |
| TPEx-111 | 參考 | 開放式基金市場現況 | `GET /tpex_opfund_market_highlight` |
| TPEx-112 | P3 | 黃金現貨市場現況 | `GET /tpex_gold_market_highlight` |
| TPEx-113 | P3 | 造市商與造市之黃金現貨 | `GET /tpex_gold_recommended_dealer` |
| TPEx-114 | P3 | 黃金現貨當日行情表 | `GET /tpex_gold_latest` |
| TPEx-115 | 參考 | 創櫃板公司市場現況 | `GET /tpex_gisa_highlight` |
| TPEx-116 | 參考 | 創櫃板公司資訊 | `GET /tpex_gisa_company` |
| TPEx-117 | 參考 | 於登錄創櫃板前辦理籌資資訊 | `GET /tpex_gisa_financing_before` |
| TPEx-118 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟  | `GET /t187ap46_O_20` |
| TPEx-119 | P2 | 上櫃公司企業ESG資訊揭露彙總資料-風險管理政策  | `GET /t187ap46_O_19` |
| TPEx-120 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-社區關係  | `GET /t187ap46_O_15` |
| TPEx-121 | P2 | 上櫃公司企業ESG資訊揭露彙總資料-供應鏈管理  | `GET /t187ap46_O_13` |
| TPEx-122 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-食品安全 | `GET /t187ap46_O_12` |
| TPEx-123 | P2 | 上櫃公司企業ESG資訊揭露彙總資料-產品品質與安全 | `GET /t187ap46_O_14` |
| TPEx-124 | P2 | 櫃買「富櫃200指數」當日成分股 | `GET /tpex200_constituents` |
| TPEx-125 | P2 | 上櫃公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表 | `GET /t187ap41_O` |
| TPEx-126 | 參考 | 興櫃公司每月營業收入彙總表 | `GET /t187ap05_R` |
| TPEx-127 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-廢棄物管理 | `GET /t187ap46_O_4` |
| TPEx-128 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-能源管理 | `GET /t187ap46_O_2` |
| TPEx-129 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-投資人溝通 | `GET /t187ap46_O_7` |
| TPEx-130 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-溫室氣體排放 | `GET /t187ap46_O_1` |
| TPEx-131 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-董事會 | `GET /t187ap46_O_6` |
| TPEx-132 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-人力發展 | `GET /t187ap46_O_5` |
| TPEx-133 | P3 | 上櫃公司企業ESG資訊揭露彙總資料-水資源管理 | `GET /t187ap46_O_3` |
| TPEx-134 | P1 | 二十九大類股營收變化統計表 | `GET /mopsfin_t187ap05_OA` |
| TPEx-135 | P1 | 發行公司營收創新高一覽表(上櫃) | `GET /mopsfin_t187ap05_OB` |
| TPEx-136 | P3 | 美元固定利率不可贖回國際債券理論價格 | `GET /BDdos216UTF` |
| TPEx-137 | P3 | 美元附息固定利率可贖回國際債券理論價格 | `GET /BDdos215UTF` |
| TPEx-138 | P3 | 美元零息可贖回國際債券理論價格 | `GET /BDdos209UTF` |
| TPEx-139 | 參考 | 創櫃板公司透過籌資系統辦理籌資資訊 | `GET /tpex_gisa_financing_history` |
| TPEx-140 | P3 | 上櫃公司股東行使提案權情形彙總表 | `GET /mopsfin_t187ap35_O` |
| TPEx-141 | 參考 | 上櫃權證基本資料彙總表 | `GET /mopsfin_t187ap37_O` |
| TPEx-142 | 參考 | 上櫃認購(售)權證每日成交資料檔 | `GET /mopsfin_t187ap42_O` |
| TPEx-143 | P3 | 上櫃公司公司治理之相關規程規則 | `GET /mopsfin_t187ap32_O` |
| TPEx-144 | P3 | 上櫃公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表 | `GET /mopsfin_t187ap34_O` |
| TPEx-145 | P3 | 上櫃公司董事長是否兼任總經理 | `GET /mopsfin_t187ap33_O` |
| TPEx-146 | P3 | 上櫃公司財務報告經監察人承認情形 | `GET /mopsfin_t187ap31_O` |
| TPEx-147 | P2 | 上櫃公司董事、監察人質權設定占董事及監察人實際持有股數彙總表 | `GET /mopsfin_t187ap09_O` |
| TPEx-148 | P2 | 上櫃公司董事、監察人持股不足法定成數連續達3個月以上彙總表 | `GET /mopsfin_t187ap10_O` |
| TPEx-149 | P2 | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動公司 | `GET /mopsfin_t187ap24_O` |
| TPEx-150 | P2 | 上櫃公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司 | `GET /mopsfin_t187ap25_O` |
| TPEx-151 | 參考 | 創櫃板辦理中籌資資訊 | `GET /tpex_gisa_financing_in_process` |
| TPEx-152 | P0 | 上櫃股票基本資料 | `GET /mopsfin_t187ap03_O` |
| TPEx-153 | P2 | 上櫃股票外資及陸資買賣超彙總表 | `GET /tpex_3insti_qfii_trading` |
| TPEx-154 | 參考 | 興櫃股票當日行情表 | `GET /tpex_esb_latest_statistics` |
| TPEx-155 | 參考 | 上櫃認購(售)權證年度發行量概況統計表 | `GET /mopsfin_t187ap36_O` |
| TPEx-156 | 參考 | 興櫃公司基本資料 | `GET /mopsfin_t187ap03_R` |
| TPEx-157 | P1 | 上櫃公司每日重大訊息 | `GET /mopsfin_t187ap04_O` |
| TPEx-158 | 參考 | 券商業務別人員數 | `GET /mopsfin_t187ap01` |
| TPEx-159 | P2 | 上櫃公司持股逾 10% 大股東名單 | `GET /mopsfin_t187ap02_O` |
| TPEx-160 | P2 | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司 | `GET /mopsfin_t187ap26_O` |
| TPEx-161 | P2 | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司 | `GET /mopsfin_t187ap27_O` |
| TPEx-162 | P1 | 上櫃公司每月營業收入彙總表 | `GET /mopsfin_t187ap05_O` |
| TPEx-163 | P0 | 上櫃股利分派情形-董事會通過 | `GET /mopsfin_t187ap39_O` |
| TPEx-164 | P3 | 轉(交)換公司債買賣斷券商買賣日報表 | `GET /bond_cb_daily` |
| TPEx-165 | P2 | 上櫃公司資產負債表(金融業) | `GET /mopsfin_t187ap07_O_basi` |
| TPEx-166 | P2 | 上櫃公司資產負債表(證券期貨業) | `GET /mopsfin_t187ap07_O_bd` |
| TPEx-167 | P1 | 上櫃公司資產負債表(一般業) | `GET /mopsfin_t187ap07_O_ci` |
| TPEx-168 | P2 | 上櫃公司資產負債表(金控業) | `GET /mopsfin_t187ap07_O_fh` |
| TPEx-169 | P2 | 上櫃公司資產負債表(保險業) | `GET /mopsfin_t187ap07_O_ins` |
| TPEx-170 | P2 | 上櫃公司資產負債表(異業) | `GET /mopsfin_t187ap07_O_mim` |
| TPEx-171 | P2 | 上櫃公司綜合損益表(金融業) | `GET /mopsfin_t187ap06_O_basi` |
| TPEx-172 | P2 | 上櫃公司綜合損益表(證券期貨業) | `GET /mopsfin_t187ap06_O_bd` |
| TPEx-173 | P1 | 上櫃公司綜合損益表(一般業) | `GET /mopsfin_t187ap06_O_ci` |
| TPEx-174 | P2 | 上櫃公司綜合損益表(金控業) | `GET /mopsfin_t187ap06_O_fh` |
| TPEx-175 | P2 | 上櫃公司綜合損益表(保險業) | `GET /mopsfin_t187ap06_O_ins` |
| TPEx-176 | P2 | 上櫃公司綜合損益表(異業) | `GET /mopsfin_t187ap06_O_mim` |
| TPEx-177 | P2 | 上櫃公司財報資訊(金融業) | `GET /mopsfin_t187ap06_O_basiA` |
| TPEx-178 | P2 | 上櫃公司財報資訊(證券期貨業) | `GET /mopsfin_t187ap06_O_bdA` |
| TPEx-179 | P1 | 上櫃公司財報資訊( 一般業) | `GET /mopsfin_t187ap06_O_ciA` |
| TPEx-180 | P2 | 上櫃公司財報資訊(金控業) | `GET /mopsfin_t187ap06_O_fhA` |
| TPEx-181 | P2 | 上櫃公司財報資訊(保險業) | `GET /mopsfin_t187ap06_O_insA` |
| TPEx-182 | P2 | 上櫃公司財報資訊(異業) | `GET /mopsfin_t187ap06_O_mimA` |
| TPEx-183 | 參考 | 興櫃公司資產負債表-證券期貨業 | `GET /mopsfin_t187ap07_U_bd` |
| TPEx-184 | 參考 | 興櫃公司資產負債表-一般業 | `GET /mopsfin_t187ap07_U_ci` |
| TPEx-185 | 參考 | 興櫃公司資產負債表-金控業 | `GET /mopsfin_t187ap07_U_fh` |
| TPEx-186 | 參考 | 興櫃公司資產負債表-保險業 | `GET /mopsfin_t187ap07_U_ins` |
| TPEx-187 | 參考 | 興櫃公司資產負債表-異業 | `GET /mopsfin_t187ap07_U_mim` |
| TPEx-188 | 參考 | 興櫃公司綜合損益表-金融業 | `GET /mopsfin_t187ap06_U_basi` |
| TPEx-189 | 參考 | 興櫃公司綜合損益表-證券期貨業 | `GET /mopsfin_t187ap06_U_bd` |
| TPEx-190 | 參考 | 興櫃公司綜合損益表-一般業 | `GET /mopsfin_t187ap06_U_ci` |
| TPEx-191 | 參考 | 興櫃公司綜合損益表-金控業 | `GET /mopsfin_t187ap06_U_fh` |
| TPEx-192 | 參考 | 興櫃公司綜合損益表-保險業 | `GET /mopsfin_t187ap06_U_ins` |
| TPEx-193 | 參考 | 興櫃公司綜合損益表-異業 | `GET /mopsfin_t187ap06_U_mim` |
| TPEx-194 | 參考 | 興櫃公司資產負債表-金融業 | `GET /mopsfin_t187ap07_U_basi` |
| TPEx-195 | 參考 | 興櫃公司董監事持股餘額明細資料 | `GET /mopsfin_t187ap11_R` |
| TPEx-196 | P2 | 上櫃公司各產業EPS統計資訊 | `GET /mopsfin_t187ap14_O` |
| TPEx-197 | P2 | 上櫃公司截至各季綜合損益財測達成情形(簡式) | `GET /mopsfin_t187ap15_O` |
| TPEx-198 | P2 | 上櫃公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式) | `GET /mopsfin_t187ap16_O` |
| TPEx-199 | P2 | 上櫃公司營益分析查詢彙總表(全體公司彙總報表) | `GET /mopsfin_187ap17_O` |
| TPEx-200 | P2 | 上櫃公司董事、監察人持股不足法定成數彙總表 | `GET /mopsfin_t187ap08_O` |
| TPEx-201 | P2 | 上櫃公司董監事持股餘額明細資料 | `GET /mopsfin_t187ap11_O` |
| TPEx-202 | P2 | 上櫃公司每日內部人持股轉讓事前申報表-持股轉讓日報表 | `GET /mopsfin_t187ap12_O` |
| TPEx-203 | P2 | 上櫃公司每日內部人持股轉讓事前申報表-持股未轉讓日報表 | `GET /mopsfin_t187ap13_O` |
| TPEx-204 | P2 | 上櫃公司金管會證券期貨局裁罰案件專區 | `GET /mopsfin_t187ap22_O` |
| TPEx-205 | P3 | 上櫃公司獨立董監事兼任情形彙總表 | `GET /mopsfin_t187ap30_O` |
| TPEx-206 | P3 | 上櫃公司董事酬金相關資訊 | `GET /mopsfin_t187ap29_A_O` |
| TPEx-207 | P3 | 上櫃公司監察人酬金相關資訊 | `GET /mopsfin_t187ap29_B_O` |
| TPEx-208 | P3 | 上櫃公司合併報表董事酬金相關資訊 | `GET /mopsfin_t187ap29_C_O` |
| TPEx-209 | P3 | 上櫃公司合併報表監察人酬金相關資訊 | `GET /mopsfin_t187ap29_D_O` |
| TPEx-210 | P2 | 上櫃公司違反資訊申報、重大訊息及說明記者會規定專區 | `GET /mopsfin_t187ap23_O` |
| TPEx-211 | P3 | 電子式交易統計資訊(上櫃) | `GET /mopsfin_t187ap19_O` |
| TPEx-212 | 參考 | 興櫃股票市場現況 | `GET /tpex_esb_highlight` |
| TPEx-213 | P3 | 公債發行資料下載 | `GET /bond_ISSBD1_data` |
| TPEx-214 | P3 | 外國金融債發行資料下載 | `GET /bond_ISSBD2_data` |
| TPEx-215 | P3 | 金融債發行資料下載 | `GET /bond_ISSBD3_data` |
| TPEx-216 | P3 | 普通債發行資料下載 | `GET /bond_ISSBD4_data` |
| TPEx-217 | P3 | 轉(交)換債發行資料下載 | `GET /bond_ISSBD5_data` |
| TPEx-218 | P3 | 海外轉換債發行資料下載 | `GET /bond_ISSBD6_data` |
| TPEx-219 | P3 | 附認股權公司債發行資料下載 | `GET /bond_ISSBD7_data` |
| TPEx-220 | P3 | 海外附認股權公司債發行資料下載 | `GET /bond_ISSBD8_data` |
| TPEx-221 | P3 | 海外普通債發行資料下載 | `GET /bond_ISSBD9_data` |
| TPEx-222 | P3 | 國際債券(寶島債券)-本國發行人及第一、二上市(櫃)公司之外國發行人發行資料下載 | `GET /bond_ISSBD10_data` |
| TPEx-223 | P3 | 國際債券(寶島債券)-外國發行人(在我國未公開發行股權商品者)發行資料下載 | `GET /bond_ISSBD11_data` |
| TPEx-224 | P3 | 上櫃股票各券商總公司當日營業金額統計表 | `GET /tpex_daily_broker2` |
| TPEx-225 | P2 | 高殖利率指數歷史收盤指數 | `GET /tphd_index` |

## TPEx-001 · 上櫃股票市場現況

- **方法／URL**：[GET /tpex_mainborad_highlight](https://www.tpex.org.tw/openapi/v1/tpex_mainborad_highlight)
- **官方 tags**：上櫃
- **決策分類／優先序**：總體與跨市場／P1
- **可支持需求**：D18、D43
- **用途**：市場家數、漲跌廣度、成交量值與當前收市指數；非長歷史序列。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"ListedCompanyNumbers"` | string | 上櫃家數 |
| `"AuthorizedCapital"` | string | 總資本額 |
| `"MarketCapitalization"` | string | 總市值 |
| `"DailyTradingValue"` | string | 本日總成交值 |
| `"DailyTradingVolume"` | string | 本日總成交股數 |
| `"CloseIndex"` | string | 收市指數 |
| `"IndexChange"` | string | 指數漲跌 |
| `"PriceRiseCompanyNumbers"` | string | 上漲家數 |
| `"LimitUpCompanyNumbers"` | string | 漲停家數 |
| `"PriceDeclineCompanyNumbers"` | string | 下跌家數 |
| `"LimitDownCompanyNumbers"` | string | 跌停家數 |
| `"PriceFlatCompanyNumbers"` | string | 平盤家數 |
| `"UnmatchedCompanyNumbersSuspensionStocksIncluded"` | string | 未成交含暫停交易家數 |

## TPEx-002 · 上櫃股票現股當沖交易標的資訊

- **方法／URL**：[GET /tpex_securities](https://www.tpex.org.tw/openapi/v1/tpex_securities)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"資料日期"` | string | 資料日期 |
| `"證券代號"` | string | 證券代號 |
| `"證券名稱"` | string | 證券名稱 |
| `"暫停現股賣出後現款買進當沖註記"` | string | 暫停現股賣出後現款買進當沖註記 |

## TPEx-003 · 上櫃當日公布暫停/恢復交易股票

- **方法／URL**：[GET /tpex_spendi_today](https://www.tpex.org.tw/openapi/v1/tpex_spendi_today)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P0
- **可支持需求**：D11
- **用途**：暫停、恢復、變更交易及處置狀態檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"暫停交易"` | string | 暫停交易 |
| `"恢復交易"` | string | 恢復交易 |

## TPEx-004 · 上櫃歷史公布暫停/恢復交易股票

- **方法／URL**：[GET /tpex_spendi_history](https://www.tpex.org.tw/openapi/v1/tpex_spendi_history)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P0
- **可支持需求**：D11
- **用途**：暫停、恢復、變更交易及處置狀態檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Serial"` | string | 編號 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"DateOfSuspendedTrading"` | string | 暫停交易日期 |
| `"TimeOfSuspendedTrading"` | string | 暫停交易時間 |
| `"DateOfResumedTrading"` | string | 恢復交易日期 |
| `"TimeOfResumedTrading"` | string | 恢復交易時間 |

## TPEx-005 · 上櫃股票行情

- **方法／URL**：[GET /tpex_mainboard_daily_close_quotes](https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P0
- **可支持需求**：D04、D07、D09、D10、D31、D33、D34、D57
- **用途**：官方成交均價、日價量、估值及研究序列的原始輸入；先限定固定 150 檔宇宙中的上櫃股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。 多 Average／NextReferencePrice；Average 必須以成交金額／股數核對競賽公式；正式收盤時間前不採用未完成日資料。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"Close"` | string | 收盤 |
| `"Change"` | string | 漲跌 |
| `"Open"` | string | 開盤 |
| `"High"` | string | 最高 |
| `"Low"` | string | 最低 |
| `"Average"` | string | 均價 |
| `"TradingShares"` | string | 成交股數 |
| `"TransactionAmount"` | string | 成交金額 |
| `"TransactionNumber"` | string | 成交筆數 |
| `"LatestBidPrice"` | string | 最後買價 |
| `"LatesAskPrice"` | string | 最後賣價 |
| `"Capitals"` | string | 發行股數 |
| `"NextReferencePrice"` | string | 次日參考價 |
| `"NextLimitUp"` | string | 次日漲停價 |
| `"NextLimitDown"` | string | 次日跌停價 |

## TPEx-006 · 上櫃股票收盤行情

- **方法／URL**：[GET /tpex_mainboard_quotes](https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P0
- **可支持需求**：D04、D07、D09、D10、D31、D33、D34、D57
- **用途**：官方成交均價、日價量、估值及研究序列的原始輸入；先限定固定 150 檔宇宙中的上櫃股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；代表實測 HTTP 200
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。 與 daily_close_quotes 的標的範圍不同，含權證等；按150檔白名單過濾。

**代表探測證據**：`{"http_status": 200, "rows": 1011, "actual_shape": "list", "fetched_at": "2026-10-09T06:25:59.295946+00:00", "sha256": "32b36a57cb91934e099298c7b327c52e3182a53344b1be1aa820d49296eec384", "date_ranges": {"Date": ["1151008"]}, "observed_fields": ["Date", "SecuritiesCompanyCode", "CompanyName", "Close", "Change", "Open", "High", "Low", "TradingShares", "TransactionAmount", "TransactionNumber", "LatestBidPrice", "LatesAskPrice", "Capitals", "NextLimitUp", "NextLimitDown"]}`

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"Close"` | string | 收盤 |
| `"Change"` | string | 漲跌 |
| `"Open"` | string | 開盤 |
| `"High"` | string | 最高 |
| `"Low"` | string | 最低 |
| `"TradingShares"` | string | 成交股數 |
| `"TransactionAmount"` | string | 成交金額 |
| `"TransactionNumber"` | string | 成交筆數 |
| `"LatestBidPrice"` | string | 最後買價 |
| `"LatesAskPrice"` | string | 最後賣價 |
| `"Capitals"` | string | 發行股數 |
| `"NextLimitUp"` | string | 次日漲停價 |
| `"NextLimitDown"` | string | 次日跌停價 |

## TPEx-007 · 上櫃股票個股本益比、殖利率、股價淨值比

- **方法／URL**：[GET /tpex_mainboard_peratio_analysis](https://www.tpex.org.tw/openapi/v1/tpex_mainboard_peratio_analysis)
- **官方 tags**：上櫃
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D23
- **用途**：估值比較與殖利率，核對盈餘分母、年度及不適用值。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 名稱 |
| `"PriceEarningRatio"` | string | 本益比 |
| `"DividendPerShare"` | string | 每股股利 |
| `"YieldRatio"` | string | 殖利率 |
| `"PriceBookRatio"` | string | 股價淨值比 |

## TPEx-008 · 上櫃股票融資融券餘額

- **方法／URL**：[GET /tpex_mainboard_margin_balance](https://www.tpex.org.tw/openapi/v1/tpex_mainboard_margin_balance)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"MarginPurchaseBalancePreviousDay"` | string | 前資餘額 |
| `"MarginPurchase"` | string | 資買 |
| `"MarginSales"` | string | 資賣 |
| `"CashRedemption"` | string | 現償 |
| `"MarginPurchaseBalance"` | string | 資餘額 |
| `"MarginPurchaseBalanceBelongSecuritiesFinanceEnterprise"` | string | 資屬證金 |
| `"MarginPurchaseUtilizationRate"` | string | 資使用率 |
| `"MarginPurchaseQuota"` | string | 資限額 |
| `"ShortSaleBalancePreviousDay"` | string | 前券餘額 |
| `"ShortSale"` | string | 券賣 |
| `"ShortConvering"` | string | 券買 |
| `"StockRedemption"` | string | 券償 |
| `"ShortSaleBalance"` | string | 券餘額 |
| `"ShortSaleBalanceBelongSecuritiesFinanceEnterprise"` | string | 券屬證金 |
| `"ShortSaleUtilizationRate"` | string | 券使用率 |
| `"ShortSaleQuota"` | string | 券限額 |
| `"Offsetting"` | string | 資券相抵 |
| `"Note"` | string | 備註 |

## TPEx-009 · 櫃買指數歷史資料

- **方法／URL**：[GET /tpex_index](https://www.tpex.org.tw/openapi/v1/tpex_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P1
- **可支持需求**：D18、D31、D32、D43、D56
- **用途**：櫃買市場與總報酬基準，估 Beta、相對強弱與績效歸因。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；代表實測 HTTP 200
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

**代表探測證據**：`{"http_status": 200, "rows": 6, "actual_shape": "list", "fetched_at": "2026-10-09T06:25:59.641774+00:00", "sha256": "60efcd179cb7097141950d5efc4a304849d68bf3e8db6addfe8848f794f4b622", "date_ranges": {"Date": ["20261001", "20261002", "20261005", "20261006", "20261007", "20261008"]}, "observed_fields": ["Date", "Open", "High", "Low", "Close", "Change"]}`

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Open"` | string | 開市 |
| `"High"` | string | 最高 |
| `"Low"` | string | 最低 |
| `"Close"` | string | 收市 |
| `"Change"` | string | 漲跌 |

## TPEx-010 · 富櫃50指數歷史收盤指數

- **方法／URL**：[GET /tpex50_index](https://www.tpex.org.tw/openapi/v1/tpex50_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"TPEx50Index"` | string | 櫃買富櫃五十指數 |
| `"TPEx50TotalReturnIndex"` | string | 櫃買富櫃五十報酬指數 |

## TPEx-011 · 上櫃股票現股當沖交易統計資訊

- **方法／URL**：[GET /tpex_intraday_trading_statistics](https://www.tpex.org.tw/openapi/v1/tpex_intraday_trading_statistics)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"DayTradingVolume"` | string | 當日沖銷交易總成交股數 |
| `"DayTradingVolumeOfTheMarket"` | string | 當日沖銷交易總成交股數占市場比重 |
| `"DayTradingValueOfBuys"` | string | 當日沖銷交易總買進成交金額 |
| `"DayTradingValueOfBuyOfTheMarket"` | string | 當日沖銷交易總買進成交金額占市場比重 |
| `"DayTradingValueOfSells"` | string | 當日沖銷交易總賣出成交金額 |
| `"DayTradingValueOfSellsOfTheMarket"` | string | 當日沖銷交易總賣出成交金額占市場比重 |

## TPEx-012 · 上櫃股票熱門股證券商進出排行

- **方法／URL**：[GET /tpex_active_broker_volume](https://www.tpex.org.tw/openapi/v1/tpex_active_broker_volume)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P3
- **可支持需求**：D30
- **用途**：熱門股券商進出排行，作為可延後的部分分點代理資料。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。 熱門排行不是全部個股完整分點流，也不識別最終受益人。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"StockRanking"` | string | 股票排行 |
| `"SecuritiesCompanyCodeAndCompanyName"` | string | 股票名稱及代號 |
| `"SecuritiesFirmsRanking"` | string | 證商排行 |
| `"SecuritiesFirmsCode"` | string | 證商名稱 |
| `"TotalPurchaseShares"` | string | 總買量 |
| `"TotalSellShares"` | string | 總賣量 |

## TPEx-013 · 上櫃股票融券借券賣出餘額

- **方法／URL**：[GET /tpex_margin_sbl](https://www.tpex.org.tw/openapi/v1/tpex_margin_sbl)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"SaleBalancePreviousDay"` | string | 融券前日餘額 |
| `"SaleSell"` | string | 融券賣出 |
| `"SaleBuy"` | string | 融券買進 |
| `"SaleSpotSecurities"` | string | 融券現券 |
| `"SaleBalanceOfTheMarketDay"` | string | 融券當日餘額 |
| `"SaleAvailableVolumes"` | string | 融券限額 |
| `"SecuritiesBorrowingBalancePreviousDay"` | string | 借券賣出前日餘額 |
| `"SecuritiesBorrowingSale"` | string | 借券賣出當日賣出 |
| `"SecuritiesBorrowingReturn"` | string | 借券賣出當日還券 |
| `"SecuritiesBorrowingAdjustment"` | string | 借券賣出當日調整數額 |
| `"SecuritiesBorrowingBalanceOfTheMarketDay"` | string | 借券賣出當日餘額 |
| `"AvailableVolumesForSBLShortSale"` | string | 次一營業日可借券賣出限額 |
| `"Note"` | string | 備註 |

## TPEx-014 · 上櫃股票除權除息計算結果表

- **方法／URL**：[GET /tpex_exright_daily](https://www.tpex.org.tw/openapi/v1/tpex_exright_daily)
- **官方 tags**：上櫃
- **決策分類／優先序**：競賽與交易狀態／P0
- **可支持需求**：D05、D08、D39
- **用途**：除權息與公司行動預告、計算結果，對照競賽權益帳；公告中的理論值不能直接取代官方結算。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 除權息日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"ClosePriceBeforeExRightsDiviend"` | string | 除權息前收盤價 |
| `"ExRightsDiviendQuote"` | string | 除權息參考價 |
| `"StockDividend"` | string | 權值 |
| `"CashDividend"` | string | 息值 |
| `"StockDividendPlusCashDividend"` | string | 權值加息值 |
| `"ExRightsDiviend"` | string | 權或息 |
| `"LimitUp"` | string | 漲停價 |
| `"LimitDown"` | string | 跌停價 |
| `"OpeningReferencePrice"` | string | 開始交易基準價 |
| `"DividendDeductedQuote"` | string | 減除股利參考價 |
| `"CashDivdend"` | string | 現金股利 |
| `"StockDivdendThousandShares"` | string | 每仟股無償配股 |
| `"CashCapitalIncreaseShares"` | string | 現金增資股數 |
| `"SubscriptionPricePerShare"` | string | 現金增資認購價 |
| `"AllocatedForPublicUnderwriting"` | string | 公開承銷股數 |
| `"SubscribedByEmployees"` | string | 員工認購股數 |
| `"SubscribedByExistingShareholders"` | string | 原股東認購股數 |
| `"SubscribedProRataThousandShares"` | string | 按持股比例仟股認購 |

## TPEx-015 · 上櫃股票除權除息預告表

- **方法／URL**：[GET /tpex_exright_prepost](https://www.tpex.org.tw/openapi/v1/tpex_exright_prepost)
- **官方 tags**：上櫃
- **決策分類／優先序**：競賽與交易狀態／P0
- **可支持需求**：D05、D08、D39
- **用途**：除權息與公司行動預告、計算結果，對照競賽權益帳；公告中的理論值不能直接取代官方結算。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"ExRrightsExDividendDate"` | string | 除權息日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 名稱 |
| `"ExRrightsExDividend"` | string | 除權息 |
| `"StockDividendRatio"` | string | 無償配股率 |
| `"SubscriptionRatioToNewSharesIssued"` | string | 現金增資配股率 |
| `"SubscriptionPricePerShare"` | string | 現金增資認購價 |
| `"CashDividend"` | string | 現金股利 |
| `"AllocatedForPublicUnderwriting"` | string | 公開承銷股數 |
| `"SubscribedByEmployees"` | string | 員工認購股數 |
| `"SubscribedByExistingShareholders"` | string | 原股東認購股數 |
| `"SubscribedProRataInThousandShares"` | string | 按持股比例仟股認購 |

## TPEx-016 · 上櫃股票變更交易、分盤交易、管理股票與停止交易資訊

- **方法／URL**：[GET /tpex_cmode](https://www.tpex.org.tw/openapi/v1/tpex_cmode)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P0
- **可支持需求**：D11
- **用途**：暫停、恢復、變更交易及處置狀態檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"AlteredTrading"` | string | 變更交易 |
| `"PeriodicTrading"` | string | 分盤交易 |
| `"ManagedStock"` | string | 管理股票 |
| `"MatchingFrequency"` | string | 分盤或管理股票撮合循環時間 |
| `"SuspensionOfTrading"` | string | 停止交易 |
| `" FinancialAnnouncements"` | string | 財務重點專區 |

## TPEx-017 · 上櫃股票零股交易資訊

- **方法／URL**：[GET /tpex_odd_stock](https://www.tpex.org.tw/openapi/v1/tpex_odd_stock)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"TradeVolume"` | string | 成交股數 |
| `"NumberOfTransactions"` | string | 成交筆數 |
| `"TradeAmount"` | string | 成交金額 |
| `"Price"` | string | 成交價格 |
| `"LastBestBidPrice"` | string | 未成交買價 |
| `"LastBestBidVolume"` | string | 未成交買量 |
| `"LastBestAskPrice"` | string | 未成交賣價 |
| `"LastBestAskVolume"` | string | 未成交賣量 |

## TPEx-018 · 上櫃股票盤後定價行情

- **方法／URL**：[GET /tpex_off_market](https://www.tpex.org.tw/openapi/v1/tpex_off_market)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"BidTransactions"` | string | 委買筆數 |
| `"BidVolume"` | string | 委買張數 |
| `"OfferTransactions"` | string | 委賣筆數 |
| `"AskVolume"` | string | 委賣張數 |
| `"Close"` | string | 成交價 |
| `"Transactions"` | string | 成交筆數 |
| `"TradeVolume"` | string | 成交張數 |
| `"TradeAmount"` | string | 成交金額 |
| `"BidVolumeUnexecute"` | string | 委買未成交張數 |
| `"OfferVolumeUnexecute"` | string | 委賣未成交張數 |

## TPEx-019 · 申請上櫃公司

- **方法／URL**：[GET /tpex_esb_applicant_companies](https://www.tpex.org.tw/openapi/v1/tpex_esb_applicant_companies)
- **官方 tags**：上櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 申請日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"Chairman"` | string | 董事長 |
| `"CapitalWhileApplying"` | string | 申請時股本 |
| `"TPExListingScreeningCommitteeDate"` | string | 上櫃審議委員會審議日期 |
| `"TPExSanctionedDate"` | string | 櫃買董事會通過上櫃日期 |
| `"TPExApprovedTradingDate"` | string | 櫃買同意上櫃契約日期或證期局核准上櫃契約日期 |
| `"ListingDate"` | string | 股票上櫃買賣日期 |
| `"LeadUnderwriter"` | string | 主辦承銷商 |
| `"OfferingPrice"` | string | 承銷價 |
| `"Note"` | string | 備註 |

## TPEx-020 · 上櫃公布注意股票資訊

- **方法／URL**：[GET /tpex_trading_warning_information](https://www.tpex.org.tw/openapi/v1/tpex_trading_warning_information)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 公告日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"TradingInformation"` | string | 注意交易資訊 |
| `"ClosePrice"` | string | 收盤價 |
| `"PriceEarningRatio"` | string | 本益比 |

## TPEx-021 · 上櫃處置有價證券資訊

- **方法／URL**：[GET /tpex_disposal_information](https://www.tpex.org.tw/openapi/v1/tpex_disposal_information)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P0
- **可支持需求**：D11
- **用途**：暫停、恢復、變更交易及處置狀態檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 公布日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"DispositionPeriod"` | string | 處置起訖時間 |
| `"DispositionReasons"` | string | 處置原因 |
| `"DisposalCondition"` | string | 處置內容 |

## TPEx-022 · 上櫃公布注意累計次數異常資訊

- **方法／URL**：[GET /tpex_trading_warning_note](https://www.tpex.org.tw/openapi/v1/tpex_trading_warning_note)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"AccumulationSituation"` | string | 近期達本公司「公布注意交易資訊」標準之情形 |

## TPEx-023 · 上櫃融資融券暫停融券賣出預告表

- **方法／URL**：[GET /tpex_margin_trading_term](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_term)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"ShortSaleSuspensionStartDate"` | string | 停券起日(最後回補日) |
| `"ShortSaleSuspensionEndDate"` | string | 停券迄日 |
| `"Reason"` | string | 原因 |

## TPEx-024 · 上櫃融資融券調整成數

- **方法／URL**：[GET /tpex_margin_trading_adjust](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_adjust)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"ReductionDate"` | string | 降成日 |
| `"TradeResumptionDate"` | string | 恢復日 |
| `"ReasonExcessiveStockPriceVolatilityFiveConsecutiveDays"` | string | 原因股價波動過度劇烈連續五日 |
| `"ReasonExcessiveStockPriceVolatilitySixDaysOutOfTen"` | string | 原因股價波動過度劇烈十日內有六日 |
| `"ReasonAbnormalTradeVolumeConsecutiveDays"` | string | 原因成交量過度異常連續五日 |
| `"ReasonAbnormalTradeVolumeSixDaysOutOfTen"` | string | 原因成交量過度異常十日內有六日 |
| `"ReasonShareholdingOverconcentration"` | string | 原因股權過度集中 |
| `"ReasonSecondDispositionByMarketSurveillanceDepartment"` | string | 原因監視第二次處置 |
| `"ReasonUponResolutionByTheSurveillanceOperationsOversightCommittee"` | string | 原因監視業務督導會報決議 |

## TPEx-025 · 上櫃融資融券標借

- **方法／URL**：[GET /tpex_margin_trading_lend](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_lend)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"DateOfTheCompetitiveDids"` | string | 標借日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"SecuritiesFinanceEnterprise"` | string | 證金公司 |
| `"TheVolumeOfTheCompetitiveDids"` | number | 標借張數 |
| `"TheHighestAcceptableRate"` | number | 最高標借單價 |
| `"TheVolumeOfTheWinningBids"` | number | 得標張數 |
| `"LendingRates"` | number | 標定單價 |
| `"Shortfall"` | string | 不足張數 |

## TPEx-026 · 上櫃信用交易餘額概況表

- **方法／URL**：[GET /tpex_margin_trading_marginspot](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_marginspot)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Month"` | string | 資料月份 |
| `"Ranking"` | string | 排名 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"MonthlyAverageMarginPurchaseBalance"` | string | 月均融資餘額 |
| `"MarketShare"` | string | 市場佔有率 |
| `"MonthlyAverageShortSaleBalance"` | string | 月均融券餘額 |
| `"MonthlyAverageMarginTradingBalance"` | string | 月均融資融券餘額 |

## TPEx-027 · 上櫃平盤下得融(借)券賣出之證券名單

- **方法／URL**：[GET /tpex_margin_trading_margin_mark](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_margin_mark)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `"BannedFromMarginShortSelling"` | string | 暫停融券賣出 |
| `"BannedFromSBLShortSelling"` | string | 暫停借券賣出 |
| `"SubjectToUptickRule"` | string | 前一交易日收盤價跌停本日禁止平盤下融借券賣出 |

## TPEx-028 · 上櫃融資融券使用率報表

- **方法／URL**：[GET /tpex_margin_trading_margin_used](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_margin_used)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"UsageRatio"` | string | 使用率 |

## TPEx-029 · 上櫃融資融券增減排行表

- **方法／URL**：[GET /tpex_margin_trading_short_sell](https://www.tpex.org.tw/openapi/v1/tpex_margin_trading_short_sell)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"PreviousBalance"` | string | 前日餘額 |
| `"CurrentBalance"` | string | 本日餘額 |
| `"Used"` | string | 使用張數 |

## TPEx-030 · 上櫃僑外資及陸資持股比例排行表

- **方法／URL**：[GET /tpex_3insti_qfii](https://www.tpex.org.tw/openapi/v1/tpex_3insti_qfii)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D25、D26
- **用途**：法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"NumberOfSharesIssued"` | string | 發行股數 |
| `"AvailableSharesForOC/FIToInvest"` | string | 僑外資及陸資尚可投資股數 |
| `"CurrentlySharesOC/FIHeld"` | string | 僑外資及陸資持有股數 |
| `"PercentageOfAvailableInvestmentForOC/FI"` | string | 僑外資及陸資尚可投資比率 |
| `"PercentageOfSharesOC/FMIHeld"` | string | 僑外資及陸資持股比率 |
| `"UpperLimitOfRegulatedInvestment"` | string | 法令投資上限比率 |
| `"Note"` | string | 備註 |

## TPEx-031 · 上櫃各類股僑外資及陸資持股比例表

- **方法／URL**：[GET /tpex_3insti_qfii_industry](https://www.tpex.org.tw/openapi/v1/tpex_3insti_qfii_industry)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D25、D26
- **用途**：法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Industry"` | string | 類股 |
| `"NumberOfCompanies"` | string | 家數 |
| `"NumberOfSharesIssued"` | string | 總發行股數 |
| `"CurrentlySharesOC/FIHeld"` | string | 僑外資及陸資持有總股數 |
| `"PercentageOfSharesOC/FMIHeld"` | string | 僑外資及陸資持股比率 |

## TPEx-032 · 上櫃股票三大法人買賣明細資訊

- **方法／URL**：[GET /tpex_3insti_daily_trading](https://www.tpex.org.tw/openapi/v1/tpex_3insti_daily_trading)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P1
- **可支持需求**：D25
- **用途**：三大法人逐股買賣股數與淨額；區分自營商自行買賣及避險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；代表實測 HTTP 200
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。 實測同樣只有此規格的20欄；避險買進等完整拆分不足，不得由缺欄推造值。含前導空白鍵，需明確映射。

**代表探測證據**：`{"http_status": 200, "rows": 892, "actual_shape": "list", "fetched_at": "2026-10-09T06:30:46.290563+00:00", "sha256": "8325f809040c52e07e45634c4608d5e7e71e92616213d77b790ca6cde69e0b5c", "date_ranges": {}, "observed_fields": ["Date", "SecuritiesCompanyCode", "CompanyName", "Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Total Buy", " Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Total Sell", "Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Difference", "Foreign Dealers-Total Buy", "Foreign Dealers-TotalSell", "ForeignDealers-Difference", "ForeignInvestorsIncludeMainlandAreaInvestors-TotalBuy", "ForeignInvestorsIncludeMainlandAreaInvestors-TotalSell", "ForeignInvestorsInclude MainlandAreaInvestors-Difference", "SecuritiesInvestmentTrustCompanies-TotalBuy", "SecuritiesInvestmentTrustCompanies-TotalSell", "SecuritiesInvestmentTrustCompanies-Difference", "Dealers-TotalBuy", "Dealers-TotalSell", "Dealers-Difference", "Dealers -TotalSell", "TotalDifference"]}`

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Total Buy"` | string | 外資及陸資不含外資自營商買進股數 |
| `" Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Total Sell"` | string | 外資及陸資不含外資自營商賣出股數 |
| `"Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Difference"` | string | 外資及陸資不含外資自營商買賣超股數 |
| `"Foreign Dealers-Total Buy"` | string | 外資自營商買進股數 |
| `"Foreign Dealers-TotalSell"` | string | 外資自營商賣出股數 |
| `"ForeignDealers-Difference"` | string | 外資自營商買賣超股數 |
| `"ForeignInvestorsIncludeMainlandAreaInvestors-TotalBuy"` | string | 外資及陸資買進股數 |
| `"ForeignInvestorsIncludeMainlandAreaInvestors-TotalSell"` | string | 外資及陸資賣出股數 |
| `"ForeignInvestorsInclude MainlandAreaInvestors-Difference"` | string | 外資及陸資買賣超股數 |
| `"SecuritiesInvestmentTrustCompanies-TotalBuy"` | string | 投信買進股數 |
| `"SecuritiesInvestmentTrustCompanies-TotalSell"` | string | 投信賣出股數 |
| `"SecuritiesInvestmentTrustCompanies-Difference"` | string | 投信買賣超股數 |
| `"Dealers-TotalBuy"` | string | 自營商買進股數 |
| `"Dealers-TotalSell"` | string | 自營商賣出股數 |
| `"Dealers-Difference"` | string | 自營商買賣超股數 |
| `"Dealers -TotalSell"` | string | 自營商避險賣出股數 |
| `"TotalDifference"` | string | 三大法人買賣超股數合計 |

## TPEx-033 · 上櫃股票自營商買賣超彙總表

- **方法／URL**：[GET /tpex_3insti_dealer_trading](https://www.tpex.org.tw/openapi/v1/tpex_3insti_dealer_trading)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D25、D26
- **用途**：法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"Buy"` | string | 避險買進金額 |
| `"Sell"` | string | 避險賣出金額 |
| `"NetBuySell"` | string | 避險買賣超 |
| `"NetBuy"` | string | 買賣超 |

## TPEx-034 · 上櫃漲跌停未成交資訊

- **方法／URL**：[GET /tpex_ceil_non_trading](https://www.tpex.org.tw/openapi/v1/tpex_ceil_non_trading)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 名稱 |
| `"ClosingPrice"` | string | 收盤價 |
| `"Change"` | string | 漲跌 |
| `"Tot.Trans.Vol."` | string | 總成交張數 |
| `"Trans.Vol.AtUp-limitPr."` | string | 漲跌停成交張數 |
| `"OrderVol.AtUp-limitPr."` | string | 漲跌停委託張數 |
| `"Difference"` | string | 漲跌停未成交張數 |

## TPEx-035 · 上櫃日成交量值指數

- **方法／URL**：[GET /tpex_daily_trading_index](https://www.tpex.org.tw/openapi/v1/tpex_daily_trading_index)
- **官方 tags**：上櫃
- **決策分類／優先序**：總體與跨市場／P1
- **可支持需求**：D18、D31、D32、D43、D56
- **用途**：櫃買市場與總報酬基準，估 Beta、相對強弱與績效歸因。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 交易日期 |
| `"TradeVolume"` | string | 成交股數 |
| `"TradeAmount"` | string | 成交金額 |
| `"NumberOfTransactions"` | string | 筆數 |
| `"TPExIndex"` | string | 櫃買指數 |
| `"Change"` | string | 漲跌 |

## TPEx-036 · 上櫃當日融券賣出與借券賣出成交量值

- **方法／URL**：[GET /tpex_short_sell](https://www.tpex.org.tw/openapi/v1/tpex_short_sell)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D28
- **用途**：融資融券、借券賣出與使用率，作擁擠及潛在賣壓特徵；競賽仍禁止融資、放空。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"ShortSaleVolume"` | string | 融券賣出成交張數 |
| `"ShortSaleAmount"` | string | 融券賣出成交金額 |
| `"SBLVolume"` | string | 借券賣出成交張數 |
| `"SBLAmount"` | string | 借券賣出成交金額 |

## TPEx-037 · 上櫃各券商當日營業金額統計表

- **方法／URL**：[GET /tpex_daily_broker1](https://www.tpex.org.tw/openapi/v1/tpex_daily_broker1)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Ranking"` | string | 排名 |
| `"PreviousDayRanking"` | string | 前日排名 |
| `"Code"` | string | 券商 |
| `"Name"` | string | 名稱 |
| `"TradingAmount"` | string | 成交金額 |
| `"DayClosingRatio"` | string | 日成交比率 |
| `"CurrentMonthRanking"` | string | 本月排名 |
| `"CurrentMonthCumulativeAmount"` | string | 本月累計金額 |
| `"CurrentMonthClosingRatio"` | string | 本月成交比率 |

## TPEx-038 · 上櫃盤中個股成交金額排行

- **方法／URL**：[GET /tpex_active_dollar_volume](https://www.tpex.org.tw/openapi/v1/tpex_active_dollar_volume)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"NumberOfThousandSharesTraded"` | string | 成交仟股數 |
| `"TradeAmount"` | string | 成交值 |

## TPEx-039 · 上櫃盤中個股漲幅排行

- **方法／URL**：[GET /tpex_active_advanced](https://www.tpex.org.tw/openapi/v1/tpex_active_advanced)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"ClosingPrice"` | string | 收盤價 |
| `"Up"` | string | 上漲金額 |
| `"UpRatio"` | string | 漲幅百分比 |

## TPEx-040 · 上櫃盤中個股跌幅排行

- **方法／URL**：[GET /tpex_active_declined](https://www.tpex.org.tw/openapi/v1/tpex_active_declined)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代碼 |
| `"CompanyName"` | string | 名稱 |
| `"ClosingPrice"` | string | 收盤價 |
| `"Down"` | string | 下跌金額 |
| `"DownRatio"` | string | 跌幅百分比 |

## TPEx-041 · 上櫃應付現股當日沖銷券差借券費率

- **方法／URL**：[GET /tpex_intraday_fee](https://www.tpex.org.tw/openapi/v1/tpex_intraday_fee)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 券差日期 |
| `"SecuritiesCompanyCode"` | string | 證券代號 |
| `"CompanyName"` | string | 證券名稱 |
| `" LendingVolume"` | string | 借券股數 |
| `"LendingFee"` | string | 借券費率 |

## TPEx-042 · 上櫃暫停先賣後買當日沖銷交易標的預告表

- **方法／URL**：[GET /tpex_intraday_trading_pre](https://www.tpex.org.tw/openapi/v1/tpex_intraday_trading_pre)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"FirstDayToSuspendSellThenBuy"` | string | 停止先賣後買開始日 |
| `"DayOfReinstatingSellThenBuy"` | string | 恢復先賣後買日 |
| `"Reason"` | string | 原因 |

## TPEx-043 · 上櫃暫停先賣後買當日沖銷交易歷史查詢

- **方法／URL**：[GET /tpex_intraday_trading_his](https://www.tpex.org.tw/openapi/v1/tpex_intraday_trading_his)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"FirstDayToSuspendSellThenBuy"` | string | 停止先賣後買開始日 |
| `"LastDayToSuspendSellThenBuy"` | string | 停止先賣後買結束日 |
| `"Reason"` | string | 原因 |

## TPEx-044 · 上櫃歷史個股市值排行

- **方法／URL**：[GET /tpex_daily_market_value](https://www.tpex.org.tw/openapi/v1/tpex_daily_market_value)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D09
- **用途**：發行股數、收盤價與市值排名；規模與流通分析的部分原料。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"Capitals"` | string | 發行股數 |
| `"ClosePrice"` | string | 收盤價 |
| `"MarketValue"` | string | 市值 |

## TPEx-045 · 上櫃歷史個股週轉率排行

- **方法／URL**：[GET /tpex_daily_turnover](https://www.tpex.org.tw/openapi/v1/tpex_daily_turnover)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"TradingShares"` | string | 總成交股數 |
| `"Capitalization"` | string | 發行股數 |
| `"TurnoverRatio"` | string | 週轉率 |

## TPEx-046 · 上櫃歷史個股日均量排行

- **方法／URL**：[GET /tpex_trading_volumes_avg](https://www.tpex.org.tw/openapi/v1/tpex_trading_volumes_avg)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"AverageDailyTradingVolume"` | string | 日均張數 |

## TPEx-047 · 上櫃歷史個股日均值排行

- **方法／URL**：[GET /tpex_trading_amount_avg](https://www.tpex.org.tw/openapi/v1/tpex_trading_amount_avg)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"StockCode"` | string | 股票代號 |
| `"StockName"` | string | 股票名稱 |
| `"AverageDailyTradingAmount"` | string | 日均值 |

## TPEx-048 · 上櫃歷史類股成交價量比重

- **方法／URL**：[GET /tpex_trading_volume_ratio](https://www.tpex.org.tw/openapi/v1/tpex_trading_volume_ratio)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Sector"` | string | 類股名稱 |
| `"TradeAmount"` | string | 成交金額 |
| `"TradeWeight"` | string | 成交比重 |
| `" NumberOfSharesTraded"` | string | 成交股數 |

## TPEx-049 · 上櫃歷史個股本益比排行

- **方法／URL**：[GET /tpex_pe_ratio_top10](https://www.tpex.org.tw/openapi/v1/tpex_pe_ratio_top10)
- **官方 tags**：上櫃
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D23
- **用途**：本益比排行的部分估值觀測；全體股票估值優先用 peratio_analysis。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"ClosePrice"` | string | 收盤價 |
| `"EarningsPerShare"` | string | 每股盈餘 |
| `"P/ERatio"` | string | 本益比 |

## TPEx-050 · 上櫃鉅額交易日成交資訊

- **方法／URL**：[GET /tpex_daily_qutoes_block](https://www.tpex.org.tw/openapi/v1/tpex_daily_qutoes_block)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"TransactionType"` | string | 交易型態 |
| `"SettlementPeriod"` | string | 交割期別 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"TradePrice"` | string | 成交價格 |
| `"NumberOfSharesTraded"` | string | 成交股數 |
| `"TradeValue"` | string | 成交值 |
| `"TradingTime"` | string | 成交時間 |

## TPEx-051 · 上櫃個股單一證券鉅額交易日成交資訊

- **方法／URL**：[GET /tpex_daily_trading_block](https://www.tpex.org.tw/openapi/v1/tpex_daily_trading_block)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"TradingDate"` | string | 成交日期 |
| `"Name"` | string | 名稱 |
| `"NumberOfSharesTraded"` | string | 成交股數 |
| `"TradingValue"` | string | 成交金額 |
| `"HighestPrice"` | string | 最高價 |
| `"LowestPrice"` | string | 最低價 |
| `"WeightedAveragePrice"` | string | 加權平均價 |
| `"NumberOfTransactions"` | string | 成交筆數 |
| `"TransactionType"` | string | 交易型態 |
| `"SettlementPeriod"` | string | 交割期別 |

## TPEx-052 · 上櫃鉅額交易日成交量值統計

- **方法／URL**：[GET /tpex_daily_trading_summary_odd](https://www.tpex.org.tw/openapi/v1/tpex_daily_trading_summary_odd)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"TradingDate"` | string | 成交日期 |
| `"Type"` | string | 類別 |
| `"NumberOfTransactions"` | string | 成交筆數 |
| `"NumberOfSharesTraded"` | string | 成交股數 |
| `"MarketShare"` | string | 成交股數占全市場比重 |
| `"TradeValue"` | string | 成交金額 |
| `"Market Share"` | string | 成交金額占全市場比重 |

## TPEx-053 · 上櫃鉅額交易月成交量值統計

- **方法／URL**：[GET /tpex_monthly_trading_summary_block](https://www.tpex.org.tw/openapi/v1/tpex_monthly_trading_summary_block)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Month"` | string | 成交月份 |
| `"Type"` | string | 類別 |
| `"NumberOfTransactions"` | string | 成交筆數 |
| `"NumberOfSharesTraded"` | string | 成交股數 |
| `"MarketShare"` | string | 成交金額占全市場比重 |
| `"TradeValue"` | string | 成交金額 |

## TPEx-054 · 上櫃鉅額交易年成交量值統計

- **方法／URL**：[GET /tpex_yearly_trading_summary_block](https://www.tpex.org.tw/openapi/v1/tpex_yearly_trading_summary_block)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Year"` | string | 成交年度 |
| `"Type"` | string | 類別 |
| `"NumberOfTransactions"` | string | 成交筆數 |
| `"NumberOfSharesTraded"` | string | 成交股數 |
| `"MarketShare"` | string | 成交金額占全市場比重 |
| `"TradeValue"` | string | 成交金額 |

## TPEx-055 · 上櫃歷史個股成交量排行

- **方法／URL**：[GET /tpex_volume_rank](https://www.tpex.org.tw/openapi/v1/tpex_volume_rank)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"TradingVolume"` | string | 成交張數 |

## TPEx-056 · 上櫃歷史個股成交值排行

- **方法／URL**：[GET /tpex_amount_rank](https://www.tpex.org.tw/openapi/v1/tpex_amount_rank)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"TradingAmount"` | string | 成交值 |

## TPEx-057 · 上櫃股票等價系統成交分價表

- **方法／URL**：[GET /tpex_prvol](https://www.tpex.org.tw/openapi/v1/tpex_prvol)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyNam"` | string | 名稱 |
| `"TradingPrice"` | string | 成交價 |
| `"PriceNote"` | string | 價格註記 |
| `"NumberOfSharesTraded"` | string | 成交張數 |

## TPEx-058 · 上櫃股票三大法人買賣金額彙總表

- **方法／URL**：[GET /tpex_3insti_summary](https://www.tpex.org.tw/openapi/v1/tpex_3insti_summary)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D25、D26
- **用途**：法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Investor"` | string | 單位名稱 |
| `"PurchaseAmount"` | string | 買進金額 |
| `"SaleAmount"` | string | 賣出金額 |
| `"Net"` | string | 買賣超 |

## TPEx-059 · 上櫃股票投信買賣超彙總表

- **方法／URL**：[GET /tpex_3insti_trading](https://www.tpex.org.tw/openapi/v1/tpex_3insti_trading)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D25、D26
- **用途**：法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"Buy"` | string | 買進 |
| `"Sell"` | string | 賣出 |
| `"NetBuy"` | string | 買賣超 |

## TPEx-060 · 鉅額交易歷史成交資訊

- **方法／URL**：[GET /tpex_daily_trade_block_day](https://www.tpex.org.tw/openapi/v1/tpex_daily_trade_block_day)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"TradingDate"` | string | 成交日期 |
| `"Name"` | string | 名稱 |
| `"NumberOfSharesTraded"` | string | 成交股數 |
| `"TradingValue"` | string | 成交金額 |
| `"HighestPrice"` | string | 最高價 |
| `"LowestPrice"` | string | 最低價 |
| `"WeightedAveragePrice"` | string | 加權平均價 |
| `"NumberOfTransactions"` | string | 成交筆數 |
| `"TransactionType"` | string | 交易型態 |
| `"SettlementPeriod"` | string | 交割期別 |

## TPEx-061 · 上櫃每日暫緩開盤股票

- **方法／URL**：[GET /tpex_delayed_stock_open](https://www.tpex.org.tw/openapi/v1/tpex_delayed_stock_open)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 交易日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-062 · 上櫃每日暫緩收盤股票

- **方法／URL**：[GET /tpex_delayed_stock_close](https://www.tpex.org.tw/openapi/v1/tpex_delayed_stock_close)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 交易日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-063 · 上櫃首五日無漲跌幅資訊

- **方法／URL**：[GET /tpex_ipo_no_limit](https://www.tpex.org.tw/openapi/v1/tpex_ipo_no_limit)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P2
- **可支持需求**：D10、D11、D16、D18
- **用途**：行情、交易風險、成交活躍度及流動性輔助檢查。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"StartDateForStabilizationOperation"` | string | 穩定操作起始日 |
| `"EndDateForStabilizationOperation"` | string | 穩定操作截止日 |
| `"UnderwritingPrice"` | string | 承銷價格 |
| `"OverAllotmentShares"` | string | 過額配售數量 |
| `"TransactionType"` | string | 專戶種類 |
| `"Underwriter"` | string | 承銷商名稱 |
| `"TradingType"` | string | 買賣別 |
| `"TradingPrice"` | string | 成交價格 |
| `"TradingVolume"` | string | 成交數量 |
| `"CurrentDayCumulativeTradingVolume"` | string | 當日累計成交數量 |

## TPEx-064 · 本國興櫃公司EPS排名

- **方法／URL**：[GET /tpex_esb_eps_rank](https://www.tpex.org.tw/openapi/v1/tpex_esb_eps_rank)
- **官方 tags**：公司治理
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排名 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"EPS"` | string | EPS |

## TPEx-065 · 興櫃公司資本額排名

- **方法／URL**：[GET /tpex_esb_capitals_rank](https://www.tpex.org.tw/openapi/v1/tpex_esb_capitals_rank)
- **官方 tags**：公司治理
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排名 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"Capital"` | string | 資本額百萬元 |

## TPEx-066 · 櫃買「富櫃200指數」當日收盤指數

- **方法／URL**：[GET /tpex200_change](https://www.tpex.org.tw/openapi/v1/tpex200_change)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"資料日期"` | string | 資料日期 |
| `"指數"` | string | 指數 |
| `"收盤指數"` | string | 收盤指數 |
| `"漲跌"` | string | 漲跌 |
| `"漲跌點數"` | string | 漲跌點數 |
| `"漲跌百分比"` | string | 漲跌百分比 |

## TPEx-067 · 上櫃公司治理指數當日成分股資訊

- **方法／URL**：[GET /tpcgi_constituents](https://www.tpex.org.tw/openapi/v1/tpcgi_constituents)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-068 · 上櫃公司治理指數歷史收盤指數

- **方法／URL**：[GET /tpcgi_reward_index](https://www.tpex.org.tw/openapi/v1/tpcgi_reward_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"TPExCorporateGovernanceIndex"` | string | 櫃買公司治理指數 |
| `"TPExCorporateGovernanceReturnIndex"` | string | 櫃買公司治理報酬指數 |

## TPEx-069 · 上櫃公司治理指數當日收盤指數

- **方法／URL**：[GET /tpcgi_change](https://www.tpex.org.tw/openapi/v1/tpcgi_change)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Name"` | string | 指數 |
| `"Index"` | string | 收盤指數 |
| `"Change"` | string | 漲跌百分比 |

## TPEx-070 · 櫃買指數成分股

- **方法／URL**：[GET /tpex_index_consti](https://www.tpex.org.tw/openapi/v1/tpex_index_consti)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P1
- **可支持需求**：D18、D31、D32、D43、D56
- **用途**：櫃買市場與總報酬基準，估 Beta、相對強弱與績效歸因。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"Capitals"` | string | 發行仟股數 |
| `"ClosePrice"` | string | 收市價 |
| `"SecuritiesIndustryCode"` | string | 產業類別 |

## TPEx-071 · 櫃買指數與報酬指數之收市指數

- **方法／URL**：[GET /tpex_reward_index](https://www.tpex.org.tw/openapi/v1/tpex_reward_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P1
- **可支持需求**：D18、D31、D32、D43、D56
- **用途**：櫃買市場與總報酬基準，估 Beta、相對強弱與績效歸因。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"TPExIndex"` | string | 櫃買指數 |
| `"TPExTotalReturnIndex"` | string | 櫃買報酬指數 |

## TPEx-072 · 櫃買「富櫃50指數」當日成分股

- **方法／URL**：[GET /tpex50_constituents](https://www.tpex.org.tw/openapi/v1/tpex50_constituents)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-073 · 櫃買「富櫃50指數」當日收盤指數

- **方法／URL**：[GET /tpex50_change](https://www.tpex.org.tw/openapi/v1/tpex50_change)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Name"` | string | 指數 |
| `"Index"` | string | 收盤指數 |
| `"Change"` | string | 漲跌百分比 |

## TPEx-074 · 櫃買「高殖利率指數」當日成分股

- **方法／URL**：[GET /tphd_constituents](https://www.tpex.org.tw/openapi/v1/tphd_constituents)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-075 · 櫃買「高殖利率指數」當日收盤指數

- **方法／URL**：[GET /tphd_change](https://www.tpex.org.tw/openapi/v1/tphd_change)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Name"` | string | 指數 |
| `"Index"` | string | 收盤指數 |
| `"Change"` | string | 漲跌百分比 |

## TPEx-076 · 櫃買「薪酬指數」當日成分股

- **方法／URL**：[GET /tpci_constituents](https://www.tpex.org.tw/openapi/v1/tpci_constituents)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-077 · 櫃買「薪酬指數」當日收盤指數

- **方法／URL**：[GET /tpci_change](https://www.tpex.org.tw/openapi/v1/tpci_change)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Name"` | string | 指數 |
| `"Index"` | string | 收盤指數 |
| `"Change"` | string | 漲跌百分比 |

## TPEx-078 · 櫃買「薪酬指數」歷史收盤指數

- **方法／URL**：[GET /tpci_reward_index](https://www.tpex.org.tw/openapi/v1/tpci_reward_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"GTSMCompensationIndex"` | string | 櫃買薪酬指數 |
| `"GTSMCompensationTotalReturnIndex"` | string | 櫃買薪酬報酬指數 |

## TPEx-079 · 櫃買「勞工就業88指數」當日成分股

- **方法／URL**：[GET /tpex_emp88_constituents](https://www.tpex.org.tw/openapi/v1/tpex_emp88_constituents)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |

## TPEx-080 · 櫃買「勞工就業88指數」當日收盤指數

- **方法／URL**：[GET /tpex_emp88_change](https://www.tpex.org.tw/openapi/v1/tpex_emp88_change)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Name"` | string | 指數 |
| `"Index"` | string | 收盤指數 |
| `"Change"` | string | 漲跌百分比 |

## TPEx-081 · 櫃買「勞工就業88指數」歷史收盤指數

- **方法／URL**：[GET /tpex_emp88_reward_index](https://www.tpex.org.tw/openapi/v1/tpex_emp88_reward_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"GretaiLaborEmployment88Index"` | string | 櫃買勞工就業88指數 |
| `"GretaiLaborEmployment88TotalReturnIndex"` | string | 櫃買勞工就業88報酬指數 |

## TPEx-082 · 可轉債資產交換ASO及ASW銀行承作餘額

- **方法／URL**：[GET /tpex_dpsp_monthly_CBmcs007](https://www.tpex.org.tw/openapi/v1/tpex_dpsp_monthly_CBmcs007)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"FinancialInstitutionsCode"` | string | 代號 |
| `"FinancialInstitutionsName"` | string | 名稱 |
| `"ASWFixedIncomeOutstanding"` | string | ASW固定收益端 |
| `"ASOOptionOutstanding"` | string | ASO選擇權端 |
| `"TotalOutstanding"` | string | 合計 |

## TPEx-083 · 國際債券當日盤中報價行情表(含寶島債)

- **方法／URL**：[GET /tpex_international_bond_quotes](https://www.tpex.org.tw/openapi/v1/tpex_international_bond_quotes)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Time"` | string | 資料時間 |
| `"BondCode"` | string | 債券代號 |
| `"BondName"` | string | 債券簡稱 |
| `"BidYieldPrice"` | string | 買進殖利率百元價 |
| `"AskYieldPrice"` | string | 賣出殖利率百元價 |

## TPEx-084 · 國際債券當日盤中成交行情表(含寶島債)

- **方法／URL**：[GET /tpex_international_bond_trade](https://www.tpex.org.tw/openapi/v1/tpex_international_bond_trade)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Time"` | string | 資料時間 |
| `"BondCode"` | string | 債券代號 |
| `"BondName"` | string | 債券簡稱 |
| `"LastField"` | string | 最近殖利率 |
| `"Change"` | string | 變動 |
| `"Highest"` | string | 最高殖利率 |
| `"Lowest"` | string | 最低殖利率 |
| `"Volume"` | string | 累計成交萬元 |
| `"LastClose"` | string | 前日收盤 |

## TPEx-085 · 國際債券(一般投資人)

- **方法／URL**：[GET /tpex_international_bond_issue_investor](https://www.tpex.org.tw/openapi/v1/tpex_international_bond_issue_investor)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"BondCode"` | string | 債券代號 |
| `"ShortName"` | string | 債券簡稱 |
| `"Issuer"` | string | 發行人 |
| `"IssuingDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"Tenor"` | string | 年期 |
| `"CurrencyDenomination"` | string | 計價幣別 |
| `"AmountOfIssuance"` | string | 發行總額 |
| `"Coupon"` | string | 票面利率 |
| `"IRR"` | string | 隱含利率 |
| `"EarlyRedemption"` | string | 提前贖回權 |
| `"NonCallPeriodYearxCallFrequencyYear"` | string | 贖回型態 |
| `"SecuritiesUnderwriterOrFinancialConsultingCompany"` | string | 承銷商或財務顧問 |
| `"LiquidityProvider"` | string | 流動量提供者 |
| `"ISIN"` | string | 國際編碼 |
| `"BondDatabase"` | string | 發行資料 |

## TPEx-086 · 國際債券(僅售予專業投資人者)

- **方法／URL**：[GET /tpex_international_bond_issue_org](https://www.tpex.org.tw/openapi/v1/tpex_international_bond_issue_org)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"BondCode"` | string | 債券代號 |
| `"ShortName"` | string | 債券簡稱 |
| `"Issuer"` | string | 發行人 |
| `"IssuingDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"Tenor"` | string | 年期 |
| `"CurrencyDenomination"` | string | 計價幣別 |
| `"AmountOfIssuance"` | string | 發行總額 |
| `"Coupon"` | string | 票面利率 |
| `"IRR"` | string | 隱含利率 |
| `"EarlyRedemption"` | string | 提前贖回權 |
| `"NonCallPeriodYearxCallFrequencyYear"` | string | 贖回型態 |
| `"SecuritiesUnderwriterOrFinancialConsultingCompany"` | string | 承銷商或財務顧問 |
| `"LiquidityProvider"` | string | 流動量提供者 |
| `"ISIN"` | string | 國際編碼 |
| `"BondDatabase"` | string | 發行資料 |

## TPEx-087 · 上櫃公司企業ESG資訊揭露彙總資料-職業安全衛生

- **方法／URL**：[GET /t187ap46_O_21](https://www.tpex.org.tw/openapi/v1/t187ap46_O_21)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"職業災害人數及比率-人數"` | string | 職業災害人數及比率-人數 |
| `"職業災害人數及比率-比率"` | string | 職業災害人數及比率-比率 |
| `"火災件數(件)"` | string | 火災件數(件) |
| `"火災死傷人數(人)"` | string | 火災死傷人數(人) |
| `"火災死傷人數占員工總人數比率"` | string | 火災死傷人數占員工總人數比率 |

## TPEx-088 · 上櫃公司企業ESG資訊揭露彙總資料-功能性委員會

- **方法／URL**：[GET /t187ap46_O_9](https://www.tpex.org.tw/openapi/v1/t187ap46_O_9)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"薪酬委員會席次(席)"` | string | 薪酬委員會席次(席) |
| `"薪酬委員會獨立董事席次(席)"` | string | 薪酬委員會獨立董事席次(席) |
| `"薪酬委員會出席率"` | string | 薪酬委員會出席率 |
| `"審計委員會席次(席)"` | string | 審計委員會席次(席) |
| `"審計委員會出席率"` | string | 審計委員會出席率 |

## TPEx-089 · 上櫃公司企業ESG資訊揭露彙總資料-氣候相關議題管理

- **方法／URL**：[GET /t187ap46_O_8](https://www.tpex.org.tw/openapi/v1/t187ap46_O_8)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"董事會與管理階層對於氣候相關風險與機會之監督及治理"` | string | 董事會與管理階層對於氣候相關風險與機會之監督及治理 |
| `"辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)"` | string | 辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期) |
| `"極端氣候事件及轉型行動對財務之影響"` | string | 極端氣候事件及轉型行動對財務之影響 |
| `"氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度"` | string | 氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度 |
| `"若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響"` | string | 若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響 |
| `"若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標"` | string | 若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標 |
| `"使用內部碳定價作為規劃工具，應說明價格制定基礎"` | string | 使用內部碳定價作為規劃工具，應說明價格制定基礎 |
| `"若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量"` | string | 若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量 |

## TPEx-090 · 興櫃處置有價證券資訊

- **方法／URL**：[GET /tpex_esb_disposal_information](https://www.tpex.org.tw/openapi/v1/tpex_esb_disposal_information)
- **官方 tags**：興櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"公布日期"` | string | 公布日期 |
| `"證券代號"` | string | 證券代號 |
| `"證券名稱"` | string | 證券名稱 |
| `"處置起訖時間"` | string | 處置起訖時間 |
| `"處置原因"` | string | 處置原因 |
| `"處置內容"` | string | 處置內容 |

## TPEx-091 · 興櫃公布注意有價證券資訊

- **方法／URL**：[GET /tpex_esb_warning_information](https://www.tpex.org.tw/openapi/v1/tpex_esb_warning_information)
- **官方 tags**：興櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"公告日期"` | string | 公告日期 |
| `"證券代號"` | string | 證券代號 |
| `"證券名稱"` | string | 證券名稱 |
| `"注意交易資訊"` | string | 注意交易資訊 |
| `"收盤價"` | string | 收盤價 |

## TPEx-092 · 興櫃推薦證券商與推薦之股票

- **方法／URL**：[GET /tpex_esb_recommended_dealer](https://www.tpex.org.tw/openapi/v1/tpex_esb_recommended_dealer)
- **官方 tags**：興櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 股票名稱 |
| `"RecommendationNumber"` | string | 推薦序號 |
| `"DealerCode"` | string | 券商代號 |
| `"DealerName"` | string | 券商名稱 |
| `"RecommendedDealersForAssistance"` | string | 主辦券商 |
| `"AddDate"` | string | 加入日期 |
| `"Contact"` | string | 連絡人 |
| `"Telephone"` | string | 電話 |
| `"Fax"` | string | 傳真 |
| `"Address"` | string | 地址 |

## TPEx-093 · 黃金現貨權證發行基本資料

- **方法／URL**：[GET /tpex_warrant_gold](https://www.tpex.org.tw/openapi/v1/tpex_warrant_gold)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"ListedDate"` | string | 上櫃日期 |
| `"ExpiryDate"` | string | 到期日 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"Type"` | string | 種類 |
| `"American/European"` | string | 美式或歐式 |
| `"CapPrice/Index"` | string | 上限價格或指數 |
| `"FloorPrice/Index"` | string | 下限價格或指數 |
| `"Reset"` | string | 重設型 |
| `"LatestExercisePrice"` | string | 最新履約價 |
| `"LatestExerciseRatio"` | string | 最新行使比例 |
| `"InitialIssuance"` | string | 初次發行單位數量 |
| `"Accum.Accum.Issuance"` | string | 累計增額發行單位數量 |
| `"Accum.CanceledWarrant"` | string | 累計註銷權證數量 |

## TPEx-094 · 黃金現貨權證收盤行情

- **方法／URL**：[GET /tpex_warrant_gold_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_gold_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-095 · 上櫃權證收盤行情日報表

- **方法／URL**：[GET /tpex_warrant_daily_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_daily_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-096 · 上櫃權證收盤行情月報表

- **方法／URL**：[GET /tpex_warrant_monthly_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_monthly_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-097 · 上櫃權證發行基本資料

- **方法／URL**：[GET /tpex_warrant_issue](https://www.tpex.org.tw/openapi/v1/tpex_warrant_issue)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"ListedDate"` | string | 上櫃日期 |
| `"ExpiryDate"` | string | 到期日 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"Type"` | string | 種類 |
| `"American/European"` | string | 美式或歐式 |
| `"CapPrice/Index"` | string | 上限價格或指數 |
| `"FloorPrice/Index"` | string | 下限價格或指數 |
| `"Reset"` | string | 重設型 |
| `"LatestExercisePrice"` | string | 最新履約價 |
| `"Latest ExerciseRatio"` | string | 最新行使比例 |
| `"InitialIssuance"` | string | 初次發行單位數量仟單位 |
| `"Accum.Accum.Issuance"` | string | 累計增額發行單位數量仟單位 |
| `"Accum.CanceledWarrant"` | string | 累計註銷權證數量仟單位 |

## TPEx-098 · 上櫃牛熊證收盤行情(不含展延型牛熊證)日報表

- **方法／URL**：[GET /tpex_warrant_wcb_daily_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_wcb_daily_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-099 · 上櫃牛熊證收盤行情(不含展延型牛熊證)月報表

- **方法／URL**：[GET /tpex_warrant_wcb_monthly_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_wcb_monthly_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-100 · 上櫃牛熊證發行基本資料(不含展延型牛熊證)

- **方法／URL**：[GET /tpex_warrant_wcb_issue](https://www.tpex.org.tw/openapi/v1/tpex_warrant_wcb_issue)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"ListedDate"` | string | 上櫃日期 |
| `"ExpiryDate"` | string | 到期日 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"Type"` | string | 種類 |
| `"American/European"` | string | 美式或歐式 |
| `"CapPrice/Index"` | string | 上限價格或指數 |
| `"FloorPrice/Index"` | string | 下限價格或指數 |
| `"Reset"` | string | 重設型 |
| `"LatestExercisePrice"` | string | 最新履約價 |
| `"Latest ExerciseRatio"` | string | 最新行使比例 |
| `"InitialIssuance"` | string | 初次發行單位數量仟單位 |
| `"Accum.Accum.Issuance"` | string | 累計增額發行單位數量仟單位 |
| `"Accum.CanceledWarrant"` | string | 累計註銷權證數量仟單位 |

## TPEx-101 · 上櫃展延型牛熊證收盤行情日報表

- **方法／URL**：[GET /tpex_warrant_wxy_daily_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_wxy_daily_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-102 · 上櫃展延型牛熊證收盤行情月報表

- **方法／URL**：[GET /tpex_warrant_wxy_monthly_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_wxy_monthly_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol."` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-103 · 上櫃展延型牛熊證發行基本資料

- **方法／URL**：[GET /tpex_warrant_wxy_issue](https://www.tpex.org.tw/openapi/v1/tpex_warrant_wxy_issue)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"ListedDate"` | string | 上櫃日期 |
| `"ExpiryDate"` | string | 到期日 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"Type"` | string | 種類 |
| `"American/European"` | string | 美式或歐式 |
| `"CapPrice/Index"` | string | 上限價格或指數 |
| `"FloorPrice/Index"` | string | 下限價格或指數 |
| `"Reset"` | string | 重設型 |
| `"LatestExercisePrice"` | string | 最新履約價 |
| `"Latest ExerciseRatio"` | string | 最新行使比例 |
| `"InitialIssuance"` | string | 初次發行單位數量仟單位 |
| `"Accum.Accum.Issuance"` | string | 累計增額發行單位數量仟單位 |
| `"Accum.CanceledWarrant"` | string | 累計註銷權證數量仟單位 |

## TPEx-104 · 單筆權證成交資料

- **方法／URL**：[GET /tpex_warrant_quts](https://www.tpex.org.tw/openapi/v1/tpex_warrant_quts)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Code"` | string | 代號 |
| `"Name"` | string | 名稱 |
| `"Open"` | string | 開市價 |
| `"High"` | string | 最高價 |
| `"Low"` | string | 最低價 |
| `"Close"` | string | 收市價 |
| `"Change"` | string | 漲跌 |
| `"TradeVol. "` | string | 成交量 |
| `"No.OfTransactions"` | string | 筆數 |
| `"TradeValue"` | string | 成交金額 |
| `"UnderlyingStockCode"` | string | 標的代號 |
| `"UnderlyingStock"` | string | 證券 |
| `"UnderlyingStockClosePrice"` | string | 標的或指數收盤 |
| `"UnderlyingStock PriceChange"` | string | 標的或指數漲跌 |

## TPEx-105 · 每日權證交易人數(上櫃)

- **方法／URL**：[GET /tpex_warrant_statistics](https://www.tpex.org.tw/openapi/v1/tpex_warrant_statistics)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Category"` | string | 統計類別 |
| `"Statistics"` | string | 統計數據 |

## TPEx-106 · 上櫃股票權證資訊

- **方法／URL**：[GET /tpex_warrant](https://www.tpex.org.tw/openapi/v1/tpex_warrant)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Item"` | string | 項次 |
| `"Code"` | string | 權證代號 |
| `"Name"` | string | 權證名稱 |
| `"UnderlyingCode"` | string | 權證標的 |
| `"Call /Put"` | string | 認購售 |
| `"ExerciseStyle"` | string | 美式歐式 |
| `"WithCeiling-floorStyleOrNot"` | string | 上下限型 |
| `"WithResetStyleOrNot"` | string | 重設型 |
| `"CallableBullOrBearStyle"` | string | 牛熊證 |
| `"LatestStrikePrice"` | string | 最新履約價 |
| `"LatestExercise Ratio"` | string | 最新行使比例 |
| `"OriginalIssuedUnits"` | string | 初次發行單位數量 |
| `"AccumulatedFollow-OnIssuedUnits"` | string | 累計增額發行單位數量 |
| `"AccumulatedCancellationUnits"` | string | 累計註銷權證數量 |
| `"ExpirationDate"` | string | 到期日 |

## TPEx-107 · 上櫃權證當日暫停/恢復交易資訊

- **方法／URL**：[GET /tpex_warrant_suspend_today](https://www.tpex.org.tw/openapi/v1/tpex_warrant_suspend_today)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"WarrantCode"` | string | 權證代號 |
| `"WarrantName"` | string | 權證名稱 |
| `"SecuritiesCompanyCode"` | string | 標的證券代號 |
| `"CompanyName"` | string | 標的證券名稱 |
| `"SuspendedTime"` | string | 暫停交易 |
| `"ResumedTime"` | string | 恢復交易 |

## TPEx-108 · 上櫃權證歷史暫停/恢復交易資訊

- **方法／URL**：[GET /tpex_warrant_suspend_history](https://www.tpex.org.tw/openapi/v1/tpex_warrant_suspend_history)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Year"` | string | 資料年份 |
| `"No."` | string | 序號 |
| `"Date"` | string | 交易日期 |
| `"WarrantCode"` | string | 權證代號 |
| `"WarrantName"` | string | 權證名稱 |
| `"StockCode"` | string | 標的證券代號 |
| `"StockName"` | string | 標的證券名稱 |
| `"SuspendedTime"` | string | 暫停交易時間 |
| `"ResumedTime"` | string | 恢復交易時間 |

## TPEx-109 · 開放式基金當日行情表

- **方法／URL**：[GET /tpex_opfund_latest](https://www.tpex.org.tw/openapi/v1/tpex_opfund_latest)
- **官方 tags**：開放式基金
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：開放式基金行情及造市商，不是指定 30 ETF 的每日前 15 持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Time"` | string | 資料時間 |
| `"SecurityCode"` | string | 受益憑證代號 |
| `"ListedOpenEndedFund"` | string | 基金簡稱 |
| `"PreNAV"` | string | 前日淨值 |
| `"EstimatedNAV"` | string | 當日預估淨值 |
| `"Pre Avg."` | string | 前日均價 |
| `"B.Price"` | string | 報買價 |
| `"B.Qty."` | string | 報買量 |
| `"S.Price"` | string | 報賣價 |
| `"S.Qty."` | string | 報賣量 |
| `"Highest"` | string | 日最高 |
| `"Lowest"` | string | 日最低 |
| `"Avg."` | string | 日均價 |
| `"LatestPrice"` | string | 成交 |
| `"Type"` | string | 投資人成交買賣別 |
| `"Volume"` | string | 成交量 |

## TPEx-110 · 開放式基金受益憑證造市商與造市之基金

- **方法／URL**：[GET /tpex_opfund_recommended_dealer](https://www.tpex.org.tw/openapi/v1/tpex_opfund_recommended_dealer)
- **官方 tags**：開放式基金
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：開放式基金行情及造市商，不是指定 30 ETF 的每日前 15 持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecurityCode"` | string | 受益憑證代號 |
| `"SecurityName"` | string | 基金簡稱 |
| `"No."` | string | 推薦序號 |
| `"MarketMakerCode"` | string | 造市商代號 |
| `"MarketMakerName"` | string | 造市商名稱 |
| `"AddDate"` | string | 加入日期 |
| `"Contact"` | string | 連絡人 |
| `"Telephone"` | string | 電話 |
| `"Address"` | string | 地址 |

## TPEx-111 · 開放式基金市場現況

- **方法／URL**：[GET /tpex_opfund_market_highlight](https://www.tpex.org.tw/openapi/v1/tpex_opfund_market_highlight)
- **官方 tags**：開放式基金
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：開放式基金行情及造市商，不是指定 30 ETF 的每日前 15 持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"NumberOfFunds"` | string | 登錄基金檔數 |
| `"TotalTradingAmount"` | string | 本日總成交值 |
| `"TotalTradingVolume"` | string | 本日總成交量受益權單位數 |
| `"TotalNumberOfTransactions"` | string | 本日總成交筆數 |
| `"NumberOfMarketMakers"` | string | 造市商總家數 |
| `"TotalNumberOfPositionsRecommended"` | string | 造市部位總數 |
| `"AverageNumberOfFundsPerMarketMaker"` | string | 平均每家造市商造市之基金檔數 |
| `"AverageNumberOfMarketMakersPerFund"` | string | 平均每檔基金之造市商家數 |
| `"NumberOfIncrease"` | string | 上漲檔數 |
| `"NumberOfDecrease"` | string | 下跌檔數 |
| `"NumberOfUnchanged"` | string | 持平檔數 |
| `"NumberOfIncompleteIincludingSuspended"` | string | 未成交含暫停交易檔數 |

## TPEx-112 · 黃金現貨市場現況

- **方法／URL**：[GET /tpex_gold_market_highlight](https://www.tpex.org.tw/openapi/v1/tpex_gold_market_highlight)
- **官方 tags**：黃金現貨
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D48
- **用途**：台灣黃金現貨價格背景；需另核單位與國際金價基差。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"NumberOfRegisteredGold"` | string | 登錄檔數 |
| `"TotalTradingAmount"` | string | 本日總成交值 |
| `"TotalTradingVolume"` | string | 本日總成交量 |
| `"TotalNumberOfTransactions"` | string | 本日總成交筆數 |
| `"NumberOfMarketMakers"` | string | 造市商總家數 |
| `"AverageNumberOfMarketMakersPerGold"` | string | 平均每檔黃金之造市商家數 |
| `"NumberOfIncrease"` | string | 上漲檔數 |
| `"NumberOfDecrease"` | string | 下跌檔數 |
| `"NumberOfUnchanged"` | string | 持平檔數 |
| `"NumberOfIncompleteIincludingSuspended"` | string | 未成交含暫停交易檔數 |

## TPEx-113 · 造市商與造市之黃金現貨

- **方法／URL**：[GET /tpex_gold_recommended_dealer](https://www.tpex.org.tw/openapi/v1/tpex_gold_recommended_dealer)
- **官方 tags**：黃金現貨
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D48
- **用途**：台灣黃金現貨價格背景；需另核單位與國際金價基差。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"GoldCode"` | string | 黃金現貨代號 |
| `"GoldName"` | string | 黃金現貨簡稱 |
| `"No."` | string | 推薦序號 |
| `"MarketMakerCode"` | string | 造市商代號 |
| `"MarketMakerName"` | string | 造市商名稱 |
| `"AddDate"` | string | 加入日期 |
| `"Contact"` | string | 連絡人 |
| `"Telephone"` | string | 電話 |
| `"Fax"` | string | 傳真 |
| `"Address"` | string | 地址 |

## TPEx-114 · 黃金現貨當日行情表

- **方法／URL**：[GET /tpex_gold_latest](https://www.tpex.org.tw/openapi/v1/tpex_gold_latest)
- **官方 tags**：黃金現貨
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D48
- **用途**：台灣黃金現貨價格背景；需另核單位與國際金價基差。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Time"` | string | 資料時間 |
| `"GoldCode"` | string | 黃金現貨代號 |
| `"GoldShortName"` | string | 黃金現貨簡稱 |
| `"QuotedBuyingPrePrice"` | string | 買進報價前日價格 |
| `"QuotedBuyingB.Price"` | string | 買進報價價格 |
| `"QuotedBuyingB.Qty."` | string | 買進報價數量 |
| `"QuotedBuyingChange"` | string | 買進報價漲跌幅 |
| `"QuotedSellingPrePrice"` | string | 賣出報價前日價格 |
| `"QuotedSellingS.Price"` | string | 賣出報價價格 |
| `"QuotedSellingS.Qty."` | string | 賣出報價數量 |
| `"QuotedSellingChange"` | string | 賣出報價漲跌幅 |
| `"TradingPreAvg."` | string | 投資人成交前日均價 |
| `"TradingHighest"` | string | 投資人成交當日最高 |
| `"TradingLowest"` | string | 投資人成交當日最低 |
| `"TradingAvg."` | string | 投資人成交當日均價 |
| `"TradingLatestTradingInfo.Type"` | string | 投資人最近一筆成交買賣別 |
| `"TradingLatestTradingInfo.LatestPrice"` | string | 投資人最近一筆成交價 |
| `"TradingLatestTradingInfo.Volume"` | string | 投資人最近一筆成交量 |
| `"TradingVolume"` | string | 投資人成交量 |
| `"TradingTransaction"` | string | 投資人成交筆數 |

## TPEx-115 · 創櫃板公司市場現況

- **方法／URL**：[GET /tpex_gisa_highlight](https://www.tpex.org.tw/openapi/v1/tpex_gisa_highlight)
- **官方 tags**：創櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"CumulativeNumberOfCompaniesApplyingForGISARegistration"` | string | 申請公司 |
| `"AmountOfCapitalRaisedThroughTheGISACapitalRaisingPlatform"` | string | 透過創櫃板籌資系統籌資金額 |
| `"NumberOfCompaniesInIntegrativeCounseling"` | string | 受輔導公司（不包含已登錄創櫃板公司） |
| `"NumberOfGISACompanies"` | string | 創櫃板公司 |

## TPEx-116 · 創櫃板公司資訊

- **方法／URL**：[GET /tpex_gisa_company](https://www.tpex.org.tw/openapi/v1/tpex_gisa_company)
- **官方 tags**：創櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司簡稱 |
| `"Industry"` | string | 產業類別 |

## TPEx-117 · 於登錄創櫃板前辦理籌資資訊

- **方法／URL**：[GET /tpex_gisa_financing_before](https://www.tpex.org.tw/openapi/v1/tpex_gisa_financing_before)
- **官方 tags**：創櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"現金增資期別"` | string | 現金增資期別 |
| `"發行新股種類"` | string | 發行新股種類 |
| `"籌資資金用途"` | string | 籌資資金用途 |
| `"每股面額"` | string | 每股面額 |
| `"每股發行價格"` | string | 每股發行價格 |
| `"於創櫃板籌資金額"` | string | 於創櫃板籌資金額 |
| `"於創櫃板辦理籌資股數"` | string | 於創櫃板辦理籌資股數 |
| `"於創櫃板投資人已認購股數"` | string | 於創櫃板投資人已認購股數 |
| `"認購率"` | string | 認購率 |
| `"僅限天使投資人認購"` | string | 僅限天使投資人認購 |
| `"決定認購人名單方式"` | string | 決定認購人名單方式 |
| `"認購期間"` | string | 認購期間 |
| `"繳款期間"` | string | 繳款期間 |
| `"籌資計畫"` | string | 籌資計畫 |
| `"產業類別"` | string | 產業類別 |
| `"推薦或出具創新創意意見書單位"` | string | 推薦或出具創新創意意見書單位 |
| `"籌資辦理進度"` | string | 籌資辦理進度 |
| `"備註"` | string | 備註 |

## TPEx-118 · 上櫃公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟 

- **方法／URL**：[GET /t187ap46_O_20](https://www.tpex.org.tw/openapi/v1/t187ap46_O_20)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)"` | string | 因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元) |

## TPEx-119 · 上櫃公司企業ESG資訊揭露彙總資料-風險管理政策 

- **方法／URL**：[GET /t187ap46_O_19](https://www.tpex.org.tw/openapi/v1/t187ap46_O_19)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"重大事件之風險管理政策"` | string | 重大事件之風險管理政策 |
| `"與使用關鍵材料相關的風險管理之描述"` | string | 與使用關鍵材料相關的風險管理之描述 |

## TPEx-120 · 上櫃公司企業ESG資訊揭露彙總資料-社區關係 

- **方法／URL**：[GET /t187ap46_O_15](https://www.tpex.org.tw/openapi/v1/t187ap46_O_15)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"在人口密集地區的煉油廠數量(座)"` | string | 在人口密集地區的煉油廠數量(座) |

## TPEx-121 · 上櫃公司企業ESG資訊揭露彙總資料-供應鏈管理 

- **方法／URL**：[GET /t187ap46_O_13](https://www.tpex.org.tw/openapi/v1/t187ap46_O_13)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D24、D49
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"採購符合國際認可之產品責任標準者占整體採購之百分比，並依標準區分"` | string | 採購符合國際認可之產品責任標準者占整體採購之百分比，並依標準區分 |
| `"對供應商進行稽核之家數(家)"` | string | 對供應商進行稽核之家數(家) |
| `"對供應商進行稽核之百分比"` | string | 對供應商進行稽核之百分比 |

## TPEx-122 · 上櫃公司企業ESG資訊揭露彙總資料-食品安全

- **方法／URL**：[GET /t187ap46_O_12](https://www.tpex.org.tw/openapi/v1/t187ap46_O_12)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"為改善食品衛生、安全與品質，而針對其從業人員、作業場所、設施衛生管理及其品保制度等方面進行之評估與改進及所影響之百分比"` | string | 為改善食品衛生、安全與品質，而針對其從業人員、作業場所、設施衛生管理及其品保制度等方面進行之評估與改進及所影響之百分比 |
| `"違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之事件類別與次數"` | string | 違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之事件類別與次數 |
| `"違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之產品下架次數(次)"` | string | 違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之產品下架次數(次) |
| `"違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之下架產品總重量(公噸_t)"` | string | 違反有關產品與服務之健康與安全法規及未遵循產品與服務之資訊與標示法規之下架產品總重量(公噸_t) |
| `"經獨立第三方驗證符合國際認證之食品安全管理系統標準之廠房所生產產品之百分比"` | string | 經獨立第三方驗證符合國際認證之食品安全管理系統標準之廠房所生產產品之百分比 |
| `"依法規要求或自願進行產品追溯與追蹤管理之相關產品占所有產品之百分比"` | string | 依法規要求或自願進行產品追溯與追蹤管理之相關產品占所有產品之百分比 |
| `"依法規要求或自願設置食品安全實驗室之相關支出(仟元)"` | string | 依法規要求或自願設置食品安全實驗室之相關支出(仟元) |
| `"依法規要求或自願設置食品安全實驗室之相關支出占營業收入淨額之百分比"` | string | 依法規要求或自願設置食品安全實驗室之相關支出占營業收入淨額之百分比 |

## TPEx-123 · 上櫃公司企業ESG資訊揭露彙總資料-產品品質與安全

- **方法／URL**：[GET /t187ap46_O_14](https://www.tpex.org.tw/openapi/v1/t187ap46_O_14)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"售出產品重量(公噸_t)"` | string | 售出產品重量(公噸_t) |
| `"生產設施場所數量(座)"` | string | 生產設施場所數量(座) |
| `"依產品類別之產品產量"` | string | 依產品類別之產品產量 |

## TPEx-124 · 櫃買「富櫃200指數」當日成分股

- **方法／URL**：[GET /tpex200_constituents](https://www.tpex.org.tw/openapi/v1/tpex200_constituents)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"資料日期"` | string | 資料日期 |
| `"股票代號"` | string | 股票代號 |
| `"股票名稱"` | string | 股票名稱 |

## TPEx-125 · 上櫃公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表

- **方法／URL**：[GET /t187ap41_O](https://www.tpex.org.tw/openapi/v1/t187ap41_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D05、D23、D39
- **用途**：董事會股利方案與股東會日曆，提案不等於最終實施或可用現金。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"公司地址"` | string | 公司地址 |
| `"股東常(臨時)會"` | string | 股東常(臨時)會 |
| `"開會日期"` | string | 開會日期 |
| `"開會地點"` | string | 開會地點 |
| `"是否改選董監"` | string | 是否改選董監 |
| `"聯絡電話"` | string | 聯絡電話 |
| `"股務單位"` | string | 股務單位 |
| `"股務單位電話"` | string | 股務單位電話 |
| `"是否採電子投票"` | string | 是否採電子投票 |

## TPEx-126 · 興櫃公司每月營業收入彙總表

- **方法／URL**：[GET /t187ap05_R](https://www.tpex.org.tw/openapi/v1/t187ap05_R)
- **官方 tags**：公司治理
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"資料年月"` | string | 資料年月 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"產業別"` | string | 產業別 |
| `"營業收入-當月營收"` | string | 營業收入-當月營收 |
| `"營業收入-上月營收"` | string | 營業收入-上月營收 |
| `"營業收入-去年當月營收"` | string | 營業收入-去年當月營收 |
| `"營業收入-上月比較增減(%)"` | string | 營業收入-上月比較增減(%) |
| `"營業收入-去年同月增減(%)"` | string | 營業收入-去年同月增減(%) |
| `"累計營業收入-當月累計營收"` | string | 累計營業收入-當月累計營收 |
| `"累計營業收入-去年累計營收"` | string | 累計營業收入-去年累計營收 |
| `"累計營業收入-前期比較增減(%)"` | string | 累計營業收入-前期比較增減(%) |
| `"備註"` | string | 備註 |

## TPEx-127 · 上櫃公司企業ESG資訊揭露彙總資料-廢棄物管理

- **方法／URL**：[GET /t187ap46_O_4](https://www.tpex.org.tw/openapi/v1/t187ap46_O_4)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"有害廢棄物量-數據(公噸)"` | string | 有害廢棄物量-數據(公噸) |
| `"有害廢棄物量-資料範圍"` | string | 有害廢棄物量-資料範圍 |
| `"非有害廢棄物量-數據(公噸)"` | string | 非有害廢棄物量-數據(公噸) |
| `"非有害廢棄物量-資料範圍"` | string | 非有害廢棄物量-資料範圍 |
| `"總重量(有害+非有害)-數據(公噸)"` | string | 總重量(有害+非有害)-數據(公噸) |
| `"總重量(有害+非有害)-資料範圍"` | string | 總重量(有害+非有害)-資料範圍 |
| `"廢棄物密集度-密集度(公噸/單位)"` | string | 廢棄物密集度-密集度(公噸/單位) |
| `"廢棄物密集度-單位"` | string | 廢棄物密集度-單位 |
| `"取得驗證"` | string | 取得驗證 |

## TPEx-128 · 上櫃公司企業ESG資訊揭露彙總資料-能源管理

- **方法／URL**：[GET /t187ap46_O_2](https://www.tpex.org.tw/openapi/v1/t187ap46_O_2)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"使用率(再生能源/總能源)"` | string | 使用率(再生能源/總能源) |
| `"資料範圍"` | string | 資料範圍 |
| `"取得驗證"` | string | 取得驗證 |

## TPEx-129 · 上櫃公司企業ESG資訊揭露彙總資料-投資人溝通

- **方法／URL**：[GET /t187ap46_O_7](https://www.tpex.org.tw/openapi/v1/t187ap46_O_7)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"公司年度召開法說會次數(次)"` | string | 公司年度召開法說會次數(次) |

## TPEx-130 · 上櫃公司企業ESG資訊揭露彙總資料-溫室氣體排放

- **方法／URL**：[GET /t187ap46_O_1](https://www.tpex.org.tw/openapi/v1/t187ap46_O_1)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"範疇一排放量(噸CO2e)"` | string | 範疇一排放量(噸CO2e) |
| `"範疇一資料邊界"` | string | 範疇一資料邊界 |
| `"範疇一取得驗證"` | string | 範疇一取得驗證 |
| `"範疇二排放量(噸CO2e)"` | string | 範疇二排放量(噸CO2e) |
| `"範疇二資料邊界"` | string | 範疇二資料邊界 |
| `"範疇二取得驗證"` | string | 範疇二取得驗證 |
| `"範疇三排放量(噸CO2e)"` | string | 範疇三排放量(噸CO2e) |
| `"範疇三資料邊界"` | string | 範疇三資料邊界 |
| `"範疇三取得驗證"` | string | 範疇三取得驗證 |
| `"溫室氣體排放密集度(公噸CO₂e/百萬元營業額)"` | string | 溫室氣體排放密集度(公噸CO₂e/百萬元營業額) |

## TPEx-131 · 上櫃公司企業ESG資訊揭露彙總資料-董事會

- **方法／URL**：[GET /t187ap46_O_6](https://www.tpex.org.tw/openapi/v1/t187ap46_O_6)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"董事席次(含獨立董事)(席)"` | string | 董事席次(含獨立董事)(席) |
| `"獨立董事席次(席)"` | string | 獨立董事席次(席) |
| `"女性董事席次及比率-席"` | string | 女性董事席次及比率-席 |
| `"女性董事席次及比率-比率"` | string | 女性董事席次及比率-比率 |
| `"董事出席董事會出席率"` | string | 董事出席董事會出席率 |
| `"董監事進修時數符合進修要點比率"` | string | 董監事進修時數符合進修要點比率 |

## TPEx-132 · 上櫃公司企業ESG資訊揭露彙總資料-人力發展

- **方法／URL**：[GET /t187ap46_O_5](https://www.tpex.org.tw/openapi/v1/t187ap46_O_5)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"員工福利平均數(仟元/人)"` | string | 員工福利平均數(仟元/人) |
| `"員工薪資平均數(仟元/人)"` | string | 員工薪資平均數(仟元/人) |
| `"非擔任主管職務之全時員工薪資平均數(仟元/人)"` | string | 非擔任主管職務之全時員工薪資平均數(仟元/人) |
| `"非擔任主管職務之全時員工薪資平均數變動百分比"` | string | 非擔任主管職務之全時員工薪資平均數變動百分比 |
| `"非擔任主管之全時員工薪資中位數(仟元/人)"` | string | 非擔任主管之全時員工薪資中位數(仟元/人) |
| `"非擔任主管職務之全時員工薪資中位數變動百分比"` | string | 非擔任主管職務之全時員工薪資中位數變動百分比 |
| `"管理職女性主管佔比"` | string | 管理職女性主管佔比 |
| `"新進員工年齡分布"` | string | 新進員工年齡分布 |
| `"離職員工年齡分布"` | string | 離職員工年齡分布 |
| `"高齡員工晉用政策及培訓計畫"` | string | 高齡員工晉用政策及培訓計畫 |

## TPEx-133 · 上櫃公司企業ESG資訊揭露彙總資料-水資源管理

- **方法／URL**：[GET /t187ap46_O_3](https://www.tpex.org.tw/openapi/v1/t187ap46_O_3)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"報告年度"` | string | 報告年度 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"用水量(公噸)"` | string | 用水量(公噸) |
| `"資料範圍"` | string | 資料範圍 |
| `"用水密集度-密集度(公噸/單位)"` | string | 用水密集度-密集度(公噸/單位) |
| `"用水密集度-單位"` | string | 用水密集度-單位 |
| `"取得驗證"` | string | 取得驗證 |

## TPEx-134 · 二十九大類股營收變化統計表

- **方法／URL**：[GET /mopsfin_t187ap05_OA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_OA)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D19、D50
- **用途**：月營收年增、累計與加速度，保留各次發布快照。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"資料年月"` | string | 資料年月 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"產業別"` | string | 產業別 |
| `"營業收入-當月營收"` | string | 營業收入-當月營收 |
| `"營業收入-上月營收"` | string | 營業收入-上月營收 |
| `"營業收入-去年當月營收"` | string | 營業收入-去年當月營收 |
| `"營業收入-上月比較增減(%)"` | string | 營業收入-上月比較增減(%) |
| `"營業收入-去年同月增減(%)"` | string | 營業收入-去年同月增減(%) |
| `"累計營業收入-當月累計營收"` | string | 累計營業收入-當月累計營收 |
| `"累計營業收入-去年累計營收"` | string | 累計營業收入-去年累計營收 |
| `"累計營業收入-前期比較增減(%)"` | string | 累計營業收入-前期比較增減(%) |
| `"備註"` | string | 備註 |

## TPEx-135 · 發行公司營收創新高一覽表(上櫃)

- **方法／URL**：[GET /mopsfin_t187ap05_OB](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_OB)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D19、D50
- **用途**：月營收年增、累計與加速度，保留各次發布快照。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"資料年月"` | string | 資料年月 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"產業別"` | string | 產業別 |
| `"營業收入-當月營收"` | string | 營業收入-當月營收 |
| `"營業收入-上月營收"` | string | 營業收入-上月營收 |
| `"營業收入-去年當月營收"` | string | 營業收入-去年當月營收 |
| `"營業收入-上月比較增減(%)"` | string | 營業收入-上月比較增減(%) |
| `"營業收入-去年同月增減(%)"` | string | 營業收入-去年同月增減(%) |
| `"累計營業收入-當月累計營收"` | string | 累計營業收入-當月累計營收 |
| `"累計營業收入-去年累計營收"` | string | 累計營業收入-去年累計營收 |
| `"累計營業收入-前期比較增減(%)"` | string | 累計營業收入-前期比較增減(%) |
| `"備註"` | string | 備註 |

## TPEx-136 · 美元固定利率不可贖回國際債券理論價格

- **方法／URL**：[GET /BDdos216UTF](https://www.tpex.org.tw/openapi/v1/BDdos216UTF)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"資料日期"` | string | 資料日期 |
| `"債券代碼"` | string | 債券代碼 |
| `"債券簡稱"` | string | 債券簡稱 |
| `"發行人"` | string | 發行人 |
| `"發行日"` | string | 發行日 |
| `"到期日"` | string | 到期日 |
| `"信用評等"` | string | 信用評等 |
| `"利率"` | string | 利率 |
| `"理論價格含息"` | string | 理論價格含息 |
| `"應計利息"` | string | 應計利息 |
| `"除息價格"` | string | 除息價格 |

## TPEx-137 · 美元附息固定利率可贖回國際債券理論價格

- **方法／URL**：[GET /BDdos215UTF](https://www.tpex.org.tw/openapi/v1/BDdos215UTF)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"資料日期"` | string | 資料日期 |
| `"債券代碼"` | string | 債券代碼 |
| `"債券簡稱"` | string | 債券簡稱 |
| `"發行人"` | string | 發行人 |
| `"發行日"` | string | 發行日 |
| `"到期日"` | string | 到期日 |
| `"信用評等"` | string | 信用評等 |
| `"利率"` | string | 利率 |
| `"贖回期間結構"` | string | 贖回期間結構 |
| `"公平價格含隱含息"` | string | 公平價格含隱含息 |
| `"隱含應計利息"` | string | 隱含應計利息 |
| `"扣除隱含息價格"` | string | 扣除隱含息價格 |

## TPEx-138 · 美元零息可贖回國際債券理論價格

- **方法／URL**：[GET /BDdos209UTF](https://www.tpex.org.tw/openapi/v1/BDdos209UTF)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"資料日期"` | string | 資料日期 |
| `"債券代碼"` | string | 債券代碼 |
| `"債券簡稱"` | string | 債券簡稱 |
| `"發行人"` | string | 發行人 |
| `"發行日"` | string | 發行日 |
| `"到期日"` | string | 到期日 |
| `"信用評等"` | string | 信用評等 |
| `"隱含利率%"` | string | 隱含利率% |
| `"贖回期間結構"` | string | 贖回期間結構 |
| `"理論價格"` | string | 理論價格 |
| `"隱含應計利息"` | string | 隱含應計利息 |
| `"扣除隱含息價格"` | string | 扣除隱含息價格 |

## TPEx-139 · 創櫃板公司透過籌資系統辦理籌資資訊

- **方法／URL**：[GET /tpex_gisa_financing_history](https://www.tpex.org.tw/openapi/v1/tpex_gisa_financing_history)
- **官方 tags**：創櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"現金增資期別"` | string | 現金增資期別 |
| `"發行新股種類"` | string | 發行新股種類 |
| `"籌資資金用途"` | string | 籌資資金用途 |
| `"每股發行價格"` | string | 每股發行價格 |
| `"於創櫃板辦理籌資股數"` | string | 於創櫃板辦理籌資股數 |
| `"於創櫃板籌資金額"` | string | 於創櫃板籌資金額 |
| `"於創櫃板投資人已認購股數"` | string | 於創櫃板投資人已認購股數 |
| `"認購率"` | string | 認購率 |
| `"僅限天使投資人認購"` | string | 僅限天使投資人認購 |
| `"決定認購人名單方式"` | string | 決定認購人名單方式 |
| `"認購期間"` | string | 認購期間 |
| `"繳款期間"` | string | 繳款期間 |
| `"籌資計畫"` | string | 籌資計畫 |
| `"產業類別"` | string | 產業類別 |
| `"推薦或出具創新創意意見書單位"` | string | 推薦或出具創新創意意見書單位 |
| `"籌資辦理進度"` | string | 籌資辦理進度 |
| `"備註"` | string | 備註 |

## TPEx-140 · 上櫃公司股東行使提案權情形彙總表

- **方法／URL**：[GET /mopsfin_t187ap35_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap35_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"召開股東會日期"` | string | 召開股東會日期 |
| `"股東依公司法第172條之1行使提案權-提案受理期間"` | string | 股東依公司法第172條之1行使提案權-提案受理期間 |
| `"提案受理處所"` | string | 提案受理處所 |
| `"股東提案內容"` | string | 股東提案內容 |

## TPEx-141 · 上櫃權證基本資料彙總表

- **方法／URL**：[GET /mopsfin_t187ap37_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap37_O)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"權證代號"` | string | 權證代號 |
| `"權證簡稱"` | string | 權證簡稱 |
| `"權證類型"` | string | 權證類型 |
| `"類別"` | string | 類別 |
| `"流動量提供者報價方式"` | string | 流動量提供者報價方式 |
| `"履約開始日"` | string | 履約開始日 |
| `"最後交易日"` | string | 最後交易日 |
| `"履約截止日"` | string | 履約截止日 |
| `"發行單位數量(仟單位)"` | string | 發行單位數量(仟單位) |
| `"結算方式(詳附註編號說明)"` | string | 結算方式(詳附註編號說明) |
| `"標的證券/指數"` | string | 標的證券/指數 |
| `"最新標的履約配發數量(每仟單位權證)"` | string | 最新標的履約配發數量(每仟單位權證) |
| `"原始履約價格(元)/履約指數"` | string | 原始履約價格(元)/履約指數 |
| `"原始上限價格(元)/上限指數"` | string | 原始上限價格(元)/上限指數 |
| `"原始下限價格(元)/下限指數"` | string | 原始下限價格(元)/下限指數 |
| `"最新履約價格(元)/履約指數"` | string | 最新履約價格(元)/履約指數 |
| `"最新上限價格(元)/上限指數"` | string | 最新上限價格(元)/上限指數 |
| `"最新下限價格(元)/下限指數"` | string | 最新下限價格(元)/下限指數 |
| `"備註"` | string | 備註 |

## TPEx-142 · 上櫃認購(售)權證每日成交資料檔

- **方法／URL**：[GET /mopsfin_t187ap42_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap42_O)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"交易日期"` | string | 交易日期 |
| `"權證代號"` | string | 權證代號 |
| `"權證名稱"` | string | 權證名稱 |
| `"成交金額"` | string | 成交金額 |
| `"成交數量"` | string | 成交數量 |

## TPEx-143 · 上櫃公司公司治理之相關規程規則

- **方法／URL**：[GET /mopsfin_t187ap32_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap32_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"公司治理之相關規程規則"` | string | 公司治理之相關規程規則 |

## TPEx-144 · 上櫃公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表

- **方法／URL**：[GET /mopsfin_t187ap34_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap34_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"股東常(臨時)會日期-常或臨時"` | string | 股東常(臨時)會日期-常或臨時 |
| `"股東常(臨時)會日期-日期"` | string | 股東常(臨時)會日期-日期 |
| `"是否選任董監事"` | string | 是否選任董監事 |
| `"董監事選任方式"` | string | 董監事選任方式 |
| `"是否採候選人提名制選任董監事"` | string | 是否採候選人提名制選任董監事 |
| `"採候選人提名制選任董監事相關公告-提名受理期間"` | string | 採候選人提名制選任董監事相關公告-提名受理期間 |
| `"採候選人提名制選任董監事相關公告-提名受理處所"` | string | 採候選人提名制選任董監事相關公告-提名受理處所 |
| `"候選人類別"` | string | 候選人類別 |
| `"候選人姓名"` | string | 候選人姓名 |
| `"是否當選"` | string | 是否當選 |

## TPEx-145 · 上櫃公司董事長是否兼任總經理

- **方法／URL**：[GET /mopsfin_t187ap33_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap33_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"Chairman"` | string | 董事長 |
| `"GeneralManager"` | string | 總經理 |
| `"董事長是否兼任總經理"` | string | 董事長是否兼任總經理 |

## TPEx-146 · 上櫃公司財務報告經監察人承認情形

- **方法／URL**：[GET /mopsfin_t187ap31_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap31_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"是否設置審計委員會"` | string | 是否設置審計委員會 |
| `"出具本次財務報告審查報告書之監察人姓名"` | string | 出具本次財務報告審查報告書之監察人姓名 |
| `"監察人實際在任席次"` | string | 監察人實際在任席次 |

## TPEx-147 · 上櫃公司董事、監察人質權設定占董事及監察人實際持有股數彙總表

- **方法／URL**：[GET /mopsfin_t187ap09_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap09_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Percent"` | string | 百分比 |
| `"CompanyName"` | string | 公司名稱 |

## TPEx-148 · 上櫃公司董事、監察人持股不足法定成數連續達3個月以上彙總表

- **方法／URL**：[GET /mopsfin_t187ap10_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap10_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"連續不足達3個月"` | string | 連續不足達3個月 |
| `"107/10-12連續不足達4個月"` | string | 107/10-12連續不足達4個月 |
| `"107/09-12連續不足達5個月"` | string | 107/09-12連續不足達5個月 |
| `"107/08-12連續不足達6個月"` | string | 107/08-12連續不足達6個月 |
| `"107/07-12連續不足達7個月"` | string | 107/07-12連續不足達7個月 |
| `"107/06-12連續不足達8個月"` | string | 107/06-12連續不足達8個月 |
| `"107/05-12連續不足達9個月"` | string | 107/05-12連續不足達9個月 |
| `"107/04-12連續不足達10個月"` | string | 107/04-12連續不足達10個月 |
| `"107/03-12連續不足達11個月"` | string | 107/03-12連續不足達11個月 |
| `"107/02-12連續不足達12個月"` | string | 107/02-12連續不足達12個月 |
| `"107/01-12連續不足逾1年以上"` | string | 107/01-12連續不足逾1年以上 |

## TPEx-149 · 上櫃公司經營權及營業範圍異(變)動專區-經營權異動公司

- **方法／URL**：[GET /mopsfin_t187ap24_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap24_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D24、D37、D42
- **用途**：經營權變動、裁罰與資訊申報違規，作公司事件風險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"經營權異動日期"` | string | 經營權異動日期 |
| `"經營權異動說明"` | string | 經營權異動說明 |

## TPEx-150 · 上櫃公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司

- **方法／URL**：[GET /mopsfin_t187ap25_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap25_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D24、D37、D42
- **用途**：經營權變動、裁罰與資訊申報違規，作公司事件風險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"序號"` | string | 序號 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"營業範圍重大變更說明"` | string | 營業範圍重大變更說明 |

## TPEx-151 · 創櫃板辦理中籌資資訊

- **方法／URL**：[GET /tpex_gisa_financing_in_process](https://www.tpex.org.tw/openapi/v1/tpex_gisa_financing_in_process)
- **官方 tags**：創櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"現金增資期別"` | string | 現金增資期別 |
| `"發行新股種類"` | string | 發行新股種類 |
| `"籌資資金用途"` | string | 籌資資金用途 |
| `"現增總股數"` | string | 現增總股數 |
| `"每股面額"` | string | 每股面額 |
| `"每股發行價格"` | string | 每股發行價格 |
| `"籌資金額"` | string | 籌資金額 |
| `"於創櫃板辦理籌資股數"` | string | 於創櫃板辦理籌資股數 |
| `"已認購股數"` | string | 已認購股數 |
| `"認購率"` | string | 認購率 |
| `"僅限天使投資人認購"` | string | 僅限天使投資人認購 |
| `"決定認購人名單方式"` | string | 決定認購人名單方式 |
| `"認購期間"` | string | 認購期間 |
| `"繳款期間"` | string | 繳款期間 |
| `"委託代收價款行庫"` | string | 委託代收價款行庫 |
| `"股務代理機構"` | string | 股務代理機構 |
| `"是否印製實體股票"` | string | 是否印製實體股票 |
| `"籌資計畫"` | string | 籌資計畫 |
| `"點選認購申請"` | string | 點選認購申請 |
| `"產業類別"` | string | 產業類別 |
| `"推薦或出具創新創意意見書單位"` | string | 推薦或出具創新創意意見書單位 |
| `"備註"` | string | 備註 |

## TPEx-152 · 上櫃股票基本資料

- **方法／URL**：[GET /mopsfin_t187ap03_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：競賽與交易狀態／P0
- **可支持需求**：D01、D09、D49
- **用途**：證券識別、發行股數、產業、上市櫃日期與基本資料映射。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"CompanyAbbreviation"` | string | 公司簡稱 |
| `"Registration"` | string | 外國企業註冊地國 |
| `"SecuritiesIndustryCode"` | string | 產業別 |
| `"Address"` | string | 英文通訊地址 |
| `"UnifiedBusinessNo."` | string | 營利事業統一編號 |
| `"Chairman"` | string | 董事長 |
| `"GeneralManager"` | string | 總經理 |
| `"Spokesman"` | string | 發言人 |
| `"TitleOfSpokesman"` | string | 發言人職稱 |
| `"DeputySpokesperson"` | string | 代理發言人 |
| `"Telephone"` | string | 總機電話 |
| `"DateOfIncorporation"` | string | 成立日期 |
| `"DateOfListing"` | string | 上市日期 |
| `"ParValueOfCommonStock"` | string | 普通股每股面額 |
| `"Paidin.Capital.NTDollars"` | string | 實收資本額 |
| `"PrivateStock.shares"` | string | 私募股數 |
| `"PreferredStock.shares"` | string | 特別股 |
| `"PreparationOfFinancialReportType"` | string | 編制財務報表類型 |
| `"StockTransferAgent"` | string | 股票過戶機構 |
| `"StockTransferAgentTelephone"` | string | 過戶電話 |
| `"StockTransferAgentAddress"` | string | 過戶地址 |
| `"AccountingFirm"` | string | 簽證會計師事務所 |
| `"CPA.CharteredPublicAccountant.First"` | string | 簽證會計師1 |
| `"CPA.CharteredPublicAccountant.Second"` | string | 簽證會計師2 |
| `"Symbol"` | string | 英文簡稱 |
| `"Fax"` | string | 傳真機號碼 |
| `"EmailAddress"` | string | 電子郵件信箱 |
| `"WebAddress"` | string | 網址 |
| `"IssueShares"` | string | 已發行普通股數或TDR原股發行股數 |

## TPEx-153 · 上櫃股票外資及陸資買賣超彙總表

- **方法／URL**：[GET /tpex_3insti_qfii_trading](https://www.tpex.org.tw/openapi/v1/tpex_3insti_qfii_trading)
- **官方 tags**：上櫃
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D25、D26
- **用途**：法人交易排行、總體資金流或外資持股水位；股數與金額單位分開。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Rank"` | string | 排行 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `" ForeignInvestorsIncludeMainlandAreaInvestors-TotalBuy"` | string | 外資及陸資合計買進 |
| `" ForeignInvestorsIncludeMainlandAreaInvestors-Total Sell"` | string | 外資及陸資不含自營商賣出 |
| `" ForeignInvestorsInclude MainlandAreaInvestors-Difference"` | string | 外資及陸資不含自營商買賣超仟股 |
| `" ForeignDealers-TotalBuy"` | string | 外資自營商買進 |
| `" ForeignDealers-TotalSell"` | string | 外資自營商賣出 |
| `" ForeignDealers-Difference"` | string | 外資自營商買賣超 |
| `"ForeignInvestorsIncludeMainlandAreaInvestors-TotalSell"` | string | 外資及陸資合計賣出 |
| `" ForeignInvestorsIncludeMainlandAreaInvestors-Difference"` | string | 外資及陸資合計買賣超 |

## TPEx-154 · 興櫃股票當日行情表

- **方法／URL**：[GET /tpex_esb_latest_statistics](https://www.tpex.org.tw/openapi/v1/tpex_esb_latest_statistics)
- **官方 tags**：興櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Time"` | string | 資料時間 |
| `"SecuritiesCompanyCode"` | string | 代號 |
| `"CompanyName"` | string | 名稱 |
| `"PreviousAveragePrice"` | string | 前日均價 |
| `"BuyingPrice"` | string | 報買價 |
| `"BuyingQuantity"` | string | 報買量 |
| `"SellingPrice"` | string | 報賣價 |
| `"SellingQuantity"` | string | 報賣量 |
| `"Highest"` | string | 日最高 |
| `"Lowest"` | string | 日最低 |
| `"Average"` | string | 日均價 |
| `"LatestPrice"` | string | 成交 |
| `"Buy/Sell"` | string | 投資人成交買賣別 |
| `"SuspendTime"` | string | 暫停交易開始時間 |
| `"TransactionVolume"` | string | 成交量 |
| `"ApplyingDate"` | string | 進度日期 |
| `"ApplyingStatus"` | string | 上市櫃進度 |

## TPEx-155 · 上櫃認購(售)權證年度發行量概況統計表

- **方法／URL**：[GET /mopsfin_t187ap36_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap36_O)
- **官方 tags**：權證
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：固定 150 檔股票策略目前不使用；保留完整規格，未來若研究需另設假說。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"發行人代號"` | string | 發行人代號 |
| `"發行人名稱"` | string | 發行人名稱 |
| `"權證代號"` | string | 權證代號 |
| `"名稱"` | string | 名稱 |
| `"標的代號"` | string | 標的代號 |
| `"標的名稱"` | string | 標的名稱 |
| `"申請發行日期"` | string | 申請發行日期 |

## TPEx-156 · 興櫃公司基本資料

- **方法／URL**：[GET /mopsfin_t187ap03_R](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R)
- **官方 tags**：公司治理
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"CompanyAbbreviation"` | string | 公司簡稱 |
| `"Registration"` | string | 外國企業註冊地國 |
| `"SecuritiesIndustryCode"` | string | 產業別 |
| `"Address"` | string | 英文通訊地址 |
| `"UnifiedBusinessNo."` | string | 營利事業統一編號 |
| `"Chairman"` | string | 董事長 |
| `"GeneralManager"` | string | 總經理 |
| `"Spokesman"` | string | 發言人 |
| `"TitleOfSpokesman"` | string | 發言人職稱 |
| `"DeputySpokesperson"` | string | 代理發言人 |
| `"Telephone"` | string | 總機電話 |
| `"DateOfIncorporation"` | string | 成立日期 |
| `"DateOfListing"` | string | 上市日期 |
| `"ParValueOfCommonStock"` | string | 普通股每股面額 |
| `"Paidin.Capital.NTDollars"` | string | 實收資本額 |
| `"PrivateStock.shares"` | string | 私募股數 |
| `"PreferredStock.shares"` | string | 特別股 |
| `"PreparationOfFinancialReportType"` | string | 編制財務報表類型 |
| `"StockTransferAgent"` | string | 股票過戶機構 |
| `"StockTransferAgentTelephone"` | string | 過戶電話 |
| `"StockTransferAgentAddress"` | string | 過戶地址 |
| `"AccountingFirm"` | string | 簽證會計師事務所 |
| `"CPA.CharteredPublicAccountant.First"` | string | 簽證會計師1 |
| `"CPA.CharteredPublicAccountant.Second"` | string | 簽證會計師2 |
| `"Symbol"` | string | 英文簡稱 |
| `"Fax"` | string | 傳真機號碼 |
| `"EmailAddress"` | string | 電子郵件信箱 |
| `"WebAddress"` | string | 網址 |
| `"IssueShares"` | string | 已發行普通股數或TDR原股發行股數 |

## TPEx-157 · 上櫃公司每日重大訊息

- **方法／URL**：[GET /mopsfin_t187ap04_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap04_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P1
- **可支持需求**：D37、D38、D39、D40、D41
- **用途**：重大訊息與事件證據，分別保留發言日期時間、事實發生日、出表與首見時間。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；代表實測 HTTP 200
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

**代表探測證據**：`{"http_status": 200, "rows": 63, "actual_shape": "list", "fetched_at": "2026-10-09T06:26:00.415684+00:00", "sha256": "e506e7f240dffe5f58dc8e3a1baac12e0d7d8ca499e0793c42bd205541f7b5f3", "date_ranges": {"Date": ["1151009"], "發言日期": ["1151008"]}, "observed_fields": ["Date", "發言日期", "發言時間", "SecuritiesCompanyCode", "CompanyName", "主旨", "符合條款", "事實發生日", "說明"]}`

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"發言日期"` | string | 發言日期 |
| `"發言時間"` | string | 發言時間 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"主旨"` | string | 主旨 |
| `"符合條款"` | string | 符合條款 |
| `"事實發生日"` | string | 事實發生日 |
| `"說明"` | string | 說明 |

## TPEx-158 · 券商業務別人員數

- **方法／URL**：[GET /mopsfin_t187ap01](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap01)
- **官方 tags**：券商資料
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：券商人員數等營運資料，與每日選股沒有已驗證直接關係。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"職位"` | string | 職位 |
| `"受託買賣"` | string | 受託買賣 |
| `"受託買賣（衍生性商品銷售）"` | string | 受託買賣（衍生性商品銷售） |
| `"內部稽核"` | string | 內部稽核 |
| `"融資融券"` | string | 融資融券 |
| `"證券借貸"` | string | 證券借貸 |
| `"自行買賣"` | string | 自行買賣 |
| `"其他人員"` | string | 其他人員 |
| `"結算交割"` | string | 結算交割 |
| `"股務人員"` | string | 股務人員 |
| `"承銷人員"` | string | 承銷人員 |
| `"法令遵循"` | string | 法令遵循 |
| `"風險管理-模型管理"` | string | 風險管理-模型管理 |
| `"驗證人員-模型管理"` | string | 驗證人員-模型管理 |
| `"內部稽核-模型管理"` | string | 內部稽核-模型管理 |
| `"共同行銷"` | string | 共同行銷 |
| `"合作推廣"` | string | 合作推廣 |
| `"開戶"` | string | 開戶 |
| `"徵信"` | string | 徵信 |
| `"營業櫃檯輸單"` | string | 營業櫃檯輸單 |
| `"主辦會計"` | string | 主辦會計 |
| `"財富管理"` | string | 財富管理 |
| `"風險管理-其他"` | string | 風險管理-其他 |
| `"公司治理人員"` | string | 公司治理人員 |
| `"受託管理私募股權基金人員"` | string | 受託管理私募股權基金人員 |
| `"基金買賣及互易"` | string | 基金買賣及互易 |
| `"數位服務（數位體驗專區）"` | string | 數位服務（數位體驗專區） |
| `"數位服務（客戶服務中心）"` | string | 數位服務（客戶服務中心） |
| `"合計"` | string | 合計 |

## TPEx-159 · 上櫃公司持股逾 10% 大股東名單

- **方法／URL**：[GET /mopsfin_t187ap02_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap02_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"大股東名稱"` | string | 大股東名稱 |

## TPEx-160 · 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司

- **方法／URL**：[GET /mopsfin_t187ap26_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap26_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D24、D37、D42
- **用途**：經營權變動、裁罰與資訊申報違規，作公司事件風險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"停止買賣開始日"` | string | 停止買賣開始日 |

## TPEx-161 · 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司

- **方法／URL**：[GET /mopsfin_t187ap27_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap27_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D24、D37、D42
- **用途**：經營權變動、裁罰與資訊申報違規，作公司事件風險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"變更交易開始日"` | string | 變更交易開始日 |

## TPEx-162 · 上櫃公司每月營業收入彙總表

- **方法／URL**：[GET /mopsfin_t187ap05_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D19、D50
- **用途**：月營收年增、累計與加速度，保留各次發布快照。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；代表實測 HTTP 200
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

**代表探測證據**：`{"http_status": 200, "rows": 892, "actual_shape": "list", "fetched_at": "2026-10-09T06:26:00.077597+00:00", "sha256": "f00e3fdd7060db0db943b79dc53d732df940d038ef208a1b075363e06660bd92", "date_ranges": {"出表日期": ["1150917"], "資料年月": ["11508"]}, "observed_fields": ["出表日期", "資料年月", "公司代號", "公司名稱", "產業別", "營業收入-當月營收", "營業收入-上月營收", "營業收入-去年當月營收", "營業收入-上月比較增減(%)", "營業收入-去年同月增減(%)", "累計營業收入-當月累計營收", "累計營業收入-去年累計營收", "累計營業收入-前期比較增減(%)", "備註"]}`

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"資料年月"` | string | 資料年月 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"產業別"` | string | 產業別 |
| `"營業收入-當月營收"` | string | 營業收入-當月營收 |
| `"營業收入-上月營收"` | string | 營業收入-上月營收 |
| `"營業收入-去年當月營收"` | string | 營業收入-去年當月營收 |
| `"營業收入-上月比較增減(%)"` | string | 營業收入-上月比較增減(%) |
| `"營業收入-去年同月增減(%)"` | string | 營業收入-去年同月增減(%) |
| `"累計營業收入-當月累計營收"` | string | 累計營業收入-當月累計營收 |
| `"累計營業收入-去年累計營收"` | string | 累計營業收入-去年累計營收 |
| `"累計營業收入-前期比較增減(%)"` | string | 累計營業收入-前期比較增減(%) |
| `"備註"` | string | 備註 |

## TPEx-163 · 上櫃股利分派情形-董事會通過

- **方法／URL**：[GET /mopsfin_t187ap39_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap39_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：競賽與交易狀態／P0
- **可支持需求**：D05、D39
- **用途**：董事會通過股利分派，與除權息預告／結果交叉核對。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"股利年度"` | string | 股利年度 |
| `"期別"` | string | 期別 |
| `"董事會決議通過股利分派日"` | string | 董事會決議通過股利分派日 |
| `"股東會日期配盈餘/待彌補虧損(元)"` | string | 股東會日期配盈餘/待彌補虧損(元) |
| `"期初未分配盈餘/待彌補虧損(元)"` | string | 期初未分配盈餘/待彌補虧損(元) |
| `"本期淨利(淨損)(元)"` | string | 本期淨利(淨損)(元) |
| `"可分配盈餘(元)"` | string | 可分配盈餘(元) |
| `"分配後期末未分配盈餘(元)"` | string | 分配後期末未分配盈餘(元) |
| `"股東配發內容-盈餘分配之現金股利(元/股)"` | string | 股東配發內容-盈餘分配之現金股利(元/股) |
| `"股東配發內容-法定盈餘公積、資本公積發放之現金(元/股)"` | string | 股東配發內容-法定盈餘公積、資本公積發放之現金(元/股) |
| `"股東配發內容-股東配發之現金(股利)總金額(元)"` | string | 股東配發內容-股東配發之現金(股利)總金額(元) |
| `"股東配發內容-盈餘轉增資配股(元/股)"` | string | 股東配發內容-盈餘轉增資配股(元/股) |
| `"股東配發內容-法定盈餘公積、資本公積轉增資配股(元/股)"` | string | 股東配發內容-法定盈餘公積、資本公積轉增資配股(元/股) |
| `"股東配發內容-股東配股總股數(股)"` | string | 股東配發內容-股東配股總股數(股) |
| `"董監酬勞(元)"` | string | 董監酬勞(元) |
| `"員工紅利-現金紅利金額(元)H"` | string | 員工紅利-現金紅利金額(元)H |
| `"員工紅利-股票紅利金額(元)I"` | string | 員工紅利-股票紅利金額(元)I |
| `"有無全數分派員工股票紅利而股東未配發股票股利之情事"` | string | 有無全數分派員工股票紅利而股東未配發股票股利之情事 |
| `"摘錄公司章程-股利分派部分"` | string | 摘錄公司章程-股利分派部分 |
| `"備註"` | string | 備註 |
| `"普通股每股面額"` | string | 普通股每股面額 |

## TPEx-164 · 轉(交)換公司債買賣斷券商買賣日報表

- **方法／URL**：[GET /bond_cb_daily](https://www.tpex.org.tw/openapi/v1/bond_cb_daily)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 日期 |
| `"FinancialInstitutionsCode"` | string | 證商代號 |
| `"FinancialInstitutionsName"` | string | 名稱 |
| `"ParValueOfPurchase"` | string | 買進面額 |
| `"AmountOfPurchase"` | string | 買進金額 |
| `"ParValueOfSell"` | string | 賣出面額 |
| `"AmountOfSell"` | string | 賣出金額 |

## TPEx-165 · 上櫃公司資產負債表(金融業)

- **方法／URL**：[GET /mopsfin_t187ap07_O_basi](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_basi)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D22
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"現金及約當現金"` | string | 現金及約當現金 |
| `"存放央行及拆借銀行同業"` | string | 存放央行及拆借銀行同業 |
| `"透過損益按公允價值衡量之金融資產"` | string | 透過損益按公允價值衡量之金融資產 |
| `"透過其他綜合損益按公允價值衡量之金融資產"` | string | 透過其他綜合損益按公允價值衡量之金融資產 |
| `"按攤銷後成本衡量之債務工具投資"` | string | 按攤銷後成本衡量之債務工具投資 |
| `"避險之衍生金融資產淨額"` | string | 避險之衍生金融資產淨額 |
| `"附賣回票券及債券投資淨額"` | string | 附賣回票券及債券投資淨額 |
| `"應收款項－淨額"` | string | 應收款項－淨額 |
| `"當期所得稅資產"` | string | 當期所得稅資產 |
| `"待出售資產－淨額"` | string | 待出售資產－淨額 |
| `"待分配予業主之資產－淨額"` | string | 待分配予業主之資產－淨額 |
| `"貼現及放款－淨額"` | string | 貼現及放款－淨額 |
| `"採用權益法之投資－淨額"` | string | 採用權益法之投資－淨額 |
| `"受限制資產－淨額"` | string | 受限制資產－淨額 |
| `"其他金融資產－淨額"` | string | 其他金融資產－淨額 |
| `"保險合約資產"` | string | 保險合約資產 |
| `"再保險合約資產"` | string | 再保險合約資產 |
| `"不動產及設備－淨額"` | string | 不動產及設備－淨額 |
| `"使用權資產－淨額"` | string | 使用權資產－淨額 |
| `"投資性不動產投資－淨額"` | string | 投資性不動產投資－淨額 |
| `"無形資產－淨額"` | string | 無形資產－淨額 |
| `"遞延所得稅資產"` | string | 遞延所得稅資產 |
| `"其他資產－淨額"` | string | 其他資產－淨額 |
| `"資產總額"` | string | 資產總額 |
| `"央行及銀行同業存款"` | string | 央行及銀行同業存款 |
| `"央行及同業融資"` | string | 央行及同業融資 |
| `"透過損益按公允價值衡量之金融負債"` | string | 透過損益按公允價值衡量之金融負債 |
| `"避險之衍生金融負債－淨額"` | string | 避險之衍生金融負債－淨額 |
| `"附買回票券及債券負債"` | string | 附買回票券及債券負債 |
| `"應付款項"` | string | 應付款項 |
| `"當期所得稅負債"` | string | 當期所得稅負債 |
| `"與待出售資產直接相關之負債"` | string | 與待出售資產直接相關之負債 |
| `"存款及匯款"` | string | 存款及匯款 |
| `"應付金融債券"` | string | 應付金融債券 |
| `"應付公司債"` | string | 應付公司債 |
| `"特別股負債"` | string | 特別股負債 |
| `"其他金融負債"` | string | 其他金融負債 |
| `"負債準備"` | string | 負債準備 |
| `"保險合約負債"` | string | 保險合約負債 |
| `"再保險合約負債"` | string | 再保險合約負債 |
| `"租賃負債"` | string | 租賃負債 |
| `"遞延所得稅負債"` | string | 遞延所得稅負債 |
| `"其他負債"` | string | 其他負債 |
| `"負債總額"` | string | 負債總額 |
| `"股本"` | string | 股本 |
| `"權益─具證券性質之虛擬通貨"` | string | 權益─具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總額"` | string | 權益總額 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-166 · 上櫃公司資產負債表(證券期貨業)

- **方法／URL**：[GET /mopsfin_t187ap07_O_bd](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_bd)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D22
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"流動資產"` | string | 流動資產 |
| `"非流動資產"` | string | 非流動資產 |
| `"資產總計"` | string | 資產總計 |
| `"流動負債"` | string | 流動負債 |
| `"非流動負債"` | string | 非流動負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益－具證券性質之虛擬通貨"` | string | 權益－具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘（或累積虧損）"` | string | 保留盈餘（或累積虧損） |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主權益合計"` | string | 歸屬於母公司業主權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總計"` | string | 權益總計 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-167 · 上櫃公司資產負債表(一般業)

- **方法／URL**：[GET /mopsfin_t187ap07_O_ci](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_ci)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D22
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"流動資產"` | string | 流動資產 |
| `"非流動資產"` | string | 非流動資產 |
| `"資產總計"` | string | 資產總計 |
| `"流動負債"` | string | 流動負債 |
| `"非流動負債"` | string | 非流動負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益─具證券性質之虛擬通貨"` | string | 權益─具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總計"` | string | 權益總計 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-168 · 上櫃公司資產負債表(金控業)

- **方法／URL**：[GET /mopsfin_t187ap07_O_fh](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_fh)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D22
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"Season"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"現金及約當現金"` | string | 現金及約當現金 |
| `"存放央行及拆借金融同業"` | string | 存放央行及拆借金融同業 |
| `"透過損益按公允價值衡量之金融資產"` | string | 透過損益按公允價值衡量之金融資產 |
| `"透過其他綜合損益按公允價值衡量之金融資產"` | string | 透過其他綜合損益按公允價值衡量之金融資產 |
| `"按攤銷後成本衡量之債務工具投資"` | string | 按攤銷後成本衡量之債務工具投資 |
| `"避險之衍生金融資產"` | string | 避險之衍生金融資產 |
| `"附賣回票券及債券投資"` | string | 附賣回票券及債券投資 |
| `"應收款項－淨額"` | string | 應收款項－淨額 |
| `"當期所得稅資產"` | string | 當期所得稅資產 |
| `"待出售資產－淨額"` | string | 待出售資產－淨額 |
| `" "` | string |   |
| `"貼現及放款－淨額"` | string | 貼現及放款－淨額 |
| `"保險合約資產及再保險合約資產－淨額"` | string | 保險合約資產及再保險合約資產－淨額 |
| `"採用權益法之投資－淨額"` | string | 採用權益法之投資－淨額 |
| `"受限制資產－淨額"` | string | 受限制資產－淨額 |
| `"其他金融資產－淨額"` | string | 其他金融資產－淨額 |
| `"投資性不動產－淨額"` | string | 投資性不動產－淨額 |
| `"不動產及設備－淨額"` | string | 不動產及設備－淨額 |
| `"使用權資產－淨額"` | string | 使用權資產－淨額 |
| `"無形資產－淨額"` | string | 無形資產－淨額 |
| `"遞延所得稅資產"` | string | 遞延所得稅資產 |
| `"其他資產－淨額"` | string | 其他資產－淨額 |
| `"資產總額"` | string | 資產總額 |
| `"央行及金融同業存款"` | string | 央行及金融同業存款 |
| `"央行及同業融資"` | string | 央行及同業融資 |
| `"透過損益按公允價值衡量之金融負債"` | string | 透過損益按公允價值衡量之金融負債 |
| `"避險之衍生金融負債"` | string | 避險之衍生金融負債 |
| `"附買回票券及債券負債"` | string | 附買回票券及債券負債 |
| `"應付商業本票－淨額"` | string | 應付商業本票－淨額 |
| `"應付款項"` | string | 應付款項 |
| `"當期所得稅負債"` | string | 當期所得稅負債 |
| `"與待出售資產直接相關之負債"` | string | 與待出售資產直接相關之負債 |
| `"存款及匯款"` | string | 存款及匯款 |
| `"應付債券"` | string | 應付債券 |
| `"其他借款"` | string | 其他借款 |
| `"特別股負債"` | string | 特別股負債 |
| `"負債準備"` | string | 負債準備 |
| `"其他金融負債"` | string | 其他金融負債 |
| `"保險合約負債及再保險合約負債"` | string | 保險合約負債及再保險合約負債 |
| `"租賃負債"` | string | 租賃負債 |
| `"遞延所得稅負債"` | string | 遞延所得稅負債 |
| `"其他負債"` | string | 其他負債 |
| `"負債總額"` | string | 負債總額 |
| `"股本"` | string | 股本 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"歸屬於母公司業主之權益"` | string | 歸屬於母公司業主之權益 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總額"` | string | 權益總額 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-169 · 上櫃公司資產負債表(保險業)

- **方法／URL**：[GET /mopsfin_t187ap07_O_ins](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_ins)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D22
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `" "` | string |   |
| `"現金及約當現金"` | string | 現金及約當現金 |
| `"應收款項"` | string | 應收款項 |
| `"本期所得稅資產"` | string | 本期所得稅資產 |
| `"待出售資產"` | string | 待出售資產 |
| `"待分配予業主之資產（或處分群組）"` | string | 待分配予業主之資產（或處分群組） |
| `"透過損益按公允價值衡量之金融資產"` | string | 透過損益按公允價值衡量之金融資產 |
| `"透過其他綜合損益按公允價值衡量之金融資產"` | string | 透過其他綜合損益按公允價值衡量之金融資產 |
| `"按攤銷後成本衡量之金融資產"` | string | 按攤銷後成本衡量之金融資產 |
| `"避險之金融資產"` | string | 避險之金融資產 |
| `"採用權益法之投資－淨額"` | string | 採用權益法之投資－淨額 |
| `"其他金融資產－淨額"` | string | 其他金融資產－淨額 |
| `"投資性不動產"` | string | 投資性不動產 |
| `"放款"` | string | 放款 |
| `"保險合約資產"` | string | 保險合約資產 |
| `"再保險合約資產"` | string | 再保險合約資產 |
| `"不動產及設備"` | string | 不動產及設備 |
| `"使用權資產"` | string | 使用權資產 |
| `"無形資產"` | string | 無形資產 |
| `"遞延所得稅資產"` | string | 遞延所得稅資產 |
| `"其他資產"` | string | 其他資產 |
| `"分離帳戶保險商品資產"` | string | 分離帳戶保險商品資產 |
| `"資產總計"` | string | 資產總計 |
| `"短期債務"` | string | 短期債務 |
| `"應付款項"` | string | 應付款項 |
| `"本期所得稅負債"` | string | 本期所得稅負債 |
| `"與待出售資產直接相關之負債"` | string | 與待出售資產直接相關之負債 |
| `"透過損益按公允價值衡量之金融負債"` | string | 透過損益按公允價值衡量之金融負債 |
| `"避險之衍生金融負債"` | string | 避險之衍生金融負債 |
| `"應付債券"` | string | 應付債券 |
| `"特別股負債"` | string | 特別股負債 |
| `"其他金融負債"` | string | 其他金融負債 |
| `"租賃負債"` | string | 租賃負債 |
| `"負債準備"` | string | 負債準備 |
| `"遞延所得稅負債"` | string | 遞延所得稅負債 |
| `"其他負債"` | string | 其他負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益─具證券性質之虛擬通貨"` | string | 權益─具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總計"` | string | 權益總計 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-170 · 上櫃公司資產負債表(異業)

- **方法／URL**：[GET /mopsfin_t187ap07_O_mim](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_mim)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D22
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"流動資產"` | string | 流動資產 |
| `"非流動資產"` | string | 非流動資產 |
| `"資產總計"` | string | 資產總計 |
| `"流動負債"` | string | 流動負債 |
| `"非流動負債"` | string | 非流動負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益－具證券性質之虛擬通貨"` | string | 權益－具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總額"` | string | 權益總額 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-171 · 上櫃公司綜合損益表(金融業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_basi](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_basi)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"Season"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"利息淨收益"` | string | 利息淨收益 |
| `"利息以外淨損益"` | string | 利息以外淨損益 |
| `"呆帳費用、承諾及保證責任準備提存"` | string | 呆帳費用、承諾及保證責任準備提存 |
| `"營業費用"` | string | 營業費用 |
| `"繼續營業單位稅前淨利（淨損）"` | string | 繼續營業單位稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期稅後淨利（淨損）"` | string | 繼續營業單位本期稅後淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期稅後淨利（淨損）"` | string | 本期稅後淨利（淨損） |
| `"其他綜合損益（稅後）"` | string | 其他綜合損益（稅後） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額（稅後）"` | string | 本期綜合損益總額（稅後） |
| `"淨利（損）歸屬於母公司業主"` | string | 淨利（損）歸屬於母公司業主 |
| `"淨利（損）歸屬於共同控制下前手權益"` | string | 淨利（損）歸屬於共同控制下前手權益 |
| `"淨利（損）歸屬於非控制權益"` | string | 淨利（損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-172 · 上櫃公司綜合損益表(證券期貨業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_bd](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_bd)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"收益"` | string | 收益 |
| `"支出及費用"` | string | 支出及費用 |
| `"營業利益"` | string | 營業利益 |
| `"營業外損益"` | string | 營業外損益 |
| `"稅前淨利（淨損）"` | string | 稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"本期其他綜合損益（稅後淨額）"` | string | 本期其他綜合損益（稅後淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（損）歸屬於母公司業主"` | string | 淨利（損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（損）歸屬於非控制權益"` | string | 淨利（損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-173 · 上櫃公司綜合損益表(一般業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_ci](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_ci)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"Season"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"營業收入"` | string | 營業收入 |
| `"營業成本"` | string | 營業成本 |
| `"原始認列生物資產及農產品之利益（損失）"` | string | 原始認列生物資產及農產品之利益（損失） |
| `"生物資產當期公允價值減出售成本之變動利益（損失）"` | string | 生物資產當期公允價值減出售成本之變動利益（損失） |
| `"營業毛利（毛損）"` | string | 營業毛利（毛損） |
| `"未實現銷貨（損）益"` | string | 未實現銷貨（損）益 |
| `"已實現銷貨（損）益"` | string | 已實現銷貨（損）益 |
| `"營業毛利（毛損）淨額"` | string | 營業毛利（毛損）淨額 |
| `"營業費用"` | string | 營業費用 |
| `"其他收益及費損淨額"` | string | 其他收益及費損淨額 |
| `"營業利益（損失）"` | string | 營業利益（損失） |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"稅前淨利（淨損）"` | string | 稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益（淨額）"` | string | 其他綜合損益（淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-174 · 上櫃公司綜合損益表(金控業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_fh](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_fh)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"利息淨收益"` | string | 利息淨收益 |
| `"利息以外淨收益"` | string | 利息以外淨收益 |
| `"淨收益"` | string | 淨收益 |
| `"呆帳費用、承諾及保證責任準備提存"` | string | 呆帳費用、承諾及保證責任準備提存 |
| `"保險其他營業成本"` | string | 保險其他營業成本 |
| `"營業費用"` | string | 營業費用 |
| `"繼續營業單位稅前損益"` | string | 繼續營業單位稅前損益 |
| `"所得稅（費用）利益"` | string | 所得稅（費用）利益 |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"本期稅後淨利（淨損）"` | string | 本期稅後淨利（淨損） |
| `"本期其他綜合損益（稅後淨額）"` | string | 本期其他綜合損益（稅後淨額） |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-175 · 上櫃公司綜合損益表(保險業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_ins](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_ins)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"Season"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"營業收入"` | string | 營業收入 |
| `"營業成本"` | string | 營業成本 |
| `"營業費用"` | string | 營業費用 |
| `"營業利益（損失）"` | string | 營業利益（損失） |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"繼續營業單位稅前純益（純損）"` | string | 繼續營業單位稅前純益（純損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期純益（純損）"` | string | 繼續營業單位本期純益（純損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益（稅後淨額）"` | string | 其他綜合損益（稅後淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-176 · 上櫃公司綜合損益表(異業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_mim](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_mim)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"Season"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"收入"` | string | 收入 |
| `"支出"` | string | 支出 |
| `"繼續營業單位稅前淨利（淨損）"` | string | 繼續營業單位稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益"` | string | 其他綜合損益 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-177 · 上櫃公司財報資訊(金融業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_basiA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_basiA)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"利息淨收益"` | string | 利息淨收益 |
| `"利息以外淨損益"` | string | 利息以外淨損益 |
| `"呆帳費用、承諾及保證責任準備提存"` | string | 呆帳費用、承諾及保證責任準備提存 |
| `"營業費用"` | string | 營業費用 |
| `"繼續營業單位稅前淨利（淨損）"` | string | 繼續營業單位稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期稅後淨利（淨損）"` | string | 繼續營業單位本期稅後淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期稅後淨利（淨損）"` | string | 本期稅後淨利（淨損） |
| `"其他綜合損益（稅後）"` | string | 其他綜合損益（稅後） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額（稅後）"` | string | 本期綜合損益總額（稅後） |
| `"淨利（損）歸屬於母公司業主"` | string | 淨利（損）歸屬於母公司業主 |
| `"淨利（損）歸屬於共同控制下前手權益"` | string | 淨利（損）歸屬於共同控制下前手權益 |
| `"淨利（損）歸屬於非控制權益"` | string | 淨利（損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-178 · 上櫃公司財報資訊(證券期貨業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_bdA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_bdA)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"收益"` | string | 收益 |
| `"支出及費用"` | string | 支出及費用 |
| `"營業利益"` | string | 營業利益 |
| `"營業外損益"` | string | 營業外損益 |
| `"稅前淨利（淨損）"` | string | 稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"本期其他綜合損益（稅後淨額）"` | string | 本期其他綜合損益（稅後淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（損）歸屬於母公司業主"` | string | 淨利（損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（損）歸屬於非控制權益"` | string | 淨利（損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-179 · 上櫃公司財報資訊( 一般業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_ciA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_ciA)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P1
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"營業收入"` | string | 營業收入 |
| `"營業成本"` | string | 營業成本 |
| `"原始認列生物資產及農產品之利益（損失）"` | string | 原始認列生物資產及農產品之利益（損失） |
| `"生物資產當期公允價值減出售成本之變動利益（損失）"` | string | 生物資產當期公允價值減出售成本之變動利益（損失） |
| `"營業毛利（毛損）"` | string | 營業毛利（毛損） |
| `"未實現銷貨（損）益"` | string | 未實現銷貨（損）益 |
| `"已實現銷貨（損）益"` | string | 已實現銷貨（損）益 |
| `"營業毛利（毛損）淨額"` | string | 營業毛利（毛損）淨額 |
| `"營業費用"` | string | 營業費用 |
| `"其他收益及費損淨額"` | string | 其他收益及費損淨額 |
| `"營業利益（損失）"` | string | 營業利益（損失） |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"稅前淨利（淨損）"` | string | 稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益（淨額）"` | string | 其他綜合損益（淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-180 · 上櫃公司財報資訊(金控業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_fhA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_fhA)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"利息淨收益"` | string | 利息淨收益 |
| `"利息以外淨收益"` | string | 利息以外淨收益 |
| `"淨收益"` | string | 淨收益 |
| `"呆帳費用、承諾及保證責任準備提存"` | string | 呆帳費用、承諾及保證責任準備提存 |
| `"保險其他營業成本"` | string | 保險其他營業成本 |
| `"營業費用"` | string | 營業費用 |
| `"繼續營業單位稅前損益"` | string | 繼續營業單位稅前損益 |
| `"所得稅（費用）利益"` | string | 所得稅（費用）利益 |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"本期稅後淨利（淨損）"` | string | 本期稅後淨利（淨損） |
| `"本期其他綜合損益（稅後淨額）"` | string | 本期其他綜合損益（稅後淨額） |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-181 · 上櫃公司財報資訊(保險業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_insA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_insA)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"營業收入"` | string | 營業收入 |
| `"營業成本"` | string | 營業成本 |
| `"營業費用"` | string | 營業費用 |
| `"營業利益（損失）"` | string | 營業利益（損失） |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"繼續營業單位稅前純益（純損）"` | string | 繼續營業單位稅前純益（純損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期純益（純損）"` | string | 繼續營業單位本期純益（純損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益（稅後淨額）"` | string | 其他綜合損益（稅後淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-182 · 上櫃公司財報資訊(異業)

- **方法／URL**：[GET /mopsfin_t187ap06_O_mimA](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_mimA)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D23
- **用途**：財務報表按一般業／金融／金控／證券／保險／異業分別處理；年季及出表日期不等於歷史公告可用時點。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"收入"` | string | 收入 |
| `"支出"` | string | 支出 |
| `"繼續營業單位稅前淨利（淨損）"` | string | 繼續營業單位稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益"` | string | 其他綜合損益 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-183 · 興櫃公司資產負債表-證券期貨業

- **方法／URL**：[GET /mopsfin_t187ap07_U_bd](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_U_bd)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"流動資產"` | string | 流動資產 |
| `"非流動資產"` | string | 非流動資產 |
| `"資產總計"` | string | 資產總計 |
| `"流動負債"` | string | 流動負債 |
| `"非流動負債"` | string | 非流動負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益－具證券性質之虛擬通貨"` | string | 權益－具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘（或累積虧損）"` | string | 保留盈餘（或累積虧損） |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主權益合計"` | string | 歸屬於母公司業主權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總計"` | string | 權益總計 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-184 · 興櫃公司資產負債表-一般業

- **方法／URL**：[GET /mopsfin_t187ap07_U_ci](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_U_ci)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"流動資產"` | string | 流動資產 |
| `"非流動資產"` | string | 非流動資產 |
| `"資產總計"` | string | 資產總計 |
| `"流動負債"` | string | 流動負債 |
| `"非流動負債"` | string | 非流動負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益─具證券性質之虛擬通貨"` | string | 權益─具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總計"` | string | 權益總計 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-185 · 興櫃公司資產負債表-金控業

- **方法／URL**：[GET /mopsfin_t187ap07_U_fh](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_U_fh)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"現金及約當現金"` | string | 現金及約當現金 |
| `"存放央行及拆借金融同業"` | string | 存放央行及拆借金融同業 |
| `"透過損益按公允價值衡量之金融資產"` | string | 透過損益按公允價值衡量之金融資產 |
| `"透過其他綜合損益按公允價值衡量之金融資產"` | string | 透過其他綜合損益按公允價值衡量之金融資產 |
| `"按攤銷後成本衡量之債務工具投資"` | string | 按攤銷後成本衡量之債務工具投資 |
| `"避險之衍生金融資產"` | string | 避險之衍生金融資產 |
| `"附賣回票券及債券投資"` | string | 附賣回票券及債券投資 |
| `"應收款項－淨額"` | string | 應收款項－淨額 |
| `"當期所得稅資產"` | string | 當期所得稅資產 |
| `"待出售資產－淨額"` | string | 待出售資產－淨額 |
| `" "` | string |   |
| `"貼現及放款－淨額"` | string | 貼現及放款－淨額 |
| `"保險合約資產及再保險合約資產－淨額"` | string | 保險合約資產及再保險合約資產－淨額 |
| `"採用權益法之投資－淨額"` | string | 採用權益法之投資－淨額 |
| `"受限制資產－淨額"` | string | 受限制資產－淨額 |
| `"其他金融資產－淨額"` | string | 其他金融資產－淨額 |
| `"投資性不動產－淨額"` | string | 投資性不動產－淨額 |
| `"不動產及設備－淨額"` | string | 不動產及設備－淨額 |
| `"使用權資產－淨額"` | string | 使用權資產－淨額 |
| `"無形資產－淨額"` | string | 無形資產－淨額 |
| `"遞延所得稅資產"` | string | 遞延所得稅資產 |
| `"其他資產－淨額"` | string | 其他資產－淨額 |
| `"資產總額"` | string | 資產總額 |
| `"央行及金融同業存款"` | string | 央行及金融同業存款 |
| `"央行及同業融資"` | string | 央行及同業融資 |
| `"透過損益按公允價值衡量之金融負債"` | string | 透過損益按公允價值衡量之金融負債 |
| `"避險之衍生金融負債"` | string | 避險之衍生金融負債 |
| `"附買回票券及債券負債"` | string | 附買回票券及債券負債 |
| `"應付商業本票－淨額"` | string | 應付商業本票－淨額 |
| `"應付款項"` | string | 應付款項 |
| `"當期所得稅負債"` | string | 當期所得稅負債 |
| `"與待出售資產直接相關之負債"` | string | 與待出售資產直接相關之負債 |
| `"存款及匯款"` | string | 存款及匯款 |
| `"應付債券"` | string | 應付債券 |
| `"其他借款"` | string | 其他借款 |
| `"特別股負債"` | string | 特別股負債 |
| `"負債準備"` | string | 負債準備 |
| `"其他金融負債"` | string | 其他金融負債 |
| `"保險合約負債及再保險合約負債"` | string | 保險合約負債及再保險合約負債 |
| `"租賃負債"` | string | 租賃負債 |
| `"遞延所得稅負債"` | string | 遞延所得稅負債 |
| `"其他負債"` | string | 其他負債 |
| `"負債總額"` | string | 負債總額 |
| `"股本"` | string | 股本 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"歸屬於母公司業主之權益"` | string | 歸屬於母公司業主之權益 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總額"` | string | 權益總額 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-186 · 興櫃公司資產負債表-保險業

- **方法／URL**：[GET /mopsfin_t187ap07_U_ins](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_U_ins)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `" "` | string |   |
| `"現金及約當現金"` | string | 現金及約當現金 |
| `"應收款項"` | string | 應收款項 |
| `"本期所得稅資產"` | string | 本期所得稅資產 |
| `"待出售資產"` | string | 待出售資產 |
| `"待分配予業主之資產（或處分群組）"` | string | 待分配予業主之資產（或處分群組） |
| `"透過損益按公允價值衡量之金融資產"` | string | 透過損益按公允價值衡量之金融資產 |
| `"透過其他綜合損益按公允價值衡量之金融資產"` | string | 透過其他綜合損益按公允價值衡量之金融資產 |
| `"按攤銷後成本衡量之金融資產"` | string | 按攤銷後成本衡量之金融資產 |
| `"避險之金融資產"` | string | 避險之金融資產 |
| `"採用權益法之投資－淨額"` | string | 採用權益法之投資－淨額 |
| `"其他金融資產－淨額"` | string | 其他金融資產－淨額 |
| `"投資性不動產"` | string | 投資性不動產 |
| `"放款"` | string | 放款 |
| `"保險合約資產"` | string | 保險合約資產 |
| `"再保險合約資產"` | string | 再保險合約資產 |
| `"不動產及設備"` | string | 不動產及設備 |
| `"使用權資產"` | string | 使用權資產 |
| `"無形資產"` | string | 無形資產 |
| `"遞延所得稅資產"` | string | 遞延所得稅資產 |
| `"其他資產"` | string | 其他資產 |
| `"分離帳戶保險商品資產"` | string | 分離帳戶保險商品資產 |
| `"資產總計"` | string | 資產總計 |
| `"短期債務"` | string | 短期債務 |
| `"應付款項"` | string | 應付款項 |
| `"本期所得稅負債"` | string | 本期所得稅負債 |
| `"與待出售資產直接相關之負債"` | string | 與待出售資產直接相關之負債 |
| `"透過損益按公允價值衡量之金融負債"` | string | 透過損益按公允價值衡量之金融負債 |
| `"避險之衍生金融負債"` | string | 避險之衍生金融負債 |
| `"應付債券"` | string | 應付債券 |
| `"特別股負債"` | string | 特別股負債 |
| `"其他金融負債"` | string | 其他金融負債 |
| `"負債準備"` | string | 負債準備 |
| `"租賃負債"` | string | 租賃負債 |
| `"遞延所得稅負債"` | string | 遞延所得稅負債 |
| `"其他負債"` | string | 其他負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益─具證券性質之虛擬通貨"` | string | 權益─具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"非控制權益"` | string | 非控制權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"權益總計"` | string | 權益總計 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-187 · 興櫃公司資產負債表-異業

- **方法／URL**：[GET /mopsfin_t187ap07_U_mim](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_U_mim)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"流動資產"` | string | 流動資產 |
| `"非流動資產"` | string | 非流動資產 |
| `"資產總計"` | string | 資產總計 |
| `"流動負債"` | string | 流動負債 |
| `"非流動負債"` | string | 非流動負債 |
| `"負債總計"` | string | 負債總計 |
| `"股本"` | string | 股本 |
| `"權益－具證券性質之虛擬通貨"` | string | 權益－具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總額"` | string | 權益總額 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-188 · 興櫃公司綜合損益表-金融業

- **方法／URL**：[GET /mopsfin_t187ap06_U_basi](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_U_basi)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"利息淨收益"` | string | 利息淨收益 |
| `"利息以外淨損益"` | string | 利息以外淨損益 |
| `"呆帳費用、承諾及保證責任準備提存"` | string | 呆帳費用、承諾及保證責任準備提存 |
| `"營業費用"` | string | 營業費用 |
| `"繼續營業單位稅前淨利（淨損）"` | string | 繼續營業單位稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期稅後淨利（淨損）"` | string | 繼續營業單位本期稅後淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期稅後淨利（淨損）"` | string | 本期稅後淨利（淨損） |
| `"其他綜合損益（稅後）"` | string | 其他綜合損益（稅後） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額（稅後）"` | string | 本期綜合損益總額（稅後） |
| `"淨利（損）歸屬於母公司業主"` | string | 淨利（損）歸屬於母公司業主 |
| `"淨利（損）歸屬於共同控制下前手權益"` | string | 淨利（損）歸屬於共同控制下前手權益 |
| `"淨利（損）歸屬於非控制權益"` | string | 淨利（損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-189 · 興櫃公司綜合損益表-證券期貨業

- **方法／URL**：[GET /mopsfin_t187ap06_U_bd](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_U_bd)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"收益"` | string | 收益 |
| `"支出及費用"` | string | 支出及費用 |
| `"營業利益"` | string | 營業利益 |
| `"營業外損益"` | string | 營業外損益 |
| `"稅前淨利（淨損）"` | string | 稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"本期其他綜合損益（稅後淨額）"` | string | 本期其他綜合損益（稅後淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（損）歸屬於母公司業主"` | string | 淨利（損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（損）歸屬於非控制權益"` | string | 淨利（損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-190 · 興櫃公司綜合損益表-一般業

- **方法／URL**：[GET /mopsfin_t187ap06_U_ci](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_U_ci)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"營業收入"` | string | 營業收入 |
| `"營業成本"` | string | 營業成本 |
| `"原始認列生物資產及農產品之利益（損失）"` | string | 原始認列生物資產及農產品之利益（損失） |
| `"生物資產當期公允價值減出售成本之變動利益（損失）"` | string | 生物資產當期公允價值減出售成本之變動利益（損失） |
| `"營業毛利（毛損）"` | string | 營業毛利（毛損） |
| `"未實現銷貨（損）益"` | string | 未實現銷貨（損）益 |
| `"已實現銷貨（損）益"` | string | 已實現銷貨（損）益 |
| `"營業毛利（毛損）淨額"` | string | 營業毛利（毛損）淨額 |
| `"營業費用"` | string | 營業費用 |
| `"其他收益及費損淨額"` | string | 其他收益及費損淨額 |
| `"營業利益（損失）"` | string | 營業利益（損失） |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"稅前淨利（淨損）"` | string | 稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益（淨額）"` | string | 其他綜合損益（淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-191 · 興櫃公司綜合損益表-金控業

- **方法／URL**：[GET /mopsfin_t187ap06_U_fh](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_U_fh)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"利息淨收益"` | string | 利息淨收益 |
| `"利息以外淨收益"` | string | 利息以外淨收益 |
| `"淨收益"` | string | 淨收益 |
| `"呆帳費用、承諾及保證責任準備提存"` | string | 呆帳費用、承諾及保證責任準備提存 |
| `"保險其他營業成本"` | string | 保險其他營業成本 |
| `"營業費用"` | string | 營業費用 |
| `"繼續營業單位稅前損益"` | string | 繼續營業單位稅前損益 |
| `"所得稅（費用）利益"` | string | 所得稅（費用）利益 |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"本期稅後淨利（淨損）"` | string | 本期稅後淨利（淨損） |
| `"本期其他綜合損益（稅後淨額）"` | string | 本期其他綜合損益（稅後淨額） |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-192 · 興櫃公司綜合損益表-保險業

- **方法／URL**：[GET /mopsfin_t187ap06_U_ins](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_U_ins)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"營業收入"` | string | 營業收入 |
| `"營業成本"` | string | 營業成本 |
| `"營業費用"` | string | 營業費用 |
| `"營業利益（損失）"` | string | 營業利益（損失） |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"繼續營業單位稅前純益（純損）"` | string | 繼續營業單位稅前純益（純損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期純益（純損）"` | string | 繼續營業單位本期純益（純損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"合併前非屬共同控制股權損益"` | string | 合併前非屬共同控制股權損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益（稅後淨額）"` | string | 其他綜合損益（稅後淨額） |
| `"合併前非屬共同控制股權綜合損益淨額"` | string | 合併前非屬共同控制股權綜合損益淨額 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-193 · 興櫃公司綜合損益表-異業

- **方法／URL**：[GET /mopsfin_t187ap06_U_mim](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_U_mim)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"收入"` | string | 收入 |
| `"支出"` | string | 支出 |
| `"繼續營業單位稅前淨利（淨損）"` | string | 繼續營業單位稅前淨利（淨損） |
| `"所得稅費用（利益）"` | string | 所得稅費用（利益） |
| `"繼續營業單位本期淨利（淨損）"` | string | 繼續營業單位本期淨利（淨損） |
| `"停業單位損益"` | string | 停業單位損益 |
| `"本期淨利（淨損）"` | string | 本期淨利（淨損） |
| `"其他綜合損益"` | string | 其他綜合損益 |
| `"本期綜合損益總額"` | string | 本期綜合損益總額 |
| `"淨利（淨損）歸屬於母公司業主"` | string | 淨利（淨損）歸屬於母公司業主 |
| `"淨利（淨損）歸屬於共同控制下前手權益"` | string | 淨利（淨損）歸屬於共同控制下前手權益 |
| `"淨利（淨損）歸屬於非控制權益"` | string | 淨利（淨損）歸屬於非控制權益 |
| `"綜合損益總額歸屬於母公司業主"` | string | 綜合損益總額歸屬於母公司業主 |
| `"綜合損益總額歸屬於共同控制下前手權益"` | string | 綜合損益總額歸屬於共同控制下前手權益 |
| `"綜合損益總額歸屬於非控制權益"` | string | 綜合損益總額歸屬於非控制權益 |
| `"基本每股盈餘（元）"` | string | 基本每股盈餘（元） |

## TPEx-194 · 興櫃公司資產負債表-金融業

- **方法／URL**：[GET /mopsfin_t187ap07_U_basi](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_U_basi)
- **官方 tags**：財務報表
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"年度"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"現金及約當現金"` | string | 現金及約當現金 |
| `"存放央行及拆借銀行同業"` | string | 存放央行及拆借銀行同業 |
| `"透過損益按公允價值衡量之金融資產"` | string | 透過損益按公允價值衡量之金融資產 |
| `"透過其他綜合損益按公允價值衡量之金融資產"` | string | 透過其他綜合損益按公允價值衡量之金融資產 |
| `"按攤銷後成本衡量之債務工具投資"` | string | 按攤銷後成本衡量之債務工具投資 |
| `"避險之衍生金融資產淨額"` | string | 避險之衍生金融資產淨額 |
| `"附賣回票券及債券投資淨額"` | string | 附賣回票券及債券投資淨額 |
| `"應收款項－淨額"` | string | 應收款項－淨額 |
| `"當期所得稅資產"` | string | 當期所得稅資產 |
| `"待出售資產－淨額"` | string | 待出售資產－淨額 |
| `"待分配予業主之資產－淨額"` | string | 待分配予業主之資產－淨額 |
| `"貼現及放款－淨額"` | string | 貼現及放款－淨額 |
| `"採用權益法之投資－淨額"` | string | 採用權益法之投資－淨額 |
| `"受限制資產－淨額"` | string | 受限制資產－淨額 |
| `"其他金融資產－淨額"` | string | 其他金融資產－淨額 |
| `"保險合約資產"` | string | 保險合約資產 |
| `"再保險合約資產"` | string | 再保險合約資產 |
| `"不動產及設備－淨額"` | string | 不動產及設備－淨額 |
| `"使用權資產－淨額"` | string | 使用權資產－淨額 |
| `"投資性不動產投資－淨額"` | string | 投資性不動產投資－淨額 |
| `"無形資產－淨額"` | string | 無形資產－淨額 |
| `"遞延所得稅資產"` | string | 遞延所得稅資產 |
| `"其他資產－淨額"` | string | 其他資產－淨額 |
| `"資產總額"` | string | 資產總額 |
| `"央行及銀行同業存款"` | string | 央行及銀行同業存款 |
| `"央行及同業融資"` | string | 央行及同業融資 |
| `"透過損益按公允價值衡量之金融負債"` | string | 透過損益按公允價值衡量之金融負債 |
| `"避險之衍生金融負債－淨額"` | string | 避險之衍生金融負債－淨額 |
| `"附買回票券及債券負債"` | string | 附買回票券及債券負債 |
| `"應付款項"` | string | 應付款項 |
| `"當期所得稅負債"` | string | 當期所得稅負債 |
| `"與待出售資產直接相關之負債"` | string | 與待出售資產直接相關之負債 |
| `"存款及匯款"` | string | 存款及匯款 |
| `"應付金融債券"` | string | 應付金融債券 |
| `"應付公司債"` | string | 應付公司債 |
| `"特別股負債"` | string | 特別股負債 |
| `"其他金融負債"` | string | 其他金融負債 |
| `"負債準備"` | string | 負債準備 |
| `"保險合約負債"` | string | 保險合約負債 |
| `"再保險合約負債"` | string | 再保險合約負債 |
| `"租賃負債"` | string | 租賃負債 |
| `"遞延所得稅負債"` | string | 遞延所得稅負債 |
| `"其他負債"` | string | 其他負債 |
| `"負債總額"` | string | 負債總額 |
| `"股本"` | string | 股本 |
| `"權益─具證券性質之虛擬通貨"` | string | 權益─具證券性質之虛擬通貨 |
| `"資本公積"` | string | 資本公積 |
| `"保留盈餘"` | string | 保留盈餘 |
| `"其他權益"` | string | 其他權益 |
| `"庫藏股票"` | string | 庫藏股票 |
| `"歸屬於母公司業主之權益合計"` | string | 歸屬於母公司業主之權益合計 |
| `"共同控制下前手權益"` | string | 共同控制下前手權益 |
| `"合併前非屬共同控制股權"` | string | 合併前非屬共同控制股權 |
| `"非控制權益"` | string | 非控制權益 |
| `"權益總額"` | string | 權益總額 |
| `"待註銷股本股數（單位：股）"` | string | 待註銷股本股數（單位：股） |
| `"母公司暨子公司所持有之母公司庫藏股股數（單位：股）"` | string | 母公司暨子公司所持有之母公司庫藏股股數（單位：股） |
| `"預收股款（權益項下）之約當發行股數（單位：股）"` | string | 預收股款（權益項下）之約當發行股數（單位：股） |
| `"每股參考淨值"` | string | 每股參考淨值 |

## TPEx-195 · 興櫃公司董監事持股餘額明細資料

- **方法／URL**：[GET /mopsfin_t187ap11_R](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap11_R)
- **官方 tags**：公司治理
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"資料年月"` | string | 資料年月 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"職稱"` | string | 職稱 |
| `"姓名"` | string | 姓名 |
| `"選任時持股"` | string | 選任時持股 |
| `"目前持股"` | string | 目前持股 |
| `"設質股數"` | string | 設質股數 |
| `"設質股數佔持股比例"` | string | 設質股數佔持股比例 |
| `"內部人關係人目前持股合計"` | string | 內部人關係人目前持股合計 |
| `"內部人關係人設質股數"` | string | 內部人關係人設質股數 |
| `"內部人關係人設質比例"` | string | 內部人關係人設質比例 |

## TPEx-196 · 上櫃公司各產業EPS統計資訊

- **方法／URL**：[GET /mopsfin_t187ap14_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap14_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D40、D41
- **用途**：公司／產業 EPS 及財測達成與差異，樣本數、有效期及實際發布時點須另核。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"產業別"` | string | 產業別 |
| `"基本每股盈餘"` | string | 基本每股盈餘(元) |
| `"普通股每股面額"` | string | 普通股每股面額 |
| `"營業收入"` | string | 營業收入 |
| `"營業利益"` | string | 營業利益 |
| `"營業外收入及支出"` | string | 營業外收入及支出 |
| `"稅後淨利"` | string | 稅後淨利 |

## TPEx-197 · 上櫃公司截至各季綜合損益財測達成情形(簡式)

- **方法／URL**：[GET /mopsfin_t187ap15_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap15_O)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D40、D41
- **用途**：公司／產業 EPS 及財測達成與差異，樣本數、有效期及實際發布時點須另核。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"財測序號"` | string | 財測序號 |
| `"涵蓋期間"` | string | 涵蓋期間 |
| `"截至第1季經會計師查核或核閱數"` | string | 截至第1季經會計師查核或核閱數 |
| `"截至第1季稅前損益預測數"` | string | 截至第1季稅前損益預測數 |

## TPEx-198 · 上櫃公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式)

- **方法／URL**：[GET /mopsfin_t187ap16_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap16_O)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D40、D41
- **用途**：公司／產業 EPS 及財測達成與差異，樣本數、有效期及實際發布時點須另核。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"財測序號"` | string | 財測序號 |
| `"涵蓋期間"` | string | 涵蓋期間 |
| `"經會計師查核或核閱數第4季"` | string | 經會計師查核或核閱數第4季 |
| `"經會計師查核或核閱數截至第4季"` | string | 經會計師查核或核閱數截至第4季 |
| `"稅前綜合損益預測數第4季"` | string | 稅前(綜合)損益預測數第4季 |
| `"稅前綜合損益預測數截至第4季"` | string | 稅前(綜合)損益預測數截至第4季 |

## TPEx-199 · 上櫃公司營益分析查詢彙總表(全體公司彙總報表)

- **方法／URL**：[GET /mopsfin_187ap17_O](https://www.tpex.org.tw/openapi/v1/mopsfin_187ap17_O)
- **官方 tags**：財務報表
- **決策分類／優先序**：基本面與估值／P2
- **可支持需求**：D20、D40、D41
- **用途**：公司／產業 EPS 及財測達成與差異，樣本數、有效期及實際發布時點須另核。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"Year"` | string | 年度 |
| `"季別"` | string | 季別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"營業收入百萬元"` | string | 營業收入(百萬元) |
| `"毛利率"` | string | 毛利率(%)(營業毛利)/(營業收入) |
| `"營業利益率"` | string | 營業利益率(%)(營業利益)/(營業收入) |
| `"稅前純益率"` | string | 稅前純益率(%)(稅前純益)/(營業收入) |
| `"稅後純益率"` | string | 稅後純益率(%)(稅後純益)/(營業收入) |

## TPEx-200 · 上櫃公司董事、監察人持股不足法定成數彙總表

- **方法／URL**：[GET /mopsfin_t187ap08_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap08_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"已發行股份總額"` | string | 已發行股份總額 |
| `"全體董事不包含獨立董事應持有股數"` | string | 全 體 董 事(不包含獨立董事)-應持有股數 |
| `"全體董事不包含獨立董事本人實際持有股數"` | string | 全 體 董 事(不包含獨立董事)-本人實際持有股數 |
| `"全體董事不包含獨立董事法人代表人分戶集保股數"` | string | 全 體 董 事(不包含獨立董事)-法人代表人分戶集保股數 |
| `"全體董事不包含獨立董事保留運用決定權信託股數"` | string | 全 體 董 事(不包含獨立董事)-保留運用決定權信託股數 |
| `"全體董事不包含獨立董事不足股數"` | string | 全 體 董 事(不包含獨立董事)-不足股數 |
| `"全體監察人應持有股數"` | string | 全 體 監 察 人-應持有股數 |
| `"全體監察人本人實際持有股數"` | string | 全 體 監 察 人-本人實際持有股數 |
| `"全體監察人法人代表人分戶集保股數"` | string | 全 體 監 察 人-法人代表人分戶集保股數 |
| `"全體監察人保留運用決定權信託股數"` | string | 全 體 監 察 人-保留運用決定權信託股數 |
| `"全體監察人不足股數"` | string | 全 體 監 察 人-不足股數 |
| `"持股不足已通知其董監"` | string | 持股不足已通知其董監 |

## TPEx-201 · 上櫃公司董監事持股餘額明細資料

- **方法／URL**：[GET /mopsfin_t187ap11_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap11_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"資料年月"` | string | 資料年月 |
| `"公司代號"` | string | 公司代號 |
| `"公司名稱"` | string | 公司名稱 |
| `"職稱"` | string | 職稱 |
| `"姓名"` | string | 姓名 |
| `"選任時持股"` | string | 選任時持股 |
| `"目前持股"` | string | 目前持股 |
| `"設質股數"` | string | 設質股數 |
| `"設質股數佔持股比例"` | string | 設質股數佔持股比例 |
| `"內部人關係人目前持股合計"` | string | 內部人關係人目前持股合計 |
| `"內部人關係人設質股數"` | string | 內部人關係人設質股數 |
| `"內部人關係人設質比例"` | string | 內部人關係人設質比例 |

## TPEx-202 · 上櫃公司每日內部人持股轉讓事前申報表-持股轉讓日報表

- **方法／URL**：[GET /mopsfin_t187ap12_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap12_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"申請人身分"` | string | 申請人身分 |
| `"姓名"` | string | 姓名 |
| `"預定轉讓方式及股數-轉讓方式"` | string | 預定轉讓方式及股數-轉讓方式 |
| `"預定轉讓方式及股數-轉讓股數"` | string | 預定轉讓方式及股數-轉讓股數 |
| `"每日於盤中交易最大得轉讓股數"` | string | 每日於盤中交易最大得轉讓股數 |
| `"受讓人"` | string | 受讓人 |
| `"目前持有股數-自有持股"` | string | 目前持有股數-自有持股 |
| `"目前持有股數-保留運用決定權信託股數"` | string | 目前持有股數-保留運用決定權信託股數 |
| `"預定轉讓總股數-自有持股"` | string | 預定轉讓總股數-自有持股 |
| `"預定轉讓總股數-保留運用決定權信託股數"` | string | 預定轉讓總股數-保留運用決定權信託股數 |
| `"預定轉讓後持股-自有持股"` | string | 預定轉讓後持股-自有持股 |
| `"預定轉讓後持股-保留運用決定權信託股數"` | string | 預定轉讓後持股-保留運用決定權信託股數 |
| `"有效轉讓期間"` | string | 有效轉讓期間 |

## TPEx-203 · 上櫃公司每日內部人持股轉讓事前申報表-持股未轉讓日報表

- **方法／URL**：[GET /mopsfin_t187ap13_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap13_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：籌碼與持有人／P2
- **可支持需求**：D29、D24
- **用途**：董監事、大股東持股、質押及事前轉讓申報；申報與實際轉讓不同。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"申請人身分"` | string | 申請人身分 |
| `"姓名"` | string | 姓名 |
| `"未轉讓股數自有持股"` | string | 未轉讓股數-自有持股 |
| `"未轉讓股數保留運用決定權信託股數"` | string | 未轉讓股數-保留運用決定權信託股數 |
| `"目前持股自有持股"` | string | 目前持股-自有持股 |
| `"目前持股保留運用決定權信託股數"` | string | 目前持股-保留運用決定權信託股數 |
| `"原申報預定轉讓股數自有持股"` | string | 原申報預定轉讓股數-自有持股 |
| `"原申報預定轉讓股數保留運用決定權信託股數"` | string | 原申報預定轉讓股數-保留運用決定權信託股數 |
| `"未轉讓理由"` | string | 未轉讓理由 |

## TPEx-204 · 上櫃公司金管會證券期貨局裁罰案件專區

- **方法／URL**：[GET /mopsfin_t187ap22_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap22_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D24、D37、D42
- **用途**：經營權變動、裁罰與資訊申報違規，作公司事件風險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"發函日期"` | string | 發函日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"違規事由"` | string | 違規事由 |
| `"違反法規"` | string | 違反法規 |
| `"裁處情形"` | string | 裁處情形 |

## TPEx-205 · 上櫃公司獨立董監事兼任情形彙總表

- **方法／URL**：[GET /mopsfin_t187ap30_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap30_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"序號"` | string | 序號 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"職稱"` | string | 職稱 |
| `"Name"` | string | 姓名 |
| `"就任日期"` | string | 就任日期 |
| `"主要現職"` | string | 主要現職 |
| `"主要經歷"` | string | 主要經歷 |
| `"目前兼任其他公司名稱"` | string | 目前兼任其他公司名稱 |
| `"其他公司職稱"` | string | 其他公司職稱 |
| `"備註"` | string | 備註 |

## TPEx-206 · 上櫃公司董事酬金相關資訊

- **方法／URL**：[GET /mopsfin_t187ap29_A_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap29_A_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"產業類別"` | string | 產業類別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"董事酬金108年支付"` | string | 董事酬金-108年支付 |
| `"董事酬金109年支付"` | string | 董事酬金-109年支付 |
| `"董事酬金合計"` | string | 董事酬金-合計 |
| `"董事酬金加計兼任員工酬金108年支付"` | string | 董事酬金加計兼任員工酬金-108年支付 |
| `"董事酬金加計兼任員工酬金109年支付"` | string | 董事酬金加計兼任員工酬金-109年支付 |
| `"加計兼任員工酬金合計"` | string | 加計兼任員工酬金-合計 |
| `"酬金總額占稅後損益百分比董事酬金"` | string | 酬金總額占稅後損益百分比(%)-董事酬金 |
| `"酬金總額占稅後損益百分比加計兼任員工酬金"` | string | 酬金總額占稅後損益百分比(%)-加計兼任員工酬金 |
| `"平均每位董事酬金董事酬金"` | string | 平均每位董事酬金-董事酬金 |
| `"平均每位董事酬金加計兼任員工酬金"` | string | 平均每位董事酬金-加計兼任員工酬金 |
| `"領取來自子公司以外轉投資事業或母公司酬金"` | string | 領取來自子公司以外轉投資事業或母公司酬金 |
| `"稅後純益"` | string | 稅後純益 |
| `"每股盈餘"` | string | 每股盈餘 |
| `"股東權益報酬率"` | string | 股東權益報酬率(%) |
| `"實收資本額"` | string | 實收資本額(仟元) |
| `"稅後損益與董監酬金變動之關聯性與合理性說明"` | string | 稅後損益與董監酬金變動之關聯性與合理性說明 |

## TPEx-207 · 上櫃公司監察人酬金相關資訊

- **方法／URL**：[GET /mopsfin_t187ap29_B_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap29_B_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"產業類別"` | string | 產業類別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"監察人酬金108年支付"` | string | 監察人酬金-108年支付 |
| `"監察人酬金109年支付"` | string | 監察人酬金-109年支付 |
| `"監察人酬金合計"` | string | 監察人酬金-合計 |
| `"酬金總額占稅後損益百分比"` | string | 酬金總額占稅後損益百分比(%) |
| `"平均每位監察人酬金"` | string | 平均每位監察人酬金 |
| `"領取來自子公司以外轉投資事業或母公司酬金"` | string | 領取來自子公司以外轉投資事業或母公司酬金 |
| `"稅後純益"` | string | 稅後純益 |
| `"每股盈餘"` | string | 每股盈餘 |
| `"股東權益報酬率"` | string | 股東權益報酬率(%) |
| `"實收資本額"` | string | 實收資本額(仟元) |
| `"稅後損益與董監酬金變動之關聯性與合理性說明"` | string | 稅後損益與董監酬金變動之關聯性與合理性說明 |

## TPEx-208 · 上櫃公司合併報表董事酬金相關資訊

- **方法／URL**：[GET /mopsfin_t187ap29_C_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap29_C_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"產業類別"` | string | 產業類別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"董事酬金108年支付"` | string | 董事酬金-108年支付 |
| `"董事酬金109年支付"` | string | 董事酬金-109年支付 |
| `"董事酬金合計"` | string | 董事酬金-合計 |
| `"董事酬金加計兼任員工酬金108年支付"` | string | 董事酬金加計兼任員工酬金-108年支付 |
| `"董事酬金加計兼任員工酬金109年支付"` | string | 董事酬金加計兼任員工酬金-109年支付 |
| `"加計兼任員工酬金合計"` | string | 加計兼任員工酬金-合計 |
| `"酬金總額占稅後損益百分比董事酬金"` | string | 酬金總額占稅後損益百分比(%)-董事酬金 |
| `"酬金總額占稅後損益百分比加計兼任員工酬金"` | string | 酬金總額占稅後損益百分比(%)-加計兼任員工酬金 |
| `"平均每位董事酬金董事酬金"` | string | 平均每位董事酬金-董事酬金 |
| `"平均每位董事酬金加計兼任員工酬金"` | string | 平均每位董事酬金-加計兼任員工酬金 |
| `"領取來自子公司以外轉投資事業或母公司酬金"` | string | 領取來自子公司以外轉投資事業或母公司酬金 |
| `"稅後純益"` | string | 稅後純益 |
| `"每股盈餘"` | string | 每股盈餘 |
| `"股東權益報酬率"` | string | 股東權益報酬率(%) |
| `"實收資本額"` | string | 實收資本額(仟元) |
| `"稅後損益與董監酬金變動之關聯性與合理性說明"` | string | 稅後損益與董監酬金變動之關聯性與合理性說明 |

## TPEx-209 · 上櫃公司合併報表監察人酬金相關資訊

- **方法／URL**：[GET /mopsfin_t187ap29_D_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap29_D_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：基本面與估值／P3
- **可支持需求**：D24
- **用途**：治理或 ESG 背景、風險事件佐證；多為低頻揭露，未經樣本外驗證不提高每日權重。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"產業類別"` | string | 產業類別 |
| `"SecuritiesCompanyCode"` | string | 公司代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"監察人酬金108年支付"` | string | 監察人酬金-108年支付 |
| `"監察人酬金109年支付"` | string | 監察人酬金-109年支付 |
| `"監察人酬金合計"` | string | 監察人酬金-合計 |
| `"酬金總額占稅後損益百分比"` | string | 酬金總額占稅後損益百分比(%) |
| `"平均每位監察人酬金"` | string | 平均每位監察人酬金 |
| `"領取來自子公司以外轉投資事業或母公司酬金"` | string | 領取來自子公司以外轉投資事業或母公司酬金 |
| `"稅後純益"` | string | 稅後純益 |
| `"每股盈餘"` | string | 每股盈餘 |
| `"股東權益報酬率"` | string | 股東權益報酬率(%) |
| `"實收資本額"` | string | 實收資本額(仟元) |
| `"稅後損益與董監酬金變動之關聯性與合理性說明"` | string | 稅後損益與董監酬金變動之關聯性與合理性說明 |

## TPEx-210 · 上櫃公司違反資訊申報、重大訊息及說明記者會規定專區

- **方法／URL**：[GET /mopsfin_t187ap23_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap23_O)
- **官方 tags**：公司治理
- **決策分類／優先序**：新聞與公司事件／P2
- **可支持需求**：D24、D37、D42
- **用途**：經營權變動、裁罰與資訊申報違規，作公司事件風險。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 出表日期 |
| `"發函日期"` | string | 發函日期 |
| `"SecuritiesCompanyCode"` | string | 股票代號 |
| `"CompanyName"` | string | 公司名稱 |
| `"違規事由"` | string | 違規事由 |
| `"違反資訊申報作業辦法條款"` | string | 違反資訊申報作業辦法條款 |
| `"違反重大訊息之查證暨公開處理程序條款"` | string | 違反重大訊息之查證暨公開處理程序條款 |
| `"裁罰金額"` | string | 裁罰金額(萬) |

## TPEx-211 · 電子式交易統計資訊(上櫃)

- **方法／URL**：[GET /mopsfin_t187ap19_O](https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap19_O)
- **官方 tags**：上櫃
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"出表日期"` | string | 出表日期 |
| `"成交月份"` | string | 成交月份 |
| `"本月新增戶數"` | string | 本月新增戶數 |
| `"本月註銷戶數"` | string | 本月註銷戶數 |
| `"累計開戶數"` | string | 累計開戶數 |
| `"本月交易戶數"` | string | 本月交易戶數 |
| `"本月交易人數"` | string | 本月交易人數 |
| `"委託筆數"` | string | 委託筆數 |
| `"委託金額"` | string | 委託金額 |
| `"成交筆數"` | string | 成交筆數 |
| `"成交金額"` | string | 成交金額 |
| `"平均每筆成交金額"` | string | 平均每筆成交金額 |
| `"公司總成交筆數"` | string | 公司總成交筆數 |
| `"公司總成交金額"` | string | 公司總成交金額 |
| `"占公司成交比率筆數"` | string | 占公司成交比率(筆數) |
| `"占公司成交比率金額"` | string | 占公司成交比率(金額) |
| `"市場成交總筆數買賣合計"` | string | 市場成交總筆數(買賣合計) |
| `"市場成交總金額買賣合計"` | string | 市場成交總金額(買賣合計) |
| `"占市場成交比率筆數"` | string | 占市場成交比率(筆數) |
| `"占市場成交比率金額"` | string | 占市場成交比率(金額) |

## TPEx-212 · 興櫃股票市場現況

- **方法／URL**：[GET /tpex_esb_highlight](https://www.tpex.org.tw/openapi/v1/tpex_esb_highlight)
- **官方 tags**：興櫃
- **決策分類／優先序**：完整索引／本賽延後參考／參考
- **可支持需求**：非目前主線
- **用途**：興櫃／創櫃或申請上櫃公司不是本次固定可投資宇宙；僅另案產業觀察。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"RegisteredStocksNumber"` | string | 登錄興櫃家數 |
| `"TotalPaidinCapital"` | string | 總資本額 |
| `"TotalMarketValue"` | string | 總市值 |
| `"TransactionAmount"` | string | 本日總成交值 |
| `"TradingShares"` | string | 本日總成交股數 |
| `"TransactionNumber"` | string | 本日總成交筆數 |
| `"RecommendingDealersNumber"` | string | 推薦證券商總家數 |
| `"RecommendedPositions"` | string | 推薦部位總數 |
| `"RecommendationsPerRecommendingDealerAverageNumber"` | string | 平均每家推薦證券商推薦家數 |
| `"RecommendingDealersPerStockAverageNumber"` | string | 平均每檔股票之推薦證券商家數 |
| `"IncreaseNumber"` | string | 上漲家數 |
| `"DecreaseNumber"` | string | 下跌家數 |
| `"UnchangedNumber"` | string | 持平家數 |
| `"IncompleteNumberIncludingSuspended"` | string | 未成交含暫停交易家數 |

## TPEx-213 · 公債發行資料下載

- **方法／URL**：[GET /bond_ISSBD1_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD1_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-214 · 外國金融債發行資料下載

- **方法／URL**：[GET /bond_ISSBD2_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD2_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-215 · 金融債發行資料下載

- **方法／URL**：[GET /bond_ISSBD3_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD3_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-216 · 普通債發行資料下載

- **方法／URL**：[GET /bond_ISSBD4_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD4_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-217 · 轉(交)換債發行資料下載

- **方法／URL**：[GET /bond_ISSBD5_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD5_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-218 · 海外轉換債發行資料下載

- **方法／URL**：[GET /bond_ISSBD6_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD6_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-219 · 附認股權公司債發行資料下載

- **方法／URL**：[GET /bond_ISSBD7_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD7_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-220 · 海外附認股權公司債發行資料下載

- **方法／URL**：[GET /bond_ISSBD8_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD8_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-221 · 海外普通債發行資料下載

- **方法／URL**：[GET /bond_ISSBD9_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD9_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-222 · 國際債券(寶島債券)-本國發行人及第一、二上市(櫃)公司之外國發行人發行資料下載

- **方法／URL**：[GET /bond_ISSBD10_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD10_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondType"` | string | 債券種類 |
| `"SeriesNumber"` | string | 債券期 |
| `"TrancheNumber"` | string | 債券別 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 目前餘額 |
| `"CouponRate"` | string | 票面利率 |
| `"InterestBasis"` | string | 計付息方式 |
| `"CouponFrequency"` | string | 計息次數 |
| `"PaidFrequency"` | string | 付息次數 |
| `"BondRatingAgency"` | string | 債券評等機構 |
| `"BondRating"` | string | 債券評等等級 |
| `"IssuerRatingAgency"` | string | 發行公司評等機構 |
| `"IssuerRating"` | string | 發行公司評等等級 |
| `"GuarantorRatingAgency"` | string | 擔保機構評等機構 |
| `"GuarantorRating"` | string | 擔保機構評等等級 |
| `"ListingCountry"` | string | 掛牌地點 |
| `"PrincipalRepayment"` | string | 還本FLAG |
| `"PrincipalRepaymentDescription"` | string | 還本敘述 |
| `"ShortName"` | string | 債券簡稱 |
| `"ListingDate"` | string | 掛牌日期 |
| `"TenorYear"` | string | 發行期限年 |
| `"TenorMonth"` | string | 發行期限月 |
| `"ListingStatus"` | string | 上市櫃否 |
| `"Guaranteed"` | string | 有無擔保 |
| `"GuaranteeDescription"` | string | 債券擔保情形  |
| `"PutOptionDate"` | string | 賣回權日期 |
| `"PutOptionPrice"` | string | 賣回權價格 |
| `"Underwriter"` | string | 承銷機構 |
| `"OutstandingChangeDate"` | string | 最近餘額變動日 |
| `"OutstandingChangeDescription"` | string | 最近餘額變動原因 |
| `"Currency"` | string | 幣別 |
| `"OfferingMethod"` | string | 募集方式 |
| `"Conversion/ExchangePriceAtIssuance"` | string | 發行時轉換價格 |
| `"Conversion/ExchangePeriodStartDate"` | string | 轉換期間起 |
| `"Conversion/ExchangePeriodEndDate"` | string | 迄 |
| `"Trustee"` | string | 受託人 |

## TPEx-223 · 國際債券(寶島債券)-外國發行人(在我國未公開發行股權商品者)發行資料下載

- **方法／URL**：[GET /bond_ISSBD11_data](https://www.tpex.org.tw/openapi/v1/bond_ISSBD11_data)
- **官方 tags**：債券
- **決策分類／優先序**：總體與跨市場／P3
- **可支持需求**：D45
- **用途**：債券價格、發行或可轉債候選背景；不得直接當作殖利率、信用利差或股價訊號，需另行推導。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"IssuerCode"` | string | 機構代碼 |
| `"IssuerName"` | string | 機構名稱 |
| `"BondCode"` | string | 債券代碼 |
| `"BondName"` | string | 債券名稱 |
| `"ShortName"` | string | 債券簡稱 |
| `"BondType"` | string | 債券種類 |
| `"IssueDate"` | string | 發行日期 |
| `"MaturityDate"` | string | 到期日期 |
| `"ListingDate"` | string | 櫃檯買賣日期 |
| `"Denomination"` | string | 面額 |
| `"Volume"` | string | 發行張數 |
| `"IssueAmount"` | string | 發行總額 |
| `"OutstandingAmount"` | string | 流通餘額 |
| `"Coupon"` | string | 利率 |
| `"Currency"` | string | 交易幣別 |
| `"CreditRating"` | string | 信用評等等級 |
| `"BookRuningManager"` | string | 債券安排機構 |
| `"Note"` | string | 備註 |
| `"ListedOnTPEx"` | string | 債券於櫃買中心掛牌 |

## TPEx-224 · 上櫃股票各券商總公司當日營業金額統計表

- **方法／URL**：[GET /tpex_daily_broker2](https://www.tpex.org.tw/openapi/v1/tpex_daily_broker2)
- **官方 tags**：券商資料
- **決策分類／優先序**：價量與可交易性／P3
- **可支持需求**：D10、D12、D30
- **用途**：當沖、零股、盤後定價、分價、鉅額或券商排行僅作輔助市場結構研究；券商資料不等於最終投資人。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"Ranking"` | string | 排名 |
| `"PreviousDayRanking"` | string | 前日排名 |
| `"FinancialInstitutionsCode"` | string | 券商 |
| `"FinancialInstitutionsName"` | string | 名稱 |
| `"NumberOfCompanies"` | string | 家數 |
| `"TradingAmount"` | string | 成交金額 |
| `"DayClosingRatio"` | string | 日成交比率 |
| `"CurrentMonthRanking"` | string | 本月排名 |
| `"CurrentMonthCumulativeAmount"` | string | 本月累計金額 |
| `"CurrentMonthClosingRatio"` | string | 本月成交比率 |

## TPEx-225 · 高殖利率指數歷史收盤指數

- **方法／URL**：[GET /tphd_index](https://www.tpex.org.tw/openapi/v1/tphd_index)
- **官方 tags**：指數系列
- **決策分類／優先序**：總體與跨市場／P2
- **可支持需求**：D18、D32、D43、D55、D56
- **用途**：風格／產業基準與當日指數成分；成分股不是 ETF 實際持股。
- **參數**：規格未宣告；沒有已文件化的日期／代號／分頁參數。
- **歷史限制**：未宣告查詢參數；回傳可能為最新快照或有限歷史集合，未探測時保留未知。
- **回應**：規格根型別 `object`；媒體型態 application/json、text/csv；已核對 Swagger；未逐端點實測
- **授權設定**：規格未宣告 security，不等於服務無限制或可任意再散布。
- **接入注意**：Swagger 未宣告日期、代號、分頁參數；不保證可查任意歷史日期。數字欄位宣告 string；單位、缺值與發布時間需逐表核對。名稱雖含「歷史」，仍須確認實際保留期間。

| 原始欄位名稱（保留空白） | 型別 | 官方描述 |
|---|---|---|
| `"Date"` | string | 資料日期 |
| `"TPExHighDividendYieldIndex"` | string | 櫃買高殖利率指數 |
| `"TPExHighDividendYieldTotalReturnIndex"` | string | 櫃買高殖利率報酬指數 |
