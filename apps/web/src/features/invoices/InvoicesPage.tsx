import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Plus, Trash2 } from 'lucide-react';
import { apiClient } from '../../api/client';
import type { InvoiceCreatePayload, InvoiceLineItemInput } from '../../api/types';
import { formatINR, formatISTDate } from '../../lib/format';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';
import { Modal, ModalContent, ModalHeader, ModalTitle } from '../../components/ui/Modal';

export function InvoicesPage() {
  const queryClient = useQueryClient();
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  // Form State
  const [invoiceNumber, setInvoiceNumber] = useState(
    () => `INV-${Date.now().toString().slice(-5)}`
  );
  const [supplierGstin, setSupplierGstin] = useState('27AAPFU0939F1ZV');
  const [buyerGstin, setBuyerGstin] = useState('29ABCDE1234F1ZW');
  const [placeOfSupply, setPlaceOfSupply] = useState('29-Karnataka');
  const [lineItems, setLineItems] = useState<InvoiceLineItemInput[]>([
    {
      product_name: "Men's Leather Jacket",
      hsn_code: '42031010',
      quantity: 2,
      unit_price: 3500.0,
      gst_rate: 18.0,
      cess_rate: 0.0,
    },
  ]);

  const {
    data: invoices,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['invoices'],
    queryFn: apiClient.listInvoices,
  });

  const createMutation = useMutation({
    mutationFn: (payload: InvoiceCreatePayload) => apiClient.createInvoice(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      setIsCreateOpen(false);
    },
  });

  const handleAddItem = () => {
    setLineItems([
      ...lineItems,
      {
        product_name: '',
        hsn_code: '',
        quantity: 1,
        unit_price: 1000.0,
        gst_rate: 18.0,
        cess_rate: 0.0,
      },
    ]);
  };

  const handleRemoveItem = (index: number) => {
    setLineItems(lineItems.filter((_, i) => i !== index));
  };

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate({
      invoice_number: invoiceNumber,
      invoice_date: new Date().toISOString().split('T')[0],
      supplier_gstin: supplierGstin,
      buyer_gstin: buyerGstin,
      place_of_supply: placeOfSupply,
      line_items: lineItems,
    });
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-[var(--text-main)]">
            Tax Invoices & E-Way Generation
          </h1>
          <p className="text-sm text-[var(--text-muted)]">
            Statutory B2B GST invoices computed strictly with Decimal precision and verified place
            of supply.
          </p>
        </div>
        <Button onClick={() => setIsCreateOpen(true)}>
          <Plus className="mr-1.5 h-4 w-4" />
          Create Invoice
        </Button>
      </div>

      {/* Invoice List Table */}
      <Card>
        <CardContent className="p-0">
          {isLoading && (
            <div className="py-12 flex justify-center items-center">
              <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
            </div>
          )}

          {isError && (
            <div className="p-6 text-center text-sm text-[var(--danger)]">
              {(error as Error)?.message || 'Failed to load invoices from database.'}
            </div>
          )}

          {!isLoading && invoices && invoices.length === 0 && (
            <div className="py-12 text-center text-sm text-[var(--text-muted)]">
              No invoices created yet. Click "Create Invoice" to start.
            </div>
          )}

          {invoices && invoices.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-[var(--surface-hover)] text-[var(--text-muted)] border-b border-[var(--border)] uppercase">
                  <tr>
                    <th className="px-4 py-3 font-medium">Invoice No.</th>
                    <th className="px-4 py-3 font-medium">Date</th>
                    <th className="px-4 py-3 font-medium">Supplier & Buyer GSTIN</th>
                    <th className="px-4 py-3 font-medium">Taxable Value</th>
                    <th className="px-4 py-3 font-medium">Grand Total</th>
                    <th className="px-4 py-3 font-medium">Status</th>
                    <th className="px-4 py-3 font-medium text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {invoices.map((inv) => (
                    <tr key={inv.id} className="hover:bg-[var(--surface-hover)]/40">
                      <td className="px-4 py-3 font-mono font-medium text-[var(--text-main)]">
                        <Link
                          to={`/invoices/${inv.id}`}
                          className="hover:text-[var(--primary)] underline"
                        >
                          {inv.invoice_number}
                        </Link>
                      </td>
                      <td className="px-4 py-3 font-mono">{formatISTDate(inv.invoice_date)}</td>
                      <td className="px-4 py-3">
                        <div className="font-mono text-[var(--text-main)]">
                          {inv.supplier_gstin}
                        </div>
                        <div className="font-mono text-[var(--text-muted)]">
                          → {inv.buyer_gstin}
                        </div>
                      </td>
                      <td className="px-4 py-3 font-mono">{formatINR(inv.subtotal)}</td>
                      <td className="px-4 py-3 font-mono font-bold text-[var(--text-main)]">
                        {formatINR(inv.grand_total)}
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant={inv.status === 'FINALIZED' ? 'success' : 'neutral'}>
                          {inv.status}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Link to={`/invoices/${inv.id}`}>
                          <Button variant="secondary" size="sm">
                            View Details
                          </Button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Create Invoice Modal */}
      <Modal open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <ModalContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <ModalHeader>
            <ModalTitle>Create Statutory Tax Invoice</ModalTitle>
          </ModalHeader>
          <form onSubmit={handleCreateSubmit} className="space-y-4 pt-2">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-[var(--text-muted)]">
                  Invoice Number
                </label>
                <Input
                  value={invoiceNumber}
                  onChange={(e) => setInvoiceNumber(e.target.value)}
                  className="font-mono"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-medium text-[var(--text-muted)]">
                  Place of Supply
                </label>
                <Input
                  value={placeOfSupply}
                  onChange={(e) => setPlaceOfSupply(e.target.value)}
                  placeholder="29-Karnataka"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-[var(--text-muted)]">
                  Supplier GSTIN
                </label>
                <Input
                  value={supplierGstin}
                  onChange={(e) => setSupplierGstin(e.target.value.toUpperCase())}
                  className="font-mono"
                  required
                  maxLength={15}
                />
              </div>
              <div>
                <label className="text-xs font-medium text-[var(--text-muted)]">Buyer GSTIN</label>
                <Input
                  value={buyerGstin}
                  onChange={(e) => setBuyerGstin(e.target.value.toUpperCase())}
                  className="font-mono"
                  required
                  maxLength={15}
                />
              </div>
            </div>

            {/* Line items */}
            <div className="space-y-2 pt-2 border-t border-[var(--border)]">
              <div className="flex justify-between items-center">
                <span className="text-xs font-semibold text-[var(--text-main)]">
                  Invoice Line Items
                </span>
                <Button type="button" variant="secondary" size="sm" onClick={handleAddItem}>
                  <Plus className="mr-1 h-3.5 w-3.5" />
                  Add Line
                </Button>
              </div>

              {lineItems.map((item, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-[var(--surface-hover)] rounded-[var(--radius-md)] space-y-2 text-xs"
                >
                  <div className="grid grid-cols-3 gap-2">
                    <div className="col-span-2">
                      <Input
                        placeholder="Product name"
                        value={item.product_name}
                        onChange={(e) => {
                          const updated = [...lineItems];
                          updated[idx].product_name = e.target.value;
                          setLineItems(updated);
                        }}
                        required
                      />
                    </div>
                    <div>
                      <Input
                        placeholder="HSN (8 digits)"
                        value={item.hsn_code}
                        onChange={(e) => {
                          const updated = [...lineItems];
                          updated[idx].hsn_code = e.target.value;
                          setLineItems(updated);
                        }}
                        className="font-mono"
                        required
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-2 items-center">
                    <div>
                      <label className="text-[10px] text-[var(--text-muted)]">Qty</label>
                      <Input
                        type="number"
                        min="1"
                        value={item.quantity}
                        onChange={(e) => {
                          const updated = [...lineItems];
                          updated[idx].quantity = Number(e.target.value);
                          setLineItems(updated);
                        }}
                        required
                      />
                    </div>
                    <div>
                      <label className="text-[10px] text-[var(--text-muted)]">Unit Price (₹)</label>
                      <Input
                        type="number"
                        step="0.01"
                        value={item.unit_price}
                        onChange={(e) => {
                          const updated = [...lineItems];
                          updated[idx].unit_price = Number(e.target.value);
                          setLineItems(updated);
                        }}
                        required
                      />
                    </div>
                    <div>
                      <label className="text-[10px] text-[var(--text-muted)]">GST Rate (%)</label>
                      <Input
                        type="number"
                        value={item.gst_rate}
                        onChange={(e) => {
                          const updated = [...lineItems];
                          updated[idx].gst_rate = Number(e.target.value);
                          setLineItems(updated);
                        }}
                        required
                      />
                    </div>
                    <div className="flex justify-end pt-3">
                      {lineItems.length > 1 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveItem(idx)}
                          className="text-[var(--danger)] hover:opacity-80 p-1"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-2 pt-4">
              <Button type="button" variant="secondary" onClick={() => setIsCreateOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" isLoading={createMutation.isPending}>
                Create Draft Invoice
              </Button>
            </div>
          </form>
        </ModalContent>
      </Modal>
    </div>
  );
}
