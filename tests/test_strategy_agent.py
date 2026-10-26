import json
from pathlib import Path
import pytest
from esun_research.candidate import prepare
from esun_research.research_tools import AgentSettings,ResearchWorkspace,StrategyProposal
from esun_research.strategy_agent import research_portfolio
from esun_research.llm import ModelConfig
from test_candidate import environment


def workspace(env):
    store,sources,universe,pack,policy,schema,req=env
    frozen=store.freeze(req,sources,namespace='candidates')
    snapshot=prepare(store,sources,universe,frozen,pack,policy)
    settings=AgentSettings.model_validate_json((Path(__file__).parents[1]/'config/strategy-agent.json').read_bytes())
    return ResearchWorkspace(snapshot,pack,policy,settings),snapshot,settings


def proposal(pid='growth',direction='higher',**extra):
    return {'proposal_id':pid,'name':'營收分散研究','hypothesis':'比較月營收年增率與當日可交易性，檢查短期配置假說是否可行。',
        'failure_condition':'營收高成長未必延續至獲利，若估值或消息反轉則假說失效。',
        'factors':[{'feature':'revenue_yoy_pct','direction':direction,'weight':'1','transform':'percentile'}],
        'holdings':25,'cash_target':'.15','weighting':'equal',**extra}


def test_open_factor_composition_changes_positions_and_never_imputes_absent_flows(environment):
    w,_,_=workspace(environment)
    growth=w.evaluate(proposal());reverse=w.evaluate(proposal('reverse','lower',weighting='rank_tilt'))
    assert not growth['errors'] and not reverse['errors']
    assert set(growth['targets'])!=set(reverse['targets'])
    assert growth['performance_verified'] is False
    assert next(f for f in w.catalog()['features'] if f['feature']=='foreign_net_ratio')['coverage']==0
    absent=w.evaluate(proposal(factors=[{'feature':'foreign_net_ratio','weight':'1'}]))
    assert absent['eligible_count']==0 and absent['errors']
    assert w.inspect(['foreign_net_ratio'])['rows'][0]['values']['foreign_net_ratio'] is None


def test_factor_identity_limits_and_canonical_economic_comparison(environment):
    w,_,_=workspace(environment)
    with pytest.raises(ValueError):w.evaluate(proposal(factors=[{'feature':'future_return','weight':1}]))
    with pytest.raises(ValueError):w.evaluate(proposal(cash_target='.24'))
    with pytest.raises(ValueError):w.evaluate(proposal(factors=[{'feature':'revenue_yoy_pct','weight':'.3'}]))
    a=StrategyProposal.model_validate(proposal());b=StrategyProposal.model_validate(proposal('renamed',cash_target='0.1500',factors=[{'feature':'revenue_yoy_pct','weight':'1.000'}]))
    assert a.economic_hash()==b.economic_hash()


def action(tool,**extra):
    return {'tool':tool,'reason':'依已取得的資料與限制繼續研究，避免把未驗證績效當成決策證據。',**extra}

class ScriptedModel:
    def __init__(self,wrong_reference=False):self.calls=0;self.wrong_reference=wrong_reference
    def complete(self,messages,schema):
        data=json.loads(messages[1]['content']);self.calls+=1
        steps=[action('inspect',features=['revenue_yoy_pct']),action('inspect',features=['intraday_return']),
            action('inspect',features=['foreign_net_ratio']),action('news'),action('evaluate',proposal=proposal()),
            action('evaluate',proposal=proposal('reverse','lower'))]
        selected=action('select',selected_id='reverse',comparisons=[
            {'proposal_id':'growth','reason':'高成長方案可行但短期延續尚無證據，保留作對照而未採用。','evidence_refs':['T5']},
            {'proposal_id':'reverse','reason':'低成長方向作為不同假說，根據實際壓力與成本檢查採用。','evidence_refs':['T6']}],
            limitations=['籌碼資料缺失，且沒有時間點一致的歷史績效驗證，選擇屬短期研究假說。'])
        if data['step']<len(steps):value=steps[data['step']]
        elif self.wrong_reference and data['step']==6:value={**selected,'comparisons':[{**c,'evidence_refs':['T999']} if c['proposal_id']=='reverse' else c for c in selected['comparisons']]}
        else:value=selected
        return {'value':value,'identity':{'digest':'a'*64},'latency_seconds':0,'input_tokens':1,'output_tokens':1}


