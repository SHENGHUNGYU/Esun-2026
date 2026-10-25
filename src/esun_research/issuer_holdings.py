"""Date-preserving adapters for verified official complete-equity tables."""
import base64
import json
import re
import subprocess
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from . import issuer_transport
from .benchmarks import Benchmark, import_benchmark
from .gateway import RemoteGateway
from .store import digest, encoded

SUPPORTED = issuer_transport.SUPPORTED

def number(value):
    return Decimal(str(value).replace(',', '').replace('%', '').strip())

def security(value):
    value = value.strip()
    if re.fullmatch(r'\d{4,6}', value):
        return 'TW:' + value
    if re.fullmatch(r'[A-Z0-9.\-]+ US', value):
        return 'US:' + value[:-3]
    raise ValueError('unknown_security_market')

def row(ticker, weight, shares, index):
    quantity = number(shares)
    if quantity < 0 or quantity != quantity.to_integral_value():
        raise ValueError('invalid_equity_quantity')
    return {'asset_type':'equity', 'security_id':security(ticker),
        'weight_nav':str(number(weight)/100), 'shares':int(quantity), 'raw_row':int(index)}

def parse(issuer, code, record, identity):
    if code not in SUPPORTED[issuer]:
        raise ValueError('unsupported_benchmark')
    raw = base64.b64decode(record['raw_base64'], validate=True)
    value = json.loads(raw, parse_float=Decimal)
    proof = json.loads(base64.b64decode(identity['raw_base64']), parse_float=Decimal) if identity else None
    notes = ['完整股票表；保留官方NAV百分比精度，不重新正規化，不將海外ADR與台股合併。',
        '抓取時間、股票評價日與PCF適用日分開；日期不符不升格為有效比較。']
    pcf = None
    if issuer in {'nomura','allianz'}:
        if value['StatusCode'] != 0:
            raise ValueError('issuer_body_status_failed')
        entries = value['Entries']
        expected_id = code
        if issuer == 'allianz':
            if proof['StatusCode'] != 0:
                raise ValueError('issuer_identity_failed')
            matches = [x for x in proof['Entries'] if x['CSecuritiesCode'] == code]
            if len(matches) != 1:
                raise ValueError('issuer_identity_not_unique')
            expected_id = matches[0]['CFundNo']
        if entries['FundID'] != expected_id or record['request']['FundID'] != expected_id:
            raise ValueError('issuer_fund_identity_mismatch')
        data = entries['Data']; assets = data['FundAsset']
        valuation = assets['NavDate'].replace('/', '-'); nav = assets['Aum']
        pcf = assets.get('PCFDate')
        if pcf: pcf = pcf.replace('/', '-')
        tabs = [x for x in data['Table'] if x['TableTitle'] == '股票' or re.fullmatch(r'股票 \([0-9.]+%\)', x['TableTitle'])]
        if len(tabs) != 1:
            raise ValueError('complete_equity_table_not_unique')
        tab = tabs[0]; columns = [x['Name'] for x in tab['Columns']]
        expected = ['股票代號','股票名稱','股數','權重(%)']
        if issuer == 'allianz': expected = ['序號'] + expected
        if columns != expected or any(len(x) != len(columns) for x in tab['Rows']):
            raise ValueError('issuer_table_columns_changed')
        offset = 1 if issuer == 'allianz' else 0
        holdings = [row(x[offset], x[offset+3], x[offset+2], i+1) for i,x in enumerate(tab['Rows'])]
        if issuer == 'allianz':
            total = Decimal(re.search(r'\(([0-9.]+)%\)',tab['TableTitle'])[1])/100
            if abs(sum(Decimal(x['weight_nav']) for x in holdings)-total) > Decimal('.00005')*len(holdings)+Decimal('.00005'):
                raise ValueError('issuer_equity_total_mismatch')
    elif issuer == 'ctbc':
        if value['ResultCode'] != 0 or proof['ResultCode'] != 0:
            raise ValueError('issuer_body_status_failed')
        matches = [x for x in proof['Data']['List'] if x['ETF_ID'] == code]
        if len(matches) != 1 or record['request']['FID'] != matches[0]['FID']:
            raise ValueError('issuer_fund_identity_mismatch')
        data = value['Data']
        if len(data['Data']) != 1 or data['Data'][0]['ETF_ID'] != code:
            raise ValueError('issuer_fund_identity_mismatch')
        fund = data['Data'][0]
        valuation = fund['淨值日期'].replace('/', '-'); pcf = fund['公告日'].replace('/', '-')
        nav = number(fund['基金淨資產價值'])
        tabs = [x for x in data['Detail'] if x['Code'] == 'STOCK']
        if len(tabs) != 1 or any(x['invtp_'] != 'STOCK' for x in tabs[0]['Data']):
            raise ValueError('complete_equity_table_not_unique')
        holdings = [row(x['code_'], x['weights_'], x['qty_'], x['SNO']) for x in tabs[0]['Data']]
        if abs(sum(Decimal(x['weight_nav']) for x in holdings)-number(tabs[0]['Sum'])/100) > Decimal('.0001'):
            raise ValueError('issuer_equity_total_mismatch')
        for source, item in zip(tabs[0]['Data'], holdings):
            if item['security_id'].startswith('TW:') and abs(number(source['amount_'])/nav-Decimal(item['weight_nav'])) > Decimal('.0000501'):
                raise ValueError('issuer_nav_weight_mismatch')
    else:
        if value['code'] != 200 or proof['code'] != 200 or proof['data']['stockNo'] != code:
            raise ValueError('issuer_fund_identity_mismatch')
        data = value['data']; p = data['pcf']
        if str(proof['data']['fundNo']) != str(record['request']['fundId']) or p['inKind'] != 'N':
            raise ValueError('issuer_fund_identity_mismatch')
        valuation = p['date2']; pcf = p['date1']; nav = p['nav']
        if any(x['date1'].split(' ')[0].replace('/','-') != pcf for x in data['stocks']):
            raise ValueError('mixed_issuer_dates')
        holdings = [row(x['stocNo'], x['weight'], x['share'], i+1) for i,x in enumerate(data['stocks'])]
    if len(holdings) < 15:
        raise ValueError('suspiciously_short_equity_table')
    value = dict(schema_version='1.0', benchmark_code=code, valuation_date=valuation,
        pcf_applicable_date=pcf, fetched_at=max(record['fetched_at'], identity['fetched_at'] if identity else record['fetched_at']),
        source_url=record['url'], source_name=issuer+' 官方完整股票持股',
        evidence_kind='official_actual_holdings_table', complete_equity_table=True,
        nav_twd=str(number(nav)), raw_sha256=digest(raw), holdings=holdings,
        method=record['method'], request=record['request'], provenance_notes=notes)
    # Bind identity evidence in the existing supporting-proof contract.
    if identity:
        value.update(identity_source_url=identity['url'], identity_raw_sha256=digest(base64.b64decode(identity['raw_base64'])))
        notes.append('補充原始檔是公開基金代碼對照，供識別核對；NAV本身取持股回應，並非取對照表。')
    return Benchmark.model_validate(value), raw

