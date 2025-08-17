import json
import redis
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

class RedisWorkerService:
    """Redis worker servisi - analiz sonuçlarını kaydeder"""
    
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
            logger.info(f"Redis Worker başarıyla bağlandı: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            
        except Exception as e:
            logger.error(f"Redis Worker bağlantı hatası: {str(e)}")
            raise
    
    def save_analysis_result(self, analysis_id: str, result: Dict[str, Any], 
                           original_data: Dict[str, Any]) -> bool:
        """Analiz sonucunu Redis'e kaydet"""
        try:
            # Tam sonuç verisini hazırla
            complete_result = {
                "id": analysis_id,
                "status": "completed",
                "code": original_data.get("code", ""),
                "language": original_data.get("language", ""),
                "fileName": original_data.get("fileName", ""),
                "errors": result.get("errors", []),
                "security": result.get("security", []),
                "refactor": result.get("refactor", []),
                "readability": result.get("readability", []),
                "createdAt": original_data.get("timestamp", datetime.now().isoformat()),
                "completedAt": datetime.now().isoformat()
            }
            
            # Redis'e kaydet
            key = f"result:{analysis_id}"
            value = json.dumps(complete_result, ensure_ascii=False)
            
            self.redis_client.setex(
                key,
                3600,  # 1 saat sonra expire olsun
                value
            )
            
            # Durumu da güncelle
            status_key = f"status:{analysis_id}"
            self.redis_client.setex(status_key, 3600, "completed")
            
            logger.info(f"Analiz sonucu kaydedildi: {analysis_id}")
            return True
            
        except Exception as e:
            logger.error(f"Redis kaydetme hatası: {str(e)}")
            return False
    
    def save_error_result(self, analysis_id: str, error_message: str, 
                         original_data: Dict[str, Any]) -> bool:
        """Hata sonucunu Redis'e kaydet"""
        try:
            # Hata sonucu verisini hazırla
            error_result = {
                "id": analysis_id,
                "status": "failed",
                "code": original_data.get("code", ""),
                "language": original_data.get("language", ""),
                "fileName": original_data.get("fileName", ""),
                "errors": [],
                "security": [],
                "refactor": [],
                "readability": [],
                "error": error_message,
                "createdAt": original_data.get("timestamp", datetime.now().isoformat()),
                "completedAt": datetime.now().isoformat()
            }
            
            # Redis'e kaydet
            key = f"result:{analysis_id}"
            value = json.dumps(error_result, ensure_ascii=False)
            
            self.redis_client.setex(
                key,
                3600,  # 1 saat sonra expire olsun
                value
            )
            
            # Durumu da güncelle
            status_key = f"status:{analysis_id}"
            self.redis_client.setex(status_key, 3600, "failed")
            
            logger.info(f"Hata sonucu kaydedildi: {analysis_id}")
            return True
            
        except Exception as e:
            logger.error(f"Redis hata kaydetme hatası: {str(e)}")
            return False
    
    def update_status(self, analysis_id: str, status: str) -> bool:
        """Analiz durumunu güncelle"""
        try:
            key = f"status:{analysis_id}"
            self.redis_client.setex(key, 3600, status)
            logger.info(f"Durum güncellendi: {analysis_id} - {status}")
            return True
        except Exception as e:
            logger.error(f"Durum güncelleme hatası: {str(e)}")
            return False
    
    def close_connection(self) -> None:
        """Bağlantıyı kapat"""
        try:
            if self.redis_client:
                self.redis_client.close()
                logger.info("Redis Worker bağlantısı kapatıldı")
        except Exception as e:
            logger.error(f"Bağlantı kapatma hatası: {str(e)}")

# Global Redis Worker servis instance'ı
redis_worker = RedisWorkerService() 