from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    notes = Column(Text)
