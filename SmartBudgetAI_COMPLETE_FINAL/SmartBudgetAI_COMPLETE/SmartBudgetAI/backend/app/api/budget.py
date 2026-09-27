from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.budget_service import recommendation
router=APIRouter(prefix="/budget",tags=["Budget"])
@router.get("/recommendation")
def get_recommendation(user_id="demo-user", monthly_income:float=0, db:Session=Depends(get_db)):
    return recommendation(db,user_id,monthly_income)
