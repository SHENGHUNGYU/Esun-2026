"""Public cross-market observations: immutable, cutoff-bound, observation-only.

No portfolio weights or trading permission are derived from these new sources.
Date-only history is first available at capture time, never its observation date.
"""
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import httpx
from defusedxml import ElementTree as ET
from .contracts import now, instant, TAIPEI
from .store import encoded, digest, immutable

VERSION = 'public-context-1'
BASE = 'https://openapi.taifex.com.tw/v1/'

def contracts(year):
    common = {'enabled': True, 'required_for_orders': False, 'auth': 'none',
              'mode': 'shadow', 'refresh_hours': 6, 'max_age_days': 7}
    definitions = [
        ('TAIFEX-PCR', '臺指選擇權 Put/Call', BASE+'PutCallRatio', 'taifex', 'ratio_percent', ['Date','PutCallVolumeRatio%','PutCallOIRatio%']),
        ('TAIFEX-FUTURES', '期貨日夜盤行情', BASE+'DailyMarketReportFut', 'taifex', 'points_contracts', ['Date','Contract','ContractMonth(Week)','TradingSession','Last','Volume']),
        ('TAIFEX-INSTITUTIONS', '期貨三大法人部位', BASE+'MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate', 'taifex', 'contracts_and_thousand_TWD', ['Date','ContractCode','Item','OpenInterest(Net)']),
        ('TAIFEX-LARGE', '大額交易人未沖銷', BASE+'OpenInterestOfLargeTradersFutures', 'taifex', 'contracts', ['Date','Contract','SettlementMonth','TypeOfTraders','Top5Buy','Top5Sell','OIOfMarket']),
        ('CBC-USDTWD', '銀行間美元臺幣收盤', 'https://cpx.cbc.gov.tw/api/OpenData/FTDOpenData_Day', 'cbc', 'TWD_per_USD', ['日期','NTD_USD']),
        ('FED-POLICY', 'Fed 貨幣政策公告', 'https://www.federalreserve.gov/feeds/press_monetary.xml', 'rss', 'event', []),
        ('FED-SPEECHES', 'Fed 官員談話', 'https://www.federalreserve.gov/feeds/speeches.xml', 'rss', 'event', []),
        ('UST-NOMINAL', '美債名目殖利率', 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value='+str(year), 'treasury', 'percent_per_year', ['NEW_DATE','BC_2YEAR','BC_10YEAR']),
        ('UST-REAL', '美債實質殖利率', 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_real_yield_curve&field_tdr_date_value='+str(year), 'treasury', 'percent_per_year', ['NEW_DATE','TC_5YEAR','TC_10YEAR']),
    ]
    result = [{**common, 'id': sid, 'name': name, 'url': url, 'parser': parser, 'unit': unit,
               'required_fields': fields, 'license': 'provider_terms_internal_research_review_before_redistribution',
               'publication_time': 'item_timestamp' if parser=='rss' else 'not_provided_first_seen_only'}
              for sid,name,url,parser,unit,fields in definitions]
    for item in result:
        if item['parser']=='rss': item['max_age_days']=45
        if item['parser']=='cbc': item['license']='Taiwan_Open_Government_Data_License_1.0'
    result.append({**common, 'id':'FRED-ALFRED', 'name':'FRED／ALFRED 歷史版本', 'url':'https://api.stlouisfed.org/fred/series/observations',
                   'enabled':False, 'auth':'FRED_API_KEY', 'parser':'disabled', 'unit':'series_specific',
                   'required_fields':[], 'license':'series_specific', 'publication_time':'vintage_required',
                   'disabled_reason':'requires_personal_api_key_not_configured'})
    return result


def numeric(value):
    try:
        v=Decimal(str(value).replace(',','').strip().rstrip('%'))
        return str(v) if v.is_finite() else None
    except (InvalidOperation,ValueError): return None


def day(value):
    text=str(value).strip()
    if re.fullmatch(r'\d{8}',text):text=text[:4]+'-'+text[4:6]+'-'+text[6:]
    return date.fromisoformat(text[:10]).isoformat()


def parse(source, body, capture, cutoff):
    """All records bind to a hash-checked raw object and real acquisition time."""
    if instant(capture['fetched_at'])>instant(cutoff):raise ValueError('capture_after_cutoff')
    latest_day=instant(cutoff).astimezone(TAIPEI).date().isoformat()
    kind=source['parser']; result=[]
    def record(index, observed, values, **extra):
        if observed>latest_day:return
        row={'source_id':source['id'],'observed_date':observed,'values':values,'unit':source['unit'],
             'raw_ref':capture['ref'],'raw_row':index,'available_at':capture.get('first_seen_at',capture['fetched_at']),
             'published_at':None,'availability_basis':'first_seen_not_historical_publication',**extra}
        row['evidence_id']='W'+digest(encoded(row))[:20];result.append(row)
    if kind in {'taifex','cbc'}:
        rows=json.loads(body)
        if not isinstance(rows,list) or not rows:raise ValueError('expected_nonempty_json_array')
        seen=set()
        for i,row in enumerate(rows):
            if not isinstance(row,dict) or not set(source['required_fields'])<=set(row):raise ValueError('public_source_schema_changed')
            observed=day(row['日期'] if kind=='cbc' else row['Date'])
            if kind=='cbc':
                value=numeric(row['NTD_USD'])
                if value is None or Decimal(value)<=0:raise ValueError('invalid_fx_rate')
                if observed in seen:raise ValueError('duplicate_fx_date')
                seen.add(observed);record(i,observed,{'USDTWD':value})
            else:
                # Keep contract/month/session/trader type distinct; never sum
                # overlapping months, trading sessions or concentration groups.
                identity={k:v for k,v in row.items() if k not in {'Date'}}
                record(i,observed,identity)
    elif kind=='rss':
        root=ET.fromstring(body);items=root.findall('./channel/item')
        if root.tag!='rss':raise ValueError('expected_rss')
        for i,item in enumerate(items):
            stamp=item.findtext('pubDate')
            published=parsedate_to_datetime(stamp).isoformat() if stamp else None
            if not published or instant(published)>instant(cutoff):continue
            link=item.findtext('link') or ''
            if urlparse(link).hostname!='www.federalreserve.gov':raise ValueError('unexpected_feed_link')
            record(i,instant(published).astimezone(TAIPEI).date().isoformat(),
                   {'title':(item.findtext('title') or '')[:600],'url':link,
                    'description':(item.findtext('description') or '')[:1800]},published_at=published,
                   availability_basis='publication_and_first_seen_cutoff')
    elif kind=='treasury':
        root=ET.fromstring(body)
        ns={'a':'http://www.w3.org/2005/Atom','m':'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'}
        for i,entry in enumerate(root.findall('a:entry',ns)):
            props=entry.find('.//m:properties',ns)
            if props is None:raise ValueError('treasury_properties_missing')
            row={p.tag.split('}')[-1]:p.text for p in props}
            if not set(source['required_fields'])<=set(row):raise ValueError('treasury_schema_changed')
            values={k:numeric(v) for k,v in row.items() if k.startswith(('BC_','TC_'))}
            if not any(v is not None for v in values.values()):continue
            record(i,day(row['NEW_DATE']),values)
        if not result:raise ValueError('treasury_no_observations')
    else:raise ValueError('unsupported_public_parser')
    return result


def collect(store, client=None):
    """One bounded request/source; cache successes, preserve failures, no WAF bypass."""
    started=now();defs=contracts(instant(started).year);owned=client is None
    client=client or httpx.Client(timeout=httpx.Timeout(12),follow_redirects=False,headers={'User-Agent':'EsunResearch/1.0 public-data-research'})
    def fetch(source):
        if not source['enabled']:return {'source_id':source['id'],'status':'disabled','error':source['disabled_reason']}
        prior=store.select('WORLD:'+source['id'],started)
        if prior['status']=='ok' and (instant(started)-instant(prior['fetched_at'])).total_seconds()<source['refresh_hours']*3600:
            return {**prior,'cached':True}
        body=None
        try:
            response=client.get(source['url']);response.raise_for_status();body=response.content
            if len(body)>12_000_000:raise ValueError('public_response_too_large')
            at=now();probe={'ref':store.put(body,'bin'),'fetched_at':at}
            parse(source,body,probe,at)
            return store.capture('WORLD:'+source['id'],body,fetched_at=at)
        except Exception as error:
            # Exceptions contain request URLs; no secrets are ever placed here.
            detail=('http_'+str(error.response.status_code)) if isinstance(error,httpx.HTTPStatusError) else type(error).__name__+':'+str(error)[:100]
            return store.capture('WORLD:'+source['id'],body,error=detail)
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:captures=list(pool.map(fetch,defs))
    finally:
        if owned:client.close()
    cutoff=now();bundle=build(store,cutoff)
    ref=store.put_json(bundle);ident=digest(encoded(bundle))
    immutable(store.root/'public-context'/(ident+'.json'),encoded({'id':ident,'bundle_ref':ref,'cutoff_at':cutoff}))
    return bundle,ident


def build(store,cutoff):
    sources=[];observations=[]
    for source in contracts(instant(cutoff).year):
        item={**source,'status':'disabled' if not source['enabled'] else 'missing','records':0}
        if source['enabled']:
            cap=store.select('WORLD:'+source['id'],cutoff)
            item.update(status=cap['status'],raw_ref=cap.get('ref'),fetched_at=cap.get('fetched_at'),error=cap.get('error'))
            if cap['status']=='ok':
                try:
                    rows=parse(source,store.read(cap['ref']),cap,cutoff)
                    latest=max((r['observed_date'] for r in rows),default=None)
                    days=(instant(cutoff).astimezone(TAIPEI).date()-date.fromisoformat(latest)).days if latest else None
                    capture_age=(instant(cutoff)-instant(cap['fetched_at'])).total_seconds()/3600
                    item.update(records=len(rows),latest_observation=latest,capture_age_hours=round(capture_age,2),
                                status='stale' if capture_age>source['refresh_hours']*2 or (source['parser']!='rss' and (days is None or days>source['max_age_days'])) else 'ok')
                    # RSS can legitimately have no recent release; freshness is
                    # acquisition health, not an invented daily event requirement.
                    if item['status']=='ok':observations.extend(rows)
                except Exception as error:item.update(status='error',error=type(error).__name__+':'+str(error)[:100])
        sources.append(item)
    return {'schema_version':VERSION,'cutoff_at':cutoff,'mode':'shadow','production_authorized':False,
            'sources':sources,'observations':observations,
            'limitations':['Date-only history is available at first capture, not at the historical observation date.',
            'New public context does not change production factors, constraints or orders before validation.',
            'Futures sessions, contract months and trader groups are not interchangeable.',
            'No US equity/ADR prices, consensus expectations or complete international news coverage.']}


def latest(store):
    paths=list((store.root/'public-context').glob('*.json'))
    if not paths:return {'status':'NOT_STARTED','sources':contracts(instant(now()).year),'observations':[]}
    item=max((json.loads(p.read_bytes()) for p in paths),key=lambda r:instant(r['cutoff_at']))
    bundle=store.json(item['bundle_ref'])
    if digest(encoded(bundle))!=item['id']:raise ValueError('public_context_integrity_failed')
    return {**bundle,'id':item['id'],'bundle_ref':item['bundle_ref'],'status':'COLLECTED',
            'current_health':[{k:s.get(k) for k in ['id','status','error','latest_observation','capture_age_hours']} for s in build(store,now())['sources']]}
