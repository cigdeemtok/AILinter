import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Settings:
    """Worker ayarları sınıfı"""
    
    # Gemini API Ayarları
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
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
    
    # Worker Ayarları
    WORKER_NAME = os.getenv("WORKER_NAME", "ailinter_worker")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Global settings instance
settings = Settings() 