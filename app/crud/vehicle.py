from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from app.models.vehicle import Vehicle
from app.models.customer import Customer
from app.schemas.vehicle import VehicleCreate

# CREATE VEHICLE

def create_vehicle(db: Session, v: VehicleCreate):

    # Validate FK
    cust = db.query(Customer).filter(Customer.id == v.customer_id).first()
    if not cust:
        raise HTTPException(404, "Customer ID does not exist.")

    obj = Vehicle(**v.dict())

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Vehicle with same VIN already exists.")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Database error creating vehicle.")



# LIST VEHICLES

def list_vehicles(db: Session):
    try:
        return db.query(Vehicle).all()
    except SQLAlchemyError:
        raise HTTPException(500, "Error fetching vehicles.")



# GET VEHICLE

def get_vehicle(db: Session, vehicle_id: int):
    try:
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    except SQLAlchemyError:
        raise HTTPException(500, "Error retrieving vehicle.")



# DELETE VEHICLE

def delete_vehicle(db: Session, vehicle_id: int):
    obj = get_vehicle(db, vehicle_id)
    if not obj:
        raise HTTPException(404, "Vehicle not found.")

    try:
        db.delete(obj)
        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Error deleting vehicle.")
