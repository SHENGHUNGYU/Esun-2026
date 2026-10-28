import json
from decimal import Decimal
from datetime import date
from pathlib import Path
import pytest
from esun_research.candidate import generate_candidate,prepare,compile_document,jsonable
from esun_research.datapack import DataPack
from esun_research.portfolio import Policy,target_shares
from esun_research.research_tools import AgentSettings,ResearchWorkspace
from esun_research.turnover import weights_for_positions,held_positions
from esun_research.dplan import validate_plan
from test_candidate import environment
from test_strategy_agent import proposal,ScriptedModel,action
from test_llm import EvidenceModel
from esun_research.llm import ModelConfig


def settled(env):
    store,sources,universe,pack,policy,schema,req=env
    base=generate_candidate(store,req,sources,universe);projection=store.json(base['plan'])['projected'];snapshot=store.json(base['snapshot'])
    data=pack.model_dump(mode='json');data['as_of_date']='2026-10-22';data['prev_day_orders']['outcome']='executed'
    data['holdings']=[{'code':c,'shares':n,'receivable_shares':0,'close_price':snapshot['prices'][c]} for c,n in projection['positions'].items()]
    data['account'].update(cash=projection['cash'],nav_tradable=projection['nav'],aum=projection['nav'],cash_ratio_tradable=projection['cash_ratio'],holdings_count=25)
    official=DataPack.model_validate(data)
    req=req.model_copy(update={'run_id':'settled-continuity','datapack_ref':store.put(official.model_dump_json().encode())})
    snapshot=prepare(store,sources,universe,store.freeze(req,sources,namespace='candidates'),official,policy)
    settings=AgentSettings.model_validate_json(Path('config/strategy-agent.json').read_bytes())
    return store,sources,universe,official,policy,schema,req,snapshot,settings


def test_hold_produces_schema_valid_zero_order_dplan_with_all_positions(environment):
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    workspace=ResearchWorkspace(snapshot,pack,policy,settings)
    hold=workspace.evaluate(proposal('BASE_HOLD',mode='hold',factors=[]));assert not hold['errors']
    assert hold['orders']==[] and hold['cost_twd']=='0'
    plan,_,projection=compile_document(snapshot,hold['ranking'],hold['targets'],pack,Policy.model_validate(hold['policy']),req.model_dump(mode='json'),sources)
    assert plan['orders']==[] and plan['decisions']==[] and len(plan['no_trade_decisions'])==25
    assert not validate_plan(plan,schema,pack,snapshot['prices'],universe,req.cutoff_at,Policy.model_validate(hold['policy']))
    assert projection['positions']==held_positions(pack)
    for c,n in held_positions(pack).items():assert target_shares(hold['targets'][c],pack.account.nav_tradable,snapshot['prices'][c])==n


def test_rank_drift_does_not_force_topups_and_full_rotation_is_rejected(environment):
    *_,pack,policy,schema,req,snapshot,settings=settled(environment)
    workspace=ResearchWorkspace(snapshot,pack,policy,settings)
    controlled=workspace.evaluate(proposal('reverse','lower'))
    full=workspace.evaluate(proposal('full','lower',mode='full_rebalance'))
    assert not controlled['errors']
    assert Decimal(controlled['turnover_notional_fraction'])<=settings.maximum_daily_turnover
    assert Decimal(controlled['cost_twd'])/pack.account.nav_tradable<=settings.maximum_daily_cost
    assert len([o for o in controlled['orders'] if o['side']=='BUY'])<=settings.maximum_replacements
    assert full['errors'] and any('budget_exceeded' in e for e in full['errors'])
    unchanged=ResearchWorkspace(snapshot,pack,policy,settings.model_copy(update={'maximum_replacements':0})).evaluate(proposal('same'))
    assert unchanged['orders']==[]
    assert unchanged['continuity']['suppressed_adjustments']


def test_zero_replacement_budget_really_holds_existing_names(environment):
    *_,pack,policy,schema,req,snapshot,settings=settled(environment)
    settings=settings.model_copy(update={'maximum_replacements':0})
    result=ResearchWorkspace(snapshot,pack,policy,settings).evaluate(proposal('reverse','lower'))
    assert not result['errors'] and result['orders']==[]


