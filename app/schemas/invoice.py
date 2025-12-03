from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
import re
from app.core.config import ALLOWED_CURRENCIES, now_date

class InvoiceCreate(BaseModel):
    invoice_id: str
    name: str = Field(..., max_length=50)
    issue_date: date
    due_date: date
    currency: str
    labor_cost: float
    parts_cost: float
    notes: Optional[str]

    @validator("invoice_id")
    def invoice_format(cls, v):
        if not re.fullmatch(r"INV-\d{5}", v):
            raise ValueError("Invoice ID must be in format INV-12345")
        return v

    @validator("name")
    def name_alpha(cls, v):
        if not re.fullmatch(r"[A-Za-z ]{1,50}", v):
            raise ValueError("Name must be alphabetic and less than 50 chars")
        return v.strip()

    @validator("issue_date")
    def issue_date_not_future(cls, v):
        today = now_date()
        if v > today:
            raise ValueError("Issue date must be today or earlier")
        return v

    @validator("due_date")
    def due_date_not_past(cls, v):
        today = date.today()
        if v < today:
            raise ValueError("Due date must be today or later")
        return v

    @validator("currency")
    def currency_allowed(cls, v):
        v = v.upper()
        if v not in ALLOWED_CURRENCIES:
            raise ValueError(f"Currency must be one of {ALLOWED_CURRENCIES}")
        return v

    @validator("labor_cost")
    def labor_cost_range(cls, v):
        if not (0 <= v <= 50000):
            raise ValueError("Labor cost must be between 0 and 50,000")
        return v

    @validator("parts_cost")
    def parts_cost_range(cls, v):
        if not (0 <= v <= 200000):
            raise ValueError("Parts cost must be between 0 and 200,000")
        return v

class InvoiceOut(BaseModel):
    id: int
    invoice_id: str
    name: str
    issue_date: date
    due_date: date
    currency: str
    labor_cost: float
    parts_cost: float
    total_cost: float
    notes: Optional[str] = None

    class Config:
        orm_mode = True
