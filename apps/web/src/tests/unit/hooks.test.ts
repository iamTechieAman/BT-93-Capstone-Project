import { describe, it, expect, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from '@/hooks/useDebounce';

describe('useDebounce hook', () => {
  it('updates debounced value after specified timeout', () => {
    vi.useFakeTimers();

    const { result, rerender } = renderHook(({ val, delay }) => useDebounce(val, delay), {
      initialProps: { val: 'initial', delay: 300 },
    });

    expect(result.current).toBe('initial');

    rerender({ val: 'updated', delay: 300 });
    expect(result.current).toBe('initial');

    act(() => {
      vi.advanceTimersByTime(300);
    });

    expect(result.current).toBe('updated');

    vi.useRealTimers();
  });
});
