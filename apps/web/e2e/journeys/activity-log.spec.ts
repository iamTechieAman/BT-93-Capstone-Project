import { test } from '@playwright/test';
import { ActivityLogPage } from '../pages/ActivityLogPage';

test.describe('Journey: Activity Log viewing and export triggers', () => {
  test('Navigates to activity log and checks CSV/JSON export readiness', async ({ page }) => {
    const activityLogPage = new ActivityLogPage(page);
    await activityLogPage.goto();
    await activityLogPage.expectExportButtonsVisibleAndEnabled();
  });
});
