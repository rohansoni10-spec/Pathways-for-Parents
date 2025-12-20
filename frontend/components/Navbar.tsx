"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Menu, X, User, Map, BookOpen, LogOut, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white border-b border-slate-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center" onClick={closeMenu}>
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-400 to-emerald-400 flex items-center justify-center mr-2">
                <span className="text-white font-bold text-lg">P</span>
              </div>
              <span className="font-bold text-xl text-slate-800 hidden sm:block">Pathways for Parents</span>
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
                <div className="h-6 w-px bg-slate-200 mx-2"></div>
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
                  <Button className="bg-sky-600 hover:bg-sky-700 text-white">Get Started</Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-slate-400 hover:text-slate-500 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-sky-500"
            >
              <span className="sr-only">Open main menu</span>
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-b border-slate-100">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {user ? (
              <>
                <Link href="/journey" onClick={closeMenu}>
                  <div className={cn("block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2", isActive('/journey') ? "bg-emerald-50 text-emerald-700" : "text-slate-600 hover:bg-slate-50")}>
                    <Map size={18} />
                    Journey
                  </div>
                </Link>
                <Link href="/resources" onClick={closeMenu}>
                  <div className={cn("block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2", isActive('/resources') ? "bg-emerald-50 text-emerald-700" : "text-slate-600 hover:bg-slate-50")}>
                    <BookOpen size={18} />
                    Resources
                  </div>
                </Link>
                <Link href="/profile" onClick={closeMenu}>
                  <div className={cn("block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2", isActive('/profile') ? "bg-emerald-50 text-emerald-700" : "text-slate-600 hover:bg-slate-50")}>
                    <User size={18} />
                    Profile
                  </div>
                </Link>
                <button 
                  onClick={() => { logout(); closeMenu(); }}
                  className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:bg-slate-50 flex items-center gap-2"
                >
                  <LogOut size={18} />
                  Log Out
                </button>
              </>
            ) : (
              <>
                <Link href="/resources" onClick={closeMenu}>
                  <div className="block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:bg-slate-50">Resources</div>
                </Link>
                <Link href="/login" onClick={closeMenu}>
                  <div className="block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:bg-slate-50">Log In</div>
                </Link>
                <Link href="/onboarding" onClick={closeMenu}>
                  <div className="block px-3 py-2 rounded-md text-base font-medium bg-sky-50 text-sky-700 hover:bg-sky-100">Get Started</div>
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}

