from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
import json

from database.db_manager import get_db
from database.models import User
from services.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str = None
    age: int = None
    gender: str = None
    height_cm: float = None
    weight_kg: float = None
    activity_level: str = None
    goal: str = None
    diet_preference: str = None
    allergies: list[str] = []
    medical_conditions: list[str] = []
    budget_preference: str = None
    region: str = None

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        id=user_id,
        username=user.username,
        password_hash=hashed_password,
        full_name=user.full_name,
        age=user.age,
        gender=user.gender,
        height_cm=user.height_cm,
        weight_kg=user.weight_kg,
        activity_level=user.activity_level,
        goal=user.goal,
        diet_preference=user.diet_preference,
        allergies=json.dumps(user.allergies),
        medical_conditions=json.dumps(user.medical_conditions),
        budget_preference=user.budget_preference,
        region=user.region
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_record = db.query(User).filter(User.username == form_data.username).first()
    if not user_record or not verify_password(form_data.password, user_record.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    access_token = create_access_token(data={"sub": user_record.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.get("/me")
def get_me(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "age": user.age,
        "gender": user.gender,
        "height_cm": user.height_cm,
        "weight_kg": user.weight_kg,
        "activity_level": user.activity_level,
        "goal": user.goal,
        "diet_preference": user.diet_preference,
        "allergies": json.loads(user.allergies),
        "medical_conditions": json.loads(user.medical_conditions),
        "budget_preference": user.budget_preference,
        "region": user.region
    }
