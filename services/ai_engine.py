import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API if available
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
else:
    model = None
    logger.warning("No GEMINI_API_KEY found. Falling back to heuristic AI engine.")

def parse_meal_nlp(text: str, diet_preference: str = "any") -> list:
    """
    Parses natural language (e.g. "2 dosa and coffee") into exact macros.
    Uses diet preference to disambiguate (e.g. Biryani -> Veg Biryani if veg).
    """
    if model:
        try:
            prompt = f"""
            Analyze this meal: "{text}". The user is {diet_preference}. 
            Return a JSON array of food items. For each item, provide:
            - food_name: string
            - calories: float
            - protein: float
            - carbs: float
            - fats: float
            Only return the raw JSON array, nothing else.
            """
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3]
            return json.loads(json_text)
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            pass
            
    # Advanced Heuristic Fallback
    text = text.lower()
    results = []
    
    if "dosa" in text:
        results.append({"food_name": "Dosa", "calories": 133, "protein": 2.6, "carbs": 22.3, "fats": 3.7})
    if "coffee" in text:
        results.append({"food_name": "Coffee (with milk & sugar)", "calories": 45, "protein": 1.0, "carbs": 8.0, "fats": 1.0})
    if "chicken" in text or ("biryani" in text and diet_preference == "non-veg"):
        results.append({"food_name": "Chicken Meal", "calories": 300, "protein": 31, "carbs": 30, "fats": 10})
    if "paneer" in text or ("biryani" in text and diet_preference == "veg"):
        results.append({"food_name": "Paneer Meal", "calories": 350, "protein": 18, "carbs": 40, "fats": 22})
        
    if not results:
        results.append({"food_name": text.title(), "calories": 150, "protein": 5, "carbs": 15, "fats": 5})
        
    return results

def chat_assistant(user_profile: dict, query: str, history: list = None) -> str:
    """
    Personalized nutritionist AI chatbot.
    """
    if model:
        try:
            profile_str = f"User is {user_profile.get('age', 25)}yo {user_profile.get('gender', 'person')}, goal: {user_profile.get('goal', 'health')}, allergies: {user_profile.get('allergies', 'none')}."
            prompt = f"{profile_str}\nYou are an expert Indian nutritionist. Answer this: {query}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            
    # Heuristic Fallback
    query = query.lower()
    if "diet" in query or "plan" in query:
        return f"Based on your {user_profile.get('goal', 'goal')}, I recommend focusing on a balanced Indian diet. Try adding more local millets and legumes for protein!"
    elif "allergy" in query:
        return f"Since you are allergic to {user_profile.get('allergies', 'certain foods')}, avoid those entirely and check ingredient labels carefully."
    
    return "That's a great question! Make sure to keep logging your meals so I can track your progress."

def generate_meal_plan(user_profile: dict) -> dict:
    """
    Generates a 7-day personalized Indian meal plan based on goals, budget, and region.
    """
    if model:
        try:
            profile_str = f"User is {user_profile.get('age', 25)}yo {user_profile.get('gender', 'person')}, goal: {user_profile.get('goal', 'health')}, diet: {user_profile.get('diet_preference', 'any')}, budget: {user_profile.get('budget_preference', 'any')}, region: {user_profile.get('region', 'India')}."
            prompt = f"{profile_str}\nGenerate a 7-day meal plan. Return ONLY raw JSON in this format: {{'monday': {{'breakfast': '...', 'lunch': '...', 'dinner': '...', 'total_calories': '...'}}, 'tuesday': {{...}}, ...}}"
            
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3]
            return json.loads(json_text)
        except Exception as e:
            logger.error(f"Gemini Meal Plan Error: {e}")
            
    # Heuristic Fallback for 7 Days
    goal = user_profile.get("goal", "maintenance")
    
    day_plan = {
        "breakfast": "Poha with peanuts",
        "lunch": "2 Rotis, Dal Tadka, and Sabzi",
        "dinner": "Moong dal khichdi",
        "total_calories": "1500" if goal != "muscle_gain" else "2200"
    }
    
    return {
        "Monday": day_plan,
        "Tuesday": {"breakfast": "Idli Sambar", "lunch": "Rice and Rajma", "dinner": "Light Soup and Salad", "total_calories": day_plan["total_calories"]},
        "Wednesday": day_plan,
        "Thursday": {"breakfast": "Upma", "lunch": "Roti and Chana Masala", "dinner": "Besan Chilla", "total_calories": day_plan["total_calories"]},
        "Friday": day_plan,
        "Saturday": day_plan,
        "Sunday": day_plan
    }
    
