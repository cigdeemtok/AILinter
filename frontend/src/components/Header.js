import React from 'react';

const Header = ({ onThemeToggle, theme, currentTheme }) => {
  return (
    <header className={`${theme.colors.header} shadow-sm border-b ${theme.colors.border} transition-colors duration-200`}>
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h1 className={`text-2xl font-bold ${theme.colors.text.primary}`}>AILinter</h1>
              <p className={`text-sm ${theme.colors.text.secondary}`}>Kod Analizi ve Öneriler Platformu</p>
            </div>
          </div>
          
          <button
            onClick={onThemeToggle}
            className={`relative inline-flex h-8 w-16 items-center rounded-full transition-colors duration-200 ${currentTheme === 'night' ? 'bg-primary-600' : 'bg-gray-200'}`}
            title="Tema Değiştir"
          >
            <span className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform duration-200 flex items-center justify-center ${currentTheme === 'night' ? 'translate-x-8' : 'translate-x-1'}`}>
              {currentTheme === 'day' ? (
                <svg className="w-3 h-3 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-3 h-3 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              )}
            </span>
            <span className="sr-only">Tema Değiştir</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header; 