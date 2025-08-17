import React, { useState } from 'react';
import axios from 'axios';
import API_CONFIG from '../config/api';

// Axios instance oluştur
const api = axios.create(API_CONFIG);

const CodeAnalyzer = ({ onAnalysisComplete, onError, onLoadingChange, isLoading, theme }) => {
  const [code, setCode] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('javascript');
  const [fileName, setFileName] = useState('');
  const [inputMethod, setInputMethod] = useState('text'); // 'text' veya 'file'

  // Dosya okuma fonksiyonu
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      const reader = new FileReader();
      reader.onload = (e) => {
        setCode(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  // Kod analizi gönderme fonksiyonu
  const handleAnalyze = async () => {
    if (!code.trim()) {
      onError('Lütfen analiz edilecek kodu girin.');
      return;
    }

    try {
      onLoadingChange(true);
      onError(null);

      // POST /analyze endpoint'ine istek gönder
      const response = await api.post('/analyze', {
        code: code.trim(),
        language: selectedLanguage,
        fileName: fileName || 'code.txt'
      });

      const { analysisId } = response.data;
      
      console.log('Backend response:', response.data);
      console.log('Analysis ID:', analysisId);

      // Analiz tamamlanana kadar sonucu bekle
      await waitForResult(analysisId);

    } catch (error) {
      console.error('Analiz hatası:', error);
      onError(
        error.response?.data?.message || 
        'Kod analizi sırasında bir hata oluştu. Lütfen tekrar deneyin.'
      );
    } finally {
      onLoadingChange(false);
    }
  };

  // Analiz sonucunu bekleme fonksiyonu
  const waitForResult = async (analysisId) => {
    console.log('Starting polling for analysis ID:', analysisId);
    let attempts = 0;
    const maxAttempts = 60; // 60 saniye bekle
    const pollInterval = 2000; // 2 saniye aralıklarla kontrol et

    while (attempts < maxAttempts) {
             try {
         const response = await api.get(`/result/${analysisId}`);
         
         console.log('Polling response:', response.data);
         
                   // Eğer response varsa, analiz tamamlanmış demektir
          if (response.data && response.data.id) {
            console.log('Analysis completed, calling onAnalysisComplete with:', response.data);
            onAnalysisComplete(response.data);
            return;
          }
         
         // Henüz tamamlanmamış, bekle
         await new Promise(resolve => setTimeout(resolve, pollInterval));
         attempts++;
        
      } catch (error) {
        if (error.response?.status === 404) {
          // Henüz sonuç hazır değil, devam et
          await new Promise(resolve => setTimeout(resolve, pollInterval));
          attempts++;
        } else {
          throw error;
        }
      }
    }

    throw new Error('Analiz zaman aşımına uğradı. Lütfen tekrar deneyin.');
  };

  // Programlama dilleri listesi
  const languages = [
    { value: 'javascript', label: 'JavaScript', icon: '⚡' },
    { value: 'typescript', label: 'TypeScript', icon: '🔷' },
    { value: 'python', label: 'Python', icon: '🐍' },
    { value: 'java', label: 'Java', icon: '☕' },
    { value: 'cpp', label: 'C++', icon: '⚙️' },
    { value: 'csharp', label: 'C#', icon: '🎯' },
    { value: 'php', label: 'PHP', icon: '🐘' },
    { value: 'ruby', label: 'Ruby', icon: '💎' },
    { value: 'go', label: 'Go', icon: '🚀' },
    { value: 'rust', label: 'Rust', icon: '🦀' },
    { value: 'swift', label: 'Swift', icon: '🍎' },
    { value: 'kotlin', label: 'Kotlin', icon: '📱' },
    { value: 'scala', label: 'Scala', icon: '⚡' },
    { value: 'html', label: 'HTML', icon: '🌐' },
    { value: 'css', label: 'CSS', icon: '🎨' },
    { value: 'sql', label: 'SQL', icon: '🗄️' }
  ];

  return (
    <div className={`${theme.colors.card} rounded-lg shadow-sm border ${theme.colors.border} p-6 transition-colors duration-200`}>
      <div className="mb-6">
        <h2 className={`text-xl font-semibold ${theme.colors.text.primary} mb-2`}>
          Kod Analizi
        </h2>
        <p className={theme.colors.text.secondary}>
          Analiz etmek istediğiniz kodu aşağıdaki alana yapıştırın veya dosya yükleyin.
        </p>
      </div>

      <div className="space-y-6">
        {/* Giriş Yöntemi Seçimi */}
        <div>
          <label className={`block text-sm font-medium ${theme.colors.text.primary} mb-3`}>
            Giriş Yöntemi
          </label>
          <div className="flex space-x-4">
            <button
              onClick={() => setInputMethod('text')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                inputMethod === 'text' 
                  ? theme.colors.button.primary 
                  : theme.colors.button.secondary
              }`}
            >
              📝 Metin Girişi
            </button>
            <button
              onClick={() => setInputMethod('file')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                inputMethod === 'file' 
                  ? theme.colors.button.primary 
                  : theme.colors.button.secondary
              }`}
            >
              📁 Dosya Yükleme
            </button>
          </div>
        </div>

        {/* Programlama Dili Seçimi */}
        <div>
          <label htmlFor="language-select" className={`block text-sm font-medium ${theme.colors.text.primary} mb-2`}>
            Programlama Dili
          </label>
          <select
            id="language-select"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className={`w-full px-4 py-3 border ${theme.colors.input.border} rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${theme.colors.input.background} ${theme.colors.input.text} transition-colors duration-200`}
            disabled={isLoading}
          >
            {languages.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.icon} {lang.label}
              </option>
            ))}
          </select>
        </div>

        {/* Kod Girişi */}
        {inputMethod === 'text' ? (
          <div>
            <label htmlFor="code-input" className={`block text-sm font-medium ${theme.colors.text.primary} mb-2`}>
              Kod
            </label>
            <textarea
              id="code-input"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Analiz edilecek kodu buraya yapıştırın..."
              className={`w-full h-64 px-4 py-3 border ${theme.colors.input.border} rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none font-mono text-sm ${theme.colors.input.background} ${theme.colors.input.text} ${theme.colors.input.placeholder} transition-colors duration-200`}
              disabled={isLoading}
            />
          </div>
        ) : (
          <div>
            <label htmlFor="file-input" className={`block text-sm font-medium ${theme.colors.text.primary} mb-2`}>
              Dosya Yükleme
            </label>
            <div className={`border-2 border-dashed ${theme.colors.input.border} rounded-lg p-6 text-center transition-colors duration-200`}>
              <input
                id="file-input"
                type="file"
                accept=".js,.ts,.py,.java,.cpp,.cs,.php,.rb,.go,.rs,.swift,.kt,.scala,.html,.css,.sql,.txt"
                onChange={handleFileUpload}
                className="hidden"
                disabled={isLoading}
              />
              <label htmlFor="file-input" className={`cursor-pointer block ${theme.colors.text.secondary}`}>
                <div className="mb-4">
                  <svg className={`w-12 h-12 mx-auto ${theme.colors.text.muted}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <div className="text-lg font-medium mb-2">
                  Dosya seçmek için tıklayın
                </div>
                <div className="text-sm">
                  Desteklenen formatlar: .js, .ts, .py, .java, .cpp, .cs, .php, .rb, .go, .rs, .swift, .kt, .scala, .html, .css, .sql, .txt
                </div>
                {fileName && (
                  <div className={`mt-4 p-2 ${theme.colors.input.background} rounded-lg`}>
                    <div className={`text-sm font-medium ${theme.colors.text.primary}`}>
                      Seçilen dosya: {fileName}
                    </div>
                    <div className={`text-xs ${theme.colors.text.secondary} mt-1`}>
                      {code.length} karakter
                    </div>
                  </div>
                )}
              </label>
            </div>
          </div>
        )}

        {/* Analiz Butonu */}
        <div className="flex justify-between items-center">
          <div className={`text-sm ${theme.colors.text.secondary}`}>
            {code.length > 0 && (
              <span>
                {code.length} karakter • {selectedLanguage.toUpperCase()}
                {fileName && ` • ${fileName}`}
              </span>
            )}
          </div>
          <button
            onClick={handleAnalyze}
            disabled={isLoading || !code.trim()}
            className={`
              px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2
              ${isLoading || !code.trim()
                ? theme.colors.button.disabled
                : theme.colors.button.primary
              }
            `}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Analiz Ediliyor...</span>
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Analiz Et</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CodeAnalyzer; 