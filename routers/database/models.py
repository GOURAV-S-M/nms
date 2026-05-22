from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True) # UUID
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Extended Profile
    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    activity_level = Column(String, nullable=True) # sedentary, active, etc.
    goal = Column(String, nullable=True) # weight_loss, muscle_gain, diabetic
    diet_preference = Column(String, nullable=True) # veg, non-veg, vegan
    allergies = Column(Text, default="[]") # JSON string
    medical_conditions = Column(Text, default="[]") # JSON string
    budget_preference = Column(String, nullable=True) # low, medium, high
    region = Column(String, nullable=True) # e.g., South India, North India
    
    logs = relationship("DailyLog", back_populates="user")
    plans = relationship("MealPlan", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")

class DailyLog(Base):
    __tablename__ = "daily_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Food tracking
    food_name = Column(String, nullable=True)
    calories = Column(Float, default=0)
    protein = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fats = Column(Float, default=0)
    
    # Other Trackers
    water_ml = Column(Integer, default=0)
    mood = Column(String, nullable=True) # happy, tired, stressed
    sleep_hours = Column(Float, default=0)
    
    user = relationship("User", back_populates="logs")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    plan_data = Column(Text) # JSON structure containing the 7-day or daily meal plan
    
    user = relationship("User", back_populates="plans")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    role = Column(String) # 'user' or 'ai'
    message = Column(Text)
    
    user = relationship("User", back_populates="chats")
