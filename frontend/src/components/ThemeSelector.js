import React from 'react';
import { themes } from '../themes';

const ThemeSelector = ({ currentTheme, onThemeChange, theme }) => {
  return (
    <div className={`${theme.colors.card} rounded-lg shadow-sm border ${theme.colors.border} p-6 transition-colors duration-200`}>
      <div className="mb-4">
        <h3 className={`text-lg font-semibold ${theme.colors.text.primary}`}>Tema Seçimi</h3>
        <p className={`text-sm ${theme.colors.text.secondary}`}>Arayüzünüzün görünümünü özelleştirin</p>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(themes).map(([key, themeOption]) => (
          <button
            key={key}
            onClick={() => onThemeChange(key)}
            className={`
              p-6 rounded-lg border-2 transition-all duration-200
              ${currentTheme === key 
                ? 'border-primary-500 bg-primary-50' 
                : 'border-gray-200 hover:border-gray-300'
              }
            `}
          >
            <div className="text-center">
              <div className="w-16 h-12 rounded mb-3 mx-auto flex items-center justify-center">
                {key === 'day' && (
                  <div className="w-full h-full bg-gradient-to-r from-yellow-400 to-orange-500 rounded flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                )}
                {key === 'night' && (
                  <div className="w-full h-full bg-gradient-to-r from-gray-800 to-gray-900 rounded flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                  </div>
                )}
              </div>
              <div className={`text-sm font-medium ${theme.colors.text.primary}`}>{themeOption.name}</div>
              <div className={`text-xs ${theme.colors.text.muted} mt-1`}>
                {currentTheme === key ? 'Aktif' : 'Seç'}
              </div>
            </div>
          </button>
        ))}
      </div>
      
      <div className={`mt-4 p-3 ${theme.colors.text.muted} rounded-lg`}>
        <div className={`text-xs ${theme.colors.text.secondary}`}>
          <strong>Özellikler:</strong>
          <ul className="mt-1 space-y-1">
            <li>• <strong>Gündüz Modu:</strong> Parlak ve net görünüm</li>
            <li>• <strong>Gece Modu:</strong> Göz yorgunluğunu azaltır</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ThemeSelector; 