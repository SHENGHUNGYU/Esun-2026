from fastapi.testclient import TestClient
from esun_research.application import create_app


def test_maintenance_rejects_writes_and_jobs_but_allows_reads(tmp_path):
    app=create_app(tmp_path,model_config=None);client=TestClient(app)
    assert client.get('/api/health').json()['read_only'] is False
    (tmp_path/'maintenance-readonly.json').write_text('{}')
    assert client.get('/api/health').json()['read_only'] is True
    assert client.get('/api/holdings').status_code==200
    assert client.post('/api/public-context/collect',headers={'x-esun-token':app.state.csrf_token}).status_code==423
    import pytest
    with pytest.raises(ValueError,match='維護'):app.state.jobs.start([],'not-started')
