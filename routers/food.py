from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database.db_manager import get_db
from database.models import User
from services.auth import get_current_user
from services.ai_engine import parse_meal_nlp
from services.swap_engine import find_swadeshi_swap

router = APIRouter(prefix="/api/food", tags=["Food"])

@router.get("/search")
def search_food_endpoint(query: str = Query(..., description="The meal or food item to search for"), user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Search for a food item using AI natural language parsing.
    """
    user = db.query(User).filter(User.id == user_id).first()
    diet_preference = user.diet_preference if user else "any"
    
    results = parse_meal_nlp(query, diet_preference)
    if not results:
        raise HTTPException(status_code=404, detail="No matching foods found.")
        
    return {"results": results}


@router.get("/swap")
async def swap_food_endpoint(target: str = Query(...), calories: float = 0, protein: float = 0, carbs: float = 0, fats: float = 0):
    """
    Finds a budget-friendly local Indian swap for an expensive/premium food.
    """
    target_macros = {
        "calories_100g": calories,
        "protein_100g": protein,
        "carbs_100g": carbs,
        "fats_100g": fats
    }
    
    swap = find_swadeshi_swap(target, target_macros)
    if not swap:
        raise HTTPException(status_code=404, detail="No swap found for this food category.")
        
    return {"swap": swap}

from fastapi import UploadFile, File
from pydantic import BaseModel
from services.ai_engine import analyze_meal_image, generate_recipe_from_ingredients

@router.post("/vision")
async def vision_food_endpoint(file: UploadFile = File(...), user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Parses a meal using AI vision based on an uploaded image.
    """
    user = db.query(User).filter(User.id == user_id).first()
    diet_preference = user.diet_preference if user else "any"
    
    # Read file bytes
    contents = await file.read()
    results = analyze_meal_image(contents, diet_preference)
    
    if not results:
        raise HTTPException(status_code=400, detail="Could not identify meal from image.")
    return {"results": results}

class RecipeRequest(BaseModel):
    ingredients: str
    target_calories: int

@router.post("/recipe")
async def generate_recipe_endpoint(req: RecipeRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Generate custom recipe based on ingredients and target calories.
    """
    user = db.query(User).filter(User.id == user_id).first()
    diet_preference = user.diet_preference if user else "any"
    
    recipe = generate_recipe_from_ingredients(req.ingredients, req.target_calories, diet_preference)
    return {"recipe": recipe}

from services.ai_engine import analyze_barcode

@router.get("/barcode/{code}")
def scan_barcode_endpoint(code: str, user_id: str = Depends(get_current_user)):
    """
    Simulates fetching packaged food info from a barcode.
    """
    result = analyze_barcode(code)
    return result
