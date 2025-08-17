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
            # Hata durumunda boş sonuç döndür
            return self._create_empty_result()
    
    def _create_analysis_prompt(self, code: str, language: str, fileName: str) -> str:
        """Analiz için prompt oluştur"""
        return f"""
Bu {language} kodunu analiz et ve 4 kategoride detaylı öneriler sun. Her öneri için açık bir açıklama ver.

Kod:
```{language}
{code}
```

Sadece bu alanları içeren bir JSON objesi döndür:
{{
    "errors": ["detaylı hata açıklamaları"],
    "security": ["detaylı güvenlik açığı açıklamaları"],
    "refactor": ["detaylı refactor önerileri ve açıklamaları"],
    "readability": ["detaylı okunabilirlik iyileştirme önerileri"]
}}

Her öneri, sorunu ve nasıl düzeltileceğini açıklayan tam bir cümle olmalı.
Sadece JSON döndür, başka metin yok.
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

# Global Gemini servis instance'ı
gemini_service = GeminiService() 