import csv, io
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut

router=APIRouter(prefix="/transactions", tags=["Transactions"])
@router.get("", response_model=list[TransactionOut])
def list_transactions(user_id="demo-user", db:Session=Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id==user_id).order_by(Transaction.date.desc()).all()
@router.post("", response_model=TransactionOut)
def create_transaction(payload:TransactionCreate, db:Session=Depends(get_db)):
    row=Transaction(**payload.model_dump()); db.add(row); db.commit(); db.refresh(row); return row
@router.post("/import-csv")
def import_csv(file:UploadFile=File(...), user_id="demo-user", db:Session=Depends(get_db)):
    if not file.filename.lower().endswith('.csv'): raise HTTPException(400,'CSV file required')
    raw=file.file.read().decode('utf-8-sig'); reader=csv.DictReader(io.StringIO(raw)); count=0
    for item in reader:
        try:
            row=Transaction(user_id=user_id,date=item['date'],description=item['description'],category=item['category'],amount=float(item['amount']),type=item['type'].lower())
            db.add(row); count+=1
        except (KeyError,ValueError): continue
    db.commit(); return {"imported":count}
