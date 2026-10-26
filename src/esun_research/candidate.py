"""Frozen snapshots → autonomous baseline → locally validated D-Plan candidate.

No submission transport exists in this module. External checks stay explicit.
"""
import json
import calendar
import sqlite3
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .contracts import RunRequest,instant,now
from .datapack import load_datapack
from .normalize import normalize,day
from .store import encoded,digest,immutable
from .portfolio import Policy,decimal,rank_candidates,allocate,target_shares,compile_orders,estimate,breaches
from .dplan import validate_plan
from .risk import FEEDS, RiskPolicy, assess, order_errors

class DecisionRequest(RunRequest):
    team_id: str
    trade_date: date
    mode: Literal['live','fixture']
    datapack_ref: str
    policy_ref: str
    schema_ref: str
    session_ref: str
    datapack_seen_at: str
    risk_policy_ref: str | None = None
    llm_ref: str | None = None
    benchmark_universe_ref: str | None = None
    benchmark_refs: list[str] = []
    decision_engine: Literal['baseline','llm_agent'] = 'baseline'
    agent_settings_ref: str | None = None
    research_data_ref: str | None = None

class State(TypedDict,total=False):
    snapshot: str
    features: str
    allocation: str
    plan: str
    validation: str
    llm_review: str
    active_share: str
    errors: list[str]
    status: str
    report: str
    agent_research: str

def jsonable(value):
    if isinstance(value,Decimal):return str(value)
    if isinstance(value,dict):return {k:jsonable(v) for k,v in value.items()}
    if isinstance(value,list):return [jsonable(v) for v in value]
    return value

def prepare(store,sources,universe,frozen,pack,policy):
    req=frozen['request'];records=[];issues=[];errors=[]
    if pack.decision_gate().startswith('BLOCKED'):errors.append(pack.decision_gate())
    if instant(pack.generated_at)>instant(req['cutoff_at']) or instant(req['datapack_seen_at'])>instant(req['cutoff_at']):errors.append('datapack_after_cutoff')
    if req['mode']=='live':
        session=store.json(req['session_ref'])
        expected=pack.as_of_date.isoformat() if pack.as_of_date else session['first_reference_date']
        if req['as_of']!=expected:errors.append('official_reference_date_mismatch')
        if pack.as_of_date is None and pack.trade_date.isoformat()!=session['first_trade_date']:errors.append('unverified_initial_trade_date')
    for s in sources:
        if s.id in FEEDS:continue  # Dedicated date/interval semantics below.
        c=frozen['captures'][s.id]
        if c['status']!='ok':issues.append({'source':s.id,'reason':c.get('error') or c['status']});continue
        rows,problems=normalize(s,c,store.read(c['ref']),universe,req['cutoff_at'])
        records.extend(rows);issues.extend(problems)
    by=defaultdict(list)
    for r in records:by[(r['kind'],r['security_id'])].append(r)
    prices={};coverage=[]
    for code in sorted(universe):
        quotes=[r for r in by[('quotes',code)] if r['date']==req['as_of']]
        valid=len(quotes)==1 and all(quotes[0]['values'].get(k) is not None for k in ['open','high','low','close','volume','amount'])
        if valid:prices[code]=quotes[0]['values']['close']
        coverage.append({'code':code,'valid':valid})
    if len(prices)!=len(universe):errors.append('incomplete_reference_quotes')
    for h in pack.holdings or []:
        if h.shares<=0:continue
        if h.code not in universe:errors.append('holding_outside_universe')
        if h.shares%1000:errors.append('official_odd_lot_holding')
        if pack.as_of_date and h.code in prices and h.close_price is not None and abs(h.close_price-decimal(prices[h.code]))>Decimal('.01'):
            errors.append('official_close_mismatch:'+h.code)
    risk=assess(store,sources,frozen,universe,RiskPolicy.model_validate(store.json(req['risk_policy_ref']))) if req.get('risk_policy_ref') else None
    if risk:
        errors.extend(risk['errors'])
        for h in pack.holdings or []:
            if h.shares>0 and h.code in risk['securities'] and not risk['securities'][h.code]['sell_allowed']:
                errors.append('held_security_requires_risk_resolution:'+h.code)
    candidates=[];exclusions=[]
    for code in sorted(prices):
        quote=next(r for r in by[('quotes',code)] if r['date']==req['as_of'])
        valuations=[r for r in by[('valuation',code)] if r['date']==req['as_of']]
        revenues=by[('revenue',code)]
        reason=None
        if req.get('decision_engine')=='llm_agent':
            if risk and not risk['securities'][code]['buy_allowed']:reason='trading_risk_new_buy_excluded'
            elif decimal(quote['values']['amount'])<policy.minimum_daily_amount or decimal(quote['values']['volume'])<=0:reason='low_liquidity'
            else:
                v=valuations[0] if len(valuations)==1 else None
                r=revenues[0] if len(revenues)==1 else None
                if r:
                    period=date.fromisoformat(r['date']);end=period.replace(day=calendar.monthrange(period.year,period.month)[1])
                    age=(instant(req['cutoff_at']).date()-period).days
                    if end>instant(req['cutoff_at']).date() or not 0<=age<=policy.maximum_revenue_age_days:r=None
                pe=v['values'].get('pe') if v else None
                industry=str(json.loads(r['raw_json']).get('產業別','')).strip() if r else ''
                candidates.append({'code':code,'industry':industry or 'unknown','close':prices[code],
                    'revenue_yoy_pct':r['values'].get('revenue_yoy_pct') if r else None,'pe':pe,
                    'earnings_yield':str(1/decimal(pe)) if pe is not None and decimal(pe)>0 else None,
                    'amount':quote['values']['amount'],'quote':quote,'valuation':v,'revenue':r})
            if reason:exclusions.append({'code':code,'reason':reason})
            continue
        if risk and not risk['securities'][code]['buy_allowed']:reason='trading_risk_new_buy_excluded'
        elif len(valuations)!=1 or len(revenues)!=1:reason='missing_or_conflicting_factors'
        else:
            v=valuations[0];r=revenues[0];pe=v['values'].get('pe');growth=r['values'].get('revenue_yoy_pct')
            industry=str(json.loads(r['raw_json']).get('產業別','')).strip()
            period=date.fromisoformat(r['date'])
            period_end=period.replace(day=calendar.monthrange(period.year,period.month)[1])
            age=(instant(req['cutoff_at']).date()-period).days
            if not industry:reason='missing_industry'
            elif period_end>instant(req['cutoff_at']).date() or not 0<=age<=policy.maximum_revenue_age_days:reason='revenue_period_stale_or_future'
            elif pe is None or decimal(pe)<=0:reason='no_positive_earnings_valuation'
            elif growth is None or decimal(growth)<=0:reason='nonpositive_or_missing_revenue_growth'
            elif decimal(quote['values']['amount'])<policy.minimum_daily_amount or decimal(quote['values']['volume'])<=0:reason='low_liquidity'
            else:candidates.append({'code':code,'industry':industry,'close':prices[code],
                'revenue_yoy_pct':growth,'pe':pe,'earnings_yield':str(1/decimal(pe)),
                'amount':quote['values']['amount'],'quote':quote,'valuation':v,'revenue':r})
        if reason:exclusions.append({'code':code,'reason':reason})
    return {'records':records,'prices':prices,'coverage':coverage,'candidates':candidates,'exclusions':exclusions,'issues':issues,'errors':sorted(set(errors)),'trading_risk':risk}

