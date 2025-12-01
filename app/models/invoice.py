from sqlalchemy import Column, Integer, String, Date, Float, Text
from app.core.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String(20), unique=True, index=True)
    name = Column(String(50))
    issue_date = Column(Date)
    due_date = Column(Date)
    currency = Column(String(3))
    labor_cost = Column(Float)
    parts_cost = Column(Float)
    total_cost = Column(Float)
    notes = Column(Text)
