/**
 * Centralized Indian Currency and Date Formatting Utilities.
 * Strictly adheres to:
 * - Indian grouping (e.g. ₹ 1,23,456.78)
 * - Tabular numbers (ISO / IST timestamps)
 * - Percentage rates
 */

const CURRENCY_FORMATTER = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const NUMBER_FORMATTER = new Intl.NumberFormat('en-IN', {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

export function formatINR(amount: number | string | null | undefined): string {
  if (amount === null || amount === undefined || isNaN(Number(amount))) {
    return '₹ 0.00';
  }
  return CURRENCY_FORMATTER.format(Number(amount));
}

export function formatIndianNumber(val: number | string | null | undefined): string {
  if (val === null || val === undefined || isNaN(Number(val))) {
    return '0';
  }
  return NUMBER_FORMATTER.format(Number(val));
}

export function formatGSTRate(rate: number | string | null | undefined): string {
  if (rate === null || rate === undefined || isNaN(Number(rate))) {
    return '0%';
  }
  return `${Number(rate)}%`;
}

export function formatISTDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString('en-IN', {
      timeZone: 'Asia/Kolkata',
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

export function formatISTDateTime(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    });
  } catch {
    return dateStr;
  }
}
