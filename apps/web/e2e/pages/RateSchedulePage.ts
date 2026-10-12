import { type Page, type Locator, expect } from '@playwright/test';

export class RateSchedulePage {
  readonly page: Page;
  readonly pageTitle: Locator;
  readonly searchInput: Locator;
  readonly viewHierarchyButton: Locator;
  readonly drawerHeader: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageTitle = page.locator('h1:has-text("Statutory GST Rate Schedule")');
    this.searchInput = page.locator('input[placeholder*="Search by HSN code"]').first();
    this.viewHierarchyButton = page.locator('button:has-text("View Hierarchy")').first();
    this.drawerHeader = page.locator('text=Tariff Hierarchy & Schedule Notes').first();
  }

  async goto() {
    await this.page.goto('/rate-schedule');
    await expect(this.pageTitle).toBeVisible({ timeout: 10000 });
  }

  async searchRateRule(query: string) {
    await this.searchInput.fill(query);
  }

  async openHierarchyDrawer() {
    await this.viewHierarchyButton.click();
    await expect(this.drawerHeader).toBeVisible({ timeout: 10000 });
  }

  async closeDrawerWithEscape() {
    await this.page.keyboard.press('Escape');
    await expect(this.drawerHeader).not.toBeVisible({ timeout: 10000 });
  }
}
