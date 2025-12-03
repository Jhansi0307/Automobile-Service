from pydantic import BaseModel
from typing import Optional
from datetime import date   

class RepairEntryCreate(BaseModel):
    service_request_id: int
    note: Optional[str] = None
    labor_hours: float = 0.0


class RepairEntryOut(BaseModel):
    id: int
    service_request_id: int
    note: Optional[str] = None
    labor_hours: float
    created_at: date   # <-- correct type

    class Config:
        orm_mode = True
