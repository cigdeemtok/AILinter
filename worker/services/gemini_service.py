import google.generativeai as genai
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    """Gemini API ile kod analizi servisi"""
    
    def __init__(self):
        self.model = None
        self._setup_gemini()
    
    def _setup_gemini(self) -> None:
        """Gemini API'yi yapılandır"""
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY ortam değişkeni bulunamadı")
            
            # Gemini API'yi yapılandır
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Model seç (gemini-1.5-flash daha hızlı ve daha az quota kullanır)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            logger.info("Gemini API başarıyla yapılandırıldı")
            
        except Exception as e:
            logger.error(f"Gemini API yapılandırma hatası: {str(e)}")
            raise
    
    def analyze_code(self, code: str, language: str, fileName: str = "code.txt") -> Dict[str, Any]:
        """
        Kodu Gemini API ile analiz et
        
        Args:
            code: Analiz edilecek kod
            language: Programlama dili
            fileName: Dosya adı
            
        Returns:
            Analiz sonucu dictionary
        """
        try:
            # Analiz prompt'unu hazırla
            prompt = self._create_analysis_prompt(code, language, fileName)
            
            # Gemini API'ye istek gönder
            response = self.model.generate_content(prompt)
            
            # Yanıtı parse et
            analysis_result = self._parse_gemini_response(response.text)
            
            logger.info(f"Kod analizi tamamlandı: {fileName}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Kod analizi hatası: {str(e)}")
            
            # Quota hatası kontrolü
            if "quota" in str(e).lower() or "rate limit" in str(e).lower():
                logger.error("Gemini API quota'sı dolmuş. Lütfen daha sonra tekrar deneyin.")
                return self._create_quota_error_result()
            
            # Hata durumunda boş sonuç döndür
            return self._create_empty_result()
    
    def _create_analysis_prompt(self, code: str, language: str, fileName: str) -> str:
        """Analiz için prompt oluştur"""
        return f"""
Kodu incele ve şu 4 kategoride öneriler sun:

**Dosya:** {fileName}
**Dil:** {language}

**Kod:**
```{language}
{code}
```

**Analiz Kategorileri:**

1) **Hatalar/Buglar**: Syntax hataları, mantık hataları, runtime hataları
2) **Güvenlik Açıkları**: SQL injection, XSS, CSRF, input validation sorunları
3) **Refactor Önerileri**: Kod iyileştirmeleri, performans optimizasyonları, best practices
4) **Okunabilirlik**: Kod okunabilirliği, yorum eksiklikleri, değişken isimlendirme

**Yanıt Formatı (JSON):**
{{
    "errors": ["Hata 1", "Hata 2"],
    "security": ["Güvenlik açığı 1", "Güvenlik açığı 2"],
    "refactor": ["Refactor önerisi 1", "Refactor önerisi 2"],
    "readability": ["Okunabilirlik önerisi 1", "Okunabilirlik önerisi 2"]
}}

Sadece JSON formatında yanıt ver, başka açıklama ekleme.
"""
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Gemini yanıtını parse et"""
        try:
            # JSON formatını bul
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.warning("JSON formatı bulunamadı, boş sonuç döndürülüyor")
                return self._create_empty_result()
            
            json_text = response_text[start_idx:end_idx]
            parsed_response = json.loads(json_text)
            
            # Gerekli alanları kontrol et
            required_fields = ['errors', 'security', 'refactor', 'readability']
            for field in required_fields:
                if field not in parsed_response:
                    parsed_response[field] = []
            
            return parsed_response
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse hatası: {str(e)}")
            return self._create_empty_result()
        except Exception as e:
            logger.error(f"Yanıt parse hatası: {str(e)}")
            return self._create_empty_result()
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """Boş analiz sonucu oluştur"""
        return {
            "errors": [],
            "security": [],
            "refactor": [],
            "readability": []
        }
    
    def _create_quota_error_result(self) -> Dict[str, Any]:
        """Quota hatası sonucu oluştur"""
        return {
            "errors": ["⚠️ Gemini API quota'sı dolmuş. Lütfen birkaç dakika bekleyip tekrar deneyin."],
            "security": [],
            "refactor": [],
            "readability": []
        }

# Global Gemini servis instance'ı
gemini_service = GeminiService() 