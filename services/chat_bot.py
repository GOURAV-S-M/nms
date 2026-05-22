import re
from services.nutrition_api import search_food

# A very basic grounding engine to demonstrate AI grounding
# In a real app, this would use an LLM (like OpenAI or Gemini) to extract food entities.
def extract_food_entities(user_message: str) -> list:
    """
    Extracts potential food entities from a user message using simple regex rules.
    """
    # Simple naive extraction for demo purposes
    # E.g., "I ate some avocado" -> "avocado"
    words = re.sub(r'[^\w\s]', '', user_message.lower()).split()
    
    # Common stop words to ignore
    stop_words = {"i", "ate", "some", "had", "a", "an", "the", "for", "breakfast", "lunch", "dinner", "want", "eat"}
    
    potential_foods = [w for w in words if w not in stop_words and len(w) > 2]
    return potential_foods

def ground_chat_response(user_message: str, allergies: list = None) -> dict:
    """
    Intercepts a chat query, identifies foods, verifies nutrition via the internal API,
    and constructs a grounded response.
    """
    foods = extract_food_entities(user_message)
    
    if not foods:
        return {
            "response": "I'm your NutriBharat AI assistant. Tell me what you ate today!",
            "grounded_data": []
        }
        
    grounded_data = []
    response_parts = []
    
    for food in foods:
        # Search the internal API route (simulated by calling the service directly)
        results = search_food(food, allergies)
        
        if results:
            best_match = results[0]
            grounded_data.append(best_match)
            response_parts.append(
                f"I found {best_match['food_name']} which has {best_match['calories_100g']} kcal, "
                f"{best_match['protein_100g']}g protein per 100g."
            )
        else:
            response_parts.append(f"I couldn't verify the nutritional info for '{food}' (maybe it contains allergens you listed?).")
            
    final_response = " ".join(response_parts)
    final_response += " Would you like to log this in your diary?"
    
    return {
        "response": final_response,
        "grounded_data": grounded_data
    }
