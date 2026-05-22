import requests
import json
import logging

logger = logging.getLogger(__name__)

# Using OpenFoodFacts API as it requires no keys for prototyping.
# The search API endpoint returns matching food items.
OPEN_FOOD_FACTS_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

def search_food(query: str, allergies: list = None) -> list:
    """
    Search for a food item and return a list of matches.
    If allergies are provided, filters out foods that contain allergen strings.
    """
    if allergies is None:
        allergies = []
        
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 10
    }

    headers = {
        "User-Agent": "NutriBharat/1.0 (likith@example.com)"
    }

    try:
        response = requests.get(OPEN_FOOD_FACTS_SEARCH_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        
        results = []
        for p in products:
            # Extract relevant fields
            product_name = p.get("product_name", "Unknown Food")
            
            # Check allergens
            allergens_tags = p.get("allergens_tags", [])
            ingredients_text = p.get("ingredients_text", "").lower()
            
            flagged = False
            for allergy in allergies:
                allergy_lower = allergy.lower()
                if allergy_lower in ingredients_text or any(allergy_lower in tag.lower() for tag in allergens_tags):
                    flagged = True
                    break
                    
            if flagged:
                continue # Skip this food as it contains an allergen
                
            nutriments = p.get("nutriments", {})
            calories = nutriments.get("energy-kcal_100g", 0)
            protein = nutriments.get("proteins_100g", 0)
            carbs = nutriments.get("carbohydrates_100g", 0)
            fats = nutriments.get("fat_100g", 0)
            sodium = nutriments.get("sodium_100g", 0)
            
            results.append({
                "food_name": product_name,
                "calories_100g": calories,
                "protein_100g": protein,
                "carbs_100g": carbs,
                "fats_100g": fats,
                "sodium_100g": sodium,
                "image_url": p.get("image_url", "")
            })
            
        return results
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying OpenFoodFacts API: {e}")
        return []
