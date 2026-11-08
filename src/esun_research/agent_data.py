"""Recompute research factors from captured official raw responses, never from model values."""
import json
import statistics
from datetime import date
from collections import defaultdict
from decimal import Decimal
from .contracts import instant
from .store import digest,encoded
from .normalize import day,number,normalize
from .history import normalize_month,request_for

VERSION='agent-research-data-2'
LEGACY_VERSION='agent-research-data-1'
FLOW_URLS={'TWSE':'https://www.twse.com.tw/rwd/zh/fund/T86','TPEx':'https://www.tpex.org.tw/openapi/v1/tpex_3insti_daily_trading'}
FLOW_FIELDS={
 'TWSE':{'foreign_net_ratio':'外陸資買賣超股數(不含外資自營商)','trust_net_ratio':'投信買賣超股數','dealer_net_ratio':'自營商買賣超股數','dealer_self_net_ratio':'自營商買賣超股數(自行買賣)','dealer_hedge_net_ratio':'自營商買賣超股數(避險)'},
 'TPEx':{'foreign_net_ratio':'Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Difference',
 'trust_net_ratio':'SecuritiesInvestmentTrustCompanies-Difference','dealer_net_ratio':'Dealers-Difference'}}


def parse_flows(body,provider,reference):
    value=json.loads(body);result=[]
    if provider=='TWSE':
        if not isinstance(value,dict) or value.get('stat')!='OK' or day(value['date'])!=reference:raise ValueError('flow_date_or_status_mismatch')
        fields=[str(f).strip() for f in value['fields']]
        if len(fields)!=len(set(fields)):raise ValueError('duplicate_flow_fields')
        if '證券代號' not in fields or not set(list(FLOW_FIELDS[provider].values())[:3])<=set(fields):raise ValueError('flow_schema_changed')
        rows=[]
        for row in value['data']:
            if len(row)!=len(fields):raise ValueError('flow_row_shape_changed')
            rows.append(dict(zip(fields,row)))
    else:
        if not isinstance(value,list) or not value:raise ValueError('flow_empty_or_invalid')
        rows=[{str(k).strip():v for k,v in r.items()} for r in value]
        if any(len(r)!=len(raw) for r,raw in zip(rows,value)):raise ValueError('duplicate_flow_fields')
        if {day(r['Date']) for r in rows}!={reference}:raise ValueError('flow_date_or_status_mismatch')
    seen=set()
    for index,row in enumerate(rows):
        code=str(row['證券代號' if provider=='TWSE' else 'SecuritiesCompanyCode']).strip()
        if code in seen:raise ValueError('duplicate_flow_security')
        if not set(list(FLOW_FIELDS[provider].values())[:3])<=set(row):raise ValueError('flow_schema_changed')
        seen.add(code);values={}
        for feature,key in FLOW_FIELDS[provider].items():
            value=number(row.get(key))
            if value is None:continue
            n=Decimal(value)
            if n!=n.to_integral_value():raise ValueError('flow_shares_not_integer')
            values[feature]=str(n)
        result.append({'code':code,'values':values,'raw_row':index})
    return result


