import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  Sparkles,
  FileText,
  Building2,
  TableProperties,
  History,
  Database,
  Settings,
  ShieldCheck,
  Menu,
  X,
} from 'lucide-react';
import { cn } from '../../lib/utils';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  adminOnly?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { name: 'Classify', href: '/classify', icon: Sparkles },
  { name: 'Invoices', href: '/invoices', icon: FileText },
  { name: 'Parties (GSTIN)', href: '/parties', icon: Building2 },
  { name: 'Rate schedule', href: '/rate-schedule', icon: TableProperties },
  { name: 'Activity log', href: '/activity-log', icon: History },
  { name: 'Data sync', href: '/admin/data-sync', icon: Database, adminOnly: true },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  return (
    <>
      {/* Mobile Toggle Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-3 left-3 z-50 p-2 bg-[var(--surface)] border border-[var(--border)] rounded-[var(--radius-md)] text-[var(--text-main)] shadow-xs"
        aria-label="Toggle navigation"
      >
        {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </button>

      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-xs lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-[var(--border)] bg-[var(--surface)] transition-transform duration-200 lg:static lg:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Brand Header */}
        <div className="flex h-16 items-center gap-3 border-b border-[var(--border)] px-6">
          <div className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-md)] bg-[var(--primary)] text-white font-bold text-sm">
            SG
          </div>
          <div>
            <span className="text-sm font-bold tracking-tight text-[var(--text-main)] block leading-none">
              Smart GST
            </span>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Compliance SaaS
            </span>
          </div>
        </div>

        {/* Navigation List */}
        <nav className="flex-1 space-y-1 px-3 py-4 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive =
              location.pathname === item.href ||
              (item.href !== '/' && location.pathname.startsWith(`${item.href}/`));

            return (
              <NavLink
                key={item.name}
                to={item.href}
                onClick={() => setIsOpen(false)}
                className={cn(
                  'flex items-center gap-3 rounded-[var(--radius-md)] px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-[var(--surface-hover)] text-[var(--primary)] font-semibold shadow-xs'
                    : 'text-[var(--text-muted)] hover:bg-[var(--surface-hover)] hover:text-[var(--text-main)]'
                )}
              >
                <Icon
                  className={cn(
                    'h-4 w-4 shrink-0 transition-colors',
                    isActive ? 'text-[var(--primary)]' : 'text-[var(--text-muted)]'
                  )}
                />
                <span>{item.name}</span>
                {item.adminOnly && (
                  <span className="ml-auto rounded-xs bg-[var(--surface-hover)] px-1.5 py-0.5 text-[10px] font-medium text-[var(--text-muted)] border border-[var(--border)]">
                    Admin
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Bottom Compliance Badge */}
        <div className="p-4 border-t border-[var(--border)]">
          <div className="p-3 bg-[var(--surface-hover)] rounded-[var(--radius-md)] flex items-center gap-2.5">
            <ShieldCheck className="h-4 w-4 text-[var(--primary)] shrink-0" />
            <div className="text-[11px] leading-tight">
              <span className="font-semibold text-[var(--text-main)] block">CBIC 2026.1</span>
              <span className="text-[var(--text-muted)]">Statutory verified</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
