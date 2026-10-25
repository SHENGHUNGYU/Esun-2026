"""Standalone public exchange-report downloader; no login or write requests."""
import base64
import json
import sys
import time
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler

REPORTS={
 'TWSE-WEB-STOP':('https://www.twse.com.tw/rwd/zh/violation/stop','GET','formal_stop'),
 'TWSE-WEB-DELIST':('https://www.twse.com.tw/rwd/zh/company/suspendListing','GET','delist'),
 'TWSE-WEB-REDUCTION':('https://www.twse.com.tw/rwd/zh/reducation/TWTAVU','GET','reduction'),
 'TWSE-WEB-FACE':('https://www.twse.com.tw/rwd/zh/change/TWTB7U','GET','face_change'),
 'TPEx-WEB-DELIST':('https://www.tpex.org.tw/www/zh-tw/company/deListed','POST','delist'),
 'TPEx-WEB-REDUCTION':('https://www.tpex.org.tw/www/zh-tw/bulletin/decap','POST','reduction'),
 'TPEx-WEB-FACE':('https://www.tpex.org.tw/www/zh-tw/bulletin/pvChgAnn','POST','face_change'),
}

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args):return None

def fetch(sid,year):
    url,method,role=REPORTS[sid]
    year=int(year)
    if not 2001<=year<=2100:raise ValueError('invalid_report_year')
    params={'response':'json'}
    if sid=='TWSE-WEB-DELIST':params['date']=str(year)+'0101'
    if sid=='TPEx-WEB-DELIST':params.update(code='',date='',reason='-1',**{'paging-offset':0,'paging-size':10})
    client=build_opener(NoRedirect());pages=[];offset=0;expected=None
    while True:
        if pages:time.sleep(1)
        encoded=urlencode(params).encode()
        request=Request(url+('?' + encoded.decode() if method=='GET' else ''),
            data=encoded if method=='POST' else None,
            headers={'Content-Type':'application/x-www-form-urlencoded'})
        with client.open(request,timeout=20) as response:raw=response.read(25_000_001)
        if len(raw)>25_000_000:raise ValueError('event_report_too_large')
        value=json.loads(raw)
        pages.append({'parameters':dict(params),'raw_base64':base64.b64encode(raw).decode()})
        if sid!='TPEx-WEB-DELIST':break
        table=value['tables'][0];total=table['totalCount'];count=len(table['data'])
        if type(total) is not int or total<0 or (expected is not None and total!=expected):raise ValueError('event_paging_total_changed')
        expected=total;offset+=count
        if offset==total:break
        if count!=10 or offset>total or len(pages)>=100:raise ValueError('event_report_incomplete_paging')
        params['paging-offset']=offset
    return {'format':'official_web_pages_v1','source_id':sid,'pages':pages}

def main():
    try:result={'body':fetch(sys.argv[1],sys.argv[2]),'error':None}
    except Exception:result={'body':None,'error':'official_event_report_download_failed'}
    print(json.dumps(result))

if __name__=='__main__':main()
