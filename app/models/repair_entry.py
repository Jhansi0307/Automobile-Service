from sqlalchemy import Column, Integer, Text, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.core.database import Base

class RepairEntry(Base):
    __tablename__ = "repair_entries"

    id = Column(Integer, primary_key=True, index=True)
    service_request_id = Column(Integer, ForeignKey("service_requests.id"))
    note = Column(Text)
    labor_hours = Column(Float)
    created_at = Column(Date, default=date.today)

    service_request = relationship("ServiceRequest")
