from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    vin = Column(String(50), index=True, unique=True)
    registration = Column(String(50))
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    color = Column(String(50))
    customer = relationship("Customer", back_populates="vehicles")