def generate_grocery_list(user_profile: dict) -> list:
    """
    Generates a dynamic 7-day grocery list using Gemini based on the user's profile.
    """
    if model:
        try:
            profile_str = f"Diet: {user_profile.get('diet_preference', 'any')}, budget: {user_profile.get('budget_preference', 'any')}, region: {user_profile.get('region', 'India')}."
            prompt = f"{profile_str}\nAct as an expert Indian nutritionist. Generate a weekly grocery list for a single person. Return ONLY raw JSON in this format: {{ 'groceries': ['Item 1 (quantity)', 'Item 2 (quantity)'] }}"
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3]
            if json_text.startswith("```"):
                json_text = json_text[3:-3]
            data = json.loads(json_text)
            return data.get("groceries", [])
        except Exception as e:
            logger.error(f"Gemini Grocery Error: {e}")
            pass
            
    # Heuristic Fallback
    return ["Toor Dal (1kg)", "Basmati Rice (2kg)", "Paneer (500g)", "Spinach (2 bunches)", "Apples (1kg)", "Oats (500g)"]
    
def get_ai_swadeshi_swap(target: str) -> dict:
    """
    AI Fallback for Swadeshi Swap if the static dictionary fails.
    """
    if model:
        try:
            prompt = f"Find a cheap Indian swadeshi alternative for '{target}'. Return ONLY raw JSON in this format: {{'original_food': '{target}', 'swap_food': '...', 'swap_macros': {{'calories_100g': 0, 'protein_100g': 0, 'carbs_100g': 0, 'fats_100g': 0}}}}"
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3]
            return json.loads(json_text)
        except Exception:
            pass
            
    # Generic fallback
    return {
        "original_food": target,
        "swap_food": "Local Indian Legumes/Millets (Generic)",
        "swap_macros": {"calories_100g": 350, "protein_100g": 15, "carbs_100g": 60, "fats_100g": 5}
    }

def analyze_meal_image(image_bytes: bytes, diet_preference: str = "any") -> list:
    """
    Simulates or performs Vision-based macro extraction from an image.
    """
    if model:
        try:
            # Note: actual production would use genai vision methods
            # Since this is local dev without a guaranteed key, we mock the vision response
            pass
        except Exception:
            pass
            
    # Mock Vision Fallback
    return [
        {"food_name": "AI Vision: Mixed Indian Thali", "calories": 450, "protein": 15, "carbs": 60, "fats": 12}
    ]

def generate_recipe_from_ingredients(ingredients: str, target_calories: int, diet: str) -> dict:
    """
    Generates a recipe based on available ingredients and macro targets.
    """
    if model:
        try:
            prompt = f"I have these ingredients: {ingredients}. My target is ~{target_calories} calories and I am {diet}. Generate a recipe. Return raw JSON: {{'title': '...', 'prep_time': '...', 'calories': {target_calories}, 'ingredients': ['...'], 'steps': ['...']}}"
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3]
            return json.loads(json_text)
        except Exception:
            pass
            
    # Heuristic Fallback
    return {
        "title": "AI Custom Scramble/Stir-fry",
        "prep_time": "15 mins",
        "calories": target_calories,
        "ingredients": [i.strip() for i in ingredients.split(",")],
        "steps": [
            "Chop all ingredients finely.",
            "Heat 1 tsp oil in a pan, temper cumin seeds.",
            "Sauté the ingredients until cooked.",
            "Season with salt, turmeric, and chili powder."
        ]
    }

