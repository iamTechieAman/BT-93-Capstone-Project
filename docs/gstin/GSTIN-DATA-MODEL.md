# GSTIN Data Model & Domain Specification

## Schema Definitions

### 1. `GSTINVerificationRequest`
```json
{
  "gstin": "29ABCDE1234F1ZW",
  "requested_at": "2026-10-09T03:35:13Z"
}
```

### 2. `TaxpayerDetails`
```json
{
  "legal_name": "Acme Global Solutions Pvt Ltd (DEMO DATA)",
  "trade_name": "Acme Tech",
  "registration_date": "01/07/2017",
  "cancellation_date": null,
  "constitution_of_business": "Private Limited Company",
  "taxpayer_type": "Regular",
  "principal_place_of_business": "124 Innovation Park, Electronic City, Bengaluru, Karnataka - 560100",
  "nature_of_business": ["Manufacturing", "IT Services"],
  "state_jurisdiction": "Ward 4, Zone 1, Bengaluru",
  "center_jurisdiction": "Range 12, Division II, Bengaluru West"
}
```

### 3. `SourceInfo`
```json
{
  "name": "Mock GST Provider (DEMO DATA)",
  "url": "https://services.gst.gov.in/services/searchtp",
  "verified_at": "2026-10-09T03:35:13Z",
  "cache_hit": false
}
```

### 4. `GSTINVerificationResult`
```json
{
  "gstin": "29ABCDE1234F1ZW",
  "masked_gstin": "29ABCDE****F1ZW",
  "format_valid": true,
  "structural_valid": true,
  "checksum_valid": true,
  "registration_verified": true,
  "taxpayer_status": "ACTIVE",
  "taxpayer": { ... },
  "source": { ... },
  "verification_status": "PASSED",
  "warnings": [],
  "error_code": null,
  "latency_ms": 12.5
}
```
