"""Replayable moving-average cost ledger; intentions never become confirmed fills."""
import json
from decimal import Decimal
from .store import encoded, digest, immutable
from .contracts import now

D=Decimal
FEE=D('0.001425'); TAX=D('0.003')

def amount(v):
    x=D(str(v))
    if not x.is_finite() or x<0:raise ValueError('金額必須為非負有限數字')
    return x


def apply(position,event):
    """Gross and explicit fees stay separate; partial sales release average cost."""
    p=dict(position);kind=event['kind'];n=event.get('shares',0)
    if type(n) is not int or n<0:raise ValueError('股數必須為非負整數')
    gross=amount(event.get('gross_twd','0'));fee=amount(event.get('fee_twd','0'));tax=amount(event.get('tax_twd','0'))
    if kind=='BUY':
        if n<=0 or gross<=0 or tax:raise ValueError('無效買入事件')
        if p['cost'] is not None:p['cost']+=gross+fee
        p['shares']+=n
    elif kind=='SELL':
        if not 0<n<=p['shares'] or gross<=0:raise ValueError('賣出股數超過庫存或金額無效')
        if p['cost'] is not None:
            released=p['cost']*n/p['shares'];p['cost']-=released
            if p['realized'] is not None:p['realized']+=gross-fee-tax-released
        else:p['realized']=None
        p['shares']-=n
    elif kind=='DIVIDEND':
        if n or fee or tax:raise ValueError('股息事件只接受已入帳淨現金')
        if p['income'] is not None:p['income']+=gross
    elif kind=='SHARE_ADJUSTMENT':
        # Shares become tradable only on the evidenced account transition;
        # receivable shares are not silently promoted into tradable holdings.
        if n<=0 or gross or fee or tax:raise ValueError('股數調整需填新增可交易股數，成本分攤另核對')
        p['shares']+=n
    else:raise ValueError('未知交易事件')
    p['fees']+=fee+tax
    return p


def import_events(store,snapshot_id,body,proof):
    from .holding_ledger import settlements
    rows=settlements(store);current=next(((e,p) for e,p in rows if e['id']==snapshot_id),None)
    if not current or not current[1].account or not current[1].as_of_date:raise ValueError('需要有效結算快照')
    data=json.loads(body)
    if not isinstance(data,dict) or set(data)!={'team_id','as_of_date','previous_snapshot_id','events','authority'}:raise ValueError('交易事件欄位不符')
    e,p=current
    if data['team_id']!=p.team_id or data['as_of_date']!=str(p.as_of_date):raise ValueError('交易事件隊伍或日期不符')
    prior=next(((a,b) for a,b in rows if a['id']==data['previous_snapshot_id'] and b.team_id==p.team_id),None)
    if not prior or prior[1].trade_date!=p.as_of_date or not prior[1].account:raise ValueError('需要相鄰且同隊的前份帳戶')
    if data['authority'] not in {'user_supplied_evidence','reconstructed_estimate'}:raise ValueError('不可自稱官方已驗證成交')
    if not proof or not isinstance(data['events'],list) or len(data['events'])>200:raise ValueError('需附原始成交／公司行動證據')
    positions={h.code:h.shares for h in prior[1].holdings}
    for row in data['events']:
        if not isinstance(row,dict) or set(row)!={'code','kind','shares','gross_twd','fee_twd','tax_twd'}:raise ValueError('每筆事件欄位不符')
        if not isinstance(row['code'],str) or not __import__('re').fullmatch(r'\d{4,6}',row['code']):raise ValueError('股票代碼無效')
        if row['kind'] in {'BUY','SELL'} and (p.prev_day_orders.outcome!='executed' or row['code'] in p.prev_day_orders.excluded_codes):raise ValueError('官方成交結果不允許此交易事件')
        q=apply({'shares':positions.get(row['code'],0),'cost':None,'realized':None,'income':None,'fees':D(0)},row)
        positions[row['code']]=q['shares']
    actual={h.code:h.shares for h in p.holdings if h.shares}
    if {c:n for c,n in positions.items() if n}!=actual:raise ValueError('事件股數與官方結算不一致')
    existing=store.root/'holding-ledger'/'transactions'/(snapshot_id+'.json')
    if existing.exists():
        saved=json.loads(existing.read_bytes())
        if store.read(saved['raw_ref'])!=body or store.read(saved['proof_ref'])!=proof:raise ValueError('Immutable transaction conflict')
        return saved
    envelope={'snapshot_id':snapshot_id,'raw_ref':store.put(body),'proof_ref':store.put(proof,'bin'),'data':data,'received_at':now()}
    immutable(store.root/'holding-ledger'/'transactions'/(snapshot_id+'.json'),encoded(envelope))
    return envelope


