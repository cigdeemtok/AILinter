# AILinter Docker Başlatma Scripti
# Bu script infra klasöründen çalıştırılmalı

Write-Host "🚀 AILinter Docker Servisleri Başlatılıyor..." -ForegroundColor Green

# .env dosyasını kontrol et
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env dosyası bulunamadı!" -ForegroundColor Yellow
    Write-Host "📝 env.example dosyasını .env olarak kopyalayın ve GEMINI_API_KEY ekleyin" -ForegroundColor Cyan
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env"
        Write-Host "✅ env.example .env olarak kopyalandı" -ForegroundColor Green
        Write-Host "🔑 Lütfen .env dosyasına GEMINI_API_KEY ekleyin" -ForegroundColor Yellow
        exit 1
    }
}

# Docker Compose ile servisleri başlat
Write-Host "🐳 Docker Compose başlatılıyor..." -ForegroundColor Blue
docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tüm servisler başarıyla başlatıldı!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Erişim Noktaları:" -ForegroundColor Cyan
    Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
    Write-Host "   RabbitMQ Management: http://localhost:15672" -ForegroundColor White
    Write-Host "   (guest/guest)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📊 Servis Durumu:" -ForegroundColor Cyan
    docker-compose ps
} else {
    Write-Host "❌ Servisler başlatılırken hata oluştu!" -ForegroundColor Red
    Write-Host "🔍 Logları kontrol edin: docker-compose logs" -ForegroundColor Yellow
} 