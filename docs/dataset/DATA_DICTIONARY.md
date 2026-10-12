# DATA_DICTIONARY.md — HSN & GST Dataset Data Dictionary

**Project**: Smart GST Verification and Manufacturing Sales Automation System  
**Document Identifier**: DD-GST-2026-V2.4  
**Date**: October 8, 2026  
**Status**: Official CBIC Tax Data Specification  

---

## 1. Field Definitions & Metadata

Every record in the GST/HSN Dataset adheres to the following 25 normalized schema fields:

| Field Name | Type | Description | Example | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `product_name` | String | Common commercial/trade name of product | "Leather Jacket with Zip" | Required |
| `product_description` | Text | Detailed natural language description | "Genuine men's leather jacket with brass zipper" | Required |
| `hsn_code` | String | Official Harmonized System code | "42031010" | Format: `^\d{2,8}$` |
| `hsn_level` | String | Taxonomy level (`CHAPTER`, `HEADING`, `SUBHEADING`, `TARIFF`) | "TARIFF" | Enum |
| `chapter` | String | 2-digit Chapter code | "42" | Format: `^\d{2}$` |
| `heading` | String | 4-digit Heading code | "4203" | Format: `^\d{4}$` |
| `subheading` | String | 6-digit Subheading code | "420310" | Format: `^\d{6}$` |
| `technical_description` | Text | Official WCO/CBIC tariff schedule description | "Articles of apparel of leather or composition leather" | Required |
| `trade_description` | Text | Industry trade terminology | "Leather garments, jackets, coats" | Optional |
| `material` | String | Dominant constituent material | "Leather / Composition Leather" | Required |
| `category` | String | Industry sector category | "Apparel & Leather Goods" | Required |
| `gst_rate` | Float | Total GST percentage rate | 18.0 | Non-negative |
| `cgst_rate` | Float | Central GST percentage | 9.0 | Rate / 2 (Intra) |
| `sgst_rate` | Float | State GST percentage | 9.0 | Rate / 2 (Intra) |
| `igst_rate` | Float | Integrated GST percentage | 18.0 | Equals `gst_rate` |
| `cess_rate` | Float | Compensation Cess percentage | 0.0 | Non-negative |
| `conditions` | Text | Specific exemption or conditional tax rules | "Includes composite items with zippers" | Optional |
| `source_document` | String | Official CBIC Notification or Circular name | "Notification No. 1/2017-Central Tax (Rate)" | Required |
| `source_url` | String | Goverment PDF/Web source URL | "https://cbic-gst.gov.in" | Valid URL |
| `notification_number` | String | Official Notification Serial Identifier | "NOTIF-1-2017-CT" | Required |
| `effective_from` | Date | Effective start date of rule | "2017-07-01" | ISO Date YYYY-MM-DD |
| `effective_to` | Date / Null | Expiry date of rule (or Null if active) | Null | ISO Date YYYY-MM-DD |
| `retrieved_at` | Timestamp | Retrieval timestamp | "2026-10-08T00:00:00Z" | ISO 8601 |
| `source_type` | String | Data provenance classification | "AUTHORITATIVE_CBIC" | Enum |
| `validation_status` | String | Verification audit state | "VALIDATED" | Enum |
