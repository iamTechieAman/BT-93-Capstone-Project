import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Layers, ChevronRight } from 'lucide-react';
import { apiClient } from '../../api/client';
import type { TariffRateRule } from '../../api/types';
import { formatGSTRate, formatISTDate } from '../../lib/format';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerDescription,
} from '../../components/ui/Drawer';

export function RateSchedulePage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRule, setSelectedRule] = useState<TariffRateRule | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const {
    data: rules,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['rates', searchQuery],
    queryFn: () => apiClient.searchRates(searchQuery),
  });

  const { data: hierarchy } = useQuery({
    queryKey: ['tariff-hierarchy', selectedRule?.hsn_code],
    queryFn: () => apiClient.getTariffHierarchy(selectedRule!.hsn_code),
    enabled: !!selectedRule,
  });

  const handleOpenPreview = (rule: TariffRateRule) => {
    setSelectedRule(rule);
    setIsDrawerOpen(true);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-[var(--text-main)]">
          Statutory GST Rate Schedule
        </h1>
        <p className="text-sm text-[var(--text-muted)]">
          Search CBIC Central Tax & Integrated Tax rate notifications with statutory hierarchy and
          effective dates.
        </p>
      </div>

      {/* Search Input */}
      <Card>
        <CardContent className="p-5">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-[var(--text-muted)]" />
            <Input
              className="pl-9"
              placeholder="Search by HSN code (e.g. 4203, 8541, 0901) or description (leather, solar, coffee, software)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Rate Table */}
      <Card>
        <CardContent className="p-0">
          {isLoading && (
            <div className="py-12 flex justify-center items-center">
              <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
            </div>
          )}

          {isError && (
            <div className="p-8 text-center space-y-3">
              <div className="text-sm font-medium text-[var(--danger)]">
                {(error as Error)?.message ||
                  'Failed to load statutory rate schedules from server.'}
              </div>
              <Button variant="secondary" size="sm" onClick={() => refetch()}>
                Retry Request
              </Button>
            </div>
          )}

          {!isLoading && !isError && rules && rules.length === 0 && (
            <div className="py-12 text-center space-y-2">
              <p className="text-sm font-medium text-[var(--text-main)]">
                {searchQuery
                  ? `No matching statutory rate schedules found for "${searchQuery}".`
                  : 'No rate data loaded. Run data sync.'}
              </p>
              {!searchQuery && (
                <p className="text-xs text-[var(--text-muted)]">
                  The statutory database has no active tariff schedules. Ingest official
                  notifications or apply seed data.
                </p>
              )}
            </div>
          )}

          {rules && rules.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-[var(--surface-hover)] text-[var(--text-muted)] border-b border-[var(--border)] uppercase">
                  <tr>
                    <th className="px-4 py-3 font-medium">HSN / SAC</th>
                    <th className="px-4 py-3 font-medium">Description</th>
                    <th className="px-4 py-3 font-medium">Rate</th>
                    <th className="px-4 py-3 font-medium">Schedule & Notification</th>
                    <th className="px-4 py-3 font-medium">Effective From</th>
                    <th className="px-4 py-3 font-medium text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {rules.map((rule) => (
                    <tr key={rule.id} className="hover:bg-[var(--surface-hover)]/40">
                      <td className="px-4 py-3 font-mono font-bold text-[var(--text-main)]">
                        {rule.hsn_code}
                      </td>
                      <td className="px-4 py-3 text-[var(--text-main)] max-w-xs">
                        {rule.description}
                      </td>
                      <td className="px-4 py-3 font-mono font-bold text-[var(--primary)]">
                        {formatGSTRate(rule.rate)}
                      </td>
                      <td className="px-4 py-3 text-[var(--text-muted)]">
                        {rule.schedule} • {rule.notification_no}
                      </td>
                      <td className="px-4 py-3 font-mono">{formatISTDate(rule.effective_from)}</td>
                      <td className="px-4 py-3 text-right">
                        <Button
                          variant="secondary"
                          size="sm"
                          onClick={() => handleOpenPreview(rule)}
                        >
                          <Layers className="mr-1 h-3.5 w-3.5" />
                          View Hierarchy
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Hierarchy Drawer */}
      <Drawer open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
        <DrawerContent>
          <DrawerHeader>
            <DrawerTitle>Tariff Hierarchy & Schedule Notes</DrawerTitle>
            <DrawerDescription>
              Relational taxonomy structure: Chapter &gt; Heading &gt; Sub-heading &gt; Tariff Item
            </DrawerDescription>
          </DrawerHeader>

          {selectedRule && (
            <div className="space-y-6 pt-4 text-xs">
              <div className="p-4 bg-[var(--surface-hover)] rounded-[var(--radius-md)] space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-mono text-base font-bold text-[var(--text-main)]">
                    HSN {selectedRule.hsn_code}
                  </span>
                  <Badge variant="primary">{formatGSTRate(selectedRule.rate)}</Badge>
                </div>
                <p className="text-[var(--text-main)] font-medium">{selectedRule.description}</p>
                <div className="text-[var(--text-muted)] pt-1 border-t border-[var(--border)]">
                  {selectedRule.notification_no} ({selectedRule.notification_date}) •{' '}
                  {selectedRule.schedule}
                </div>
              </div>

              {/* Taxonomy Breadcrumb Steps */}
              <div className="space-y-3">
                <span className="font-semibold text-[var(--text-main)] block">
                  Classification Hierarchy Chain:
                </span>
                <div className="space-y-2">
                  {hierarchy && hierarchy.length > 0 ? (
                    hierarchy.map((node) => (
                      <div
                        key={node.code}
                        className="p-3 border border-[var(--border)] rounded-[var(--radius-md)] flex items-start gap-2 bg-[var(--surface)]"
                      >
                        <span className="font-mono font-bold text-[var(--primary)] uppercase text-[10px]">
                          {node.level}:
                        </span>
                        <div>
                          <div className="font-mono font-medium text-[var(--text-main)]">
                            {node.code}
                          </div>
                          <div className="text-[var(--text-muted)] mt-0.5">{node.title}</div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="p-3 border border-[var(--border)] rounded-[var(--radius-md)] space-y-1">
                      <div>Chapter {selectedRule.hsn_code.slice(0, 2)}</div>
                      <ChevronRight className="h-3 w-3 text-[var(--text-muted)]" />
                      <div>Heading {selectedRule.hsn_code.slice(0, 4)}</div>
                      <ChevronRight className="h-3 w-3 text-[var(--text-muted)]" />
                      <div className="font-mono font-bold text-[var(--text-main)]">
                        {selectedRule.hsn_code}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </DrawerContent>
      </Drawer>
    </div>
  );
}