def compile_document(snapshot,ranked,targets,pack,policy,request,source_models,research=None):
    prices=snapshot['prices'];held={h.code:h.shares for h in pack.holdings if h.shares>0}
    involved=sorted(set(targets)|set(held));bycode={c['code']:c for c in ranked}
    quote_by={r['security_id']:r for r in snapshot['records'] if r['kind']=='quotes' and r['date']==request['as_of']}
    used={r['source_id'] for r in quote_by.values()}
    index_rows=sorted([r for r in snapshot['records'] if r['kind']=='market_index' and r['date']<=request['as_of']],key=lambda r:r['date'])
    market_index=next((r for r in reversed(index_rows) if r['date']==request['as_of']),None)
    if market_index:used.add(market_index['source_id'])
    used.update(r['source_id'] for r in snapshot['records'] if r['security_id'] in involved and r['kind'] in {'valuation','revenue'})
    if research:used.update(r['source_id'] for r in snapshot['records'] if r['kind'] in {'rss','announcements'})
    # An aggregate of all competition-universe quotes is a market-level fact,
    # explicitly labelled as a pool proxy, never called the TAIEX index.
    sources=[];smap={};models={s.id:s for s in source_models}
    for sid in sorted(used):
        rows=[r for r in snapshot['records'] if r['source_id']==sid]
        source=models[sid];index='S'+str(len(sources)+1);smap[sid]=index
        period=max(r['date'] or request['as_of'] for r in rows)
        if source.kind=='revenue':
            month=date.fromisoformat(period)
            period=month.replace(day=calendar.monthrange(month.year,month.month)[1]).isoformat()
        sources.append({'source_id':index,'authority':'twse' if source.provider=='TWSE' else 'tpex',
            'url':source.url,'name':source.id+' '+source.kind,'content_as_of':period+'T13:30:00+08:00',
            'fetched_at':max(rows,key=lambda r:instant(r['fetched_at']))['fetched_at']})
        if source.kind in {'rss','announcements'}:
            sources[-1]['authority']='media' if source.provider=='CNA' else source.provider.lower()
            sources[-1]['content_as_of']=max((r['published_at'] or r['available_at'] for r in rows),key=instant)
    if research:
        selected_codes=set(targets)|set(held)
        evidence_ids={eid for c in ranked if c['code'] in selected_codes for ids in c.get('research_evidence',{}).values() for eid in ids}
        for eid in sorted(evidence_ids):
            for row in research['evidence'][eid].get('rows',[]):
                sid=row['source_id']
                if sid in smap:continue
                meta=research['data_sources'][sid];smap[sid]='S'+str(len(sources)+1)
                sources.append({'source_id':smap[sid],**meta})
    risk=snapshot.get('trading_risk')
    if risk:
        for sid,evidence in sorted(risk['feed_refs'].items()):
            smap[sid]='S'+str(len(sources)+1)
            sources.append({'source_id':smap[sid],'authority':evidence['provider'].lower(),
                'url':evidence['url'],'name':sid+' trading_risk_snapshot',
                'content_as_of':evidence['fetched_at'],'fetched_at':evidence['fetched_at']})
    changes=[decimal(r['values']['close'])/decimal(r['values']['open'])-1 for r in quote_by.values()]
    up=sum(v>0 for v in changes);down=sum(v<0 for v in changes)
    observations=[{'obs_id':'O1','source_ref':sorted({smap[r['source_id']] for r in quote_by.values()}),
       'topic':'tw_market','statement':f'競賽股票池共{len(changes)}檔，收盤較開盤上漲{up}檔、下跌{down}檔；此為股票池日內廣度，不是大盤指數或隔日預測。',
       'values':{'universe_count':len(changes),'close_above_open_count':up,'close_below_open_count':down,
                 'equal_weight_intraday_return':float(sum(changes)/len(changes))}}]
    if market_index:
        observations[0]['source_ref'].append(smap[market_index['source_id']])
        observations[0]['statement']+=f' 加權指數參考日收盤為{market_index["values"]["close"]}點。'
        observations[0]['values']['taiex_close_points']=float(decimal(market_index['values']['close']))
        prior=[r for r in index_rows if r['date']<request['as_of']]
        if prior:
            observations[0]['values']['taiex_close_return']=float(decimal(market_index['values']['close'])/decimal(prior[-1]['values']['close'])-1)
    lineage={'O1':{'derivation':'count/mean(close/open-1) over fixed competition universe; optional official TAIEX close',
        'rows':[{'source_id':r['source_id'],'raw_ref':r['raw_ref'],'raw_row':r['raw_row']} for r in quote_by.values()]}}
    if market_index:
        lineage['O1']['rows'].append({'source_id':market_index['source_id'],'raw_ref':market_index['raw_ref'],'raw_row':market_index['raw_row']})
    risk_observations=defaultdict(list)
    if risk:
        for provider in sorted({e['provider'].upper() for e in risk['feed_refs'].values()}):
            ids=sorted(sid for sid,e in risk['feed_refs'].items() if e['provider'].upper()==provider)
            members=[code for code,q in quote_by.items() if models[q['source_id']].provider.upper()==provider]
            for start in range(0,len(ids),10):
                group=ids[start:start+10];oid='O'+str(len(observations)+1)
                risk_observations[provider].append(oid)
                observations.append({'obs_id':oid,'source_ref':[smap[sid] for sid in group],
                    'topic':'trading_risk_snapshot',
                    'statement':'已依本組封存官方事件快照核對本市場競賽股票；下列檔數按本組來源去重，各來源組之間不可直接相加。資料範圍仍未完整涵蓋合併與企業分割，後續公告也尚未知。',
                    'values':{'cited_source_count':len(group),'market_universe_count':len(members),
                        'new_buy_blocked_count':sum(any(f['source_id'] in group and f['blocks_new_buys'] for f in risk['securities'][c]['flags']) for c in members),
                        'sell_blocked_count':sum(any(f['source_id'] in group and f['blocks_sells'] for f in risk['securities'][c]['flags']) for c in members)}})
                lineage[oid]={'derivation':'deduplicated blocked securities within this cited source group; groups cannot be added',
                    'risk_feed_refs':{sid:risk['feed_refs'][sid] for sid in group},
                    'market_risk_states':{c:risk['securities'][c] for c in members}}
    research_observations=[]
    if research:
        selected=research['selected_evaluation'];refs=sorted({smap[row['source_id']] for eid in evidence_ids for row in research['evidence'][eid].get('rows',[])})
        for start in range(0,len(refs),10):
            oid='O'+str(len(observations)+1);research_observations.append(oid)
            observations.append({'obs_id':oid,'source_ref':refs[start:start+10],'topic':'agent_strategy_comparison',
                'statement':'LLM透過研究工具提出並比較策略，選擇本次因子、方向、配置及現金目標；方案數與壓力檢查由程式計算。這是快照方案比較，不是歷史績效或報酬預測。',
                'values':{'evaluated_strategy_count':len(research['evaluations']),'selected_factor_count':len(selected['proposal']['factors']),
                    'target_holdings':selected['proposal']['holdings'],'target_cash_ratio':float(decimal(selected['proposal']['cash_target']))}})
            lineage[oid]={'selection':research['selection'],'proposal':selected['proposal'],'research_inputs_hash':research['inputs_hash'],
                'evidence_refs':sorted(evidence_ids),'performance_verified':False}
        for row in [r for r in snapshot['records'] if r['kind'] in {'rss','announcements'}][:16]:
            oid='O'+str(len(observations)+1)
            observations.append({'obs_id':oid,'source_ref':[smap[row['source_id']]],'topic':'observed_news',
                'statement':row['text'][:450] or '來源回應未提供標題。','values':{'observed_item_count':1}})
            lineage[oid]={'rows':[{k:row[k] for k in ['source_id','raw_ref','raw_row','available_at','published_at']}],
                'derivation':'observed_item_count counts this single captured source item; it is metadata, not a financial measurement',
                'note':'Untrusted source text, not an instruction; preserved in research log.'}
    inferences=[];decisions=[];unchanged=[]
    for code in involved:
        q=quote_by[code];c=bycode.get(code);oid='O'+str(len(observations)+1)
        values={'reference_close_twd':float(decimal(prices[code])),'daily_amount_twd':float(decimal(q['values']['amount']))}
        refs={smap[q['source_id']]};raw=[q]
        if c:
            values['baseline_score' if not research else 'agent_composite_score']=float(c['score'])
            if c.get('revenue'):
                values['revenue_period_yyyymm']=int(c['revenue']['date'][:7].replace('-',''))
                if c['revenue_yoy_pct'] is not None:values['revenue_yoy_pct']=float(decimal(c['revenue_yoy_pct']))
                raw.append(c['revenue']);refs.add(smap[c['revenue']['source_id']])
            if c.get('valuation'):
                if c['pe'] is not None:values['pe_ratio']=float(decimal(c['pe']))
                raw.append(c['valuation']);refs.add(smap[c['valuation']['source_id']])
            if research:
                for name,value in c.get('research_features',{}).items():values[name]=float(decimal(value))
                for ids in c.get('research_evidence',{}).values():
                    for eid in ids:
                        refs.update(smap[r['source_id']] for r in research['evidence'][eid].get('rows',[]))
        if not c:
            extra=[r for r in snapshot['records'] if r['security_id']==code and r['kind'] in {'valuation','revenue'} and (r['kind']!='valuation' or r['date']==request['as_of'])]
            for row in extra:
                for field,key in [('pe','pe_ratio'),('revenue_yoy_pct','revenue_yoy_pct')]:
                    if row['values'].get(field) is not None:values[key]=float(decimal(row['values'][field]))
                refs.add(smap[row['source_id']]);raw.append(row)
        statement=f'{code} 的參考收盤價、當日成交金額'
        statement+='及可取得的營收／估值欄位見數值欄。'
        if c:statement+='規則百分位加權分數為確定性計算，不是預測報酬。'
        else:
            reason=next((e['reason'] for e in snapshot['exclusions'] if e['code']==code),'not_eligible')
            statement+='候選資料／條件檢查：'+reason+'。'
        if risk:
            statement+='已依封存的交易事件快照執行內部篩選；快照時間不等於後續公告已完整，仍須於收件窗重抓。'
        observations.append({'obs_id':oid,'source_ref':sorted(refs),'topic':'company_facts','statement':statement,'values':values})
        lineage[oid]={'code':code,'rows':[{'source_id':r['source_id'],'raw_ref':r['raw_ref'],'raw_row':r['raw_row'],'date':r['date'],'available_at':r['available_at']} for r in raw],
            'score_formula':f'growth_percentile*{policy.growth_score_weight} + earnings_yield_percentile*{policy.value_score_weight} + amount_percentile*{policy.liquidity_score_weight}' if c else None}
        if risk:
            lineage[oid]['risk_evidence']=risk['securities'][code]
            lineage[oid]['risk_feed_refs']={sid:e for sid,e in risk['feed_refs'].items() if e['provider'].upper()==models[q['source_id']].provider.upper()}
        if research:
            lineage[oid]['score_formula']=research['selected_evaluation']['proposal']['factors']
            lineage[oid]['feature_evidence']=c.get('research_evidence',{}) if c else {}
        iid='I'+str(len(inferences)+1)
        selected=code in targets
        logic=(f'依{policy.version}對正營收成長、正本益比與流動性作百分位加權排序，並限制產業集中及整張預算；'
               +('本檔進入分散候選，依固定等權政策換算目標部位。' if selected else '本檔未進入本次完整資料且分散限制下的候選，依規則退出可交易部位，不代表預測一定下跌。'))
        if research:
            logic='LLM自主研究比較後選定「'+research['selected_evaluation']['proposal']['name']+'」，以其因子、篩選與配置方案計算排名、產業分散與整張部位；'+('本檔進入該方案配置。' if selected else '本檔未進入本次選定方案，依該方案調整部位，不代表預測必然下跌。')
        risk_refs=risk_observations.get(models[q['source_id']].provider.upper(),[]) if risk else []
        inferences.append({'inf_id':iid,'premise_refs':[oid,'O1',*risk_refs,*research_observations],'logic':logic,
          'counter_evidence':'單月成長、本益比與單日流動性無法驗證完整品質或長期趨勢；未完成樣本外績效驗證。'})
        old=held.get(code,0);weight=targets.get(code,0);new=target_shares(weight,pack.account.nav_tradable,prices[code])
        if new==old:
            unchanged.append({'ticker':code,'reason_refs':[iid],'reason':'公式換算後股數與官方庫存相同，保留可交易部位。'})
        else:
            action='BUY' if old==0 else 'SELL_ALL' if new==0 else 'ADD' if new>old else 'TRIM'
            decisions.append({'decision_id':'D'+str(len(decisions)+1),'ticker':code,'action':action,
                              'target_weight':weight,'inference_refs':[iid]})
    orders=compile_orders(decisions,pack,prices)
    projected=estimate(pack,orders,prices,policy)
    net=projected['net_flow'];intent='hold' if abs(net)<=pack.account.nav_tradable*Decimal('.02') else 'increase' if net>0 else 'reduce'
    plan={'schema_version':'4.3','doc_type':'D-Plan','team_id':pack.team_id,'trade_date':pack.trade_date.isoformat(),
        'sources':sources,'observations':observations,'market_view':{'basis_refs':['O1'],
          'logic':'官方指數與股票池日內廣度按實際可用來源作市場背景，單日證據不足以判斷下一交易日方向，因此採中性情境；依正營收成長與估值規則建立分散部位，曝險意圖與現金區間由實際委託換算核對。',
          'regime':'neutral','stance':'neutral','posture':{'net_exposure_intent':intent,'target_cash_pct_range':[float(v) for v in policy.cash_band]},
          'counter_evidence':'缺少完整歷史、隔夜市場與風險事件驗證；市場可能在參考收盤後出現跳空或相關性改變。'},
        'inferences':inferences,'decisions':decisions,'no_trade_decisions':unchanged,'orders':orders,
        'agent_metadata':{'model_provider':'other','model_version':policy.version+'-deterministic-no-llm',
            'run_started_at':now(),'run_completed_at':now(),'code_version':'sha256:'+digest(encoded({k:request.get(k) for k in ['code_hash','policy_ref','schema_ref','session_ref','universe_hash','registry_hash','risk_policy_ref','llm_ref','benchmark_universe_ref','benchmark_refs']}))[:48]}}
    if research:
        plan['market_view']['logic']='市場情境以實際可得的指數及股票池廣度作背景；LLM研究、比較後選擇本次策略，資金配置及曝險意圖由該方案與官方股數公式核對。'
        plan['agent_metadata']['code_version']='sha256:'+digest(encoded({k:request.get(k) for k in request if k not in {'run_id'}}))[:48]
    # Funding is a numerical declaration. Only add it when omitting all sells
    # genuinely pushes cash below the declared lower bound.
    buys=[d['decision_id'] for d in decisions if d['action'] in {'BUY','ADD'}]
    sells=[d for d in decisions if d['action'] in {'TRIM','SELL_ALL'}]
    if buys and sells and estimate(pack,[o for o in orders if o['side']=='BUY'],prices,policy)['cash_ratio_previous_nav']<policy.cash_band[0]:
        for d in sells:
            d['funding_for']=buys[:5]
            inferences[int(d['inference_refs'][0][1:])-1]['logic']+=' 不執行調度賣出會低於現金區間下限；讓位順序依同一完整候選及分散規則決定。'
    return plan,lineage,projected

