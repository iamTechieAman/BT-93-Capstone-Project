import { test, expect } from '@playwright/test';
import { RateSchedulePage } from '../pages/RateSchedulePage';

test.describe('Journey: Rate Schedule Search and Hierarchy Drawer', () => {
  test('Searches HSN rules, inspects hierarchy drawer, and closes on Escape', async ({ page }) => {
    const ratePage = new RateSchedulePage(page);
    await ratePage.goto();

    // Search HSN
    await ratePage.searchRateRule('4203');
    await expect(page.locator('text=42031010').first()).toBeVisible({ timeout: 10000 });

    // Hierarchy drawer
    await ratePage.openHierarchyDrawer();
    await ratePage.closeDrawerWithEscape();
  });
});