def quote_index(store):
    """Only official captured daily turnover; reconstruction remains an estimate."""
    from .cli import candidate_sources, settings
    from .normalize import normalize
    _,universe=settings();sources={s.id:s for s in candidate_sources() if s.kind=='quotes'}
    quotes={}
    with store.connect() as db:
        captures=db.execute("SELECT source_id,ref,fetched_at FROM captures WHERE status='ok' ORDER BY epoch,id").fetchall()
    for sid,ref,at in captures:
        if sid not in sources:continue
        try:
            rows,issues=normalize(sources[sid],{'ref':ref,'first_seen_at':at,'fetched_at':at},store.read(ref),universe,now())
            if issues:continue
            for r in rows:
                v=r['values'];volume=v.get('volume');total=v.get('amount')
                if volume and total and D(volume)>0 and D(total)>0:
                    quotes[(r['date'],r['security_id'])]={'price':D(total)/D(volume),'raw_ref':ref,'raw_row':r['raw_row'],'method':'official_daily_turnover_divided_by_volume_not_confirmed_execution'}
        except (ValueError,KeyError,TypeError):continue
    # The factor bundles carry hash-checked monthly raw captures, including
    # older dates no longer in rolling OpenAPI responses.
    from .history import normalize_month
    seen=set()
    for path in sorted((store.root/'agent-inputs').glob('research-data-*.json')):
        bundle=json.loads(path.read_bytes())
        for ref in bundle.get('history_inputs',[]):
            if ref in seen:continue
            seen.add(ref);cap=store.json(ref)
            for r in normalize_month(store.read(cap['raw_ref']),cap['market'],cap['code'],cap['month'],cap['fetched_at'],cap['raw_ref']):
                if r['usable_quote'] and not r['corporate_action_marker'] and not r['listing_boundary_marker']:
                    key=(r['date'],r['code'])
                    quotes.setdefault(key,{'price':D(r['amount_twd'])/D(r['volume_shares']),'raw_ref':r['raw_ref'],'raw_row':r['raw_row'],'method':'downloaded_monthly_turnover_not_confirmed_execution'})
    return quotes


