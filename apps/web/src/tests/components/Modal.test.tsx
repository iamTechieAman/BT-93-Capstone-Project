import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {
  Modal,
  ModalTrigger,
  ModalContent,
  ModalTitle,
  ModalDescription,
} from '@/components/ui/Modal';

describe('Modal Primitive', () => {
  it('opens and displays dialog with proper aria attributes', async () => {
    render(
      <Modal>
        <ModalTrigger asChild>
          <button>Open Modal</button>
        </ModalTrigger>
        <ModalContent>
          <ModalTitle>Statutory Audit Confirmation</ModalTitle>
          <ModalDescription>Review your entries before dispatching.</ModalDescription>
          <button>Confirm</button>
        </ModalContent>
      </Modal>
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

    const trigger = screen.getByRole('button', { name: /open modal/i });
    await userEvent.click(trigger);

    const dialog = screen.getByRole('dialog');
    expect(dialog).toBeInTheDocument();
    expect(screen.getByText('Statutory Audit Confirmation')).toBeInTheDocument();
    expect(screen.getByText('Review your entries before dispatching.')).toBeInTheDocument();
  });

  it('closes dialog on Escape key press', async () => {
    render(
      <Modal>
        <ModalTrigger asChild>
          <button>Open Modal</button>
        </ModalTrigger>
        <ModalContent>
          <ModalTitle>Escape Test</ModalTitle>
          <button>Inside Button</button>
        </ModalContent>
      </Modal>
    );

    const trigger = screen.getByRole('button', { name: /open modal/i });
    await userEvent.click(trigger);

    expect(screen.getByRole('dialog')).toBeInTheDocument();

    await userEvent.keyboard('{Escape}');
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
