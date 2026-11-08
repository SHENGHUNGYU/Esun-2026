from types import SimpleNamespace
from esun_research.gateway import RemoteGateway
from esun_research.contracts import Source
from esun_research.gateway import Gateway,official_payload_error,ingest
from esun_research.store import Store
import httpx

BLOCK=b'<html>FOR SECURITY REASONS, THIS PAGE CAN NOT BE ACCESSED.</html>'

def test_http_200_block_page_is_retried_and_never_captured_as_success(tmp_path,monkeypatch):
    s=source().model_copy(update={'id':'TWSE-108','provider':'TWSE','url':'https://openapi.twse.com.tw/v1/announcement/punish'})
    calls=[]
    def respond(request):calls.append(request);return httpx.Response(200,content=BLOCK)
    gateway=Gateway(httpx.Client(transport=httpx.MockTransport(respond)),sleep=lambda _:None)
    store=Store(tmp_path);result=ingest(store,[s],gateway)[0]
    assert len(calls)==2 and result['status']=='error' and result['error']=='official_security_block_page'
    assert store.read(result['ref'])==BLOCK
    monkeypatch.setattr('esun_research.gateway.time.sleep',lambda _:None)
    replies=iter([SimpleNamespace(returncode=0,stderr=b'',stdout=BLOCK),SimpleNamespace(returncode=0,stderr=b'',stdout=b'[]')])
    monkeypatch.setattr('esun_research.gateway.subprocess.run',lambda *a,**k:next(replies))
    assert RemoteGateway('120.107.172.133').get(s)==(b'[]',None)
    monkeypatch.setattr('esun_research.gateway.subprocess.run',lambda *a,**k:SimpleNamespace(returncode=0,stderr=b'',stdout=BLOCK))
    assert RemoteGateway('120.107.172.133').get(s)==(BLOCK,'official_security_block_page')

def test_official_json_empty_is_valid_but_error_objects_and_malformed_bodies_are_not():
    assert official_payload_error(source(),b'[]') is None
    assert official_payload_error(source(),b'{"error":"busy"}')=='official_expected_json_array'
    assert official_payload_error(source(),b'<html>unavailable</html>')=='official_invalid_json_response'


def source():return Source(id='TPEx-004',url='https://www.tpex.org.tw/openapi/v1/tpex_spendi_history',provider='TPEx',branch='market',kind='raw',enabled=True,fields=[])


def test_transient_ssh_failure_retries_once(monkeypatch):
    calls=[]
    def run(*args,**kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=255 if len(calls)==1 else 0,stderr=b'Connection reset by peer',stdout=b'[]')
    monkeypatch.setattr('esun_research.gateway.subprocess.run',run)
    monkeypatch.setattr('esun_research.gateway.time.sleep',lambda _:None)
    assert RemoteGateway('120.107.172.133').get(source())==(b'[]',None)
    assert len(calls)==2


def test_authentication_failure_does_not_retry(monkeypatch):
    calls=[]
    def run(*args,**kwargs):
        calls.append(args);return SimpleNamespace(returncode=255,stderr=b'Host key verification failed.',stdout=b'')
    monkeypatch.setattr('esun_research.gateway.subprocess.run',run)
    assert RemoteGateway('120.107.172.133').get(source())==(None,'remote_ssh_auth_or_host_key_failed')
    assert len(calls)==1


def test_connection_retries_are_bounded(monkeypatch):
    calls=[]
    def run(*args,**kwargs):
        calls.append(args);return SimpleNamespace(returncode=255,stderr=b'Connection reset',stdout=b'')
    monkeypatch.setattr('esun_research.gateway.subprocess.run',run)
    monkeypatch.setattr('esun_research.gateway.time.sleep',lambda _:None)
    assert RemoteGateway('120.107.172.133').get(source())==(None,'remote_ssh_connection_failed_after_retry')
    assert len(calls)==2
