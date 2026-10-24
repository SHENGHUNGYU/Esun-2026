"""Official account input: validate independently from the D-Plan schema."""
import json
from decimal import Decimal
from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from .contracts import instant

class OfficialModel(BaseModel):
    model_config=ConfigDict(extra='allow',allow_inf_nan=False)

class Account(OfficialModel):
    cash: Decimal=Field(ge=0)
    cash_ratio_tradable: Decimal | None
    nav_tradable: Decimal=Field(ge=0)
    aum: Decimal=Field(ge=0)
    receivable_cash: Decimal=Field(ge=0)
    holdings_count: int=Field(ge=0)

class Holding(OfficialModel):
    code: str
    shares: int=Field(ge=0)
    receivable_shares: int=Field(ge=0)
    close_price: Decimal | None=Field(default=None,ge=0)
    tradable_weight: Decimal | None=Field(default=None,ge=0)

class PreviousOrders(OfficialModel):
    outcome: Literal['none','unknown','voided','executed']
    void_reasons: list[str]
    excluded_codes: list[str]

    @model_validator(mode='after')
    def reasons(self):
        if (self.outcome=='voided') != bool(self.void_reasons):
            raise ValueError('void_reasons inconsistent with outcome')
        return self

class Incident(OfficialModel):
    date: date
    check_code: str
    status: Literal['warn','fail']
    message: str

class Compliance(OfficialModel):
    violations: int=Field(ge=0)
    notices: int=Field(ge=0)
    incidents: list[Incident]

class DataPack(OfficialModel):
    schema_version: str
    doc_type: Literal['DataPack']
    team_id: str
    trade_date: date
    as_of_date: date | None
    generated_at: str
    missing: list[str]
    prev_day_orders: PreviousOrders
    account: Account | None
    holdings: list[Holding] | None
    compliance: Compliance

    @field_validator('generated_at')
    @classmethod
    def timestamp(cls,v):
        parsed=instant(v)
        if parsed.utcoffset().total_seconds()!=28800:
            raise ValueError('DataPack timestamp must use +08:00')
        return v

    @model_validator(mode='after')
    def consistency(self):
        pending='prev_settlement' in self.missing
        if pending:
            if self.account is not None or self.holdings is not None or self.as_of_date is not None:
                raise ValueError('Pending settlement must have null account, holdings and as_of_date')
            return self
        if self.account is None or self.holdings is None:
            raise ValueError('Null account/holdings without prev_settlement')
        codes=[h.code for h in self.holdings]
        if len(codes)!=len(set(codes)):
            raise ValueError('Duplicate holding codes')
        if self.account.holdings_count!=sum(h.shares>0 for h in self.holdings):
            raise ValueError('holdings_count must count shares>0')
        if self.as_of_date is not None and self.as_of_date>=self.trade_date:
            raise ValueError('Settlement date must precede trade date')
        if self.as_of_date is None:
            if self.holdings or self.account.holdings_count or self.account.receivable_cash:
                raise ValueError('Initial account must be all cash')
            if not self.account.cash==self.account.nav_tradable==self.account.aum:
                raise ValueError('Initial cash/nav/aum mismatch')
        if 'prev_close' in self.missing and self.account.cash_ratio_tradable is not None:
            raise ValueError('Missing close requires null cash ratio')
        # When all holding prices exist, reconcile the official tradable NAV.
        tradable=[h for h in self.holdings if h.shares>0]
        if all(h.close_price is not None for h in tradable):
            estimated=self.account.cash+sum((h.shares*h.close_price for h in tradable),Decimal(0))
            if abs(estimated-self.account.nav_tradable)>Decimal('0.01'):
                raise ValueError('Official tradable NAV inconsistent with cash and shares')
        return self

    def decision_gate(self):
        if self.schema_version!='3.0':return 'BLOCKED_UNSUPPORTED_DATAPACK_VERSION'
        if self.missing or self.account is None or self.holdings is None:return 'BLOCKED_MISSING_OFFICIAL_INPUT'
        if self.account.nav_tradable<=0:return 'BLOCKED_NONPOSITIVE_NAV'
        if any(h.shares>0 and (h.close_price is None or h.close_price<=0) for h in self.holdings):
            return 'BLOCKED_MISSING_HOLDING_PRICE'
        if self.prev_day_orders.outcome=='unknown':return 'BLOCKED_UNKNOWN_ORDER_OUTCOME'
        if self.as_of_date is None:
            if self.prev_day_orders.outcome!='none':return 'BLOCKED_INITIAL_ORDER_HISTORY'
            return 'INITIAL_CASH_ACCOUNT'
        return 'SETTLED_ACCOUNT'

def load_datapack(body: bytes, team_id: str, trade_date: date):
    # Decimal conversion avoids introducing binary rounding into financial input.
    value=json.loads(body,parse_float=Decimal)
    pack=DataPack.model_validate(value)
    if pack.team_id!=team_id or pack.trade_date!=trade_date:
        raise ValueError('DataPack team or trade date does not match request')
    return pack
