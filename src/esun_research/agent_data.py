"""Recompute research factors from captured official raw responses, never from model values."""
import json
import statistics
from collections import defaultdict
from decimal import Decimal
from .contracts import instant
from .store import digest,encoded
from .normalize import day,number,normalize
from .history import normalize_month,request_for

VERSION='agent-research-data-1'
FLOW_URLS={'TWSE':'https://www.twse.com.tw/rwd/zh/fund/T86','TPEx':'https://www.tpex.org.tw/openapi/v1/tpex_3insti_daily_trading'}
FLOW_FIELDS={
 'TWSE':{'foreign_net_ratio':'外陸資買賣超股數(不含外資自營商)','trust_net_ratio':'投信買賣超股數','dealer_net_ratio':'自營商買賣超股數'},
 'TPEx':{'foreign_net_ratio':'Foreign Investors include Mainland Area Investors (Foreign Dealers excluded)-Difference',
 'trust_net_ratio':'SecuritiesInvestmentTrustCompanies-Difference','dealer_net_ratio':'Dealers-Difference'}}


def parse_flows(body,provider,reference):
    value=json.loads(body);result=[]
    if provider=='TWSE':
        if not isinstance(value,dict) or value.get('stat')!='OK' or day(value['date'])!=reference:raise ValueError('flow_date_or_status_mismatch')
        fields=[str(f).strip() for f in value['fields']]
        if len(fields)!=len(set(fields)):raise ValueError('duplicate_flow_fields')
        if '證券代號' not in fields or not set(FLOW_FIELDS[provider].values())<=set(fields):raise ValueError('flow_schema_changed')
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
        seen.add(code);values={}
        for feature,key in FLOW_FIELDS[provider].items():
            value=number(row[key])
            if value is None:continue
            n=Decimal(value)
            if n!=n.to_integral_value():raise ValueError('flow_shares_not_integer')
            values[feature]=str(n)
        result.append({'code':code,'values':values,'raw_row':index})
    return result


def build_bundle(store,reference,created_at,history_inputs=None,flow_inputs=None,quote_inputs=None):
    history_inputs=history_inputs or [];flow_inputs=flow_inputs or [];quote_inputs=quote_inputs or []
    if reference>instant(created_at).date().isoformat():raise ValueError('research_reference_after_cutoff')
    cells=[];sources={};missing=[];prices=defaultdict(dict);quotes={}
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
        try:rows=parse_flows(store.read(cap['raw_ref']),provider,reference)
        except ValueError as error:
            missing.append({'source':sid,'reason':str(error)});continue
        source(sid,provider,cap['url'],when)
        for row in rows:
            code=row['code'];quote=quotes.get(code)
            if not quote or universe[code]['market'].upper()!=provider.upper():continue
            volume=quote['values'].get('volume')
            if volume is None or Decimal(volume)<=0:continue
            for name,net in row['values'].items():
                evidence=[{'source_id':sid,'raw_ref':cap['raw_ref'],'raw_row':row['raw_row'],'date':reference,'available_at':when},
                    {k:quote[k] for k in ['source_id','raw_ref','raw_row','date','available_at']}]
                cell(code,name,Decimal(net)/Decimal(volume),evidence)
    keys=[(c['code'],c['feature']) for c in cells]
    if len(keys)!=len(set(keys)):raise ValueError('duplicate_research_cells')
    return {'schema_version':VERSION,'as_of':reference,'created_at':created_at,'history_inputs':history_inputs,'flow_inputs':flow_inputs,'quote_inputs':quote_inputs,
        'cells':sorted(cells,key=lambda c:(c['code'],c['feature'])),'sources':sources,'missing':missing,
        'limitations':['Downloaded historical prices are not original historical vintages.','Corporate-action markers and raw-jump filters are conservative, not complete price adjustment.','Flow ratios are net shares divided by daily volume, not ownership fractions.','No PIT strategy performance, Sharpe or expected return has been computed.']}


def validate_bundle(store,bundle,request):
    if bundle.get('schema_version')!=VERSION or bundle.get('as_of')!=request['as_of']:raise ValueError('research_bundle_reference_mismatch')
    if instant(bundle['created_at'])>instant(request['cutoff_at']):raise ValueError('research_bundle_after_cutoff')
    expected=build_bundle(store,bundle['as_of'],bundle['created_at'],bundle['history_inputs'],bundle['flow_inputs'],bundle['quote_inputs'])
    if encoded(expected)!=encoded(bundle):raise ValueError('research_bundle_cannot_be_reproduced')
    return expected


