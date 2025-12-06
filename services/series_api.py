import requests
from config.config import Config

def send_message(chat_id: str, text: str) -> bool:
    """Send message using chat_id from Kafka message"""
    url = f"{Config.SERIES_API_BASE_URL}/api/chats/{chat_id}/chat_messages"
    headers = {
        'Authorization': f'Bearer {Config.SERIES_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {"message": {"text": text}}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"   ✅ Reply sent!")
            return True
        else:
            print(f"   ❌ Send failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Send error: {e}")
        return False

def format_recommendations(places: list) -> str:
    if not places:
        return "No spots from your network yet! Ask friends to share their favorites 🙂"
    
    lines = ["Here's what your network recommends:\n"]
    
    for i, p in enumerate(places[:3], 1):
        degree_emoji = "👤" if p["degree"] == "1st" else "👥"
        lines.append(f"{i}. {p['name']} {p.get('price', '')}")
        lines.append(f"   {degree_emoji} {p['from_user']} says: \"{p['description'][:50]}...\"")
        lines.append("")
    
    return "\n".join(lines)