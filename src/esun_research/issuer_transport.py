"""Standalone, read-only issuer worker (stdlib only, also runs over SSH).

Only observed public page requests are allowed. Anonymous page cookies stay in
memory and never enter the returned records, metadata or error messages.
"""
import base64
import http.cookiejar
import json
import sys
import time
from datetime import date, datetime, timezone
from urllib.error import HTTPError
from urllib.parse import urlencode, unquote
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPRedirectHandler

SUPPORTED = {
    'nomura': ('00980A', '00985A', '00999A'),
    'allianz': ('00984A', '00993A', '00402A'),
    'ctbc': ('00983A', '00995A', '00406A'),
    'capital': ('00982A', '00992A'),
}

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch(issuer, reference_date, pcf_date):
    if issuer not in SUPPORTED:
        raise ValueError('unsupported_issuer')
    date.fromisoformat(reference_date); date.fromisoformat(pcf_date)
    cookies = http.cookiejar.CookieJar()
    client = build_opener(HTTPCookieProcessor(cookies), NoRedirect())
    records = []
    last = 0.0

    def request(url, fields=None, *, query=None, headers=None, label=None):
        nonlocal last
        time.sleep(max(0, 1 - (time.monotonic() - last)))
        last = time.monotonic()
        target = url + ('?' + urlencode(query) if query else '')
        body = json.dumps(fields).encode() if fields is not None else None
        req = Request(target, body, headers={
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'EsunResearch/0.1 (public holdings; read-only)',
            **(headers or {}),
        })
        try:
            with client.open(req, timeout=20) as response:
                raw = response.read(25_000_001)
        except HTTPError as error:
            raise ValueError('issuer_http_' + str(error.code)) from None
        if len(raw) > 25_000_000:
            raise ValueError('issuer_response_too_large')
        value = json.loads(raw)
        if label:
            def credentials(item):
                if isinstance(item, dict):
                    return any(str(k).lower() in {'token','access_token','refresh_token','authorization','cookie','password'} or credentials(v) for k,v in item.items())
                return isinstance(item, list) and any(credentials(v) for v in item)
            if credentials(value):
                raise ValueError('issuer_unexpected_credential_field')
            # Session fields and query strings deliberately excluded.
            public_fields = {k:v for k,v in (fields or {}).items() if k != 'token'}
            records.append({'label': label, 'url': url,
                'method': 'POST' if body is not None else 'GET',
                'request': public_fields, 'fetched_at': datetime.now(timezone.utc).isoformat(),
                'raw_base64': base64.b64encode(raw).decode()})
        return value

    if issuer == 'nomura':
        url = 'https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundAssets'
        for code in SUPPORTED[issuer]:
            request(url, {'FundID':code, 'SearchDate':reference_date}, label=code)
    elif issuer == 'allianz':
        base = 'https://etf.allianzgi.com.tw/webapi/api/'
        request(base + 'AntiForgery/GetAntiForgeryToken')
        xsrf = [c.value for c in cookies if c.name == 'X-XSRF-TOKEN']
        if len(xsrf) != 1:
            raise ValueError('anonymous_page_context_missing')
        headers = {'X-XSRF-TOKEN':unquote(xsrf[0]), 'Origin':'https://etf.allianzgi.com.tw',
            'Referer':'https://etf.allianzgi.com.tw/instant-estimated'}
        overview = request(base + 'Fund/GetFundOverview',
            {'Keyword':'','FundNo':'','FundType':-1,'PageSize':999,'PageIndex':1},
            headers=headers, label='identity')
        if overview.get('StatusCode') != 0:
            raise ValueError('issuer_identity_failed')
        for code in SUPPORTED[issuer]:
            matches = [r for r in overview['Entries'] if r['CSecuritiesCode'] == code]
            if len(matches) != 1:
                raise ValueError('issuer_identity_not_unique')
            request(base + 'Fund/GetFundAssets', {'FundID':matches[0]['CFundNo']},
                headers=headers, label=code)
    elif issuer == 'ctbc':
        base = 'https://www.ctbcinvestments.com.tw/API/'
        auth = request(base + 'home/AuthToken', {'token':''}, query={'token':''})
        if auth.get('ResultCode') != 0:
            raise ValueError('anonymous_page_context_missing')
        session = auth['Data']['token']
        def post(path, fields, label):
            return request(base + path, {'token':session, **fields}, query={'token':session}, label=label)
        overview = post('etf/ETFCNOList', {}, 'identity')
        if overview.get('ResultCode') != 0:
            raise ValueError('issuer_identity_failed')
        for code in SUPPORTED[issuer]:
            matches = [r for r in overview['Data']['List'] if r['ETF_ID'] == code]
            if len(matches) != 1:
                raise ValueError('issuer_identity_not_unique')
            post('etf/Buyback', {'FID':matches[0]['FID'], 'StartDate':pcf_date}, code)
    elif issuer == 'capital':
        base = 'https://www.capitalfund.com.tw/CFWeb/api/etf/'
        for code, fund in [('00982A','399'), ('00992A','500')]:
            request(base + 'basic/' + fund, label=code+'-identity')
            request(base + 'buyback', {'fundId':fund, 'date':None}, label=code)
    return records

def main():
    try:
        result = {'records':fetch(*sys.argv[1:]), 'error':None}
    except Exception as error:
        # urllib errors may contain a session URL. Never serialize their text.
        safe = str(error) if isinstance(error, ValueError) and str(error).startswith(('issuer_', 'anonymous_', 'unsupported_')) else 'issuer_transport_failed'
        result = {'records':[], 'error':safe}
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
