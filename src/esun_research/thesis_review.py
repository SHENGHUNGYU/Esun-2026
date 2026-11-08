"""Evidence-bound, symmetric reviews before either holding or trading.

Attention rules select questions, never trades or thesis verdicts. Full source
rows remain in immutable packets; the model sees a bounded batch of questions.
"""
from decimal import Decimal
import copy
from .store import digest, encoded
from .decision_review import trade_observations


def review_packets(workspace, memory, changes, evaluations):
    held={h.code for h in workspace.pack.holdings if h.shares>0}
    if not workspace.pack.as_of_date or not held:return {}
    historical={h['code']:h for h in (memory or {}).get('holdings',[])}
    attention={}
    for code in sorted(held):
        values=workspace.rows.get(code,{}).get('values',{})
        negative=lambda f:values.get(f) is not None and Decimal(values[f])<0
        reasons=[]
        if (negative('momentum_5') or negative('momentum_20')) and negative('foreign_net_ratio'):
            reasons.append('negative_momentum_and_foreign_flow')
        if reasons:attention[code]=reasons
    for pid,e in evaluations.items():
        if not e['proposal']['factors']:continue
        for o in e.get('orders',[]):
            if o['side']=='SELL' and o['ticker'] in held:
                attention.setdefault(o['ticker'],[]).append('candidate_reduction:'+pid)
    packets={}
    for code,reasons in sorted(attention.items()):
        h=historical.get(code,{})
        thesis=h.get('entry_thesis') or {}
        features=['momentum_5','momentum_20','foreign_net_ratio','trust_net_ratio','revenue_yoy_pct','earnings_yield',
            'momentum_1','momentum_3','foreign_net_ratio_5','foreign_buy_days_5','trust_net_ratio_5','relative_pool_20',
            'relative_industry_20','volume_ratio_5','ma_distance_20','drawdown_20']
        rows=[r for r in changes.get(code,[]) if r['feature'] in features]
        # Include observed new dimensions even when prior memory did not store them.
        current=workspace.rows.get(code,{})
        present={r['feature'] for r in rows}
        rows += [{'feature':f,'previous':None,'current':current.get('values',{}).get(f),'change':'unavailable',
                   'previous_rows':[],'current_evidence_refs':current.get('evidence',{}).get(f,[])} for f in features if f not in present]
        current_refs=sorted({eid for r in rows for eid in r.get('current_evidence_refs',[])})
        raw={eid:workspace.evidence[eid] for eid in current_refs}
        dates=lambda rs:sorted({r['date'] for r in rs if r.get('date')})
        feature_rows=[]
        for r in rows:
            old_dates=dates(r.get('previous_rows',[]));new_dates=dates([row for eid in r.get('current_evidence_refs',[]) for row in raw[eid].get('rows',[])])
            feature_rows.append([r['feature'],r['previous'],r['current'],max(old_dates,default=None),max(new_dates,default=None),r['change']])
        ranked=[]
        for pid,e in evaluations.items():
            if not e['proposal']['factors'] or pid.startswith('ALT_'):continue
            row=next(((i+1,r) for i,r in enumerate(e.get('ranking',[])) if r['code']==code),None)
            if row:ranked.append([pid,row[0],len(e['ranking']),str(row[1]['score'])])
        news=[n for n in workspace.news if n.get('code')==code]
        packets['H'+code]={'kind':'holding','code':code,'triggers':reasons,
            'original_hypothesis':thesis.get('reason'),'original_invalidation':thesis.get('invalidation'),
            'historical_source_run':thesis.get('source_run'),'history_is_submission_proof':False,
            'feature_columns':['feature','previous','current','previous_observation_date','current_observation_date','change'],
            'feature_rows':feature_rows,'named_rank_columns':['proposal','rank','universe','score'],'named_ranks':ranked,
            'news':news[:2],'omitted_news':max(0,len(news)-2),'news_absence_is_not_no_news':True,
            'source_evidence':raw,'previous_source_rows':{r['feature']:r.get('previous_rows',[]) for r in rows},
            'current_account_errors':evaluations.get('BASE_HOLD',{}).get('errors'),
            'alternatives':[{'proposal_id':pid,'mode':e['proposal']['mode'],'errors':e['errors'],
                'orders_for_this_holding':[o for o in e.get('orders',[]) if o['ticker']==code],
                'portfolio_cost_twd':e.get('cost_twd'),'portfolio_turnover':e.get('turnover_notional_fraction')}
                for pid,e in evaluations.items() if e['proposal']['factors']],
            'note':'Two snapshots are not a continuous daily series. Negative signals and candidate reductions require review, not sale. Compare original hypothesis, counter-evidence, holding, gradual and replacement.'}
    def consequence(e):
        return {k:e.get(k) for k in ['errors','orders','cost_twd','cost_fraction_nav','turnover_notional_fraction','cash_ratio','replacement_count']}
    for pid,e in evaluations.items():
        if e['proposal']['mode']!='gradual':continue
        parent=e.get('comparison_parent')
        packets['G'+pid]={'kind':'gradual','proposal_id':pid,'parent_id':parent,
            'factors':e['proposal']['factors'],'gradual':consequence(e),
            'hold':consequence(evaluations['BASE_HOLD']) if 'BASE_HOLD' in evaluations else None,
            'replacement':consequence(evaluations[parent]) if parent in evaluations else None,
            'trade_evidence':trade_observations(e),
            'risk_comparison':e.get('risk_comparison'),
            'hold_risk_comparison':evaluations.get('BASE_HOLD',{}).get('risk_comparison'),
            'note':'Cost is not expected benefit. Compare which exposures change, costs, residual weak positions and evidence uncertainty. A lower cost alone does not establish superiority.'}
    for pid,e in evaluations.items():
        if e['proposal']['mode']!='cash_probe':continue
        features=['revenue_yoy_pct','relative_pool_20','momentum_1','momentum_3','foreign_net_ratio_3','trust_net_ratio_3']
        purchases=[];eids=set()
        for order in e.get('orders',[]):
            c=order['ticker'];current=workspace.rows.get(c,{})
            purchases.append({'code':c,'shares':order['shares'],'observations':{f:current.get('values',{}).get(f) for f in features},
                'evidence_refs':{f:current.get('evidence',{}).get(f,[]) for f in features}})
            eids.update(eid for f in features for eid in current.get('evidence',{}).get(f,[]))
        packets['C'+pid]={'kind':'deployment','proposal_id':pid,'market_state':getattr(workspace,'market_state',{}),
            'cash_deployment':e.get('cash_deployment'),'purchases':purchases,'outcome':consequence(e),
            'hold':consequence(evaluations['BASE_HOLD']) if 'BASE_HOLD' in evaluations else None,
            'risk_comparison':e.get('risk_comparison'),
            'source_evidence':{eid:workspace.evidence[eid] for eid in eids},
            'note':'Compare opportunity and drawdown risk, not only fees. Initial stabilization is not a confirmed bottom. No eligible purchase is a valid outcome.'}
    for key,packet in packets.items():
        packet['review_id']=key
        packet['input_hash']=digest(encoded(packet))
    return packets


