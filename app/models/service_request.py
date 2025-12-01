from sqlalchemy import Column, Integer, String, Date, Text
from app.core.database import Base

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    vehicle_vin = Column(String(50), index=True)
    mechanic_name = Column(String(50))
    status = Column(String(20), index=True)
    priority = Column(Integer)
    status_completion_date = Column(Date)
    description = Column(Text)
