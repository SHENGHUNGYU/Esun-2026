import json
import pytest
from esun_research.dated_quotes import rows,FIELDS,SOURCE_ID
from esun_research.normalize import normalize
from esun_research.contracts import Source
from esun_research.store import Store

def report(day='20261027'):
    return json.dumps({'stat':'OK','date':day,'tables':[{'fields':FIELDS,'data':[['2330','台積電','1000','50','2400000','2380','2405','2380','2400']]}]}).encode()

def test_dated_report_date_identity_and_raw_table_lineage(tmp_path):
    source=Source(id=SOURCE_ID,url='https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX',provider='TWSE',branch='market',kind='quotes')
    store=Store(tmp_path);cap=store.capture(SOURCE_ID,report(),fetched_at='2026-10-28T01:00:00+08:00')
    cap=store.select(SOURCE_ID,'2026-10-28T02:00:00+08:00')
    result,issues=normalize(source,cap,report(),{'2330':{'market':'TWSE'}},'2026-10-28T02:00:00+08:00')
    assert not issues and result[0]['date']=='2026-10-27'
    assert result[0]['values']['close']=='2400' and result[0]['values']['volume']=='1000'
    assert result[0]['raw_table']==0 and result[0]['raw_row']==0
    with pytest.raises(ValueError,match='date_mismatch'):rows(report(),'2026-10-22')
    store.capture(SOURCE_ID,report('20261028'),fetched_at='2026-10-29T01:00:00+08:00')
    archived=store.select_reference(source,'2026-10-29T02:00:00+08:00','2026-10-27')
    assert archived['ref']==cap['ref'] and archived['selection_basis']=='official_reference_date_archive'
    store.capture(SOURCE_ID,None,'network_error',fetched_at='2026-10-29T01:30:00+08:00')
    assert store.select_reference(source,'2026-10-29T02:00:00+08:00','2026-10-27')['status']=='error'

def test_duplicate_or_changed_table_rejected():
    value=json.loads(report());value['tables']*=2
    with pytest.raises(ValueError,match='table_changed'):rows(json.dumps(value))
    value=json.loads(report());value['tables'][0]['data']*=2
    with pytest.raises(ValueError,match='duplicate_code'):rows(json.dumps(value))
