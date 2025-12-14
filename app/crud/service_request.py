from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate
from app.models.repair_entry import RepairEntry


# CREATE SERVICE REQUEST

def create_service_request(db: Session, sr: ServiceRequestCreate):

    obj = ServiceRequest(**sr.dict())

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Database error creating service request.")



# LIST

def list_service_requests(db: Session):
    try:
        return db.query(ServiceRequest).all()
    except SQLAlchemyError:
        raise HTTPException(500, "Error reading service requests.")



# GET ONE

def get_service_request(db: Session, sr_id: int):
    try:
        return db.query(ServiceRequest).filter(ServiceRequest.id == sr_id).first()
    except SQLAlchemyError:
        raise HTTPException(500, "Error retrieving service request.")



# UPDATE STATUS

def update_service_request_status(db: Session, sr_id: int, status: str):
    obj = get_service_request(db, sr_id)
    if not obj:
        raise HTTPException(404, "Service request not found.")

    try:
        obj.status = status
        db.commit()
        db.refresh(obj)
        return obj

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Error updating status.")



# DELETE


def delete_service_request(db: Session, sr_id: int):
    # 1️⃣ Check if Service Request exists
    obj = db.query(ServiceRequest).filter(ServiceRequest.id == sr_id).first()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Service request not found."
        )

    # 2️⃣ Check for dependent repair entries
    has_repairs = (
        db.query(RepairEntry)
        .filter(RepairEntry.service_request_id == sr_id)
        .first()
    )

    if has_repairs:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete service request. Repair entries exist."
        )

    # 3️⃣ Safe delete
    try:
        db.delete(obj)
        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting service request."
        )