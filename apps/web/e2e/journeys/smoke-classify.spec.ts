import { test, expect } from '@playwright/test';

test.describe('Classification Smoke Test & Statutory Evidence Verification', () => {
  test('classify "leather jacket" returns statutory HSN 42031010, 18% rate, and CBIC source link', async ({ page }) => {
    // 1. Open /classify page
    await page.goto('/classify');

    // 2. Verify page header
    await expect(page.locator('h1')).toContainText('Statutory HSN / SAC Classification');

    // 3. Search for "leather jacket"
    const input = page.locator('input[placeholder*="Enter product or service description"]');
    await input.fill('leather jacket');
    await page.getByRole('button', { name: /classify/i }).click();

    // 4. Assert suggested HSN code and description
    await expect(page.getByText('42031010').first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Articles of apparel and clothing accessories, of leather').first()).toBeVisible();

    // 5. Assert 18% statutory GST rate
    await expect(page.getByText('18.0%').first()).toBeVisible();

    // 6. Assert CBIC statutory evidence document and source link
    await expect(page.getByText('Notification No. 1/2017-Central Tax (Rate)').first()).toBeVisible();
    const sourceLink = page.locator('a[href*="Notification1-CGST-Rate.pdf"]').first();
    await expect(sourceLink).toBeVisible();
    await expect(sourceLink).toHaveAttribute('target', '_blank');
  });
});
