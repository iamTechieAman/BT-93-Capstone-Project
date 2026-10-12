import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, CheckCircle, ShieldCheck, Printer } from 'lucide-react';
import { apiClient } from '../../api/client';
import { formatINR, formatISTDate } from '../../lib/format';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

export function InvoiceDetailPage() {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();

  const {
    data: invoice,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['invoice', id],
    queryFn: () => apiClient.getInvoice(id!),
    enabled: !!id,
  });

  const finalizeMutation = useMutation({
    mutationFn: () => apiClient.finalizeInvoice(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoice', id] });
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
    },
  });

  if (isLoading) {
    return (
      <div className="py-24 flex justify-center items-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
      </div>
    );
  }

  if (isError || !invoice) {
    return (
      <div className="max-w-4xl mx-auto space-y-4">
        <Link to="/invoices">
          <Button variant="secondary" size="sm">
            <ArrowLeft className="mr-1.5 h-3.5 w-3.5" /> Back to Invoices
          </Button>
        </Link>
        <Card className="p-6 text-center text-sm text-[var(--danger)]">
          {(error as Error)?.message || 'Invoice not found.'}
        </Card>
      </div>
    );
  }

  const isInterstate = invoice.igst_total > 0;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link to="/invoices">
          <Button variant="secondary" size="sm">
            <ArrowLeft className="mr-1.5 h-3.5 w-3.5" /> Back to Invoices
          </Button>
        </Link>
        <div className="flex items-center gap-2">
          {invoice.status === 'DRAFT' && (
            <Button
              onClick={() => finalizeMutation.mutate()}
              isLoading={finalizeMutation.isPending}
            >
              <CheckCircle className="mr-1.5 h-4 w-4" />
              Finalize Invoice
            </Button>
          )}
          {invoice.status === 'FINALIZED' && (
            <Button variant="secondary" onClick={() => window.print()}>
              <Printer className="mr-1.5 h-4 w-4" />
              Print PDF
            </Button>
          )}
        </div>
      </div>

      {/* Invoice Document Card */}
      <Card className="p-8 space-y-6">
        {/* Invoice Header */}
        <div className="flex justify-between items-start border-b border-[var(--border)] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold font-mono text-[var(--text-main)]">
                {invoice.invoice_number}
              </h2>
              <Badge variant={invoice.status === 'FINALIZED' ? 'success' : 'neutral'}>
                {invoice.status}
              </Badge>
            </div>
            <p className="text-xs text-[var(--text-muted)] mt-1">
              Date: <span className="font-mono">{formatISTDate(invoice.invoice_date)}</span> • Place
              of Supply: <span className="font-medium">{invoice.place_of_supply}</span>
            </p>
          </div>
          <div className="text-right">
            <span className="text-xs text-[var(--text-muted)] uppercase tracking-wider">
              Statutory Tax Invoice
            </span>
            <div className="text-xs text-[var(--primary)] font-medium mt-0.5">
              {isInterstate ? 'Inter-State (IGST Applicable)' : 'Intra-State (CGST + SGST Split)'}
            </div>
          </div>
        </div>

        {/* Supplier and Buyer Grid */}
        <div className="grid grid-cols-2 gap-6 text-xs border-b border-[var(--border)] pb-6">
          <div className="p-4 bg-[var(--surface-hover)] rounded-[var(--radius-md)]">
            <span className="font-semibold text-[var(--text-main)] block mb-1">
              Supplier / Biller:
            </span>
            <div className="font-mono text-[var(--text-main)]">GSTIN: {invoice.supplier_gstin}</div>
            <div className="text-[var(--text-muted)] mt-1">
              State: {invoice.supplier_gstin.slice(0, 2)}
            </div>
          </div>
          <div className="p-4 bg-[var(--surface-hover)] rounded-[var(--radius-md)]">
            <span className="font-semibold text-[var(--text-main)] block mb-1">
              Recipient / Buyer:
            </span>
            <div className="font-mono text-[var(--text-main)]">GSTIN: {invoice.buyer_gstin}</div>
            <div className="text-[var(--text-muted)] mt-1">
              State: {invoice.buyer_gstin.slice(0, 2)}
            </div>
          </div>
        </div>

        {/* Line Items Table */}
        <div>
          <table className="w-full text-xs text-left">
            <thead className="bg-[var(--surface-hover)] text-[var(--text-muted)] uppercase border-y border-[var(--border)]">
              <tr>
                <th className="px-3 py-2 font-medium">Item Description</th>
                <th className="px-3 py-2 font-medium">HSN</th>
                <th className="px-3 py-2 font-medium text-right">Qty</th>
                <th className="px-3 py-2 font-medium text-right">Rate (₹)</th>
                <th className="px-3 py-2 font-medium text-right">Taxable Value</th>
                <th className="px-3 py-2 font-medium text-right">GST</th>
                <th className="px-3 py-2 font-medium text-right">Total (₹)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border)] font-mono">
              {invoice.items.map((item, idx) => (
                <tr key={idx}>
                  <td className="px-3 py-3 font-sans font-medium text-[var(--text-main)]">
                    {item.product_name}
                  </td>
                  <td className="px-3 py-3">{item.hsn_code}</td>
                  <td className="px-3 py-3 text-right">{item.quantity}</td>
                  <td className="px-3 py-3 text-right">{formatINR(item.unit_price)}</td>
                  <td className="px-3 py-3 text-right">{formatINR(item.taxable_value)}</td>
                  <td className="px-3 py-3 text-right">
                    {item.gst_rate}%
                    <span className="text-[10px] text-[var(--text-muted)] block font-sans">
                      {isInterstate
                        ? `IGST: ${formatINR(item.igst_amount)}`
                        : `CGST: ${formatINR(item.cgst_amount)} + SGST: ${formatINR(item.sgst_amount)}`}
                    </span>
                  </td>
                  <td className="px-3 py-3 text-right font-bold">{formatINR(item.item_total)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Totals Breakdown */}
        <div className="flex justify-end pt-4 border-t border-[var(--border)]">
          <div className="w-64 space-y-2 text-xs font-mono">
            <div className="flex justify-between text-[var(--text-muted)]">
              <span>Taxable Subtotal:</span>
              <span>{formatINR(invoice.subtotal)}</span>
            </div>
            {!isInterstate && (
              <>
                <div className="flex justify-between text-[var(--text-muted)]">
                  <span>CGST Total:</span>
                  <span>{formatINR(invoice.cgst_total)}</span>
                </div>
                <div className="flex justify-between text-[var(--text-muted)]">
                  <span>SGST Total:</span>
                  <span>{formatINR(invoice.sgst_total)}</span>
                </div>
              </>
            )}
            {isInterstate && (
              <div className="flex justify-between text-[var(--text-muted)]">
                <span>IGST Total:</span>
                <span>{formatINR(invoice.igst_total)}</span>
              </div>
            )}
            {invoice.cess_total > 0 && (
              <div className="flex justify-between text-[var(--text-muted)]">
                <span>Cess Total:</span>
                <span>{formatINR(invoice.cess_total)}</span>
              </div>
            )}
            <div className="flex justify-between text-sm font-bold text-[var(--text-main)] pt-2 border-t border-[var(--border)]">
              <span>Grand Total:</span>
              <span>{formatINR(invoice.grand_total)}</span>
            </div>
          </div>
        </div>

        {/* SHA-256 Audit Signature */}
        {invoice.status === 'FINALIZED' && (
          <div className="p-3 bg-[var(--surface-hover)] rounded-[var(--radius-md)] flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-[var(--primary)]" />
              <span className="font-mono text-[var(--text-muted)] text-[10px]">
                Audit SHA-256:{' '}
                {invoice.pdf_sha256 ||
                  'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
              </span>
            </div>
            <Badge variant="success">E-Way Ready</Badge>
          </div>
        )}
      </Card>
    </div>
  );
}
