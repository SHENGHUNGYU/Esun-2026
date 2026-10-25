import copy
import json
from pathlib import Path
import httpx
import pytest
from esun_research.llm import ModelConfig,OllamaModel,apply_review,review_document
from esun_research.candidate import generate_candidate
from esun_research.store import encoded
from test_candidate import environment

ROOT=Path(__file__).resolve().parents[1]

class EvidenceModel:
    def __init__(self,bad=False):self.calls=0;self.bad=bad
    def complete(self,messages,schema):
        self.calls+=1;data=json.loads(messages[1]['content'])
        reason='觀測顯示營收與估值具備規則要求的條件，仍應以分散配置與流動性門檻控制風險。'
        counter='單月資訊及單日行情不足以驗證長期競爭力，未來走勢仍有不確定性。'
        if 'items' in data:
            value={'explanations':[{'inference_id':i['inference_id'],'observation_ids':i['observation_ids'],
                'reasoning':reason,'counter_evidence':counter} for i in data['items']]}
        else:value={'observation_ids':[o['obs_id'] for o in data['observations']],'reasoning':reason,'counter_evidence':counter}
        if self.bad:value['orders']=[{'ticker':'2330','shares':9999999}]
        return {'value':value,'input_tokens':10,'output_tokens':20,'latency_seconds':.1,'request':messages,'response':value}

def enable(env):
    store,sources,universe,pack,policy,schema,req=env
    config=ModelConfig.model_validate_json((ROOT/'config/llm-local.json').read_bytes())
    req=req.model_copy(update={'llm_ref':store.put_json(config.model_dump())})
    return store,sources,universe,req,config

def test_local_model_pin_and_transport():
    config=ModelConfig.model_validate_json((ROOT/'config/llm-local.json').read_bytes())
    def handler(request):
        if request.url.path=='/api/tags':return httpx.Response(200,json={'models':[{'name':config.model,'digest':config.digest}]})
        payload=json.loads(request.content);assert payload['think'] is False and payload['format']=={'type':'object'}
        return httpx.Response(200,json={'model':config.model,'done':True,'done_reason':'stop','message':{'content':'{}'},'prompt_eval_count':2,'eval_count':3})
    result=OllamaModel(config,httpx.Client(transport=httpx.MockTransport(handler))).complete([],{'type':'object'})
    assert result['value']=={} and result['output_tokens']==3
    invalid=config.model_copy(update={'digest':'0'*64})
    with pytest.raises(ValueError,match='digest_mismatch'):OllamaModel(invalid,httpx.Client(transport=httpx.MockTransport(handler))).complete([],{'type':'object'})
    for url in ['http://remote:11434','http://127.0.0.1@external','http://localhost:8000/?token=x','http://user@localhost:8000']:
        with pytest.raises(ValueError):ModelConfig.model_validate({**config.model_dump(),'base_url':url})

def test_complete_review_cannot_change_orders_and_resumes_without_model(environment):
    store,sources,universe,req,config=enable(environment);model=EvidenceModel()
    result=generate_candidate(store,req,sources,universe,model=model)
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS'
    assert model.calls==8
    plan=store.json(result['plan'])['plan'];review=store.json(result['llm_review'])
    assert plan['agent_metadata']['model_provider']=='other'
    assert config.digest[:16] in plan['agent_metadata']['model_version']
    assert plan['agent_metadata']['input_tokens']==80
    baseline=json.loads((store.root/'candidates'/req.run_id/'compiled.json').read_bytes())['plan']
    assert plan['orders']==baseline['orders'] and plan['decisions']==baseline['decisions']
    assert plan['inferences']!=baseline['inferences']
    before=model.calls;generate_candidate(store,req,sources,universe,model=model);assert model.calls==before
    other=copy.deepcopy(review);other['explanations'][0]['observation_ids']=['O999']
    with pytest.raises(ValueError,match='reference'):apply_review(baseline,other)
    assert not store.json(result['validation'])['errors']

def test_bad_output_is_blocked_instead_of_silently_using_no_llm(environment):
    store,sources,universe,req,config=enable(environment);model=EvidenceModel(bad=True)
    result=generate_candidate(store,req,sources,universe,model=model)
    assert result['status']=='BLOCKED_LOCAL_CHECKS' and model.calls==2
    assert not list((store.root/'candidates'/req.run_id).glob('D-Plan_*.json'))
    assert any(e.startswith('llm_review_failed') for e in result['errors'])

def test_numeric_and_missing_coverage_reviews_are_rejected(environment):
    store,sources,universe,req,config=enable(environment)
    result=generate_candidate(store,req,sources,universe,model=EvidenceModel())
    baseline=json.loads((store.root/'candidates'/req.run_id/'compiled.json').read_bytes())['plan'];review=store.json(result['llm_review'])
    tampered=copy.deepcopy(review);tampered['explanations'][0]['reasoning']='明天預估上漲99%，保證獲利。'
    with pytest.raises(ValueError):apply_review(baseline,tampered)
    tampered=copy.deepcopy(review);tampered['explanations']=tampered['explanations'][:-1]
    with pytest.raises(ValueError):apply_review(baseline,tampered)

def test_interrupted_model_review_uses_completed_batch_journal(environment):
    store,sources,universe,req,config=enable(environment)
    class InterruptedModel(EvidenceModel):
        crashed=False
        def complete(self,messages,schema):
            if self.calls==2 and not self.crashed:
                self.crashed=True;raise KeyboardInterrupt('simulated interruption')
            return super().complete(messages,schema)
    model=InterruptedModel()
    with pytest.raises(KeyboardInterrupt):generate_candidate(store,req,sources,universe,model=model)
    assert model.calls==2
    result=generate_candidate(store,req,sources,universe,model=model)
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS' and model.calls==8
    assert len(store.json(result['llm_review'])['call_refs'])==8

@pytest.mark.parametrize('change',[{'done':False},{'done_reason':'length'},{'message':{'content':'{}','tool_calls':[{'name':'send_order'}]}}])
def test_incomplete_or_tool_request_model_response_is_rejected(change):
    config=ModelConfig.model_validate_json((ROOT/'config/llm-local.json').read_bytes())
    def handler(request):
        if request.url.path=='/api/tags':return httpx.Response(200,json={'models':[{'name':config.model,'digest':config.digest}]})
        response={'model':config.model,'done':True,'done_reason':'stop','message':{'content':'{}'}};response.update(change)
        return httpx.Response(200,json=response)
    with pytest.raises(ValueError):OllamaModel(config,httpx.Client(transport=httpx.MockTransport(handler))).complete([],{'type':'object'})
