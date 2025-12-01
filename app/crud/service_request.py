from sqlalchemy.orm import Session
from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate

def create_service_request(db: Session, sr: ServiceRequestCreate):
    obj = ServiceRequest(**sr.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_service_requests(db: Session):
    return db.query(ServiceRequest).all()

def get_service_request(db: Session, sr_id: int):
    return db.query(ServiceRequest).filter(ServiceRequest.id == sr_id).first()

def update_service_request_status(db: Session, sr_id: int, status: str):
    obj = get_service_request(db, sr_id)
    if not obj:
        return None
    obj.status = status
    db.commit()
    db.refresh(obj)
    return obj

def delete_service_request(db: Session, sr_id: int):
    obj = get_service_request(db, sr_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
