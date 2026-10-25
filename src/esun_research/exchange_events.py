"""Strict public web-report envelopes and conservative event windows."""
import base64
import json
import subprocess
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from .contracts import now
from .event_transport import REPORTS
from .normalize import day,number
from .store import encoded

FIELDS={
 'TWSE-WEB-STOP':['證券代號','證券名稱','違反營業細則條款','停止買賣原因','停止買賣開始日期'],
 'TWSE-WEB-DELIST':['終止上市日期','公司名稱','上市編號'],
 'TWSE-WEB-REDUCTION':['停止買賣日期','股票代號','名稱','恢復買賣日期','減資換股率','減資原因','每股退還股款(元)','減資後現金增資配股率','現金增資認購價(元)','詳細資料','恢復買賣參考價','參考價試算'],
 'TWSE-WEB-FACE':['停止買賣日期','股票代號','名稱','恢復買賣日期','變更股票面額換股率','變更前面額','變更後面額','詳細資料','恢復買賣參考價','參考價試算'],
 'TPEx-WEB-DELIST':['股票代號','公司名稱','終止上櫃日期','終止上櫃原因','公司資料網址'],
 'TPEx-WEB-REDUCTION':['代號','名稱','停止買賣日期','減資換股率','每股退還股款(元)','減資原因','恢復買賣日期','減資後現金增資配股率','現金增資認購價(元)','恢復買賣參考價'],
 'TPEx-WEB-FACE':['證券代號','證券名稱','停止買賣日期','變更股票面額換股率','變更前股票面額','變更後股票面額','恢復買賣日期','恢復買賣參考價'],
}

def download(source,ssh_host=None):
    from . import event_transport
    if source.id not in REPORTS or source.url!=REPORTS[source.id][0]:return None,'unverified_event_report'
    args=[source.id,now()[:4]]
    if ssh_host:
        from .gateway import RemoteGateway
        if ssh_host not in RemoteGateway.ALLOWED_HOSTS:raise ValueError('unapproved_ssh_host')
        command=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=8',
            '-o','ConnectionAttempts=1','nelson@'+ssh_host,'python3','-',*args]
        code=Path(event_transport.__file__).read_bytes()
    else:command=[sys.executable,'-m','esun_research.event_transport',*args];code=None
    try:
        result=subprocess.run(command,input=code,capture_output=True,timeout=70)
        if result.returncode or len(result.stdout)>35_000_000:return None,'event_report_worker_failed'
        value=json.loads(result.stdout)
        return (encoded(value['body']),None) if value['body'] is not None and not value['error'] else (None,'event_report_worker_failed')
    except (subprocess.TimeoutExpired,ValueError,KeyError):return None,'event_report_worker_failed'

def rows(sid,payload):
    if not isinstance(payload,dict) or payload.get('format')!='official_web_pages_v1' or payload.get('source_id')!=sid:raise ValueError('invalid_event_report_wrapper')
    pages=payload['pages'];output=[];total=None;seen=set()
    if not pages:raise ValueError('empty_event_report_pages')
    if sid!='TPEx-WEB-DELIST' and len(pages)!=1:raise ValueError('unexpected_event_pages')
    for page_index,page in enumerate(pages):
        value=json.loads(base64.b64decode(page['raw_base64'],validate=True))
        if not isinstance(value,dict):raise ValueError('event_report_not_object')
        if str(value.get('stat',value.get('status',''))).lower()!='ok':raise ValueError('event_report_status_failed')
        if 'tables' in value:
            tables=[t for t in value['tables'] if t]
            if len(tables)!=1:raise ValueError('event_report_table_changed')
            table=tables[0]
        else:table=value
        if table['fields']!=FIELDS[sid]:raise ValueError('event_report_fields_changed')
        if not isinstance(table['data'],list):raise ValueError('event_report_rows_not_array')
        if sid=='TPEx-WEB-DELIST':
            count=table['totalCount']
            if type(count) is not int or count<0 or (total is not None and total!=count):raise ValueError('event_paging_total_changed')
            total=count
            if page['parameters']['paging-offset']!=len(output) or page['parameters']['paging-size']!=10:raise ValueError('event_paging_offset_mismatch')
            if page_index<len(pages)-1 and len(table['data'])!=10:raise ValueError('event_report_short_intermediate_page')
        elif 'totalCount' in table and (type(table['totalCount']) is not int or table['totalCount']!=len(table['data'])):raise ValueError('event_report_incomplete_rows')
        elif sid=='TWSE-WEB-DELIST' and (type(table['total']) is not int or table['total']!=len(table['data'])):raise ValueError('event_report_incomplete_rows')
        for index,raw in enumerate(table['data']):
            if not isinstance(raw,list) or len(raw)!=len(FIELDS[sid]):raise ValueError('event_report_row_shape_changed')
            key=json.dumps(raw,ensure_ascii=False,sort_keys=True)
            if key in seen:raise ValueError('duplicate_event_report_row')
            seen.add(key);output.append({'values':dict(zip(FIELDS[sid],raw)),'page':page_index,'page_row':index})
    if total is not None and total!=len(output):raise ValueError('event_report_incomplete_paging')
    return output

def event(sid,row,reference,trade):
    """No automatic share conversion or invented payment date."""
    role=REPORTS[sid][2]
    code=str(next(row[k] for k in ['證券代號','股票代號','代號','上市編號'] if k in row)).strip()
    detail={'code':code,'kind':role,'buy_allowed':True,'sell_allowed':True}
    if role=='formal_stop':
        start=day(row['停止買賣開始日期']);affected=start<=trade
        detail.update(start=start,resume=None,scope='financial_business_abnormality_only')
    elif role=='delist':
        effective=day(row['終止上市日期' if sid.startswith('TWSE') else '終止上櫃日期'])
        # End-date alone cannot establish the last tradable day. Exclude new
        # buys before announced delisting; block both sides from that date.
        detail.update(effective_date=effective,buy_allowed=False,last_tradable_date=None)
        affected=effective<=trade
    else:
        start=day(row['停止買賣日期']);resume=day(row['恢復買賣日期'])
        if start>=resume:raise ValueError('invalid_action_interval')
        ratio=number(row['減資換股率' if role=='reduction' else '變更股票面額換股率'])
        if ratio is None or Decimal(ratio)<=0:raise ValueError('invalid_action_ratio')
        detail.update(start=start,resume=resume,new_shares_per_old_share=ratio,share_rounding_verified=False)
        if role=='reduction':
            cash=number(row['每股退還股款(元)'])
            if cash is not None and Decimal(cash)<0:raise ValueError('invalid_action_cash')
            detail.update(cash_per_old_share=cash,cash_payment_date=None)
        else:
            before=number(row['變更前面額' if sid.startswith('TWSE') else '變更前股票面額'])
            after=number(row['變更後面額' if sid.startswith('TWSE') else '變更後股票面額'])
            if before is None or after is None or Decimal(after)<=0 or abs(Decimal(before)/Decimal(after)-Decimal(ratio))>Decimal('.00000001'):raise ValueError('face_change_ratio_mismatch')
            detail.update(old_face_value=before,new_face_value=after)
        # Block active suspension and any reference-to-trade interval crossing
        # the conversion/resumption boundary. Future announcements are retained.
        affected=(start<=trade<resume) or (reference<resume<=trade) or (reference<start<=trade)
    if affected:detail.update(buy_allowed=False,sell_allowed=False)
    detail['policy']=('block_until_official_account_and_reference_adjustment_verified' if affected else
        'internal_avoid_new_buys_before_announced_delisting' if role=='delist' else 'announced_future_event_or_outside_reference_gap')
    return detail
