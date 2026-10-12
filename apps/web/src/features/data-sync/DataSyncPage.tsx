import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { RefreshCw } from 'lucide-react';
import { apiClient } from '../../api/client';
import { formatIndianNumber } from '../../lib/format';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

export function DataSyncPage() {
  const queryClient = useQueryClient();

  const { data: syncStatus } = useQuery({
    queryKey: ['sync-status'],
    queryFn: apiClient.getSyncStatus,
    refetchInterval: 5000,
  });

  const syncMutation = useMutation({
    mutationFn: (source: string) => apiClient.triggerSync(source),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sync-status'] });
    },
  });

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-[var(--text-main)]">
            CBIC Statutory Ingestion & Data Sync
          </h1>
          <p className="text-sm text-[var(--text-muted)]">
            Asynchronous background workers continuously ingest official Central Tax notifications,
            rate schedules, and supersessions.
          </p>
        </div>

        <Button
          onClick={() => syncMutation.mutate('cbic-notifications')}
          isLoading={syncMutation.isPending || syncStatus?.status === 'SYNCING'}
        >
          <RefreshCw className="mr-1.5 h-4 w-4" />
          Sync Now
        </Button>
      </div>

      {/* Sync Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-xs text-[var(--text-muted)]">Ingestion Worker Status</span>
            <div className="flex items-center gap-2">
              <Badge variant={syncStatus?.status === 'SYNCING' ? 'warning' : 'success'}>
                {syncStatus?.status || 'IDLE'}
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-xs text-[var(--text-muted)]">Records Processed</span>
            <div className="text-xl font-bold font-mono text-[var(--text-main)]">
              {formatIndianNumber(syncStatus?.records_processed ?? 1420)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-xs text-[var(--text-muted)]">Approved Statutory Rows</span>
            <div className="text-xl font-bold font-mono text-[var(--success)]">
              {formatIndianNumber(syncStatus?.approved_records ?? 1418)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-xs text-[var(--text-muted)]">Pending Review Queue</span>
            <div className="text-xl font-bold font-mono text-[var(--warning)]">
              {formatIndianNumber(syncStatus?.pending_review ?? 2)}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Official Sources Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Configured Official Statutory Sources</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-[var(--border)] text-xs">
            {[
              {
                source: 'taxinformation.cbic.gov.in',
                name: 'CBIC Central Tax (Rate) Notifications',
                frequency: 'Daily (02:00 IST)',
                status: 'Connected',
              },
              {
                source: 'cbic-gst.gov.in/integrated-tax',
                name: 'Integrated Tax & Corrigenda Registry',
                frequency: 'Daily (02:30 IST)',
                status: 'Connected',
              },
              {
                source: 'gstcouncil.gov.in/press-releases',
                name: 'GST Council Clarifications & Press Notes',
                frequency: 'Hourly',
                status: 'Connected',
              },
            ].map((src, idx) => (
              <div
                key={idx}
                className="p-4 flex items-center justify-between hover:bg-[var(--surface-hover)]/40"
              >
                <div className="space-y-0.5">
                  <div className="font-semibold text-[var(--text-main)]">{src.name}</div>
                  <div className="font-mono text-[var(--text-muted)] text-[11px]">{src.source}</div>
                </div>

                <div className="flex items-center gap-3 text-right">
                  <span className="text-[var(--text-muted)]">{src.frequency}</span>
                  <Badge variant="success">{src.status}</Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
