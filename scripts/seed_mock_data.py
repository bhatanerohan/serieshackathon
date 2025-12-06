"""Seed mock places to test queries"""
import sys
sys.path.append('..')

from services.place_extractor import generate_embedding
from services.pinecone_service import store_place

MOCK_PLACES = [
    {"user": "user_2", "place": {"name": "Tatte", "description": "Amazing pastries and great coffee, quiet enough to work", "type": "cafe", "price": "$$", "vibe": "cozy"}},
    {"user": "user_2", "place": {"name": "Flour Bakery", "description": "Best sticky buns in Boston, always packed on weekends", "type": "cafe", "price": "$$", "vibe": "lively"}},
    {"user": "user_3", "place": {"name": "Thinking Cup", "description": "Perfect for studying, great lattes, never too loud", "type": "cafe", "price": "$", "vibe": "quiet"}},
    {"user": "user_3", "place": {"name": "Barcelona Wine Bar", "description": "Romantic tapas spot, amazing sangria, great for dates", "type": "restaurant", "price": "$$$", "vibe": "trendy"}},
    {"user": "user_4", "place": {"name": "Mike's Pastry", "description": "Iconic cannolis, always a line but worth it", "type": "cafe", "price": "$", "vibe": "lively"}},
    {"user": "user_4", "place": {"name": "Row 34", "description": "Fresh oysters and craft beer, upscale but casual vibe", "type": "restaurant", "price": "$$$", "vibe": "trendy"}},
]

def seed():
    print("🌱 Seeding mock data...")
    
    for item in MOCK_PLACES:
        place = item["place"]
        embed_text = f"{place['name']} {place['description']} {place['type']} {place['vibe']}"
        embedding = generate_embedding(embed_text)
        store_place(item["user"], place, embedding)
        print(f"  ✅ {place['name']} ({item['user']})")
    
    print("\n🎉 Done! Test queries via iMessage.")

if __name__ == "__main__":
    seed()