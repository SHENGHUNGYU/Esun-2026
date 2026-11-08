from pathlib import Path
import json
from test_candidate import environment
from test_turnover import settled,HoldModel
from test_llm import EvidenceModel
from esun_research.llm import ModelConfig
from esun_research.candidate import generate_candidate
from esun_research.review_retry import retry_review
from esun_research.review_retry import retry_research


def test_prose_retry_preserves_autonomous_decision_and_never_calls_research_model(environment):
    class FailedProse(HoldModel):
        def complete(self,messages,schema):
            if 'step' not in json.loads(messages[1]['content']):raise ValueError('test_prose_failure')
            return super().complete(messages,schema)
    class ProseOnly(EvidenceModel):
        def complete(self,messages,schema):
            assert 'step' not in json.loads(messages[1]['content'])
            return super().complete(messages,schema)
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    config=ModelConfig.model_validate_json(Path('config/llm-local.json').read_bytes()).model_copy(update={'model':'test-only','digest':'a'*64})
    req=req.model_copy(update={'run_id':'prose-fail','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),'llm_ref':store.put_json(config.model_dump())})
    result=generate_candidate(store,req,sources,universe,model=FailedProse())
    assert result['status']=='BLOCKED_LOCAL_CHECKS'
    # Fixture source registry is intentionally different from production.
    import unittest.mock
    with unittest.mock.patch('esun_research.cli.candidate_sources',return_value=sources),unittest.mock.patch('esun_research.cli.settings',return_value=(sources,universe)):
        result=retry_review(store,req.run_id,'prose-repaired',model=ProseOnly())
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS',result
    r=store.json(result['agent_research']);assert r['selection']['selected_id']=='BASE_HOLD'
    assert r['decision_origin']['source_run']==req.run_id
    assert (store.root/'candidates/prose-repaired/decision-origin.json').exists()


def test_exhausted_research_continues_verified_work_without_repeating_research(environment):
    import unittest.mock
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    settings=settings.model_copy(update={'max_steps':8})
    config=ModelConfig.model_validate_json(Path('config/llm-local.json').read_bytes()).model_copy(update={'model':'test-only','digest':'a'*64})
    req=req.model_copy(update={'run_id':'budget-fail','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),'llm_ref':store.put_json(config.model_dump())})
    result=generate_candidate(store,req,sources,universe,model=HoldModel())
    assert result['errors']==['agent_research_budget_exhausted']
    class ContinueModel(HoldModel):
        def complete(self,messages,schema):
            data=json.loads(messages[1]['content'])
            if 'step' in data:assert data['step']>=8 and data['phase'] in {'review','select'}
            return super().complete(messages,schema)
    with unittest.mock.patch('esun_research.cli.candidate_sources',return_value=sources),unittest.mock.patch('esun_research.cli.settings',return_value=(sources,universe)):
        result=retry_research(store,req.run_id,'budget-continued',model=ContinueModel())
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS',result
    research=store.json(result['agent_research'])
    assert research['research_origin']['source_run']==req.run_id
    assert len([t for t in research['trace'] if t['action'].get('tool')=='evaluate'])==2


def test_context_capacity_retry_reuses_all_verified_reviews_and_only_selects(environment):
    import unittest.mock as mock
    from esun_research.agent_context import fit_context
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    config=ModelConfig.model_validate_json(Path('config/llm-local.json').read_bytes()).model_copy(update={'model':'test-only','digest':'a'*64})
    req=req.model_copy(update={'run_id':'context-capacity-fail','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),'llm_ref':store.put_json(config.model_dump())})
    def exhausted(system,data,config):
        value,stats=fit_context(system,data,config)
        if data.get('phase')=='select':stats['fits']=False
        return value,stats
    with mock.patch('esun_research.agent_context.fit_context',side_effect=exhausted):
        result=generate_candidate(store,req,sources,universe,model=HoldModel())
    assert result['errors']==['agent_context_budget_exceeded']
    folder=store.root/'candidates'/req.run_id
    original=(folder/'agent-research.json').read_bytes()
    old=json.loads(original);review_steps={key:t['tool_id'] for t in old['trace'] for key in store.json(t['result_ref']).get('reviewed',[])}
    assert review_steps
    class SelectOnly(HoldModel):
        def complete(self,messages,schema):
            data=json.loads(messages[1]['content'])
            if 'step' in data:assert data['phase']=='select' # no re-research or re-review
            return super().complete(messages,schema)
    with mock.patch('esun_research.cli.candidate_sources',return_value=sources),mock.patch('esun_research.cli.settings',return_value=(sources,universe)):
        result=retry_research(store,req.run_id,'context-capacity-fixed',model=SelectOnly())
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS',result
    research=store.json(result['agent_research'])
    assert all(research['decision_reviews'][key]['tool_id']==step for key,step in review_steps.items())
    assert (folder/'agent-research.json').read_bytes()==original


def test_validation_retry_preserves_completed_selection_and_prose_without_model_calls(environment):
    import unittest.mock as mock
    from esun_research.review_retry import retry_validation
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    config=ModelConfig.model_validate_json(Path('config/llm-local.json').read_bytes()).model_copy(update={'model':'test-only','digest':'a'*64})
    req=req.model_copy(update={'run_id':'validation-checkpoint','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),'llm_ref':store.put_json(config.model_dump())})
    generate_candidate(store,req,sources,universe,interrupt_before=['validate'],model=HoldModel())
    source=store.root/'candidates'/req.run_id
    assert (source/'llm-review.json').exists() and not (source/'manifest.json').exists()
    before=(source/'compiled.json').read_bytes()
    with mock.patch('esun_research.cli.candidate_sources',return_value=sources),mock.patch('esun_research.cli.settings',return_value=(sources,universe)):
        result=retry_validation(store,req.run_id,'validation-recovered')
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS',result
    r=store.json(result['agent_research']);assert r['decision_origin']['source_run']==req.run_id
    assert r['selection']['selected_id']=='BASE_HOLD'
    assert (source/'compiled.json').read_bytes()==before
