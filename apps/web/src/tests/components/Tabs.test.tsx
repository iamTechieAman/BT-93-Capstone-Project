import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';

describe('Tabs Primitive', () => {
  it('renders tablist and triggers with proper aria-selected states', async () => {
    render(
      <Tabs defaultValue="hsn">
        <TabsList>
          <TabsTrigger value="hsn">HSN Lookup</TabsTrigger>
          <TabsTrigger value="rates">Rates Schedule</TabsTrigger>
        </TabsList>
        <TabsContent value="hsn">HSN Content Area</TabsContent>
        <TabsContent value="rates">Rates Content Area</TabsContent>
      </Tabs>
    );

    const hsnTab = screen.getByRole('tab', { name: /hsn lookup/i });
    const ratesTab = screen.getByRole('tab', { name: /rates schedule/i });

    expect(hsnTab).toHaveAttribute('aria-selected', 'true');
    expect(ratesTab).toHaveAttribute('aria-selected', 'false');
    expect(screen.getByText('HSN Content Area')).toBeInTheDocument();

    await userEvent.click(ratesTab);

    expect(hsnTab).toHaveAttribute('aria-selected', 'false');
    expect(ratesTab).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByText('Rates Content Area')).toBeInTheDocument();
  });
});
