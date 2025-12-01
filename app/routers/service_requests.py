from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestOut
from app.crud.service_request import (
    create_service_request,
    list_service_requests,
    get_service_request,
    update_service_request_status,
    delete_service_request,
)

router = APIRouter(tags=["Service Requests"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ServiceRequestOut, status_code=201)
def create(sr: ServiceRequestCreate, db: Session = Depends(get_db)):
    return create_service_request(db, sr)


@router.get("/", response_model=list[ServiceRequestOut])
def list_all(db: Session = Depends(get_db)):
    return list_service_requests(db)


@router.get("/{sr_id}", response_model=ServiceRequestOut)
def get_one(sr_id: int, db: Session = Depends(get_db)):
    obj = get_service_request(db, sr_id)
    if not obj:
        raise HTTPException(404, "Service Request not found")
    return obj


@router.put("/{sr_id}/status")
def update_status(sr_id: int, payload: dict, db: Session = Depends(get_db)):
    status = payload.get("status")
    if status not in ("Pending", "In-Progress", "Completed"):
        raise HTTPException(400, "Invalid status")

    updated = update_service_request_status(db, sr_id, status)
    if not updated:
        raise HTTPException(404, "Service Request not found")

    return updated


@router.delete("/{sr_id}")
def delete(sr_id: int, db: Session = Depends(get_db)):
    ok = delete_service_request(db, sr_id)
    if not ok:
        raise HTTPException(404, "Service Request not found")
    return {"message": "Service Request deleted"}
