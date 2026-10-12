import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import {
  Search,
  Sparkles,
  AlertTriangle,
  FileText,
  ChevronRight,
  Layers,
  HelpCircle,
} from 'lucide-react';
import { apiClient } from '../../api/client';
import { formatGSTRate, formatISTDate } from '../../lib/format';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';

export function ClassifyPage() {
  const [productDesc, setProductDesc] = useState('');
  const [unitPrice, setUnitPrice] = useState<string>('');
  const [isBranded] = useState<boolean>(true);

  const mutation = useMutation({
    mutationFn: (desc: string) =>
      apiClient.classifyProduct({
        product_description: desc,
        invoice_date: new Date().toISOString().split('T')[0],
        attributes: unitPrice
          ? { unit_price: Number(unitPrice), is_branded: isBranded }
          : undefined,
      }),
  });

  const handleClassify = (e: React.FormEvent) => {
    e.preventDefault();
    if (!productDesc.trim()) return;
    mutation.mutate(productDesc);
  };

  const handleRecalculate = () => {
    if (productDesc.trim()) {
      mutation.mutate(productDesc);
    }
  };

  const result = mutation.data;

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Search Header */}
      <div className="flex flex-col gap-1">
        <h1 className="text-xl font-semibold text-[var(--text-main)]">
          Statutory HSN / SAC Classification
        </h1>
        <p className="text-sm text-[var(--text-muted)]">
          Statutory classification engine powered by CBIC statutory rate schedules and real signal
          validation.
        </p>
      </div>

      {/* Input Form */}
      <Card>
        <CardContent className="p-5">
          <form onSubmit={handleClassify} className="space-y-4">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-[var(--text-muted)]" />
                <Input
                  className="pl-9"
                  placeholder="Enter product or service description (e.g. Men's genuine leather jacket with brass zip, Cotton shirt)..."
                  value={productDesc}
                  onChange={(e) => setProductDesc(e.target.value)}
                />
              </div>
              <Button type="submit" isLoading={mutation.isPending}>
                <Sparkles className="mr-1.5 h-4 w-4" />
                Classify
              </Button>
            </div>

            {/* Presets */}
            <div className="flex items-center gap-2 text-xs text-[var(--text-muted)]">
              <span>Quick presets:</span>
              {[
                'Leather jacket',
                'Solar panel',
                'Coffee beans',
                'Cotton t-shirt',
                'SaaS cloud subscription',
              ].map((preset) => (
                <button
                  key={preset}
                  type="button"
                  onClick={() => {
                    setProductDesc(preset);
                    mutation.mutate(preset);
                  }}
                  className="underline hover:text-[var(--text-main)] cursor-pointer"
                >
                  {preset}
                </button>
              ))}
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Loading State */}
      {mutation.isPending && (
        <Card>
          <CardContent className="py-12 flex flex-col items-center justify-center space-y-3">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
            <p className="text-sm text-[var(--text-muted)]">
              Evaluating CBIC tariff schedule, section notes, and computing real signal
              confidence...
            </p>
          </CardContent>
        </Card>
      )}

      {/* Error State */}
      {mutation.isError && (
        <Card className="border-[var(--danger-subtle)] bg-[var(--danger-subtle)]/20">
          <CardContent className="p-5 flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-[var(--danger)] shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-[var(--danger)]">
                Classification Service Unavailable
              </h4>
              <p className="text-xs text-[var(--text-main)] mt-1">
                {(mutation.error as Error)?.message ||
                  'Could not verify HSN classification against statutory schedule.'}
              </p>
              <Button
                variant="secondary"
                size="sm"
                className="mt-3"
                onClick={() => mutation.mutate(productDesc)}
              >
                Retry Request
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results View */}
      {result && (
        <div className="space-y-6">
          {/* Top Summary Card */}
          <Card className="border-l-4 border-l-[var(--primary)]">
            <CardContent className="p-6 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-2xl font-bold tracking-tight text-[var(--text-main)]">
                      {result.suggested_hsn}
                    </span>
                    <Badge variant={result.status === 'Matched' ? 'success' : 'warning'}>
                      {result.status}
                    </Badge>
                    <Badge variant="neutral">Match Quality: {result.match_quality}</Badge>
                  </div>
                  <p className="text-sm text-[var(--text-main)] font-medium mt-1">
                    {result.hsn_description}
                  </p>
                </div>

                <div className="text-right sm:border-l sm:border-[var(--border)] sm:pl-6">
                  <div className="text-2xl font-bold text-[var(--text-main)] font-mono">
                    {formatGSTRate(result.gst_rate)}
                  </div>
                  <div className="text-xs text-[var(--text-muted)] mt-0.5">
                    {result.effective_rate_text}
                  </div>
                </div>
              </div>

              {/* Hierarchy Breadcrumb */}
              <div className="flex items-center gap-1.5 text-xs text-[var(--text-muted)] pt-2 border-t border-[var(--border)]">
                <Layers className="h-3.5 w-3.5 text-[var(--text-muted)]" />
                <span>Chapter {result.chapter}</span>
                <ChevronRight className="h-3 w-3" />
                <span>Heading {result.heading}</span>
                <ChevronRight className="h-3 w-3" />
                <span className="font-mono font-medium text-[var(--text-main)]">
                  {result.suggested_hsn}
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Conditional Attributes Recalculation */}
          {result.signals.missing_conditions_penalty > 0 && (
            <Card className="border-[var(--warning)] bg-[var(--warning-subtle)]/30">
              <CardContent className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-3">
                  <HelpCircle className="h-5 w-5 text-[var(--warning)] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-semibold text-[var(--text-main)] uppercase tracking-wide">
                      Conditional Rate Rule Detected
                    </h4>
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">
                      Statutory GST rate for this commodity depends on price threshold or branding.
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Input
                    type="number"
                    placeholder="Unit price per piece (₹)"
                    value={unitPrice}
                    onChange={(e) => setUnitPrice(e.target.value)}
                    className="w-44 h-8 text-xs bg-[var(--surface)]"
                  />
                  <Button size="sm" onClick={handleRecalculate}>
                    Recalculate
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Grid of Reasoning and Signal Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Real Signal Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Real Confidence Signal Breakdown</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-[var(--text-muted)]">Computed Raw Score:</span>
                  <span className="font-mono font-bold text-[var(--text-main)]">
                    {result.signals.computed_raw_confidence} / 100
                  </span>
                </div>
                <div className="w-full bg-[var(--surface-hover)] rounded-full h-2">
                  <div
                    className="bg-[var(--primary)] h-2 rounded-full transition-all"
                    style={{
                      width: `${Math.min(100, Math.max(0, result.signals.computed_raw_confidence))}%`,
                    }}
                  />
                </div>

                <div className="pt-2 space-y-2 text-xs border-t border-[var(--border)]">
                  <div className="flex justify-between">
                    <span className="text-[var(--text-muted)]">Keyword Match Signal:</span>
                    <span className="font-mono">{result.signals.keyword_match_score}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[var(--text-muted)]">Vector Similarity Score:</span>
                    <span className="font-mono">{result.signals.vector_similarity_score}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[var(--text-muted)]">Statutory Rule Verified:</span>
                    <span>{result.signals.statutory_rule_match ? 'Yes (+15%)' : 'No'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[var(--text-muted)]">Agreeing CBIC Sources:</span>
                    <span className="font-mono">{result.signals.agreeing_sources_count}</span>
                  </div>
                  {result.signals.missing_conditions_penalty > 0 && (
                    <div className="flex justify-between text-[var(--warning)]">
                      <span>Missing Condition Penalty:</span>
                      <span className="font-mono">
                        -{result.signals.missing_conditions_penalty}%
                      </span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Legal Reasoning Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Audit-Defensible Legal Rationale</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-xs">
                <p className="text-[var(--text-main)] leading-relaxed italic bg-[var(--surface-hover)] p-3 rounded-[var(--radius-md)] border border-[var(--border)]">
                  "{result.reasoning_summary}"
                </p>
                <div className="space-y-1 pt-1">
                  <span className="font-medium text-[var(--text-muted)]">Evaluated Factors:</span>
                  <ul className="list-disc list-inside space-y-0.5 text-[var(--text-muted)]">
                    {result.evaluation_factors.map((factor, idx) => (
                      <li key={idx}>{factor}</li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sources Table */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Statutory Evidence & CBIC Notifications</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-[var(--surface-hover)] text-[var(--text-muted)] border-y border-[var(--border)] uppercase">
                    <tr>
                      <th className="px-4 py-2.5 font-medium">Document</th>
                      <th className="px-4 py-2.5 font-medium">Notification No. & Date</th>
                      <th className="px-4 py-2.5 font-medium">Schedule & S.No.</th>
                      <th className="px-4 py-2.5 font-medium">Effective From</th>
                      <th className="px-4 py-2.5 font-medium text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border)]">
                    {result.sources.map((src, idx) => (
                      <tr key={idx} className="hover:bg-[var(--surface-hover)]/50">
                        <td className="px-4 py-3 font-medium text-[var(--text-main)]">
                          {src.document}
                        </td>
                        <td className="px-4 py-3">
                          {src.notification} ({src.notification_date})
                        </td>
                        <td className="px-4 py-3">
                          {src.schedule} • S.No. {src.serial_no}
                        </td>
                        <td className="px-4 py-3 font-mono">{formatISTDate(src.effective_from)}</td>
                        <td className="px-4 py-3 text-right">
                          {src.url ? (
                            <a
                              href={src.url}
                              target="_blank"
                              rel="noreferrer"
                              className="inline-flex items-center gap-1 text-[var(--primary)] hover:underline"
                            >
                              <FileText className="h-3.5 w-3.5" />
                              Open PDF
                            </a>
                          ) : (
                            '—'
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          {/* Alternatives Considered */}
          {result.alternatives_considered.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">
                  Alternative Classifications Considered (Score ≥ 40%)
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <div className="divide-y divide-[var(--border)] text-xs">
                  {result.alternatives_considered.map((alt, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 flex items-center justify-between hover:bg-[var(--surface-hover)]/40"
                    >
                      <div>
                        <span className="font-mono font-bold text-[var(--text-main)] mr-2">
                          {alt.hsn_code}
                        </span>
                        <span className="text-[var(--text-muted)]">{alt.description}</span>
                      </div>
                      <Badge variant="neutral">Score: {Math.round(alt.score * 100)}%</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
