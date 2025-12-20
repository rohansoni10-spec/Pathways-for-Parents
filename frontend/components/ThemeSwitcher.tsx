"use client";

import React from 'react';
import { useTheme } from '@/lib/theme';
import { Button } from '@/components/ui/button';
import { Palette } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function ThemeSwitcher() {
  const { setTheme } = useTheme();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="rounded-full">
          <Palette className="h-5 w-5 text-muted-foreground" />
          <span className="sr-only">Change Theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme('ocean')}>
          <div className="w-4 h-4 rounded-full bg-sky-500 mr-2"></div>
          Ocean (Default)
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('lavender')}>
          <div className="w-4 h-4 rounded-full bg-purple-500 mr-2"></div>
          Lavender Dream
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('earth')}>
          <div className="w-4 h-4 rounded-full bg-emerald-700 mr-2"></div>
          Earth & Sage
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
