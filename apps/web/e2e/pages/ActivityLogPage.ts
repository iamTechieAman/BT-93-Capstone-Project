import { type Page, type Locator, expect } from '@playwright/test';

export class ActivityLogPage {
  readonly page: Page;
  readonly pageTitle: Locator;
  readonly exportCsvButton: Locator;
  readonly exportJsonButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageTitle = page.locator('h1:has-text("Statutory Activity Log")');
    this.exportCsvButton = page.locator('button:has-text("Export CSV")').first();
    this.exportJsonButton = page.locator('button:has-text("Export JSON")').first();
  }

  async goto() {
    await this.page.goto('/activity-log');
    await expect(this.pageTitle).toBeVisible({ timeout: 10000 });
  }

  async expectExportButtonsVisibleAndEnabled() {
    await expect(this.exportCsvButton).toBeVisible({ timeout: 10000 });
    await expect(this.exportCsvButton).toBeEnabled();
  }
}
