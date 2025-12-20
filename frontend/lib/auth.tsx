"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: string;
  email: string;
  name?: string;
  recommendedStageId?: string;
  completedMilestones: string[];
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string) => void;
  register: (email: string, name?: string) => void;
  logout: () => void;
  updateUser: (updates: Partial<User>) => void;
  toggleMilestone: (milestoneId: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check local storage for existing session
    const storedUser = localStorage.getItem('pathways_user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error("Failed to parse user data", e);
        localStorage.removeItem('pathways_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (email: string) => {
    // Mock login - in real app this would verify credentials
    // For MVP, we just simulate a user or create a temp one if not found in a "db"
    // But since we don't have a DB, we'll just look for a stored user or create a new session
    // For simplicity, let's just create a session for this email
    const newUser: User = {
      id: 'u_' + Math.random().toString(36).substr(2, 9),
      email,
      completedMilestones: []
    };
    
    // In a real mock, we might want to retrieve data associated with email
    // But for this frontend-only demo, we'll just set the user
    setUser(newUser);
    localStorage.setItem('pathways_user', JSON.stringify(newUser));
  };

  const register = (email: string, name?: string) => {
    const newUser: User = {
      id: 'u_' + Math.random().toString(36).substr(2, 9),
      email,
      name,
      completedMilestones: []
    };
    setUser(newUser);
    localStorage.setItem('pathways_user', JSON.stringify(newUser));
    
    // Simulate sending welcome email
    console.log(`Sending welcome email to ${email}...`);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('pathways_user');
  };

  const updateUser = (updates: Partial<User>) => {
    setUser(prev => {
      if (!prev) return null;
      const updated = { ...prev, ...updates };
      localStorage.setItem('pathways_user', JSON.stringify(updated));
      return updated;
    });
  };

  const toggleMilestone = (milestoneId: string) => {
    setUser(prev => {
      if (!prev) return null;
      const isCompleted = prev.completedMilestones.includes(milestoneId);
      let newCompleted;
      if (isCompleted) {
        newCompleted = prev.completedMilestones.filter(id => id !== milestoneId);
      } else {
        newCompleted = [...prev.completedMilestones, milestoneId];
      }
      const updated = { ...prev, completedMilestones: newCompleted };
      localStorage.setItem('pathways_user', JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, updateUser, toggleMilestone }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
