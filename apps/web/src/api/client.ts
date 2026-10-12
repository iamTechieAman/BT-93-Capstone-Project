/**
 * Centralized API Client with standard error handling and Request-ID propagation.
 */
import type {
  ApiErrorPayload,
  ClassificationRequest,
  ClassificationResult,
  GstinVerifyResponse,
  InvoiceCreatePayload,
  InvoiceResponse,
  TariffRateRule,
  TariffHierarchyNode,
  AuditLogItem,
  SyncStatusResponse,
} from './types';

const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export class ApiError extends Error {
  public readonly code: string;
  public readonly requestId?: string;
  public readonly statusCode: number;
  public readonly details?: Record<string, unknown>;

  constructor(payload: ApiErrorPayload, statusCode: number) {
    super(payload.message || 'An API error occurred');
    this.name = 'ApiError';
    this.code = payload.code || 'API_ERROR';
    this.requestId = payload.request_id;
    this.statusCode = statusCode;
    this.details = payload.details;
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (!response.ok) {
    let errorPayload: ApiErrorPayload;
    try {
      errorPayload = await response.json();
    } catch {
      errorPayload = {
        code: 'HTTP_ERROR',
        message: response.statusText || `Request failed with status ${response.status}`,
      };
    }
    throw new ApiError(errorPayload, response.status);
  }

  // Handle blob responses (e.g. exports)
  if (response.headers.get('Content-Type')?.includes('text/csv')) {
    return (await response.text()) as unknown as T;
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  // 1. Classification
  classifyProduct: (payload: ClassificationRequest): Promise<ClassificationResult> => {
    return request<ClassificationResult>('/classify', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // 2. GSTIN Verification
  verifyGstin: (gstin: string): Promise<GstinVerifyResponse> => {
    return request<GstinVerifyResponse>('/gstin/verify', {
      method: 'POST',
      body: JSON.stringify({ gstin }),
    });
  },

  // 3. Invoices
  listInvoices: (): Promise<InvoiceResponse[]> => {
    return request<InvoiceResponse[]>('/invoices');
  },

  getInvoice: (id: string): Promise<InvoiceResponse> => {
    return request<InvoiceResponse>(`/invoices/${id}`);
  },

  createInvoice: (payload: InvoiceCreatePayload): Promise<InvoiceResponse> => {
    return request<InvoiceResponse>('/invoices', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  finalizeInvoice: (id: string): Promise<InvoiceResponse> => {
    return request<InvoiceResponse>(`/invoices/${id}/finalize`, {
      method: 'POST',
    });
  },

  // 4. Rate Schedules & Tariff Hierarchy
  searchRates: (query: string): Promise<TariffRateRule[]> => {
    return request<TariffRateRule[]>(`/rates/search?q=${encodeURIComponent(query)}`);
  },

  getTariffHierarchy: (hsnCode: string): Promise<TariffHierarchyNode[]> => {
    return request<TariffHierarchyNode[]>(`/rates/hierarchy/${encodeURIComponent(hsnCode)}`);
  },

  // 5. Activity Log & Audit
  listAuditLogs: (limit = 50, actionFilter?: string): Promise<AuditLogItem[]> => {
    const query = new URLSearchParams({ limit: limit.toString() });
    if (actionFilter) query.set('action', actionFilter);
    return request<AuditLogItem[]>(`/audit/logs?${query.toString()}`);
  },

  exportAuditLogs: (format: 'json' | 'csv'): Promise<Blob | string> => {
    return request<Blob | string>(`/audit/logs/export?format=${format}`);
  },

  // 6. Data Sync & Telemetry
  getSyncStatus: (): Promise<SyncStatusResponse> => {
    return request<SyncStatusResponse>('/admin/sync/status');
  },

  triggerSync: (source: string): Promise<SyncStatusResponse> => {
    return request<SyncStatusResponse>('/admin/sync/trigger', {
      method: 'POST',
      body: JSON.stringify({ source }),
    });
  },
};
