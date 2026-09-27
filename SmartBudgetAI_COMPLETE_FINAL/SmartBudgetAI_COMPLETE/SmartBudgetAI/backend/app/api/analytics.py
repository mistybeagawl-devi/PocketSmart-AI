from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.anomaly_service import detect
from app.services.forecast_service import forecast
router=APIRouter(prefix="/analytics",tags=["Analytics"])
@router.get("/anomalies")
def anomalies(user_id="demo-user",db:Session=Depends(get_db)): return detect(db,user_id)
@router.get("/forecast")
def expense_forecast(user_id="demo-user",days:int=30,db:Session=Depends(get_db)): return forecast(db,user_id,days)