def build_bundle(store,reference,created_at,history_inputs=None,flow_inputs=None,quote_inputs=None,version=VERSION):
    history_inputs=history_inputs or [];flow_inputs=flow_inputs or [];quote_inputs=quote_inputs or []
    if reference>instant(created_at).date().isoformat():raise ValueError('research_reference_after_cutoff')
    cells=[];sources={};missing=[];prices=defaultdict(dict);quotes={};flow_rows=defaultdict(dict)
    def cell(code,feature,value,rows):
        value=str(Decimal(str(value)))
        value_dict={'code':code,'feature':feature,'value':value,'rows':rows}
        value_dict['evidence_id']='E'+digest(encoded(value_dict))[:18];cells.append(value_dict)
    def source(sid,provider,url,when):
        meta={'authority':provider.lower(),'url':url,'name':sid+' research input','content_as_of':reference+'T13:30:00+08:00','fetched_at':when}
        if sid not in sources or instant(when)>instant(sources[sid]['fetched_at']):sources[sid]=meta
    from .cli import settings
    definitions,universe=settings();definitions={s.id:s for s in definitions}
    for item in quote_inputs:
        sid=item['source_id'];ref=item['raw_ref'];source_model=definitions[sid]
        if source_model.kind!='quotes':raise ValueError('research_quote_source_mismatch')
        with store.connect() as db:
            cap=db.execute('SELECT fetched_at FROM captures WHERE source_id=? AND ref=? ORDER BY epoch LIMIT 1',(sid,ref)).fetchone()
        if not cap or instant(cap[0])>instant(created_at):raise ValueError('research_quote_not_observed_before_cutoff')
        capture={'ref':ref,'first_seen_at':cap[0],'fetched_at':cap[0]}
        records,issues=normalize(source_model,capture,store.read(ref),universe,created_at)
        if issues:raise ValueError('research_quote_normalization_failed')
        for row in records:
            if row['date']==reference:quotes[row['security_id']]=row
    for ref in history_inputs:
        cap=store.json(ref);market=cap['market'];provider='TWSE' if market=='TWSE' else 'TPEx';code=cap['code'];when=cap['fetched_at']
        if instant(when)>instant(created_at):raise ValueError('research_history_after_cutoff')
        url,params=request_for(market,code,cap['month'])
        if cap['url']!=url or cap['parameters']!=params or cap['http_status']!=200:raise ValueError('research_history_capture_identity_mismatch')
        rows=normalize_month(store.read(cap['raw_ref']),market,code,cap['month'],when,cap['raw_ref'])
        sid='AGENT-HISTORY-'+market
        for row in rows:
            if row['date']>reference:continue
            if row['date'] in prices[code]:raise ValueError('overlapping_research_history')
            row['source_id']=sid;prices[code][row['date']]=row
        source(sid,provider,url,when)
    sessions=sorted({date for values in prices.values() for date in values})
    for code,dated in sorted(prices.items()):
        for feature,period in [('momentum_5',5),('momentum_20',20),('volatility_20',20)]:
            dates=sessions[-(period+1):]
            if len(dates)!=period+1 or dates[-1]!=reference or any(d not in dated or not dated[d]['usable_quote'] for d in dates):
                missing.append({'code':code,'feature':feature,'reason':'incomplete_reference_window'});continue
            if version==VERSION and any((date.fromisoformat(b)-date.fromisoformat(a)).days>10 for a,b in zip(dates,dates[1:])):
                missing.append({'code':code,'feature':feature,'reason':'unverified_calendar_gap'});continue
            rows=[dated[d] for d in dates];close=[Decimal(r['close_twd']) for r in rows]
            returns=[b/a-1 for a,b in zip(close,close[1:])]
            if any(r['corporate_action_marker'] or r['listing_boundary_marker'] for r in rows) or any(abs(r)>Decimal('.15') for r in returns):
                missing.append({'code':code,'feature':feature,'reason':'unverified_raw_price_boundary'});continue
            # A historical reference must agree with the official decision quote.
            if code not in quotes or close[-1]!=Decimal(quotes[code]['values']['close']):
                missing.append({'code':code,'feature':feature,'reason':'historical_reference_close_not_verified'});continue
            value=statistics.stdev(returns) if feature=='volatility_20' else close[-1]/close[0]-1
            evidence=[{'source_id':r['source_id'],'raw_ref':r['raw_ref'],'raw_row':r['raw_row'],'date':r['date'],'available_at':r['fetched_at']} for r in rows]
            cell(code,feature,value,evidence)
    for ref in flow_inputs:
        cap=store.json(ref);provider=cap['provider'];when=cap['fetched_at'];sid='AGENT-FLOWS-'+provider.upper()
        if provider not in FLOW_URLS or cap['url']!=FLOW_URLS[provider] or cap.get('http_status')!=200 or instant(when)>instant(created_at):raise ValueError('research_flow_source_or_time_mismatch')
        flow_date=cap.get('reference_date',reference) if version==VERSION else reference
        if flow_date>reference:raise ValueError('research_flow_after_reference')
        try:rows=parse_flows(store.read(cap['raw_ref']),provider,flow_date)
        except ValueError as error:
            missing.append({'source':sid,'reason':str(error)});continue
        source(sid,provider,cap['url'],when)
        for row in rows:
            code=row['code']
            if code not in universe or universe[code]['market'].upper()!=provider.upper():continue
            row['evidence']={'source_id':sid,'raw_ref':cap['raw_ref'],'raw_row':row['raw_row'],'date':flow_date,'available_at':when}
            if flow_date in flow_rows[code] and flow_rows[code][flow_date]['values']!=row['values']:raise ValueError('conflicting_flow_capture')
            duplicate=flow_date in flow_rows[code]
            flow_rows[code][flow_date]=row
            if duplicate:continue
            if flow_date!=reference:continue
            quote=quotes.get(code)
            if not quote or universe[code]['market'].upper()!=provider.upper():continue
            volume=quote['values'].get('volume')
            if volume is None or Decimal(volume)<=0:continue
            for name,net in row['values'].items():
                if version==LEGACY_VERSION and name not in {'foreign_net_ratio','trust_net_ratio','dealer_net_ratio'}:continue
                evidence=[{'source_id':sid,'raw_ref':cap['raw_ref'],'raw_row':row['raw_row'],'date':reference,'available_at':when},
                    {k:quote[k] for k in ['source_id','raw_ref','raw_row','date','available_at']}]
                cell(code,name,Decimal(net)/Decimal(volume),evidence)
    extension={}
    if version==VERSION:
        from .market_signals import price_signals,flow_signals
        extension['risk_data']=price_signals(prices,sessions,quotes,universe,cell,missing)
        flow_signals(flow_rows,prices,sessions,cell,missing)
    keys=[(c['code'],c['feature']) for c in cells]
    if len(keys)!=len(set(keys)):raise ValueError('duplicate_research_cells')
    return {**extension,'schema_version':version,'as_of':reference,'created_at':created_at,'history_inputs':history_inputs,'flow_inputs':flow_inputs,'quote_inputs':quote_inputs,
        'cells':sorted(cells,key=lambda c:(c['code'],c['feature'])),'sources':sources,'missing':missing,
        'limitations':['Downloaded historical prices are not original historical vintages.','Corporate-action markers and raw-jump filters are conservative, not complete price adjustment.','Flow ratios are net shares divided by daily volume, not ownership fractions.','No PIT strategy performance, Sharpe or expected return has been computed.']}


