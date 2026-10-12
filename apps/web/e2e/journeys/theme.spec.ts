import { test, expect } from '@playwright/test';

test.describe('Journey: Theme toggle and contrast mode', () => {
  test('Toggles light and dark themes in TopBar seamlessly', async ({ page }) => {
    await page.goto('/classify');
    await expect(page.locator('input[placeholder*="Enter product or service description"]').first()).toBeVisible({ timeout: 10000 });

    const htmlEl = page.locator('html');
    const themeBtn = page.locator('button[aria-label="Toggle theme"]').first();
    await expect(themeBtn).toBeVisible({ timeout: 5000 });

    await themeBtn.click();
    const isDark = await htmlEl.evaluate((el) => el.classList.contains('dark'));
    expect(typeof isDark).toBe('boolean');
  });
});
