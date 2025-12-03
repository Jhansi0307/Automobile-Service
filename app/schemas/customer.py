from pydantic import BaseModel, Field
from typing import Optional

# CREATE SCHEMA (input only)
class CustomerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


# OUTPUT SCHEMA (NO VALIDATION)
class CustomerOut(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True
