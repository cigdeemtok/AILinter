from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class Language(str, Enum):
    """Desteklenen programlama dilleri"""
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    PHP = "php"
    RUBY = "ruby"
    GO = "go"
    RUST = "rust"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SCALA = "scala"
    HTML = "html"
    CSS = "css"
    SQL = "sql"

class AnalysisRequest(BaseModel):
    """Kod analizi isteği modeli"""
    code: str
    language: Language
    fileName: Optional[str] = "code.txt"
    
    class Config:
        schema_extra = {
            "example": {
                "code": "function hello() {\n  console.log('Hello World');\n}",
                "language": "javascript",
                "fileName": "app.js"
            }
        }

class AnalysisResponse(BaseModel):
    """Kod analizi yanıt modeli"""
    analysisId: str
    message: str = "Analiz başlatıldı"
    
    class Config:
        schema_extra = {
            "example": {
                "analysisId": "550e8400-e29b-41d4-a716-446655440000",
                "message": "Analiz başlatıldı"
            }
        }

class AnalysisStatus(str, Enum):
    """Analiz durumu enum'u"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AnalysisResult(BaseModel):
    """Analiz sonucu modeli"""
    id: str
    status: AnalysisStatus
    code: str
    language: Language
    fileName: Optional[str]
    errors: list = []
    security: list = []
    refactor: list = []
    readability: list = []
    error: Optional[str] = None
    createdAt: Optional[str] = None
    completedAt: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "code": "function hello() {\n  console.log('Hello World');\n}",
                "language": "javascript",
                "fileName": "app.js",
                "errors": ["Syntax error on line 2"],
                "security": ["Potential XSS vulnerability"],
                "refactor": ["Consider using const instead of let"],
                "readability": ["Add comments for better understanding"],
                "createdAt": "2024-01-01T12:00:00Z",
                "completedAt": "2024-01-01T12:00:05Z"
            }
        } 