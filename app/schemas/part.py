from pydantic import BaseModel
from typing import Optional

class PartCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str]
    unit_cost: float = 0.0
    selling_price: float = 0.0
    stock_qty: int = 0
    reorder_level: int = 0

class PartOut(PartCreate):
    id: int

    class Config:
        orm_mode = True