def collect_bundle(store,universe,reference,history_root):
    """Reuse verified monthly raw bodies, then obtain only the missing reference month."""
    from pathlib import Path
    from datetime import date
    import httpx
    from .store import Store
    from .contracts import now
    from .history import HistoricalGateway,atomic
    reference=date.fromisoformat(reference).isoformat()
    if reference>instant(now()).date().isoformat():raise ValueError('research_reference_in_future')
    folder=store.root/'agent-inputs';folder.mkdir(exist_ok=True)
    inputs=[];flows=[];quote_inputs=[];problems=[]
    report=Path(history_root)/'history/report.json'
    if report.exists():
        old=Store(Path(history_root));data=json.loads(report.read_bytes())
        # Enough history for supported windows; no need to copy all six months.
        months=sorted({r['month'] for r in data['results'] if r['month']<=reference[:7]})[-3:]
        for row in data['results']:
            if row['status']!='ok' or row['month'] not in months:continue
            cap=old.json(row['capture_ref']);raw=old.read(cap['raw_ref']);store.put(raw,'bin')
            ref=store.capture('AGENT-HISTORY:'+cap['market']+':'+cap['code']+':'+cap['month'],encoded(cap),fetched_at=cap['fetched_at'])['ref']
            inputs.append(ref)
    gateway=HistoricalGateway()
    try:
        for index,(code,item) in enumerate(sorted(universe.items())):
            market=item['market'].upper();sid='AGENT-HISTORY:'+market+':'+code+':'+reference[:7]
            existing=store.select(sid,now())
            if existing['status']=='ok':
                cap=store.json(existing['ref']);rows=normalize_month(store.read(cap['raw_ref']),market,code,reference[:7],cap['fetched_at'],cap['raw_ref'])
                if any(r['date']==reference for r in rows):
                    if existing['ref'] not in inputs:inputs.append(existing['ref'])
                    continue
            body,error,status=gateway.get(market,code,reference[:7]);when=now()
            if error:problems.append({'code':code,'market':market,'error':error})
            else:
                url,params=request_for(market,code,reference[:7]);raw_ref=store.put(body,'bin')
                cap={'code':code,'market':market,'month':reference[:7],'url':url,'parameters':params,'fetched_at':when,'http_status':status,'raw_ref':raw_ref}
                # Verify identity and fields before adding it to a factor bundle.
                normalize_month(body,market,code,reference[:7],when,raw_ref)
                ref=store.capture(sid,encoded(cap),fetched_at=when)['ref']
                if ref not in inputs:inputs.append(ref)
            atomic(folder/'progress.json',encoded({'status':'RUNNING','processed':index+1,'expected':len(universe),'problems':problems,'at':now()}))
    finally:gateway.close()
    with httpx.Client(timeout=25,follow_redirects=False) as client:
        for provider,url in FLOW_URLS.items():
            params={'response':'json','date':reference.replace('-',''),'selectType':'ALLBUT0999'} if provider=='TWSE' else None
            try:
                response=client.get(url,params=params);when=now()
                if response.status_code!=200:
                    problems.append({'source':provider+' flows','error':'http_'+str(response.status_code)});continue
                if len(response.content)>5_000_000:raise ValueError('flow_response_too_large')
                cap={'provider':provider,'url':url,'parameters':params,'raw_ref':store.put(response.content,'bin'),'fetched_at':when,'http_status':200}
                flows.append(store.capture('AGENT-FLOWS:'+provider+':'+reference,encoded(cap),fetched_at=when)['ref'])
            except (httpx.HTTPError,ValueError) as error:problems.append({'source':provider+' flows','error':type(error).__name__})
    from .cli import candidate_sources
    for model in candidate_sources():
        if model.kind!='quotes':continue
        capture=store.select_reference(model,now(),reference)
        if capture['status']=='ok':quote_inputs.append({'source_id':model.id,'raw_ref':capture['ref']})
    result=build_bundle(store,reference,now(),inputs,flows,quote_inputs)
    output=folder/('research-data-'+reference+'.json');atomic(output,encoded(result))
    atomic(folder/'progress.json',encoded({'status':'COMPLETE_WITH_GAPS' if problems or result['missing'] else 'COMPLETE',
        'at':now(),'output':str(output),'cells':len(result['cells']),'problems':problems,'missing_count':len(result['missing'])}))
    return output,result
