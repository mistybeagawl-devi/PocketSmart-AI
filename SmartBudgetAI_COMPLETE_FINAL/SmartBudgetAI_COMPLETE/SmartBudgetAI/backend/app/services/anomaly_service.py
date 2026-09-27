from datetime import date
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from app.db.models import Transaction

def detect(db: Session, user_id: str):
    rows = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.type == "expense").order_by(Transaction.date).all()
    if len(rows) < 5:
        return {"count": 0, "anomalies": [], "message": "At least 5 expense transactions are needed for anomaly detection."}
    X = [[r.amount] for r in rows]
    model = IsolationForest(contamination="auto", random_state=42)
    labels = model.fit_predict(X)
    anomalies=[]
    for r,label in zip(rows,labels):
        if label == -1:
            anomalies.append({"id":r.id,"date":r.date.isoformat(),"description":r.description,"category":r.category,"amount":r.amount,"reason":"Unusual transaction amount relative to the user's recent expense distribution."})
    return {"count":len(anomalies),"anomalies":anomalies}
