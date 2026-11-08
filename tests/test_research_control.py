import json
from types import SimpleNamespace
import pytest
from esun_research.research_control import evaluation_contract,check_proposal_contract,stalled_error
from esun_research.research_tools import StrategyProposal
from test_candidate import environment
from test_strategy_agent import ScriptedModel,proposal,action,run_agent


def test_archived_november_six_revision_loop_requires_new_hypothesis():
    # Minimal shape of the real failure: one valid primary, automatic baselines
    # and gradual alternative, and an already exhausted primary revision budget.
    values={k:{'economic_hash':h} for k,h in [('BASE_REPAIR','base'),('ALT_auto','alt'),('CASH_PROBE_QUALITY','cash')]}
    settings=SimpleNamespace(minimum_compared_strategies=2,maximum_strategies=6,maximum_revisions=2)
    contract=evaluation_contract(values,{'CASH_PROBE_QUALITY':21},settings)
    assert contract['operation']=='create' and contract['distinct_primary_count']==1
    assert not contract['revisable_ids']
    with pytest.raises(ValueError,match='new_independent_proposal_required'):
        check_proposal_contract(StrategyProposal.model_validate(proposal('CASH_PROBE_QUALITY')),contract,values)
    check_proposal_contract(StrategyProposal.model_validate(proposal(contract['suggested_new_id'])),contract,values)


def test_revision_limit_applies_before_evaluation_and_fresh_continuation_ignores_old_stall():
    settings=SimpleNamespace(minimum_compared_strategies=2,maximum_strategies=6,maximum_revisions=2)
    values={'one':{'economic_hash':'a'},'two':{'economic_hash':'b'}}
    contract=evaluation_contract(values,{'one':2},settings)
    assert contract['revisable_ids']==['two']
    with pytest.raises(ValueError,match='proposal_revision_not_available'):
        check_proposal_contract(StrategyProposal.model_validate(proposal('one')),contract,values)
    trace=[{'error':'maximum_revisions_reached'}]*19
    assert stalled_error(trace,0)=='maximum_revisions_reached'
    assert stalled_error(trace,19) is None
    assert stalled_error([{'error':'a'},{}],0) is None


def test_repeated_primary_is_repaired_before_consuming_a_tool_step(environment):
    class Repeating(ScriptedModel):
        repeated=False
        def complete(self,messages,schema):
            data=json.loads(messages[1]['content']);out=super().complete(messages,schema)
            if data['step']==5:
                assert data['evaluation_contract']['new_id_required']
                if not self.repeated:
                    self.repeated=True;out['value']=action('evaluate',proposal=proposal('growth'))
                else:assert 'new_independent_proposal_required' in messages[-1]['content']
            return out
    model=Repeating();r=run_agent(environment,model)
    assert r['status']=='SELECTED' and model.calls==8
    assert len(r['trace'])==7 # invalid repeated ID never reaches execute


def test_noncompliant_repeated_primary_stops_after_two_calls_not_twenty_four_steps(environment):
    class Repeating(ScriptedModel):
        def complete(self,messages,schema):
            out=super().complete(messages,schema)
            if json.loads(messages[1]['content'])['step']==5:out['value']=action('evaluate',proposal=proposal('growth'))
            return out
    model=Repeating();r=run_agent(environment,model)
    assert r['errors']==['agent_action_contract_failed:new_independent_proposal_required']
    assert model.calls==7 and len(r['trace'])==5 and r['selection'] is None


def test_renaming_same_economics_is_rejected_and_stops_without_fake_diversity(environment):
    class Renaming(ScriptedModel):
        def complete(self,messages,schema):
            data=json.loads(messages[1]['content']);out=super().complete(messages,schema)
            if data['step']>=5:out['value']=action('evaluate',proposal=proposal('renamed_'+str(data['step'])))
            return out
    model=Renaming();r=run_agent(environment,model)
    assert r['errors']==['agent_research_stalled:strategies_are_not_economically_distinct']
    assert model.calls==7 and len(r['evaluations'])==1 and len(r['trace'])==7


def test_incomplete_response_is_accounted_and_archived_without_masking_root_failure(environment):
    from esun_research.llm import ModelResponseError
    class Incomplete:
        calls=0
        def complete(self,messages,schema):
            self.calls+=1
            # Older journals lack normalized usage fields; recovery must support them.
            raise ModelResponseError('incomplete_model_response',{'request':{},'identity':{},
                'response':{'done_reason':'length','prompt_eval_count':10,'eval_count':30,'total_duration':1000000000}})
    m=Incomplete();r=run_agent(environment,m)
    assert r['errors']==['agent_model_output_failed'] and m.calls==2
    assert r['usage']=={'calls':2,'input_tokens':20,'output_tokens':60,'latency_seconds':2}
    assert r['selection'] is None


def test_workflow_budgets_do_not_change_economic_replay_but_trade_limits_do(environment):
    from test_turnover import settled
    from esun_research.research_tools import ResearchWorkspace
    from decimal import Decimal
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    baseline=ResearchWorkspace(snapshot,pack,policy,settings).evaluate(proposal())
    workflow=settings.model_copy(update={'maximum_exploration_steps':12,'maximum_review_steps':24,'maximum_selection_steps':6})
    assert ResearchWorkspace(snapshot,pack,policy,workflow).evaluate(proposal())==baseline
    financial=settings.model_copy(update={'maximum_daily_turnover':Decimal('.10')})
    assert ResearchWorkspace(snapshot,pack,policy,financial).evaluate(proposal())!=baseline
