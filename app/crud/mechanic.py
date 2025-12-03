from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from app.models.mechanic import Mechanic
from app.schemas.mechanic import MechanicCreate



# CREATE MECHANIC

def create_mechanic(db: Session, m: MechanicCreate):
    obj = Mechanic(**m.dict())

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A mechanic with similar details already exists."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while creating mechanic."
        )



# LIST MECHANICS

def list_mechanics(db: Session):
    try:
        return db.query(Mechanic).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving mechanics."
        )



# GET SINGLE MECHANIC

def get_mechanic(db: Session, mechanic_id: int):
    try:
        return db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving mechanic."
        )



# DELETE MECHANIC

def delete_mechanic(db: Session, mechanic_id: int):
    obj = get_mechanic(db, mechanic_id)
    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Mechanic not found."
        )

    try:
        db.delete(obj)
        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error occurred while deleting mechanic."
        )
