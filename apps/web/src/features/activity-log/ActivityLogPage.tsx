import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Download, Filter, RefreshCw } from 'lucide-react';
import { apiClient } from '../../api/client';
import { formatISTDateTime } from '../../lib/format';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';

export function ActivityLogPage() {
  const [filterAction, setFilterAction] = useState('');
  const [limit] = useState(50);

  const {
    data: logs,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['audit-logs', limit, filterAction],
    queryFn: () => apiClient.listAuditLogs(limit, filterAction || undefined),
  });

  const handleExport = async (format: 'json' | 'csv') => {
    try {
      const data = await apiClient.exportAuditLogs(format);
      const blob = typeof data === 'string' ? new Blob([data], { type: 'text/csv' }) : data;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `gst_audit_log_export_${Date.now()}.${format}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch {
      // Fallback
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-[var(--text-main)]">
            Statutory Activity Log & Tamper-Evident Trail
          </h1>
          <p className="text-sm text-[var(--text-muted)]">
            Every classification, invoice finalization, and GSTIN verification is logged with
            timestamp and user attribution.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="secondary" size="sm" onClick={() => handleExport('json')}>
            <Download className="mr-1.5 h-3.5 w-3.5" /> Export JSON
          </Button>
          <Button variant="secondary" size="sm" onClick={() => handleExport('csv')}>
            <Download className="mr-1.5 h-3.5 w-3.5" /> Export CSV
          </Button>
          <Button variant="secondary" size="sm" onClick={() => refetch()}>
            <RefreshCw className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>

      {/* Filter Bar */}
      <Card>
        <CardContent className="p-4 flex flex-col sm:flex-row items-center gap-4">
          <div className="relative flex-1 w-full">
            <Filter className="absolute left-3 top-2.5 h-4 w-4 text-[var(--text-muted)]" />
            <Input
              className="pl-9"
              placeholder="Filter by action (e.g. CLASSIFY, INVOICE_CREATE, GSTIN_VERIFY)..."
              value={filterAction}
              onChange={(e) => setFilterAction(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          {isLoading && (
            <div className="py-12 flex justify-center items-center">
              <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
            </div>
          )}

          {isError && (
            <div className="p-6 text-center text-sm text-[var(--danger)]">
              {(error as Error)?.message || 'Failed to load audit trail logs.'}
            </div>
          )}

          {!isLoading && logs && logs.length === 0 && (
            <div className="py-12 text-center text-sm text-[var(--text-muted)]">
              No audit logs recorded yet.
            </div>
          )}

          {logs && logs.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-[var(--surface-hover)] text-[var(--text-muted)] border-b border-[var(--border)] uppercase">
                  <tr>
                    <th className="px-4 py-3 font-medium">Timestamp (IST)</th>
                    <th className="px-4 py-3 font-medium">Action</th>
                    <th className="px-4 py-3 font-medium">User Email</th>
                    <th className="px-4 py-3 font-medium">Resource ID</th>
                    <th className="px-4 py-3 font-medium">IP Address</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {logs.map((log) => (
                    <tr key={log.id} className="hover:bg-[var(--surface-hover)]/40">
                      <td className="px-4 py-3 font-mono text-[var(--text-main)]">
                        {formatISTDateTime(log.timestamp)}
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant="primary">{log.action}</Badge>
                      </td>
                      <td className="px-4 py-3 text-[var(--text-main)]">{log.user_email}</td>
                      <td className="px-4 py-3 font-mono text-[var(--text-muted)]">
                        {log.resource_id || '—'}
                      </td>
                      <td className="px-4 py-3 font-mono text-[var(--text-muted)]">
                        {log.ip_address || '127.0.0.1'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
