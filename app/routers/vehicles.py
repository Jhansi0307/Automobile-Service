from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.vehicle import VehicleCreate, VehicleOut
from app.crud.vehicle import (
    create_vehicle,
    list_vehicles,
    get_vehicle,
    delete_vehicle,
)
from app.crud.customer import get_customer   # ← REQUIRED IMPORT

router = APIRouter(tags=["Vehicles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  Validate customer_id before creating vehicle
@router.post("/", response_model=VehicleOut, status_code=201)
def create(v: VehicleCreate, db: Session = Depends(get_db)):

    # ❗ Check if customer exists before inserting vehicle
    customer = get_customer(db, v.customer_id)
    if not customer:
        raise HTTPException(
            status_code=400,
            detail=f"Customer with id={v.customer_id} does not exist. Please provide a valid customer_id."
        )

    return create_vehicle(db, v)


@router.get("/", response_model=list[VehicleOut])
def list_all(db: Session = Depends(get_db)):
    return list_vehicles(db)


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_one(vehicle_id: int, db: Session = Depends(get_db)):
    obj = get_vehicle(db, vehicle_id)
    if not obj:
        raise HTTPException(404, "Vehicle not found")
    return obj


@router.delete("/{vehicle_id}")
def delete(vehicle_id: int, db: Session = Depends(get_db)):
    ok = delete_vehicle(db, vehicle_id)
    if not ok:
        raise HTTPException(404, "Vehicle not found")
    return {"message": "Vehicle deleted"}