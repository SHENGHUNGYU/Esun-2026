from datetime import datetime, date
from typing import Literal
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

TAIPEI = ZoneInfo('Asia/Taipei')

def now() -> str:
    return datetime.now(TAIPEI).isoformat()

def instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('Timestamp must include timezone')
    return parsed

class Source(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    id: str
    url: str
    provider: Literal['TWSE', 'TPEx', 'CNA', 'FinMind']
    branch: Literal['market', 'fundamentals', 'events']
    kind: str
    enabled: bool = False
    fields: list[str] = []
    dataset: str | None = None

class RunRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    run_id: str = Field(pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$')
    cutoff_at: str
    as_of: date  # Explicit expected market-data date, never inferred from stale payloads.
    universe_hash: str
    registry_hash: str
    code_hash: str
    model: str | None = None
    model_url: str | None = None

    @field_validator('cutoff_at')
    @classmethod
    def timestamp(cls, v):
        instant(v)
        return v

    @model_validator(mode='after')
    def coherent(self):
        if self.as_of > instant(self.cutoff_at).astimezone(TAIPEI).date():
            raise ValueError('Expected market date must not follow cutoff')
        return self

class Claim(BaseModel):
    model_config = ConfigDict(extra='forbid')
    kind: Literal['hypothesis', 'uncertainty']
    statement: str = Field(min_length=1, max_length=500)
    observation_ids: list[str] = Field(min_length=1, max_length=8)

class Analysis(BaseModel):
    model_config = ConfigDict(extra='forbid')
    claims: list[Claim] = Field(max_length=12)

