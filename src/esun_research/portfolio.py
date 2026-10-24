"""Deterministic research baseline and exact competition order arithmetic."""
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_FLOOR
from pydantic import BaseModel, ConfigDict, Field, model_validator

D=Decimal
LOT=1000

def decimal(v):
    if isinstance(v,bool):raise ValueError('Boolean is not a financial number')
    n=D(str(v))
    if not n.is_finite():raise ValueError('Nonfinite financial number')
    return n

class Policy(BaseModel):
    model_config=ConfigDict(extra='forbid',frozen=True,allow_inf_nan=False)
    name: str
    version: str
    holdings: int=Field(ge=20,le=30)
    cash_target: Decimal=Field(gt=0,lt=D('.25'))
    cash_band: list[Decimal]=Field(min_length=2,max_length=2)
    single_cap: Decimal=Field(gt=0,le=D('.10'))
    tsmc_cap: Decimal=Field(gt=0,le=D('.25'))
    industry_cap: Decimal=Field(gt=0,le=1)
    minimum_daily_amount: Decimal=Field(ge=0)
    maximum_revenue_age_days: int=Field(ge=1,le=366)
    growth_score_weight: Decimal=Field(ge=0,le=1)
    value_score_weight: Decimal=Field(ge=0,le=1)
    liquidity_score_weight: Decimal=Field(ge=0,le=1)
    buy_fee: Decimal=Field(ge=0)
    sell_fee_tax: Decimal=Field(ge=0)
    price_stress_fraction: Decimal=Field(gt=0,lt=1)
    active_share_buffer: Decimal=Field(ge=D('.15'),le=1)

    @model_validator(mode='after')
    def bounds(self):
        lo,hi=self.cash_band
        if not 0<lo<=self.cash_target<=hi<D('.25'):raise ValueError('Invalid cash band')
        if self.growth_score_weight+self.value_score_weight+self.liquidity_score_weight!=1:
            raise ValueError('Score weights must sum to one')
        if self.buy_fee!=D('.001425') or self.sell_fee_tax!=D('.004425'):
            raise ValueError('Policy fees must match competition rates')
        return self

def target_shares(weight,nav,price):
    weight,nav,price=map(decimal,[weight,nav,price])
    if price<=0 or nav<=0 or weight<0:raise ValueError('Invalid order inputs')
    return int((weight*nav/price/LOT).to_integral_value(rounding=ROUND_FLOOR))*LOT

def compile_orders(decisions,pack,prices):
    if pack.decision_gate().startswith('BLOCKED'):raise ValueError(pack.decision_gate())
    held={h.code:h.shares for h in pack.holdings if h.shares>0};orders=[];seen=set()
    for d in decisions:
        code=d['ticker']
        if code in seen:raise ValueError('Duplicate decision ticker')
        seen.add(code);old=held.get(code,0)
        new=target_shares(d['target_weight'],pack.account.nav_tradable,prices[code])
        delta=new-old
        action='BUY' if old==0 and new>0 else 'SELL_ALL' if old>0 and new==0 else 'ADD' if delta>0 else 'TRIM'
        if delta==0 or d['action']!=action:raise ValueError('Decision action or zero delta inconsistent')
        if abs(delta)%LOT:raise ValueError('Odd-lot order requires official exception policy')
        if delta<0 and -delta>old:raise ValueError('Oversell')
        orders.append({'ticker':code,'side':'BUY' if delta>0 else 'SELL','shares':abs(delta),'decision_ref':d['decision_id']})
    return orders

def estimate(pack,orders,prices,policy,execution_factor=D(1),close_factor=D(1),exclude=None):
    cash=pack.account.cash;positions={h.code:h.shares for h in pack.holdings if h.shares>0}
    net=D(0);fees=D(0)
    for order in orders:
        code=order['ticker']
        if code==exclude:continue
        shares=order['shares'];notional=decimal(prices[code])*shares*execution_factor
        direction=1 if order['side']=='BUY' else -1
        fee=notional*(policy.buy_fee if direction==1 else policy.sell_fee_tax)
        cash-=direction*notional+fee;fees+=fee
        net+=direction*decimal(prices[code])*shares
        positions[code]=positions.get(code,0)+direction*shares
        if positions[code]<0:raise ValueError('Oversell in simulation')
    positions={c:n for c,n in positions.items() if n>0}
    values={c:decimal(prices[c])*n*close_factor for c,n in positions.items()}
    nav=cash+sum(values.values(),D(0))
    if nav<=0:raise ValueError('Nonpositive projected NAV')
    return {'cash':cash,'nav':nav,'fees':fees,'net_flow':net,'positions':positions,
        'weights':{c:v/nav for c,v in values.items()},'cash_ratio':cash/nav,
        'cash_ratio_previous_nav':cash/pack.account.nav_tradable}

def breaches(state,policy,industries=None):
    errors=[]
    if not 20<=len(state['positions'])<=30:errors.append('holdings_count')
    if state['cash']<0 or not 0<=state['cash_ratio']<D('.25'):errors.append('cash_ratio')
    for code,w in state['weights'].items():
        if w>(policy.tsmc_cap if code=='2330' else policy.single_cap):errors.append('weight:'+code)
    if industries:
        weights=defaultdict(lambda:D(0))
        for code,w in state['weights'].items():weights[industries[code]]+=w
        for sector,w in weights.items():
            if w>policy.industry_cap:errors.append('industry:'+sector)
    return errors

def rank_candidates(candidates,policy):
    """Average percentile ranks; ties never depend on input row order."""
    candidates=[dict(c) for c in candidates];n=len(candidates)
    for field in ['revenue_yoy_pct','earnings_yield','amount']:
        groups=defaultdict(list)
        for c in candidates:groups[decimal(c[field])].append(c)
        offset=0
        for value in sorted(groups):
            group=groups[value]
            rank=(D(offset)+D(len(group)-1)/2)/max(1,n-1) if n>1 else D('.5')
            for c in group:c[field+'_rank']=rank
            offset+=len(group)
    for c in candidates:
        c['score']=c['revenue_yoy_pct_rank']*policy.growth_score_weight+c['earnings_yield_rank']*policy.value_score_weight+c['amount_rank']*policy.liquidity_score_weight
    return sorted(candidates,key=lambda c:(-c['score'],c['code']))

def allocate(candidates,pack,policy):
    nominal=((1-policy.cash_target)/policy.holdings).quantize(D('.000000000001'),rounding=ROUND_FLOOR)
    # Canonical JSON number is also the exact input to the order compiler.
    nominal=decimal(float(nominal))
    chosen=[];sector=defaultdict(lambda:D(0))
    for c in candidates:
        cap=policy.tsmc_cap if c['code']=='2330' else policy.single_cap
        if nominal>cap or sector[c['industry']]+nominal>policy.industry_cap:continue
        if target_shares(nominal,pack.account.nav_tradable,c['close'])<LOT:continue
        chosen.append(c);sector[c['industry']]+=nominal
        if len(chosen)==policy.holdings:break
    if len(chosen)!=policy.holdings:raise ValueError('Insufficient eligible diversified round-lot candidates')
    return {c['code']:float(nominal) for c in chosen}
