import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import * as Sentry from '@sentry/react';
import './styles/tokens.css';
import './styles/globals.css';
import { AppProviders } from './app/providers';
import { appRouter } from './app/router';

// Initialize Sentry tracking if DSN is configured
if (import.meta.env.VITE_SENTRY_DSN) {
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,
    integrations: [Sentry.browserTracingIntegration()],
    tracesSampleRate: 1.0,
  });
}

const rootElement = document.getElementById('root');
if (rootElement) {
  createRoot(rootElement).render(
    <StrictMode>
      <AppProviders>
        <RouterProvider router={appRouter} />
      </AppProviders>
    </StrictMode>
  );
}
