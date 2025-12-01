from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate

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

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_invoices(db: Session):
    return db.query(Invoice).all()

def get_invoice(db: Session, id: int):
    return db.query(Invoice).filter(Invoice.id == id).first()

def delete_invoice(db: Session, id: int):
    obj = get_invoice(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
