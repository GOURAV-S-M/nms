from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from database.db_manager import get_db
from database.models import User, MealPlan
from services.auth import get_current_user
from services.ai_engine import generate_meal_plan, generate_grocery_list

router = APIRouter(prefix="/api/planner", tags=["Planner"])

@router.get("/generate")
def get_meal_plan(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    user_profile = {
        "age": user.age,
        "gender": user.gender,
        "goal": user.goal,
        "diet_preference": user.diet_preference,
        "allergies": json.loads(user.allergies),
        "budget_preference": user.budget_preference,
        "region": user.region
    }
    
    plan_data = generate_meal_plan(user_profile)
    
    # Save to db
    new_plan = MealPlan(user_id=user_id, plan_data=json.dumps(plan_data))
    db.add(new_plan)
    db.commit()
    
    return {"plan": plan_data}

@router.get("/grocery")
def get_grocery_list(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    user_profile = {
        "diet_preference": user.diet_preference,
        "budget_preference": user.budget_preference,
        "region": user.region
    }
    groceries = generate_grocery_list(user_profile)
    return {"groceries": groceries}
