from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from app.models.part import Part
from app.schemas.part import PartCreate



# CREATE PART

def create_part(db: Session, p: PartCreate):
    obj = Part(**p.dict())
    
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Part with same SKU already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Database error while creating part.")



# LIST ALL PARTS

def list_parts(db: Session):
    try:
        return db.query(Part).all()
    except SQLAlchemyError:
        raise HTTPException(500, "Database error while fetching parts.")



# GET ONE PART

def get_part(db: Session, part_id: int):
    try:
        return db.query(Part).filter(Part.id == part_id).first()
    except SQLAlchemyError:
        raise HTTPException(500, "Database error while retrieving part.")



# UPDATE STOCK

def update_part_stock(db: Session, part_id: int, qty: int):
    obj = get_part(db, part_id)
    if not obj:
        raise HTTPException(404, "Part not found.")

    try:
        obj.stock_qty = qty
        db.commit()
        db.refresh(obj)
        return obj
    
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Error updating part stock.")



# DELETE PART

def delete_part(db: Session, part_id: int):
    obj = get_part(db, part_id)
    if not obj:
        raise HTTPException(404, "Part not found.")

    try:
        db.delete(obj)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Error deleting part.")
