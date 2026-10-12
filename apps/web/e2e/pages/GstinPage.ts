import { type Page, type Locator, expect } from '@playwright/test';

export class GstinPage {
  readonly page: Page;
  readonly pageTitle: Locator;
  readonly gstinInput: Locator;
  readonly verifyButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageTitle = page.locator('h1:has-text("Party Verification")');
    this.gstinInput = page.locator('input[placeholder*="Enter 15-character GSTIN"]').first();
    this.verifyButton = page.locator('button:has-text("Verify GSTIN")').first();
  }

  async goto() {
    await this.page.goto('/parties');
    await expect(this.pageTitle).toBeVisible({ timeout: 10000 });
  }

  async verifyGstin(gstin: string) {
    await this.gstinInput.fill(gstin);
    await this.verifyButton.click();
  }

  async expectHeadline(text: string) {
    await expect(this.page.locator(`text=${text}`).first()).toBeVisible({ timeout: 10000 });
  }

  async expectTextVisible(text: string) {
    await expect(this.page.locator(`text=${text}`).first()).toBeVisible({ timeout: 10000 });
  }
}
