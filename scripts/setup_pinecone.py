"""Run once to create Pinecone index"""

from pinecone import Pinecone, ServerlessSpec
try:
    from ..config.config import Config
except Exception:
    from config.config import Config

pc = Pinecone(api_key=Config.PINECONE_API_KEY)

# Create index if doesn't exist
if Config.PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=Config.PINECONE_INDEX,
        dimension=1536,  # text-embedding-3-small
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"✅ Created index: {Config.PINECONE_INDEX}")
else:
    print(f"Index {Config.PINECONE_INDEX} already exists")