def analyze_symptoms(symptoms: list) -> dict:
    """
    Predicts possible nutritional deficiencies based on selected symptoms using Generative AI.
    """
    symptoms_str = ", ".join(symptoms).lower()
    
    if model:
        try:
            prompt = f"""
            The user is experiencing these symptoms: {symptoms_str}.
            Act as an expert clinical nutritionist. Predict the most likely nutritional deficiency.
            Return ONLY raw JSON in exactly this format:
            {{
                "deficiency": "Name of Deficiency",
                "confidence": "Percentage (e.g. 85%)",
                "recommended_foods": ["Food 1", "Food 2", "Food 3"],
                "suggestions": "A 2-sentence actionable suggestion"
            }}
            Do not include any markdown formatting like ```json.
            """
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3].strip()
            if json_text.startswith("```"):
                json_text = json_text[3:-3].strip()
            return json.loads(json_text)
        except Exception as e:
            logger.error(f"Gemini API Error in symptoms: {e}")
            pass
            
    # Heuristic logic for symptoms fallback
    deficiency = "Unknown"
    confidence = "Low"
    foods = []
    suggestions = "Please consult a healthcare professional."
    
    if any(s in symptoms_str for s in ["fatigue", "pale skin", "dizziness"]):
        deficiency = "Iron Deficiency"
        confidence = "85%"
        foods = ["Spinach", "Lentils", "Red Meat", "Pumpkin Seeds"]
        suggestions = "Consider pairing iron-rich foods with Vitamin C (like lemon juice) for better absorption."
    elif any(s in symptoms_str for s in ["muscle cramps", "bone pain", "joint pain"]):
        deficiency = "Calcium / Vitamin D Deficiency"
        confidence = "80%"
        foods = ["Milk", "Yogurt", "Ragi", "Sunlight exposure"]
        suggestions = "Ensure you get 15-20 minutes of morning sunlight daily along with dairy or fortified alternatives."
    elif any(s in symptoms_str for s in ["hair fall", "low energy", "brittle nails"]):
        deficiency = "Vitamin B12 or Protein Deficiency"
        confidence = "75%"
        foods = ["Eggs", "Paneer", "Fish", "Nutritional Yeast"]
        suggestions = "If you are strictly vegetarian, consider a B12 supplement as dietary sources are limited."
        
    return {
        "deficiency": deficiency,
        "confidence": confidence,
        "recommended_foods": foods,
        "suggestions": suggestions
    }

def generate_health_report(logs: list, user_profile: dict) -> dict:
    """
    Generates a daily health report dynamically via AI based on logged meals.
    """
    total_cals = sum(l.get("calories", 0) for l in logs)
    total_pro = sum(l.get("protein", 0) for l in logs)
    total_water = sum(l.get("water_ml", 0) for l in logs)
    
    if model:
        try:
            profile_str = f"Weight: {user_profile.get('weight', 'unknown')}kg"
            logs_str = json.dumps(logs)
            prompt = f"""
            User Profile: {profile_str}.
            Today's Log: Total Calories={total_cals}, Protein={total_pro}g, Water={total_water}ml.
            Raw Meals: {logs_str}.
            
            Act as an expert AI Nutritionist. Generate a dynamic daily health report.
            Evaluate their nutrient balance, meal consistency, and give a score out of 100.
            Return ONLY raw JSON in exactly this format:
            {{
                "calories_consumed": {total_cals},
                "protein_intake": {total_pro},
                "hydration_score": "{total_water} ml",
                "nutrient_balance": "Short evaluation string (e.g., 'Low Protein, High Carbs')",
                "meal_consistency": "Evaluation string (e.g., 'Good', 'Missed Lunch')",
                "overall_score": integer between 0-100,
                "suggestions": "2-sentence highly personalized advice based on exactly what they ate today."
            }}
            Do not include markdown formatting.
            """
            response = model.generate_content(prompt)
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:-3].strip()
            if json_text.startswith("```"):
                json_text = json_text[3:-3].strip()
            return json.loads(json_text)
        except Exception as e:
            logger.error(f"Gemini API Error in report: {e}")
            pass

    # Heuristic Fallback
    score = 100
    if total_cals < 1000 or total_cals > 3000: score -= 20
    if total_pro < 40: score -= 15
    if total_water < 1500: score -= 15
    if len(logs) < 2: score -= 20 
    
    score = max(0, min(100, score))
    
    suggestion = "Great job today! Keep up the consistency."
    if score < 70:
        suggestion = "You missed some key macro goals today. Focus on hitting protein targets and staying hydrated tomorrow!"
        
    return {
        "calories_consumed": total_cals,
        "protein_intake": total_pro,
        "hydration_score": f"{total_water} ml",
        "nutrient_balance": "Optimal" if total_pro >= 50 else "Low Protein",
        "meal_consistency": "Good" if len(logs) >= 3 else "Needs Improvement",
        "overall_score": score,
        "suggestions": suggestion
    }

def analyze_barcode(barcode: str) -> dict:
    """
    Simulates Barcode scanning for packaged foods.
    """
    # Simulated database mapping
    if barcode.startswith("890"): # India EAN
        return {
            "food_name": "Packaged Indian Snack / Biscuit",
            "health_rating": "Poor (2/10)",
            "processed_level": "Ultra-Processed",
            "high_sugar": True,
            "calories": 450,
            "protein": 5,
            "alternatives": ["Roasted Makhana", "Dry Fruits", "Homemade Ladoo"]
        }
    
    return {
        "food_name": "Generic Packaged Product",
        "health_rating": "Moderate (5/10)",
        "processed_level": "Moderately Processed",
        "high_sugar": False,
        "calories": 200,
        "protein": 8,
        "alternatives": ["Fresh Fruits", "Whole Grains"]
    }
