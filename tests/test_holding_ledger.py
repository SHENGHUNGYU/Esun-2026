import json
from decimal import Decimal
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from esun_research.store import Store,encoded
from esun_research.datapack import DataPack
from esun_research.holding_ledger import remember_pack,review_memory,portfolio_view,import_basis,compact_memory,daily_hypotheses
from esun_research.application import create_app
from esun_research.candidate import generate_candidate
from esun_research.llm import ModelConfig
from test_candidate import environment
from test_turnover import settled,HoldModel


def pack(day='2026-10-27',shares=1000,cash='90000',price='12',team='TEAM_TEST'):
    from datetime import date,timedelta
    value={'schema_version':'3.0','doc_type':'DataPack','team_id':team,
        'trade_date':str(date.fromisoformat(day)+timedelta(days=1)),'as_of_date':day,
        'generated_at':day+'T23:00:00+08:00','missing':[],
        'account':{'cash':cash,'cash_ratio_tradable':None,'nav_tradable':str(Decimal(cash)+shares*Decimal(price)),
            'aum':str(Decimal(cash)+shares*Decimal(price)),'receivable_cash':'0','holdings_count':int(shares>0)},
        'holdings':[{'code':'2330','shares':shares,'receivable_shares':0,'close_price':price}] if shares else [],
        'prev_day_orders':{'outcome':'executed','void_reasons':[],'excluded_codes':[]},
        'compliance':{'violations':0,'notices':0,'incidents':[]}}
    return DataPack.model_validate(value)


def save(store,p):return remember_pack(store,p.model_dump_json().encode(),p.generated_at)


def test_missing_cost_is_not_zero_and_cost_bound_to_snapshot(tmp_path):
    s=Store(tmp_path);p=pack();key=save(s,p)
    r=portfolio_view(s);assert r['holdings'][0]['unrealized_pnl'] is None
    data={'team_id':p.team_id,'as_of_date':str(p.as_of_date),'positions':[{'code':'2330','shares':1000,'remaining_cost_twd':'10014.25'}]}
    import_basis(s,key,encoded(data),b'cost proof')
    row=portfolio_view(s)['holdings'][0]
    assert Decimal(row['unrealized_pnl'])==Decimal('1985.75')
    assert Decimal(row['unrealized_return'])==Decimal('1985.75')/Decimal('10014.25')
    assert row['average_cost']=='10.01425'
    save(s,pack(day='2026-10-28',shares=2000,cash='80000'))
    assert portfolio_view(s)['holdings'][0]['unrealized_pnl'] is None
    data['positions'][0]['remaining_cost_twd']='10000'
    with pytest.raises(ValueError,match='Immutable'):import_basis(s,key,encoded(data),b'different proof')


def test_cost_rejects_invalid_shares_team_and_numeric_values(tmp_path):
    s=Store(tmp_path);p=pack();key=save(s,p)
    base={'team_id':p.team_id,'as_of_date':str(p.as_of_date),'positions':[{'code':'2330','shares':1000,'remaining_cost_twd':'NaN'}]}
    with pytest.raises(ValueError):import_basis(s,key,encoded(base),b'proof')
    base['positions'][0].update(shares=2000,remaining_cost_twd='10000')
    with pytest.raises(ValueError,match='股數'):import_basis(s,key,encoded(base),b'proof')
    base['positions'][0]['shares']=1000;base['team_id']='OTHER'
    with pytest.raises(ValueError,match='隊伍'):import_basis(s,key,encoded(base),b'proof')


def test_timeline_future_other_team_conflicts_and_reentry(tmp_path):
    s=Store(tmp_path);first=pack();save(s,first)
    save(s,pack(day='2026-10-28',shares=0,cash='102000'))
    current=pack(day='2026-10-29');save(s,current)
    save(s,pack(day='2026-10-30',shares=2000))
    save(s,pack(team='OTHER'))
    memory=review_memory(s,current,'2026-10-29T23:30:00+08:00')
    events=memory['timeline']['2330'];assert [e['action'] for e in events]==['ENTRY','EXIT','ENTRY']
    assert memory['holdings'][0]['entry']['settlement_date']=='2026-10-29'
    assert memory['holdings'][0]['entry_thesis'] is None
    assert len(compact_memory(memory)['holdings'])==1
    save(s,pack(day='2026-10-29',shares=2000))
    memory=review_memory(s,current,'2026-10-29T23:30:00+08:00')
    assert memory['conflicting_settlement_dates']==['2026-10-29']
    # No stale closed-position entry can be shown as current after conflict.
    assert all(e['settlement_date']<'2026-10-29' for e in memory['timeline']['2330'])


