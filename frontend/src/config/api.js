// API Konfigürasyonu
const API_CONFIG = {
  // Geliştirme ortamı için localhost
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  
  // Timeout ayarları
  timeout: 30000, // 30 saniye
  
  // Headers
  headers: {
    'Content-Type': 'application/json',
  }
};

export default API_CONFIG; 