from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from datetime import date

from app.models.repair_entry import RepairEntry
from app.models.service_request import ServiceRequest
from app.schemas.repair_entry import RepairEntryCreate


# CREATE REPAIR ENTRY
def create_repair_entry(db: Session, r: RepairEntryCreate):

    # FK validation
    sr = db.query(ServiceRequest).filter(ServiceRequest.id == r.service_request_id).first()
    if not sr:
        raise HTTPException(404, "Service Request ID does not exist.")

    obj = RepairEntry(
        service_request_id=r.service_request_id,
        note=r.note,
        labor_hours=r.labor_hours,
        created_at=date.today()
    )

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Error creating repair entry.")


# LIST REPAIRS
def list_repairs_for_service_request(db: Session, sr_id: int):
    try:
        return db.query(RepairEntry).filter(RepairEntry.service_request_id == sr_id).all()
    except SQLAlchemyError:
        raise HTTPException(500, "Error fetching repair entries.")
