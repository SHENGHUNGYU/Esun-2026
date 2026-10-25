import base64
import copy
import json
from pathlib import Path
import pytest
from esun_research.event_transport import REPORTS
from esun_research.exchange_events import rows,event

FIXTURES=Path(__file__).parent/'fixtures/events'
FILES=dict(zip(REPORTS,['twse-stop','twse-delisted','twse-reduction','twse-face-change','tpex-delisted','tpex-reduction','tpex-change']))

def report_fixture(sid,empty=False):
    value=json.loads((FIXTURES/(FILES[sid]+'.json')).read_bytes())
    if empty:
        for table in value.get('tables',[value]):
            if 'data' in table:
                table['data']=[]
                for key in ['totalCount','total']:
                    if key in table:table[key]=0
    params={'response':'json'}
    if sid=='TPEx-WEB-DELIST':params.update({'paging-offset':0,'paging-size':10})
    return {'format':'official_web_pages_v1','source_id':sid,'pages':[{'parameters':params,
        'raw_base64':base64.b64encode(json.dumps(value,ensure_ascii=False).encode()).decode()}]}

def test_actual_forecast_dates_ratios_and_no_invented_cash_availability():
    reduction=rows('TWSE-WEB-REDUCTION',report_fixture('TWSE-WEB-REDUCTION'))[0]['values']
    future=event('TWSE-WEB-REDUCTION',reduction,'2026-10-22','2026-10-27')
    assert future['buy_allowed'] and future['new_shares_per_old_share']=='0.79999999'
    suspended=event('TWSE-WEB-REDUCTION',reduction,'2026-11-11','2026-11-12')
    assert not suspended['sell_allowed'] and suspended['cash_per_old_share']=='2.000000'
    assert suspended['cash_payment_date'] is None and suspended['share_rounding_verified'] is False
    resumed=event('TWSE-WEB-REDUCTION',reduction,'2026-11-11','2026-11-23')
    assert not resumed['buy_allowed']
    assert event('TWSE-WEB-REDUCTION',reduction,'2026-11-23','2026-11-24')['buy_allowed']
    face=rows('TWSE-WEB-FACE',report_fixture('TWSE-WEB-FACE'))[0]['values']
    converted=event('TWSE-WEB-FACE',face,'2026-08-26','2026-09-07')
    assert converted['new_shares_per_old_share']=='20.00000000' and not converted['buy_allowed']

def test_tpex_reduction_resume_gap_and_formal_stop_delisting_are_distinct():
    actual=rows('TPEx-WEB-REDUCTION',report_fixture('TPEx-WEB-REDUCTION'))
    star=next(r['values'] for r in actual if r['values']['代號']=='8047')
    assert not event('TPEx-WEB-REDUCTION',star,'2026-10-22','2026-10-27')['sell_allowed']
    stop=rows('TWSE-WEB-STOP',report_fixture('TWSE-WEB-STOP'))[0]['values']
    assert event('TWSE-WEB-STOP',stop,'2026-10-22','2026-10-27')['scope']=='financial_business_abnormality_only'
    assert not event('TWSE-WEB-STOP',stop,'2026-10-22','2026-10-27')['buy_allowed']
    delisted=rows('TPEx-WEB-DELIST',report_fixture('TPEx-WEB-DELIST'))[0]['values']
    assert not event('TPEx-WEB-DELIST',delisted,'2026-10-15','2026-10-16')['sell_allowed']
    before=event('TPEx-WEB-DELIST',delisted,'2026-10-14','2026-10-15')
    assert before['sell_allowed'] and not before['buy_allowed'] and before['last_tradable_date'] is None

def test_explicit_empty_is_valid_but_error_html_and_missing_pages_are_not():
    for sid in REPORTS:assert rows(sid,report_fixture(sid,empty=True))==[]
    sample=report_fixture('TPEx-WEB-DELIST')
    value=json.loads(base64.b64decode(sample['pages'][0]['raw_base64']))
    value['tables'][0]['totalCount']=12
    sample['pages'][0]['raw_base64']=base64.b64encode(json.dumps(value).encode()).decode()
    with pytest.raises(ValueError,match='incomplete_paging'):rows('TPEx-WEB-DELIST',sample)
    sample['pages'][0]['raw_base64']=base64.b64encode(b'<html>security refused</html>').decode()
    with pytest.raises(ValueError):rows('TPEx-WEB-DELIST',sample)
    sample=report_fixture('TPEx-WEB-DELIST');value=json.loads(base64.b64decode(sample['pages'][0]['raw_base64']))
    value['tables'][0]['fields'][0]='Changed code'
    sample['pages'][0]['raw_base64']=base64.b64encode(json.dumps(value).encode()).decode()
    with pytest.raises(ValueError,match='fields_changed'):rows('TPEx-WEB-DELIST',sample)

def test_pagination_full_count_offsets_and_duplicate_pages():
    sample=report_fixture('TPEx-WEB-DELIST');value=json.loads(base64.b64decode(sample['pages'][0]['raw_base64']))
    originals=value['tables'][0]['data'];data=[[*r] for r in originals]+[[str(9100+i),*originals[0][1:]] for i in range(5)]
    sample['pages']=[]
    for offset in [0,10]:
        page=copy.deepcopy(value);page['tables'][0].update(data=data[offset:offset+10],totalCount=12)
        sample['pages'].append({'parameters':{'paging-offset':offset,'paging-size':10},'raw_base64':base64.b64encode(json.dumps(page).encode()).decode()})
    assert len(rows('TPEx-WEB-DELIST',sample))==12
    sample['pages'][1]['parameters']['paging-offset']=0
    with pytest.raises(ValueError,match='offset_mismatch'):rows('TPEx-WEB-DELIST',sample)
