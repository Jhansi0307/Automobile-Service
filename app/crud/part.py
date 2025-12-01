from sqlalchemy.orm import Session
from app.models.part import Part
from app.schemas.part import PartCreate

def create_part(db: Session, p: PartCreate):
    obj = Part(**p.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_parts(db: Session):
    return db.query(Part).all()

def get_part(db: Session, part_id: int):
    return db.query(Part).filter(Part.id == part_id).first()

def update_part_stock(db: Session, part_id: int, qty: int):
    obj = get_part(db, part_id)
    if not obj:
        return None
    obj.stock_qty = qty
    db.commit()
    db.refresh(obj)
    return obj

def delete_part(db: Session, part_id: int):
    obj = get_part(db, part_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