def replay(store,selected_event,selected_pack):
    from .holding_ledger import settlements
    rows=[(e,p) for e,p in settlements(store,selected_pack.team_id) if p.account and p.trade_date<=selected_pack.trade_date]
    groups={}
    for e,p in rows:groups.setdefault(str(p.as_of_date) if p.as_of_date else 'INITIAL',[]).append((e,p))
    timeline=[];conflicts=[]
    for key,items in groups.items():
        signatures={digest(encoded({'account':p.account.model_dump(mode='json'),'holdings':[h.model_dump(mode='json') for h in p.holdings],'outcome':p.prev_day_orders.model_dump(mode='json')})) for _,p in items}
        if len(signatures)>1:conflicts.append(key)
        else:timeline.append(next(((e,p) for e,p in items if e['id']==selected_event['id']),items[-1]))
    timeline.sort(key=lambda ep:('' if ep[1].as_of_date is None else str(ep[1].as_of_date),str(ep[1].trade_date)))
    quotes=None;positions={};events=[];warnings=[];previous=None;previous_event=None;initial=False;cash_bridge=[];selected_previous=None
    def empty(shares=0,known=False):return {'shares':shares,'cost':D(0) if known else None,'realized':D(0) if known else None,'income':D(0) if known else None,'fees':D(0),'authority':'missing'}
    for event,pack in timeline:
        if pack.as_of_date is None:
            initial=True;previous=pack;previous_event=event;continue
        if selected_pack.as_of_date and pack.as_of_date>selected_pack.as_of_date:continue
        if event['id']==selected_event['id']:selected_previous=previous_event['id'] if previous_event else None
        actual={h.code:h.shares for h in pack.holdings if h.shares}
        adjacent=previous and previous.trade_date==pack.as_of_date
        ordered=adjacent and pack.prev_day_orders.outcome=='executed'
        path=store.root/'holding-ledger'/'transactions'/(event['id']+'.json')
        imported=json.loads(path.read_bytes()) if path.exists() else None
        transition=[];authority='reconstructed_estimate';problem=False
        if imported:
            data=json.loads(store.read(imported['raw_ref']));store.read(imported['proof_ref'])
            if data!=imported['data'] or imported['snapshot_id']!=event['id']:raise ValueError('transaction_integrity_failed')
            if not previous_event or data['previous_snapshot_id']!=previous_event['id']:raise ValueError('transaction_previous_snapshot_changed')
            transition=data['events'];authority=data['authority']
        else:
            old={h.code:h for h in previous.holdings} if previous else {}
            for c in sorted(set(actual)|set(positions)):
                prev=positions.get(c,empty(known=bool(initial and adjacent)));delta=actual.get(c,0)-prev['shares']
                if not delta:continue
                current=next((h for h in pack.holdings if h.code==c),None)
                rights_changed=(old.get(c).receivable_shares if c in old else 0)!=(current.receivable_shares if current else 0)
                if quotes is None:quotes=quote_index(store)
                q=quotes.get((str(pack.as_of_date),c))
                if not ordered or c in pack.prev_day_orders.excluded_codes or rights_changed or not q:
                    positions[c]={**prev,'shares':actual.get(c,0),'cost':None,'realized':None,'income':None,'authority':'missing'}
                    warnings.append({'date':str(pack.as_of_date),'code':c,'reason':'missing_transition_price_or_action_evidence'});problem=True;continue
                gross=abs(delta)*q['price']
                transition.append({'code':c,'kind':'BUY' if delta>0 else 'SELL','shares':abs(delta),'gross_twd':str(gross),'fee_twd':str(gross*FEE),'tax_twd':str(gross*TAX if delta<0 else 0),'price_evidence':q|{'price':str(q['price'])}})
        cash_effect=D(0)
        for t in transition:
            c=t['code'];prior=positions.get(c,empty(known=bool(initial and adjacent)))
            positions[c]=apply(prior,t)
            if prior['authority']=='missing' and prior['shares']>0:positions[c]['authority']='missing'
            else:positions[c]['authority']='reconstructed_estimate' if authority=='reconstructed_estimate' or prior['authority']=='reconstructed_estimate' else authority
            events.append({**t,'date':str(pack.as_of_date),'snapshot_id':event['id'],'authority':authority})
            gross=D(t['gross_twd']);charges=D(t['fee_twd'])+D(t['tax_twd'])
            cash_effect+=-gross-charges if t['kind']=='BUY' else gross-charges if t['kind']=='SELL' else gross if t['kind']=='DIVIDEND' else D(0)
        if adjacent:
            residual=pack.account.cash-previous.account.cash-cash_effect
            cash_bridge.append({'date':str(pack.as_of_date),'official_cash_change':str(pack.account.cash-previous.account.cash),'reconstructed_cash_change':str(cash_effect),'unexplained_residual':str(residual),'complete':not problem and abs(residual)<=D('.01')})
        for c in set(positions)|set(actual):
            q=positions.setdefault(c,empty(actual.get(c,0)))
            conflict_crossed=bool(previous and any(str(previous.as_of_date or 'INITIAL')<=d<=str(pack.as_of_date) for d in conflicts))
            if q['shares']!=actual.get(c,0) or not adjacent or conflict_crossed:
                q.update(shares=actual.get(c,0),cost=None,realized=None,income=None,authority='missing')
        # An evidenced snapshot balance anchors remaining cost, not unknown
        # historical realized gains or dividend attribution.
        basis=store.root/'holding-ledger'/'cost-basis'/(event['id']+'.json')
        if basis.exists():
            b=json.loads(basis.read_bytes());raw=json.loads(store.read(b['raw_ref']));store.read(b['proof_ref'])
            for r in raw['positions']:r['remaining_cost_twd']=str(D(str(r['remaining_cost_twd'])))
            if raw!=b['data'] or b['pack_id']!=event['id']:raise ValueError('holding_cost_integrity_failed')
            for r in raw['positions']:
                positions[r['code']].update(cost=D(r['remaining_cost_twd']),authority='user_supplied_evidence')
        if cash_bridge and cash_bridge[-1]['date']==str(pack.as_of_date) and not cash_bridge[-1]['complete']:
            for position in positions.values():position['income']=None
        previous=pack;previous_event=event
        if event['id']==selected_event['id']:break
    if str(selected_pack.as_of_date or 'INITIAL') in conflicts:
        warnings.append({'reason':'conflicting_official_settlement'})
        positions={h.code:empty(h.shares) for h in selected_pack.holdings if h.shares}
    result=[]
    current={h.code:h for h in selected_pack.holdings}
    for c,p in sorted(positions.items()):
        h=current.get(c);market=h.shares*h.close_price if h and h.close_price is not None else D(0) if not p['shares'] else None
        unrealized=market-p['cost'] if market is not None and p['cost'] is not None else None
        trading=unrealized+p['realized'] if unrealized is not None and p['realized'] is not None else None
        total=unrealized+p['realized']+p['income'] if all(v is not None for v in [unrealized,p['realized'],p['income']]) else None
        result.append({'code':c,'shares':p['shares'],'cost':str(p['cost']) if p['cost'] is not None else None,
          'average_cost':str(p['cost']/p['shares']) if p['cost'] is not None and p['shares'] else None,
          'unrealized_pnl':str(unrealized) if unrealized is not None else None,
          'unrealized_return':str(unrealized/p['cost']) if unrealized is not None and p['cost'] else None,
          'realized_pnl':str(p['realized']) if p['realized'] is not None else None,'dividend_income':str(p['income']) if p['income'] is not None else None,
          'trading_pnl':str(trading) if trading is not None else None,'total_pnl':str(total) if total is not None else None,'fees_taxes':str(p['fees']),'cost_authority':p['authority']})
    return {'previous_snapshot_id':selected_previous,'method':'moving_weighted_average','rows':result,'events':events,'cash_reconciliation':cash_bridge,'warnings':warnings,'conflicting_dates':conflicts,
            'note':'重建估計以官方股數差及日成交金額／量計算，非官方逐筆成交證明；費用取整、公司行動與現金殘差需核對。未實現損益未扣未來賣出費稅；應收權益不計入可交易成本。'}