def run_agent(env,model):
    store,sources,universe,pack,policy,schema,req=env
    w,snapshot,settings=workspace(env)
    config=ModelConfig(base_url='http://127.0.0.1:11435',model='test-only',digest='a'*64)
    return research_portfolio(store,store.root/'agent-test',req.model_dump(mode='json'),snapshot,pack,policy,settings.model_dump(),config,model)


def test_llm_tool_loop_selects_nondefault_strategy_and_resumes_without_new_calls(environment):
    model=ScriptedModel();result=run_agent(environment,model)
    assert result['status']=='SELECTED' and result['selection']['selected_id']=='reverse'
    assert model.calls==7 and len(result['trace'])==7
    assert result['selection']['comparisons'][0]['evidence_refs']==['T5']
    restored=run_agent(environment,model)
    assert model.calls==7 and restored==result


def test_unknown_selection_reference_is_feedback_not_a_silent_baseline(environment):
    model=ScriptedModel(wrong_reference=True);result=run_agent(environment,model)
    assert result['status']=='SELECTED' and model.calls==8
    store=environment[0];bad=store.json(result['trace'][6]['result_ref'])
    assert 'comparison_requires_current_evaluation_reference' in bad['error']
    assert result['selection']['selected_id']=='reverse'


def test_failed_price_scenarios_are_visible_and_require_revision(environment):
    class RepairModel(ScriptedModel):
        def complete(self,messages,schema):
            data=json.loads(messages[1]['content']);result=super().complete(messages,schema)
            if data['step'] in {4,5}:result['value']['proposal']['cash_target']='.22'
            if data['step']==7:
                assert not data['remaining_requirements']['locally_selectable_strategies']
                assert 'evaluate' in data['remaining_requirements']['next_phase']
                feedback=data['recent_tool_results'][-1]
                assert feedback['error']=='selected_strategy_not_locally_feasible'
                assert feedback['selected_evaluation']['stress_failure_details']
                assert feedback['selected_evaluation']['locally_selectable'] is False
                result['value']=action('evaluate',proposal=proposal('reverse','lower'))
            if data['step']==8:
                result['value']['comparisons'][1]['evidence_refs']=['T8']
            return result
    result=run_agent(environment,RepairModel())
    assert result['status']=='SELECTED' and result['selection']['selected_id']=='reverse'
    assert not result['selected_evaluation']['errors']
    assert result['selected_evaluation']['proposal']['cash_target']=='0.15'


