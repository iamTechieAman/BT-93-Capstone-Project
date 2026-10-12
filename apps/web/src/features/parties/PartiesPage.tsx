import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Search, CheckCircle2, XCircle, MinusCircle, AlertCircle } from 'lucide-react';
import { apiClient } from '../../api/client';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';

export function PartiesPage() {
  const [gstinInput, setGstinInput] = useState('');

  const mutation = useMutation({
    mutationFn: (gstin: string) => apiClient.verifyGstin(gstin),
  });

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    const cleaned = gstinInput.trim().toUpperCase();
    if (!cleaned) return;
    mutation.mutate(cleaned);
  };

  const result = mutation.data;

  // Small client-side format hint strictly for typing feedback (API remains single source of truth)
  const formatHint =
    gstinInput.length > 0 && gstinInput.length !== 15
      ? `GSTIN must be 15 characters (${gstinInput.length}/15)`
      : null;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-[var(--text-main)]">
          Party Verification & GSTIN Lookup
        </h1>
        <p className="text-sm text-[var(--text-muted)]">
          Real-time statutory format validation, Mod-36 checksum verification, and registry taxpayer
          status.
        </p>
      </div>

      {/* Lookup Card */}
      <Card>
        <CardContent className="p-5">
          <form onSubmit={handleVerify} className="space-y-3">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-[var(--text-muted)]" />
                <Input
                  className="pl-9 font-mono uppercase"
                  placeholder="Enter 15-character GSTIN (e.g. 27AAPFU0939F1ZV, 29ABCDE1234F1ZW)..."
                  value={gstinInput}
                  onChange={(e) => setGstinInput(e.target.value.toUpperCase())}
                  maxLength={15}
                />
              </div>
              <Button type="submit" isLoading={mutation.isPending}>
                Verify GSTIN
              </Button>
            </div>

            {formatHint && (
              <div className="text-xs text-[var(--text-muted)] flex items-center gap-1">
                <AlertCircle className="h-3.5 w-3.5 text-[var(--text-muted)]" />
                {formatHint}
              </div>
            )}

            {/* Quick Test Vectors */}
            <div className="flex flex-wrap items-center gap-2 text-xs text-[var(--text-muted)] pt-1">
              <span>Test vectors:</span>
              {[
                { label: 'Maharashtra Valid', gstin: '27AAPFU0939F1ZV' },
                { label: 'Karnataka Valid', gstin: '29ABCDE1234F1ZW' },
                { label: 'Delhi Valid', gstin: '07AAAAA0000A1Z4' },
                { label: 'Invalid Checksum', gstin: '29ABCDE1234F1ZX' },
                { label: 'Invalid State', gstin: '99ABCDE1234F1ZW' },
              ].map((item) => (
                <button
                  key={item.gstin}
                  type="button"
                  onClick={() => {
                    setGstinInput(item.gstin);
                    mutation.mutate(item.gstin);
                  }}
                  className="underline hover:text-[var(--text-main)] cursor-pointer font-mono"
                >
                  {item.label}
                </button>
              ))}
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Loading Indicator */}
      {mutation.isPending && (
        <Card>
          <CardContent className="py-12 flex flex-col items-center justify-center space-y-3">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
            <p className="text-sm text-[var(--text-muted)]">
              Verifying state code, PAN pattern, Mod-36 checksum, and registry status...
            </p>
          </CardContent>
        </Card>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Headline Summary Card */}
          <Card
            className={
              result.verification_status === 'PASSED'
                ? 'border-l-4 border-l-[var(--success)]'
                : 'border-l-4 border-l-[var(--danger)]'
            }
          >
            <CardContent className="p-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-2xl font-bold text-[var(--text-main)]">
                      {result.gstin}
                    </span>
                    <Badge variant={result.verification_status === 'PASSED' ? 'success' : 'danger'}>
                      {result.verification_status}
                    </Badge>
                  </div>
                  <h3 className="text-base font-semibold text-[var(--text-main)] mt-1">
                    {result.headline}
                  </h3>
                  {result.state_name && (
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">
                      State:{' '}
                      <span className="font-medium text-[var(--text-main)]">
                        {result.state_name} ({result.state_code})
                      </span>{' '}
                      • PAN:{' '}
                      <span className="font-mono font-medium text-[var(--text-main)]">
                        {result.pan}
                      </span>
                    </p>
                  )}
                </div>

                <div className="text-right sm:border-l sm:border-[var(--border)] sm:pl-6 text-xs text-[var(--text-muted)]">
                  <div>
                    Latency: <span className="font-mono">{result.latency_ms}ms</span>
                  </div>
                  <div>
                    Taxpayer Status:{' '}
                    <span className="font-medium text-[var(--text-main)]">
                      {result.taxpayer_status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Failures or Warnings */}
              {result.validation_failures.length > 0 && (
                <div className="mt-4 p-3 bg-[var(--danger-subtle)]/40 rounded-[var(--radius-md)] border border-[var(--danger-subtle)] text-xs text-[var(--danger)] space-y-1">
                  <span className="font-semibold block">Validation Errors:</span>
                  <ul className="list-disc list-inside space-y-0.5">
                    {result.validation_failures.map((err, i) => (
                      <li key={i}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Step-by-Step Statutory Pipeline Card */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Statutory Verification Pipeline Steps</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="divide-y divide-[var(--border)] text-xs">
                {result.steps.map((step) => (
                  <div
                    key={step.id}
                    className="p-3.5 flex items-center justify-between hover:bg-[var(--surface-hover)]/40"
                  >
                    <div className="flex items-center gap-3">
                      {step.state === 'PASSED' && (
                        <CheckCircle2 className="h-4 w-4 text-[var(--success)]" />
                      )}
                      {step.state === 'FAILED' && (
                        <XCircle className="h-4 w-4 text-[var(--danger)]" />
                      )}
                      {step.state === 'SKIPPED' && (
                        <MinusCircle className="h-4 w-4 text-[var(--text-muted)]" />
                      )}
                      <span className="font-medium text-[var(--text-main)]">{step.name}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="text-[var(--text-muted)]">{step.detail || '—'}</span>
                      <Badge
                        variant={
                          step.state === 'PASSED'
                            ? 'success'
                            : step.state === 'FAILED'
                              ? 'danger'
                              : 'neutral'
                        }
                      >
                        {step.state}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
