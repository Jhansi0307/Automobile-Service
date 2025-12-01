from pydantic import BaseModel, Field
from typing import Optional

class MechanicCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    phone: Optional[str]
    notes: Optional[str]

class MechanicOut(MechanicCreate):
    id: int

    class Config:
        orm_mode = True
