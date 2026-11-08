import json
from decimal import Decimal as D
import pytest
from esun_research.pnl import apply,replay,import_events
from esun_research.store import Store,encoded
from esun_research.holding_ledger import remember_pack,settlements,portfolio_view
from test_holding_ledger import pack,save


def test_average_cost_partial_sale_and_dividend():
    p={'shares':0,'cost':D(0),'realized':D(0),'income':D(0),'fees':D(0)}
    p=apply(p,dict(kind='BUY',shares=1000,gross_twd='10000',fee_twd='14.25',tax_twd='0'))
    p=apply(p,dict(kind='BUY',shares=1000,gross_twd='12000',fee_twd='17.1',tax_twd='0'))
    p=apply(p,dict(kind='SELL',shares=500,gross_twd='6500',fee_twd='9.2625',tax_twd='19.5'))
    assert p['cost']==D('22031.35')*D('.75')
    assert p['realized']==D('6500')-D('28.7625')-D('22031.35')/4
    p=apply(p,dict(kind='DIVIDEND',shares=0,gross_twd='500',fee_twd='0',tax_twd='0'))
    assert p['income']==500
    with pytest.raises(ValueError):apply(p,dict(kind='SELL',shares=2000,gross_twd='1'))


def initial(p):
    data=p.model_dump(mode='json');data.update(as_of_date=None,holdings=[],trade_date=str(p.as_of_date),generated_at=str(p.as_of_date)+'T01:00:00+08:00')
    data['account'].update(cash='100000',nav_tradable='100000',aum='100000',holdings_count=0)
    data['prev_day_orders']['outcome']='none'
    return type(p).model_validate(data)


def test_reconstruct_then_carry_and_unknown_transition(tmp_path,monkeypatch):
    s=Store(tmp_path);p=pack(cash='89985.75');save(s,initial(p));key=save(s,p)
    monkeypatch.setattr('esun_research.pnl.quote_index',lambda s:{('2026-10-27','2330'):{'price':D(10),'raw_ref':'test','raw_row':0}})
    r=portfolio_view(s);h=r['holdings'][0]
    assert h['cost']=='10014.250000' and D(h['unrealized_pnl'])==D('1985.75')
    assert h['cost_authority']=='reconstructed_estimate'
    assert r['pnl_ledger']['cash_reconciliation'][0]['complete']
    p2=pack(day='2026-10-28',cash='89985.75',price='13');save(s,p2)
    assert D(portfolio_view(s)['holdings'][0]['cost'])==D('10014.25')
    save(s,pack(day='2026-10-29',shares=2000))
    assert portfolio_view(s)['holdings'][0]['cost'] is None


def test_import_transaction_reconciles_shares_and_is_immutable(tmp_path):
    s=Store(tmp_path);p=pack(cash='89985.75');first=save(s,initial(p));key=save(s,p)
    data={'team_id':p.team_id,'as_of_date':str(p.as_of_date),'previous_snapshot_id':first,'authority':'user_supplied_evidence',
          'events':[dict(code='2330',kind='BUY',shares=1000,gross_twd='10000',fee_twd='14.25',tax_twd='0')]}
    import_events(s,key,encoded(data),b'evidence')
    row=portfolio_view(s)['holdings'][0]
    assert row['cost']=='10014.25' and row['cost_authority']=='user_supplied_evidence'
    assert row['total_pnl']=='1985.75'
    import_events(s,key,encoded(data),b'evidence') # idempotence should preserve original receipt
    data['events'][0]['shares']=2000
    with pytest.raises(ValueError,match='股數'):import_events(s,key,encoded(data),b'evidence')
