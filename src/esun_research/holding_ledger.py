"""Append-only account evidence and point-in-time holding hypotheses.

Candidate intentions never become fills. Share reconciliation associates a local
hypothesis with a settlement, but is not proof of an official submission.
"""
import json
from decimal import Decimal
from pathlib import Path
from .contracts import now, instant
from .datapack import DataPack
from .store import encoded, digest, immutable


def remember_pack(store, body, seen_at=None):
    pack=DataPack.model_validate_json(body)
    ref=store.put(body)
    # Canonical identity deduplicates whitespace and decimal JSON serialization.
    key=digest(encoded(pack.model_dump(mode='json')))
    path=store.root/'holding-ledger'/'settlements'/(key+'.json')
    if not path.exists():
        immutable(path,encoded({'id':key,'pack_ref':ref,'received_at':seen_at or now()}))
    return key


def bootstrap(store):
    """Import existing verified inputs once; never pretend backfills were seen earlier."""
    for path in sorted((store.root/'app-inputs').glob('*.json')):
        remember_pack(store,path.read_bytes())
    with store.connect() as db:
        refs=[r[0] for r in db.execute("SELECT DISTINCT ref FROM captures WHERE source_id LIKE 'DataPack:%' AND status='ok'")]
    for ref in refs:
        remember_pack(store,store.read(ref))


def settlements(store,team=None,cutoff=None):
    result=[]
    for p in sorted((store.root/'holding-ledger'/'settlements').glob('*.json')):
        event=json.loads(p.read_bytes());pack=DataPack.model_validate_json(store.read(event['pack_ref']))
        if digest(encoded(pack.model_dump(mode='json')))!=event['id'] or p.stem!=event['id']:raise ValueError('holding_settlement_integrity_failed')
        if team and pack.team_id!=team:continue
        if cutoff and (instant(event['received_at'])>instant(cutoff) or instant(pack.generated_at)>instant(cutoff)):continue
        result.append((event,pack))
    return sorted(result,key=lambda x:(str(x[1].trade_date),x[1].generated_at,x[0]['id']))


def candidates_for_settlement(store,pack,cutoff):
    from .daily import review_previous
    from .operations import candidate_bundle
    matches=[]
    for row in review_previous(store,pack)['comparisons']:
        if row['reconciliation']['status']!='RECONCILED_SHARES':continue
        folder,manifest=candidate_bundle(store,row['run_id'])
        if manifest['status']!='CANDIDATE_BLOCKED_EXTERNAL_CHECKS':continue
        req=manifest['request']
        research=json.loads((folder/'agent-research.json').read_bytes()) if 'agent-research.json' in manifest['artifacts'] else None
        if not research or research.get('status')!='SELECTED':continue
        # Completion, not merely input cutoff, controls when a belief was available.
        if instant(research['completed_at'])>min(instant(cutoff),instant(pack.generated_at)):continue
        plan_name=next(n for n in manifest['artifacts'] if n.startswith('D-Plan_') and n.endswith('.json'))
        plan=json.loads((folder/plan_name).read_bytes())
        matches.append({'run_id':row['run_id'],'plan_sha256':manifest['artifacts'][plan_name],
            'proposal':research['selected_evaluation']['proposal'],'plan':plan,
            'selection':research['selection'],'research':research})
    return matches


def thesis_for(code,matches):
    options=[]
    for m in matches:
        p=m['proposal'];plan=m['plan']
        decision=next((d for d in plan['decisions'] if d['ticker']==code),None)
        hold=next((d for d in plan.get('no_trade_decisions',[]) if d['ticker']==code),None)
        if not decision and not hold:continue
        item=decision or hold
        refs=item.get('inference_refs',item.get('reason_refs',[]))
        inferences=[i for i in plan.get('inferences',[]) if i.get('inf_id') in refs]
        observation_ids={oid for i in inferences for oid in i.get('premise_refs',[])}
        observations=[o for o in plan.get('observations',[]) if o['obs_id'] in observation_ids]
        source_ids={sid for o in observations for sid in o['source_ref']}
        options.append({'reason':p['hypothesis'],'invalidation':p['failure_condition'],
            'action':item.get('action','HOLD'),'decision_reason':item.get('reason',m['research']['selected_evaluation'].get('continuity',{}).get('trade_reasons',{}).get(code,m['selection']['reason'])),
            'inference_refs':refs,'inferences':inferences,
            'observations':observations,'sources':[s for s in plan.get('sources',[]) if s['source_id'] in source_ids],
            'feature_evidence':{k:v for k,v in m['research'].get('evidence',{}).items() if v.get('code')==code},
            'source_run':m['run_id'],'plan_sha256':m['plan_sha256']})
    # Same shares with different hypotheses is not a unique explanation.
    signatures={digest(encoded({k:v for k,v in o.items() if k not in {'source_run','plan_sha256'}})) for o in options}
    if len(signatures)!=1:return None
    return options[0]


