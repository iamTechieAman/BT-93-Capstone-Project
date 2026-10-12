import React, { useState, useEffect } from 'react';
import { Sun, Moon, CheckCircle2 } from 'lucide-react';
import { Badge } from '../../components/ui/Badge';

export function TopBar() {
  const [isDark, setIsDark] = useState(() => {
    if (typeof window === 'undefined') return false;
    const saved = localStorage.getItem('theme');
    return (
      saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)
    );
  });

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      setIsDark(false);
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
      setIsDark(true);
    }
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-[var(--border)] bg-[var(--surface)] px-6 backdrop-blur-xs">
      {/* Left Title / Breadcrumbs Area */}
      <div className="flex items-center gap-3 pl-10 lg:pl-0">
        <Badge variant="neutral" className="font-mono text-[10px]">
          v0.1.0 • PROD
        </Badge>
        <span className="hidden sm:inline-block text-xs text-[var(--text-muted)] font-medium">
          Statutory Indian Goods & Services Tax Compliance Engine
        </span>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-1.5 text-xs text-[var(--success)] font-medium bg-[var(--success-subtle)] px-2.5 py-1 rounded-full border border-[var(--success-subtle)]">
          <CheckCircle2 className="h-3.5 w-3.5" />
          <span>API Connected</span>
        </div>

        <button
          type="button"
          onClick={toggleTheme}
          className="p-2 text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--surface-hover)] rounded-[var(--radius-md)] transition-colors cursor-pointer"
          aria-label="Toggle theme"
        >
          {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>

        <div className="h-8 w-8 rounded-full bg-[var(--surface-hover)] border border-[var(--border)] flex items-center justify-center font-bold text-xs text-[var(--text-main)] select-none">
          AK
        </div>
      </div>
    </header>
  );
}
