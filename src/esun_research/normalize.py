"""Strict date/unit parsing; raw keys and rows stay in the immutable raw object."""
import json
import re
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from html import unescape
from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException
from .contracts import TAIPEI, instant
from .store import digest, encoded

def day(value):
    text=str(value).strip()
    if re.fullmatch(r'\d{7,8}',text):
        year=int(text[:-4]);month=int(text[-4:-2]);d=int(text[-2:])
    else:
        parts=re.split(r'[-/年/月日]+',text.strip('日'))
        if len(parts)!=3: raise ValueError('Unrecognized date')
        year,month,d=map(int,parts)
    return date(year+1911 if year<1911 else year,month,d).isoformat()

def number(value):
    s=str(value).strip().replace(',','')
    if s in {'','--','---','N/A','None','nan','NaN','不適用'}:return None
    try:v=Decimal(s)
    except InvalidOperation: raise ValueError('Invalid numeric field') from None
    if not v.is_finite():raise ValueError('Nonfinite number')
    return str(v)

def clean_text(value):
    return re.sub(r'\s+',' ',unescape(re.sub('<[^>]*>',' ',str(value)))).strip()

def rss_records(body):
    root=ElementTree.fromstring(body)
    if root.tag!='rss':raise ValueError('Expected RSS document')
    result=[]
    for item in root.findall('./channel/item'):
        published=item.findtext('pubDate')
        timestamp=parsedate_to_datetime(published).astimezone(TAIPEI).isoformat() if published else None
        link=item.findtext('link','')
        if not link.startswith(('https://','http://')):raise ValueError('Invalid news link')
        result.append({'title':clean_text(item.findtext('title','')),
                       'summary':clean_text(item.findtext('description',''))[:700],
                       'link':link,'published_at':timestamp,'guid':item.findtext('guid') or link})
    return result

def normalize(source, capture, body, universe, cutoff_at):
    issues=[];records=[]
    try:
        raw=rss_records(body) if source.kind=='rss' else json.loads(body)
        if source.provider=='FinMind':raw=raw['data']
        if not isinstance(raw,list):raise ValueError('Expected array')
        if raw and source.fields and not set(source.fields)<=set(raw[0]):
            missing=sorted(set(source.fields)-set(raw[0]))
            raise ValueError('Schema missing: '+','.join(missing))
    except (ValueError,KeyError,TypeError,ElementTree.ParseError,DefusedXmlException) as e:
        return [],[{'source':source.id,'reason':'parse_or_schema_error','detail':str(e)[:300]}]
    for index,row in enumerate(raw):
        try:
            if not isinstance(row,dict):raise ValueError('Row is not an object')
            r={str(k).strip():v for k,v in row.items()}
            if len(r)!=len(row):raise ValueError('Trimmed key collision')
            code=str(r.get('Code',r.get('SecuritiesCompanyCode',r.get('公司代號',r.get('stock_id',''))))).strip()
            if code and code not in universe:continue
            if code and source.provider in {'TWSE','TPEx'} and universe[code]['market'].upper()!=source.provider.upper():
                raise ValueError('Security market mismatch')
            if source.kind not in {'rss','raw','market_index'} and not code:raise ValueError('Missing company identifier')
            base={'source_id':source.id,'kind':source.kind,'security_id':code,
                  'raw_ref':capture['ref'],'raw_row':index,'first_seen_at':capture['first_seen_at'],
                  'fetched_at':capture['fetched_at'],'published_at':None,
                  'available_at':capture['first_seen_at'],'date':None,'unit':'unverified',
                  'values':{},'text':'','source_url':source.url,'raw_json':json.dumps(row,ensure_ascii=False)}
            if source.kind=='quotes':
                keys=(['OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','TradeVolume','TradeValue']
                      if source.provider=='TWSE' else ['Open','High','Low','Close','TradingShares','TransactionAmount'])
                base['date']=day(r['Date']);base['unit']='TWD/share;volume=shares;amount=TWD'
                base['values']=dict(zip(['open','high','low','close','volume','amount'],[number(r[k]) for k in keys]))
                nums=base['values']
                if any(v is not None and Decimal(v)<0 for v in nums.values()):raise ValueError('Negative price/volume')
                for k in ['open','high','low','close']:
                    if nums[k] is not None and Decimal(nums[k])==0:nums[k]=None
                if all(nums[k] is not None for k in ['open','high','low','close']):
                    op,hi,lo,cl=[Decimal(nums[k]) for k in ['open','high','low','close']]
                    if not lo<=min(op,cl)<=max(op,cl)<=hi:raise ValueError('OHLC inconsistent')
            elif source.kind=='market_index':
                base['date']=day(r['Date']);base['unit']='index_points'
                base['values']=dict(zip(['open','high','low','close'],[number(r[k]) for k in ['OpeningIndex','HighestIndex','LowestIndex','ClosingIndex']]))
                if any(v is None or Decimal(v)<=0 for v in base['values'].values()):raise ValueError('Invalid market index')
            elif source.kind=='valuation':
                base['date']=day(r['Date']);base['unit']='PE/PB=ratio;yield=percent'
                keys=['PEratio','PBratio','DividendYield'] if source.provider=='TWSE' else ['PriceEarningRatio','PriceBookRatio','YieldRatio']
                base['values']=dict(zip(['pe','pb','yield_pct'],[number(r[k]) for k in keys]))
            elif source.kind=='revenue':
                period=re.sub(r'\D','',str(r['資料年月']))
                if len(period) not in {5,6}:raise ValueError('Invalid revenue period')
                year=int(period[:-2]);year=year+1911 if year<1911 else year
                base['date']=date(year,int(period[-2:]),1).isoformat();base['unit']='percent'
                base['values']={'revenue_yoy_pct':number(r['營業收入-去年同月增減(%)']),
                                'revenue_mom_pct':number(r['營業收入-上月比較增減(%)'])}
                # Absolute revenue units not yet independently verified; preserve raw only.
            elif source.kind=='announcements':
                d=day(r['發言日期']);t=str(r['發言時間']).strip()
                if re.fullmatch(r'\d{6}',t):t=f'{t[:2]}:{t[2:4]}:{t[4:]}'
                pub=datetime.fromisoformat(d+'T'+t).replace(tzinfo=TAIPEI).isoformat()
                base.update(date=d,published_at=pub,text=clean_text(r['主旨'])[:500])
            elif source.kind=='rss':
                base.update(text=r['title'],published_at=r['published_at'],source_url=r['link'])
            elif source.kind=='master':
                base['text']=str(r.get('公司名稱',r.get('CompanyName','')))
            # Financial statements and conditional datasets retain raw fields but no guessed financial ratios.
            if base['published_at']:
                base['available_at']=max(instant(base['available_at']),instant(base['published_at'])).isoformat()
            if instant(base['available_at'])>instant(cutoff_at):
                issues.append({'source':source.id,'row':index,'reason':'published_after_cutoff'});continue
            base['record_id']=digest(encoded({k:v for k,v in base.items() if k not in {'fetched_at'}}))
            records.append(base)
        except (ValueError,KeyError,TypeError) as e:
            issues.append({'source':source.id,'row':index,'reason':'invalid_row','detail':str(e)[:200]})
    return records,issues
