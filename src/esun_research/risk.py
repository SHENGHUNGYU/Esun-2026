"""Official event snapshots as evidence, with explicit internal eligibility policy.

Capture freshness never proves the absence of future announcements. Historical
halt/resume rows are an event stream, not independent perpetual suspensions.
"""
import json
import re
import unicodedata
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, ConfigDict, Field
from .contracts import instant, TAIPEI
from .normalize import day
from .event_transport import REPORTS

FEEDS = {
    'TWSE-063':'halts', 'TWSE-072':'altered', 'TWSE-108':'disposition',
    'TWSE-116':'attention', 'TWSE-126':'ex_date',
    'TPEx-003':'halt_today', 'TPEx-004':'halts', 'TPEx-015':'ex_date',
    'TPEx-016':'status', 'TPEx-020':'attention', 'TPEx-021':'disposition',
}
FEEDS.update({sid:'web_'+value[2] for sid,value in REPORTS.items()})

class RiskPolicy(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    version: str
    maximum_capture_age_hours: int = Field(ge=1, le=72)
    avoid_new_buys_during_disposition: bool
    avoid_new_buys_in_altered_trading: bool
    attention_blocks_buys: bool
    refresh_hour_on_trade_eve: int = Field(ge=0, le=23)
    refresh_minute_on_trade_eve: int = Field(ge=0, le=59)

DATE_TOKEN = r'(?:\d{7,8}|\d{2,4}[/年.\-]\d{1,2}[/月.\-]\d{1,2}日?)'

def dates(text):
    return [day(re.sub(r'[.年月]', '/', v).rstrip('日')) for v in re.findall(DATE_TOKEN, str(text))]

def flag(value):
    value=unicodedata.normalize('NFKC',str(value)).strip().upper()
    if value in {'', 'N', '0'}:return False
    if value in {'Y','1'}:return True
    raise ValueError('unknown_status_flag')

def event_time(d, t):
    parsed=date.fromisoformat(day(d))
    t=str(t).strip().replace(':','')
    if not re.fullmatch(r'\d{6}',t):raise ValueError('missing_or_invalid_event_time')
    return datetime.combine(parsed,time(int(t[:2]),int(t[2:4]),int(t[4:])),TAIPEI)

def empty_sentinel(sid, row):
    # Only formats observed in official responses are treated as explicit empties.
    if sid=='TWSE-116':
        return ({'Number','Code','Name','TradingInfoForAttention','Date'}<=row.keys()
            and str(row.get('Number'))=='0' and not str(row.get('Code','')).strip()
            and all(not str(row.get(k,'')).strip() for k in ['Name','TradingInfoForAttention','Date']))
    if sid=='TPEx-003':
        day(row['Date'])
        keys=['SecuritiesCompanyCode','CompanyName','暫停交易','恢復交易']
        return set(keys)<=row.keys() and all(not str(row[k]).strip() for k in keys)
    return False

def assess(store, sources, frozen, universe, policy):
    req=frozen['request'];cutoff=instant(req['cutoff_at']).astimezone(TAIPEI)
    trade=date.fromisoformat(req['trade_date']);reference=date.fromisoformat(req['as_of'])
    states={code:{'buy_allowed':True,'sell_allowed':True,'flags':[]} for code in sorted(universe)}
    health=[];errors=[];timeline={code:[] for code in universe};models={s.id:s for s in sources}
    feed_refs={};blockers=['corporate_action_scope_incomplete','trading_status_scope_incomplete']
    threshold=datetime.combine(trade-timedelta(days=1),time(policy.refresh_hour_on_trade_eve,policy.refresh_minute_on_trade_eve),TAIPEI)
    for sid,role in FEEDS.items():
        c=frozen['captures'].get(sid); h={'source_id':sid,'role':role,'status':'ok','rows':0,'in_universe_rows':0,'explicit_empty_rows':0}
        health.append(h)
        if sid not in models or not c or c['status']!='ok':
            h.update(status='unavailable',reason=(c or {}).get('error') or 'missing_capture');errors.append('risk_feed_unavailable:'+sid);continue
        h.update(raw_ref=c['ref'],fetched_at=c['fetched_at']);feed_refs[sid]={'raw_ref':c['ref'],'fetched_at':c['fetched_at'],'url':models[sid].url,'provider':models[sid].provider}
        age=(cutoff-instant(c['fetched_at'])).total_seconds()/3600
        if not 0<=age<=policy.maximum_capture_age_hours:
            h['status']='stale';errors.append('risk_feed_stale:'+sid)
        if instant(c['fetched_at'])<threshold:blockers.append('risk_snapshot_needs_trade_window_refresh')
        try:
            rows=json.loads(store.read(c['ref']))
            if sid in REPORTS:
                from .exchange_events import rows as report_rows
                rows=report_rows(sid,rows)
            elif not isinstance(rows,list):raise ValueError('expected_array')
        except (ValueError,TypeError):
            h['status']='invalid';errors.append('risk_feed_invalid:'+sid);continue
        h['rows']=len(rows)
        def add(code,kind,buy=True,sell=True,**info):
            state=states[code];state['buy_allowed'] &= buy;state['sell_allowed'] &= sell
            state['flags'].append({'kind':kind,'source_id':sid,'raw_ref':c['ref'],'raw_row':index,
                'blocks_new_buys':not buy,'blocks_sells':not sell,**info})
        for index,raw in enumerate(rows):
            code=None
            try:
                if not isinstance(raw,dict):raise ValueError('expected_object')
                row={str(k).strip():v for k,v in raw.items()}
                if len(row)!=len(raw):raise ValueError('trimmed_key_collision')
                if sid in REPORTS:
                    from .exchange_events import event
                    values=row['values']
                    code=str(next(values[k] for k in ['證券代號','股票代號','代號','上市編號'] if k in values)).strip()
                    if not re.fullmatch(r'\d{4,6}',code):raise ValueError('invalid_event_security')
                    if code not in states:continue
                    h['in_universe_rows']+=1
                    if universe[code]['market'].upper()!=models[sid].provider.upper():raise ValueError('security_market_mismatch')
                    item=event(sid,values,reference.isoformat(),trade.isoformat())
                    item.pop('code')
                    add(code,item.pop('kind'),buy=item.pop('buy_allowed'),sell=item.pop('sell_allowed'),
                        page=row['page'],page_row=row['page_row'],**item)
                    continue
                key='Code' if sid.startswith('TWSE') else 'SecuritiesCompanyCode'
                if key not in row:raise ValueError('missing_security_field')
                if role=='halt_today' and date.fromisoformat(day(row['Date']))>cutoff.date():raise ValueError('record_date_after_cutoff')
                code=str(row[key]).strip()
                if not code:
                    if empty_sentinel(sid,row):h['explicit_empty_rows']+=1;continue
                    raise ValueError('unrecognized_empty_security')
                if code not in states:continue
                h['in_universe_rows']+=1
                if universe[code]['market'].upper()!=models[sid].provider.upper():raise ValueError('security_market_mismatch')
                evidence={'source_id':sid,'raw_ref':c['ref'],'raw_row':index}
                # Date on TPEx history is a ROC year, not a publication date.
                if role in {'attention','disposition','status','halt_today'}:
                    published=day(row['Date'])
                    if date.fromisoformat(published)>cutoff.date():raise ValueError('record_date_after_cutoff')
                if role=='attention':
                    add(code,'attention',buy=not policy.attention_blocks_buys,record_date=published,policy='annotation_only' if not policy.attention_blocks_buys else 'internal_avoid_new_buys')
                elif role=='disposition':
                    span=dates(row['DispositionPeriod'])
                    if len(span)!=2 or span[0]>span[1]:raise ValueError('invalid_disposition_period')
                    active=span[0]<=trade.isoformat()<=span[1]
                    add(code,'disposition' if active else 'disposition_outside_nominal_period',buy=not(active and policy.avoid_new_buys_during_disposition),start=span[0],end=span[1],policy='internal_avoid_new_buys' if active else 'nominal_dates_only')
                elif role=='ex_date':
                    effective=day(row['Date' if sid=='TWSE-126' else 'ExRrightsExDividendDate'])
                    affected=reference<date.fromisoformat(effective)<=trade
                    add(code,'corporate_action_between_reference_and_trade' if affected else 'corporate_action_outside_reference_gap',buy=not affected,sell=not affected,effective_date=effective,policy='block_until_reference_adjustment_verified' if affected else 'no_double_adjustment')
                elif role=='altered':
                    # Every row is altered-trading stock; an empty periodic flag
                    # only means no additional periodic auction designation.
                    flag(row['PeriodicCallAuctionTrading'])
                    add(code,'altered_trading',buy=not policy.avoid_new_buys_in_altered_trading,policy='internal_avoid_new_buys')
                elif role=='status':
                    values={k:flag(row[k]) for k in ['AlteredTrading','PeriodicTrading','ManagedStock','SuspensionOfTrading']}
                    if values['SuspensionOfTrading']:add(code,'suspended',buy=False,sell=False)
                    if any(values[k] for k in ['AlteredTrading','PeriodicTrading','ManagedStock']):add(code,'altered_trading',buy=not policy.avoid_new_buys_in_altered_trading,policy='internal_avoid_new_buys')
                else:
                    if sid=='TWSE-063':pairs=[('halt',row['TradingHaltDate'],row['TradingHaltTime']),('resume',row['TradingResumptionDate'],row['TradingResumptionTime'])]
                    elif sid=='TPEx-004':pairs=[('halt',row['DateOfSuspendedTrading'],row['TimeOfSuspendedTrading']),('resume',row['DateOfResumedTrading'],row['TimeOfResumedTrading'])]
                    else:
                        pairs=[]
                        for kind,key in [('halt','暫停交易'),('resume','恢復交易')]:
                            if str(row[key]).strip():
                                # Daily summary text has not yet been observed
                                # with an event; never guess its date/time format.
                                raise ValueError('unverified_daily_halt_text_format')
                    if pairs and not any(str(d).strip() for _,d,_ in pairs):raise ValueError('empty_halt_event')
                    parsed=[(kind,event_time(d,t)) for kind,d,t in pairs if str(d).strip()]
                    if len(parsed)==2 and parsed[1][1]<=parsed[0][1]:raise ValueError('nonpositive_halt_interval')
                    for kind,stamp in parsed:timeline[code].append({'event':kind,'at':stamp.isoformat(),**evidence})
            except (ValueError,KeyError,TypeError,StopIteration) as e:
                detail=str(e)[:160]
                if code in states:add(code,'unresolved_event',buy=False,sell=False,detail=detail)
                else:errors.append('risk_unscoped_row_error:'+sid+':'+str(index))
                h.setdefault('row_errors',[]).append({'raw_row':index,'code':code,'reason':detail})
                h['status']='partial_unknown'
    opening=datetime.combine(trade,time(9),TAIPEI);closing=datetime.combine(trade,time(13,30),TAIPEI)
    for code,events in timeline.items():
        # Merge split resume rows and identical duplicate announcements. Resume
        # before halt at equal time conservatively leaves a new halt active.
        active=None;intervals=[]
        for event in sorted(events,key=lambda e:(e['at'],0 if e['event']=='resume' else 1)):
            stamp=instant(event['at'])
            if event['event']=='halt':
                if active is None:active=event
            elif active:
                intervals.append((active,stamp));active=None
        if active:intervals.append((active,None))
        for start,end in intervals:
            if instant(start['at'])<=closing and (end is None or end>opening):
                states[code]['buy_allowed']=states[code]['sell_allowed']=False
                states[code]['flags'].append({'kind':'halt_overlaps_session',**start,'resume_at':end.isoformat() if end else None,
                    'blocks_new_buys':True,'blocks_sells':True})
        states[code]['halt_timeline']=sorted(events,key=lambda e:e['at'])
    return {'policy':policy.model_dump(),'trade_date':trade.isoformat(),'reference_date':reference.isoformat(),
        'feeds':health,'feed_refs':feed_refs,'securities':states,'errors':sorted(set(errors)),
        'release_blockers':sorted(set(blockers)),
        'scope_note':'Includes official financial-abnormality suspension, current-year delistings, capital-reduction and face-value-change forecasts. No complete merger/demerger/organization-change consideration chain; old forecasts are not a historical PIT calendar. Refresh in the collection window; absence is not exchange certification.'}

def order_errors(report,orders):
    return ['risk_order_not_allowed:'+o['ticker']+':'+o['side'] for o in orders
        if not report['securities'][o['ticker']]['buy_allowed' if o['side']=='BUY' else 'sell_allowed']]
