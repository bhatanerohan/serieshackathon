from kafka import KafkaConsumer
import json
from config.config import Config
from services.place_extractor import extract_place_info, generate_embedding
from services.pinecone_service import store_place, query_places
from services.series_api import send_message, format_recommendations
from services.gemini_service import search_places_web, get_place_details

MIN_SCORE_THRESHOLD = 0.4
MIN_RESULTS = 2

def create_consumer():
    return KafkaConsumer(
        Config.KAFKA_TOPIC,
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        security_protocol='SASL_SSL',
        sasl_mechanism='PLAIN',
        sasl_plain_username=Config.KAFKA_SASL_USERNAME,
        sasl_plain_password=Config.KAFKA_SASL_PASSWORD,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=Config.KAFKA_CONSUMER_GROUP
    )

def handle_message(chat_id: str, phone: str, user_id: str, text: str):
    print(f"📩 From {phone}: {text}")
    print(f"   Chat ID: {chat_id}")
    
    # Extract intent and data
    extracted = extract_place_info(text)
    intent = extracted.get("intent")
    print(f"   Intent: {intent}")
    
    if intent == "add_place":
        place = extracted["place"]
        print(f"   📦 Extracted: {place}")
        embed_text = f"{place['name']} {place.get('description', '')} {place.get('type', '')} {place.get('vibe', '')}"
        embedding = generate_embedding(embed_text)
        print(f"   ✅ Embedding generated")
        store_place(user_id, place, embedding)
        print(f"   📍 Stored in Pinecone: {place['name']}")
        response = f"✅ Added {place['name']} to your spots! Your friends will see this when searching."
        print(f"   💬 Sending reply: {response}")
        send_message(chat_id, response)
        
    elif intent == "query":
        query = extracted["query"]
        print(f"   📦 Extracted query: {query}")
        embedding = generate_embedding(query["text"])
        filters = {"type": query["type"]} if query.get("type") and query["type"] != "any" else {}
        print(f"   🔎 Searching with filters: {filters}")
        places = query_places(user_id, embedding, filters)
        
        # Check if results are good enough
        good_results = [p for p in places if p['score'] >= MIN_SCORE_THRESHOLD]
        
        if len(good_results) >= MIN_RESULTS:
            print(f"   🔍 Found {len(good_results)} good results from network")
            response = format_recommendations(good_results)
        else:
            print(f"   ⚠️ Only {len(good_results)} good results, falling back to web search...")
            web_results = search_places_web(query["text"])
            print(f"   🌐 Web results: {web_results[:100]}...")
            
            if good_results:
                response = f"From your network:\n{format_recommendations(good_results)}\n\nAlso found online:\n{web_results}"
            else:
                response = f"No one in your network has shared spots for this yet!\n\nHere's what I found online:\n{web_results}"
        
        print(f"   💬 Sending reply:\n{response}")
        send_message(chat_id, response)
        
    else:
        print(f"   ❓ No action taken")
        response = "Hey! You can:\n• Share a spot: \"Tatte is a great quiet cafe\"\n• Find spots: \"where's good for a date?\""
        print(f"   💬 Sending reply: {response}")
        send_message(chat_id, response)

def run():
    print("🚀 Starting Places Consumer...")
    consumer = create_consumer()
    print("✅ Connected to Kafka\n")
    
    # Map phone → user_id (mock - replace with real lookup)
    PHONE_TO_USER = {
        "+15512298798": "user_1",
        "+18574659967": "user_2",
    }
    
    for message in consumer:
        data = message.value
        
        if data.get('event_type') == 'message.received':
            msg = data.get('data', {})
            chat_id = msg.get('chat_id')
            phone = msg.get('from_phone')
            text = msg.get('text', '')
            
            user_id = PHONE_TO_USER.get(phone, f"user_{phone[-4:]}")
            
            if not chat_id or not text:
                print(f"⚠️ Missing chat_id or text")
                continue
            
            try:
                handle_message(chat_id, phone, user_id, text)
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()