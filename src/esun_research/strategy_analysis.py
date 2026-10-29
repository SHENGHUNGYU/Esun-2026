"""Selection diagnostics and accounting bridges; never infer fills or alpha."""
from collections import Counter
from decimal import Decimal
from .portfolio import decimal


def selection_diagnostics(workspace,spec,ranked,targets):
    snapshot=workspace.snapshot;rank={r['code']:i+1 for i,r in enumerate(ranked)}
    required={f.feature for f in spec.factors}|{s.feature for s in spec.screens}
    exclusions={r['code']:r['reason'] for r in snapshot['exclusions']}
    held={h.code for h in workspace.pack.holdings if h.shares>0};rows=[]
    for entry in snapshot['coverage']:
        code=entry['code'];values=workspace.rows.get(code,{}).get('values',{})
        missing=sorted(required-set(values));failed=[]
        for screen in spec.screens:
            if screen.feature not in values:continue
            v=decimal(values[screen.feature]);cut=screen.value
            if not {'gt':v>cut,'ge':v>=cut,'lt':v<cut,'le':v<=cut}[screen.operator]:failed.append(screen.model_dump(mode='json'))
        stage=('quote_unavailable' if not entry['valid'] else 'preselection_excluded' if code in exclusions
            else 'missing_features' if missing else 'screen_failed' if failed else 'ranked')
        rows.append({'code':code,'stage':stage,'preselection_reason':exclusions.get(code),'missing_features':missing,
            'failed_screens':failed,'rank':rank.get(code),'held':code in held,'targeted':code in targets,
            'allocation_outcome':'targeted' if code in targets else 'not_targeted' if targets else 'allocation_unavailable',
            'feature_evidence':workspace.rows.get(code,{}).get('evidence',{}),
            'note':'Missing data is not a bearish signal. Ranked but not targeted can reflect caps, lots or continuity; rank alone does not identify the cause.'})
    return {'rows':rows,'counts':dict(Counter(r['stage'] for r in rows)),
        'missing_feature_counts':dict(Counter(f for r in rows for f in r['missing_features'])),
        'required_features':sorted(required),'universe_count':len(rows)}


def asset_bridge(previous,current,closing_prices=None,price_date=None):
    """Exact two-snapshot identity, not execution-price P&L attribution.

ΔAUM = Σ(q0*(p1-p0)) + Σ((q1-q0)*p1) + Δcash + Δ(AUM-NAV).
Unknown marks remain in an explicit residual. Corporate actions confound the
price component, so it is always labelled an unadjusted valuation bridge.
"""
    if previous.team_id!=current.team_id:raise ValueError('attribution_team_mismatch')
    if not previous.account or not current.account:return {'status':'UNAVAILABLE','reason':'missing_settlement'}
    if not current.as_of_date or (previous.as_of_date and previous.as_of_date>=current.as_of_date):raise ValueError('attribution_date_order')
    if closing_prices is not None and str(price_date)!=str(current.as_of_date):raise ValueError('attribution_price_date_mismatch')
    old={h.code:h for h in previous.holdings if h.shares>0};new={h.code:h for h in current.holdings if h.shares>0}
    rows=[];price_total=Decimal(0);quantity_total=Decimal(0);unavailable=[]
    for code in sorted(set(old)|set(new)):
        a,b=old.get(code),new.get(code);q0=a.shares if a else 0;q1=b.shares if b else 0
        p0=a.close_price if a else None;p1=b.close_price if b else None
        if p1 is None and code in (closing_prices or {}):p1=decimal(closing_prices[code])
        # A completely exited stock has no closing quote in DataPack. Do not invent one.
        if p1 is None or (q0 and p0 is None):
            unavailable.append(code);rows.append({'code':code,'status':'missing_close','old_shares':q0,'new_shares':q1});continue
        price=q0*(p1-p0) if q0 else Decimal(0);quantity=(q1-q0)*p1
        price_total+=price;quantity_total+=quantity
        rows.append({'code':code,'status':'unadjusted_bridge','old_shares':q0,'new_shares':q1,
            'previous_close':str(p0) if p0 is not None else None,'current_close':str(p1),
            'price_effect':str(price),'quantity_at_close_effect':str(quantity),
            'price_contribution':str(price/previous.account.aum) if previous.account.aum else None})
    delta=current.account.aum-previous.account.aum;cash=current.account.cash-previous.account.cash
    rights=(current.account.aum-current.account.nav_tradable)-(previous.account.aum-previous.account.nav_tradable)
    residual=delta-price_total-quantity_total-cash-rights
    return {'status':'COMPLETE_BRIDGE' if not unavailable and abs(residual)<=Decimal('.01') else 'PARTIAL_BRIDGE',
        'from_date':str(previous.as_of_date) if previous.as_of_date else 'initial_cash','to_date':str(current.as_of_date),
        'previous_aum':str(previous.account.aum),'current_aum':str(current.account.aum),'aum_change':str(delta),
        'aum_change_ratio':str(delta/previous.account.aum) if previous.account.aum else None,
        'price_effect':str(price_total),'quantity_at_close_effect':str(quantity_total),'cash_change':str(cash),
        'receivables_value_change':str(rights),'unexplained_residual':str(residual),'missing_codes':unavailable,'rows':rows,
        'limits':['非還原收盤價；除權息、分割及股數調整可能影響拆解，不能視為純市場報酬。',
            '現金變化包含交易、費稅及其他現金流；沒有官方成交明細，不能分離已實現損益與費用。',
            '區間為兩份已取得結算，不保證相鄰交易日；未建立同期指數、市值或產業基準歸因。']}


