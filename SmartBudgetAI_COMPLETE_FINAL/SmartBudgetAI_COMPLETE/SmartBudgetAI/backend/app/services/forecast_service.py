from collections import defaultdict
from datetime import timedelta
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy.orm import Session
from app.db.models import Transaction

def forecast(db: Session, user_id: str, days: int = 30):
    rows = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.type == "expense").order_by(Transaction.date).all()
    if len(rows) < 3:
        avg = sum(r.amount for r in rows) / max(len(rows),1)
        return {"method":"historical_average","daily_forecast":round(avg,2),"monthly_forecast":round(avg*30,2),"points":[]}
    by_day=defaultdict(float)
    first=rows[0].date
    for r in rows:
        by_day[(r.date-first).days]+=r.amount
    X=np.array(list(by_day.keys())).reshape(-1,1)
    y=np.array(list(by_day.values()))
    model=RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=1)
    model.fit(X,y)
    last=max(by_day)
    future=np.arange(last+1,last+days+1).reshape(-1,1)
    preds=np.maximum(model.predict(future),0)
    points=[{"date":(first+timedelta(days=int(d))).isoformat(),"amount":round(float(v),2)} for d,v in zip(future.ravel(),preds)]
    return {"method":"random_forest_regression","daily_forecast":round(float(preds.mean()),2),"monthly_forecast":round(float(preds.sum()),2),"points":points}
