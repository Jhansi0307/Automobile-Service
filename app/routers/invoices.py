from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.invoice import InvoiceCreate, InvoiceOut
from app.crud.invoice import (
    create_invoice,
    list_invoices,
    get_invoice,
    delete_invoice,
)

router = APIRouter(tags=["Invoices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=InvoiceOut, status_code=201)
def create(inv: InvoiceCreate, db: Session = Depends(get_db)):
    return create_invoice(db, inv)


@router.get("/", response_model=list[InvoiceOut])
def list_all(db: Session = Depends(get_db)):
    return list_invoices(db)


@router.get("/{id}", response_model=InvoiceOut)
def get_one(id: int, db: Session = Depends(get_db)):
    obj = get_invoice(db, id)
    if not obj:
        raise HTTPException(404, "Invoice not found")
    return obj


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    ok = delete_invoice(db, id)
    if not ok:
        raise HTTPException(404, "Invoice not found")
    return {"message": "Invoice deleted"}
