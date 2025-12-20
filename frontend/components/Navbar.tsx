"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Map, BookOpen, User, LogOut, Menu, X } from 'lucide-react';
import { ThemeSwitcher } from './ThemeSwitcher';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-card border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center" onClick={closeMenu}>
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center mr-2">
                <span className="text-primary-foreground font-bold text-lg">P</span>
              </div>
              <span className="font-bold text-xl text-foreground hidden sm:block">Pathways for Parents</span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex md:items-center md:space-x-4">
            {user ? (
              <>
                <Link href="/journey">
                  <Button variant={isActive('/journey') ? 'secondary' : 'ghost'} className="flex items-center gap-2">
                    <Map size={18} />
                    Journey
                  </Button>
                </Link>
                <Link href="/resources">
                  <Button variant={isActive('/resources') ? 'secondary' : 'ghost'} className="flex items-center gap-2">
                    <BookOpen size={18} />
                    Resources
                  </Button>
                </Link>
                <div className="h-6 w-px bg-border mx-2"></div>
                <Link href="/profile">
                  <Button variant="ghost" className="flex items-center gap-2">
                    <User size={18} />
                    Profile
                  </Button>
                </Link>
              </>
            ) : (
              <>
                <Link href="/resources">
                  <Button variant="ghost">Resources</Button>
                </Link>
                <Link href="/login">
                  <Button variant="ghost">Log In</Button>
                </Link>
                <Link href="/onboarding">
                  <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">Get Started</Button>
                </Link>
              </>
            )}
            <div className="ml-2">
              <ThemeSwitcher />
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <ThemeSwitcher />
            <button
              onClick={toggleMenu}
              className="ml-2 inline-flex items-center justify-center p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary"
            >
              <span className="sr-only">Open main menu</span>
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-card border-b border-border">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {user ? (
              <>
                <Link href="/journey" onClick={closeMenu}>
                  <div className={cn("block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2", isActive('/journey') ? "bg-accent text-accent-foreground" : "text-muted-foreground hover:bg-accent hover:text-accent-foreground")}>
                    <Map size={18} />
                    Journey
                  </div>
                </Link>
                <Link href="/resources" onClick={closeMenu}>
                  <div className={cn("block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2", isActive('/resources') ? "bg-accent text-accent-foreground" : "text-muted-foreground hover:bg-accent hover:text-accent-foreground")}>
                    <BookOpen size={18} />
                    Resources
                  </div>
                </Link>
                <Link href="/profile" onClick={closeMenu}>
                  <div className={cn("block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2", isActive('/profile') ? "bg-accent text-accent-foreground" : "text-muted-foreground hover:bg-accent hover:text-accent-foreground")}>
                    <User size={18} />
                    Profile
                  </div>
                </Link>
                <button 
                  onClick={() => { logout(); closeMenu(); }}
                  className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center gap-2"
                >
                  <LogOut size={18} />
                  Log Out
                </button>
              </>
            ) : (
              <>
                <Link href="/resources" onClick={closeMenu}>
                  <div className="block px-3 py-2 rounded-md text-base font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground">Resources</div>
                </Link>
                <Link href="/login" onClick={closeMenu}>
                  <div className="block px-3 py-2 rounded-md text-base font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground">Log In</div>
                </Link>
                <Link href="/onboarding" onClick={closeMenu}>
                  <div className="block px-3 py-2 rounded-md text-base font-medium bg-primary/10 text-primary hover:bg-primary/20">Get Started</div>
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}



