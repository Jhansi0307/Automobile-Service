from fastapi import FastAPI

from app.core.database import init_db
from app.core.database import SessionLocal

# Import all routers (updated paths)
from app.routers import (
    customers,
    vehicles,
    mechanics,
    parts,
    service_requests,
    repair_entries,
    invoices,
)

# Import all models so SQLAlchemy knows them and can create tables
from app.models.customer import Customer
from app.models.vehicle import Vehicle
from app.models.mechanic import Mechanic
from app.models.part import Part
from app.models.service_request import ServiceRequest
from app.models.repair_entry import RepairEntry
from app.models.invoice import Invoice
    
# FastAPI App
app = FastAPI(
    title="Automobile Service Management API",
    description="""
A complete backend system for managing automobile service operations, including:

- **Customer Management**
- **Vehicle Management**
- **Service Requests**
- **Mechanics**
- **Inventory / Parts**
- **Repair History**
- **Billing / Invoices**

""",
    version="1.0.0"
)

init_db()
# ==========================
# ROUTER REGISTRATIONS
# ==========================
app.include_router(
    service_requests.router,
    prefix="/api/service_requests",
    tags=["Service Requests"]
)
app.include_router(
    invoices.router,
    prefix="/api/invoices",
    tags=["Invoices"]
)

app.include_router(
    customers.router,
    prefix="/api/customers",
    tags=["Customers"]
)

app.include_router(
    vehicles.router,
    prefix="/api/vehicles",
    tags=["Vehicles"]
)

app.include_router(
    mechanics.router,
    prefix="/api/mechanics",
    tags=["Mechanics"]
)

app.include_router(
    parts.router,
    prefix="/api/parts",
    tags=["Parts / Inventory"]
)


app.include_router(
    repair_entries.router,
    prefix="/api/repair_entries",
    tags=["Repair History"]
)
    


# ==========================
# ROOT HEALTH CHECK
# ==========================

@app.get("/")
def root():
    return {"message": "Automobile Service API is running successfully!"}
