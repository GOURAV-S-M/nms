import math

# A static mapping of expensive/premium foods to local Indian alternatives.
# This could be expanded by querying an API, but for deterministic Swadeshi swaps,
# a categorized mapping is very effective when paired with macro-matching.
SWAP_CANDIDATES = {
    "avocado": [
        {"name": "Peanuts", "calories": 567, "protein": 25.8, "carbs": 16.1, "fats": 49.2, "category": "fats"},
        {"name": "Coconut (Fresh)", "calories": 354, "protein": 3.3, "carbs": 15.2, "fats": 33.5, "category": "fats"},
        {"name": "Walnuts (Akhrot)", "calories": 654, "protein": 15.2, "carbs": 13.7, "fats": 65.2, "category": "fats"}
    ],
    "quinoa": [
        {"name": "Amaranth (Rajgira)", "calories": 371, "protein": 13.6, "carbs": 65.2, "fats": 7.0, "category": "grains"},
        {"name": "Foxtail Millet (Kangni)", "calories": 331, "protein": 12.3, "carbs": 60.9, "fats": 4.3, "category": "grains"},
        {"name": "Sorghum (Jowar)", "calories": 329, "protein": 10.4, "carbs": 72.1, "fats": 3.3, "category": "grains"}
    ],
    "chia seeds": [
        {"name": "Basil Seeds (Sabja)", "calories": 442, "protein": 14.8, "carbs": 63.8, "fats": 13.8, "category": "seeds"},
        {"name": "Flax Seeds (Alsi)", "calories": 534, "protein": 18.3, "carbs": 28.9, "fats": 42.2, "category": "seeds"}
    ],
    "kale": [
        {"name": "Spinach (Palak)", "calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "category": "greens"},
        {"name": "Amaranth Leaves (Chaulai)", "calories": 23, "protein": 2.5, "carbs": 4.0, "fats": 0.3, "category": "greens"},
        {"name": "Mustard Greens (Sarson)", "calories": 27, "protein": 2.9, "carbs": 4.7, "fats": 0.4, "category": "greens"}
    ]
}

from services.ai_engine import get_ai_swadeshi_swap

def calculate_macro_distance(target, candidate):
    """
    Calculate Euclidean distance between macro profiles to find the closest match.
    """
    p_diff = target.get("protein_100g", 0) - candidate.get("protein", 0)
    c_diff = target.get("carbs_100g", 0) - candidate.get("carbs", 0)
    f_diff = target.get("fats_100g", 0) - candidate.get("fats", 0)
    
    return math.sqrt(p_diff**2 + c_diff**2 + f_diff**2)

def find_swadeshi_swap(target_food_name: str, target_macros: dict) -> dict:
    """
    Matches an expensive/premium target food to a budget-friendly Indian equivalent.
    """
    target_tokens = set(target_food_name.lower().split())
    
    # Check if any words match the keys in our swap dictionary
    candidates = None
    matched_key = None
    for key, cands in SWAP_CANDIDATES.items():
        key_tokens = set(key.lower().split())
        if target_tokens.intersection(key_tokens):
            candidates = cands
            matched_key = key
            break
            
    if not candidates:
        return get_ai_swadeshi_swap(target_food_name)
        
    # Rank candidates by macro similarity (lowest distance is best)
    best_match = None
    min_distance = float('inf')
    
    for candidate in candidates:
        distance = calculate_macro_distance(target_macros, candidate)
        if distance < min_distance:
            min_distance = distance
            best_match = candidate
            
    if best_match:
        return {
            "original_food": target_food_name,
            "swap_food": best_match["name"],
            "swap_macros": {
                "calories_100g": best_match["calories"],
                "protein_100g": best_match["protein"],
                "carbs_100g": best_match["carbs"],
                "fats_100g": best_match["fats"]
            },
            "similarity_score": round(100 - min_distance, 2) # Arbitrary score for UI
        }
    return None
