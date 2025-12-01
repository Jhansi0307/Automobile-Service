from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.customer import CustomerCreate, CustomerOut
from app.crud.customer import (
    create_customer,
    list_customers,
    get_customer,
    delete_customer,
)

router = APIRouter(tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CustomerOut, status_code=201)
def create(c: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, c)


@router.get("/", response_model=list[CustomerOut])
def list_all(db: Session = Depends(get_db)):
    return list_customers(db)


@router.get("/{customer_id}", response_model=CustomerOut)
def get_one(customer_id: int, db: Session = Depends(get_db)):
    obj = get_customer(db, customer_id)
    if not obj:
        raise HTTPException(404, "Customer not found")
    return obj


@router.delete("/{customer_id}")
def delete(customer_id: int, db: Session = Depends(get_db)):
    ok = delete_customer(db, customer_id)
    if not ok:
        raise HTTPException(404, "Customer not found")
    return {"message": "Customer deleted"}
