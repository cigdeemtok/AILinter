import React, { useState } from 'react';
import CodeAnalyzer from './components/CodeAnalyzer';
import AnalysisResults from './components/AnalysisResults';
import Header from './components/Header';
import History from './components/History';

import { themes } from './themes';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [historyData, setHistoryData] = useState([]);
  const [currentTheme, setCurrentTheme] = useState('day');


  // Analiz sonucunu güncelleme fonksiyonu
  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    setError(null);
    
    // Geçmişe yeni analizi ekle (her analizden sonra)
    const newHistoryItem = {
      ...result,
      analysisId: result.id
    };
    setHistoryData(prev => [newHistoryItem, ...prev]);
  };

  // Hata durumunu güncelleme fonksiyonu
  const handleError = (errorMessage) => {
    setError(errorMessage);
    setAnalysisResult(null);
  };

  // Yükleme durumunu güncelleme fonksiyonu
  const handleLoadingChange = (loading) => {
    setIsLoading(loading);
  };

  // Geçmiş analiz seçimi
  const handleSelectAnalysis = (selectedAnalysis) => {
    setAnalysisResult(selectedAnalysis);
    setError(null);
  };



  const theme = themes[currentTheme];

  return (
    <div className={`min-h-screen ${theme.colors.background} transition-colors duration-200`}>
      <Header onThemeToggle={() => setCurrentTheme(currentTheme === 'day' ? 'night' : 'day')} theme={theme} currentTheme={currentTheme} />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="space-y-8">
          {/* Geçmiş Analizler */}
          <History onSelectAnalysis={handleSelectAnalysis} historyData={historyData} theme={theme} />
          
          {/* Kod Analizi Bölümü */}
          <CodeAnalyzer 
            onAnalysisComplete={handleAnalysisComplete}
            onError={handleError}
            onLoadingChange={handleLoadingChange}
            isLoading={isLoading}
            theme={theme}
          />

          {/* Hata Mesajı */}
          {error && (
            <div className={`${theme.colors.card} border border-red-200 rounded-lg p-4`}>
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className={`text-sm font-medium ${theme.colors.text.primary}`}>
                    Analiz Hatası
                  </h3>
                  <div className={`mt-2 text-sm ${theme.colors.text.secondary}`}>
                    {error}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Analiz Sonuçları */}
          {analysisResult && (
            <AnalysisResults result={analysisResult} theme={theme} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App; 