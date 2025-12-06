import json
from openai import OpenAI
from config.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

EXTRACTION_PROMPT = """Extract place information from this message. If it's adding a place recommendation, extract details. If it's asking for recommendations, return query info.

Message: {message}

Respond in JSON:
{{
    "intent": "add_place" | "query" | "other",
    "place": {{
        "name": "place name",
        "description": "what user said about it",
        "type": "cafe|restaurant|bar|park|gym|store|other",
        "price": "$|$$|$$$|$$$$|unknown",
        "vibe": "quiet|lively|cozy|trendy|casual|fancy|unknown"
    }},
    "query": {{
        "text": "what they're looking for",
        "type": "cafe|restaurant|bar|any",
        "constraints": ["quiet", "cheap", etc]
    }}
}}

Only include "place" for add_place, only "query" for query intent."""

def extract_place_info(message: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You extract structured place data from casual messages. Be flexible with informal language."},
            {"role": "user", "content": EXTRACTION_PROMPT.format(message=message)}
        ],
        temperature=0
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"intent": "other"}

def generate_embedding(text: str) -> list:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding