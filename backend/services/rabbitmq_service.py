import json
import pika
from typing import Dict, Any
from config import settings
import logging

logger = logging.getLogger(__name__)

class RabbitMQService:
    """RabbitMQ bağlantı ve mesaj gönderme servisi"""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        # Başlangıçta bağlanma
        self._connect()
    
    def _connect(self) -> None:
        """RabbitMQ'ya bağlan"""
        try:
            # Bağlantı parametrelerini oluştur
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USERNAME, 
                settings.RABBITMQ_PASSWORD
            )
            
            parameters = pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            # Bağlantıyı kur
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Kuyruğu tanımla (eğer yoksa oluştur)
            self.channel.queue_declare(
                queue=settings.RABBITMQ_QUEUE,
                durable=True  # Kuyruk kalıcı olsun
            )
            
            logger.info(f"RabbitMQ'ya başarıyla bağlandı: {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}")
            
        except Exception as e:
            logger.error(f"RabbitMQ bağlantı hatası: {str(e)}")
            raise
    
    def send_message(self, message: Dict[str, Any]) -> bool:
        """Mesajı kuyruğa gönder"""
        try:
            if not self.connection or self.connection.is_closed:
                self._connect()
            
            # Mesajı JSON formatında gönder
            message_body = json.dumps(message, ensure_ascii=False)
            
            self.channel.basic_publish(
                exchange='',
                routing_key=settings.RABBITMQ_QUEUE,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Mesaj kalıcı olsun
                    content_type='application/json'
                )
            )
            
            logger.info(f"Mesaj başarıyla gönderildi: {message.get('analysisId', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Mesaj gönderme hatası: {str(e)}")
            return False
    
    def close_connection(self) -> None:
        """Bağlantıyı kapat"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("RabbitMQ bağlantısı kapatıldı")
        except Exception as e:
            logger.error(f"Bağlantı kapatma hatası: {str(e)}")

# Global RabbitMQ servis instance'ı (lazy loading)
rabbitmq_service = RabbitMQService() 