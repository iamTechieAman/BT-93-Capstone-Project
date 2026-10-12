import React, { type HTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors border',
  {
    variants: {
      variant: {
        neutral: 'bg-[var(--surface-hover)] text-[var(--text-main)] border-[var(--border)]',
        primary: 'bg-[var(--primary-subtle)] text-[var(--primary)] border-[var(--primary-subtle)]',
        success: 'bg-[var(--success-subtle)] text-[var(--success)] border-[var(--success-subtle)]',
        warning: 'bg-[var(--warning-subtle)] text-[var(--warning)] border-[var(--warning-subtle)]',
        danger: 'bg-[var(--danger-subtle)] text-[var(--danger)] border-[var(--danger-subtle)]',
      },
    },
    defaultVariants: {
      variant: 'neutral',
    },
  }
);

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant, className }))} {...props} />;
}
