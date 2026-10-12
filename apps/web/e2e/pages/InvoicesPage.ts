import { type Page, type Locator, expect } from '@playwright/test';

export class InvoicesPage {
  readonly page: Page;
  readonly pageTitle: Locator;
  readonly createInvoiceButton: Locator;
  readonly createDraftSubmitButton: Locator;
  readonly modalTitle: Locator;
  readonly invoicesTable: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageTitle = page.locator('h1:has-text("Tax Invoices")');
    this.createInvoiceButton = page.locator('button:has-text("Create Invoice")').first();
    this.modalTitle = page.locator('text=Create Statutory Tax Invoice');
    this.createDraftSubmitButton = page.locator('button:has-text("Create Draft Invoice")').first();
    this.invoicesTable = page.locator('table').first();
  }

  async goto() {
    await this.page.goto('/invoices');
    await expect(this.pageTitle).toBeVisible({ timeout: 10000 });
  }

  async openCreateInvoiceModal() {
    await this.createInvoiceButton.click();
    await expect(this.modalTitle).toBeVisible({ timeout: 10000 });
  }

  async submitDraftInvoice() {
    await this.createDraftSubmitButton.click();
  }

  async expectInvoicesListLoaded() {
    await expect(this.invoicesTable).toBeVisible({ timeout: 10000 });
  }
}
