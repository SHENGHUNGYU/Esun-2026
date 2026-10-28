"""Typed factor research: evidence inventory, strategy evaluation and constrained allocation.

The LLM chooses the hypothesis and policy. This module computes their consequences;
it never reports unobserved strategy returns or fills absent factors with zero.
"""
from collections import defaultdict
from decimal import Decimal,ROUND_FLOOR
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,model_validator,field_serializer
from .portfolio import Policy,decimal,target_shares,compile_orders,estimate,breaches
from .store import digest,encoded

class Strict(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)

class AgentSettings(Strict):
    version: str
    max_steps: int=Field(default=20,ge=8,le=40)
    minimum_compared_strategies: int=Field(default=2,ge=2,le=4)
    maximum_strategies: int=Field(default=6,ge=2,le=8)
    maximum_revisions: int=Field(default=2,ge=0,le=3)
    minimum_holdings: int=Field(default=20,ge=20,le=30)
    maximum_holdings: int=Field(default=30,ge=20,le=30)
    maximum_news_items: int=Field(default=16,ge=0,le=30)
    maximum_tool_rows: int=Field(default=12,ge=1,le=20)
    short_horizon_sessions: int=Field(default=10,ge=1,le=30)
    maximum_daily_turnover: Decimal=Field(default=Decimal('.20'),gt=0,le=2)
    maximum_daily_cost: Decimal=Field(default=Decimal('.0006'),gt=0,le=Decimal('.02'))
    maximum_replacements: int=Field(default=3,ge=0,le=10)
    retention_rank_buffer: int=Field(default=10,ge=0,le=50)
    minimum_rank_score_gap: Decimal=Field(default=Decimal('.15'),ge=0,le=1)
    weight_deadband: Decimal=Field(default=Decimal('.003'),ge=0,le=Decimal('.10'))
    minimum_trade_fraction: Decimal=Field(default=Decimal('.003'),ge=0,le=Decimal('.10'))

    @field_serializer('maximum_daily_turnover','maximum_daily_cost','minimum_rank_score_gap','weight_deadband','minimum_trade_fraction')
    def serialize_controls(self,value):return str(value)

    @model_validator(mode='after')
    def ranges(self):
        if self.minimum_holdings>self.maximum_holdings or self.minimum_compared_strategies>self.maximum_strategies:raise ValueError('invalid_agent_limits')
        return self

class Factor(Strict):
    feature: str=Field(pattern=r'^[a-z][a-z0-9_]{1,60}$')
    direction: Literal['higher','lower']='higher'
    transform: Literal['percentile','sector_percentile']='percentile'
    weight: Decimal=Field(gt=0,le=1)

class Screen(Strict):
    feature: str=Field(pattern=r'^[a-z][a-z0-9_]{1,60}$')
    operator: Literal['gt','ge','lt','le']
    value: Decimal=Field(ge=Decimal('-1e12'),le=Decimal('1e12'))

class StrategyProposal(Strict):
    proposal_id: str=Field(pattern=r'^[A-Za-z][A-Za-z0-9_-]{0,39}$')
    name: str=Field(min_length=2,max_length=70)
    hypothesis: str=Field(min_length=15,max_length=500)
    failure_condition: str=Field(min_length=10,max_length=350)
    mode: Literal['rebalance','full_rebalance','hold','risk_repair','previous']='rebalance'
    factors: list[Factor]=Field(min_length=0,max_length=8)
    screens: list[Screen]=Field(default_factory=list,max_length=8)
    holdings: int=Field(ge=20,le=30)
    cash_target: Decimal=Field(ge=Decimal('.05'),le=Decimal('.22'))
    weighting: Literal['equal','rank_tilt']='equal'

    @model_validator(mode='after')
    def coherent(self):
        if self.mode not in {'hold','risk_repair'} and sum((t.weight for t in self.factors),Decimal(0))!=1:raise ValueError('factor_weights_must_sum_to_one')
        if len({(f.feature,f.direction,f.transform) for f in self.factors})!=len(self.factors):raise ValueError('duplicate_factor_terms')
        return self

    def economic_hash(self):
        body=self.model_dump(mode='json',exclude={'proposal_id','name','hypothesis','failure_condition'})
        body['cash_target']=str(self.cash_target.normalize())
        for f in body['factors']:f['weight']=str(decimal(f['weight']).normalize())
        for f in body['screens']:f['value']=str(decimal(f['value']).normalize())
        body['factors']=sorted(body['factors'],key=lambda f:(f['feature'],f['direction'],f['transform']))
        body['screens']=sorted(body['screens'],key=lambda f:(f['feature'],f['operator'],f['value']))
        return digest(encoded(body))