def test_agent_selection_changes_real_dplan_orders_instead_of_only_narrative(environment):
    from esun_research.candidate import generate_candidate
    from esun_research.store import encoded,digest
    from test_llm import EvidenceModel
    from test_candidate import TIME
    store,sources,universe,pack,policy,schema,req=environment
    baseline=generate_candidate(store,req,sources,universe)
    baseline_orders=store.json(baseline['plan'])['plan']['orders']
    from esun_research.contracts import Source
    news=Source(id='CNA-news',url='https://www.cna.com.tw/rss/finance.xml',provider='CNA',branch='events',kind='rss',enabled=True)
    sources=sources+[news]
    store.capture(news.id,b'<rss version="2.0"><channel><item><title>Market research update</title><link>https://www.cna.com.tw/news/afe/202610220001.aspx</link><pubDate>Thu, 22 Oct 2026 07:00:00 GMT</pubDate></item></channel></rss>',fetched_at=TIME)
    # A negative-growth stock is not a hard competition exclusion. The agent
    # must be free to research it rather than inherit the old growth baseline.
    c=store.select('TWSE-revenue',TIME);rows=store.json(c['ref']);rows[0]['營業收入-去年同月增減(%)']='-80'
    store.capture('TWSE-revenue',encoded(rows),fetched_at=TIME)
    settings=AgentSettings.model_validate_json((Path(__file__).parents[1]/'config/strategy-agent.json').read_bytes())
    config=ModelConfig(base_url='http://127.0.0.1:11435',model='test-only',digest='a'*64)
    agent_req=req.model_copy(update={'run_id':'agent-final','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump()),'llm_ref':store.put_json(config.model_dump()),
        'registry_hash':digest(encoded([s.model_dump() for s in sources]))})
    class CompleteModel(EvidenceModel):
        def __init__(self):super().__init__();self.agent=ScriptedModel()
        def complete(self,messages,schema):
            if schema.get('title')=='ResearchAction':return self.agent.complete(messages,schema)
            return super().complete(messages,schema)
    model=CompleteModel();result=generate_candidate(store,agent_req,sources,universe,model=model)
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS'
    plan=store.json(result['plan'])['plan']
    assert model.agent.calls==7 and model.calls==8
    assert plan['agent_metadata']['input_tokens']==87 and plan['agent_metadata']['output_tokens']==167
    assert plan['orders']!=baseline_orders
    assert any(o['ticker']=='1000' and o['side']=='BUY' for o in plan['orders'])
    folder=store.root/'candidates/agent-final';research=json.loads((folder/'agent-research.json').read_bytes())
    assert research['selection']['selected_id']=='reverse'
    assert (folder/'strategy-comparison.md').exists()
    assert json.loads((folder/'targets.json').read_bytes())==research['selected_evaluation']['targets']
    assert any(o['topic']=='agent_strategy_comparison' for o in plan['observations'])
    assert any(o['topic']=='observed_news' and o['values']=={'observed_item_count':1} for o in plan['observations'])
    assert all('LLM自主研究比較' in i['logic'] for i in plan['inferences'])
    assert not json.loads((folder/'validation.json').read_bytes())['errors']
    from fastapi.testclient import TestClient
    from esun_research.application import create_app
    import zipfile,io
    client=TestClient(create_app(store.root));review=json.loads((Path(__file__).parents[1]/'delivery/AGENT_PDF_REVIEW.json').read_bytes())
    pdf=client.get('/api/candidates/agent-final/strategy.pdf')
    assert digest(pdf.content)==review['pdf_sha256']
    from esun_research.deliverables import operating_guide_pdf
    guide=client.get('/api/candidates/agent-final/guide.pdf')
    assert guide.content==operating_guide_pdf('llm_agent')
    assert guide.content!=operating_guide_pdf('baseline')
    with zipfile.ZipFile(io.BytesIO(client.get('/api/candidates/agent-final/handoff.zip').content)) as archive:
        assert 'strategy-comparison.md' in archive.namelist() and 'agent-call-evidence.json' in archive.namelist()
        assert digest(archive.read('ETF_strategy.pdf'))==review['pdf_sha256']
        assert archive.read('Operator_guide.pdf')==guide.content
    generate_candidate(store,agent_req,sources,universe,model=model)
    assert model.agent.calls==7 and model.calls==8


def test_known_research_identifiers_are_not_fabricated_financial_numbers():
    from esun_research.strategy_agent import ResearchAction,validate_action
    good=ResearchAction.model_validate(action('inspect',reason='P1未通過壓力情境，改以momentum_20與低波動研究不同的短期方案。'))
    validate_action(good,{'P1','T3'})
    for reason in ['P999未通過壓力情境，先檢查其他策略的可用資料。','預期報酬可達99%，足以保證策略獲利並勝過市場。','P1保證獲利，因此不需要再進行任何風險檢查。']:
        with pytest.raises(ValueError):validate_action(ResearchAction.model_validate(action('inspect',reason=reason)),{'P1'})
