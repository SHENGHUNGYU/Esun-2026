import json
from pathlib import Path
import pytest
from esun_research.deliverables import StrategyDescription,strategy_pdf
ROOT=Path(__file__).resolve().parents[1]

def test_strategy_character_limits_and_portable_deterministic_pdf():
    data=json.loads((ROOT/'config/strategy-description.json').read_bytes());description=StrategyDescription.model_validate(data)
    assert description.etf_name.startswith('主動') and 100<=len(description.philosophy)<=300
    first=strategy_pdf(data);second=strategy_pdf(data)
    assert first==second and first.startswith(b'%PDF') and b'/FontFile2' in first
    with pytest.raises(ValueError):StrategyDescription.model_validate({**data,'etf_name':'ETF123'})
    with pytest.raises(ValueError):StrategyDescription.model_validate({**data,'philosophy':'太短'})
