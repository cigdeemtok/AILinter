import logging
import signal
import sys
from typing import Dict, Any
from config import settings
from services.rabbitmq_service import rabbitmq_worker
from services.redis_service import redis_worker
from services.gemini_service import gemini_service

# Logging konfigürasyonu
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AILinterWorker:
    """AILinter Worker - Kod analizi işleyicisi"""
    
    def __init__(self):
        self.running = True
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self) -> None:
        """Sinyal işleyicilerini ayarla"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame) -> None:
        """Sinyal işleyici - graceful shutdown"""
        logger.info(f"Sinyal alındı: {signum}, worker durduruluyor...")
        self.running = False
        rabbitmq_worker.stop_consuming()
    
    def process_analysis_message(self, message: Dict[str, Any]) -> None:
        """
        Analiz mesajını işle
        
        Args:
            message: RabbitMQ'dan gelen mesaj
        """
        try:
            # Mesaj verilerini al
            analysis_id = message.get('analysisId')
            code = message.get('code', '')
            language = message.get('language', 'javascript')
            fileName = message.get('fileName', 'code.txt')
            
            if not analysis_id:
                logger.error("Analysis ID bulunamadı")
                return
            
            logger.info(f"Analiz başlatılıyor: {analysis_id}")
            
            # Durumu "processing" olarak güncelle
            redis_worker.update_status(analysis_id, "processing")
            
            # Gemini API ile kod analizi yap
            analysis_result = gemini_service.analyze_code(
                code=code,
                language=language,
                fileName=fileName
            )
            
            # Sonucu Redis'e kaydet
            success = redis_worker.save_analysis_result(
                analysis_id=analysis_id,
                result=analysis_result,
                original_data=message
            )
            
            if success:
                logger.info(f"Analiz başarıyla tamamlandı: {analysis_id}")
            else:
                logger.error(f"Analiz sonucu kaydedilemedi: {analysis_id}")
                # Hata durumunu kaydet
                redis_worker.save_error_result(
                    analysis_id=analysis_id,
                    error_message="Analiz sonucu kaydedilemedi",
                    original_data=message
                )
                
        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {str(e)}")
            
            # Hata durumunu kaydet
            analysis_id = message.get('analysisId')
            if analysis_id:
                redis_worker.save_error_result(
                    analysis_id=analysis_id,
                    error_message=str(e),
                    original_data=message
                )
    
    def start(self) -> None:
        """Worker'ı başlat"""
        try:
            logger.info(f"AILinter Worker başlatılıyor: {settings.WORKER_NAME}")
            logger.info("RabbitMQ kuyruğu dinleniyor...")
            
            # RabbitMQ kuyruğunu dinlemeye başla
            rabbitmq_worker.start_consuming(self.process_analysis_message)
            
        except KeyboardInterrupt:
            logger.info("Worker kullanıcı tarafından durduruldu")
        except Exception as e:
            logger.error(f"Worker hatası: {str(e)}")
        finally:
            self.shutdown()
    
    def shutdown(self) -> None:
        """Worker'ı kapat"""
        try:
            logger.info("Worker kapatılıyor...")
            
            # Bağlantıları kapat
            rabbitmq_worker.close_connection()
            redis_worker.close_connection()
            
            logger.info("Worker başarıyla kapatıldı")
            
        except Exception as e:
            logger.error(f"Worker kapatma hatası: {str(e)}")

def main():
    """Ana fonksiyon"""
    try:
        # Worker'ı oluştur ve başlat
        worker = AILinterWorker()
        worker.start()
        
    except Exception as e:
        logger.error(f"Worker başlatma hatası: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 