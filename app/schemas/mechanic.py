from pydantic import BaseModel, Field
from typing import Optional


# Create Schema (VALIDATION ONLY)

class MechanicCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    phone: Optional[str] = None
    notes: Optional[str] = None



# Output Schema (NO VALIDATORS)

class MechanicOut(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True
