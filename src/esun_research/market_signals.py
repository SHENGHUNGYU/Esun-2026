"""Evidence-derived short-horizon signals and descriptive portfolio risk.

Benchmarks are contemporaneous equal-weight competition-pool proxies, not TAIEX,
not total returns, and not historically investable universes. No return forecast.
"""
from collections import defaultdict
from decimal import Decimal
import statistics
from .contracts import instant
from .store import digest, encoded

D=Decimal
ZERO=D(0)


def evidence(row):
    return {k:row[k] for k in ['source_id','raw_ref','raw_row','date','available_at']}


def covariance(x,y):
    if len(x)<2 or len(x)!=len(y):return None
    a=sum(x)/len(x);b=sum(y)/len(y)
    return sum((u-a)*(v-b) for u,v in zip(x,y))/(len(x)-1)


def price_signals(prices,sessions,quotes,universe,cell,missing):
    """Fixed, balanced 21-session cohort avoids time-varying benchmark weights."""
    panel={};series={};dates=sessions[-21:]
    for code,dated in sorted(prices.items()):
        def gap(reason):missing.append({'code':code,'feature':'extended_price_signals','reason':reason})
        if len(dates)!=21 or any(d not in dated or not dated[d]['usable_quote'] for d in dates):
            gap('incomplete_reference_window');continue
        from datetime import date
        if any((date.fromisoformat(b)-date.fromisoformat(a)).days>10 for a,b in zip(dates,dates[1:])):
            gap('unverified_calendar_gap');continue
        rows=[dated[d] for d in dates];close=[D(r['close_twd']) for r in rows]
        returns=[b/a-1 for a,b in zip(close,close[1:])]
        if any(r['corporate_action_marker'] or r['listing_boundary_marker'] for r in rows) or any(abs(r)>D('.15') for r in returns):
            gap('unverified_raw_price_boundary');continue
        if code not in quotes or close[-1]!=D(quotes[code]['values']['close']):
            gap('historical_reference_close_not_verified');continue
        refs=[{'source_id':r['source_id'],'raw_ref':r['raw_ref'],'raw_row':r['raw_row'],'date':r['date'],'available_at':r['fetched_at']} for r in rows]
        volumes=[D(r['volume_shares']) for r in rows]
        for n in (5,20):cell(code,'ma_distance_'+str(n),close[-1]/(sum(close[-n:])/n)-1,refs[-n:])
        cell(code,'volume_ratio_5',volumes[-1]/(sum(volumes[-6:-1])/5),refs[-6:])
        cell(code,'drawdown_20',close[-1]/max(close[-20:])-1,refs[-20:])
        cell(code,'breakout_20',close[-1]/max(D(r['high_twd']) for r in rows[:-1])-1,refs)
        series[code]={'dates':dates,'closes':[str(c) for c in close],'returns':[str(r) for r in returns],
            'industry':universe.get(code,{}).get('industry','unknown'),'evidence':refs}
        panel[code]=returns
    # Minimum cohort: small fixtures / partial markets must not masquerade as market breadth.
    if len(panel)>=20:
        market=[sum(panel[c][i] for c in panel)/len(panel) for i in range(20)]
        def compact_refs(codes):
            groups={}
            for c in codes:
                for r in series[c]['evidence']:
                    key=(r['source_id'],r['raw_ref'])
                    if key not in groups:groups[key]={**r,'raw_rows':[],'dates':[]}
                    groups[key]['raw_rows'].append(r['raw_row']);groups[key]['dates'].append(r['date'])
            return list(groups.values())
        market_refs=compact_refs(sorted(series))
        def growth(rs,n):
            v=D(1)
            for r in rs[-n:]:v*=1+r
            return v-1
        for c,rs in panel.items():
            refs=market_refs
            for n in (5,20):cell(c,'relative_pool_'+str(n),growth(rs,n)-growth(market,n),refs)
            var=covariance(market,market)
            if var and var>0:cell(c,'beta_pool_20',covariance(rs,market)/var,refs)
        benchmark={'kind':'current_competition_pool_equal_weight_price_proxy','members':sorted(panel),
            'dates':dates[1:],'returns':[str(r) for r in market]}
    else:benchmark={'kind':'unavailable','reason':'fewer_than_20_verified_series','members':sorted(panel)}
    return {'series':series,'benchmark':benchmark,'limitations':[
        'Twenty sessions, raw price returns, no annualization or expected-return estimate.',
        'Current fixed competition-pool cohort; not official market/industry indices or PIT universe.',
        'Corporate-action gaps are excluded, never filled with zero.']}


