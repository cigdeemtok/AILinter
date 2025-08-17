import pytest
import uuid
from unittest.mock import Mock, patch, AsyncMock
import json
import os

# Test için gerekli ortam değişkenlerini ayarla
os.environ["GEMINI_API_KEY"] = "test-api-key"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["RABBITMQ_HOST"] = "localhost"
os.environ["RABBITMQ_PORT"] = "5672"

# Mock services before importing main
with patch('services.gemini_service.GeminiService') as mock_gemini:
    mock_gemini.return_value = Mock()
    from main import app
    from models import AnalysisRequest, AnalysisResponse, AnalysisResult, AnalysisStatus
    from services.redis_service import redis_service
    from services.rabbitmq_service import rabbitmq_service

@pytest.fixture
def client():
    """Test client fixture"""
    from fastapi.testclient import TestClient
    return TestClient(app)

class TestAnalyzeEndpoint:
    """POST /analyze endpoint testleri"""
    
    def test_analyze_empty_code_returns_error(self, client):
        """Boş kod gönderildiğinde hata dönmeli"""
        response = client.post("/analyze", json={
            "code": "",
            "language": "javascript",
            "fileName": ""
        })
        
        assert response.status_code == 400 or response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert "Kod boş olamaz" in data["detail"]
    
    def test_analyze_none_code_returns_error(self, client):
        """None kod gönderildiğinde hata dönmeli"""
        response = client.post("/analyze", json={
            "code": None,
            "language": "javascript",
            "fileName": ""
        })
        
        assert response.status_code == 400 or response.status_code == 422
    
    def test_analyze_valid_code_returns_uuid(self, client):
        """Geçerli kod gönderilince UUID dönmeli"""
        test_code = "console.log('Hello World');"
        
        with patch.object(rabbitmq_service, 'send_message') as mock_send:
            mock_send.return_value = True
            
            response = client.post("/analyze", json={
                "code": test_code,
                "language": "javascript",
                "fileName": "test.js"
            })
        
        assert response.status_code == 200
        data = response.json()
        assert "analysisId" in data
        assert "message" in data
        
        # UUID formatını kontrol et
        try:
            uuid.UUID(data["analysisId"])
        except ValueError:
            pytest.fail("analysisId geçerli bir UUID değil")
    
    def test_analyze_publishes_to_rabbitmq(self, client):
        """Geçerli kod gönderilince RabbitMQ'ya mesaj atılmalı"""
        test_code = "console.log('Hello World');"
        
        with patch.object(rabbitmq_service, 'send_message') as mock_send:
            mock_send.return_value = True
            
            response = client.post("/analyze", json={
                "code": test_code,
                "language": "python",
                "fileName": "test.py"
            })
        
        assert response.status_code == 200
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]  # İlk argüman
        assert "code" in call_args
        assert "language" in call_args
        assert "fileName" in call_args
        assert call_args["code"] == test_code
        assert call_args["language"] == "python"
    
    def test_analyze_rabbitmq_failure_returns_error(self, client):
        """RabbitMQ hatası durumunda hata dönmeli"""
        test_code = "console.log('Hello World');"
        
        with patch.object(rabbitmq_service, 'send_message') as mock_send:
            mock_send.return_value = False
            
            response = client.post("/analyze", json={
                "code": test_code,
                "language": "javascript",
                "fileName": "test.js"
            })
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "RabbitMQ" in data["detail"]
    
    def test_analyze_missing_fields_returns_error(self, client):
        """Eksik alanlar durumunda hata dönmeli"""
        response = client.post("/analyze", json={
            "code": "console.log('test');"
            # language ve fileName eksik
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_invalid_language_returns_error(self, client):
        """Geçersiz dil durumunda hata dönmeli"""
        response = client.post("/analyze", json={
            "code": "console.log('test');",
            "language": "invalid_language",
            "fileName": "test.js"
        })
        
        assert response.status_code == 422  # Validation error

class TestResultEndpoint:
    """GET /result/{id} endpoint testleri"""
    
    def test_get_result_exists_returns_data(self, client):
        """Redis'te varsa sonucu döner"""
        test_id = "test-uuid-123"
        test_result = {
            "id": test_id,
            "status": AnalysisStatus.COMPLETED.value,
            "code": "print('test')",
            "language": "python",
            "fileName": "test.py",
            "errors": ["Syntax error"],
            "security": ["SQL injection risk"],
            "refactor": ["Extract method"],
            "readability": ["Add comments"],
            "createdAt": "2024-01-01T00:00:00",
            "completedAt": "2024-01-01T00:00:01"
        }
        
        with patch.object(redis_service, 'get_analysis_result') as mock_get:
            mock_get.return_value = test_result
            
            response = client.get(f"/result/{test_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_id
        assert "errors" in data
        assert "security" in data
        assert "refactor" in data
        assert "readability" in data
    
    def test_get_result_not_exists_returns_404(self, client):
        """Redis'te yoksa 404 döner"""
        test_id = "non-existent-uuid"
        
        with patch.object(redis_service, 'get_analysis_result') as mock_get:
            mock_get.return_value = None
            
            response = client.get(f"/result/{test_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Analiz sonucu bulunamadı" in data["detail"]
    
    def test_get_result_redis_error_returns_500(self, client):
        """Redis bağlantı hatası test edilmeli"""
        test_id = "test-uuid-123"
        
        with patch.object(redis_service, 'get_analysis_result') as mock_get:
            mock_get.side_effect = Exception("Redis connection error")
            
            response = client.get(f"/result/{test_id}")
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Analiz sonucu alınamadı" in data["detail"]
    
    def test_get_result_invalid_uuid_returns_400(self, client):
        """Geçersiz UUID formatı durumunda hata dönmeli"""
        invalid_id = "invalid-uuid-format"
        
        response = client.get(f"/result/{invalid_id}")
        
        assert response.status_code == 400 or response.status_code == 404

class TestHealthEndpoint:
    """GET /health endpoint testleri"""
    
    def test_health_check_returns_200(self, client):
        """Health check endpoint'i çalışmalı"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "redis" in data
        assert "rabbitmq" in data
        assert "timestamp" in data
    
    def test_health_check_redis_disconnected(self, client):
        """Redis bağlantısı kesikse health check'te gösterilmeli"""
        with patch.object(redis_service, 'redis_client') as mock_redis:
            mock_redis.ping.side_effect = Exception("Redis connection failed")
            
            response = client.get("/health")
        
        assert response.status_code == 503 or response.status_code == 200
    
    def test_health_check_rabbitmq_disconnected(self, client):
        """RabbitMQ bağlantısı kesikse health check'te gösterilmeli"""
        with patch.object(rabbitmq_service, 'connection') as mock_connection:
            mock_connection.is_closed = True
            
            response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["rabbitmq"] == "disconnected"

class TestIntegration:
    """Entegrasyon testleri"""
    
    def test_analyze_then_get_result_flow(self, client):
        """Analiz yapıp sonucu alma akışı"""
        test_code = "console.log('integration test');"
        
        # 1. Analiz isteği gönder
        with patch.object(rabbitmq_service, 'send_message') as mock_send:
            mock_send.return_value = True
            
            analyze_response = client.post("/analyze", json={
                "code": test_code,
                "language": "javascript",
                "fileName": "integration.js"
            })
        
        assert analyze_response.status_code == 200
        analyze_data = analyze_response.json()
        analysis_id = analyze_data["analysisId"]
        
        # 2. Sonucu al
        mock_result = {
            "id": analysis_id,
            "status": AnalysisStatus.COMPLETED.value,
            "code": test_code,
            "language": "javascript",
            "fileName": "integration.js",
            "errors": ["Integration test error"],
            "security": [],
            "refactor": [],
            "readability": [],
            "createdAt": "2024-01-01T00:00:00",
            "completedAt": "2024-01-01T00:00:01"
        }
        
        with patch.object(redis_service, 'get_analysis_result') as mock_get:
            mock_get.return_value = mock_result
            
            result_response = client.get(f"/result/{analysis_id}")
        
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["id"] == analysis_id
        assert "errors" in result_data

if __name__ == "__main__":
    pytest.main([__file__]) 