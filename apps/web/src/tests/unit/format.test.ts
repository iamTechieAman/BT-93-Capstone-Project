import { describe, it, expect } from 'vitest';
import {
  formatINR,
  formatIndianNumber,
  formatGSTRate,
  formatISTDate,
  formatISTDateTime,
} from '@/lib/format';
import { cn } from '@/lib/utils';

describe('formatINR utility', () => {
  it('formats numbers to Indian Rupee currency standard with two decimals', () => {
    const formatted = formatINR(123456.78);
    expect(formatted).toContain('1,23,456.78');
    expect(formatted).toMatch(/₹|INR/);
  });

  it('handles null, undefined and invalid amounts gracefully', () => {
    expect(formatINR(null)).toBe('₹ 0.00');
    expect(formatINR(undefined)).toBe('₹ 0.00');
    expect(formatINR('invalid')).toBe('₹ 0.00');
  });

  it('formats 0 properly', () => {
    const res = formatINR(0);
    expect(res).toContain('0.00');
  });
});

describe('formatIndianNumber utility', () => {
  it('formats numbers with Indian grouping without currency symbol', () => {
    const formatted = formatIndianNumber(1000000);
    expect(formatted).toBe('10,00,000');
  });

  it('handles edge cases', () => {
    expect(formatIndianNumber(null)).toBe('0');
    expect(formatIndianNumber(undefined)).toBe('0');
  });
});

describe('formatGSTRate utility', () => {
  it('appends percentage sign properly', () => {
    expect(formatGSTRate(18)).toBe('18%');
    expect(formatGSTRate(0)).toBe('0%');
    expect(formatGSTRate('12.5')).toBe('12.5%');
    expect(formatGSTRate(null)).toBe('0%');
  });
});

describe('formatISTDate and DateTime', () => {
  it('formats ISO dates accurately in IST timezone', () => {
    const res = formatISTDate('2026-10-09T08:00:00Z');
    expect(res).toContain('09');
    expect(res).toContain('2026');
  });

  it('returns fallback dash for empty or null dates', () => {
    expect(formatISTDate(null)).toBe('—');
    expect(formatISTDate('')).toBe('—');
    expect(formatISTDateTime(null)).toBe('—');
  });
});

describe('cn class combiner utility', () => {
  it('merges class names and handles conditionals', () => {
    const isHidden = false;
    expect(cn('btn', isHidden && 'hidden', 'primary')).toBe('btn primary');
  });
});
