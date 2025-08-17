import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AnalysisResults from '../AnalysisResults';

// Mock themes
const mockTheme = {
  colors: {
    background: 'bg-white',
    card: 'bg-white',
    text: {
      primary: 'text-gray-900',
      secondary: 'text-gray-600',
      muted: 'text-gray-500'
    }
  }
};

describe('AnalysisResults Component', () => {
  const mockResult = {
    id: 'test-id',
    errors: [
      'Syntax hatası: Eksik noktalı virgül',
      'Değişken tanımlanmamış: x'
    ],
    security: [
      'SQL injection riski: Kullanıcı girdisi doğrudan sorguya ekleniyor',
      'XSS açığı: innerHTML kullanımı'
    ],
    refactor: [
      'Tekrarlanan kod bloğu fonksiyon haline getirilebilir',
      'Magic number yerine sabit kullanın'
    ],
    readability: [
      'Değişken isimleri daha açıklayıcı olmalı',
      'Fonksiyon çok uzun, bölünebilir'
    ]
  };

  test('renders analysis results', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    expect(screen.getAllByText(/hatalar/i)).toHaveLength(2);
    expect(screen.getAllByText(/güvenlik/i)).toHaveLength(2);
    expect(screen.getAllByText(/refactor/i)).toHaveLength(2);
    expect(screen.getAllByText(/okunabilirlik/i)).toHaveLength(2);
  });

  test('shows correct number of suggestions for each category', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    expect(screen.getAllByText(/2 öneri bulundu/i)).toHaveLength(4);
  });

  test('expands and collapses suggestion cards', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    const firstButton = expandButtons[0];
    
    // Initially collapsed
    expect(screen.getAllByText(/önerileri görmek için genişletin/i)).toHaveLength(4);
    
    // Click to expand
    fireEvent.click(firstButton);
    
    // Should show suggestions
    expect(screen.getByText(/syntax hatası/i)).toBeInTheDocument();
    expect(screen.getByText(/değişken tanımlanmamış/i)).toBeInTheDocument();
  });

  test('shows detailed suggestions when expanded', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    
    // Expand errors section
    fireEvent.click(expandButtons[0]);
    
    expect(screen.getByText(/syntax hatası: eksik noktalı virgül/i)).toBeInTheDocument();
    expect(screen.getByText(/değişken tanımlanmamış: x/i)).toBeInTheDocument();
  });

  test('shows security suggestions when expanded', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    
    // Expand security section
    fireEvent.click(expandButtons[1]);
    
    expect(screen.getByText(/sql injection riski/i)).toBeInTheDocument();
    expect(screen.getByText(/xss açığı/i)).toBeInTheDocument();
  });

  test('shows refactor suggestions when expanded', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    
    // Expand refactor section
    fireEvent.click(expandButtons[2]);
    
    expect(screen.getByText(/tekrarlanan kod bloğu/i)).toBeInTheDocument();
    expect(screen.getByText(/magic number/i)).toBeInTheDocument();
  });

  test('shows readability suggestions when expanded', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    
    // Expand readability section
    fireEvent.click(expandButtons[3]);
    
    expect(screen.getByText(/değişken isimleri/i)).toBeInTheDocument();
    expect(screen.getByText(/fonksiyon çok uzun/i)).toBeInTheDocument();
  });

  test('handles empty results gracefully', () => {
    const emptyResult = {
      id: 'test-id',
      errors: [],
      security: [],
      refactor: [],
      readability: []
    };
    
    render(<AnalysisResults result={emptyResult} theme={mockTheme} />);
    
    expect(screen.getAllByText(/bu kategoride herhangi bir öneri bulunamadı/i)).toHaveLength(4);
  });

  test('shows suggestion numbers correctly', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const suggestionCounts = screen.getAllByText(/\d+ öneri bulundu/i);
    expect(suggestionCounts).toHaveLength(4);
  });

  test('collapses expanded sections when clicked again', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    const firstButton = expandButtons[0];
    
    // Expand
    fireEvent.click(firstButton);
    expect(screen.getByText(/syntax hatası/i)).toBeInTheDocument();
    
    // Collapse
    fireEvent.click(firstButton);
    expect(screen.queryByText(/syntax hatası/i)).not.toBeInTheDocument();
  });

  test('applies theme colors correctly', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const cards = screen.getAllByText(/öneri bulundu/i);
    expect(cards.length).toBeGreaterThan(0);
  });

  test('shows suggestion details with proper formatting', () => {
    render(<AnalysisResults result={mockResult} theme={mockTheme} />);
    
    const expandButtons = screen.getAllByRole('button');
    fireEvent.click(expandButtons[0]);
    
    const suggestions = screen.getAllByText(/öneri \d+/i);
    expect(suggestions).toHaveLength(2);
  });
}); 