def download(issuer, reference_date, pcf_date, ssh_host=None):
    args = [issuer, date.fromisoformat(reference_date).isoformat(), date.fromisoformat(pcf_date).isoformat()]
    if issuer not in SUPPORTED: raise ValueError('unsupported_issuer')
    if ssh_host:
        if ssh_host not in RemoteGateway.ALLOWED_HOSTS: raise ValueError('unapproved_ssh_host')
        command = ['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
            '-o','ConnectTimeout=8','-o','ConnectionAttempts=1','nelson@'+ssh_host,'python3','-',*args]
        source = Path(issuer_transport.__file__).read_bytes()
    else:
        command = [sys.executable, '-m', 'esun_research.issuer_transport', *args]; source = None
    try:
        proc = subprocess.run(command, input=source, capture_output=True, timeout=210)
        if proc.returncode or len(proc.stdout) > 100_000_000:
            return {'records':[], 'error':'issuer_worker_failed'}
        result = json.loads(proc.stdout)
        if set(result) != {'records','error'}: raise ValueError('invalid_worker_result')
        return result
    except (subprocess.TimeoutExpired, ValueError):
        return {'records':[], 'error':'issuer_worker_failed'}

def collect(store, reference_date, pcf_date, allowed_codes, allowed_hosts, ssh_host=None, downloader=download):
    results = []
    for issuer, codes in SUPPORTED.items():
        response = downloader(issuer, reference_date, pcf_date, ssh_host)
        records = {r['label']:r for r in response['records']}
        for label, record in records.items():
            raw=base64.b64decode(record['raw_base64'],validate=True)
            store.capture('issuer-raw:'+issuer+':'+label,encoded({
                'url':record['url'],'method':record['method'],'request':record['request'],
                'fetched_at':record['fetched_at'],'raw_ref':store.put(raw,'bin')}))
        for code in codes:
            try:
                if response['error']: raise ValueError(response['error'])
                identity = records.get(code+'-identity', records.get('identity'))
                benchmark, raw = parse(issuer, code, records[code], identity)
                supporting = {digest(b):b} if identity and (b:=base64.b64decode(identity['raw_base64'])) else {}
                capture = import_benchmark(store, benchmark.model_dump_json().encode(), raw, allowed_codes, allowed_hosts, supporting)
                results.append({'code':code, 'status':'ok' if str(benchmark.valuation_date)==reference_date else 'date_mismatch',
                    'valuation_date':str(benchmark.valuation_date), 'equity_count':len(benchmark.holdings), 'ref':capture['ref']})
            except (ValueError, KeyError, TypeError, ArithmeticError) as error:
                # No stale-success fallback; next candidate must see this failure.
                reason=str(error)
                if not re.fullmatch(r'(?:issuer|anonymous|unsupported|unknown_security|complete_equity|suspiciously|invalid_equity|mixed_issuer)_[a-z_0-9]{1,100}',reason):reason='official_issuer_collection_failed'
                capture = store.capture('ETF:'+code, error=reason)
                results.append({'code':code, 'status':'error', 'error':capture['error']})
        store.capture('issuer-collection:'+issuer, encoded({'reference_date':reference_date,'pcf_date':pcf_date,
            'results':[r for r in results if r['code'] in codes]}))
    return results
