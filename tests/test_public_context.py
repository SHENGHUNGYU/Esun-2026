import json
import httpx
import pytest
from esun_research.store import Store,encoded
from esun_research.public_context import contracts,parse,collect,build

CUT='2026-11-04T07:00:00+08:00'

def test_fx_pit_and_schema(tmp_path):
    s=Store(tmp_path);source=next(x for x in contracts(2026) if x['id']=='CBC-USDTWD')
    body=encoded([{'日期':'20261103','NTD_USD':'31.2'},{'日期':'20261105','NTD_USD':'31.1'}]);cap=s.capture('WORLD:CBC-USDTWD',body,fetched_at=CUT)
    rows=parse(source,body,cap,CUT)
    assert len(rows)==1 and rows[0]['values']['USDTWD']=='31.2' and rows[0]['available_at']==CUT
    with pytest.raises(ValueError,match='capture_after_cutoff'):parse(source,body,cap,'2026-11-03T07:00:00+08:00')
    with pytest.raises(ValueError,match='schema'):parse(source,b'[{"date":"20261103"}]',cap,CUT)
    assert not build(s,'2026-11-03T07:00:00+08:00')['observations']


def test_latest_error_not_silently_replaced_and_staleness(tmp_path):
    s=Store(tmp_path);s.capture('WORLD:CBC-USDTWD',encoded([{'日期':'20261103','NTD_USD':'31.2'}]),fetched_at=CUT)
    stale=build(s,'2026-11-05T07:00:00+08:00')
    assert not stale['observations'] and next(x for x in stale['sources'] if x['id']=='CBC-USDTWD')['status']=='stale'
    s.capture('WORLD:CBC-USDTWD',b'<html>blocked</html>',error='schema',fetched_at='2026-11-04T07:01:00+08:00')
    result=build(s,'2026-11-04T07:02:00+08:00')
    assert not result['observations'] and next(x for x in result['sources'] if x['id']=='CBC-USDTWD')['status']=='error'


def test_collect_html_errors_captured_and_no_key_calls(tmp_path):
    s=Store(tmp_path);urls=[]
    def respond(request):urls.append(str(request.url));return httpx.Response(200,text='<html>security block</html>')
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:result,ident=collect(s,client)
    assert all(x['status']=='error' for x in result['sources'] if x['enabled'])
    assert not any('stlouisfed' in url for url in urls) and len(urls)==9
    assert all(x.get('raw_ref') for x in result['sources'] if x['enabled'])


def test_rss_future_and_treasury_units(tmp_path):
    s=Store(tmp_path);source=next(x for x in contracts(2026) if x['id']=='FED-POLICY')
    body=b'<rss><channel><item><title>Policy</title><pubDate>Tue, 03 Nov 2026 18:00:00 GMT</pubDate><link>https://www.federalreserve.gov/newsevents/test.htm</link></item><item><pubDate>Thu, 05 Nov 2026 18:00:00 GMT</pubDate></item></channel></rss>'
    cap=s.capture('test',body,fetched_at=CUT);rows=parse(source,body,cap,CUT)
    assert len(rows)==1 and rows[0]['observed_date']=='2026-11-04'
    source=next(x for x in contracts(2026) if x['id']=='UST-NOMINAL')
    body=b'<feed xmlns="http://www.w3.org/2005/Atom" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices"><entry><content><m:properties><d:NEW_DATE>2026-11-03T00:00:00</d:NEW_DATE><d:BC_2YEAR>3.4</d:BC_2YEAR><d:BC_10YEAR>4.1</d:BC_10YEAR></m:properties></content></entry></feed>'
    cap=s.capture('test',body,fetched_at=CUT);rows=parse(source,body,cap,CUT)
    assert rows[0]['values']['BC_10YEAR']=='4.1' and rows[0]['unit']=='percent_per_year'


def test_treasury_contracts_use_documented_path():
    assert all('/resource-center/data-chart-center/' in x['url'] for x in contracts(2026) if x['parser']=='treasury')


def test_context_api_auth_and_raw_evidence(tmp_path):
    from fastapi.testclient import TestClient
    from esun_research.application import create_app
    app=create_app(tmp_path,model_config=None);client=TestClient(app)
    assert client.get('/api/public-context').json()['status']=='NOT_STARTED'
    assert client.post('/api/public-context/collect').status_code==403
    ref=app.state.store.put(b'<rss/>','bin')
    assert client.get('/api/public-context/evidence',params={'ref':ref}).content==b'<rss/>'
    assert client.get('/api/public-context/evidence',params={'ref':'../../etc/passwd'}).status_code==400
    assert client.get('/api/research-board').json()=={'reports':[]}
