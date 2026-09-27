from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Transaction
from app.services.budget_service import recommendation
from app.services.anomaly_service import detect
from app.services.forecast_service import forecast
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/summary")
def summary(user_id="demo-user",monthly_income:float=0,db:Session=Depends(get_db)):
    rows=db.query(Transaction).filter(Transaction.user_id==user_id).all()
    income=sum(r.amount for r in rows if r.type=='income')
    expense=sum(r.amount for r in rows if r.type=='expense')
    cats=defaultdict(float)
    for r in rows:
        if r.type=='expense': cats[r.category]+=r.amount
    return {"income":round(income,2),"expense":round(expense,2),"balance":round(income-expense,2),"categories":dict(sorted(cats.items(),key=lambda x:x[1],reverse=True)),"budget":recommendation(db,user_id,monthly_income or income),"anomalies":detect(db,user_id),"forecast":forecast(db,user_id)}
