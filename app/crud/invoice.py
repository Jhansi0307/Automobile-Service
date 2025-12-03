from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate



# CREATE INVOICE

def create_invoice(db: Session, inv: InvoiceCreate):
    total_cost = inv.labor_cost + inv.parts_cost

    obj = Invoice(
        invoice_id=inv.invoice_id,
        name=inv.name,
        issue_date=inv.issue_date,
        due_date=inv.due_date,
        currency=inv.currency,
        labor_cost=inv.labor_cost,
        parts_cost=inv.parts_cost,
        total_cost=total_cost,
        notes=inv.notes
    )

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,  
            detail=f"Invoice ID '{inv.invoice_id}' already exists. Use a unique ID."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while creating invoice."
        )



# LIST INVOICES

def list_invoices(db: Session):
    try:
        return db.query(Invoice).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving invoices."
        )



# GET ONE INVOICE

def get_invoice(db: Session, id: int):
    try:
        return db.query(Invoice).filter(Invoice.id == id).first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while retrieving invoice."
        )



# DELETE INVOICE

def delete_invoice(db: Session, id: int):
    obj = get_invoice(db, id)
    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found."
        )

    try:
        db.delete(obj)
        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error occurred while deleting invoice."
        )