def pending_reviews(packets,completed):
    return [k for k,p in packets.items() if completed.get(k,{}).get('input_hash')!=p['input_hash']]


def review_batch(packets,completed):
    pending=pending_reviews(packets,completed)
    if not pending:return []
    kind=packets[pending[0]]['kind']
    return [key for key in pending if packets[key]['kind']==kind][:2]


def prompt_packet(packet):
    result={k:v for k,v in packet.items() if k not in {'source_evidence','previous_source_rows','input_hash'}}
    if packet['kind']=='holding':
        result['available_features']=[r[0] for r in packet['feature_rows'] if r[2] is not None]
        result['missing_features']=[r[0] for r in packet['feature_rows'] if r[2] is None]
    return result


def scoped_review_definitions(base,packets,batch):
    """Bind each review to its own code, evidence and non-null features."""
    definitions={};variants=[]
    for index,key in enumerate(batch):
        schema=copy.deepcopy(base);p=packets[key];props=schema['properties']
        props['review_id']['enum']=[key];props['evidence_refs']['items']['enum']=[key]
        if p['kind']=='holding':
            allowed=[r[0] for r in p['feature_rows'] if r[2] is not None]
            props['features']['items']={'type':'string','enum':allowed} if allowed else {'type':'string'}
            props['features']['minItems']=1 if allowed else 0
            if not allowed:props['features']['maxItems']=0
        schema['required']=list(dict.fromkeys(schema['required']+['features']))
        for field in ['reason','counter_evidence','action_tradeoff']:props[field].pop('pattern',None)
        name='ScopedReview'+str(index);definitions[name]=schema;variants.append({'$ref':'#/$defs/'+name})
    return definitions,{'anyOf':variants}


def check_reviews(items,packets,required):
    ids=[r.review_id for r in items]
    if len(ids)!=len(set(ids)) or set(ids)!=set(required):raise ValueError('review_batch_coverage_mismatch')
    for r in items:
        p=packets[r.review_id]
        if r.evidence_refs!=[r.review_id]:raise ValueError('review_requires_own_packet_reference')
        if p['kind']=='holding':
            if r.verdict not in {'supported','weakened','invalidated','unknown'}:raise ValueError('invalid_holding_verdict')
            if not p['original_hypothesis'] and r.verdict!='unknown':raise ValueError('missing_original_thesis_requires_unknown')
            allowed={row[0] for row in p['feature_rows'] if row[2] is not None}
            if allowed and (not r.features or not set(r.features)<=allowed):
                raise ValueError('review_requires_observed_features:'+r.review_id+':allowed='+','.join(sorted(allowed))+':invalid='+','.join(sorted(set(r.features)-allowed)))
        elif r.verdict not in {'useful','insufficient','uncertain'}:raise ValueError('invalid_gradual_verdict')


def review_markdown(packets,reviews):
    lines=['# 跨日假說與漸進方案檢查','','下列結論為模型解讀；原始假說與輸入封存，不是成交證據或績效驗證。','']
    for key,p in packets.items():
        r=reviews[key]['value']
        lines.extend(['## '+key+' — '+r['verdict'],'',
            '原始假說：'+(p.get('original_hypothesis') or '不適用／未知'),
            '原始失效條件：'+(p.get('original_invalidation') or '不適用／未知'),
            '當日判斷：'+r['reason'],'反證／不確定性：'+r['counter_evidence'],
            '續抱／調整取捨：'+r['action_tradeoff'],'輸入雜湊：'+p['input_hash'],''])
    return '\n'.join(lines)
