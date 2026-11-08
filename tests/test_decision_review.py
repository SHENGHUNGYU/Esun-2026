from types import SimpleNamespace
from pathlib import Path
import json
import pytest
from esun_research.decision_review import review_selection,alternative_id,history_audit,history_text
from esun_research.llm import verify_trade_direction
from esun_research.research_tools import ResearchWorkspace
from esun_research.candidate import compile_document
from esun_research.dplan import validate_plan
from test_candidate import environment
from test_turnover import settled,HoldModel
from test_strategy_agent import proposal,action


def selection(**extra):
    base=dict(reason='當日訊號與交易成本需要一起判斷。',trade_justification='實際訊號與限制作為交易判斷依據。',why_not_hold='',why_not_gradual='',memory_review='當日證據不足以證明持股應調整，暫時維持原股數。',comparisons=[],selected_id='GROWTH')
    return SimpleNamespace(**{**base,**extra})


def test_trade_selection_requires_explicit_hold_and_same_factor_gradual():
    values={'GROWTH':{'orders':[{'ticker':'2330'}],'proposal':{'mode':'rebalance'}}}
    with pytest.raises(ValueError,match='hold_is_insufficient'):review_selection(selection(),values,{},True)
    why='個股 2330 當日訊號較弱，續抱會保留當日訊號已明顯弱化的部位，需比較更換與漸進調整，不能只看交易成本。'
    with pytest.raises(ValueError,match='gradual_comparison_required'):review_selection(selection(why_not_hold=why),values,{},True)
    values[alternative_id('GROWTH')]={'errors':[]}
    with pytest.raises(ValueError,match='gradual_is_insufficient'):review_selection(selection(why_not_hold=why),values,{},True)
    review_selection(selection(why_not_hold=why,why_not_gradual='漸進調整仍保留被評估為較弱的舊部位，本次選擇輪替，但尚無報酬優勢證據。'),values,{},True)
    # A wording filter must not override an otherwise evidence-backed choice.
    review_selection(selection(reason='續抱無因子驅動調整，但已觀察到持股弱化。',why_not_hold=why,
        why_not_gradual='漸進調整仍保留被評估為較弱的舊部位，本次選擇輪替，但尚無報酬優勢證據。'),values,{},True)
    with pytest.raises(ValueError,match='rewrite_history'):review_selection(selection(memory_review='進場假說現在改為低波動股票。'),values,{},False)


def test_history_copies_original_text_and_keeps_model_comment_separate():
    thesis={'reason':'原始動能與籌碼理由','invalidation':'原始限制超標','source_run':'old','plan_sha256':'x','feature_evidence':{'specific':'one'}}
    memory={'holdings':[{'code':'2330','entry_thesis':thesis},{'code':'1101','entry_thesis':{**thesis,'feature_evidence':{'specific':'two'}}},{'code':'9999','entry_thesis':None}]}
    a=history_audit(memory,{'memory_review':'當日新增低波動評估。'},{'orders':[]})
    assert len(a['entries'])==2
    assert a['entries'][0]['codes']==['2330','1101']
    assert a['entries'][0]['original_hypothesis']==thesis['reason']
    assert '低波動' not in history_text(a) and a['model_comment']=='當日新增低波動評估。'


def test_buy_reason_direction_guard():
    plan={'decisions':[{'action':'BUY','inference_refs':['I1']},{'action':'SELL_ALL','inference_refs':['I2']}]}
    with pytest.raises(ValueError,match='outside_retention'):verify_trade_direction(plan,'I1','個股排名超出續抱區間，故新買。')
    verify_trade_direction(plan,'I1','個股進入新買候選，建立部位。')
    verify_trade_direction(plan,'I2','排名超出續抱區間，減少原有部位。')


def test_compiled_buy_and_sell_reasons_are_direction_specific(environment):
    store,sources,universe,pack,policy,schema,req,snapshot,settings=settled(environment)
    ws=ResearchWorkspace(snapshot,pack,policy,settings);e=ws.evaluate(proposal('reverse','lower'))
    assert e['orders']
    for o in e['orders']:
        reason=e['continuity']['trade_reasons'][o['ticker']]
        if o['side']=='BUY':assert '超出續抱' not in reason and '新買候選' in reason
    # Machine-generated rank values can be independently checked in the official document.
    research={'selected_evaluation':e,'selection':{},'inputs_hash':'test','evidence':ws.evidence,'evaluations':{},'data_sources':{}}
    plan,_,_=compile_document(snapshot,e['ranking'],e['targets'],pack,policy,req.model_dump(mode='json'),sources,research=research)
    assert not validate_plan(plan,schema,pack,snapshot['prices'],universe,req.cutoff_at,policy)
    assert any('strategy_rank' in o['values'] for o in plan['observations'])


