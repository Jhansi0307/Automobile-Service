# from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # CUSTOMER
# class Customer(Base):
#     __tablename__ = "customers"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     phone = Column(String(20))
#     email = Column(String(100))
#     address = Column(Text)

#     vehicles = relationship("Vehicle", back_populates="customer")


# # VEHICLE
# class Vehicle(Base):
#     __tablename__ = "vehicles"

#     id = Column(Integer, primary_key=True, index=True)
#     customer_id = Column(Integer, ForeignKey("customers.id"))
#     vin = Column(String(50), index=True)
#     registration = Column(String(50))
#     make = Column(String(50))
#     model = Column(String(50))
#     year = Column(Integer)
#     color = Column(String(50))

#     customer = relationship("Customer", back_populates="vehicles")


# # MECHANIC
# class Mechanic(Base):
#     __tablename__ = "mechanics"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     phone = Column(String(20))
#     notes = Column(Text)


# # PARTS / INVENTORY
# class Part(Base):
#     __tablename__ = "parts"

#     id = Column(Integer, primary_key=True, index=True)
#     sku = Column(String(50), unique=True, index=True)
#     name = Column(String(100), nullable=False)
#     description = Column(Text)
#     unit_cost = Column(Float)
#     selling_price = Column(Float)
#     stock_qty = Column(Integer, default=0)
#     reorder_level = Column(Integer, default=0)


# # SERVICE REQUESTS
# class ServiceRequest(Base):
#     __tablename__ = "service_requests"

#     id = Column(Integer, primary_key=True, index=True)
#     customer_name = Column(String(100))
#     vehicle_vin = Column(String(50), index=True)
#     mechanic_name = Column(String(50))
#     status = Column(String(20), index=True)
#     priority = Column(Integer)
#     status_completion_date = Column(Date)
#     description = Column(Text)


# # REPAIR ENTRY (History)
# class RepairEntry(Base):
#     __tablename__ = "repair_entries"

#     id = Column(Integer, primary_key=True, index=True)
#     service_request_id = Column(Integer, ForeignKey("service_requests.id"))
#     note = Column(Text)
#     labor_hours = Column(Float)
#     created_at = Column(Date)

#     service_request = relationship("ServiceRequest")


# # INVOICES
# class Invoice(Base):
#     __tablename__ = "invoices"

#     id = Column(Integer, primary_key=True, index=True)
#     invoice_id = Column(String(20), unique=True, index=True)
#     name = Column(String(50))
#     issue_date = Column(Date)
#     due_date = Column(Date)
#     currency = Column(String(3))
#     labor_cost = Column(Float)
#     parts_cost = Column(Float)
#     total_cost = Column(Float)
#     notes = Column(Text)
