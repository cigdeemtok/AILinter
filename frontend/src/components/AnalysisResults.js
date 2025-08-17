import React from 'react';
import ResultCard from './ResultCard';

const AnalysisResults = ({ result, theme }) => {
  // Kategori konfigürasyonları
  const categories = [
    {
      key: 'errors',
      title: 'Hatalar / Buglar',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      color: 'red',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      textColor: 'text-red-800'
    },
    {
      key: 'security',
      title: 'Güvenlik Açıkları',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
      color: 'orange',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200',
      textColor: 'text-orange-800'
    },
    {
      key: 'refactor',
      title: 'Refactor Önerileri',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
      color: 'blue',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      textColor: 'text-blue-800'
    },
    {
      key: 'readability',
      title: 'Okunabilirlik İyileştirmeleri',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: 'green',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      textColor: 'text-green-800'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Başlık */}
      <div className={`${theme.colors.card} rounded-lg shadow-sm border ${theme.colors.border} p-6 transition-colors duration-200`}>
        <div className="flex items-center justify-between">
          <div>
            <h2 className={`text-xl font-semibold ${theme.colors.text.primary}`}>
              Analiz Sonuçları
            </h2>
            <p className={`${theme.colors.text.secondary} mt-1`}>
              Kodunuz analiz edildi. Aşağıda bulunan kategorilerde öneriler sunulmuştur.
            </p>
          </div>
          <div className="text-right">
            <div className={`text-sm ${theme.colors.text.muted}`}>Analiz ID</div>
            <div className={`font-mono text-sm ${theme.colors.text.primary}`}>{result.id}</div>
          </div>
        </div>
      </div>

      {/* Sonuç Kartları */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {categories.map((category) => (
          <ResultCard
            key={category.key}
            category={category}
            items={result[category.key] || []}
            theme={theme}
          />
        ))}
      </div>

      {/* Özet Bilgi */}
      <div className={`${theme.colors.card} rounded-lg shadow-sm border ${theme.colors.border} p-6 transition-colors duration-200`}>
        <h3 className={`text-lg font-medium ${theme.colors.text.primary} mb-4`}>Analiz Özeti</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {categories.map((category) => {
            const itemCount = result[category.key]?.length || 0;
            return (
              <div key={category.key} className="text-center">
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full ${category.bgColor} ${category.borderColor} border-2`}>
                  {React.cloneElement(category.icon, { className: `w-6 h-6 ${category.textColor}` })}
                </div>
                <div className="mt-2">
                  <div className={`text-2xl font-bold ${theme.colors.text.primary}`}>{itemCount}</div>
                  <div className={`text-sm ${theme.colors.text.secondary}`}>{category.title}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults; 