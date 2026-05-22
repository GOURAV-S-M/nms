from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import datetime

from database.db_manager import get_db
from database.models import DailyLog, User
from services.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

class LogEntry(BaseModel):
    food_name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    water_ml: int = 0
    mood: str = None
    sleep_hours: float = 0

@router.get("/logs")
def get_daily_logs(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    logs = db.query(DailyLog).filter(
        DailyLog.user_id == user_id, 
        DailyLog.timestamp >= today_start
    ).order_by(DailyLog.timestamp.desc()).all()
    
    return {"logs": logs}

@router.post("/log")
def add_log(entry: LogEntry, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_log = DailyLog(
        user_id=user_id,
        food_name=entry.food_name,
        calories=entry.calories,
        protein=entry.protein,
        carbs=entry.carbs,
        fats=entry.fats,
        water_ml=entry.water_ml,
        mood=entry.mood,
        sleep_hours=entry.sleep_hours
    )
    db.add(new_log)
    db.commit()
    
    return {"message": "Log added successfully"}

@router.get("/deficiencies")
def get_deficiencies(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Analyzes log history to warn about long-term macro/micro deficiencies.
    """
    user = db.query(User).filter(User.id == user_id).first()
    logs = db.query(DailyLog).filter(DailyLog.user_id == user_id).all()
    
    # Calculate simple aggregate
    total_protein = sum(log.protein for log in logs)
    # Estimate unique days by distinct timestamps (simple local approach)
    unique_days = set(log.timestamp.date() for log in logs) if logs else set()
    total_days = len(unique_days) if len(unique_days) > 0 else 1
    
    avg_protein = total_protein / total_days
    
    alerts = []
    
    if user and (user.diet_preference == "veg" or user.diet_preference == "vegan"):
        alerts.append("B12 Warning: As a vegetarian/vegan, your AI logs suggest you might be missing Vitamin B12. Consider fortified nutritional yeast or supplements.")
        
    weight = user.weight_kg if user and user.weight_kg else 60
    if avg_protein < weight * 0.8:
        alerts.append(f"Protein Deficit: Your average protein is {round(avg_protein)}g/day, which is below the recommended {round(weight * 0.8)}g for your profile.")
        
    if not alerts:
        alerts.append("No active deficiencies detected! Great job tracking your macros.")
        
    return {"alerts": alerts}

from services.ai_engine import analyze_symptoms, generate_health_report

class SymptomsRequest(BaseModel):
    symptoms: list[str]

@router.post("/symptoms")
def check_symptoms(req: SymptomsRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Analyzes symptoms and returns deficiency predictions.
    """
    result = analyze_symptoms(req.symptoms)
    return result

@router.get("/report")
def get_daily_report(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Generates an AI health report for today.
    """
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    user = db.query(User).filter(User.id == user_id).first()
    logs = db.query(DailyLog).filter(DailyLog.user_id == user_id, DailyLog.timestamp >= today_start).all()
    
    log_dicts = [{"calories": l.calories, "protein": l.protein, "water_ml": l.water_ml} for l in logs]
    
    # We pass user profile as empty dict if user missing, otherwise simple dict
    user_prof = {} if not user else {"weight": user.weight_kg}
    
    report = generate_health_report(log_dicts, user_prof)
    return {"report": report}
