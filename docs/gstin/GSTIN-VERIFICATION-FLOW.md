# GSTIN Verification Flow & Pipeline Architecture

```
User Input (GSTIN)
   │
   ▼
1. Normalize (Trim, Strip Hyphens/Spaces, Uppercase)
   │
   ▼
2. Basic Format Check (15 Alphanumeric Chars)
   │
   ▼
3. Structural Validation (State Code 01-38/97 & PAN Regex)
   │
   ▼
4. Checksum Validation (Modulus 36 Algorithm)
   │
   ▼
5. Cache Lookup (DB Cache Record with TTL) ───[ Cache Hit ]──► Return Cached Result
   │
   ▼ (Cache Miss)
6. Provider Query (LocalFormatProvider / ExternalGSTProvider / MockGSTProvider)
   │
   ▼
7. Status Normalization (ACTIVE / CANCELLED / SUSPENDED / NOT_FOUND / SOURCE_UNAVAILABLE)
   │
   ▼
8. Audit Logging & DB Cache Update
   │
   ▼
Response Generation & UI Render
```