def graph_for(store,request,sources,universe,frozen,pack,policy,schema,checkpointer,interrupt_before=None,model=None):
    req=request.model_dump(mode='json');folder=store.root/'candidates'/request.run_id
    def research_for(state):return store.json(state['agent_research']) if state.get('agent_research') else None
    def effective_policy(state):
        research=research_for(state)
        return Policy.model_validate(research['selected_evaluation']['policy']) if research and research['status']=='SELECTED' else policy
    def prepare_node(state):
        snapshot=prepare(store,sources,universe,frozen,pack,policy)
        return {'snapshot':store.put_json(snapshot),'errors':snapshot['errors']}
    def ranking_node(state):
        if req.get('decision_engine')=='llm_agent':
            from .strategy_agent import research_portfolio
            from .llm import ModelConfig,OllamaModel
            if not req.get('llm_ref') or not req.get('agent_settings_ref'):return {'errors':['agent_requires_model_and_settings']}
            config=ModelConfig.model_validate(store.json(req['llm_ref']))
            extra=None
            if req.get('research_data_ref'):
                from .agent_data import validate_bundle
                extra=validate_bundle(store,store.json(req['research_data_ref']),req)
            research=research_portfolio(store,folder,req,store.json(state['snapshot']),pack,policy,store.json(req['agent_settings_ref']),config,model or OllamaModel(config),extra)
            ref=store.put_json(research)
            if research['status']!='SELECTED':return {'agent_research':ref,'errors':research['errors']}
            return {'agent_research':ref,'features':store.put_json(research['selected_evaluation']['ranking'])}
        snap=store.json(state['snapshot']);ranked=rank_candidates(snap['candidates'],policy)
        return {'features':store.put_json(jsonable(ranked))}
    def allocate_node(state):
        research=research_for(state)
        if research:return {'allocation':store.put_json(research['selected_evaluation']['targets'])}
        ranked=store.json(state['features'])
        try:targets=allocate(ranked,pack,policy)
        except ValueError as e:return {'errors':[str(e)]}
        return {'allocation':store.put_json(targets)}
    def compile_node(state):
        cached=folder/'compiled.json'
        if cached.exists():bundle=json.loads(cached.read_bytes())
        else:
            ranked=store.json(state['features'])
            for c in ranked:c['score']=decimal(c['score'])
            try:
                plan,lineage,projected=compile_document(store.json(state['snapshot']),ranked,store.json(state['allocation']),pack,effective_policy(state),req,sources,research_for(state))
                bundle={'plan':plan,'lineage':lineage,'projected':jsonable(projected),'errors':[]}
            except (ValueError,KeyError) as e:bundle={'errors':[str(e)]}
            immutable(cached,encoded(bundle))
        return {'plan':store.put_json(bundle),'errors':bundle['errors']}
    def validate_node(state):
        policy=effective_policy(state)
        bundle=store.json(state['plan']);plan=bundle['plan'];snap=store.json(state['snapshot'])
        expected_ranked=store.json(state['features'])
        for row in expected_ranked:row['score']=decimal(row['score'])
        research=research_for(state)
        if research:
            from .research_tools import ResearchWorkspace,AgentSettings
            extra=None
            if req.get('research_data_ref'):
                from .agent_data import validate_bundle
                extra=validate_bundle(store,store.json(req['research_data_ref']),req)
            base_policy=Policy.model_validate(store.json(req['policy_ref']))
            workspace=ResearchWorkspace(snap,pack,base_policy,AgentSettings.model_validate(store.json(req['agent_settings_ref'])),extra)
            recomputed=jsonable(workspace.evaluate(research['selected_evaluation']['proposal']))
            if 'cost_twd' in recomputed:recomputed['cost_fraction_nav']=str(decimal(recomputed['cost_twd'])/pack.account.nav_tradable)
            if recomputed!=research['selected_evaluation']:raise ValueError('agent_selected_evaluation_mismatch')
            if jsonable(expected_ranked)!=recomputed['ranking'] or store.json(state['allocation'])!=recomputed['targets']:raise ValueError('agent_selection_not_applied')
        expected_plan,_,_=compile_document(snap,expected_ranked,store.json(state['allocation']),pack,policy,req,sources,research)
        if req.get('llm_ref'):
            from .llm import apply_review
            expected_plan=apply_review(expected_plan,store.json(state['llm_review']))
        errors=validate_plan(plan,schema,pack,snap['prices'],universe,req['cutoff_at'],policy,expected_plan['observations'],expected_plan['sources'])
        if snap.get('trading_risk'):errors+=order_errors(snap['trading_risk'],plan['orders'])
        for section in ['inferences','decisions','no_trade_decisions','orders','market_view']:
            if plan[section]!=expected_plan[section]:errors.append('compiled_policy_mismatch:'+section)
        industries={c['code']:c['industry'] for c in snap['candidates']}
        projected=estimate(pack,plan['orders'],snap['prices'],policy)
        if bundle['projected']!=jsonable(projected):errors.append('projection_lineage_mismatch')
        if all(c in industries for c in projected['positions']):errors+=breaches(projected,policy,industries)
        scenarios=[]
        for execution in [1-policy.price_stress_fraction,Decimal(1),1+policy.price_stress_fraction]:
            for close in [1-policy.price_stress_fraction,Decimal(1),1+policy.price_stress_fraction]:
                result=estimate(pack,plan['orders'],snap['prices'],policy,execution,close)
                failures=breaches(result,policy,industries if all(c in industries for c in result['positions']) else None)
                scenarios.append({'execution_factor':str(execution),'close_factor':str(close),'errors':failures,'cash_ratio':str(result['cash_ratio'])})
        if any(s['errors'] for s in scenarios):errors.append('price_stress_failed')
        blockers=['official_upload_and_submission_not_verified','fee_rounding_not_verified','strategy_pdf_not_submitted','no_out_of_sample_performance_validation']
        from .benchmarks import evaluate
        expected=store.json(req['benchmark_universe_ref']) if req.get('benchmark_universe_ref') else []
        active=evaluate(store,req.get('benchmark_refs',[]),projected['weights'],expected,req['as_of'],req['cutoff_at'],policy.active_share_buffer)
        if not expected:active['release_blockers'].append('active_share_30_etfs_not_verified')
        blockers+=active['release_blockers']
        blockers+=(snap['trading_risk']['release_blockers'] if snap.get('trading_risk') else ['trading_status_and_corporate_actions_not_verified'])
        if req['mode']=='fixture':blockers.append('fixture_input_not_for_submission')
        if not req.get('llm_ref'):blockers.append('llm_not_enabled')
        if not any(r['kind']=='market_index' and r['date']==req['as_of'] for r in snap['records']):blockers.append('market_background_pool_proxy_only')
        partial=[]
        for order in plan['orders']:
            result=estimate(pack,plan['orders'],snap['prices'],policy,exclude=order['ticker'])
            partial.append({'excluded_code':order['ticker'],'errors':breaches(result,policy),'holdings':len(result['positions']),'cash_ratio':str(result['cash_ratio'])})
        verdict={'schema_and_semantics_pass':not errors,'errors':sorted(set(errors)),
            'release_blockers':blockers,'official_server_validation':False,'submission_allowed':False,'scenarios':scenarios,'single_exclusion_scenarios':partial,
            'partial_execution_note':'Actual execution and excluded_codes must be reconciled from the next official DataPack; full fills are not guaranteed.'}
        return {'validation':store.put_json(verdict),'errors':verdict['errors'],'active_share':store.put_json(active)}
    def llm_node(state):
        if not req.get('llm_ref'):return {}
        from .llm import ModelConfig, OllamaModel, review_document, apply_review
        config=ModelConfig.model_validate(store.json(req['llm_ref']))
        bundle=store.json(state['plan'])
        try:
            cached=folder/'llm-review.json'
            if cached.exists():review=json.loads(cached.read_bytes())
            else:
                review=review_document(store,folder,bundle['plan'],config,model or OllamaModel(config))
                if state.get('agent_research'):
                    research=research_for(state);review['research_usage']=research['usage'];review['research_started_at']=research['started_at']
                immutable(cached,encoded(review))
            if review['config']!=config.model_dump():raise ValueError('review_model_config_mismatch')
            bundle['plan']=apply_review(bundle['plan'],review)
            return {'plan':store.put_json(bundle),'llm_review':store.put_json(review)}
        except ValueError as e:return {'errors':[str(e)]}
    def publish_node(state):
        errors=state.get('errors',[])
        verdict=store.json(state['validation']) if state.get('validation') else {'errors':errors,'schema_and_semantics_pass':False}
        status='BLOCKED_LOCAL_CHECKS' if errors else 'CANDIDATE_BLOCKED_EXTERNAL_CHECKS'
        outputs={'validation.json':encoded(verdict),'snapshot.json':store.read(state['snapshot'])}
        risk=store.json(state['snapshot']).get('trading_risk')
        if risk:
            outputs['trading-risk.json']=encoded(risk)
            outputs['trading-risk-policy.json']=store.read(req['risk_policy_ref'])
        if state.get('features'):outputs['ranking.json']=store.read(state['features'])
        if state.get('allocation'):outputs['targets.json']=store.read(state['allocation'])
        outputs['policy.json']=encoded(effective_policy(state).model_dump(mode='json'))
        if state.get('agent_research'):
            research=research_for(state);outputs['agent-research.json']=encoded(research)
            outputs['agent-call-evidence.json']=encoded([store.json(ref) for ref in research['call_refs']])
            lines=['# LLM自主策略比較','',f'研究狀態：{research["status"]}','', '這是資料快照、成本與情境比較；不是PIT策略績效回測。','']
            for pid,e in research['evaluations'].items():
                evaluation=store.json(e['ref']);p=evaluation['proposal']
                lines += ['## '+p['name'],'',p['hypothesis'],'',f'評估參照：{e["tool_id"]}；可投資檔數：{evaluation["eligible_count"]}；本地錯誤：'+(', '.join(evaluation['errors']) or '無'),'',
                    '因子組合：'+json.dumps(p['factors'],ensure_ascii=False),'','失效條件：'+p['failure_condition'],'']
            if research.get('selection'):
                lines+=['## 自主選擇','',research['selection']['reason'],'']
                lines += ['- '+c['proposal_id']+'：'+c['reason'] for c in research['selection']['comparisons']]
                lines+=['','## 資料及績效限制','']+['- '+x for x in research['selection']['limitations']]
            outputs['strategy-comparison.md']=('\n'.join(lines)+'\n').encode()
        if state.get('llm_review'):
            review=store.json(state['llm_review']);outputs['llm-review.json']=encoded(review)
            outputs['llm-call-evidence.json']=encoded([store.json(ref) for ref in review['call_refs']])
        if state.get('active_share'):outputs['active-share.json']=store.read(state['active_share'])
        if state.get('plan'):
            bundle=store.json(state['plan'])
            if 'plan' in bundle:
                name=f"D-Plan_{pack.team_id}_{pack.trade_date.isoformat()}.json" if not errors else 'rejected-plan.json'
                outputs[name]=encoded(bundle['plan']);outputs['lineage.json']=encoded(bundle['lineage']);outputs['projected-account.json']=encoded(bundle['projected'])
        lines=['# 自主決策與 D-Plan 本地驗收','',f'狀態：{status}',f'輸入類型：{req["mode"]}；行情基準：{req["as_of"]}；截止：{req["cutoff_at"]}',
            '',f'資料品質：{sum(x["valid"] for x in store.json(state["snapshot"])["coverage"])}/{len(universe)}檔有效行情。',
            '此版本候選尚有外部驗收阻礙，未由本程式上傳或送出；其他版本的試繳狀態另記。'+('策略由LLM主導研究、比較並選擇，詳見strategy-comparison.md；尚無績效優勢證據。' if state.get('agent_research') else '策略為營收成長／估值／流動性規則基線，尚無績效優勢證據。'),
            '市場判斷引用實際可用的官方指數與固定股票池廣度，兩者分開標記。'+('本地LLM已完成逐項研究推論與反證，股數／權重／硬限制由確定性程式驗證。' if state.get('llm_review') else '本次沒有通過LLM研究驗證。'),'', '## 本地錯誤']
        lines += ['- '+e for e in errors] or ['- 無本地阻擋錯誤。']
        if risk:
            lines+=['','## 交易事件風險關卡','',f'來源{len(risk["feeds"])}項；禁止新買{sum(not s["buy_allowed"] for s in risk["securities"].values())}檔；需先處理才能賣出{sum(not s["sell_allowed"] for s in risk["securities"].values())}檔。',
                '注意股票預設只註記；處置與變更交易的排除是內部政策，不宣稱官方禁止交易。除權息跨越行情基準時暫停使用未驗證的價格換算。詳見 trading-risk.json。',risk['scope_note']]
        if state.get('plan'):
            bundle=store.json(state['plan'])
            if 'projected' in bundle:
                projected=bundle['projected'];plan=bundle['plan']
                lines+=['','## 收盤價情境下的預估組合','',f'委託{len(plan["orders"])}筆；持股{len(projected["positions"])}檔；費稅後預估現金比{float(projected["cash_ratio"]):.4%}。',
                    '以下股數由Agent自主規則與官方公式產生；為參考收盤價情境，尚非實際成交與結算。','',
                    '| 代碼 | 名稱 | 目標股數 | 預估權重 |','|---|---|---|---|']
                for code,shares in sorted(projected['positions'].items()):
                    lines.append(f'| {code} | {universe[code]["name"]} | {shares} | {float(projected["weights"][code]):.4%} |')
                lines+=['','## 壓力測試','',f'價格情境{len(verdict.get("scenarios",[]))}組；另逐筆模擬單一股票被排除。',
                    '排除測試只揭露風險，不保證多檔排除或跳空時仍合規；最終依官方DataPack對帳。']
        lines += ['','## 尚待完成']+['- '+e for e in verdict.get('release_blockers',[])]
        outputs['report.md']=('\n'.join(lines)+'\n').encode()
        for name,body in outputs.items():immutable(folder/name,body)
        immutable(folder/'manifest.json',encoded({'request':req,'status':status,'artifacts':{n:digest(b) for n,b in outputs.items()}}))
        return {'status':status,'report':str(folder/'report.md')}
    graph=StateGraph(State)
    for name,fn in [('prepare',prepare_node),('rank',ranking_node),('allocate',allocate_node),('compile',compile_node),('llm_review',llm_node),('validate',validate_node),('publish',publish_node)]:graph.add_node(name,fn)
    graph.add_edge(START,'prepare')
    graph.add_conditional_edges('prepare',lambda s:'publish' if s['errors'] else 'rank')
    graph.add_conditional_edges('rank',lambda s:'publish' if s.get('errors') else 'allocate')
    graph.add_conditional_edges('allocate',lambda s:'publish' if s['errors'] else 'compile')
    graph.add_conditional_edges('compile',lambda s:'publish' if s['errors'] else 'llm_review')
    graph.add_conditional_edges('llm_review',lambda s:'publish' if s['errors'] else 'validate')
    graph.add_edge('validate','publish');graph.add_edge('publish',END)
    return graph.compile(checkpointer=checkpointer,interrupt_before=interrupt_before)

