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


def selection_fixture(count=11,reviews=30):
    from test_strategy_agent import proposal
    evaluations=[]
    for i in range(count):
        evaluations.append({'tool_id':'T'+str(i),'proposal':proposal('P'+str(i),mode='rebalance',hypothesis='研究假說'*100),
            'holdings':30,'errors':[],'cash_ratio':'.15','cost_fraction_nav':'.0002',
            'turnover_notional_fraction':'.05','order_count':6,'stress_failure_details':[],
            'trade_evidence':{'columns':['code','side','rank','score','momentum_5'],
                'rows':[[str(1000+j),'BUY',j+1,'0.1234567890123456789','0.234567890123456789'] for j in range(6)],'omitted_orders':0}})
    return {'phase':'select','step':13,'official_settlement':{'account':{'cash':'100000','nav_tradable':'1000000'},
            'holdings':[[str(i),1000,'10',0] for i in range(30)]},'evaluations':evaluations,
        'holding_memory':{'holdings':[[str(i),'entry','HOLD','reason'] for i in range(30)],'columns':['code','thesis','action','reason'],
            'theses':{str(i):{'reason':'原始進場假說'*100,'invalidation':'失效條件'*100} for i in range(30)}},
        'completed_reviews':[{'review_id':'H'+str(i),'verdict':'weakened','features':['momentum_5'],
                             'action_tradeoff':'比較續抱與部分調整的風險成本'*10} for i in range(reviews)],
        'selection_reference_contract':[{'proposal_id':'P'+str(i),'required_evaluation_reference':'T'+str(i)} for i in range(count)],
        'recent_tool_results':[{'tool_id':'T13','tool':'select','error':'hold_comparison_requires_an_actual_traded_security',
                               'selected_evaluation':evaluations[-1],'next_required_action':'需修正文字'*100}]}


def test_selection_projection_bounds_maximum_normal_live_frontier_and_repair():
    from esun_research.strategy_agent import SELECTION_SYSTEM
    data=selection_fixture();before=copy.deepcopy(data)
    value,stats=fit_context(SELECTION_SYSTEM,data,SimpleNamespace(context_tokens=16384,output_tokens=3072))
    assert stats['fits'] and stats['total_bytes']<stats['budget_bytes']-2000
    assert stats['reserved_repair_bytes']==1024
    assert data==before and value['official_settlement']==data['official_settlement']
    assert value['selection_reference_contract']==data['selection_reference_contract']
    assert len(value['evaluations'])==11 and len(value['completed_reviews'])==30
    cards=[dict(zip(value['evaluation_columns'],r)) for r in value['evaluations']]
    assert all(e['cost_fraction_nav']=='.0002' and e['cash_ratio']=='.15' for e in cards)
    assert value['recent_tool_results'][0]['error']=='hold_comparison_requires_an_actual_traded_security'
    assert 'selected_evaluation' not in value['recent_tool_results'][0]
    assert len(value['strategy_rules'])==1 # identical implementations, distinct candidates preserved


def test_selection_projection_preserves_all_infeasible_errors_and_stress_cells():
    from esun_research.strategy_agent import SELECTION_SYSTEM
    data=selection_fixture(19)
    for e in data['evaluations'][:-1]:
        e['errors']=['price_stress_failed']
        e['stress_failure_details']=[{'errors':['industry_cap'],'execution_factor':str(i),'close_factor':str(j)} for i in [.95,1,1.05] for j in [.95,1,1.05]]
    value,stats=fit_context(SELECTION_SYSTEM,data,SimpleNamespace(context_tokens=16384,output_tokens=3072))
    assert stats['fits'] and len(value['evaluations'])==19
    for e in [dict(zip(value['evaluation_columns'],r)) for r in value['evaluations']][:-1]:
        assert e['errors']==['price_stress_failed'] and len(e['stress_failures'][0]['execution_close_factors'])==9
        assert e['trade_evidence']['not_replayed_infeasible']