FEATURES={
 'revenue_yoy_pct':('fundamental','percent','營收年增率；單月不等於盈利品質'),
 'revenue_mom_pct':('fundamental','percent','營收月增率；季節性未調整'),
 'earnings_yield':('fundamental','ratio','正本益比倒數；負值或缺值不可推造'),
 'pb_ratio':('fundamental','ratio','股價淨值比；跨產業不可直接解讀品質'),
 'dividend_yield_pct':('fundamental','percent','來源披露殖利率；不是未來保證股息'),
 'amount_twd':('technical','TWD','參考日成交金額；上市櫃口徑有別'),
 'intraday_return':('technical','ratio','收盤除開盤減一；不是隔日預測'),
 'range_pct':('technical','ratio','當日高低差除參考收盤'),
 'close_location':('technical','ratio','收盤在當日區間的位置；零振幅為缺值'),
 'momentum_5':('technical','ratio','完整五交易日窗口且不跨未驗證公司行動'),
 'momentum_20':('technical','ratio','完整二十交易日窗口且不跨未驗證公司行動'),
 'volatility_20':('technical','daily_return_std','完整二十期日報酬標準差；原始價風險限制'),
 'foreign_net_ratio':('flows','net_shares/volume_shares','外資淨買股數／同日成交股數；不是持有比'),
 'trust_net_ratio':('flows','net_shares/volume_shares','投信淨買股數／同日成交股數'),
 'dealer_net_ratio':('flows','net_shares/volume_shares','自營商淨買股數／同日成交股數')}

