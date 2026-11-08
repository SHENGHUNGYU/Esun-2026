"""Bound research context without removing account truth or safety verdicts."""
import copy
from collections import defaultdict
from .store import encoded, digest
from decimal import Decimal, InvalidOperation



def selection_view(data):
    """A selection is a bounded decision record, not a replay of research prose.

    Every account row, candidate, hard error, review verdict and current reference
    survives. Full hypotheses/review arguments stay in immutable evidence files.
    """
    keys=['phase','step','steps_remaining','reference_date','trade_date','cutoff_at',
          'official_settlement','bounds','turnover_controls','planned_horizon_sessions',
          'selection_reference_contract','pending_review_count','remaining_requirements','market_state','cash_probe_required']
    value={k:copy.deepcopy(data[k]) for k in keys if k in data}
    value['projection_version']='selection-v3'
    if any(e.get('risk_comparison') for e in data.get('evaluations',[])):
        value['risk_columns']=next(e['risk_comparison']['columns'] for e in data['evaluations'] if e.get('risk_comparison'))
    rules={};evaluations=[];factors={};screens={}
    def intern(table,item,prefix):
        for key,existing in table.items():
            if existing==item:return key
        key=prefix+str(len(table)+1);table[key]=item;return key
    def display(v):
        if isinstance(v,(str,int,float)) and not isinstance(v,bool):
            try:
                n=Decimal(str(v))
                if n.is_finite():return format(n,'.8g')
            except (InvalidOperation,ValueError):pass
        return v
    for e in data.get('evaluations',[]):
        p=e['proposal']
        rule={'factors':[[f[k] for k in ['feature','direction','transform','weight']] for f in p['factors']],
              'screens':[[f[k] for k in ['feature','operator','value']] for f in p.get('screens',[])]}
        rid='R'+digest(encoded(rule))[:16]
        rules[rid]={'factor_refs':[intern(factors,r,'F') for r in rule['factors']],
                    'screen_refs':[intern(screens,r,'Q') for r in rule['screens']]}
        card={k:copy.deepcopy(e.get(k)) for k in ['tool_id','comparison_parent','errors','holdings','cash_ratio',
              'cost_fraction_nav','turnover_notional_fraction','order_count','replacement_count','cash_deployment','exclusion_counts','missing_feature_counts']}
        risk=e.get('risk_comparison')
        if risk:
            card['risk_comparison']={k:([display(v) for v in vals] if k in {'before','after'} else vals) for k,vals in risk.items() if k!='columns'}
        card.update(proposal_id=p['proposal_id'],mode=p['mode'],weighting=p['weighting'],cash_target=p['cash_target'],rule_id=rid)
        stress=defaultdict(list)
        for scenario in e.get('stress_failure_details',[]):
            stress[tuple(scenario['errors'])].append([scenario['execution_factor'],scenario['close_factor']])
        card['stress_failures']=[{'errors':list(errors),'execution_close_factors':cells} for errors,cells in stress.items()]
        trade=copy.deepcopy(e.get('trade_evidence',{}));trade.pop('note',None)
        # Infeasible proposals cannot be selected. Their errors, failing cells,
        # rules, costs and order count remain; trades remain in frozen evidence.
        if e['errors']:
            trade={'not_replayed_infeasible':True,'order_count':e.get('order_count',0)}
        elif trade.get('rows'):
            trade['rows']=[[v if i<3 else display(v) for i,v in enumerate(row)] for row in trade['rows']]
        card['trade_evidence']=trade;evaluations.append(card)
    columns=list(dict.fromkeys(k for e in evaluations for k in e))
    value['evaluation_columns']=columns
    value['evaluations']=[[e.get(k) for k in columns] for e in evaluations]
    value['strategy_rules']=rules;value['factor_definitions']=factors;value['screen_definitions']=screens
    value['factor_columns']=['feature','direction','transform','weight']
    value['screen_columns']=['feature','operator','value']
    value['trade_evidence_precision']='Scores/features/risk rounded to eight significant digits; exact originals archived. Account/cost/safety unchanged.'
    reviews=data.get('completed_reviews',[])
    value['completed_review_columns']=['review_id','verdict','features']
    value['completed_reviews']=[[r['review_id'],r['verdict'],r.get('features',[])] for r in reviews]
    value['review_detail_scope']='All verdicts retained; checked arguments archived, not reread.'
    memory=data.get('holding_memory')
    value['holding_memory']={k:copy.deepcopy(memory[k]) for k in ['columns','holdings','conflicting_dates'] if k in memory} if memory else None
    value['history_scope']='Original hypotheses copied verbatim to audit; never rewrite or claim to reread omitted history.'
    value['recent_tool_results']=[{k:r[k] for k in ['tool_id','tool','error'] if k in r} for r in data.get('recent_tool_results',[]) if r.get('error')][-1:]
    value['selection_requirements']={'comparison_count':len(evaluations),'trade_reason':'why_not_hold/trade_justification: cite actual traded 個股 代碼 and observed direction.',
        'actual_traded_codes_lookup':'Use the first two columns of the feasible proposal trade_evidence rows.'}
    return value


