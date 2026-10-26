"""Official monthly daily-price archive, separate from historical-vintage claims.

This supplies price engineering and future research. Downloaded old data are
never labelled as snapshots observed at the old dates or as official fills.
"""
import json
import re
import time
from datetime import date
from decimal import Decimal
from pathlib import Path
import httpx
from .contracts import now
from .normalize import day,number
from .store import encoded,digest,immutable

NORMALIZER_SHA256=digest(Path(__file__).read_bytes())

def atomic(path,body):
    temporary=path.with_name(path.name+'.tmp');temporary.write_bytes(body);temporary.replace(path)

def dataset_folder(root,start,end):
    base=Path(root)/'history';legacy=base/'request.json'
    if legacy.exists():
        value=json.loads(legacy.read_bytes())
        if (value['start'],value['end'])==(start,end):return base
    return base/'datasets'/(start.replace('-','')+'-'+end.replace('-',''))

URLS={'TWSE':'https://www.twse.com.tw/exchangeReport/STOCK_DAY',
      'TPEX':'https://www.tpex.org.tw/www/zh-tw/afterTrading/tradingStock'}
FIELDS={'TWSE':['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數','註記'],
        'TPEX':['日 期','成交張數','成交仟元','開盤','最高','最低','收盤','漲跌','筆數']}

def months(start,end):
    if not all(re.fullmatch(r'\d{4}-\d{2}',v) for v in [start,end]):raise ValueError('Expected YYYY-MM')
    a=date.fromisoformat(start+'-01');b=date.fromisoformat(end+'-01')
    current=date.fromisoformat(now()[:10]).replace(day=1)
    count=(b.year-a.year)*12+b.month-a.month+1
    if a.year<2010 or not 1<=count<=24 or b>=current:raise ValueError('Use 1–24 completed months, starting in 2010 or later')
    return [f'{(a.year*12+a.month-1+i)//12:04d}-{(a.year*12+a.month-1+i)%12+1:02d}' for i in range(count)]

def request_for(market,code,month):
    if market not in URLS or not re.fullmatch(r'\d{4,6}',code):raise ValueError('Unknown historical equity identity')
    date.fromisoformat(month+'-01')
    params={'response':'json'}
    params.update({'stockNo':code,'date':month.replace('-','')+'01'} if market=='TWSE' else {'code':code,'date':month.replace('-','/')+'/01'})
    return URLS[market],params

def normalize_month(body,market,code,month,fetched_at,raw_ref):
    value=json.loads(body)
    if not isinstance(value,dict) or str(value.get('stat','')).lower()!='ok':raise ValueError('history_response_not_verified_ok')
    expected=month.replace('-','')+'01'
    if value.get('date')!=expected:raise ValueError('history_response_month_mismatch')
    if market=='TWSE':
        if not re.search(r'(?<!\d)'+re.escape(code)+r'(?!\d)',str(value.get('title',''))):raise ValueError('history_response_security_mismatch')
        table=value;total=value.get('total')
    else:
        if str(value.get('code'))!=code:raise ValueError('history_response_security_mismatch')
        if len(value.get('tables',[]))!=1:raise ValueError('history_response_table_changed')
        table=value['tables'][0];total=table.get('totalCount')
        if table.get('date')!=expected:raise ValueError('history_table_month_mismatch')
    if table.get('fields')!=FIELDS[market] or not isinstance(table.get('data'),list):raise ValueError('history_fields_changed')
    if type(total) is not int or total!=len(table['data']):raise ValueError('history_response_incomplete')
    records=[];seen=set();scale=Decimal(1 if market=='TWSE' else 1000)
    for index,row in enumerate(table['data']):
        if not isinstance(row,list) or len(row)!=len(FIELDS[market]):raise ValueError('history_row_shape_changed')
        raw_date=str(row[0]).strip()
        listing_marker=market=='TPEX' and bool(re.fullmatch(r'\d{3}/\d{2}/\d{2}[*＊]',raw_date))
        trading_date=day(raw_date[:-1] if listing_marker else raw_date)
        if not trading_date.startswith(month+'-') or trading_date in seen:raise ValueError('history_duplicate_or_outside_month')
        seen.add(trading_date)
        volume=number(row[1]);amount=number(row[2]);prices=[number(x) for x in row[3:7]]
        volume=str(Decimal(volume)*scale) if volume is not None else None
        amount=str(Decimal(amount)*scale) if amount is not None else None
        if any(x is not None and Decimal(x)<0 for x in [volume,amount,*prices]):raise ValueError('history_negative_value')
        usable=all(x is not None and Decimal(x)>0 for x in [volume,amount,*prices])
        if usable:
            opening,high,low,close=map(Decimal,prices)
            if not low<=min(opening,close)<=max(opening,close)<=high:raise ValueError('history_invalid_ohlc')
        marker=str(row[7])+' '+(str(row[9]) if market=='TWSE' else '')
        action_marker=any(x in marker.upper() for x in ['X','**','除權','除息','除權息'])
        records.append({'market':market,'code':code,'date':trading_date,
            'open_twd':prices[0],'high_twd':prices[1],'low_twd':prices[2],'close_twd':prices[3],
            'volume_shares':volume,'amount_twd':amount,'usable_quote':usable,
            'corporate_action_marker':action_marker,'raw_change':str(row[7]),
            'raw_date':raw_date,'listing_boundary_marker':listing_marker,
            'raw_quantity_unit':'shares' if market=='TWSE' else 'displayed_lots_1000_shares',
            'raw_amount_unit':'TWD' if market=='TWSE' else 'displayed_thousand_TWD',
            'turnover_scope':'includes_block_trades' if market=='TWSE' else 'excludes_block_trades',
            'fetched_at':fetched_at,'published_at':None,'historical_first_seen_at':None,
            'availability_basis':'downloaded_historical_version_not_original_vintage',
            'raw_ref':raw_ref,'raw_row':index})
    return records

