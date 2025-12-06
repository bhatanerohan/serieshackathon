from pinecone import Pinecone
from config.config import Config

pc = Pinecone(api_key=Config.PINECONE_API_KEY)
index = pc.Index(Config.PINECONE_INDEX)

# Mock network - replace with real social graph later
NETWORK = {
    "user_1": {"1st": ["user_2", "user_3"], "2nd": ["user_4", "user_5"]},
    "user_2": {"1st": ["user_1", "user_4"], "2nd": ["user_3"]},
    "user_3": {"1st": ["user_1"], "2nd": ["user_2"]},
}

def store_place(user_id: str, place: dict, embedding: list) -> bool:
    place_id = f"{user_id}_{place['name'].lower().replace(' ', '_')}"
    
    index.upsert(vectors=[{
        "id": place_id,
        "values": embedding,
        "metadata": {
            "user_id": user_id,
            "place_name": place["name"],
            "description": place.get("description", ""),
            "place_type": place.get("type", "other"),
            "price": place.get("price", "unknown"),
            "vibe": place.get("vibe", "unknown")
        }
    }])
    return True

def query_places(user_id: str, query_embedding: list, filters: dict = None, top_k: int = 5) -> list:
    # Get user's network
    network = NETWORK.get(user_id, {"1st": [], "2nd": []})
    network_ids = network["1st"] + network["2nd"]
    
    if not network_ids:
        return []
    
    # Build filter
    query_filter = {"user_id": {"$in": network_ids}}
    if filters:
        if filters.get("type"):
            query_filter["place_type"] = filters["type"]
        if filters.get("price"):
            query_filter["price"] = filters["price"]
    
    results = index.query(
        vector=query_embedding,
        filter=query_filter,
        top_k=top_k,
        include_metadata=True
    )
    
    # Add degree info
    places = []
    for match in results.matches:
        meta = match.metadata
        degree = "1st" if meta["user_id"] in network["1st"] else "2nd"
        places.append({
            "name": meta["place_name"],
            "description": meta["description"],
            "type": meta["place_type"],
            "price": meta["price"],
            "vibe": meta["vibe"],
            "from_user": meta["user_id"],
            "degree": degree,
            "score": match.score
        })
    
    return places