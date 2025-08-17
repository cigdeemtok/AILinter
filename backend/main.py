import uuid
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import AnalysisRequest, AnalysisResponse, AnalysisResult, AnalysisStatus
from services.redis_service import redis_service
from services.gemini_service import gemini_service
from services.rabbitmq_service import rabbitmq_service
from config import settings

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="AILinter API",
    description="Kod analizi için REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik origin'ler belirt
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında çalışacak event"""
    logger.info("AILinter API başlatıldı")

@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapatıldığında çalışacak event"""
    logger.info("AILinter API kapatılıyor...")
    try:
        rabbitmq_service.close_connection()
    except:
        pass
    redis_service.close_connection()

@app.get("/")
async def root():
    """Ana endpoint - API durumu"""
    return {
        "message": "AILinter API çalışıyor",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    try:
        # Redis bağlantısını kontrol et
        redis_service.redis_client.ping()
        
        # RabbitMQ bağlantısını kontrol et (opsiyonel)
        try:
            if rabbitmq_service.connection and not rabbitmq_service.connection.is_closed:
                rabbitmq_status = "connected"
            else:
                rabbitmq_status = "disconnected"
        except:
            rabbitmq_status = "disconnected"
        
        return {
            "status": "healthy",
            "redis": "connected",
            "rabbitmq": rabbitmq_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servis sağlıksız"
        )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest):
    """
    Kod analizi endpoint'i
    - Gelen kodu alır
    - UUID üretir
    - RabbitMQ kuyruğuna mesaj atar
    - Analysis ID'yi döner
    """
    if not request.code or not str(request.code).strip():
        raise HTTPException(status_code=400, detail="Kod boş olamaz")
    try:
        # UUID üret
        analysis_id = str(uuid.uuid4())
        # Mesajı hazırla
        message = {
            "analysisId": analysis_id,
            "code": request.code,
            "language": request.language.value,
            "fileName": request.fileName
        }
        # RabbitMQ'ya mesaj gönder
        success = rabbitmq_service.send_message(message)
        if not success:
            raise HTTPException(status_code=500, detail="RabbitMQ mesajı gönderilemedi")
        return AnalysisResponse(
            analysisId=analysis_id,
            message="Analiz kuyruğa eklendi"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analiz hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analiz kuyruğa eklenemedi"
        )

@app.get("/result/{analysis_id}", response_model=AnalysisResult)
async def get_analysis_result(analysis_id: str):
    """
    Analiz sonucu alma endpoint'i
    
    - Redis'ten `result:{id}` key'i ile analiz sonucunu getirir
    - Sonuç yoksa 404 döner
    """
    try:
        # Redis'ten sonucu getir
        result = redis_service.get_analysis_result(analysis_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analiz sonucu bulunamadı: {analysis_id}"
            )
        
        # Pydantic model'e dönüştür
        analysis_result = AnalysisResult(**result)
        
        logger.info(f"Analiz sonucu getirildi: {analysis_id}")
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sonuç getirme hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analiz sonucu alınamadı"
        )

@app.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """
    Analiz durumu alma endpoint'i
    
    - Redis'ten `status:{id}` key'i ile durumu getirir
    - Sadece durum bilgisini döner
    """
    try:
        status = redis_service.get_analysis_status(analysis_id)
        
        if not status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analiz durumu bulunamadı: {analysis_id}"
            )
        
        return {
            "analysisId": analysis_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Durum getirme hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analiz durumu alınamadı"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Beklenmeyen hata: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "İç sunucu hatası"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 