def validate_bundle(store,bundle,request):
    if bundle.get('schema_version') not in {VERSION,LEGACY_VERSION} or bundle.get('as_of')!=request['as_of']:raise ValueError('research_bundle_reference_mismatch')
    if instant(bundle['created_at'])>instant(request['cutoff_at']):raise ValueError('research_bundle_after_cutoff')
    expected=build_bundle(store,bundle['as_of'],bundle['created_at'],bundle['history_inputs'],bundle['flow_inputs'],bundle['quote_inputs'],version=bundle['schema_version'])
    if encoded(expected)!=encoded(bundle):raise ValueError('research_bundle_cannot_be_reproduced')
    return expected


def collect_bundle(store,universe,reference,history_root):
    """Reuse verified monthly raw bodies, then obtain only the missing reference month."""
    from pathlib import Path
    from datetime import date,timedelta
    import httpx
    from .store import Store
    from .contracts import now
    from .history import HistoricalGateway,atomic
    reference=date.fromisoformat(reference).isoformat()
    if reference>instant(now()).date().isoformat():raise ValueError('research_reference_in_future')
    folder=store.root/'agent-inputs';folder.mkdir(exist_ok=True)
    inputs=[];flows=[];quote_inputs=[];problems=[]
    # Three consecutive calendar months; never bridge a missing month using
    # an old six-month archive followed only by the current month.
    index=date.fromisoformat(reference).year*12+date.fromisoformat(reference).month-1
    wanted=[f'{(index-i)//12:04d}-{(index-i)%12+1:02d}' for i in (2,1,0)]
    report=Path(history_root)/'history/report.json'
    archive={}
    if report.exists():
        old=Store(Path(history_root));data=json.loads(report.read_bytes())
        for row in data['results']:
            if row['status']=='ok' and row['month'] in wanted:
                archive[(row['market'].upper(),row['code'],row['month'])]=old.json(row['capture_ref'])
    gateway=HistoricalGateway()
    try:
        for processed,(code,item) in enumerate(sorted(universe.items())):
            market=item['market'].upper()
            for month in wanted:
                sid='AGENT-HISTORY:'+market+':'+code+':'+month
                existing=store.select(sid,now());cap=store.json(existing['ref']) if existing['status']=='ok' else None
                if not cap and (market,code,month) in archive:
                    cap=archive[(market,code,month)];store.put(old.read(cap['raw_ref']),'bin')
                valid=False
                if cap:
                    rows=normalize_month(store.read(cap['raw_ref']),market,code,month,cap['fetched_at'],cap['raw_ref'])
                    # A completed-month capture obtained before month-end is partial.
                    next_index=int(month[:4])*12+int(month[5:])
                    next_month=f'{next_index//12:04d}-{next_index%12+1:02d}-01'
                    valid=any(r['date']==reference for r in rows) if month==reference[:7] else cap['fetched_at'][:10]>=next_month
                if not valid:
                    body,error,status=gateway.get(market,code,month);when=now()
                    if error:
                        problems.append({'code':code,'market':market,'month':month,'error':error});continue
                    url,params=request_for(market,code,month);raw_ref=store.put(body,'bin')
                    cap={'code':code,'market':market,'month':month,'url':url,'parameters':params,'fetched_at':when,'http_status':status,'raw_ref':raw_ref}
                    normalize_month(body,market,code,month,when,raw_ref)
                inputs.append(store.capture(sid,encoded(cap),fetched_at=cap['fetched_at'])['ref'])
            atomic(folder/'progress.json',encoded({'status':'RUNNING','processed':processed+1,'expected':len(universe),'problems':problems,'at':now()}))
    finally:gateway.close()
    with httpx.Client(timeout=25,follow_redirects=False) as client:
        for provider,url in FLOW_URLS.items():
            params={'response':'json','date':reference.replace('-',''),'selectType':'ALLBUT0999'} if provider=='TWSE' else None
            try:
                response=client.get(url,params=params);when=now()
                if response.status_code!=200:
                    problems.append({'source':provider+' flows','error':'http_'+str(response.status_code)});continue
                if len(response.content)>5_000_000:raise ValueError('flow_response_too_large')
                cap={'provider':provider,'url':url,'parameters':params,'raw_ref':store.put(response.content,'bin'),'fetched_at':when,'http_status':200,'reference_date':reference}
                # Bind the actual response date before indexing it as this session.
                parse_flows(response.content,provider,reference)
                flows.append(store.capture('AGENT-FLOWS:'+provider+':'+reference,encoded(cap),fetched_at=when)['ref'])
            except (httpx.HTTPError,ValueError) as error:problems.append({'source':provider+' flows','error':type(error).__name__})
    from .cli import candidate_sources
    for model in candidate_sources():
        if model.kind!='quotes':continue
        capture=store.select_reference(model,now(),reference)
        if capture['status']=='ok':quote_inputs.append({'source_id':model.id,'raw_ref':capture['ref']})
    # Accumulate prior daily captures; never pretend a latest-only TPEx API supplies history.
    with store.connect() as db:
        prior=db.execute("SELECT ref FROM captures WHERE source_id LIKE 'AGENT-FLOWS:%' AND status='ok' AND epoch<=? ORDER BY epoch,id",(instant(now()).timestamp(),)).fetchall()
    for (ref,) in prior:
        cap=store.json(ref)
        flow_day=cap.get('reference_date')
        if not flow_day:
            try:
                body=json.loads(store.read(cap['raw_ref']));flow_day=day(body['date'] if isinstance(body,dict) else body[0]['Date'])
            except (ValueError,KeyError,IndexError,TypeError):continue
        if flow_day<reference and flow_day>=str(date.fromisoformat(reference)-timedelta(days=25)):
            cap={**cap,'reference_date':flow_day};ref=store.put_json(cap)
            if ref not in flows:flows.append(ref)
    trading_dates=set()
    for ref in inputs:
        cap=store.json(ref)
        trading_dates.update(r['date'] for r in normalize_month(store.read(cap['raw_ref']),cap['market'],cap['code'],cap['month'],cap['fetched_at'],cap['raw_ref']) if r['date']<=reference)
    existing_days={(store.json(r)['provider'],store.json(r).get('reference_date',reference)) for r in flows}
    with httpx.Client(timeout=15,follow_redirects=False) as client:
        for flow_day in sorted(trading_dates)[-10:]:
            if flow_day==reference or ('TWSE',flow_day) in existing_days:continue
            params={'response':'json','date':flow_day.replace('-',''),'selectType':'ALLBUT0999'}
            try:
                response=client.get(FLOW_URLS['TWSE'],params=params);when=now()
                if response.status_code!=200 or len(response.content)>5_000_000:raise ValueError('historical_flow_http_or_size')
                parse_flows(response.content,'TWSE',flow_day)
                cap={'provider':'TWSE','url':FLOW_URLS['TWSE'],'parameters':params,'raw_ref':store.put(response.content,'bin'),'fetched_at':when,'http_status':200,'reference_date':flow_day}
                flows.append(store.capture('AGENT-FLOWS:TWSE:'+flow_day,encoded(cap),fetched_at=when)['ref'])
            except (httpx.HTTPError,ValueError) as error:problems.append({'source':'TWSE flows','date':flow_day,'error':type(error).__name__})
    result=build_bundle(store,reference,now(),inputs,flows,quote_inputs)
    output=folder/('research-data-'+reference+'.json');atomic(output,encoded(result))
    atomic(folder/'progress.json',encoded({'status':'COMPLETE_WITH_GAPS' if problems or result['missing'] else 'COMPLETE',
        'at':now(),'output':str(output),'cells':len(result['cells']),'problems':problems,'missing_count':len(result['missing'])}))
    return output,result