def test_previous_rule_prefers_reported_version_only_when_reconciled_and_not_unknown(tmp_path,monkeypatch):
    from esun_research.store import Store
    from esun_research.turnover import previous_strategy
    from test_holding_ledger import pack
    store=Store(tmp_path);p=pack()
    for rid,direction in [('a','higher'),('b','lower')]:
        folder=store.root/'candidates'/rid;folder.mkdir(parents=True)
        (folder/'manifest.json').write_text(json.dumps({'request':{'cutoff_at':'2026-10-27T01:00:00+08:00'},'artifacts':{'agent-research.json':'unused'}}))
        (folder/'agent-research.json').write_text(json.dumps({'status':'SELECTED','selected_evaluation':{'proposal':proposal(rid,direction)}}))
    monkeypatch.setattr('esun_research.daily.review_previous',lambda *_:{'comparisons':[{'run_id':rid,'plan_sha256':rid,'reconciliation':{'status':'RECONCILED_SHARES'}} for rid in ['a','b']]})
    monkeypatch.setattr('esun_research.decision_review.reported_submission',lambda *_:None)
    assert previous_strategy(store,p,'2026-10-28T01:00:00+08:00')['proposal'] is None
    report={'run_id':'b','plan_hash':'b','event_hash':'receipt','event':{'stage':'submitted'}}
    monkeypatch.setattr('esun_research.decision_review.reported_submission',lambda *_:report)
    selected=previous_strategy(store,p,'2026-10-28T01:00:00+08:00')
    assert selected['run_id']=='b' and not selected['submission_verified']
    report['event']['stage']='submission_unknown'
    assert previous_strategy(store,p,'2026-10-28T01:00:00+08:00')['proposal'] is None


def test_stock_lists_are_bound_identifiers_but_same_number_as_price_is_not():
    from esun_research.decision_review import identifier_safe_text
    from esun_research.strategy_agent import ResearchAction,validate_action
    text='賣出個股1802、3017動能偏弱，買入個股3105、6415方向較強。'
    safe=identifier_safe_text(text,{'1802','3017','3105','6415'})
    assert not any(c in safe for c in ['1802','3017','3105','6415'])
    assert '1802' in identifier_safe_text('收盤價為1802元。',{'1802'})
    assert '1802' in identifier_safe_text('買入1802元。',{'1802'})
    assert not any(c in identifier_safe_text('減碼2409與4958，5289 五與二十日動能偏弱，2409與4958仍保留曝險。',{'2409','4958','5289'}) for c in ['2409','4958','5289'])
    assert '2409' in identifier_safe_text('價格2409元，減碼2409元。',{'2409'})
    validate_action(ResearchAction(tool='select',reason=text),{'1802','3017','3105','6415'})
    with pytest.raises(ValueError):validate_action(ResearchAction(tool='select',reason='預期報酬可以達到1802元，故換股。'),{'1802'})


def test_claimed_review_labels_require_real_own_packet_and_complete_comparison():
    from esun_research.decision_review import check_review_attribution
    reviews={'H5880':{'value':{'verdict':'supported'}}}
    comp=SimpleNamespace(reason='買入個股 2412 的動能訊號在審查中亦被標記為弱化，故不採用。',review_refs=['H5880'])
    a=selection(comparisons=[comp])
    with pytest.raises(ValueError,match='does_not_exist'):check_review_attribution(a,reviews)
    comp.reason='個股 5880 被標記為弱化，故不採用本方案。'
    with pytest.raises(ValueError,match='verdict_mismatch'):check_review_attribution(a,reviews)
    comp.reason='個股 5880 的審查結論為支持，但仍須比較增加曝險的風險。'
    check_review_attribution(a,reviews)
    comp.reason='比較目前成本與風險，但邏輯'
    with pytest.raises(ValueError,match='complete_sentence'):check_review_attribution(a,reviews)
    comp.reason='審查支持續抱，但仍有市場風險。';comp.review_refs=[]
    with pytest.raises(ValueError,match='reference_required'):check_review_attribution(a,reviews)