def flow_signals(flow_rows,prices,sessions,cell,missing):
    for code,dated in sorted(flow_rows.items()):
        for feature in ('foreign_net_ratio','trust_net_ratio','dealer_net_ratio','dealer_self_net_ratio','dealer_hedge_net_ratio'):
            base=feature.removesuffix('_net_ratio')
            for n in (3,5,10):
                dates=sessions[-n:]
                if len(dates)!=n or any(d not in dated or feature not in dated[d]['values'] or d not in prices.get(code,{}) or not prices[code][d]['usable_quote'] for d in dates):
                    missing.append({'code':code,'feature':base+'_net_ratio_'+str(n),'reason':'incomplete_flow_window'});continue
                nets=[D(dated[d]['values'][feature]) for d in dates]
                volumes=[D(prices[code][d]['volume_shares']) for d in dates]
                refs=[r for d in dates for r in [dated[d]['evidence'],{
                    'source_id':prices[code][d]['source_id'],'raw_ref':prices[code][d]['raw_ref'],
                    'raw_row':prices[code][d]['raw_row'],'date':d,'available_at':prices[code][d]['fetched_at']}]]
                cell(code,base+'_net_ratio_'+str(n),sum(nets)/sum(volumes),refs)
                cell(code,base+'_buy_days_'+str(n),sum(x>0 for x in nets),refs)
                if n==10:
                    # Distinct non-overlapping five-session periods, volume-normalized.
                    change=sum(nets[5:])/sum(volumes[5:])-sum(nets[:5])/sum(volumes[:5])
                    cell(code,base+'_flow_change_5',change,refs)


def event_signals(news,risk_data,cutoff,history=None):
    """Classify observed timing, not semantic novelty, sentiment, or price causality."""
    result=[];seen=set();series=risk_data.get('series',{})
    for n in sorted(news,key=lambda r:r['available_at'],reverse=True):
        if instant(n['available_at'])>instant(cutoff):continue
        # Matching content is exact normalized text, not inferred semantic equivalence.
        fingerprint=digest(encoded([n.get('code'),' '.join(n['text'].split())]))
        if fingerprint in seen:continue
        seen.add(fingerprint);item=dict(n)
        pub=n.get('published_at');publication=instant(pub) if pub else None
        if publication and publication>instant(cutoff):continue
        item['event_timing']={'publication_age_hours':str(D(str((instant(cutoff)-publication).total_seconds()))/3600) if publication else None,
            'observed_available_at':n['available_at'],
            'earliest_observed_in_archived_reports':(history or {}).get('events',{}).get(fingerprint),
            'novelty':'previously_observed_exact_content' if fingerprint in (history or {}).get('events',{}) else 'not_seen_in_archived_reports',
            'semantic_novelty':'unknown','priced_in':'unknown','post_publication_close_return':None}
        p=series.get(n.get('code'),{});dates=p.get('dates',[])
        if publication and dates:
            # Start at close strictly before publication. Includes event session
            # where applicable; never labels contemporaneous movement as causal.
            before=[i for i,d in enumerate(dates) if instant(d+'T13:30:00+08:00')<publication]
            if before and before[-1]<len(dates)-1:
                i=before[-1];item['event_timing']['post_publication_close_return']=str(D(p['closes'][-1])/D(p['closes'][i])-1)
                item['event_timing']['price_base_date']=dates[i]
                item['event_timing']['price_source_rows']=[p['evidence'][i],p['evidence'][-1]]
        result.append(item)
    return result


