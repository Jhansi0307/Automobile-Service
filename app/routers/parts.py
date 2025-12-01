from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.part import PartCreate, PartOut
from app.crud.part import (
    create_part,
    list_parts,
    get_part,
    delete_part,
    update_part_stock,
)

router = APIRouter(tags=["Parts / Inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PartOut, status_code=201)
def create(p: PartCreate, db: Session = Depends(get_db)):
    return create_part(db, p)


@router.get("/", response_model=list[PartOut])
def list_all(db: Session = Depends(get_db)):
    return list_parts(db)


@router.put("/{part_id}/stock")
def update_stock(part_id: int, payload: dict, db: Session = Depends(get_db)):
    qty = payload.get("stock_qty")
    if qty is None:
        raise HTTPException(400, "stock_qty is required")

    updated = update_part_stock(db, part_id, qty)
    if not updated:
        raise HTTPException(404, "Part not found")

    return updated


@router.delete("/{part_id}")
def delete(part_id: int, db: Session = Depends(get_db)):
    ok = delete_part(db, part_id)
    if not ok:
        raise HTTPException(404, "Part not found")
    return {"message": "Part deleted"}