def fit_context(system,data,config):
    value=selection_view(data) if data.get('phase')=='select' else evaluation_view(data) if data.get('phase')=='evaluate' else copy.deepcopy(data);stages=[]
    budget=max(2048,(config.context_tokens-config.output_tokens-512)*2)
    if data.get('phase') in {'select','evaluate'}:budget-=1024 # reserved for bounded schema repair feedback
    def size():return len(system.encode())+len(encoded(value))
    def record(stage):stages.append({'stage':stage,'bytes':size()})
    # Zero-coverage extensions stay discoverable by category, without repeating
    # definitions for dozens of windows that cannot currently be computed.
    catalog=value.get('catalog',{})
    absent=defaultdict(list);active=[]
    for row in catalog.get('features',[]):
        if row.get('coverage')==0 and row.get('feature') not in {'foreign_net_ratio','trust_net_ratio','dealer_net_ratio'}:
            absent[row.get('category','unknown')].append(row['feature'])
        else:active.append(row)
    if absent:
        catalog['features']=active;catalog['unavailable_features_by_category']=dict(absent)
        catalog['unavailable_note']='No observed values; never fill zero. Full definitions archived.'
        if value.get('phase') not in {None,'inspect'}:
            catalog['unavailable_counts_by_category']={k:len(v) for k,v in absent.items()}
            catalog.pop('unavailable_features_by_category',None)
    record('selection_projection' if data.get('phase')=='select' else 'original')
    if data.get('phase') in {'select','evaluate'}:
        if size()>budget and catalog.get('features'):
            columns=['feature','category','unit','coverage','eligible_universe']
            catalog['features']=[[r.get(k) for k in columns] for r in catalog['features']]
            catalog['feature_columns']=columns;record('dense_evaluation_catalog')
        if size()>budget:
            intern_selection_observations(value);record('shared_trade_and_risk_observations')
        size_bytes=size()
        return value,{'budget_bytes':budget,'system_bytes':len(system.encode()),'total_bytes':size_bytes,
            'section_bytes':{k:len(encoded(v)) for k,v in value.items()},'stages':stages,'fits':size_bytes<=budget,
            'projection_version':value['projection_version'],'unprojected_bytes':len(system.encode())+len(encoded(data)),'reserved_repair_bytes':1024,'note':'Phase-scoped selection; full evidence remains immutable; no safety verdict removed.'}
    if value.get('phase')=='review':
        # The current packet supplies full review evidence; previously reviewed
        # packets are already durable and are required again at final selection.
        value['completed_review_count']=len(value.get('completed_reviews',[]))
        value['completed_reviews']=[]
        for e in value.get('evaluations',[]):e['trade_evidence']={}
        record('review_packet_focus')
    if size()>budget:
        value['recent_tool_results']=value.get('recent_tool_results',[])[-1:]
        for feature in value.get('catalog',{}).get('features',[]):
            for k in ['minimum','maximum','limitation']:feature.pop(k,None)
        value['memory']=value.get('memory','')[:180]
        record('catalog_and_recent')
    if size()>budget:
        for result in value.get('recent_tool_results',[]):
            if isinstance(result.get('selected_evaluation'),dict):
                result['selected_evaluation']={k:v for k,v in result['selected_evaluation'].items() if k in {'errors','locally_selectable','stress_failure_details'}}
            for key in ['rows','items']:
                if isinstance(result.get(key),list) and len(result[key])>3:
                    result['omitted_'+key]=len(result[key])-3;result[key]=result[key][:3]
            if isinstance(result.get('news'),list) and len(result['news'])>3:
                result['omitted_news']=len(result['news'])-3;result['news']=result['news'][:3]
        memory=value.get('holding_memory')
        if memory:
            groups=defaultdict(list)
            for row in memory['holdings']:groups[tuple(row[1:])].append(row[0])
            memory['holdings']=[[codes,*keys] for keys,codes in groups.items()]
            memory['columns']=['codes','entry_thesis_id','last_action','last_reason_id']
        record('group_repeated_memory')
    if size()>budget:
        evaluations=value.get('evaluations',[])
        # Preserve complete factor rules, projected cash, costs, hard errors,
        # stress verdicts and references. Repeated names are column metadata.
        columns=['tool_id','proposal_id','comparison_parent','mode','weighting','cash_target','holdings','factors','screens','errors',
            'cash_ratio','cost_fraction_nav','turnover_notional_fraction','order_count','stress_failure_details',
            'exclusion_counts','missing_feature_counts','replacement_count','risk_comparison','trade_evidence']
        rows=[]
        for e in evaluations:
            p=e['proposal'];factors=[[f[k] for k in ['feature','direction','transform','weight']] for f in p['factors']]
            stress=defaultdict(list)
            for s in e.get('stress_failure_details',[]):stress[tuple(s['errors'])].append([s['execution_factor'],s['close_factor']])
            grouped_stress=[{'errors':list(errors),'execution_close_factors':cells} for errors,cells in stress.items()]
            rows.append([e['tool_id'],p['proposal_id'],e.get('comparison_parent'),p['mode'],p['weighting'],p['cash_target'],e.get('holdings'),
                factors,p.get('screens',[]),e['errors'],e.get('cash_ratio'),e.get('cost_fraction_nav'),
                e.get('turnover_notional_fraction'),e.get('order_count'),grouped_stress,
                e.get('exclusion_counts',{}),e.get('missing_feature_counts',{}),e.get('replacement_count',0),e.get('risk_comparison'),{k:v for k,v in e.get('trade_evidence',{}).items() if k!='note'}])
        value['evaluations']=rows;value['evaluation_columns']=columns
        value['factor_columns']=['feature','direction','transform','weight']
        value['trade_evidence_note']='Frozen observations, not expected returns; omitted_orders is an explicit display limit.'
        # The latest tool evaluation duplicates the table. Retain identifiers
        # and any error feedback, including the exact failing stress cells.
        for i,result in enumerate(value.get('recent_tool_results',[])):
            if 'proposal' in result and not result.get('error'):
                value['recent_tool_results'][i]={k:result[k] for k in ['tool_id','tool','errors','locally_selectable','performance_note'] if k in result}
        record('columnar_evaluations')
    if size()>budget:
        catalog=value.get('catalog',{})
        columns=['feature','category','unit','coverage','eligible_universe']
        if catalog.get('features'):
            catalog['feature_columns']=columns
            catalog['features']=[[f.get(k) for k in columns] for f in catalog['features']]
        for result in value.get('recent_tool_results',[]):
            rows=result.get('rows',[])
            if rows and all('values' in r and 'code' in r for r in rows):
                features=sorted({f for r in rows for f in r['values']})
                result['feature_columns']=features
                result['row_columns']=['code','industry','values','evidence_refs']
                result['rows']=[[r['code'],r.get('industry'),[r['values'].get(f) for f in features],
                    [r.get('evidence_refs',{}).get(f,[]) for f in features]] for r in rows]
        record('dense_reference_tables')
    if size()>budget:
        # Duplicate prose only; identifiers, observed values and all safety facts remain.
        value.pop('objective',None)
        catalog.pop('performance_validation',None)
        record('deduplicate_system_prose')
    telemetry={'budget_bytes':budget,'system_bytes':len(system.encode()),'total_bytes':size(),
        'section_bytes':{k:len(encoded(v)) for k,v in value.items()},'stages':stages,
        'fits':size()<=budget,'note':'Conservative UTF-8 input budget, not an exact tokenizer count; output and protocol reserve remain allocated.'}
    return value,telemetry


