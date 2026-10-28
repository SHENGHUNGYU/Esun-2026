import json
from pathlib import Path
from unittest.mock import Mock
import httpx
import pytest
from esun_research.model_connection import ModelConnection
from esun_research.daily import failure_detail
from esun_research.store import Store


def test_model_connection_recovers_authorized_tunnel_without_changing_identity(monkeypatch):
    connection=ModelConnection(Path('config/llm-local.json'),'120.107.172.133')
    check=Mock(side_effect=[httpx.ConnectError('refused'),{'digest':'pinned'}])
    monkeypatch.setattr(connection,'check',check);monkeypatch.setattr('esun_research.model_connection.time.sleep',lambda _:None)
    process=Mock();process.poll.return_value=None
    start=Mock(return_value=process);monkeypatch.setattr('esun_research.model_connection.subprocess.Popen',start)
    assert connection.ensure()=={'digest':'pinned'}
    args=start.call_args.args[0]
    assert 'StrictHostKeyChecking=yes' in args and 'ExitOnForwardFailure=yes' in args
    assert '127.0.0.1:11435:127.0.0.1:11434' in args
    assert args[-1]=='nelson@120.107.172.133'
    process.terminate.assert_not_called()


def test_model_identity_mismatch_does_not_spawn_tunnel(monkeypatch):
    connection=ModelConnection(Path('config/llm-local.json'),'120.107.172.133')
    monkeypatch.setattr(connection,'check',Mock(side_effect=ValueError('model_digest_mismatch')))
    start=Mock();monkeypatch.setattr('esun_research.model_connection.subprocess.Popen',start)
    with pytest.raises(ValueError,match='digest'):connection.ensure()
    start.assert_not_called()


def test_model_failure_ui_exposes_connection_root_cause(tmp_path):
    store=Store(tmp_path);folder=tmp_path/'candidates/test';folder.mkdir(parents=True)
    (folder/'validation.json').write_text(json.dumps({'errors':['agent_model_output_failed']}))
    (folder/'agent-call-evidence.json').write_text(json.dumps([{'completion':None,'error':'ConnectError:Connection refused'}]))
    assert '模型通道未連線' in failure_detail(store,'test',RuntimeError('Command failed'))
