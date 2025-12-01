from pydantic import BaseModel, Field
from typing import Optional

class CustomerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]

class CustomerOut(CustomerCreate):
    id: int

    class Config:
        orm_mode = True