class HistoricalGateway:
    def __init__(self,client=None,interval=1.2,sleep=time.sleep):
        self.client=client or httpx.Client(timeout=20,follow_redirects=False)
        self.interval=max(1.0,interval);self.sleep=sleep;self.last={};self.blocked={}
    def close(self):self.client.close()
    def get(self,market,code,month):
        url,params=request_for(market,code,month)
        if market in self.blocked:return None,self.blocked[market],None
        for attempt in range(2):
            self.sleep(max(0,self.interval-(time.monotonic()-self.last.get(market,0))));self.last[market]=time.monotonic()
            try:
                response=self.client.get(url,params=params)
                if len(response.content)>5_000_000:return None,'history_response_too_large',response.status_code
                if response.status_code==200:return response.content,None,200
                error='history_http_'+str(response.status_code)
                if response.status_code in {401,403}:
                    self.blocked[market]=error;return response.content,error,response.status_code
                retry=response.status_code in {429,500,502,503,504}
                wait=response.headers.get('Retry-After','2')
                try:delay=float(wait)
                except ValueError:delay=120
                if delay>30 or response.status_code==429:
                    self.blocked[market]=error+'_retry_later';return response.content,self.blocked[market],response.status_code
                if not retry or attempt:return response.content,error,response.status_code
                self.sleep(max(0,delay))
            except (httpx.NetworkError,httpx.TimeoutException):
                if attempt:return None,'history_network_error',None
                self.sleep(2)