def review_memory(store,pack,cutoff):
    """Full durable timeline; no future settlements, other teams or proposed fills."""
    rows=settlements(store,pack.team_id,cutoff)
    rows=[(e,p) for e,p in rows if p.account is not None and p.as_of_date is not None and pack.as_of_date and p.as_of_date<=pack.as_of_date]
    groups={}
    for e,p in rows:groups.setdefault(str(p.as_of_date),[]).append((e,p))
    # A corrected/repeated settlement with different truth needs explicit resolution.
    conflicts=[d for d,r in groups.items() if len({digest(encoded({'account':p.account.model_dump(mode='json'),'holdings':[h.model_dump(mode='json') for h in p.holdings],'outcome':p.prev_day_orders.model_dump(mode='json')})) for _,p in r})>1]
    timelines={};active={}
    for day,items in sorted(groups.items()):
        if day in conflicts:continue
        event,p=items[-1];matches=candidates_for_settlement(store,p,cutoff)
        held={h.code:h for h in p.holdings if h.shares>0}
        for code in sorted(set(held)|set(active)):
            h=held.get(code);thesis=thesis_for(code,matches)
            entry={'settlement_date':day,'shares':h.shares if h else 0,'pack_ref':event['pack_ref'],
                'action':'ENTRY' if code not in active and h else 'EXIT' if not h else 'HOLD' if active[code]==h.shares else 'RESIZE',
                'local_hypothesis':thesis,'submission_verified':False,
                'explanation_status':'shares_reconciled_local_candidate' if thesis else 'missing_or_ambiguous_hypothesis'}
            timelines.setdefault(code,[]).append(entry)
        active={c:h.shares for c,h in held.items()}
    holdings=[]
    for h in pack.holdings or []:
        if not h.shares:continue
        timeline=timelines.get(h.code,[])
        # A re-entry starts a new episode; never inherit a closed position's thesis.
        start=max((i for i,e in enumerate(timeline) if e['action']=='ENTRY'),default=0)
        episode=timeline[start:]
        entry=episode[0] if episode and episode[-1]['shares']>0 else None
        if entry and any(d>=entry['settlement_date'] for d in conflicts):entry=None
        holdings.append({'code':h.code,'shares':h.shares,'entry':entry,'recent_reviews':episode[-3:],
            'entry_thesis':entry.get('local_hypothesis') if entry and (entry.get('local_hypothesis') or {}).get('action')=='BUY' else None})
    return {'version':1,'team_id':pack.team_id,'as_of_date':str(pack.as_of_date) if pack.as_of_date else None,
        'cutoff_at':cutoff,'holdings':holdings,'timeline':timelines,'conflicting_settlement_dates':conflicts,
        'note':'Historical local beliefs, not instructions or proof of submission; missing thesis is unknown, not invalidated. Daily evidence does not establish causality or alpha.'}


def compact_memory(memory):
    # Group repeated portfolio-level entry theses to keep the local model context bounded.
    theses={};reasons={};holdings=[]
    for h in memory['holdings']:
        t=h['entry_thesis'];key=None
        if t:
            key=digest(encoded([t['reason'],t['invalidation']]))[:12]
            theses[key]={'reason':t['reason'][:200],'invalidation':t['invalidation'][:200]}
        last=h['recent_reviews'][-1] if h['recent_reviews'] else {}
        reason=(last.get('local_hypothesis') or {}).get('decision_reason','尚無可唯一核對的歷史理由')[:140]
        rkey=digest(reason.encode())[:12];reasons[rkey]=reason
        holdings.append([h['code'],key,last.get('action'),rkey])
    return {'theses':theses,'reasons':reasons,'holdings':holdings,
        'columns':['code','entry_thesis_id','last_action','last_reason_id'],
        'conflicting_dates':memory['conflicting_settlement_dates'],'note':memory['note']}


