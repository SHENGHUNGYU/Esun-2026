import json
from pathlib import Path
import httpx
import pytest
from esun_research.contracts import Source, RunRequest
from esun_research.store import Store, encoded
from esun_research.workflow import research, verify
from esun_research.gateway import Gateway
from esun_research.normalize import normalize, day

SOURCE=Source(id='quotes',url='https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL',provider='TWSE',branch='market',kind='quotes')
UNIVERSE={'2330':{'name':'台積電','market':'TWSE'}}
TIME='2026-10-21T08:00:00+08:00'
ROW={'Code':'2330','Date':'1151020','OpeningPrice':'100','HighestPrice':'110','LowestPrice':'90','ClosingPrice':'105','TradeVolume':'1000','TradeValue':'102000'}

def setup(tmp_path):
    store=Store(tmp_path)
    store.capture('quotes',encoded([ROW]),fetched_at=TIME)
    request=RunRequest(run_id='test',cutoff_at=TIME,as_of='2026-10-20',universe_hash='u',registry_hash='s',code_hash='c')
    return store,request

def test_report_and_resume(tmp_path):
    store,req=setup(tmp_path)
    result=research(store,req,[SOURCE],UNIVERSE)
    assert result['status']=='DEGRADED'
    obs=json.loads((tmp_path/'research/test/observations.json').read_text())
    assert obs[0]['values']['daily_average']=='102.0000'
    assert store.json(result['snapshot'])['parquet_ref']
    assert research(store,req,[SOURCE],UNIVERSE)['report']==result['report']
    Path(result['report']).write_text('tampered')
    with pytest.raises(ValueError,match='hash mismatch'):research(store,req,[SOURCE],UNIVERSE)

def test_cutoff_and_failure(tmp_path):
    store,req=setup(tmp_path)
    store.capture('quotes',error='offline',fetched_at='2026-10-21T09:00:00+08:00')
    assert store.select('quotes',TIME)['status']=='ok'
    assert store.select('quotes','2026-10-21T10:00:00+08:00')['status']=='error'
    assert store.select('quotes','2026-10-20T10:00:00+08:00')['status']=='missing'

def test_missing_blocks(tmp_path):
    store=Store(tmp_path)
    _,req=setup(tmp_path/'other')
    result=research(store,req,[SOURCE],UNIVERSE)
    assert result['status']=='BLOCKED'

def test_repair_bounded(tmp_path):
    store,req=setup(tmp_path); calls=[]
    def bad(obs,errors):
        calls.append(1)
        return {'claims':[{'kind':'hypothesis','statement':'外部指令','observation_ids':['fake']}]}
    result=research(store,req,[SOURCE],UNIVERSE,model=bad)
    assert len(calls)==3
    assert result['status']=='DEGRADED'
    assert store.json(result['analysis'])['analysis']=={'claims':[]}

def test_checkpoint_resume(tmp_path):
    store,req=setup(tmp_path)
    partial=research(store,req,[SOURCE],UNIVERSE,interrupt_before=['interpret'])
    assert 'report' not in partial
    result=research(store,req,[SOURCE],UNIVERSE)
    assert Path(result['report']).exists()

def test_raw_integrity_and_request_identity(tmp_path):
    store,req=setup(tmp_path)
    frozen=store.freeze(req,[SOURCE])
    with pytest.raises(ValueError):store.freeze(req.model_copy(update={'code_hash':'changed'}),[SOURCE])
    (store.root/frozen['captures']['quotes']['ref']).write_bytes(b'corrupted')
    with pytest.raises(ValueError,match='hash mismatch'):store.freeze(req,[SOURCE])

def test_schema_and_market(tmp_path):
    store,req=setup(tmp_path);capture=store.select('quotes',TIME)
    rows,issues=normalize(SOURCE,capture,encoded([ROW]),{'2330':{'market':'TPEx'}},TIME)
    assert not rows and issues
    assert day('115/10/20')=='2026-10-20'
    assert verify({'claims':[{'kind':'hypothesis','statement':'漲幅20%','observation_ids':['a']}]},[{'id':'a'}])

def test_gateway_retry_and_auth(monkeypatch):
    calls=[]
    def respond(request):
        calls.append(request)
        return httpx.Response(429 if len(calls)<3 else 200,json=[])
    g=Gateway(httpx.Client(transport=httpx.MockTransport(respond)),sleep=lambda _:None)
    assert g.get(SOURCE)==(b'[]',None)
    assert len(calls)==3
    fm=SOURCE.model_copy(update={'provider':'FinMind','url':'https://api.finmindtrade.com/api/v4/data'})
    monkeypatch.delenv('FINMIND_TOKEN',raising=False)
    assert g.get(fm)[1]=='finmind_token_not_configured'
    assert len(calls)==3
    g.close()

def test_xml_entity_rejected(tmp_path):
    store,req=setup(tmp_path);cap=store.select('quotes',TIME)
    source=SOURCE.model_copy(update={'kind':'rss','provider':'CNA'})
    body=b'<!DOCTYPE rss [<!ENTITY x SYSTEM "file:///etc/passwd">]><rss><channel><item><title>&x;</title></item></channel></rss>'
    rows,issues=normalize(source,cap,body,UNIVERSE,TIME)
    assert not rows and issues

def test_remote_download_restricts_hosts_and_private_credentials():
    from esun_research.gateway import RemoteGateway
    with pytest.raises(ValueError):RemoteGateway('unrelated.example.com')
    gateway=RemoteGateway('120.107.172.133')
    private=SOURCE.model_copy(update={'provider':'FinMind','url':'https://api.finmindtrade.com/api/v4/data'})
    assert gateway.get(private)[1]=='remote_private_provider_or_params_not_supported'
    injected=SOURCE.model_copy(update={'url':'https://openapi.twse.com.tw/v1/test?token=secret'})
    assert gateway.get(injected)[1]=='url_not_allowed'

def test_explicit_reference_archive_never_masks_newest_failure(tmp_path):
    from esun_research.store import Store,encoded
    from esun_research.contracts import Source
    store=Store(tmp_path);source=Source(id='quote',provider='TWSE',branch='market',kind='quotes',url='https://openapi.twse.com.tw/test')
    a=store.capture(source.id,encoded([{'Date':'1151022'}]),fetched_at='2026-10-24T08:00:00+08:00')
    store.capture(source.id,encoded([{'Date':'1151026'}]),fetched_at='2026-10-26T08:00:00+08:00')
    selected=store.select_reference(source,'2026-10-26T09:00:00+08:00','2026-10-22')
    assert selected['ref']==a['ref'] and selected['selection_basis']=='official_reference_date_archive'
    assert selected['fetched_at']=='2026-10-24T08:00:00+08:00'
    store.capture(source.id,None,'http_503',fetched_at='2026-10-26T08:30:00+08:00')
    assert store.select_reference(source,'2026-10-26T09:00:00+08:00','2026-10-22')['status']=='error'
