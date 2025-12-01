from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.repair_entry import RepairEntryCreate, RepairEntryOut
from app.crud.repair_entry import (
    create_repair_entry,
    list_repairs_for_service_request,
)

router = APIRouter(tags=["Repair History"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=RepairEntryOut, status_code=201)
def create(r: RepairEntryCreate, db: Session = Depends(get_db)):
    return create_repair_entry(db, r)


@router.get("/service_request/{sr_id}", response_model=list[RepairEntryOut])
def list_for_request(sr_id: int, db: Session = Depends(get_db)):
    return list_repairs_for_service_request(db, sr_id)