def test_selection_capacity_with_eight_factor_rules_and_thirty_reviews():
    from esun_research.strategy_agent import SELECTION_SYSTEM
    from esun_research.research_tools import FEATURES
    data=selection_fixture(11,30);features=list(FEATURES)[:8]
    for i,e in enumerate(data['evaluations']):
        e['proposal']['factors']=[{'feature':f,'direction':'higher' if i & (1<<j) else 'lower','transform':'sector_percentile','weight':'0.125'} for j,f in enumerate(features)]
        e['proposal']['screens']=[{'feature':f,'operator':'ge','value':'-1000000.12345678'} for f in features]
        e['trade_evidence']['columns']=['code','side','rank','score',*features]
        e['trade_evidence']['rows']=[[str(1000+j),'BUY',j+1,*['0.1234567890123456789012345678']*9] for j in range(6)]
        e['risk_comparison']={'columns':['max_industry_weight','equity_hhi','covered_weight','daily_volatility','beta_pool','weighted_pair_correlation'],
            'before':['0.123456789123456789']*6,'after':[str(i/100)]*6,'missing_before':[],'missing_after':[]}
    for r in data['completed_reviews']:r['features']=features[:6]
    value,stats=fit_context(SELECTION_SYSTEM,data,SimpleNamespace(context_tokens=16384,output_tokens=3072))
    assert stats['fits'],stats
    assert len(value['evaluations'])==11 and len(value['strategy_rules'])==11
    assert len(value['completed_reviews'])==30


def test_extended_risk_comparisons_fit_and_survive_selection():
    from esun_research.strategy_agent import SELECTION_SYSTEM
    data=selection_fixture(11,30)
    columns=['max_industry_weight','equity_hhi','covered_weight','daily_volatility','beta_pool','weighted_pair_correlation']
    for e in data['evaluations']:
        e['risk_comparison']={'columns':columns,'before':['0.123456789123456789']*6,
            'after':['0.234567891234567891']*6,'missing_before':[],'missing_after':[]}
    value,stats=fit_context(SELECTION_SYSTEM,data,SimpleNamespace(context_tokens=16384,output_tokens=3072))
    assert stats['fits'],stats
    assert value['risk_columns']==columns
    for row in value['evaluations']:
        e=dict(zip(value['evaluation_columns'],row));assert e['risk_comparison']['after']==['0.23456789']*6
        assert e['cost_fraction_nav']=='.0002' and e['errors']==[]


def test_evaluation_projection_retains_all_candidate_costs_and_failure_feedback():
    from esun_research.strategy_agent import EVALUATION_SYSTEM,PROBE_SYSTEM
    from esun_research.research_tools import FEATURES
    data=selection_fixture(11,30);data['phase']='evaluate'
    data['catalog']={'features':[{'feature':f,'category':v[0],'unit':v[1],'coverage':148,'eligible_universe':148,'limitation':v[2]} for f,v in FEATURES.items()]}
    data['market_state']={'state':'stressed'};data['cash_probe_required']=True
    data['remaining_requirements']={'evaluate_cash_probe':True}
    data['recent_tool_results']=[{'tool':'select','tool_id':'T13','error':'selected_strategy_not_locally_feasible',
        'selected_evaluation':{'errors':['price_stress_failed'],'locally_selectable':False,'stress_failure_details':[{'errors':['cash_ratio']}],'long_prose':'X'*10000}}]
    value,stats=fit_context(EVALUATION_SYSTEM+PROBE_SYSTEM,data,SimpleNamespace(context_tokens=16384,output_tokens=3072))
    assert stats['fits'],stats
    assert value['market_state']==data['market_state'] and value['remaining_requirements']==data['remaining_requirements']
    assert len(value['evaluations'])==11 and value['official_settlement']==data['official_settlement']
    assert value['recent_tool_results'][0]['selected_evaluation']['errors']==['price_stress_failed']
