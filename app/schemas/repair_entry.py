from pydantic import BaseModel
from typing import Optional

class RepairEntryCreate(BaseModel):
    service_request_id: int
    note: Optional[str]
    labor_hours: float = 0.0

class RepairEntryOut(RepairEntryCreate):
    id: int

    class Config:
        orm_mode = True
