import React, { useState } from 'react';

const ResultCard = ({ category, items, theme }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // Boş sonuç durumu
  if (!items || items.length === 0) {
    return (
      <div className={`${theme.colors.card} rounded-lg shadow-sm border ${category.borderColor} p-6 transition-colors duration-200`}>
        <div className="flex items-center space-x-3 mb-4">
          <div className={`p-2 rounded-lg ${category.bgColor}`}>
            {React.cloneElement(category.icon, { className: `w-5 h-5 ${category.textColor}` })}
          </div>
          <h3 className={`text-lg font-semibold ${category.textColor}`}>
            {category.title}
          </h3>
        </div>
        
        <div className="text-center py-8">
          <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${category.bgColor} mb-4`}>
            <svg className={`w-8 h-8 ${category.textColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p className={theme.colors.text.secondary}>Bu kategoride herhangi bir öneri bulunamadı.</p>
          <p className={`text-sm ${theme.colors.text.muted} mt-1`}>Kodunuz bu açıdan iyi durumda görünüyor!</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`${theme.colors.card} rounded-lg shadow-sm border ${category.borderColor} p-6 transition-colors duration-200`}>
      {/* Kart Başlığı */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${category.bgColor}`}>
            {React.cloneElement(category.icon, { className: `w-5 h-5 ${category.textColor}` })}
          </div>
          <div>
            <h3 className={`text-lg font-semibold ${category.textColor}`}>
              {category.title}
            </h3>
            <p className={`text-sm ${theme.colors.text.secondary}`}>
              {items.length} öneri bulundu
            </p>
          </div>
        </div>
        
        {/* Genişlet/Daralt Butonu */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className={`p-2 rounded-lg ${category.bgColor} hover:bg-opacity-80 transition-colors`}
        >
          <svg 
            className={`w-4 h-4 ${category.textColor} transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* Öneriler Listesi */}
      {isExpanded && (
        <div className="space-y-4">
          {items.map((item, index) => (
            <div key={index} className="border-l-4 border-gray-200 pl-4 py-2">
              <div className="flex items-start space-x-3">
                <div className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${category.bgColor.replace('bg-', 'bg-').replace('-50', '-500')}`}></div>
                <div className="flex-1">
                  <h4 className={`font-medium ${theme.colors.text.primary} mb-1`}>
                    Öneri {index + 1}
                  </h4>
                  <p className={`${theme.colors.text.secondary} text-sm mb-2`}>
                    {typeof item === 'string' ? item : item.description || item.message || 'Öneri detayı'}
                  </p>
                  
                                     {/* Kod Bloğu (varsa) */}
                   {item.code && (
                     <div className={`${theme.colors.input.background} rounded-md p-3 mb-2`}>
                       <pre className={`text-xs ${theme.colors.input.text} overflow-x-auto`}>
                         <code>{item.code}</code>
                       </pre>
                     </div>
                   )}
                  
                                     {/* Satır Numarası (varsa) */}
                   {item.line && (
                     <div className={`text-xs ${theme.colors.text.muted}`}>
                       Satır: {item.line}
                     </div>
                   )}
                  
                  {/* Önerilen Çözüm (varsa) */}
                  {item.suggestion && (
                    <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-md">
                      <div className="text-sm font-medium text-green-800 mb-1">
                        Önerilen Çözüm:
                      </div>
                      <div className="text-sm text-green-700">
                        {item.suggestion}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Özet Bilgi (daraltılmış durumda) */}
      {!isExpanded && (
        <div className={`text-sm ${theme.colors.text.secondary}`}>
          Önerileri görmek için genişletin.
        </div>
      )}
    </div>
  );
};

export default ResultCard; 