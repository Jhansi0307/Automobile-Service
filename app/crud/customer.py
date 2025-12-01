from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate

def create_customer(db: Session, c: CustomerCreate):
    obj = Customer(**c.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_customers(db: Session):
    return db.query(Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def delete_customer(db: Session, customer_id: int):
    obj = get_customer(db, customer_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
