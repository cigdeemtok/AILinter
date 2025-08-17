import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Settings:
    """Uygulama ayarları sınıfı"""
    
    # RabbitMQ Ayarları
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
    RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "code_analysis")
    
    # Redis Ayarları
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    
    # API Ayarları
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Gemini API Ayarları
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Global settings instance
settings = Settings() 