def portfolio_risk(risk_data,weights,industries):
    """Covariance on a common complete window; missing weight stays unknown."""
    series=risk_data.get('series',{});positive={c:D(str(w)) for c,w in weights.items() if D(str(w))>0}
    sectors=defaultdict(lambda:ZERO)
    for c,w in positive.items():sectors[industries.get(c,'unknown')]+=w
    result={'max_industry_weight':str(max(sectors.values(),default=ZERO)),
        'equity_hhi':str(sum(w*w for w in positive.values())),
        'missing_codes':sorted(set(positive)-set(series)),
        'covered_weight':str(sum(w for c,w in positive.items() if c in series)),
        'daily_volatility':None,'beta_pool':None,'weighted_pair_correlation':None}
    # No partial-window covariance: unknown positions must not reduce apparent risk.
    if result['missing_codes'] or not positive:return result
    codes=sorted(positive);dates=series[codes[0]]['dates']
    if any(series[c]['dates']!=dates for c in codes):return result
    rs={c:list(map(D,series[c]['returns'])) for c in codes}
    if len(rs[codes[0]])<20:return result
    pr=[sum(positive[c]*rs[c][i] for c in codes) for i in range(20)]
    variance=covariance(pr,pr);result['daily_volatility']=str(variance.sqrt()) if variance is not None else None
    market=risk_data.get('benchmark',{})
    if market.get('returns') and market['dates']==dates[1:]:
        mr=list(map(D,market['returns']));mv=covariance(mr,mr)
        if mv and mv>0:result['beta_pool']=str(covariance(pr,mr)/mv)
    numerator=ZERO;denominator=ZERO;contributions=[]
    for i,c in enumerate(codes):
        marginal=covariance(rs[c],pr)
        contributions.append([c,str(positive[c]*marginal/variance) if variance and variance>0 else None])
        for p in codes[i+1:]:
            v=covariance(rs[c],rs[c])*covariance(rs[p],rs[p])
            if v>0:
                weight=positive[c]*positive[p];numerator+=weight*covariance(rs[c],rs[p])/v.sqrt();denominator+=weight
    result['weighted_pair_correlation']=str(numerator/denominator) if denominator else None
    result['variance_contribution']=sorted(contributions,key=lambda x:D(x[1] or 0),reverse=True)
    return result


def risk_comparison(workspace,targets):
    from .turnover import held_positions,weights_for_positions
    old=weights_for_positions(held_positions(workspace.pack),workspace.pack,workspace.snapshot['prices'])
    industries={c:r['industry'] for c,r in workspace.rows.items()}
    before=portfolio_risk(workspace.risk_data,old,industries);after=portfolio_risk(workspace.risk_data,targets,industries)
    metrics=['max_industry_weight','equity_hhi','covered_weight','daily_volatility','beta_pool','weighted_pair_correlation']
    return {'columns':metrics,'before':[before[k] for k in metrics],'after':[after[k] for k in metrics],
        'missing_before':before['missing_codes'],'missing_after':after['missing_codes'],
        'variance_contribution':after.get('variance_contribution',[]),
        'scope':'Descriptive 20-session raw-price risk against pool proxy; no forecast benefit or cost recovery claim.'}


def industry_cells(risk_data,industries,classifications=None):
    """Leave-one-out peers classified by this frozen decision snapshot."""
    series=risk_data.get('series',{});groups=defaultdict(list);cells=[]
    for c in series:
        group=industries.get(c,'unknown')
        if group!='unknown':groups[group].append(c)
    def growth(rs):
        value=D(1)
        for r in rs:value*=1+D(r)
        return value-1
    for group,codes in groups.items():
        if len(codes)<4:continue
        for c in codes:
            peers=[p for p in codes if p!=c]
            if any(series[p]['dates']!=series[c]['dates'] for p in peers):continue
            mean=[sum(D(series[p]['returns'][i]) for p in peers)/len(peers) for i in range(20)]
            rows=[r for p in [c,*peers] for r in [*series[p]['evidence'],*(classifications or {}).get(p,[])]]
            v={'code':c,'feature':'relative_industry_20','value':str(growth(series[c]['returns'])-growth(mean)),'rows':rows}
            v['evidence_id']='E'+digest(encoded(v))[:18];cells.append(v)
    return cells


