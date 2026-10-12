import { type Page, type Locator, expect } from '@playwright/test';

export class ClassifyPage {
  readonly page: Page;
  readonly searchInput: Locator;
  readonly classifyButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.searchInput = page.locator('input[placeholder*="Enter product or service description"]').first();
    this.classifyButton = page.locator('button:has-text("Classify")').first();
  }

  async goto() {
    await this.page.goto('/classify');
    await expect(this.searchInput).toBeVisible({ timeout: 10000 });
  }

  async classifyProduct(productDescription: string) {
    await this.searchInput.fill(productDescription);
    await this.page.keyboard.press('Enter');
  }

  async expectResultHsn(hsn: string) {
    await expect(this.page.locator(`text=${hsn}`).first()).toBeVisible({ timeout: 10000 });
  }

  async expectResultRate(rate: string) {
    await expect(this.page.locator(`text=${rate}`).first()).toBeVisible({ timeout: 10000 });
  }
}
