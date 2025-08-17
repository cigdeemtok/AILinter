import json
import redis
from typing import Optional, Dict, Any
from config import settings
import logging

logger = logging.getLogger(__name__)

class RedisService:
    """Redis bağlantı ve veri işlemleri servisi"""
    
    def __init__(self):
        self.redis_client = None
        self._connect()
    
    def _connect(self) -> None:
        """Redis'e bağlan"""
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,  # String'leri otomatik decode et
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Bağlantıyı test et
            self.redis_client.ping()
            logger.info(f"Redis'e başarıyla bağlandı: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            
        except Exception as e:
            logger.error(f"Redis bağlantı hatası: {str(e)}")
            raise
    
    def set_analysis_result(self, analysis_id: str, result: Dict[str, Any], expire_seconds: int = 3600) -> bool:
        """Analiz sonucunu Redis'e kaydet"""
        try:
            key = f"result:{analysis_id}"
            value = json.dumps(result, ensure_ascii=False)
            
            self.redis_client.setex(
                key,
                expire_seconds,  # 1 saat sonra expire olsun
                value
            )
            
            logger.info(f"Analiz sonucu kaydedildi: {analysis_id}")
            return True
            
        except Exception as e:
            logger.error(f"Redis kaydetme hatası: {str(e)}")
            return False
    
    def get_analysis_result(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Analiz sonucunu Redis'ten getir"""
        try:
            key = f"result:{analysis_id}"
            value = self.redis_client.get(key)
            
            if value:
                result = json.loads(value)
                logger.info(f"Analiz sonucu getirildi: {analysis_id}")
                return result
            else:
                logger.warning(f"Analiz sonucu bulunamadı: {analysis_id}")
                return None
                
        except Exception as e:
            logger.error(f"Redis okuma hatası: {str(e)}")
            return None
    
    def set_analysis_status(self, analysis_id: str, status: str, expire_seconds: int = 3600) -> bool:
        """Analiz durumunu Redis'e kaydet"""
        try:
            key = f"status:{analysis_id}"
            self.redis_client.setex(key, expire_seconds, status)
            logger.info(f"Analiz durumu kaydedildi: {analysis_id} - {status}")
            return True
            
        except Exception as e:
            logger.error(f"Durum kaydetme hatası: {str(e)}")
            return False
    
    def get_analysis_status(self, analysis_id: str) -> Optional[str]:
        """Analiz durumunu Redis'ten getir"""
        try:
            key = f"status:{analysis_id}"
            status = self.redis_client.get(key)
            
            if status:
                logger.info(f"Analiz durumu getirildi: {analysis_id} - {status}")
                return status
            else:
                logger.warning(f"Analiz durumu bulunamadı: {analysis_id}")
                return None
                
        except Exception as e:
            logger.error(f"Durum okuma hatası: {str(e)}")
            return None
    
    def delete_analysis_data(self, analysis_id: str) -> bool:
        """Analiz verilerini Redis'ten sil"""
        try:
            result_key = f"result:{analysis_id}"
            status_key = f"status:{analysis_id}"
            
            self.redis_client.delete(result_key, status_key)
            logger.info(f"Analiz verileri silindi: {analysis_id}")
            return True
            
        except Exception as e:
            logger.error(f"Veri silme hatası: {str(e)}")
            return False
    
    def close_connection(self) -> None:
        """Bağlantıyı kapat"""
        try:
            if self.redis_client:
                self.redis_client.close()
                logger.info("Redis bağlantısı kapatıldı")
        except Exception as e:
            logger.error(f"Bağlantı kapatma hatası: {str(e)}")

# Global Redis servis instance'ı
redis_service = RedisService() 