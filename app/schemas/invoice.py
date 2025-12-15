from pydantic import (
    BaseModel,
    Field,
    StrictInt,
    StrictFloat,
    field_validator,
    model_validator,
    ConfigDict,
)
from typing import Optional, Union
from datetime import date
import re

from app.core.config import ALLOWED_CURRENCIES, now_date


class InvoiceCreate(BaseModel):
    invoice_id: str
    name: str = Field(..., max_length=50)
    issue_date: date
    due_date: date
    currency: str
    labor_cost: Union[StrictInt, StrictFloat]
    parts_cost: Union[StrictInt, StrictFloat]
    total_cost: Optional[Union[StrictInt, StrictFloat]] = None
    notes: Optional[str] = None

    # ---------- Field Validators ----------

    @field_validator("invoice_id")
    @classmethod
    def invoice_format(cls, v: str):
        if not re.fullmatch(r"INV-\d{5}", v):
            raise ValueError("Invoice ID must be in format INV-12345")
        return v

    @field_validator("name")
    @classmethod
    def name_alpha(cls, v: str):
        if not re.fullmatch(r"[A-Za-z ]{1,50}", v):
            raise ValueError("Name must be alphabetic and <= 50 chars")
        return v.strip()

    @field_validator("issue_date")
    @classmethod
    def issue_date_not_future(cls, v: date):
        if v > now_date():
            raise ValueError("Issue date must be today or earlier")
        return v

    @field_validator("due_date")
    @classmethod
    def due_date_not_past(cls, v: date):
        if v < date.today():
            raise ValueError("Due date must be today or later")
        return v

    @field_validator("currency")
    @classmethod
    def currency_allowed(cls, v: str):
        v = v.upper()
        if len(v) != 3 or v not in ALLOWED_CURRENCIES:
            raise ValueError(f"Currency must be one of {ALLOWED_CURRENCIES}")
        return v

    @field_validator("labor_cost", "parts_cost", "total_cost", mode="before")
    @classmethod
    def numeric_values(cls, v):
        if v is None:
            return v
        if not isinstance(v, (int, float)):
            raise ValueError("Value must be numeric")
        return v

    @field_validator("labor_cost")
    @classmethod
    def labor_cost_range(cls, v):
        if not 0 <= v <= 50_000:
            raise ValueError("Labor cost must be between 0 and 50,000")
        return v

    @field_validator("parts_cost")
    @classmethod
    def parts_cost_range(cls, v):
        if not 0 <= v <= 200_000:
            raise ValueError("Parts cost must be between 0 and 200,000")
        return v

    # ---------- Model Validator (replacement for root_validator) ----------

    @model_validator(mode="after")
    def validate_total_cost(self):
        if self.total_cost is None:
            return self

        expected = self.labor_cost + self.parts_cost
        if abs(self.total_cost - expected) > 0.01:
            raise ValueError(
                f"Total cost must be labor_cost + parts_cost "
                f"({self.labor_cost} + {self.parts_cost} = {expected})"
            )
        return self
class InvoiceOut(BaseModel):
    id: int
    invoice_id: str
    name: str
    issue_date: date
    due_date: date
    currency: str
    labor_cost: StrictFloat
    parts_cost: StrictFloat
    total_cost: StrictFloat
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_total_cost(self):
        expected = self.labor_cost + self.parts_cost
        if abs(self.total_cost - expected) > 0.01:
            raise ValueError(
                f"Total cost must be labor_cost + parts_cost "
                f"({self.labor_cost} + {self.parts_cost} = {expected})"
            )
        return self