def collect_history(store,universe,start,end,gateway,progress=None):
    import pandas as pd
    requested=months(start,end);results=[];records=[]
    base=store.root/'history';base.mkdir(exist_ok=True)
    folder=dataset_folder(store.root,start,end);folder.mkdir(parents=True,exist_ok=True)
    immutable(folder/'request.json',encoded({'start':start,'end':end,'universe_hash':digest(encoded(universe)),'urls':URLS}))
    atomic(base/'active-dataset.json',encoded({'start':start,'end':end}))
    def save_progress():
        value={'at':now(),'requested_months':requested,'expected_requests':len(universe)*len(requested),
            'completed_requests':len(results),'successful_months':sum(r['status']=='ok' for r in results),
            'failed_months':sum(r['status']=='error' for r in results),'normalized_rows':len(records),
            'status':'RUNNING','blocked_markets':getattr(gateway,'blocked',{})}
        atomic(folder/'progress.json',encoded(value))
        return value
    for code in sorted(universe):
        market=universe[code]['market'].upper()
        for month in requested:
            sid=f'HISTORY:{market}:{code}:{month}';cached=store.select(sid,now());cache_hit=cached.get('status')=='ok'
            url,params=request_for(market,code,month);error=None;wrapper=None
            try:
                if cache_hit:
                    wrapper=store.json(cached['ref'])
                    if (wrapper['market'],wrapper['code'],wrapper['month'])!=(market,code,month):raise ValueError('history_cache_identity_mismatch')
                    body=store.read(wrapper['raw_ref']);when=wrapper['fetched_at'];raw_ref=wrapper['raw_ref']
                else:
                    body,error,status=gateway.get(market,code,month);when=now();raw_ref=store.put(body,'bin') if body is not None else None
                    wrapper={'url':url,'parameters':params,'market':market,'code':code,'month':month,
                        'http_status':status,'fetched_at':when,'raw_ref':raw_ref}
                normalized=normalize_month(body,market,code,month,when,raw_ref) if error is None else []
            except (ValueError,TypeError,KeyError,AttributeError) as failure:
                error='history_integrity_or_schema_failed';normalized=[]
            if not cache_hit or error:
                capture=store.capture(sid,encoded(wrapper) if wrapper is not None else None,error=error,fetched_at=now())
            else:capture=cached
            item={'market':market,'code':code,'month':month,'status':'error' if error else 'ok',
                'cache_hit':cache_hit,'rows':len(normalized),'error':error,'capture_ref':capture.get('ref')}
            results.append(item);records.extend(normalized);save_progress()
            if progress:progress(item)
    frame=pd.DataFrame(records)
    if not frame.empty:
        if frame.duplicated(['market','code','date']).any():raise ValueError('Duplicate normalized historical key')
        frame=frame.sort_values(['market','code','date']);temp=folder/'daily-prices.tmp.parquet'
        frame.to_parquet(temp,index=False);temp.replace(folder/'daily-prices.parquet')
    else:(folder/'daily-prices.parquet').unlink(missing_ok=True)
    state=save_progress();state['status']='COMPLETE' if not state['failed_months'] else 'INCOMPLETE'
    state.update(universe_count=len(universe),usable_rows=sum(r['usable_quote'] for r in records),
        action_marked_rows=sum(r['corporate_action_marker'] for r in records),
        listing_marked_rows=sum(r['listing_boundary_marker'] for r in records),
        explicit_empty_months=sum(r['status']=='ok' and not r['rows'] for r in results),
        normalizer_sha256=NORMALIZER_SHA256,
        strict_pit_verified=False,corporate_action_adjustments_verified=False,
        official_execution_price_verified=False,strategy_backtest_ready=False,
        results=results,limitations=['Downloaded historical version; original release and revision timestamps unavailable.',
            'Current competition whitelist introduces selection/survivorship bias in past periods.',
            'TWSE turnover includes block trades; TPEx sample excludes block trades and has rounded lots/thousand-TWD units.',
            'Raw prices and partial event markers do not establish complete corporate-action adjustment.',
            'A listing-date star is preserved as a structural boundary; it does not establish prior security identity or tradability.',
            'No revenue/value production-strategy performance claim is supported by this price-only archive.'])
    if not frame.empty:state['parquet_sha256']=digest((folder/'daily-prices.parquet').read_bytes())
    report=['# 官方歷史價量資料驗收','',f'狀態：{state["status"]}；{len(universe)}檔，{start}至{end}，成功月份{state["successful_months"]}/{state["expected_requests"]}。',
        f'日紀錄{len(records)}筆；可用價量{state["usable_rows"]}筆；原始公司行動標記{state["action_marked_rows"]}筆。',
        '','本報告是資料取得與重建品質檢查，沒有策略績效或正式成交驗收。嚴格營收／估值回測仍缺當時可見版本。','',*['- '+v for v in state['limitations']]]
    atomic(folder/'report.md',('\n'.join(report)+'\n').encode())
    atomic(folder/'report.json',encoded(state))
    atomic(folder/'progress.json',encoded({k:v for k,v in state.items() if k!='results'}))
    return state
