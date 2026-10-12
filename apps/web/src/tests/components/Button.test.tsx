import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '@/components/ui/Button';

describe('Button Primitive', () => {
  it('renders children with proper role and responds to click', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Submit Action</Button>);

    const btn = screen.getByRole('button', { name: /submit action/i });
    expect(btn).toBeInTheDocument();

    await userEvent.click(btn);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('supports keyboard navigation via Enter and Space keys', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Keyboard Test</Button>);

    const btn = screen.getByRole('button', { name: /keyboard test/i });
    btn.focus();
    expect(btn).toHaveFocus();

    await userEvent.keyboard('{Enter}');
    expect(handleClick).toHaveBeenCalledTimes(1);

    await userEvent.keyboard(' ');
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  it('handles disabled state properly and prevents interaction', async () => {
    const handleClick = vi.fn();
    render(
      <Button disabled onClick={handleClick}>
        Disabled Button
      </Button>
    );

    const btn = screen.getByRole('button', { name: /disabled button/i });
    expect(btn).toBeDisabled();

    await userEvent.click(btn);
    expect(handleClick).not.toHaveBeenCalled();
  });
});