def generate_candidate(store,request,sources,universe,interrupt_before=None,model=None):
    if digest(encoded(universe))!=request.universe_hash or digest(encoded([s.model_dump() for s in sources]))!=request.registry_hash:
        raise ValueError('Universe or source registry hash mismatch')
    pack=load_datapack(store.read(request.datapack_ref),request.team_id,request.trade_date)
    policy=Policy.model_validate(store.json(request.policy_ref));schema=store.json(request.schema_ref)
    frozen=store.freeze(request,sources,namespace='candidates')
    folder=store.root/'candidates'/request.run_id
    with sqlite3.connect(store.root/'candidate-checkpoints.sqlite',check_same_thread=False) as conn:
        graph=graph_for(store,request,sources,universe,frozen,pack,policy,schema,SqliteSaver(conn),interrupt_before,model)
        config={'configurable':{'thread_id':request.run_id},'recursion_limit':20}
        previous=graph.get_state(config)
        if previous.values and not previous.next:
            manifest=json.loads((folder/'manifest.json').read_bytes())
            for name,sha in manifest['artifacts'].items():
                if digest((folder/name).read_bytes())!=sha:raise ValueError('Candidate artifact hash mismatch')
            return dict(previous.values)
        return graph.invoke(None if previous.values else {},config)