class ResearchWorkspace:
    def __init__(self,snapshot,pack,policy,settings,extra=None):
        self.snapshot=snapshot;self.pack=pack;self.policy=policy;self.settings=settings
        self.rows={};self.evidence={};self.news=[]
        by=defaultdict(list)
        for r in snapshot['records']:by[(r['security_id'],r['kind'])].append(r)
        for c in snapshot['candidates']:
            code=c['code'];q=c['quote'];v=c.get('valuation');rev=c.get('revenue')
            values={};evidence={}
            def add(name,value,raw):
                if value is None:return
                value=str(decimal(value));eid='E'+digest(encoded({'feature':name,'code':code,'value':value,'raw':raw}))[:18]
                values[name]=value;evidence[name]=[eid];self.evidence[eid]={'feature':name,'code':code,'value':value,'rows':raw}
            def refs(r):return [{k:r[k] for k in ['source_id','raw_ref','raw_row','date','available_at']}]
            if rev:
                for f in ['revenue_yoy_pct','revenue_mom_pct']:add(f,rev['values'].get(f),refs(rev))
            if v:
                pe=v['values'].get('pe')
                add('earnings_yield',1/decimal(pe) if pe is not None and decimal(pe)>0 else None,refs(v))
                add('pb_ratio',v['values'].get('pb'),refs(v));add('dividend_yield_pct',v['values'].get('yield_pct'),refs(v))
            op,hi,lo,cl=[decimal(q['values'][f]) for f in ['open','high','low','close']]
            add('amount_twd',q['values']['amount'],refs(q));add('intraday_return',cl/op-1,refs(q))
            add('range_pct',(hi-lo)/cl,refs(q));add('close_location',(cl-lo)/(hi-lo) if hi>lo else None,refs(q))
            self.rows[code]={'code':code,'industry':c['industry'],'close':c['close'],'values':values,'evidence':evidence,'candidate':c}
        # Additional computed factors must already be verified against raw inputs by
        # the input builder. Their whole bundle is frozen by the caller, never model-written.
        if extra:
            for item in extra.get('cells',[]):
                code=item['code'];name=item['feature']
                if code not in self.rows or name not in FEATURES:continue
                if name in self.rows[code]['values']:raise ValueError('research_factor_override_forbidden')
                eid=item['evidence_id'];self.evidence[eid]=item
                self.rows[code]['values'][name]=str(decimal(item['value']));self.rows[code]['evidence'][name]=[eid]
        for r in snapshot['records']:
            if r['kind'] in {'rss','announcements'}:
                eid='E'+digest(encoded(r))[:18];self.evidence[eid]=r
                self.news.append({'evidence_id':eid,'code':r['security_id'] or None,'text':r['text'][:450],
                    'published_at':r['published_at'],'available_at':r['available_at']})

    def catalog(self):
        result=[]
        for name,(category,unit,note) in FEATURES.items():
            values=[decimal(r['values'][name]) for r in self.rows.values() if name in r['values']]
            result.append({'feature':name,'category':category,'unit':unit,'coverage':len(values),'eligible_universe':len(self.rows),
                'minimum':str(min(values)) if values else None,'maximum':str(max(values)) if values else None,'limitation':note})
        return {'features':result,'news_items':len(self.news),'performance_validation':'No PIT strategy backtest; no Sharpe, win-rate or expected-return estimate is available.'}

    def inspect(self,features,codes=None,descending=True):
        if not features or len(features)>8 or any(f not in FEATURES for f in features):raise ValueError('unknown_or_excessive_features')
        if codes and (len(codes)>self.settings.maximum_tool_rows or any(c not in self.rows for c in codes)):raise ValueError('unknown_or_excessive_securities')
        rows=[r for c,r in self.rows.items() if not codes or c in codes]
        primary=features[0]
        rows.sort(key=lambda r:(primary not in r['values'],(-decimal(r['values'][primary]) if descending else decimal(r['values'][primary])) if primary in r['values'] else Decimal(0),r['code']))
        return {'rows':[{'code':r['code'],'industry':r['industry'],'values':{f:r['values'].get(f) for f in features},
            'evidence_refs':{f:r['evidence'].get(f,[]) for f in features}} for r in rows[:self.settings.maximum_tool_rows]],
            'missing_is_not_zero':True,'categories':sorted({FEATURES[f][0] for f in features})}

    def evaluate(self,proposal):
        spec=StrategyProposal.model_validate(proposal)
        names={f.feature for f in spec.factors}|{s.feature for s in spec.screens}
        if not names<=FEATURES.keys():raise ValueError('strategy_uses_unknown_feature')
        if not self.settings.minimum_holdings<=spec.holdings<=self.settings.maximum_holdings:raise ValueError('holdings_outside_agent_policy')
        policy=Policy.model_validate({**self.policy.model_dump(),'holdings':spec.holdings,'cash_target':spec.cash_target,'name':spec.name,'version':'agent-'+spec.proposal_id})
        rows=[r for r in self.rows.values() if all(f in r['values'] for f in names)]
        filtered=[]
        for r in rows:
            keep=True
            for f in spec.screens:
                v=decimal(r['values'][f.feature]);test={'gt':v>f.value,'ge':v>=f.value,'lt':v<f.value,'le':v<=f.value}[f.operator]
                keep=keep and test
            if keep:filtered.append(r)
        ranks={r['code']:Decimal(0) for r in filtered}
        for factor in spec.factors:
            sectors=defaultdict(list)
            for r in filtered:sectors[r['industry'] if factor.transform=='sector_percentile' else 'all'].append(r)
            for group in sectors.values():
                ties=defaultdict(list)
                for r in group:ties[decimal(r['values'][factor.feature])].append(r)
                offset=0
                for value in sorted(ties):
                    members=ties[value];rank=(Decimal(offset)+Decimal(len(members)-1)/2)/max(1,len(group)-1) if len(group)>1 else Decimal('.5')
                    for r in members:ranks[r['code']]+=factor.weight*(rank if factor.direction=='higher' else 1-rank)
                    offset+=len(members)
        ranked=[{**r['candidate'],'score':ranks[r['code']],
            'research_features':{f:r['values'][f] for f in sorted(names)},
            'research_evidence':{f:r['evidence'][f] for f in sorted(names)}} for r in filtered]
        ranked.sort(key=lambda c:(-c['score'],c['code']))
        result={'proposal':spec.model_dump(mode='json'),'economic_hash':spec.economic_hash(),'complete_feature_count':len(rows),'eligible_count':len(ranked),
            'errors':[],'performance_verified':False,'performance_note':'Snapshot policy comparison, not a PIT backtest or return forecast.'}
        try:
            from .turnover import held_positions,weights_for_positions,continuity_positions,repair_positions,check_positions,budget_errors
            held=held_positions(self.pack);settled=bool(held and self.pack.as_of_date)
            reasons={};suppressed=[];repair_exception=False
            if spec.mode=='hold':
                if not settled:raise ValueError('hold_requires_settled_positions')
                targets=weights_for_positions(held,self.pack,self.snapshot['prices'])
                reasons={c:'續抱官方可交易股數；本方案不交易、不產生費稅，仍須通過當日合規與情境檢查。' for c in held}
            elif spec.mode=='risk_repair':
                if not settled:raise ValueError('repair_requires_settled_positions')
                _,_,old_errors=check_positions(held,self.pack,self.snapshot,policy)
                positions,reasons=repair_positions(self.pack,self.snapshot,policy)
                repair_exception=bool(old_errors)
                targets=weights_for_positions(positions,self.pack,self.snapshot['prices'])
                for c in positions:reasons.setdefault(c,'原有部位沒有需要修正的限制，維持實際股數。')
            else:
                targets=allocate_research(ranked,self.pack,policy,spec.weighting)
                if settled and spec.mode in {'rebalance','previous'}:
                    positions,reasons,suppressed=continuity_positions(ranked,targets,self.pack,self.snapshot,policy,self.settings)
                    targets=weights_for_positions(positions,self.pack,self.snapshot['prices'])
                elif settled:
                    for c in set(targets)&set(held):
                        new=target_shares(targets[c],self.pack.account.nav_tradable,self.snapshot['prices'][c])
                        drift=abs(Decimal(new-held[c])*decimal(self.snapshot['prices'][c])/self.pack.account.nav_tradable)
                        if drift<=self.settings.weight_deadband or drift<self.settings.minimum_trade_fraction:
                            targets[c]=weights_for_positions({c:held[c]},self.pack,self.snapshot['prices'])[c]
                            suppressed.append({'code':c,'reason':'weight_deadband_or_minimum_trade'})
                    reasons={c:'本次完整配置候選；需與不交易及沿用昨日規則比較，並通過逐筆與整體成本預算。' for c in set(targets)|set(held)}
            result.update(continuity={'enabled':settled,'mode':spec.mode,'trade_reasons':reasons,'suppressed_adjustments':suppressed,
                'risk_repair_budget_exception':repair_exception,'limits':self.settings.model_dump(mode='json'),
                'note':'Internal initial controls, not validated return thresholds; factor scores are not returns.'})
            held={h.code:h.shares for h in self.pack.holdings if h.shares>0};decisions=[]
            for code in sorted(set(targets)|set(held)):
                old=held.get(code,0);new=target_shares(targets.get(code,0),self.pack.account.nav_tradable,self.snapshot['prices'][code])
                if old==new:continue
                decisions.append({'decision_id':'D'+str(len(decisions)+1),'ticker':code,'action':'BUY' if old==0 else 'SELL_ALL' if new==0 else 'ADD' if new>old else 'TRIM','target_weight':targets.get(code,0)})
            orders=compile_orders(decisions,self.pack,self.snapshot['prices']);projection=estimate(self.pack,orders,self.snapshot['prices'],policy)
            sectors={c['code']:c['industry'] for c in self.snapshot['candidates']}
            errors=breaches(projection,policy,sectors if all(c in sectors for c in projection['positions']) else None)
            from .risk import order_errors
            if self.snapshot.get('trading_risk'):errors+=order_errors(self.snapshot['trading_risk'],orders)
            stresses=[]
            for execution in [1-policy.price_stress_fraction,Decimal(1),1+policy.price_stress_fraction]:
                for close in [1-policy.price_stress_fraction,Decimal(1),1+policy.price_stress_fraction]:
                    state=estimate(self.pack,orders,self.snapshot['prices'],policy,execution,close)
                    bad=breaches(state,policy,sectors if all(c in sectors for c in state['positions']) else None)
                    stresses.append({'execution_factor':str(execution),'close_factor':str(close),'errors':bad})
            if any(s['errors'] for s in stresses):errors.append('price_stress_failed')
            if not policy.cash_band[0]<=projection['cash_ratio']<=policy.cash_band[1]:errors.append('cash_policy_band')
            if settled and not repair_exception:errors+=budget_errors(orders,projection,self.pack,self.snapshot['prices'],self.settings)
            if settled and spec.mode=='full_rebalance':
                replacements=sum(c not in held for c in projection['positions'])
                if replacements>self.settings.maximum_replacements:errors.append('replacement_budget_exceeded')
            if settled:
                for order in orders:
                    if order['ticker'] not in reasons:errors.append('trade_necessity_reason_missing')
            result.update(targets=targets,policy=policy.model_dump(mode='json'),orders=orders,
                holdings=len(projection['positions']),cash_ratio=str(projection['cash_ratio']),cost_twd=str(projection['fees']),
                turnover_notional_fraction=str(sum((decimal(self.snapshot['prices'][o['ticker']])*o['shares'] for o in orders),Decimal(0))/self.pack.account.nav_tradable),
                scenarios=stresses,errors=sorted(set(errors)))
        except ValueError as error:result['errors']=[str(error)]
        result['ranking']=ranked
        return result


