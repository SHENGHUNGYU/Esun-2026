from types import SimpleNamespace
from esun_research.gateway import RemoteGateway
from esun_research.contracts import Source


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
