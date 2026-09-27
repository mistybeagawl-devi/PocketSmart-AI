from datetime import date
from pydantic import BaseModel, Field

class TransactionCreate(BaseModel):
    user_id: str = "demo-user"
    date: date
    description: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    type: str = Field(pattern="^(income|expense)$")

class TransactionOut(TransactionCreate):
    id: int
    model_config = {"from_attributes": True}
