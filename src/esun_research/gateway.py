"""Bounded read-only transport. Secrets never appear in query strings or logs."""
import os
import time
import signal
import subprocess
import shlex
from urllib.parse import urlparse
import httpx
from .store import Store
from .contracts import Source

HOSTS = {'openapi.twse.com.tw','www.tpex.org.tw','feeds.feedburner.com','api.finmindtrade.com'}

class Gateway:
    def __init__(self, client=None, sleep=time.sleep, timeout=20, interval=1.0):
        self.client = client or httpx.Client(timeout=timeout, follow_redirects=False)
        self.sleep = sleep
        self.interval = interval
        self.last = {}

    def close(self):
        self.client.close()

    def get(self, source: Source, params=None):
        from .event_transport import REPORTS
        if source.id in REPORTS:
            from .exchange_events import download
            return download(source)
        parsed = urlparse(source.url)
        if parsed.scheme!='https' or parsed.hostname not in HOSTS or parsed.query or parsed.username:
            return None, 'url_not_allowed'
        headers={'User-Agent':'EsunResearch/0.1 (read-only; single-host throttled)'}
        if source.provider=='FinMind':
            token=os.getenv('FINMIND_TOKEN')
            if not token:
                return None, 'finmind_token_not_configured'
            headers['Authorization']='Bearer '+token
        for attempt in range(3):
            wait=max(0,self.interval-(time.monotonic()-self.last.get(parsed.hostname,0)))
            self.sleep(wait)
            self.last[parsed.hostname]=time.monotonic()
            try:
                response=self.client.get(source.url,params=params,headers=headers)
                if response.status_code==200:
                    if len(response.content)>25_000_000:
                        return None,'response_too_large'
                    if source.provider=='FinMind':
                        try:
                            value=response.json()
                        except ValueError:
                            return response.content,'invalid_json'
                        if value.get('status')!=200:
                            return response.content,'finmind_body_status_'+str(value.get('status'))
                    return response.content,None
                error='http_'+str(response.status_code)
                retry=response.status_code in {429,500,502,503,504}
                retry_after=response.headers.get('Retry-After','')
                if retry_after:
                    try: delay=float(retry_after)
                    except ValueError: return None,'retry_after_requires_later_run'
                    if delay>30: return None,'retry_after_requires_later_run'
                else: delay=2**attempt
            except (httpx.TimeoutException,httpx.NetworkError):
                error='temporary_network_error';retry=True;delay=2**attempt
            if not retry or attempt==2:
                return None,error
            self.sleep(max(0,delay))

class RemoteGateway:
    """Public read-only downloads through a user-authorized SSH host."""
    ALLOWED_HOSTS={'192.168.157.165','192.168.157.161','192.168.157.169',
        '192.168.157.124','120.107.172.133','192.168.157.135'}

    def __init__(self,host):
        if host not in self.ALLOWED_HOSTS:raise ValueError('SSH host not in project inventory')
        self.host=host

    def close(self):
        pass

    def get(self,source,params=None):
        from .event_transport import REPORTS
        if source.id in REPORTS:
            from .exchange_events import download
            return download(source,self.host)
        parsed=urlparse(source.url)
        if source.provider=='FinMind' or params:return None,'remote_private_provider_or_params_not_supported'
        if parsed.scheme!='https' or parsed.hostname not in HOSTS or parsed.query or parsed.username:
            return None,'url_not_allowed'
        command=shlex.join(['curl','--silent','--show-error','--fail','--max-time','60','--max-filesize','25000000',source.url])
        try:
            p=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
                '-o','ConnectTimeout=8','-o','ConnectionAttempts=1','nelson@'+self.host,command],
                capture_output=True,timeout=70)
        except subprocess.TimeoutExpired:return None,'remote_download_timeout'
        if p.returncode:return None,'remote_download_exit_'+str(p.returncode)
        if len(p.stdout)>25_000_000:return None,'response_too_large'
        # Throttle the host even when the next source uses the same endpoint domain.
        time.sleep(1)
        return p.stdout,None

def ingest(store: Store, sources: list[Source], gateway: Gateway, params=None):
    result=[]
    def expired(signum, frame):
        raise TimeoutError('source_deadline')
    for s in sources:
        previous=signal.signal(signal.SIGALRM,expired)
        signal.setitimer(signal.ITIMER_REAL,75)
        try:
            body,error=gateway.get(s,(params or {}).get(s.id))
        except TimeoutError:
            body,error=None,'source_deadline_exceeded'
        finally:
            signal.setitimer(signal.ITIMER_REAL,0)
            signal.signal(signal.SIGALRM,previous)
        # Timestamp after download: first availability cannot predate completion.
        result.append(store.capture(s.id,body,error))
    return result
