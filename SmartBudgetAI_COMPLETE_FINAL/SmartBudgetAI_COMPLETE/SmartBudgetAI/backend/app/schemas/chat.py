from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    user_id: str = "demo-user"
    message: str = Field(min_length=1, max_length=4000)
class ChatResponse(BaseModel):
    answer: str
    provider: str
