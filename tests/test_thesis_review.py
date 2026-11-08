from types import SimpleNamespace
import pytest
from esun_research.holding_ledger import evidence_changes
from esun_research.thesis_review import review_packets,check_reviews,pending_reviews
from esun_research.strategy_agent import EvidenceReview
from esun_research.thesis_review import scoped_review_definitions
from esun_research.llm import verify_rank_claim


def fixture():
    old={'feature':'momentum_5','value':'.1','rows':[{'date':'2026-10-27'}]}
    memory={'holdings':[{'code':'2330','entry_thesis':{'reason':'動能與籌碼支持','invalidation':'訊號與風險反證','feature_evidence':{'OLD':old}},
        'recent_reviews':[{'local_hypothesis':{'feature_evidence':{}}}]}]}
    w=SimpleNamespace(pack=SimpleNamespace(as_of_date='2026-10-30',holdings=[SimpleNamespace(code='2330',shares=1000)]),
        rows={'2330':{'values':{'momentum_5':'-.1','foreign_net_ratio':'-.2'},'evidence':{'momentum_5':['E1'],'foreign_net_ratio':['E2']}}},
        evidence={'E1':{'feature':'momentum_5','value':'-.1','rows':[{'date':'2026-10-30'}]},'E2':{'feature':'foreign_net_ratio','value':'-.2','rows':[{'date':'2026-10-30'}]}},news=[])
    return memory,w


def test_hold_day_does_not_erase_last_observed_factor_and_attention_is_not_a_verdict():
    m,w=fixture();changes=evidence_changes(m,w)
    r=next(x for x in changes['2330'] if x['feature']=='momentum_5')
    assert r['previous']=='.1' and r['current']=='-.1' and r['change']=='decreased'
    p=review_packets(w,m,changes,{})['H2330']
    assert p['original_hypothesis']=='動能與籌碼支持' and 'verdict' not in p
    assert next(row for row in p['feature_rows'] if row[0]=='momentum_5')[3:5]==['2026-10-27','2026-10-30']
    assert p['source_evidence']['E1']['rows'][0]['date']=='2026-10-30'


def test_review_coverage_and_unknown_history_are_enforced_for_hold_and_trade():
    m,w=fixture();packets=review_packets(w,None,{},{});key='H2330'
    review=EvidenceReview(review_id=key,verdict='unknown',features=['momentum_5'],evidence_refs=[key],
        reason='目前雖然有負向動能與外資觀測，但缺少可核對的原始假說，因此不能宣稱原始假說已經失效，須保留未知。',
        counter_evidence='目前觀測並不能代表未來報酬，亦無法證明弱勢持續存在。',
        action_tradeoff='續抱維持市場風險，漸進調整改變曝險並產生成本；需評估證據強度後自主決定。')
    check_reviews([review],packets,[key])
    with pytest.raises(ValueError,match='coverage'):check_reviews([],packets,[key])
    with pytest.raises(ValueError,match='requires_unknown'):check_reviews([review.model_copy(update={'verdict':'invalidated'})],packets,[key])
    with pytest.raises(ValueError,match='own_packet'):check_reviews([review.model_copy(update={'evidence_refs':['H9999']})],packets,[key])
    done={key:{'input_hash':packets[key]['input_hash']}}
    assert pending_reviews(packets,done)==[]
    w.rows['2330']['values']['momentum_5']='-.3'
    assert pending_reviews(review_packets(w,None,{},{}),done)==[key]


