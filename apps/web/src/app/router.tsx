import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppShell } from './shell/AppShell';
import { ClassifyPage } from '../features/classify/ClassifyPage';
import { InvoicesPage } from '../features/invoices/InvoicesPage';
import { InvoiceDetailPage } from '../features/invoices/InvoiceDetailPage';
import { PartiesPage } from '../features/parties/PartiesPage';
import { RateSchedulePage } from '../features/rate-schedule/RateSchedulePage';
import { ActivityLogPage } from '../features/activity-log/ActivityLogPage';
import { DataSyncPage } from '../features/data-sync/DataSyncPage';
import { SettingsPage } from '../features/settings/SettingsPage';

export const appRouter = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <Navigate to="/classify" replace /> },
      { path: 'classify', element: <ClassifyPage /> },
      { path: 'invoices', element: <InvoicesPage /> },
      { path: 'invoices/:id', element: <InvoiceDetailPage /> },
      { path: 'parties', element: <PartiesPage /> },
      { path: 'rate-schedule', element: <RateSchedulePage /> },
      { path: 'activity-log', element: <ActivityLogPage /> },
      { path: 'admin/data-sync', element: <DataSyncPage /> },
      { path: 'settings', element: <SettingsPage /> },
      { path: '*', element: <Navigate to="/classify" replace /> },
    ],
  },
]);
