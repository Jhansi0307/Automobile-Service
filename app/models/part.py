from sqlalchemy import Column, Integer, String, Float, Text
from app.core.database import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    unit_cost = Column(Float)
    selling_price = Column(Float)
    stock_qty = Column(Integer, default=0)
    reorder_level = Column(Integer, default=0)
