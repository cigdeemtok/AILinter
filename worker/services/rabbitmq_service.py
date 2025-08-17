import json
import pika
import logging
from typing import Dict, Any, Callable
from config import settings

logger = logging.getLogger(__name__)

class RabbitMQWorkerService:
    """RabbitMQ worker servisi - kuyruğu dinler ve mesajları işler"""
    
    def __init__(self):
        self.connection = None
        self.channel = None
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
            
            # QoS ayarları (bir seferde bir mesaj işle)
            self.channel.basic_qos(prefetch_count=1)
            
            logger.info(f"RabbitMQ Worker başarıyla bağlandı: {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}")
            
        except Exception as e:
            logger.error(f"RabbitMQ Worker bağlantı hatası: {str(e)}")
            raise
    
    def start_consuming(self, message_handler: Callable[[Dict[str, Any]], None]) -> None:
        """Kuyruğu dinlemeye başla"""
        try:
            # Mesaj işleyici callback'i
            def callback(ch, method, properties, body):
                try:
                    # Mesajı JSON olarak parse et
                    message = json.loads(body.decode('utf-8'))
                    logger.info(f"Mesaj alındı: {message.get('analysisId', 'Unknown')}")
                    
                    # Mesajı işle
                    message_handler(message)
                    
                    # Mesajı onayla
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logger.info(f"Mesaj başarıyla işlendi: {message.get('analysisId', 'Unknown')}")
                    
                except Exception as e:
                    logger.error(f"Mesaj işleme hatası: {str(e)}")
                    # Hata durumunda mesajı reddet
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
            # Kuyruğu dinlemeye başla
            self.channel.basic_consume(
                queue=settings.RABBITMQ_QUEUE,
                on_message_callback=callback
            )
            
            logger.info(f"Worker başlatıldı: {settings.WORKER_NAME}")
            logger.info(f"Kuyruk dinleniyor: {settings.RABBITMQ_QUEUE}")
            
            # Sonsuz döngüde mesajları bekle
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Worker durduruluyor...")
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Worker hatası: {str(e)}")
            self.stop_consuming()
    
    def stop_consuming(self) -> None:
        """Kuyruk dinlemeyi durdur"""
        try:
            if self.channel and self.channel.is_open:
                self.channel.stop_consuming()
                logger.info("Kuyruk dinleme durduruldu")
        except Exception as e:
            logger.error(f"Kuyruk dinleme durdurma hatası: {str(e)}")
    
    def close_connection(self) -> None:
        """Bağlantıyı kapat"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("RabbitMQ Worker bağlantısı kapatıldı")
        except Exception as e:
            logger.error(f"Bağlantı kapatma hatası: {str(e)}")

# Global RabbitMQ Worker servis instance'ı
rabbitmq_worker = RabbitMQWorkerService() 