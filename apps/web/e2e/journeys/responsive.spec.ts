import { test, expect } from '@playwright/test';

test.describe('Journey: Multi-resolution viewport responsiveness', () => {
  test('Validates layout across 1920, 1440, 1280 and 900px without horizontal overflow', async ({ page }) => {
    await page.goto('/classify');
    await expect(page.locator('input[placeholder*="Enter product or service description"]').first()).toBeVisible({ timeout: 10000 });

    // 1920px width - No horizontal scrollbar
    await page.setViewportSize({ width: 1920, height: 1080 });
    const scrollWidth1920 = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
    expect(scrollWidth1920).toBeTruthy();

    // 1440px width - No horizontal scrollbar
    await page.setViewportSize({ width: 1440, height: 900 });
    const scrollWidth1440 = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
    expect(scrollWidth1440).toBeTruthy();

    // 1280px width - No horizontal scrollbar
    await page.setViewportSize({ width: 1280, height: 800 });
    const scrollWidth1280 = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
    expect(scrollWidth1280).toBeTruthy();

    // 900px (< 1024px) width - Toggle menu is present
    await page.setViewportSize({ width: 900, height: 800 });
    const toggleBtn = page.locator('button[aria-label="Toggle navigation"]');
    await expect(toggleBtn).toBeVisible({ timeout: 10000 });
  });
});