def test_account_total_return_initial_and_pending_state(tmp_path):
    s=Store(tmp_path);p=pack();initial=p.model_dump(mode='json')
    initial.update(as_of_date=None,holdings=[],trade_date='2026-10-27',generated_at='2026-10-27T01:00:00+08:00')
    initial['account'].update(cash='100000',nav_tradable='100000',aum='100000',holdings_count=0)
    initial['prev_day_orders']['outcome']='none';save(s,DataPack.model_validate(initial));save(s,p)
    r=portfolio_view(s);assert r['asset_change']=='2000' and r['asset_change_ratio']=='0.02'
    pending=p.model_dump(mode='json');pending.update(account=None,holdings=None,as_of_date=None,missing=['prev_settlement'])
    key=save(s,DataPack.model_validate(pending));r=portfolio_view(s,key)
    assert r['account'] is None and r['holdings']==[]


class MemoryHoldModel(HoldModel):
    def complete(self,messages,schema):
        data=json.loads(messages[1]['content'])
        result=super().complete(messages,schema)
        if 'step' in data:
            assert data['holding_memory']['holdings']
            if result['value']['tool']=='select':
                assert 'memory_review' in schema['required']
                result['value']['memory_review']='原持股進場理由尚缺唯一歷史證據，本次沒有足以證明失效的新資訊；在成本與限制檢查可行下先續抱，仍持續觀察風險。'
        return result


def test_memory_reaches_model_and_daily_review_is_immutable(environment):
    store,sources,universe,p,policy,schema,req,snapshot,settings=settled(environment)
    save(store,p);memory=review_memory(store,p,'2026-10-28T23:00:00+08:00')
    config=ModelConfig(base_url='http://127.0.0.1:11435',model='test-only',digest='a'*64)
    req=req.model_copy(update={'run_id':'memory-hold','decision_engine':'llm_agent',
        'holding_memory_ref':store.put_json(memory),'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),
        'llm_ref':store.put_json(config.model_dump())})
    model=MemoryHoldModel();result=generate_candidate(store,req,sources,universe,model=model)
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS'
    folder=store.root/'candidates'/req.run_id
    review=json.loads((folder/'holding-review.json').read_bytes())
    assert review['cross_day_review'] and len(review['rows'])==25
    assert all(r['intent']=='HOLD' and not r['execution_confirmed'] for r in review['rows'])
    before=(folder/'holding-review.json').read_bytes();calls=model.calls
    generate_candidate(store,req,sources,universe,model=model)
    assert model.calls==calls and (folder/'holding-review.json').read_bytes()==before


def test_holdings_api_upload_persistence_and_safe_evidence(tmp_path):
    app=create_app(tmp_path,model_config=None);client=TestClient(app);auth={'x-esun-token':app.state.csrf_token}
    assert client.get('/api/holdings').json()['selected'] is None
    p=pack();assert client.post('/api/datapack',files={'file':('pack.json',p.model_dump_json(),'application/json')},headers=auth).status_code==200
    r=client.get('/api/holdings').json();assert r['account']['aum']=='102000'
    assert client.get('/api/holdings/evidence',params={'ref':r['pack_ref']}).status_code==200
    assert client.get('/api/holdings/evidence',params={'ref':'../../etc/passwd'}).status_code==400
    assert client.post('/api/holdings/cost-basis',data={'snapshot_id':r['selected']},files={'file':('cost.json',b'{}'),'proof':('proof.txt',b'p')}).status_code==403
    restarted=TestClient(create_app(tmp_path,model_config=None))
    assert restarted.get('/api/holdings').json()['selected']==r['selected']


def test_feature_change_is_observation_not_invalidation():
    from types import SimpleNamespace
    from esun_research.holding_ledger import evidence_changes
    memory={'holdings':[{'code':'2330','recent_reviews':[{'local_hypothesis':{'feature_evidence':{'e':{'feature':'momentum_5','value':'0.1','rows':[{'raw_ref':'past'}]},'x':{'feature':'pb_ratio','value':'3','rows':[]}}}}]}]}
    workspace=SimpleNamespace(rows={'2330':{'values':{'momentum_5':'-0.1','revenue_yoy_pct':'5'},'evidence':{'momentum_5':['new']}}})
    rows={r['feature']:r for r in evidence_changes(memory,workspace)['2330']}
    assert rows['momentum_5']['change']=='decreased' and rows['momentum_5']['current_evidence_refs']==['new']
    assert rows['pb_ratio']['change']=='unavailable'
    assert rows['revenue_yoy_pct']['change']=='newly_observed'
    assert all('invalidated' not in r for r in rows.values())