def run_analysis(store,run_id,refresh=False):
    """Reproducible offline comparison; never emits or submits a D-Plan."""
    import json
    from .operations import candidate_bundle
    from .candidate import prepare,jsonable
    from .cli import candidate_sources,settings,code_hash
    from .contracts import now,instant
    from .datapack import DataPack
    from .portfolio import Policy,estimate
    from .research_tools import ResearchWorkspace,AgentSettings
    from .holding_ledger import remember_pack,portfolio_view
    from .store import encoded,digest,immutable
    folder,manifest=candidate_bundle(store,run_id)
    frozen=json.loads((folder/'request.json').read_bytes());req=dict(frozen['request'])
    if req['mode']!='live':raise ValueError('analysis_requires_live_evidence')
    pack=DataPack.model_validate_json(store.read(req['datapack_ref']))
    policy=Policy.model_validate(store.json(req['policy_ref']))
    sources=candidate_sources(True);_,universe=settings()
    if refresh:
        req['cutoff_at']=now()
        frozen={'request':req,'captures':{s.id:store.select_reference(s,req['cutoff_at'],req['as_of']) for s in sources}}
        snapshot=prepare(store,sources,universe,frozen,pack,policy)
    else:snapshot=json.loads((folder/'snapshot.json').read_bytes())
    proposal=None;proposal_origin=None
    if 'agent-research.json' in manifest['artifacts']:
        research=json.loads((folder/'agent-research.json').read_bytes())
        if research.get('selected_evaluation'):
            proposal=research['selected_evaluation']['proposal'];proposal_origin=run_id
    if proposal is None and req.get('previous_strategy_ref'):
        prior=store.json(req['previous_strategy_ref']);proposal=prior.get('proposal');proposal_origin=prior.get('run_id')
    if proposal is None:raise ValueError('no_verified_strategy_for_comparison')
    controls=AgentSettings.model_validate_json((__import__('pathlib').Path(__file__).resolve().parents[2]/'config/strategy-agent.json').read_bytes())
    extra=store.json(req['research_data_ref']) if req.get('research_data_ref') else None
    workspace=ResearchWorkspace(snapshot,pack,policy,controls,extra)
    original=workspace.evaluate(proposal)
    experiment_proposal=proposal;coverage_candidates=[]
    # If the original factors are unavailable, explicitly compare a previously
    # researched alternative. Do not silently renormalize missing factors.
    if proposal_origin:
        pf,pm=candidate_bundle(store,proposal_origin)
        if 'agent-research.json' in pm['artifacts']:
            past=json.loads((pf/'agent-research.json').read_bytes())
            if instant(past['completed_at'])<=instant(req['cutoff_at']):
                for pid,e in past['evaluations'].items():
                    if pid.startswith('BASE_'):continue
                    candidate=store.json(e['ref'])['proposal'];ev=workspace.evaluate(candidate)
                    coverage_candidates.append({'proposal':candidate,'eligible_count':ev['eligible_count']})
    if not original['eligible_count'] and coverage_candidates:
        experiment_proposal=max(coverage_candidates,key=lambda r:(r['eligible_count'],r['proposal']['proposal_id']))['proposal']
    comparisons={}
    for pid,mode,weight in [('HOLD','hold','equal'),('FIXED_EQUAL','gradual','equal'),('FIXED_RANK_TILT','gradual','rank_tilt')]:
        spec={**experiment_proposal,'proposal_id':pid,'mode':mode,'weighting':weight}
        if mode=='hold':spec.update(factors=[],screens=[])
        e=workspace.evaluate(spec)
        comparisons[pid]=jsonable(e)
        if 'orders' in e:
            projection=estimate(pack,e['orders'],snapshot['prices'],policy)
            comparisons[pid]['projected_positions']=projection['positions']
            comparisons[pid]['projected_cash']=str(projection['cash'])
    # Pair only historical snapshots of this account, using existing conflict safeguards.
    pack_id=remember_pack(store,store.read(req['datapack_ref']),req['datapack_seen_at'])
    view=portfolio_view(store,pack_id)
    bridge=view.get('asset_bridge');bridge_inputs=None
    if bridge:
        from .holding_ledger import settlements
        prior=[(event,p) for event,p in settlements(store,pack.team_id,req['cutoff_at']) if p.account and (str(p.as_of_date) if p.as_of_date else 'initial_cash')==bridge['from_date']]
        if prior:
            event,previous=prior[-1]
            bridge=asset_bridge(previous,pack,snapshot['prices'],req['as_of'])
            bridge_inputs={'previous_pack_ref':event['pack_ref'],'current_pack_ref':req['datapack_ref'],'closing_price_date':req['as_of']}
        else:bridge=None
    inputs={'source_run':run_id,'source_manifest_sha256':digest((folder/'manifest.json').read_bytes()),
        'code_hash':code_hash(),'bridge_inputs':bridge_inputs,'frozen':frozen,'snapshot_sha256':digest(encoded(jsonable(snapshot))),
        'proposal':proposal,'experiment_proposal':experiment_proposal,'proposal_origin':proposal_origin,'settings':controls.model_dump(mode='json')}
    identity=digest(encoded(inputs))[:16];output=store.root/'strategy-analysis'/identity
    result={'id':identity,'team_id':pack.team_id,'trade_date':str(pack.trade_date),'reference_date':req['as_of'],
        'cutoff_at':req['cutoff_at'],'source_run':run_id,'proposal_origin':proposal_origin,
        'input_errors':snapshot['errors'],'diagnostics':original['diagnostics'],'asset_bridge':bridge,
        'experiment_proposal':experiment_proposal,'experiment_choice_reason':'Original policy if eligible; otherwise highest coverage previously researched alternative, not a performance selection.',
        'coverage_candidates':coverage_candidates,
        'comparisons':comparisons,'same_basket':all(set(e.get('projected_positions',{}))=={h.code for h in pack.holdings if h.shares>0} for e in comparisons.values()),
        'note':'Frozen-proposal offline experiments, not a new LLM selection, backtest or recommendation. Both resize variants preserve names and finance buys with trims; fees and whole lots may increase residual cash. No D-Plan was emitted.'}
    immutable(output/'inputs.json',encoded(inputs));immutable(output/'snapshot.json',encoded(jsonable(snapshot)))
    immutable(output/'report.json',encoded(result))
    lines=['# 選股診斷與漸進配置實驗','',f'行情基準：{req["as_of"]}；來源：{run_id}',
        '', '此報告重播既有策略，未呼叫 LLM 選定新方案、未產生 D-Plan，也不是樣本外績效驗證。',
        '', '## 排除診斷','',json.dumps(original['diagnostics']['counts'],ensure_ascii=False),'',
        '缺少因子：'+json.dumps(original['diagnostics']['missing_feature_counts'],ensure_ascii=False),'',
        '## 同籃子、原有現金不動用的配置比較','', '| 方案 | 委託筆數 | 費稅估算 | 買賣合計/NAV | 錯誤 |','|---|---:|---:|---:|---|']
    for pid,e in comparisons.items():lines.append(f"| {pid} | {len(e.get('orders',[]))} | {e.get('cost_twd','未知')} | {e.get('turnover_notional_fraction','未知')} | {','.join(e['errors']) or '無'} |")
    lines+=['','實驗因子方案：'+experiment_proposal['name']+'。原方案缺值時的替代僅依資料覆蓋選擇，不代表報酬勝出。',
        '','## 官方資產變化橋接','']
    if bridge:
        lines+=[bridge['from_date']+' → '+bridge['to_date'],'','| 項目 | 新台幣 |','|---|---:|']
        for key,label in [('aum_change','總資產變化'),('price_effect','原股數乘未還原收盤價變化'),('quantity_at_close_effect','股數變化按期末收盤計價'),('cash_change','現金變化'),('receivables_value_change','應收權益市值變化'),('unexplained_residual','未解釋差額')]:lines.append('| '+label+' | '+bridge[key]+' |')
        lines+=['']+['- '+x for x in bridge['limits']]
    else:lines+=['尚無可比較結算。']
    lines+=['','## 逐股排除診斷','','| 代碼 | 階段 | 缺少因子／原因 | 排名 | 原持有 | 目標持有 |','|---|---|---|---:|---|---|']
    for row in original['diagnostics']['rows']:
        lines.append('| '+row['code']+' | '+row['stage']+' | '+(', '.join(row['missing_features']) or row['preselection_reason'] or '—')+' | '+str(row['rank'] or '—')+' | '+str(row['held'])+' | '+str(row['targeted'])+' |')
    lines+=['','完整逐股診斷、結算拆解與來源參照見 report.json 和 inputs.json。估算成交使用參考收盤價，正式比賽成交價未知。']
    immutable(output/'report.md',('\n'.join(lines)+'\n').encode())
    immutable(output/'manifest.json',encoded({'artifacts':{name:digest((output/name).read_bytes()) for name in ['inputs.json','snapshot.json','report.json','report.md']}}))
    return output,result


if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    from .store import Store
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True);parser.add_argument('--run-id',required=True)
    parser.add_argument('--refresh',action='store_true',help='Reselect latest captured evidence; does not download sources')
    args=parser.parse_args();folder,result=run_analysis(Store(args.root),args.run_id,args.refresh)
    print(json.dumps({'folder':str(folder),'input_errors':result['input_errors'],'diagnostic_counts':result['diagnostics']['counts']},ensure_ascii=False))
