# GSTIN Validator & Taxpayer Verification Module Documentation

## Executive Overview
The **GSTIN Validator** module in the Smart GST System provides robust, multi-layered verification for 15-character Indian Goods and Services Tax Identification Numbers (GSTINs). It distinguishes mathematical and statutory format validity from official taxpayer registration status, enforcing a strict **No False Claim Policy**.

---

## Key Features

1. **Format & Structural Validation**:
   - Checks strict 15-character length and alphanumeric constraints.
   - Validates state code against official Indian State/UT codes (`01`-`38`, `97`).
   - Validates embedded 10-character PAN structure (`[A-Z]{5}[0-9]{4}[A-Z]{1}`).
   - Validates entity registration number (13th char) and default letter `Z` (14th char).

2. **Modulus 36 Checksum Verification**:
   - Implements official statutory Modulus 36 Luhn-like algorithm for the 15th checksum character.

3. **Multi-Provider Architecture**:
   - `LocalFormatProvider`: Performs local mathematical, state, and PAN checks.
   - `ExternalGSTProvider`: Pluggable live connection to official GST Portal / authorized GSP APIs.
   - `MockGSTProvider`: Isolated testing fixture provider containing explicit `DEMO DATA` records for active, cancelled, suspended, and non-existent GSTINs.

4. **Privacy & Masking**:
   - Provides configurable GSTIN masking (`29ABCDE****F1ZW`) for privacy compliance.

5. **Audit Logging & Caching**:
   - Logs every verification request with latency, provider name, format results, and status.
   - Caches verification results with configurable TTL (`GSTIN_VERIFICATION_CACHE_TTL`).
