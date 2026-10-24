"""Extract every declared TWSE operation; annotations are research judgments."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=json.loads((ROOT/'twse/swagger.json').read_text());probes=json.loads((ROOT/'twse/probes.json').read_text());byprobe={x['url']:x for x in probes}

def annotation(path,op):
 p=path.lower();name=op.get('summary','');fields=op.get('responses',{}).get('200',{}).get('schema',{}).get('properties',{})
 a=dict(priority='參考',category='other',data_refs=[],use='保留完整規格索引；目前固定 150 檔股票策略不優先使用。',caveat='本次只核對規格；資料日期、覆蓋、單位與實際回應仍需驗收。')
 def set_(tier,cat,refs,use,note):a.update(priority=tier,category=cat,data_refs=refs.split(','),use=use,caveat=note)
 if p=='/exchangereport/stock_day_all':set_('P0','price','D04,D07,D10,D13,D14,D16,D17,D31,D33,D34,D57','原始日 OHLC、股數與金額；支援官方日均價結算、技術與風險原料。','只按競賽 150 檔過濾；日均價 TradeValue/TradeVolume 是盤後結果。回應型態以實測為準。')
 elif p=='/opendata/t187ap03_l':set_('P0','rules','D01,D09,D49','上市主檔、產業、已發行股數、資本額与上市日。','主檔不是競賽白名單；保存版本，股本不等於自由流通股。')
 elif 'holidayschedule' in p:set_('P0','rules','D02','市場開休市與不同假日的交易安排。','日曆版本與臨時停市另確認，不能只用平日判斷。')
 elif p in ['/exchangereport/twtawu','/exchangereport/twt85u','/exchangereport/twt88u','/announcement/punish','/announcement/notice','/announcement/notetrans']:
  set_('P0' if p in ['/exchangereport/twtawu','/exchangereport/twt85u','/announcement/punish'] else 'P1','price','D11,D37','停復牌、變更交易、首五日無漲跌幅、處置／注意風險清單。','各表含義不同；注意股不等於禁止交易，公告與生效日期分開。')
 elif p in ['/exchangereport/twt48u_all','/opendata/t187ap45_l']:
  set_('P0','rules','D05,D39','除權息預告與股利分派決議，補充公司行動與事件日曆。','兩表需互相對帳；不完整覆蓋分割／減資／支付日，仍須其他官方公告。')
 elif p in ['/exchangereport/bwibbu_all','/exchangereport/bwibbu_d']:
  set_('P1','fundamental','D23','官方 PE、PB、殖利率與（依表）財報年季。','日期／代碼查询是表名，規格仍無參數；不是预估PE或股利可用現金。')
 elif p=='/exchangereport/stock_day_avg_all':set_('P1','price','D07,D14','收盤價及月平均價的價量交叉核對。','月平均價不是官方當日成交均價；不能代替 OHLC 原料。')
 elif p in ['/exchangereport/fmsrfk_all','/exchangereport/fmnptk_all']:
  set_('P2','price','D07,D10','月／年交易彙總與周轉診斷。','月／年彙總不能拆出每日序列；Year/Month 是回應欄位，不是查詢參數。')
 elif p in ['/indicesreport/mi_5mins_hist','/indicesreport/mfi94u','/indicesreport/tai50i','/indicesreport/frmsa']:
  set_('P1' if p!='/indicesreport/frmsa' else 'P2','macro','D31,D34,D43,D56','市場／報酬指數與其他基準對照，提供 Beta 與超額報酬原料。','名稱「歷史」不保證長歷史；報酬／價格指數口徑要一致，四種指數不可默認等價。')
 elif p in ['/exchangereport/mi_index','/exchangereport/fmtqik','/exchangereport/mi_index4','/opendata/twtazu_od']:
  set_('P1','technical','D18,D43','市場成交量值、漲跌家數或跨市場統計；市場狀態與廣度。','以各表實際欄位為準；廣度不等於固定 150 檔廣度，成交金額單位逐表核對。')
 elif p=='/exchangereport/mi_index20':set_('P2','technical','D10,D18','成交活躍證券排名的市場觀測。','只涵蓋前 20 名，不能當 150 檔完整量能資料。')
 elif p=='/exchangereport/mi_5mins':set_('P3','price','D12','委託／成交聚合的盤中市場觀測。','不是逐股完整 tick／委託簿；不能使用晨間決策後的數字。')
 elif p=='/exchangereport/mi_margn':set_('P2','flows','D28','逐股融資融券買賣、償還、前日／今日餘額、限額與互抵。','schema 有逐股欄位，但未宣告日期欄位／歷史參數；股、張或金額需實際資料說明驗證。')
 elif p=='/exchangereport/bfi84u':set_('P2','flows','D11,D28','停資停券預告與信用交易風險狀態。','信用交易資格不是一般現股可買資格；預告與生效日期分開。')
 elif p=='/sbl/twt96u':set_('P2','flows','D28','上市上櫃可借券賣出股數的供給觀察。','可借券賣出額度不等於實際借券賣出／借券餘額；不代表策略可放空。')
 elif p.startswith('/fund/mi_qfiis'):
  set_('P2','flows','D26','外資／陸資產業持股比率或前 20 名持股結構。','產業彙總與前 20 名都不是全體個股外資持股表；不是每日法人買賣超。')
 elif p.startswith('/block/'):
  set_('P2','flows','D10,D25','鉅額交易日／月／年量值統計的額外流動性觀察。','鉅額統計不辨識法人身分，不能當三大法人淨買。')
 elif p=='/exchangereport/twt84u':set_('P2','technical','D13,D18','個股漲跌幅與排名的輔助核對。','不能只從上榜股票建母體；完整報酬仍由日價量算。')
 elif p.startswith('/opendata/t187ap05_'):
  set_('P1' if p.endswith('_l') else 'P3','fundamental','D19','月營收、去年同期與累計成長；_L為上市、_P為公開發行範圍。','資料年月不是公告時點；本次快照只有 11508，須檢查時效；金額單位以資料集定義核對。')
 elif '/t187ap06_l_' in p or '/t187ap07_l_' in p:
  income='/t187ap06_' in p
  set_('P1','fundamental','D20,D22,D23' if income else 'D09,D20,D22,D23','各產業綜合損益或資產負債欄位；一般／金融／金控／保險／證券／異業需分表。','出表日期不等於各公司首發日；單季與累計口徑須核對。這些不是完整現金流量表或 PIT 修訂歷史。')
 elif '/t187ap06_x_' in p or '/t187ap07_x_' in p:
  set_('P3','fundamental','D20,D22','公開發行範圍財務表的備援／交叉核對。','與上市主線表有範圍重疊；不得重複列樣本或直接代替上櫃表。')
 elif p in ['/opendata/t187ap14_l','/opendata/t187ap17_l']:
  set_('P1','fundamental','D20,D23','EPS／營益與利潤率彙總，快速核對財報摘要。','無完整 CFO／FCF；百分比與百萬元欄位不可混成元。')
 elif p in ['/opendata/t187ap15_l','/opendata/t187ap16_l']:
  set_('P2','events','D40,D41','公司財測達成與查核數差異公告。','公司自有財測差異不是分析師共識預期差；只涵蓋符合揭露條件的公司。')
 elif p=='/opendata/t187ap04_l':set_('P1','events','D37,D38,D39,D42','每日重大訊息原文、發言日期／時間、事實發生日與說明，建立事件證據。','出表、發言、發生時間不混用；schema 的「主旨 」有尾端空白，保留原鍵與映射。')
 elif p in ['/news/newslist','/announcement/bfzfzu_t']:
  set_('P2','events','D37,D38','交易所新聞或異常推介公告的官方事件補充。','交易所新聞不是全市場新聞 API；newsList 主要標題／連結／日期，非完整全文。')
 elif any(f'/t187ap{x}_l' in p for x in ['08','09','10','11','12','13','02']):
  set_('P2','flows','D24,D26,D29','大股東、董監持股、質押、持股不足與轉讓／未轉讓申報。','每表範圍不同，申報不等於成交；持股餘額不等於日交易流。')
 elif p=='/opendata/t187ap11_p':set_('P3','flows','D29','公開發行董監持股資料備援。','不是150檔固定宇宙，也不等於完整外資持股。')
 elif any(f'/t187ap{x}_l' in p for x in ['22','23','24','25','26','27','31','33']):
  set_('P2','events','D24,D37,D42','裁罰、揭露違規、經營權／營業範圍異動、財報承認或治理風險。','依正式公告界定事件與生效時點，不直接用旗標產生買賣。')
 elif any(f'/t187ap{x}_l' in p for x in ['38','41']):set_('P1','events','D39','股東會公告／日期與電子投票資訊，建立公司事件日曆。','會議排程與實際結果不同；需保留已知版本。')
 elif '/t187ap46_l_' in p:
  n=int(p.rsplit('_',1)[1]);set_('P2' if n in [8,13,14,16,18,19,20] else 'P3','fundamental','D24,D49,D66','ESG／供應鏈／資安／治理等慢頻風險與主題補充。','不是高頻交易訊號；報告年度不是公告可用日，揭露與公司真實暴露需分清。')
 elif any(f'/t187ap{x}' in p for x in ['29_','30_l','32_l','34_l','35_l']):set_('P3','fundamental','D24','治理與董監事制度／酬金的延後研究資料。','慢頻且非必然增量，留作可追溯背景。')
 elif p=='/opendata/t187ap47_l':set_('P1','funds','D53,D54','基金／ETF 基本資料、指數與海外成分旗標，識別比較對象。','基金基本資料不含每日完整成分股／權重；不能用來計 Active Share。')
 elif p=='/etfreport/etfrank':set_('P3','funds','D54','定期定額戶數排名的注意力觀測。','戶數不等於申購金額、淨申贖或基金持股。')
 elif p in ['/company/newlisting','/company/suspendlistingcsvandhtml']:
  set_('P1','rules','D01,D11','新上市與終止上市主檔異動核對。','不能用新上市名單更改官方固定150檔；日期與掛牌狀態核對。')
 elif p.startswith('/company/applylisting'):set_('P3','industry','D49','上市申請的產業背景資料。','申请不是已可投資標的，固定宇宙不因申請增補。')
 elif any(z in p for z in ['twtb4u','twtbau','twt53u','bft41u','stock_first']):
  set_('P3','price','D10,D11,D12','當沖資格、零股、盤後定價或第一上市等交易制度補充。','依欄位判讀；TWTB4U 在此規格主要為當沖標的／註記，不能假定有完整當沖比率。')
 return a
rows=[]
for path,ops in s['paths'].items():
 for method,op in ops.items():
  if method.lower() not in ['get','post','put','patch','delete','head','options','trace']:continue
  schema=op.get('responses',{}).get('200',{}).get('schema',{});props=schema.get('properties',{})
  url='https://'+s['host']+s['basePath']+path
  row=dict(id=f'TWSE-{len(rows)+1:03}',exchange='TWSE',method=method.upper(),path=path,url=url,summary=op.get('summary',''),description=op.get('description',''),tags=op.get('tags',[]),parameters=ops.get('parameters',[])+op.get('parameters',[]),fields=[dict(name=k,type=v.get('type','未宣告'),description=v.get('description',''),format=v.get('format'),required=k in schema.get('required',[])) for k,v in props.items()],response_shape=schema.get('type','未宣告'),media_types=op.get('produces',s.get('produces',[])),security=op.get('security',s.get('security',[])),spec_url='https://openapi.twse.com.tw/v1/swagger.json',probe=byprobe.get(url))
  row.update(annotation(path,op));row['history']='Swagger 未宣告日期／代碼／分頁參數；回傳時間範圍逐表驗證。';rows.append(row)
(ROOT/'twse-operations.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('TWSE extracted',len(rows),'operations')
from collections import Counter
print(Counter(x['priority'] for x in rows))