def intern_selection_observations(value):
    """Share repeated trade facts across candidates, keeping every value/reference."""
    observations={};risk_values={}
    def intern(table,body,prefix):
        key=prefix+digest(encoded(body))[:16]
        table[key]=body;return key
    columns=value.get('evaluation_columns',[])
    for row in value.get('evaluations',[]):
        card=dict(zip(columns,row));trade=card.get('trade_evidence') or {}
        if trade.get('rows') and len(trade.get('columns',[]))>4:
            features=trade['columns'][4:];new=[]
            for r in trade['rows']:
                key=intern(observations,{'features':features,'values':r[4:]},'V')
                new.append([*r[:4],key])
            trade['columns']=[*trade['columns'][:4],'observation_ref'];trade['rows']=new
        risk=card.get('risk_comparison')
        if risk:
            for key in ('before','after'):
                if key in risk:risk[key+'_ref']=intern(risk_values,risk.pop(key),'K')
    value['trade_observation_definitions']=observations
    value['risk_value_definitions']=risk_values
    value['dictionary_scope']='observation_ref resolves features/values; risk before_ref/after_ref resolves risk_columns values. All values retained.'


def evaluation_view(data):
    """Evaluation reuses bounded cards, not prior full tool prose and duplicated rules."""
    value=selection_view(data);value['projection_version']='evaluation-v1'
    value.pop('selection_requirements',None)
    for key in ['catalog','inspection_limit','researched_categories','news_read','evaluation_contract']:
        if key in data:value[key]=copy.deepcopy(data[key])
    latest=[]
    for r in data.get('recent_tool_results',[]):
        if r.get('error'):
            item={k:copy.deepcopy(v) for k,v in r.items() if k!='selected_evaluation'}
            if r.get('selected_evaluation'):item['selected_evaluation']={k:v for k,v in r['selected_evaluation'].items() if k in {'errors','locally_selectable','stress_failure_details'}}
            latest.append(item)
        elif 'proposal' not in r:
            item=copy.deepcopy(r)
            for key in ['rows','items']:
                if isinstance(item.get(key),list) and len(item[key])>6:
                    item['omitted_'+key]=len(item[key])-6;item[key]=item[key][:6]
            latest.append(item)
    value['recent_tool_results']=latest
    return value