class HoldModel(ScriptedModel):
    def complete(self,messages,schema):
        if 'step' not in json.loads(messages[1]['content']):return EvidenceModel().complete(messages,schema)
        data=json.loads(messages[1]['content'])
        assert schema['properties']['codes']['maxItems']==12
        assert schema['properties']['features']['items']['enum']
        if data['step']==0:assert 'revenue_yoy_pct' in schema['properties']['features']['items']['enum']
        if data['step']<6:return super().complete(messages,schema)
        self.calls+=1
        comparisons=[{'proposal_id':r['proposal_id'],'evidence_refs':[r['required_evaluation_reference']],
            'reason':'以實際股數、成本與限制比較，未有足夠交易必要性，優先保留現有可交易部位。'} for r in data['selection_reference_contract']]
        return {'value':action('select',selected_id='BASE_HOLD',comparisons=comparisons,
            limitations=['沒有樣本外報酬優勢證據，續抱也不能保證避免市場損失。']),
            'input_tokens':1,'output_tokens':1,'latency_seconds':0,'identity':{'digest':'a'*64}}


def test_agent_can_select_hold_through_full_pipeline_and_resume(environment):
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    config=ModelConfig(base_url='http://127.0.0.1:11435',model='test-only',digest='a'*64)
    req=req.model_copy(update={'run_id':'complete-hold','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),'llm_ref':store.put_json(config.model_dump())})
    result=generate_candidate(store,req,sources,universe,model=HoldModel())
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS',result
    plan=store.json(result['plan'])['plan'];assert not plan['orders'] and len(plan['no_trade_decisions'])==25
    research=store.json(result['agent_research'])
    assert research['selection']['selected_id']=='BASE_HOLD'
    assert {'BASE_HOLD','BASE_REPAIR','BASE_PREVIOUS'}<=research['evaluations'].keys()
    assert len(research['selection']['comparisons'])==5
    assert generate_candidate(store,req,sources,universe,model=HoldModel())==result


def test_risk_repair_is_noop_when_compliant_and_repairs_excess_cash(environment):
    *_,pack,policy,schema,req,snapshot,settings=settled(environment)
    workspace=ResearchWorkspace(snapshot,pack,policy,settings)
    repair=workspace.evaluate(proposal('BASE_REPAIR',mode='risk_repair',factors=[]))
    assert not repair['errors'] and repair['orders']==[]
    assert repair['continuity']['risk_repair_budget_exception'] is False
    # Official cash increases while stock inventory stays unchanged. This is an
    # intentionally constrained account scenario, not a forecast dividend fill.
    data=pack.model_dump(mode='json');extra=Decimal('200000000')
    data['account']['cash']=str(pack.account.cash+extra)
    data['account']['nav_tradable']=str(pack.account.nav_tradable+extra)
    data['account']['aum']=data['account']['nav_tradable']
    data['account']['cash_ratio_tradable']=str((pack.account.cash+extra)/(pack.account.nav_tradable+extra))
    bad=DataPack.model_validate(data)
    workspace=ResearchWorkspace(snapshot,bad,policy,settings)
    hold=workspace.evaluate(proposal('BASE_HOLD',mode='hold',factors=[]))
    assert hold['errors']
    repair=workspace.evaluate(proposal('BASE_REPAIR',mode='risk_repair',factors=[]))
    assert not repair['errors'],repair
    assert repair['orders'] and repair['continuity']['risk_repair_budget_exception']
    assert Decimal(repair['cash_ratio'])<=policy.cash_band[1]


def test_signal_gap_can_prevent_all_replacements(environment):
    *_,pack,policy,schema,req,snapshot,settings=settled(environment)
    settings=settings.model_copy(update={'minimum_rank_score_gap':Decimal('1')})
    result=ResearchWorkspace(snapshot,pack,policy,settings).evaluate(proposal('reverse','lower'))
    assert result['orders']==[] and not result['errors']
