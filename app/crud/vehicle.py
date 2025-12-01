from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate

def create_vehicle(db: Session, v: VehicleCreate):
    obj = Vehicle(**v.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_vehicles(db: Session):
    return db.query(Vehicle).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

def delete_vehicle(db: Session, vehicle_id: int):
    obj = get_vehicle(db, vehicle_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
