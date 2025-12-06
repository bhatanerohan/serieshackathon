from google import genai
from google.genai import types
from config.config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def search_places_web(query: str, location: str = "Boston") -> str:
    """Fallback search using Gemini with Google Search grounding"""
    
    prompt = f"""Find real places for this request: "{query}" in {location}.

Return 3-5 specific places with:
- Name
- Type (cafe/restaurant/bar/etc)
- Why it matches the request
- Price range ($-$$$$)

Be specific with real place names, not generic suggestions."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    
    return response.text