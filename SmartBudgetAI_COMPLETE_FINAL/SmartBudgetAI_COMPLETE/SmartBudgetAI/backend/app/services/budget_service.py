from collections import defaultdict
from sqlalchemy.orm import Session
from app.db.models import Transaction

DEFAULT_RULE = {"needs": 0.50, "wants": 0.30, "savings": 0.20}
CATEGORY_BUCKETS = {
    "needs": {"Needs", "Food", "Transport", "Utilities", "Housing", "Health"},
    "wants": {"Wants", "Entertainment", "Shopping", "Dining"},
    "savings": {"Savings", "Investment", "Emergency Fund"},
}

def classify(category: str) -> str:
    for bucket, categories in CATEGORY_BUCKETS.items():
        if category in categories:
            return bucket
    return "wants"

def recommendation(db: Session, user_id: str, monthly_income: float):
    rows = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.type == "expense").all()
    actual = defaultdict(float)
    for row in rows:
        actual[classify(row.category)] += row.amount
    total = sum(actual.values())
    # Adapt the benchmark modestly when observed spending is available.
    observed_income = sum(x.amount for x in db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.type == "income").all())
    income = monthly_income if monthly_income > 0 else observed_income
    if income <= 0:
        income = 1.0
    weights = DEFAULT_RULE.copy()
    if total:
        needs_ratio = actual["needs"] / total
        wants_ratio = actual["wants"] / total
        weights["needs"] = min(max((weights["needs"] + needs_ratio) / 2, 0.35), 0.65)
        weights["wants"] = min(max((weights["wants"] + wants_ratio) / 2, 0.15), 0.40)
        weights["savings"] = max(1 - weights["needs"] - weights["wants"], 0.10)
    targets = {k: round(income*v, 2) for k,v in weights.items()}
    return {"income": round(income,2), "weights": weights, "targets": targets, "observed": {k: round(v,2) for k,v in actual.items()}, "total_observed_expense": round(total,2)}
