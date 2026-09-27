from app.services.budget_service import recommendation
from app.services.anomaly_service import detect
from app.db.models import Transaction
from app.db.session import Base,SessionLocal,engine
from datetime import date

def setup_function():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)

def test_budget_recommendation():
    db=SessionLocal(); db.add(Transaction(user_id='u',date=date.today(),description='salary',category='Income',amount=50000,type='income')); db.commit()
    result=recommendation(db,'u',50000)
    assert result['targets']['savings']==10000
    db.close()

def test_anomaly_requires_data():
    db=SessionLocal(); assert detect(db,'u')['count']==0; db.close()
