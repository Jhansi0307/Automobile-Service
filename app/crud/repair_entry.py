from sqlalchemy.orm import Session
from app.models.repair_entry import RepairEntry
from app.models.service_request import ServiceRequest
from app.schemas.repair_entry import RepairEntryCreate
from datetime import date

def create_repair_entry(db: Session, r: RepairEntryCreate):
    obj = RepairEntry(
        service_request_id=r.service_request_id,
        note=r.note,
        labor_hours=r.labor_hours,
        created_at=date.today()
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_repairs_for_service_request(db: Session, sr_id: int):
    return db.query(RepairEntry).filter(RepairEntry.service_request_id == sr_id).all()
