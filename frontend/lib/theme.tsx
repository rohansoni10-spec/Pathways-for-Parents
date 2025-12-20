"use client";

import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'ocean' | 'lavender' | 'earth';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('ocean');

  useEffect(() => {
    const savedTheme = localStorage.getItem('pathways_theme') as Theme;
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('theme-ocean', 'theme-lavender', 'theme-earth');
    root.classList.add(`theme-${theme}`);
    localStorage.setItem('pathways_theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
