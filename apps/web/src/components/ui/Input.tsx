import React, { forwardRef, type InputHTMLAttributes } from 'react';
import { cn } from '../../lib/utils';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          'flex h-9 w-full rounded-[var(--radius-md)] border bg-[var(--surface)] px-3 py-1 text-sm text-[var(--text-main)] shadow-xs transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-[var(--text-muted)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--primary)] disabled:cursor-not-allowed disabled:opacity-50',
          error
            ? 'border-[var(--danger)] focus-visible:ring-[var(--danger)]'
            : 'border-[var(--border)]',
          className
        )}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';