def test_no_rank_claims_for_factorless_hold_but_scored_rank_remains_usable():
    plan={'inferences':[{'inf_id':'I1','premise_refs':['O1']}],'observations':[{'obs_id':'O1','values':{}}]}
    with pytest.raises(ValueError,match='no_factor_rank'):verify_rank_claim(plan,'I1','策略排名較後，因此續抱。')
    verify_rank_claim(plan,'I1','續抱仍保留價格風險，證據不足以確認假說失效。')
    verify_rank_claim(plan,'I1','無 strategy_rank 欄位，故禁止推測名次或續抱區間。不可依據排名討論。')
    verify_rank_claim(plan,'I1','沒有策略排名資訊，不能推斷名次。')
    with pytest.raises(ValueError,match='no_factor_rank'):
        verify_rank_claim(plan,'I1','雖沒有策略排名資訊，但本股排名第一，應繼續持有。')
    plan['observations'][0]['values']['strategy_rank']=3
    verify_rank_claim(plan,'I1','策略排名較前，但不是報酬保證。')


def test_each_security_schema_rejects_its_own_missing_feature_even_if_other_security_has_it():
    from jsonschema import Draft202012Validator
    base=EvidenceReview.model_json_schema()
    packets={'H1111':{'kind':'holding','feature_rows':[['earnings_yield',None,'0.1']]},
             'H2222':{'kind':'holding','feature_rows':[['earnings_yield',None,None],['momentum_5',None,'0.1']]}}
    defs,items=scoped_review_definitions(base,packets,list(packets))
    schema={'$defs':defs,**items};v=Draft202012Validator(schema)
    row={'review_id':'H2222','verdict':'weakened','features':['momentum_5'],'evidence_refs':['H2222'],
        'reason':'本檔動能與原始假說之間仍有落差，需要對照當日實際可用的資料與原始條件；缺值不能作為已觀察到的證據。',
        'counter_evidence':'可取得的資料仍不能證明未來表現，原始假說也可能存在其他支持。',
        'action_tradeoff':'續抱保留既有風險，漸進調整會改變曝險並產生成本，需要按證據自主權衡。'}
    assert not list(v.iter_errors(row))
    row['features']=['earnings_yield'];assert list(v.iter_errors(row))


from pathlib import Path
import json
from test_candidate import environment
from test_turnover import settled,HoldModel
from esun_research.llm import ModelConfig
from esun_research.candidate import generate_candidate
from esun_research.decision_review import alternative_id


@pytest.mark.parametrize('selected',['reverse',alternative_id('reverse')])
def test_completed_reviews_allow_both_replacement_and_gradual_not_only_hold(environment,selected):
    class ChoosingModel(HoldModel):
        def complete(self,messages,schema):
            result=super().complete(messages,schema)
            data=json.loads(messages[1]['content'])
            if 'step' not in data or result['value'].get('tool')!='select':return result
            evaluations=data['evaluations']
            if 'evaluation_columns' in data:
                evaluations=[dict(zip(data['evaluation_columns'],r)) for r in evaluations]
            chosen=next(e for e in evaluations if e.get('proposal_id',e.get('proposal',{}).get('proposal_id'))==selected)
            code=chosen['trade_evidence']['rows'][0][0]
            reason='個股 '+code+' 當日觀測與既有部位出現落差，選擇調整曝險並承擔交易成本；不宣稱已證明未來報酬優勢。'
            result['value'].update(selected_id=selected,reason=reason,trade_justification=reason,why_not_hold=reason,
                why_not_gradual='漸進調整仍保留部分較弱曝險，依本次假說自主選擇換股；此判斷仍可能錯失反彈，不宣稱績效已獲驗證。')
            return result
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    config=ModelConfig.model_validate_json(Path('config/llm-local.json').read_bytes()).model_copy(update={'model':'test-only','digest':'a'*64})
    req=req.model_copy(update={'run_id':'review-trade','decision_engine':'llm_agent',
        'agent_settings_ref':store.put_json(settings.model_dump(mode='json')),'llm_ref':store.put_json(config.model_dump())})
    result=generate_candidate(store,req,sources,universe,model=ChoosingModel())
    assert result['status']=='CANDIDATE_BLOCKED_EXTERNAL_CHECKS',result
    research=store.json(result['agent_research'])
    assert research['selection']['selected_id']==selected and research['selected_evaluation']['orders']
    assert research['decision_reviews'] and all(r['input_hash'] for r in research['decision_reviews'].values())
