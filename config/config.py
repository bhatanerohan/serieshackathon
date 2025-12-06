import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
    KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP')
    KAFKA_SASL_USERNAME = os.getenv('KAFKA_SASL_USERNAME')
    KAFKA_SASL_PASSWORD = os.getenv('KAFKA_SASL_PASSWORD')
    
    # Series API
    SERIES_API_KEY = os.getenv('SERIES_API_KEY')
    SERIES_API_BASE_URL = os.getenv('SERIES_BASE_URL', 'https://api.series.com')
    SERIES_SENDER_NUMBER = os.getenv('SERIES_SENDER_NUMBER')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Pinecone
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX = os.getenv('PINECONE_INDEX', 'places')