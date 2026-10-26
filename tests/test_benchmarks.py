import json
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from pathlib import Path
import pytest
from esun_research.benchmarks import Benchmark,import_benchmark,evaluate,compare
from esun_research.contracts import now
from esun_research.store import Store,encoded,digest

RAW=b'official actual equity table'

def sample(code='00410A'):
    return {'schema_version':'1.0','benchmark_code':code,'valuation_date':'2026-10-22','pcf_applicable_date':'2026-10-27',
        'fetched_at':(datetime.now(timezone.utc)-timedelta(minutes=1)).isoformat(),'source_url':'https://official.test/holdings','source_name':'Official actual table',
        'evidence_kind':'official_actual_holdings_table','complete_equity_table':True,'nav_twd':'1000000','raw_sha256':digest(RAW),
        'holdings':[{'asset_type':'equity','security_id':'TW:'+str(1000+i),'weight_nav':'.03','shares':1000,'raw_row':i} for i in range(20)]}

def test_two_views_are_distinct_and_do_not_merge_adr():
    assert compare({'TW:2330':D('.2')},{'TW:2330':D('.1')})['normalized_top15']=='0'
    assert compare({'TW:2330':D('.2')},{'TW:2330':D('.1')})['raw_nav_top15']=='0.05'
    assert compare({'TW:2330':D('.2')},{'US:TSM':D('.1')})['normalized_top15']=='1'
    with pytest.raises(ValueError):compare({'TW:2330':D(0)},{'TW:2330':D('.1')})

def test_import_checks_hash_actual_table_and_expected_issuer(tmp_path):
    store=Store(tmp_path);value=sample()
    import_benchmark(store,encoded(value),RAW,['00410A'],{'official.test'})
    for changed,raw,codes,hosts in [(value,b'bad',['00410A'],{'official.test'}),(value,RAW,['00980A'],{'official.test'}),(value,RAW,['00410A'],{'untrusted.test'}),
            ({**value,'evidence_kind':'pcf_basket_only'},RAW,['00410A'],{'official.test'}),({**value,'complete_equity_table':False},RAW,['00410A'],{'official.test'})]:
        with pytest.raises(ValueError):import_benchmark(store,encoded(changed),raw,codes,hosts)

def test_partial_coverage_stays_unverified_and_cutoff_is_import_time(tmp_path):
    store=Store(tmp_path);value=sample();capture=import_benchmark(store,encoded(value),RAW,['00410A'],{'official.test'})
    report=evaluate(store,[capture['ref']],{'2330':'.2'},['00410A','00980A'],'2026-10-22',now(),D('.2'))
    assert report['validated_count']==1 and report['missing_codes']==['00980A'] and not report['official_pass']
    assert not report['internal_all_pass']
    cutoff=(datetime.now(timezone.utc)-timedelta(minutes=10)).isoformat()
    assert evaluate(store,[capture['ref']],{'2330':'.2'},['00410A'],'2026-10-22',cutoff,D('.2'))['validated_count']==0
    assert evaluate(store,[capture['ref']],{'2330':'.2'},['00410A'],'2026-10-23',now(),D('.2'))['validated_count']==0

def test_zero_rounded_holdings_retained_but_duplicate_identifiers_rejected():
    value=sample();value['holdings'][0]['weight_nav']='0';assert Benchmark.model_validate(value).holdings[0].shares==1000
    value['holdings'].append(value['holdings'][0])
    with pytest.raises(ValueError):Benchmark.model_validate(value)

def test_unresolved_date_cannot_be_used_even_when_calendar_date_matches(tmp_path):
    store=Store(tmp_path);value={**sample(),'valuation_date_usable':False}
    capture=import_benchmark(store,encoded(value),RAW,['00410A'],{'official.test'})
    report=evaluate(store,[capture['ref']],{'2330':'.2'},['00410A'],'2026-10-22',now(),D('.2'))
    assert report['validated_count']==0 and report['problems'][0]['reason']=='benchmark_date_requires_confirmation'

def test_derived_pcf_date_requires_archived_primary_prospectus(tmp_path):
    store=Store(tmp_path);value=sample();proof=b'official next-business-day timing definition'
    value.update(valuation_date_basis='official_pcf_timing_inference',prospectus_source_url='https://official.test/prospectus.pdf',prospectus_raw_sha256=digest(proof))
    with pytest.raises(ValueError,match='supporting_raw'):import_benchmark(store,encoded(value),RAW,['00410A'],{'official.test'})
    capture=import_benchmark(store,encoded(value),RAW,['00410A'],{'official.test'},{digest(proof):proof})
    report=evaluate(store,[capture['ref']],{'2330':'.2'},['00410A'],'2026-10-22',now(),D('.2'))
    assert report['validated_count']==1 and report['results'][0]['valuation_date_basis']=='official_pcf_timing_inference'
    assert not report['official_pass']
