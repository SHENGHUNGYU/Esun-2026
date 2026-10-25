import base64
import json
from pathlib import Path
from decimal import Decimal
import pytest
from esun_research.issuer_holdings import parse, collect, SUPPORTED
from esun_research.store import Store
from esun_research.contracts import now

FIXTURES=Path(__file__).parent/'fixtures/issuers'

def record(name, label=None):
    meta=json.loads((FIXTURES/(name+'.meta.json')).read_bytes())
    return {**meta,'label':label or name,'method':meta.get('method','GET'),
        'request':meta.get('request',{}),'raw_base64':base64.b64encode((FIXTURES/(name+'.json')).read_bytes()).decode()}

@pytest.mark.parametrize('issuer,code,name,identity,count,day',[
    ('allianz','00984A','allianz-00984A-holdings','allianz-overview-public',80,'2026-10-22'),
    ('allianz','00993A','allianz-00993A-holdings','allianz-overview-public',50,'2026-10-22'),
    ('allianz','00402A','allianz-00402A-holdings','allianz-overview-public',50,'2026-10-21'),
    ('nomura','00980A','nomura-00980A',None,50,'2026-10-22'),
    ('ctbc','00995A','ctbc-00995A-holdings','ctbc-etf-list',55,'2026-10-22'),
    ('ctbc','00983A','ctbc-00983A-holdings','ctbc-etf-list',43,'2026-10-21'),
    ('capital','00982A','capital399-holdings','capital399-basic',57,'2026-10-22'),
])
def test_actual_public_tables_keep_full_rows_dates_and_namespaces(issuer,code,name,identity,count,day):
    benchmark,raw=parse(issuer,code,record(name),record(identity) if identity else None)
    assert len(benchmark.holdings)==count and str(benchmark.valuation_date)==day
    assert benchmark.complete_equity_table and sum(x.weight_nav for x in benchmark.holdings)<=Decimal('1.0001')
    if day=='2026-10-21':assert all(x.security_id.startswith('US:') for x in benchmark.holdings)
    if identity:assert benchmark.identity_raw_sha256 and not benchmark.nav_source_raw_sha256
    assert 'token' not in benchmark.model_dump_json().lower()

def test_identity_changed_columns_and_unknown_exchange_fail_closed():
    source=record('allianz-00984A-holdings');proof=record('allianz-overview-public')
    with pytest.raises(ValueError):parse('allianz','00993A',source,proof)
    value=json.loads(base64.b64decode(source['raw_base64']))
    table=next(x for x in value['Entries']['Data']['Table'] if x['TableTitle'].startswith('股票 ('))
    table['Columns'][1]['Name']='基金代號'
    source['raw_base64']=base64.b64encode(json.dumps(value).encode()).decode()
    with pytest.raises(ValueError,match='columns_changed'):parse('allianz','00984A',source,proof)
    table['Columns'][1]['Name']='股票代號';table['Rows'][0][1]='2330 JP'
    source['raw_base64']=base64.b64encode(json.dumps(value).encode()).decode()
    with pytest.raises(ValueError,match='unknown_security_market'):parse('allianz','00984A',source,proof)

def test_failed_refresh_cannot_fall_back_to_previous_benchmark(tmp_path):
    store=Store(tmp_path)
    codes=[code for group in SUPPORTED.values() for code in group]
    store.capture('ETF:00984A',b'prior success')
    def failed(*args):return {'records':[],'error':'issuer_http_403'}
    result=collect(store,'2026-10-22','2026-10-27',codes,set(),downloader=failed)
    assert len(result)==11 and all(r['status']=='error' for r in result)
    assert store.select('ETF:00984A',now())['status']=='error'
    assert store.select('ETF:00984A',now())['error']=='issuer_http_403'

def test_successful_import_keeps_original_proof_and_other_valuation_day(tmp_path):
    store=Store(tmp_path);codes=[c for group in SUPPORTED.values() for c in group]
    def fixtures(issuer,*args):
        if issuer!='allianz':return {'records':[],'error':'issuer_http_503'}
        return {'error':None,'records':[record('allianz-overview-public','identity'),
            *[record('allianz-'+c+'-holdings',c) for c in SUPPORTED['allianz']]]}
    result=collect(store,'2026-10-22','2026-10-27',codes,{'etf.allianzgi.com.tw'},downloader=fixtures)
    rows={r['code']:r for r in result}
    assert rows['00984A']['status']=='ok' and rows['00402A']['status']=='date_mismatch'
    wrapper=store.json(rows['00984A']['ref']);sha=wrapper['benchmark']['identity_raw_sha256']
    assert store.read(wrapper['supporting_refs'][sha])==(FIXTURES/'allianz-overview-public.json').read_bytes()
    assert wrapper['imported_at']>=wrapper['benchmark']['fetched_at']

def test_worker_never_returns_anonymous_session_or_exception_urls(monkeypatch,capsys):
    from esun_research import issuer_transport as worker
    class Response:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def read(self,*args):return b'{"nested":{"token":"do-not-persist"}}'
    class Client:
        def open(self,*args,**kwargs):return Response()
    monkeypatch.setattr(worker,'build_opener',lambda *args:Client())
    with pytest.raises(ValueError,match='unexpected_credential_field'):
        worker.fetch('nomura','2026-10-22','2026-10-27')
    def failed(*args):raise ValueError('https://official.example/?token=do-not-persist')
    monkeypatch.setattr(worker,'fetch',failed)
    monkeypatch.setattr(worker.sys,'argv',['worker','nomura','2026-10-22','2026-10-27'])
    worker.main();output=capsys.readouterr().out
    assert 'do-not-persist' not in output and json.loads(output)['error']=='issuer_transport_failed'
