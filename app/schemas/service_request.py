from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
import re
from app.core.config import ALLOWED_STATUSES, now_date


# INPUT SCHEMA (validators apply here only)

class ServiceRequestCreate(BaseModel):
    customer_name: Optional[str] = Field(None, max_length=100)
    vehicle_vin: Optional[str] = Field(None, max_length=50)
    mechanic_name: str = Field(..., min_length=3, max_length=50)
    status: str
    priority: int
    status_completion_date: date
    description: Optional[str] = None

    @validator("status")
    def status_must_be_allowed(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {ALLOWED_STATUSES}")
        return v

    @validator("mechanic_name")
    def mechanic_alpha(cls, v):
        if not re.fullmatch(r"[A-Za-z ]{3,50}", v):
            raise ValueError("Mechanic name must be alphabetic and between 3 and 50 chars")
        return v.strip()

    @validator("priority")
    def priority_range(cls, v):
        if not (1 <= v <= 6):
            raise ValueError("Priority must be numeric between 1 and 6")
        return v

    @validator("status_completion_date")
    def completion_date_not_past(cls, v):
        if v < now_date():
            raise ValueError("Status completion date must be today or a future date")
        return v



# OUTPUT SCHEMA (NO VALIDATORS)

class ServiceRequestOut(BaseModel):
    id: int
    customer_name: Optional[str] = None
    vehicle_vin: Optional[str] = None
    mechanic_name: str
    status: str
    priority: int
    status_completion_date: date
    description: Optional[str] = None

    class Config:
        orm_mode = True
