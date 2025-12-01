from pydantic import BaseModel, Field
from typing import Optional

class VehicleCreate(BaseModel):
    customer_id: int
    vin: str = Field(..., max_length=50)
    registration: Optional[str]
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    color: Optional[str]

class VehicleOut(VehicleCreate):
    id: int

    class Config:
        orm_mode = True
