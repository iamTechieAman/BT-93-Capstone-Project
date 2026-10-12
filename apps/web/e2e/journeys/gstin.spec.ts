import { test } from '@playwright/test';
import { GstinPage } from '../pages/GstinPage';

test.describe('Journey: GSTIN verification offline pipeline', () => {
  test('Verifies valid GSTIN, detects invalid checksum, and invalid state code', async ({ page }) => {
    const gstinPage = new GstinPage(page);
    await gstinPage.goto();

    // 1. Valid GSTIN
    await gstinPage.verifyGstin('27AAPFU0939F1ZV');
    await gstinPage.expectHeadline('Format valid. Registration not verified.');
    await gstinPage.expectTextVisible('Maharashtra');

    // 2. Invalid Checksum
    await gstinPage.verifyGstin('27AAPFU0939F1ZX');
    await gstinPage.expectHeadline('Format invalid.');
    await gstinPage.expectTextVisible('Modulus-36 checksum mismatch');

    // 3. Invalid State Code
    await gstinPage.verifyGstin('99AAPFU0939F1ZV');
    await gstinPage.expectTextVisible('Invalid state code');
  });
});
