import json
from pathlib import Path
import httpx
import pandas as pd
import pytest
from esun_research.history import normalize_month,months,HistoricalGateway,collect_history,dataset_folder
from esun_research.store import Store
from esun_research.contracts import now

ROOT=Path(__file__).parent/'fixtures/history'

def raw(name):return (ROOT/name).read_bytes()

def test_actual_price_tables_keep_units_scope_and_vintage_limitations():
    tw=normalize_month(raw('twse-2330-202609.json'),'TWSE','2330','2026-09',now(),'objects/raw.bin')
    tp=normalize_month(raw('tpex-3105-202609.json'),'TPEX','3105','2026-09',now(),'objects/raw.bin')
    assert len(tw)==len(tp)==20
    assert tw[0]['volume_shares']=='31855287' and tw[0]['amount_twd']=='77463413685'
    assert tp[0]['volume_shares']=='56845000' and tp[0]['amount_twd']=='27034034000'
    assert tw[0]['turnover_scope']!=tp[0]['turnover_scope']
    assert all(r['published_at'] is None and r['historical_first_seen_at'] is None for r in tw+tp)
    assert next(r for r in tw if r['date']=='2026-09-16')['corporate_action_marker']

def test_history_identity_month_schema_and_ohlc_are_not_silently_coerced():
    source=json.loads(raw('twse-2330-202609.json'))
    changes=[lambda v:v.update(date='20260801'),lambda v:v.update(title='115年09月 2317 日行情'),
        lambda v:v['fields'].__setitem__(1,'lots instead of shares'),lambda v:v.update(total=19),
        lambda v:v['data'][0].__setitem__(4,'1.00'),lambda v:v['data'][1].__setitem__(0,'115/09/01')]
    for change in changes:
        value=json.loads(json.dumps(source));change(value)
        with pytest.raises(ValueError):normalize_month(json.dumps(value).encode(),'TWSE','2330','2026-09',now(),'raw')
    assert len(months('2026-04','2026-09'))==6
    for start,end in [('2026-13','2026-13'),('9999-01','9999-01'),('2026-09','2026-04'),('2009-12','2010-01')]:
        with pytest.raises(ValueError):months(start,end)

def test_observed_listing_star_is_preserved_as_structural_boundary():
    value=json.loads(raw('tpex-3105-202609.json'));value['tables'][0]['data'][0][0]='115/09/01*'
    result=normalize_month(json.dumps(value).encode(),'TPEX','3105','2026-09',now(),'raw')
    assert result[0]['date']=='2026-09-01' and result[0]['raw_date']=='115/09/01*'
    assert result[0]['listing_boundary_marker'] and not result[1]['listing_boundary_marker']
    value['tables'][0]['data'][0][0]='115/09/01?'
    with pytest.raises(ValueError):normalize_month(json.dumps(value).encode(),'TPEX','3105','2026-09',now(),'raw')

class FixtureGateway:
    def __init__(self):self.calls=0;self.blocked={}
    def get(self,*args):self.calls+=1;return raw('twse-2330-202609.json'),None,200

def test_cached_resume_preserves_actual_fetch_time_and_reproducible_parquet(tmp_path):
    store=Store(tmp_path);gateway=FixtureGateway();universe={'2330':{'market':'TWSE'}}
    report=collect_history(store,universe,'2026-09','2026-09',gateway)
    assert report['status']=='COMPLETE' and report['normalized_rows']==20 and gateway.calls==1
    assert report['strict_pit_verified'] is False and report['strategy_backtest_ready'] is False
    folder=dataset_folder(store.root,'2026-09','2026-09')
    first=pd.read_parquet(folder/'daily-prices.parquet');sha=report['parquet_sha256']
    resumed=collect_history(store,universe,'2026-09','2026-09',gateway)
    assert gateway.calls==1 and resumed['results'][0]['cache_hit']
    assert sha==resumed['parquet_sha256']
    assert first.equals(pd.read_parquet(folder/'daily-prices.parquet'))
    other=collect_history(store,universe,'2026-08','2026-09',gateway)
    assert other['status']=='INCOMPLETE' and gateway.calls==2
    assert first.equals(pd.read_parquet(folder/'daily-prices.parquet'))

def test_http_403_stops_that_market_without_retry_or_proxy_change():
    calls=[]
    def handler(request):calls.append(request);return httpx.Response(403,content=b'access denied')
    gateway=HistoricalGateway(httpx.Client(transport=httpx.MockTransport(handler)),sleep=lambda t:None)
    assert gateway.get('TWSE','2330','2026-09')[1]=='history_http_403'
    assert gateway.get('TWSE','2317','2026-09')[1]=='history_http_403'
    assert len(calls)==1
    assert gateway.get('TPEX','3105','2026-09')[1]=='history_http_403' and len(calls)==2

def test_corrupt_cache_does_not_fetch_over_or_reuse_old_derived_data(tmp_path):
    store=Store(tmp_path);gateway=FixtureGateway();universe={'2330':{'market':'TWSE'}}
    result=collect_history(store,universe,'2026-09','2026-09',gateway)
    captured=store.json(result['results'][0]['capture_ref'])
    (store.root/captured['raw_ref']).write_bytes(b'tampered source')
    report=collect_history(store,universe,'2026-09','2026-09',gateway)
    assert report['status']=='INCOMPLETE' and gateway.calls==1
    assert not (dataset_folder(store.root,'2026-09','2026-09')/'daily-prices.parquet').exists()

def test_verified_empty_month_is_distinct_from_security_html_and_failed_request(tmp_path):
    class Empty(FixtureGateway):
        def get(self,*args):
            value=json.loads(raw('twse-2330-202609.json'));value.update(data=[],total=0)
            return json.dumps(value).encode(),None,200
    store=Store(tmp_path);r=collect_history(store,{'2330':{'market':'TWSE'}},'2026-09','2026-09',Empty())
    assert r['explicit_empty_months']==1 and r['normalized_rows']==0 and not r['strategy_backtest_ready']
    with pytest.raises(ValueError):normalize_month(b'<html>security refused</html>','TWSE','2330','2026-09',now(),'raw')
