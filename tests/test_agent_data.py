import copy
import json
from pathlib import Path
import pytest
from esun_research.agent_data import build_bundle,validate_bundle,FLOW_URLS
from esun_research.store import Store,encoded
from esun_research.contracts import now
from esun_research.history import normalize_month,request_for


def inputs(tmp_path):
    store=Store(tmp_path);when=now();hist=[];quotes=[]
    folder=Path(__file__).parent/'fixtures/history'
    for market,code,name,sid in [('TWSE','2330','twse-2330-202609.json','TWSE-043'),('TPEX','3105','tpex-3105-202609.json','TPEx-006')]:
        body=(folder/name).read_bytes();raw=store.put(body,'bin');url,params=request_for(market,code,'2026-09')
        cap={'market':market,'code':code,'month':'2026-09','url':url,'parameters':params,'http_status':200,'fetched_at':when,'raw_ref':raw}
        hist.append(store.put_json(cap));last=normalize_month(body,market,code,'2026-09',when,raw)[-1]
        values=[last[f] for f in ['open_twd','high_twd','low_twd','close_twd','volume_shares','amount_twd']]
        keys=['OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','TradeVolume','TradeValue'] if market=='TWSE' else ['Open','High','Low','Close','TradingShares','TransactionAmount']
        from esun_research.cli import settings
        declared=next(s for s in settings()[0] if s.id==sid)
        row={key:'' for key in declared.fields};row.update(dict(zip(keys,values)));row.update(Date='1150930',**({'Code':code} if market=='TWSE' else {'SecuritiesCompanyCode':code}))
        capture=store.capture(sid,encoded([row]),fetched_at=when);quotes.append({'source_id':sid,'raw_ref':capture['ref']})
    raw=store.put_json({'stat':'OK','date':'20260930','fields':['證券代號','外陸資買賣超股數(不含外資自營商)','投信買賣超股數','自營商買賣超股數'],
        'data':[['2330','1000','-2000','0']]})
    flow=store.put_json({'provider':'TWSE','url':FLOW_URLS['TWSE'],'http_status':200,'fetched_at':when,'raw_ref':raw,'parameters':{'date':'20260930'}})
    return store,when,hist,[flow],quotes


def test_factors_recompute_from_original_history_flow_and_reference_quote(tmp_path):
    store,when,hist,flows,quotes=inputs(tmp_path)
    bundle=build_bundle(store,'2026-09-30',when,hist,flows,quotes)
    assert any(c['feature']=='momentum_5' and c['code']=='2330' for c in bundle['cells'])
    net=next(c for c in bundle['cells'] if c['feature']=='trust_net_ratio')
    assert net['value'].startswith('-') and len(net['rows'])==2
    assert validate_bundle(store,bundle,{'as_of':'2026-09-30','cutoff_at':when})==bundle
    changed=copy.deepcopy(bundle);changed['cells'][0]['value']='999'
    with pytest.raises(ValueError,match='cannot_be_reproduced'):validate_bundle(store,changed,{'as_of':'2026-09-30','cutoff_at':when})


def test_future_date_and_raw_action_boundaries_disable_unsupported_features(tmp_path):
    store,when,hist,flows,quotes=inputs(tmp_path)
    cap=store.json(hist[0]);body=store.json(cap['raw_ref']);body['data'][-2][7]='X0.00'
    cap['raw_ref']=store.put_json(body);hist[0]=store.put_json(cap)
    bundle=build_bundle(store,'2026-09-30',when,hist,flows,quotes)
    assert not any(c['code']=='2330' and c['feature']=='momentum_5' for c in bundle['cells'])
    assert any(m['reason']=='unverified_raw_price_boundary' for m in bundle['missing'])
    cap['fetched_at']='2099-01-01T00:00:00+08:00';hist[0]=store.put_json(cap)
    with pytest.raises(ValueError,match='after_cutoff'):build_bundle(store,'2026-09-30',when,hist,flows,quotes)


def test_wrong_flow_date_is_a_gap_not_zero_or_previous_day_fallback(tmp_path):
    store,when,hist,flows,quotes=inputs(tmp_path)
    cap=store.json(flows[0]);body=store.json(cap['raw_ref']);body['date']='20260929';cap['raw_ref']=store.put_json(body)
    flows[0]=store.put_json(cap);bundle=build_bundle(store,'2026-09-30',when,hist,flows,quotes)
    assert not any(c['feature'].endswith('net_ratio') for c in bundle['cells'])
    assert any(m.get('reason')=='flow_date_or_status_mismatch' for m in bundle['missing'])
