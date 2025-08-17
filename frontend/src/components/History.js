import React, { useState } from 'react';

const History = ({ onSelectAnalysis, historyData = [], theme }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`${theme.colors.card} rounded-lg shadow-sm border ${theme.colors.border} p-6 transition-colors duration-200`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-blue-50">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className={`text-lg font-semibold ${theme.colors.text.primary}`}>Geçmiş Analizler</h3>
            <p className={`text-sm ${theme.colors.text.secondary}`}>{historyData.length} analiz bulundu</p>
          </div>
        </div>
        
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className={`p-2 rounded-lg ${theme.colors.button.secondary} transition-colors`}
        >
          <svg 
            className={`w-4 h-4 ${theme.colors.text.secondary} transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {isExpanded && (
        <div className="space-y-3">
                     {historyData.length === 0 ? (
             <div className="text-center py-8">
               <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${theme.colors.text.muted} mb-4`}>
                 <svg className={`w-8 h-8 ${theme.colors.text.muted}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                 </svg>
               </div>
               <p className={theme.colors.text.secondary}>Henüz analiz geçmişi bulunmuyor.</p>
               <p className={`text-sm ${theme.colors.text.muted} mt-1`}>İlk analizinizi yaparak başlayın!</p>
             </div>
           ) : (
             historyData.map((item) => (
               <div 
                 key={item.id}
                 onClick={() => onSelectAnalysis(item)}
                 className={`p-4 border ${theme.colors.border} rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors`}
               >
                 <div className="flex items-center justify-between mb-2">
                   <span className={`text-sm font-medium ${theme.colors.text.primary}`}>
                     {item.fileName || 'Kod Analizi'}
                   </span>
                   <span className={`text-xs ${theme.colors.text.muted}`}>
                     {new Date(item.createdAt).toLocaleString('tr-TR')}
                   </span>
                 </div>
                 <div className={`text-sm ${theme.colors.text.secondary} mb-2 font-mono ${theme.colors.input.background} p-2 rounded text-xs`}>
                   {item.code.substring(0, 100)}...
                 </div>
                                   <div className={`text-xs ${theme.colors.text.muted}`}>
                    {item.language.toUpperCase()} • {item.errors.length + item.security.length + item.refactor.length + item.readability.length} öneri
                  </div>
                  {/* Öneri Özeti */}
                  <div className="mt-2 space-y-1">
                    {item.errors.length > 0 && (
                      <div className={`text-xs px-2 py-1 rounded ${theme.colors.text.muted} bg-red-50 dark:bg-red-900/20`}>
                        🚨 {item.errors.length} hata
                      </div>
                    )}
                    {item.security.length > 0 && (
                      <div className={`text-xs px-2 py-1 rounded ${theme.colors.text.muted} bg-orange-50 dark:bg-orange-900/20`}>
                        🔒 {item.security.length} güvenlik
                      </div>
                    )}
                    {item.refactor.length > 0 && (
                      <div className={`text-xs px-2 py-1 rounded ${theme.colors.text.muted} bg-blue-50 dark:bg-blue-900/20`}>
                        🔧 {item.refactor.length} refactor
                      </div>
                    )}
                    {item.readability.length > 0 && (
                      <div className={`text-xs px-2 py-1 rounded ${theme.colors.text.muted} bg-green-50 dark:bg-green-900/20`}>
                        📖 {item.readability.length} okunabilirlik
                      </div>
                    )}
                  </div>
               </div>
             ))
           )}
        </div>
      )}

      {!isExpanded && (
        <div className={`text-sm ${theme.colors.text.secondary}`}>
          Geçmiş analizleri görmek için genişletin.
        </div>
      )}
    </div>
  );
};

export default History; 