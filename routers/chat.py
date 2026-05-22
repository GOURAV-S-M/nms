from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from database.db_manager import get_db
from database.models import User, ChatHistory
from services.auth import get_current_user
from services.ai_engine import chat_assistant

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_endpoint(request: ChatRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch User Profile
    user = db.query(User).filter(User.id == user_id).first()
    user_profile = {
        "age": user.age,
        "gender": user.gender,
        "goal": user.goal,
        "allergies": json.loads(user.allergies)
    }
    
    # Save User message
    db.add(ChatHistory(user_id=user_id, role="user", message=request.message))
    
    # Get AI response
    response_text = chat_assistant(user_profile, request.message)
    
    # Save AI message
    db.add(ChatHistory(user_id=user_id, role="ai", message=response_text))
    db.commit()
    
    return {"reply": response_text}
