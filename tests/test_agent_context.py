import copy
from types import SimpleNamespace
from esun_research.agent_context import fit_context
from esun_research.strategy_agent import SYSTEM


def test_compaction_preserves_account_memory_costs_and_every_failed_stress_cell():
    config=SimpleNamespace(context_tokens=8192,output_tokens=1800)
    account={'account':{'cash':'100000','nav_tradable':'1000000'},'holdings':[[str(i),1000,'10',0] for i in range(25)]}
    failures=[{'errors':['cash_ratio'],'execution_factor':str(i),'close_factor':str(j)} for i in [0.95,1,1.05] for j in [0.95,1,1.05]]
    evaluations=[]
    for i in range(5):
        evaluations.append({'tool_id':'T'+str(i),'proposal':{'proposal_id':'P'+str(i),'mode':'gradual','weighting':'rank_tilt','cash_target':'.15','factors':[{'feature':'momentum_5','direction':'higher','transform':'percentile','weight':'1'}],'screens':[], 'hypothesis':'既有假說'*150},
            'holdings':25,'errors':['price_stress_failed'],'cash_ratio':'.16','cost_fraction_nav':'.0002','turnover_notional_fraction':'.05','order_count':4,'stress_failure_details':copy.deepcopy(failures)})
    data={'official_settlement':account,'holding_memory':{'holdings':[[str(i),'entry','HOLD','reason'] for i in range(25)],'theses':{'entry':{'reason':'進場原始依據','invalidation':'出現反證則重新評估'}},'reasons':{'reason':'當日續抱理由'}},
        'catalog':{'features':[{'feature':'factor_'+str(i),'category':'technical','coverage':150,'limitation':'限制'*100} for i in range(16)]},
        'evaluations':evaluations,'recent_tool_results':[{'tool':'evaluate','tool_id':'T4','proposal':evaluations[-1]['proposal'],'errors':['price_stress_failed']}],
        'selection_reference_contract':[{'proposal_id':e['proposal']['proposal_id'],'required_evaluation_reference':e['tool_id']} for e in evaluations]}
    before=copy.deepcopy(data);value,stats=fit_context(SYSTEM,data,config)
    assert stats['fits'] and stats['total_bytes']<=stats['budget_bytes']
    assert data==before and value['official_settlement']==account
    memory=value['holding_memory'];assert memory['theses']==data['holding_memory']['theses']
    assert sorted(c for row in memory['holdings'] for c in row[0])==sorted(str(i) for i in range(25))
    assert value['selection_reference_contract']==data['selection_reference_contract']
    columns=value['evaluation_columns']
    for row in value['evaluations']:
        e=dict(zip(columns,row));assert e['errors']==['price_stress_failed'] and e['cost_fraction_nav']=='.0002'
        assert e['cash_ratio']=='.16' and len(e['stress_failure_details'][0]['execution_close_factors'])==9


def test_inspection_omission_is_explicit_and_unfittable_safety_data_blocks():
    config=SimpleNamespace(context_tokens=2048,output_tokens=128)
    data={'catalog':{'features':[]},'evaluations':[],'recent_tool_results':[{'tool':'inspect','rows':[{'value':'資訊'*100} for _ in range(12)]}], 'official_settlement':{'critical':'X'*10000}}
    fitted,stats=fit_context('system',data,config)
    assert not stats['fits']
    assert fitted['official_settlement']==data['official_settlement']
    assert fitted['recent_tool_results'][0]['omitted_rows']==9
