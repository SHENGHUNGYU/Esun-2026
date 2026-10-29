"""Bound research context without removing account truth or safety verdicts."""
import copy
from collections import defaultdict
from .store import encoded


def fit_context(system,data,config):
    value=copy.deepcopy(data);stages=[]
    budget=max(2048,(config.context_tokens-config.output_tokens-512)*2)
    def size():return len(system.encode())+len(encoded(value))
    def record(stage):stages.append({'stage':stage,'bytes':size()})
    record('original')
    if size()>budget:
        value['recent_tool_results']=value.get('recent_tool_results',[])[-1:]
        for feature in value.get('catalog',{}).get('features',[]):
            for k in ['minimum','maximum','limitation']:feature.pop(k,None)
        value['memory']=value.get('memory','')[:180]
        record('catalog_and_recent')
    if size()>budget:
        for result in value.get('recent_tool_results',[]):
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
        columns=['tool_id','proposal_id','mode','weighting','cash_target','holdings','factors','screens','errors',
            'cash_ratio','cost_fraction_nav','turnover_notional_fraction','order_count','stress_failure_details',
            'exclusion_counts','missing_feature_counts']
        rows=[]
        for e in evaluations:
            p=e['proposal'];factors=[[f[k] for k in ['feature','direction','transform','weight']] for f in p['factors']]
            stress=defaultdict(list)
            for s in e.get('stress_failure_details',[]):stress[tuple(s['errors'])].append([s['execution_factor'],s['close_factor']])
            grouped_stress=[{'errors':list(errors),'execution_close_factors':cells} for errors,cells in stress.items()]
            rows.append([e['tool_id'],p['proposal_id'],p['mode'],p['weighting'],p['cash_target'],e.get('holdings'),
                factors,p.get('screens',[]),e['errors'],e.get('cash_ratio'),e.get('cost_fraction_nav'),
                e.get('turnover_notional_fraction'),e.get('order_count'),grouped_stress,
                e.get('exclusion_counts',{}),e.get('missing_feature_counts',{})])
        value['evaluations']=rows;value['evaluation_columns']=columns
        value['factor_columns']=['feature','direction','transform','weight']
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
    telemetry={'budget_bytes':budget,'system_bytes':len(system.encode()),'total_bytes':size(),
        'section_bytes':{k:len(encoded(v)) for k,v in value.items()},'stages':stages,
        'fits':size()<=budget,'note':'Conservative UTF-8 input budget, not an exact tokenizer count; output and protocol reserve remain allocated.'}
    return value,telemetry
