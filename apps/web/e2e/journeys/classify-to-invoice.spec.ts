import { test } from '@playwright/test';
import { ClassifyPage } from '../pages/ClassifyPage';
import { InvoicesPage } from '../pages/InvoicesPage';

test.describe('Journey: Classify product to invoice generation', () => {
  test('Classifies leather jacket, creates draft invoice, and verifies invoice list', async ({ page }) => {
    const classifyPage = new ClassifyPage(page);
    const invoicesPage = new InvoicesPage(page);

    // 1. Classification
    await classifyPage.goto();
    await classifyPage.classifyProduct("Men's genuine leather jacket with brass zip");
    await classifyPage.expectResultHsn('42031010');
    await classifyPage.expectResultRate('18%');

    // 2. Invoicing
    await invoicesPage.goto();
    await invoicesPage.openCreateInvoiceModal();
    await invoicesPage.submitDraftInvoice();
    await invoicesPage.expectInvoicesListLoaded();
  });
});
