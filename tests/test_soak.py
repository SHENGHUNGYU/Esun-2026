import importlib.util
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location('soak',Path(__file__).resolve().parents[1]/'scripts/soak_check.py')
soak=importlib.util.module_from_spec(spec);spec.loader.exec_module(soak)

def test_only_continuously_observed_healthy_time_counts():
    state=dict(samples=0,failed_samples=0,application_restarts=0,monitored_seconds=0.,healthy_seconds=0.,longest_healthy_seconds=0.,previous_healthy=False)
    healthy={'healthy':True,'application_boot':'a'}
    state=soak.advance(state,healthy,1,60);assert state['healthy_seconds']==0
    state=soak.advance(state,healthy,60,60);assert state['healthy_seconds']==60
    state=soak.advance(state,{'healthy':False},60,60);assert state['healthy_seconds']==0 and state['failed_samples']==1
    state=soak.advance(state,healthy,60,60);assert state['healthy_seconds']==0
    state=soak.advance(state,healthy,60,60);assert state['healthy_seconds']==60
    state=soak.advance(state,{'healthy':True,'application_boot':'b'},60,60)
    assert state['healthy_seconds']==0 and state['application_restarts']==1
    state=soak.advance(state,healthy,500,60);assert state['healthy_seconds']==0 and state['longest_healthy_seconds']==60

@pytest.mark.parametrize('value',['https://external.test','http://127.0.0.1@external.test','http://user:secret@localhost','http://localhost/?token=x'])
def test_monitor_cannot_send_health_requests_to_external_origins(value):
    with pytest.raises(ValueError):soak.local_url(value)
