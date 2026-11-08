from collections import defaultdict
from datetime import date,timedelta
from decimal import Decimal as D
import pytest
from esun_research.market_signals import price_signals,flow_signals,portfolio_risk,event_signals,industry_cells


def panel(count=24):
    start=date(2026,10,1);dates=[str(start+timedelta(days=i)) for i in range(21)]
    prices={};quotes={};universe={}
    for j in range(count):
        c=str(1000+j);rows={};price=D(100+j)
        for i,d in enumerate(dates):
            if i:price*=1+D((i%3)+1+j%4)/1000
            rows[d]={'date':d,'close_twd':str(price),'high_twd':str(price*D('1.01')),
                'volume_shares':str(1000+i*100),'usable_quote':True,'corporate_action_marker':False,
                'listing_boundary_marker':False,'source_id':'AGENT-HISTORY-TWSE','raw_ref':'objects/raw.bin',
                'raw_row':i,'fetched_at':'2026-11-04T18:00:00+08:00'}
        prices[c]=rows;quotes[c]={'values':{'close':str(price)}};universe[c]={'industry':'A' if j<12 else 'B'}
    return prices,dates,quotes,universe


def signals(count=24):
    prices,dates,quotes,universe=panel(count);cells={};missing=[]
    risk=price_signals(prices,dates,quotes,universe,lambda c,f,v,rows:cells.update({(c,f):(D(v),rows)}),missing)
    return risk,cells,missing,prices,dates


def test_price_windows_pool_beta_and_peer_comparison_have_recomputable_evidence():
    risk,cells,missing,prices,dates=signals()
    assert risk['benchmark']['kind']=='current_competition_pool_equal_weight_price_proxy'
    assert len(risk['benchmark']['returns'])==20 and len(risk['benchmark']['members'])==24
    assert ('1000','relative_pool_20') in cells and ('1000','beta_pool_20') in cells
    assert cells['1000','volume_ratio_5'][0]==D(3000)/D(2700)
    assert cells['1000','drawdown_20'][0]==0
    assert all(r['raw_rows'] for r in cells['1000','relative_pool_20'][1])
    peers=industry_cells(risk,{str(1000+i):'A' for i in range(24)})
    assert len(peers)==24 and all(c['feature']=='relative_industry_20' for c in peers)


def test_bad_windows_do_not_create_false_benchmarks_or_zero_risk():
    prices,dates,quotes,universe=panel(20)
    prices['1000'][dates[5]]['corporate_action_marker']=True
    cells=[];missing=[]
    risk=price_signals(prices,dates,quotes,universe,lambda *x:cells.append(x),missing)
    assert risk['benchmark']['kind']=='unavailable' and '1000' not in risk['series']
    r=portfolio_risk(risk,{'1000':'.5','1001':'.3'},{'1000':'A','1001':'A'})
    assert r['daily_volatility'] is None and r['beta_pool'] is None
    assert r['missing_codes']==['1000'] and D(r['covered_weight'])==D('.3')


def test_flow_ratios_weight_volume_and_count_buy_days_not_streaks():
    _,_,_,prices,dates=signals();rows=defaultdict(dict);cells={};missing=[]
    for i,d in enumerate(dates[-10:]):
        rows['1000'][d]={'values':{'foreign_net_ratio':str(100 if i%2 else -50)},
            'evidence':{'raw_ref':'objects/flow.bin','date':d,'raw_row':0}}
    flow_signals(rows,prices,dates,lambda c,f,v,refs:cells.update({f:D(v)}),missing)
    assert cells['foreign_buy_days_10']==5
    assert cells['foreign_net_ratio_10']==D(250)/sum(D(prices['1000'][d]['volume_shares']) for d in dates[-10:])
    del rows['1000'][dates[-2]]
    cells.clear();flow_signals(rows,prices,dates,lambda c,f,v,refs:cells.update({f:D(v)}),missing)
    assert 'foreign_net_ratio_3' not in cells and missing


def test_portfolio_covariance_tracks_cash_scaling_and_never_forecasts():
    risk,*_=signals()
    a=portfolio_risk(risk,{'1000':'.5','1004':'.5'},{'1000':'A','1004':'A'})
    b=portfolio_risk(risk,{'1000':'.25','1004':'.25'},{'1000':'A','1004':'A'})
    assert abs(D(a['weighted_pair_correlation'])-1)<D('1e-25')
    assert abs(D(a['daily_volatility'])-D(b['daily_volatility'])*2)<D('1e-25')
    assert abs(D(a['beta_pool'])-D(b['beta_pool'])*2)<D('1e-25')
    assert abs(sum(D(v) for c,v in a['variance_contribution'])-1)<D('1e-25')
    assert D(a['max_industry_weight'])==1


def test_event_time_dedup_unknown_publication_and_price_reaction_not_causation():
    risk,*_=signals();cutoff='2026-11-04T18:00:00+08:00'
    event={'code':'1000','text':'官方 公告','evidence_id':'E1','published_at':'2026-10-20T10:00:00+08:00','available_at':cutoff}
    future={**event,'text':'future','published_at':'2026-11-05T10:00:00+08:00'}
    unknown={**event,'text':'unknown','published_at':None}
    items=event_signals([event,{**event,'evidence_id':'E2'},future,unknown],risk,cutoff)
    assert len(items)==2
    timed=next(n['event_timing'] for n in items if n['published_at'])
    assert timed['price_base_date']=='2026-10-19' and D(timed['post_publication_close_return'])>0
    assert timed['priced_in']==timed['semantic_novelty']=='unknown'
    assert len(timed['price_source_rows'])==2
    assert next(n for n in items if n['published_at'] is None)['event_timing']['publication_age_hours'] is None


def test_archived_event_repeat_is_cutoff_bound_and_hash_verified(tmp_path):
    from esun_research.market_signals import frozen_event_history
    from esun_research.store import Store,encoded,digest
    store=Store(tmp_path);cutoff='2026-11-04T18:00:00+08:00'
    event={'code':'1000','text':'官方 公告','evidence_id':'E1','published_at':'2026-11-03T10:00:00+08:00','available_at':'2026-11-03T18:00:00+08:00'}
    folder=store.root/'candidates'/'prior';folder.mkdir(parents=True)
    body=encoded({'news':[event]});(folder/'agent-research.json').write_bytes(body)
    manifest={'request':{'run_id':'prior','cutoff_at':'2026-11-03T19:00:00+08:00'},'artifacts':{'agent-research.json':digest(body)}}
    (folder/'manifest.json').write_bytes(encoded(manifest))
    assert not frozen_event_history(store,'2026-11-02T18:00:00+08:00','new')['events']
    history=frozen_event_history(store,cutoff,'new')
    item=event_signals([{**event,'available_at':cutoff}],{},cutoff,history)[0]
    assert item['event_timing']['novelty']=='previously_observed_exact_content'
    assert item['event_timing']['earliest_observed_in_archived_reports']==event['available_at']
    (folder/'agent-research.json').write_bytes(encoded({'news':[]}))
    with pytest.raises(ValueError,match='hash_mismatch'):frozen_event_history(store,cutoff,'new')
