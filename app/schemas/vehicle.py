from pydantic import BaseModel, Field
from typing import Optional


# INPUT SCHEMA

class VehicleCreate(BaseModel):
    customer_id: int
    vin: str = Field(..., max_length=50)
    registration: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None



# OUTPUT SCHEMA

class VehicleOut(BaseModel):
    id: int
    customer_id: int
    vin: str
    registration: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None

    class Config:
        orm_mode = True