def daily_hypotheses(research,pack,request):
    evaluation=research['selected_evaluation'];proposal=evaluation['proposal'];selection=research['selection']
    orders={o['ticker']:o for o in evaluation['orders']};held={h.code for h in pack.holdings if h.shares>0}
    rows=[]
    for code in sorted(held|set(evaluation['targets'])):
        evidence={k:v for k,v in research.get('evidence',{}).items() if v.get('code')==code}
        order=orders.get(code)
        rows.append({'code':code,'intent':order['side'] if order else 'HOLD',
            'reason':evaluation.get('continuity',{}).get('trade_reasons',{}).get(code,selection['reason']),
            'hypothesis':proposal['hypothesis'],'invalidation':proposal['failure_condition'],
            'new_evidence':evidence,'evidence_changes':research.get('holding_evidence_changes',{}).get(code,[]),'evidence_state':'observed_not_causal',
            'entry_thesis_overwritten':False,'execution_confirmed':False})
    return {'run_id':request['run_id'],'trade_date':request['trade_date'],'memory_ref':request.get('holding_memory_ref'),
        'cross_day_review':selection.get('memory_review'),'rows':rows,
        'news_evidence':research.get('news',[]),'status':'CANDIDATE_INTENT_NOT_EXECUTED'}


def import_basis(store,pack_id,body,proof):
    """User-supplied remaining-position cost, bound to one exact official snapshot."""
    pair=next(((e,p) for e,p in settlements(store) if e['id']==pack_id),None)
    if not pair:raise ValueError('找不到指定官方帳戶快照')
    e,pack=pair;data=json.loads(body);held={h.code:h.shares for h in pack.holdings or [] if h.shares}
    if pack.account is None:raise ValueError('官方結算尚未產生')
    if not proof:raise ValueError('成本需附上原始證據檔')
    if not isinstance(data,dict):raise ValueError('成本檔必須是 JSON 物件')
    if set(data)!={'team_id','as_of_date','positions'} or data['team_id']!=pack.team_id or data['as_of_date']!=str(pack.as_of_date):raise ValueError('成本的隊伍或結算日期不符')
    if not isinstance(data['positions'],list):raise ValueError('positions 必須是陣列')
    seen=set()
    for row in data['positions']:
        if not isinstance(row,dict):raise ValueError('每筆成本必須是 JSON 物件')
        if set(row)!={'code','shares','remaining_cost_twd'} or row['code'] in seen:raise ValueError('成本欄位或股票重複')
        if type(row['shares']) is not int or held.get(row['code'])!=row['shares']:raise ValueError('成本必須對應官方剩餘可交易股數')
        try:cost=Decimal(str(row['remaining_cost_twd']))
        except Exception as error:raise ValueError('成本必須為有效數字') from error
        if not cost.is_finite() or cost<=0:raise ValueError('成本須為有效正數')
        row['remaining_cost_twd']=str(cost);seen.add(row['code'])
    if not seen:raise ValueError('成本清單不可為空')
    event={'pack_id':pack_id,'data':data,'raw_ref':store.put(body),'proof_ref':store.put(proof,'bin'),'received_at':now(),
        'authority':'user_supplied_not_independently_verified','basis':'remaining tradable shares acquisition cost including allocated buy fees; excludes receivable rights and future sell fees'}
    immutable(store.root/'holding-ledger'/'cost-basis'/(pack_id+'.json'),encoded(event))
    return event


