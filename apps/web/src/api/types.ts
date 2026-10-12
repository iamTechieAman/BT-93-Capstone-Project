/**
 * TypeScript Strict API Type Definitions.
 * Aligned with packages/contracts/openapi.json and FastAPI backend.
 */

export interface ApiErrorPayload {
  code: string;
  message: string;
  request_id?: string;
  details?: Record<string, unknown>;
}

// 1. Classification
export interface SignalBreakdown {
  keyword_match_score: number;
  vector_similarity_score: number;
  statutory_rule_match: boolean;
  agreeing_sources_count: number;
  missing_conditions_penalty: number;
  computed_raw_confidence: number;
}

export interface SourceEvidence {
  document: string;
  notification: string;
  notification_date: string;
  schedule: string;
  serial_no: string;
  effective_from: string;
  retrieved_at: string;
  url?: string;
}

export interface CandidateAlternative {
  hsn_code: string;
  description: string;
  score: number;
}

export interface ClassificationRequest {
  product_description: string;
  invoice_date?: string;
  context?: string;
  attributes?: Record<string, string | number | boolean>;
}

export interface ClassificationResult {
  product_description: string;
  suggested_hsn: string;
  hsn_description: string;
  chapter: string;
  heading: string;
  gst_rate: number;
  effective_rate_text: string;
  match_quality: 'Strong' | 'Moderate' | 'Weak';
  status: 'Matched' | 'Needs review';
  confidence: number;
  signals: SignalBreakdown;
  sources: SourceEvidence[];
  alternatives_considered: CandidateAlternative[];
  reasoning_summary: string;
  evaluation_factors: string[];
}

// 2. GSTIN
export interface StepStatus {
  id: string;
  name: string;
  state: 'PASSED' | 'FAILED' | 'SKIPPED';
  detail?: string;
}

export interface GstinVerifyResponse {
  gstin: string;
  masked_gstin: string;
  format_valid: boolean;
  structural_valid: boolean;
  checksum_valid: boolean;
  registration_verified: boolean;
  taxpayer_status: string;
  headline: string;
  verification_status: 'PASSED' | 'FAILED';
  legal_name?: string;
  trade_name?: string;
  state_code?: string;
  state_name?: string;
  pan?: string;
  constitution?: string;
  jurisdiction?: string;
  address?: string;
  provider_name?: string;
  fetched_at?: string;
  validation_failures: string[];
  steps: StepStatus[];
  warnings: string[];
  error_code?: string;
  latency_ms: number;
}

// 3. Invoices
export interface InvoiceLineItemInput {
  product_name: string;
  hsn_code: string;
  quantity: number;
  unit_price: number;
  gst_rate: number;
  cess_rate?: number;
}

export interface InvoiceCreatePayload {
  invoice_number: string;
  invoice_date: string;
  supplier_gstin: string;
  buyer_gstin: string;
  place_of_supply?: string;
  line_items: InvoiceLineItemInput[];
  notes?: string;
}

export interface InvoiceItemResponse {
  id: string;
  product_name: string;
  hsn_code: string;
  quantity: number;
  unit_price: number;
  taxable_value: number;
  gst_rate: number;
  cgst_amount: number;
  sgst_amount: number;
  igst_amount: number;
  cess_amount: number;
  item_total: number;
}

export interface InvoiceResponse {
  id: string;
  invoice_number: string;
  invoice_date: string;
  supplier_gstin: string;
  buyer_gstin: string;
  place_of_supply: string;
  status: 'DRAFT' | 'FINALIZED' | 'CANCELLED';
  subtotal: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  cess_total: number;
  grand_total: number;
  notes?: string;
  created_at?: string;
  pdf_url?: string;
  pdf_sha256?: string;
  items: InvoiceItemResponse[];
}

// 4. Rate Schedule & Hierarchy
export interface TariffRateRule {
  id: string;
  hsn_code: string;
  description: string;
  rate: number;
  notification_no: string;
  notification_date: string;
  schedule: string;
  serial_no: string;
  effective_from: string;
  source_url?: string;
}

export interface TariffHierarchyNode {
  code: string;
  level: 'chapter' | 'heading' | 'sub_heading' | 'tariff_item';
  title: string;
  parent_id?: string;
  children?: TariffHierarchyNode[];
}

// 5. Activity Log
export interface AuditLogItem {
  id: string;
  timestamp: string;
  action: string;
  user_email: string;
  resource_id?: string;
  details?: Record<string, unknown>;
  ip_address?: string;
}

// 6. Data Sync / Ingestion
export interface SyncStatusResponse {
  status: 'IDLE' | 'SYNCING' | 'COMPLETED' | 'ERROR';
  last_synced_at?: string;
  records_processed: number;
  approved_records: number;
  pending_review: number;
  current_source?: string;
}
