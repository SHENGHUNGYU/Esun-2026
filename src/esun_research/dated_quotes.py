"""Date-specific official TWSE closing report; preserve the original response."""
import json
import shlex
import subprocess
from datetime import date
import httpx

SOURCE_ID='TWSE-DATED-QUOTES'
URL='https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX'
FIELDS=['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價','收盤價']

def rows(body, reference=None):
    value=json.loads(body)
    if value.get('stat')!='OK':raise ValueError('twse_dated_report_not_ok')
    actual=date.fromisoformat(str(value['date'])[:4]+'-'+str(value['date'])[4:6]+'-'+str(value['date'])[6:8]).isoformat()
    if reference and actual!=reference:raise ValueError('twse_dated_report_date_mismatch')
    tables=[(i,t) for i,t in enumerate(value.get('tables',[])) if set(FIELDS)<=set(t.get('fields') or [])]
    if len(tables)!=1:raise ValueError('twse_dated_quote_table_changed')
    table_index,table=tables[0];result=[];seen=set()
    for index,row in enumerate(table['data']):
        if len(row)!=len(table['fields']):raise ValueError('twse_dated_row_shape_changed')
        item=dict(zip(table['fields'],row));code=str(item['證券代號']).strip()
        if code in seen:raise ValueError('twse_dated_duplicate_code')
        seen.add(code)
        result.append({'Date':actual,'Code':code,'Name':item['證券名稱'],
            **dict(zip(['OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','TradeVolume','TradeValue'],
                [item[k] for k in ['開盤價','最高價','最低價','收盤價','成交股數','成交金額']])),
            '_raw_table':table_index,'_raw_row':index,'_raw_values':row})
    if not result:raise ValueError('twse_dated_empty_report')
    return result

def download(reference, ssh_host=None):
    reference=date.fromisoformat(reference).isoformat()
    params={'date':reference.replace('-',''),'type':'ALLBUT0999','response':'json'}
    if ssh_host:
        from .gateway import RemoteGateway
        if ssh_host not in RemoteGateway.ALLOWED_HOSTS:raise ValueError('SSH host not in project inventory')
        url=str(httpx.URL(URL,params=params))
        command=shlex.join(['curl','--silent','--show-error','--fail','--max-time','30','--max-filesize','5000000',url])
        r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=8',
            'nelson@'+ssh_host,command],capture_output=True,timeout=40)
        if r.returncode:raise ValueError('twse_dated_remote_download_failed')
        body=r.stdout
    else:
        r=httpx.get(URL,params=params,timeout=25,follow_redirects=False);r.raise_for_status();body=r.content
    if len(body)>5_000_000:raise ValueError('twse_dated_response_too_large')
    rows(body,reference)
    return body
