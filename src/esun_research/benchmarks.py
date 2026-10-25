"""Verified ETF holdings imports and two explicitly provisional Active Share views."""
from datetime import date
from decimal import Decimal
from typing import Literal
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .contracts import instant, now
from .store import encoded,digest

class Equity(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    asset_type: Literal['equity']
    security_id: str = Field(pattern=r'^[A-Z]{2,12}:[A-Z0-9._/\-]{1,40}$')
    weight_nav: Decimal = Field(ge=0,le=1)
    shares: int | None = Field(default=None,ge=0)
    raw_row: int = Field(ge=0)

class Benchmark(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    schema_version: Literal['1.0']
    benchmark_code: str = Field(pattern=r'^[0-9]{5}A$')
    valuation_date: date
    pcf_applicable_date: date | None
    fetched_at: str
    source_url: str
    source_name: str
    evidence_kind: Literal['official_actual_holdings_table','pcf_basket_only']
    complete_equity_table: bool
    nav_twd: Decimal | None = Field(default=None,gt=0)
    raw_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    provenance_notes: list[str] = Field(default_factory=list,max_length=30)
    raw_table_header: list[str] = Field(default_factory=list,max_length=30)
    method: Literal['GET','POST'] | None = None
    request: dict[str,str | None] | None = None
    raw_row_definition: str | None = None
    valuation_date_basis: Literal['explicit_source_date','official_pcf_timing_inference'] = 'explicit_source_date'
    nav_source_url: str | None = None
    nav_source_raw_sha256: str | None = Field(default=None,pattern=r'^[a-f0-9]{64}$')
    prospectus_source_url: str | None = None
    prospectus_raw_sha256: str | None = Field(default=None,pattern=r'^[a-f0-9]{64}$')
    identity_source_url: str | None = None
    identity_raw_sha256: str | None = Field(default=None,pattern=r'^[a-f0-9]{64}$')
    holdings: list[Equity] = Field(min_length=1,max_length=2000)

    @model_validator(mode='after')
    def coherent(self):
        fetched=instant(self.fetched_at)
        if self.valuation_date>fetched.date() or fetched>instant(now()):raise ValueError('benchmark_future_date')
        p=urlparse(self.source_url)
        if p.scheme!='https' or p.username or p.password:raise ValueError('benchmark_source_not_https')
        ids=[h.security_id for h in self.holdings]
        if len(ids)!=len(set(ids)):raise ValueError('duplicate_benchmark_security')
        if not 0<sum(h.weight_nav for h in self.holdings)<=Decimal('1.0001'):raise ValueError('invalid_equity_weight_sum')
        if bool(self.nav_source_url)!=bool(self.nav_source_raw_sha256) or bool(self.prospectus_source_url)!=bool(self.prospectus_raw_sha256):raise ValueError('incomplete_supporting_source')
        if bool(self.identity_source_url)!=bool(self.identity_raw_sha256):raise ValueError('incomplete_identity_source')
        if self.valuation_date_basis=='official_pcf_timing_inference' and not self.prospectus_raw_sha256:raise ValueError('pcf_timing_requires_official_prospectus')
        return self

def import_benchmark(store,body,raw,allowed_codes,allowed_hosts,supporting_raws=None):
    value=Benchmark.model_validate_json(body)
    if value.benchmark_code not in allowed_codes:raise ValueError('benchmark_outside_official_30')
    if urlparse(value.source_url).hostname not in allowed_hosts:raise ValueError('unverified_issuer_host')
    if digest(raw)!=value.raw_sha256:raise ValueError('benchmark_raw_hash_mismatch')
    if value.evidence_kind!='official_actual_holdings_table' or not value.complete_equity_table:raise ValueError('actual_complete_equity_table_required')
    supporting_refs={}
    for url,sha in [(value.nav_source_url,value.nav_source_raw_sha256),(value.prospectus_source_url,value.prospectus_raw_sha256),(value.identity_source_url,value.identity_raw_sha256)]:
        if not sha:continue
        parsed=urlparse(url)
        if parsed.scheme!='https' or parsed.hostname not in allowed_hosts or parsed.username or parsed.password:raise ValueError('unverified_supporting_source')
        evidence=(supporting_raws or {}).get(sha)
        if evidence is None or digest(evidence)!=sha:raise ValueError('missing_or_invalid_supporting_raw:'+sha)
        supporting_refs[sha]=store.put(evidence,'bin')
    raw_ref=store.put(raw,'bin');available_at=now()
    wrapper={'benchmark':value.model_dump(mode='json'),'raw_ref':raw_ref,'supporting_refs':supporting_refs,'imported_at':available_at,
        'verification':'typed import + raw hash; source interpretation remains visible for operator review'}
    return store.capture('ETF:'+value.benchmark_code,encoded(wrapper),fetched_at=available_at)

def top15(weights):
    return dict(sorted(weights.items(),key=lambda item:(-item[1],item[0]))[:15])

def compare(weights,other):
    a=top15(weights);b=top15(other);union=set(a)|set(b)
    raw=sum((abs(a.get(c,Decimal(0))-b.get(c,Decimal(0))) for c in union),Decimal(0))/2
    sa=sum(a.values());sb=sum(b.values())
    if sa<=0 or sb<=0:raise ValueError('top15_has_no_positive_weight')
    normalized=sum((abs(a.get(c,Decimal(0))/sa-b.get(c,Decimal(0))/sb) for c in union),Decimal(0))/2
    return {'raw_nav_top15':str(raw),'normalized_top15':str(normalized),'conservative_internal_value':str(min(raw,normalized)),
        'portfolio_top15_weight_sum':str(sa),'benchmark_top15_weight_sum':str(sb),'portfolio_top15':{k:str(v) for k,v in a.items()},'benchmark_top15':{k:str(v) for k,v in b.items()}}

def evaluate(store,refs,weights,expected_codes,valuation_date,cutoff,buffer):
    results=[];problems=[];seen=set()
    own={'TW:'+c:Decimal(str(w)) for c,w in weights.items()}
    for ref in refs:
        try:
            wrapper=store.json(ref);benchmark=Benchmark.model_validate(wrapper['benchmark']);code=benchmark.benchmark_code
            if code in seen:raise ValueError('duplicate_benchmark_snapshot')
            seen.add(code)
            if code not in expected_codes:raise ValueError('benchmark_outside_official_30')
            if benchmark.valuation_date.isoformat()!=str(valuation_date):raise ValueError('benchmark_valuation_date_mismatch')
            if instant(wrapper['imported_at'])>instant(cutoff) or instant(benchmark.fetched_at)>instant(cutoff):raise ValueError('benchmark_after_cutoff')
            if digest(store.read(wrapper['raw_ref']))!=benchmark.raw_sha256:raise ValueError('benchmark_raw_hash_mismatch')
            for sha in [benchmark.nav_source_raw_sha256,benchmark.prospectus_raw_sha256,benchmark.identity_raw_sha256]:
                if sha and digest(store.read(wrapper.get('supporting_refs',{})[sha]))!=sha:raise ValueError('supporting_raw_hash_mismatch')
            if benchmark.evidence_kind!='official_actual_holdings_table' or not benchmark.complete_equity_table:raise ValueError('actual_complete_equity_table_required')
            values=compare(own,{h.security_id:h.weight_nav for h in benchmark.holdings})
            results.append({'benchmark_code':code,'snapshot_ref':ref,'source_url':benchmark.source_url,'valuation_date':benchmark.valuation_date.isoformat(),
                'valuation_date_basis':benchmark.valuation_date_basis,
                **values,'internal_buffer_pass':Decimal(values['conservative_internal_value'])>=buffer})
        except (ValueError,KeyError,TypeError) as e:problems.append({'snapshot_ref':ref,'reason':str(e)[:200]})
    covered={r['benchmark_code'] for r in results};missing=sorted(set(expected_codes)-covered)
    blockers=[]
    if missing or problems:blockers.append('active_share_30_etfs_not_verified')
    if any(not r['internal_buffer_pass'] for r in results):blockers.append('active_share_internal_buffer_failed')
    blockers.append('active_share_official_method_and_dates_unconfirmed')
    return {'expected_count':len(expected_codes),'validated_count':len(results),'missing_codes':missing,'problems':problems,
        'results':results,'internal_buffer':str(buffer),'internal_all_pass':not missing and not problems and all(r['internal_buffer_pass'] for r in results),
        'official_pass':False,'release_blockers':blockers,
        'method_note':'Both portfolios use their own top 15 equities, union identifiers and absent weights zero. View A keeps NAV weights; view B normalizes each top 15. This internal policy is not official certification; one day does not prove a consecutive-day condition.'}
