from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.mechanic import MechanicCreate, MechanicOut
from app.crud.mechanic import (
    create_mechanic,
    list_mechanics,
    get_mechanic,
    delete_mechanic,
)

router = APIRouter(tags=["Mechanics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MechanicOut, status_code=201)
def create(m: MechanicCreate, db: Session = Depends(get_db)):
    return create_mechanic(db, m)


@router.get("/", response_model=list[MechanicOut])
def list_all(db: Session = Depends(get_db)):
    return list_mechanics(db)


@router.delete("/{mechanic_id}")
def delete(mechanic_id: int, db: Session = Depends(get_db)):
    ok = delete_mechanic(db, mechanic_id)
    if not ok:
        raise HTTPException(404, "Mechanic not found")
    return {"message": "Mechanic deleted"}