def analysis_report(workspace,cutoff):
    return {'schema_version':'short-horizon-analysis-1','cutoff_at':cutoff,
        'benchmark':{k:v for k,v in workspace.risk_data.get('benchmark',{}).items() if k!='returns'},
        'stock_columns':['code','industry','values','evidence_refs'],
        'stocks':[[c,r['industry'],r['values'],r['evidence']] for c,r in sorted(workspace.rows.items())],
        'events':workspace.news,'feature_definitions':workspace.catalog(),
        'limitations':['Snapshot availability differs by stock; missing is unknown, not zero.',
            'Pool and industry proxies are not official indices; current cohort is not a historical investable universe.',
            'Exact content deduplication does not establish semantic novelty; price reaction does not establish causality or priced-in status.',
            'Portfolio risk uses 20 raw daily returns; historical risk is not a return forecast.']}


def analysis_markdown(report):
    columns=['momentum_5','relative_pool_20','relative_industry_20','volume_ratio_5','ma_distance_20',
        'drawdown_20','foreign_net_ratio_5','foreign_buy_days_5','trust_net_ratio_5','beta_pool_20']
    labels=['五日動能','相對競賽池','相對產業同儕','量比','距二十日均線','二十日回撤','外資五日流量比','外資五日買超天數','投信五日流量比','池代理Beta']
    lines=['# 個股短期研究訊號','','截止：'+report['cutoff_at'],'',
        '比例為小數；缺值顯示「—」。代理指數非官方大盤，訊號並非預測收益。',
        '外資買超天數是窗口內總天數，不代表連續買超。事件新穎性與是否反映於價格仍為未知。','',
        '|代碼|產業|'+ '|'.join(labels)+'|','|'+'---|'*(len(columns)+2)]
    for code,industry,values,refs in report['stocks']:
        line=[code,industry]
        line += [format(D(values[f]),'.5g') if values.get(f) is not None else '—' for f in columns]
        lines.append('|'+ '|'.join(line)+'|')
    lines+=['','## 資料限制','']+['- '+s for s in report['limitations']]
    lines+=['','## 已觀察事件','']
    for n in report['events']:
        timing=n.get('event_timing',{})
        text=n['text'].replace('\n',' ').replace('|','／')
        lines.append('- '+str(n.get('code') or '市場')+'：'+text+'；發布：'+str(n.get('published_at'))+
            '；可觀察時間：'+n['available_at']+'；發布後價格報酬：'+str(timing.get('post_publication_close_return'))+'；是否已反映：未知。')
    return '\n'.join(lines)+'\n'


def frozen_event_history(store,cutoff,run_id):
    """Exact content observed in older immutable candidate reports, cutoff-bound.

    This is evidence of repetition within this application's coverage, never
    proof of first publication or comprehensive news coverage.
    """
    import json
    events={};sources=[]
    for manifest_path in sorted((store.root/'candidates').glob('*/manifest.json')):
        if manifest_path.parent.name==run_id:continue
        manifest=json.loads(manifest_path.read_bytes());request=manifest['request']
        if instant(request['cutoff_at'])>instant(cutoff):continue
        expected=manifest['artifacts'].get('agent-research.json')
        if not expected:continue
        body=(manifest_path.parent/'agent-research.json').read_bytes()
        if digest(body)!=expected:raise ValueError('event_history_report_hash_mismatch')
        report=json.loads(body);sources.append({'run_id':request['run_id'],'sha256':expected})
        for n in report.get('news',[]):
            if instant(n['available_at'])>instant(cutoff):continue
            key=digest(encoded([n.get('code'),' '.join(n['text'].split())]))
            previous=events.get(key)
            if not previous or instant(n['available_at'])<instant(previous):events[key]=n['available_at']
    return {'events':events,'sources':sources,'scope':'Exact matching archived candidate news only; absence does not establish novelty.'}