def allocate_research(ranked,pack,policy,weighting):
    nominal=(1-policy.cash_target)/policy.holdings;selected=[];sectors=defaultdict(lambda:Decimal(0))
    for r in ranked:
        cap=policy.tsmc_cap if r['code']=='2330' else policy.single_cap
        if nominal>cap or sectors[r['industry']]+nominal>policy.industry_cap:continue
        if target_shares(nominal,pack.account.nav_tradable,r['close'])<1000:continue
        selected.append(r);sectors[r['industry']]+=nominal
        if len(selected)==policy.holdings:break
    if len(selected)!=policy.holdings:raise ValueError('insufficient_complete_diversified_candidates')
    budget=1-policy.cash_target
    raw={r['code']:Decimal(1) if weighting=='equal' else Decimal('.5')+r['score'] for r in selected}
    weights={c:Decimal(0) for c in raw};industries={r['code']:r['industry'] for r in selected}
    for _ in range(60):
        remaining=budget-sum(weights.values());active=[]
        for code in raw:
            cap=policy.tsmc_cap if code=='2330' else policy.single_cap
            sector=sum(w for c,w in weights.items() if industries[c]==industries[code])
            if weights[code]<cap and sector<policy.industry_cap:active.append(code)
        if remaining<Decimal('1e-15'):break
        if not active:raise ValueError('unable_to_allocate_with_caps')
        denominator=sum(raw[c] for c in active);increments={c:min(remaining*raw[c]/denominator,(policy.tsmc_cap if c=='2330' else policy.single_cap)-weights[c]) for c in active}
        for industry in {industries[c] for c in active}:
            group=[c for c in active if industries[c]==industry];capacity=policy.industry_cap-sum(w for c,w in weights.items() if industries[c]==industry)
            proposed=sum(increments[c] for c in group)
            if proposed>capacity:
                for c in group:increments[c]*=capacity/proposed
        for code,w in increments.items():weights[code]+=w
    if budget-sum(weights.values())>Decimal('1e-10'):raise ValueError('allocation_did_not_converge')
    return {c:float(w.quantize(Decimal('.000000000001'),rounding=ROUND_FLOOR)) for c,w in weights.items()}
