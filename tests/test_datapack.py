import copy
from datetime import date
from decimal import Decimal
import pytest
from esun_research.datapack import DataPack,load_datapack

@pytest.fixture
def initial():
    return {'schema_version':'3.0','doc_type':'DataPack','team_id':'TEST_TEAM','trade_date':'2026-10-27',
        'as_of_date':None,'generated_at':'2026-10-24T13:00:00+08:00','missing':[],
        'prev_day_orders':{'outcome':'none','void_reasons':[],'excluded_codes':[]},
        'account':{'cash':1000000,'nav_tradable':1000000,'aum':1000000,'receivable_cash':0,'cash_ratio_tradable':1,'holdings_count':0},
        'holdings':[],'compliance':{'violations':0,'notices':0,'incidents':[]}}

def test_initial_and_pending_are_different(initial):
    assert DataPack.model_validate(initial).decision_gate()=='INITIAL_CASH_ACCOUNT'
    initial.update(missing=['prev_settlement'],account=None,holdings=None)
    assert DataPack.model_validate(initial).decision_gate()=='BLOCKED_MISSING_OFFICIAL_INPUT'

def test_null_is_not_empty(initial):
    initial['account']=None
    with pytest.raises(ValueError):DataPack.model_validate(initial)

def test_receivable_only_does_not_count_or_fund_trade(initial):
    initial.update(as_of_date='2026-10-26',holdings=[{'code':'2330','shares':0,'receivable_shares':1000,'close_price':100,'tradable_weight':None}])
    initial['account'].update(aum=1100000)
    pack=DataPack.model_validate(initial)
    assert pack.account.holdings_count==0
    assert pack.account.nav_tradable==1000000
    initial['account']['holdings_count']=1
    with pytest.raises(ValueError):DataPack.model_validate(initial)

def test_missing_close_and_unknown_outcome_block(initial):
    initial['missing']=['prev_close'];initial['account']['cash_ratio_tradable']=None
    assert DataPack.model_validate(initial).decision_gate().startswith('BLOCKED')
    initial.update(as_of_date='2026-10-26',missing=[])
    initial['prev_day_orders']['outcome']='unknown'
    assert DataPack.model_validate(initial).decision_gate()=='BLOCKED_UNKNOWN_ORDER_OUTCOME'

def test_partial_execution_and_compliance_not_conflated(initial):
    initial['as_of_date']='2026-10-26'
    initial['prev_day_orders'].update(outcome='executed',excluded_codes=['2330'])
    initial['compliance'].update(violations=1,notices=1,incidents=[
        {'date':'2026-10-26','check_code':c,'status':'fail','message':'test'} for c in ['a','b']])
    pack=DataPack.model_validate(initial)
    assert pack.decision_gate()=='SETTLED_ACCOUNT'
    assert pack.compliance.violations==1
    assert pack.prev_day_orders.excluded_codes==['2330']

def test_wrong_team_and_version(initial):
    import json
    body=json.dumps(initial).encode()
    with pytest.raises(ValueError):load_datapack(body,'OTHER',date(2026,10,27))
    initial['schema_version']='4.3'
    assert DataPack.model_validate(initial).decision_gate()=='BLOCKED_UNSUPPORTED_DATAPACK_VERSION'

def test_nav_uses_tradable_shares_and_exact_decimal(initial):
    initial.update(as_of_date='2026-10-26',holdings=[{'code':'2330','shares':1000,'receivable_shares':2000,'close_price':'0.1','tradable_weight':None}])
    initial['account'].update(nav_tradable='1000100',aum='1000300',holdings_count=1)
    assert DataPack.model_validate(initial).account.nav_tradable==Decimal('1000100')
    initial['account']['nav_tradable']='1000300'
    with pytest.raises(ValueError):DataPack.model_validate(initial)

def test_unknown_outcome_cannot_masquerade_as_initial_cash(initial):
    initial['prev_day_orders']['outcome']='unknown'
    assert DataPack.model_validate(initial).decision_gate()=='BLOCKED_UNKNOWN_ORDER_OUTCOME'

def test_unpriced_receivable_does_not_disable_nav_reconciliation(initial):
    initial.update(as_of_date='2026-10-22',holdings=[{'code':'2330','shares':0,'receivable_shares':1000,'close_price':None,'tradable_weight':None}])
    assert DataPack.model_validate(initial).account.nav_tradable==1000000
    initial['account']['nav_tradable']=999999
    with pytest.raises(ValueError,match='NAV inconsistent'):DataPack.model_validate(initial)