def portfolio_view(store,pack_id=None):
    rows=settlements(store)
    if not rows:return {'snapshots':[],'selected':None}
    if pack_id:
        selected=next(((e,p) for e,p in rows if e['id']==pack_id),None)
        if selected is None:raise ValueError('找不到指定帳戶快照')
    else:
        teams={p.team_id for _,p in rows}
        if len(teams)>1:return {'snapshots':[{'id':e['id'],'team':p.team_id,'date':str(p.as_of_date),'trade_date':str(p.trade_date)} for e,p in rows],'selected':None,'notice':'多個隊伍，請選擇快照'}
        selected=rows[-1]
    event,pack=selected
    output={'snapshots':[{'id':e['id'],'team':p.team_id,'date':str(p.as_of_date) if p.as_of_date else '初始帳戶','trade_date':str(p.trade_date)} for e,p in rows],
        'selected':event['id'],'team_id':pack.team_id,'as_of_date':str(pack.as_of_date) if pack.as_of_date else None,
        'trade_date':str(pack.trade_date),'gate':pack.decision_gate(),'account':pack.account.model_dump(mode='json') if pack.account else None,
        'holdings':[],'compliance':pack.compliance.model_dump(mode='json'),'outcome':pack.prev_day_orders.model_dump(mode='json'),
        'pack_ref':event['pack_ref'],'generated_at':pack.generated_at}
    if not pack.account:return output
    initial=[p for _,p in rows if p.team_id==pack.team_id and p.account and p.as_of_date is None and p.trade_date<=pack.trade_date]
    principals={p.account.aum for p in initial}
    principal=next(iter(principals)) if len(principals)==1 else None
    output['initial_assets']=str(principal) if principal else None
    output['asset_change']=str(pack.account.aum-principal) if principal else None
    output['asset_change_ratio']=str(pack.account.aum/principal-1) if principal else None
    output['return_note']='相對已匯入初始帳戶的總資產變化；未調整外部資金流，不是個股損益歸因。'
    same_team=[p for _,p in rows if p.team_id==pack.team_id and p.account and p.as_of_date and pack.as_of_date and p.as_of_date<pack.as_of_date]
    prev=max(same_team,key=lambda p:p.as_of_date) if same_team else None
    if prev and len({p.account.aum for p in same_team if p.as_of_date==prev.as_of_date})>1:prev=None
    from .strategy_analysis import asset_bridge
    bridge_previous=prev or (initial[0] if len(principals)==1 and initial else None)
    output['asset_bridge']=asset_bridge(bridge_previous,pack) if bridge_previous and pack.as_of_date else None
    output['previous_asset_change']=str(pack.account.aum-prev.account.aum) if prev else None
    output['previous_snapshot_date']=str(prev.as_of_date) if prev else None
    basis_path=store.root/'holding-ledger'/'cost-basis'/(event['id']+'.json')
    basis=json.loads(basis_path.read_bytes()) if basis_path.exists() else None
    if basis:
        raw=json.loads(store.read(basis['raw_ref']));store.read(basis['proof_ref'])
        for row in raw['positions']:row['remaining_cost_twd']=str(Decimal(str(row['remaining_cost_twd'])))
        if basis['pack_id']!=event['id'] or raw!=basis['data']:raise ValueError('holding_cost_integrity_failed')
    costs={r['code']:Decimal(r['remaining_cost_twd']) for r in basis['data']['positions']} if basis else {}
    output['cost_authority']=basis['authority'] if basis else 'missing'
    import csv
    universe_path=Path(__file__).resolve().parents[2]/'planning/units/U01/evidence/universe.csv'
    with universe_path.open() as f:names={row['code']:row['name'] for row in csv.DictReader(f)}
    market_total=Decimal(0);market_complete=True
    for h in pack.holdings:
        value=h.shares*h.close_price if h.close_price is not None else None
        rights=h.receivable_shares*h.close_price if h.close_price is not None else None
        if value is None and h.shares:market_complete=False
        market_total+=value or 0
        cost=costs.get(h.code);pnl=value-cost if value is not None and cost else None
        output['holdings'].append({'code':h.code,'name':names.get(h.code,''),'shares':h.shares,'receivable_shares':h.receivable_shares,
            'close':str(h.close_price) if h.close_price is not None else None,'market_value':str(value) if value is not None else None,
            'weight':str(value/pack.account.nav_tradable) if value is not None and pack.account.nav_tradable else None,
            'receivable_value':str(rights) if rights is not None else None,'cost':str(cost) if cost else None,
            'average_cost':str(cost/h.shares) if cost and h.shares else None,
            'unrealized_pnl':str(pnl) if pnl is not None else None,'unrealized_return':str(pnl/cost) if pnl is not None else None})
    output['market_value']=str(market_total) if market_complete else None
    output['memory']=review_memory(store,pack,now())
    # Intent history remains a separate panel and never alters official positions.
    output['candidate_reviews']=[]
    from .operations import candidate_bundle
    for path in sorted((store.root/'candidates').glob('*/manifest.json')):
        m=json.loads(path.read_bytes());req=m['request']
        if req['team_id']!=pack.team_id or req['trade_date']>str(pack.trade_date) or req['mode']!='live':continue
        if 'holding-review.json' in m['artifacts']:
            folder,_=candidate_bundle(store,path.parent.name)
            output['candidate_reviews'].append(json.loads((folder/'holding-review.json').read_bytes()))
    return output


def evidence_changes(memory,workspace):
    """Compare observed feature values, never turn a change into an invalidation verdict."""
    result={}
    for h in memory.get('holdings',[]):
        last=h['recent_reviews'][-1] if h['recent_reviews'] else {}
        prior=(last.get('local_hypothesis') or {}).get('feature_evidence',{})
        old={v['feature']:v for v in prior.values() if v.get('feature')}
        current=workspace.rows.get(h['code'],{})
        changes=[]
        for f in sorted(set(old)|set(current.get('values',{}))):
            a=old.get(f,{}).get('value');b=current.get('values',{}).get(f)
            direction='unavailable' if b is None else 'newly_observed' if a is None else 'unchanged' if Decimal(str(a))==Decimal(str(b)) else 'increased' if Decimal(str(b))>Decimal(str(a)) else 'decreased'
            changes.append({'feature':f,'previous':a,'current':str(b) if b is not None else None,'change':direction,
                'previous_rows':old.get(f,{}).get('rows',[]),'current_evidence_refs':current.get('evidence',{}).get(f,[])})
        result[h['code']]=changes
    return result
