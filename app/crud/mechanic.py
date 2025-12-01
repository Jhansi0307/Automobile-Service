from sqlalchemy.orm import Session
from app.models.mechanic import Mechanic
from app.schemas.mechanic import MechanicCreate

def create_mechanic(db: Session, m: MechanicCreate):
    obj = Mechanic(**m.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_mechanics(db: Session):
    return db.query(Mechanic).all()

def get_mechanic(db: Session, mechanic_id: int):
    return db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()

def delete_mechanic(db: Session, mechanic_id: int):
    obj = get_mechanic(db, mechanic_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
