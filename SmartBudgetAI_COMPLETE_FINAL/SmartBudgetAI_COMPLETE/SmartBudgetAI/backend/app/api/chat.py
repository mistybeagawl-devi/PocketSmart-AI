from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ChatMessage
from app.schemas.chat import ChatRequest,ChatResponse
from app.services.llm_service import answer
from app.services.budget_service import recommendation
router=APIRouter(tags=['AI Assistant'])
@router.post('/chat',response_model=ChatResponse)
def chat(payload:ChatRequest,db:Session=Depends(get_db)):
    context=recommendation(db,payload.user_id,0)
    text,provider=answer(payload.message,str(context))
    db.add(ChatMessage(user_id=payload.user_id,role='user',content=payload.message))
    db.add(ChatMessage(user_id=payload.user_id,role='assistant',content=text)); db.commit()
    return ChatResponse(answer=text,provider=provider)
