import google.generativeai as genai
from config.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def search_places_web(query: str, location: str = "Boston") -> str:
    """Fallback search using Gemini with grounding"""
    
    prompt = f"""Find real places for this request: "{query}" in {location}.

Return 3-5 specific places with:
- Name
- Type (cafe/restaurant/bar/etc)
- Why it matches the request
- Price range ($-$$$$)

Be specific with real place names, not generic suggestions."""

    response = model.generate_content(
        prompt,
        tools='google_search_retrieval'
    )
    
    return response.text

def get_place_details(place_name: str, location: str = "Boston") -> str:
    """Get detailed info about a specific place"""
    
    prompt = f"""Get details about "{place_name}" in {location}:
- Address
- Hours
- Price range
- Popular items/highlights
- Recent reviews summary

Be factual and specific."""

    response = model.generate_content(
        prompt,
        tools='google_search_retrieval'
    )
    
    return response.text