// Tema Konfigürasyonları
export const themes = {
  // Day Mode (Gündüz Modu)
  day: {
    name: 'Gündüz Modu',
    colors: {
      primary: {
        50: '#eff6ff',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
      },
      background: 'bg-gray-50',
      header: 'bg-white',
      card: 'bg-white',
      border: 'border-gray-200',
      text: {
        primary: 'text-gray-900',
        secondary: 'text-gray-600',
        muted: 'text-gray-500'
      },
      input: {
        background: 'bg-white',
        border: 'border-gray-300',
        text: 'text-gray-900',
        placeholder: 'placeholder-gray-500'
      },
      button: {
        primary: 'bg-primary-600 hover:bg-primary-700 text-white',
        secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-700',
        disabled: 'bg-gray-300 text-gray-500 cursor-not-allowed'
      }
    },
    categories: {
      errors: {
        bgColor: 'bg-red-50',
        borderColor: 'border-red-200',
        textColor: 'text-red-800',
        iconColor: 'text-red-600'
      },
      security: {
        bgColor: 'bg-orange-50',
        borderColor: 'border-orange-200',
        textColor: 'text-orange-800',
        iconColor: 'text-orange-600'
      },
      refactor: {
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-200',
        textColor: 'text-blue-800',
        iconColor: 'text-blue-600'
      },
      readability: {
        bgColor: 'bg-green-50',
        borderColor: 'border-green-200',
        textColor: 'text-green-800',
        iconColor: 'text-green-600'
      }
    }
  },

  // Night Mode (Gece Modu)
  night: {
    name: 'Gece Modu',
    colors: {
      primary: {
        50: '#1e293b',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
      },
      background: 'bg-black',
      header: 'bg-gray-900',
      card: 'bg-gray-900',
      border: 'border-gray-800',
      text: {
        primary: 'text-white',
        secondary: 'text-gray-200',
        muted: 'text-gray-400'
      },
      input: {
        background: 'bg-gray-800',
        border: 'border-gray-700',
        text: 'text-white',
        placeholder: 'placeholder-gray-400'
      },
      button: {
        primary: 'bg-primary-600 hover:bg-primary-700 text-white',
        secondary: 'bg-gray-800 hover:bg-gray-700 text-gray-200',
        disabled: 'bg-gray-700 text-gray-500 cursor-not-allowed'
      }
    },
    categories: {
      errors: {
        bgColor: 'bg-red-900/30',
        borderColor: 'border-red-600',
        textColor: 'text-red-200',
        iconColor: 'text-red-300'
      },
      security: {
        bgColor: 'bg-orange-900/30',
        borderColor: 'border-orange-600',
        textColor: 'text-orange-200',
        iconColor: 'text-orange-300'
      },
      refactor: {
        bgColor: 'bg-blue-900/30',
        borderColor: 'border-blue-600',
        textColor: 'text-blue-200',
        iconColor: 'text-blue-300'
      },
      readability: {
        bgColor: 'bg-green-900/30',
        borderColor: 'border-green-600',
        textColor: 'text-green-200',
        iconColor: 'text-green-300'
      }
    }
  }
};

export default themes; 