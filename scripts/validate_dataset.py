#!/usr/bin/env python3
"""
Automated GST & HSN Dataset Validation Engine.

Performs rigorous structural, format, tax math, provenance, and date conflict checks
against GST/HSN dataset records in accordance with docs/dataset/DATA_VALIDATION_RULES.md.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple

# Schema required keys (25 fields)
REQUIRED_FIELDS = [
    "product_name",
    "product_description",
    "hsn_code",
    "hsn_level",
    "chapter",
    "heading",
    "subheading",
    "technical_description",
    "trade_description",
    "material",
    "category",
    "gst_rate",
    "cgst_rate",
    "sgst_rate",
    "igst_rate",
    "cess_rate",
    "conditions",
    "source_document",
    "source_url",
    "notification_number",
    "effective_from",
    "effective_to",
    "retrieved_at",
    "source_type",
    "validation_status",
]

VALID_HSN_LEVELS = {"2-digit", "4-digit", "6-digit", "8-digit"}
VALID_SOURCE_TYPES = {"AUTHORITATIVE_CBIC", "AUTHORITATIVE_STATE", "DEMO_SAMPLE"}
VALID_STATUSES = {"VERIFIED_AUTHORITATIVE", "PROVISIONAL", "DEPRECATED"}


class DatasetValidator:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.records: List[Dict[str, Any]] = []

    def load(self) -> bool:
        if not self.file_path.exists():
            self.errors.append({"rule": "FILE_EXISTS", "message": f"File not found: {self.file_path}"})
            return False

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.records = json.load(f)
            if not isinstance(self.records, list):
                self.errors.append({"rule": "JSON_FORMAT", "message": "Root dataset structure must be a JSON list."})
                return False
            return True
        except Exception as e:
            self.errors.append({"rule": "JSON_PARSING", "message": f"Invalid JSON syntax: {str(e)}"})
            return False

    def validate(self) -> Tuple[int, int]:
        if not self.records:
            return len(self.errors), len(self.warnings)

        seen_hsn_codes = set()
        seen_source_records = set()

        for idx, rec in enumerate(self.records):
            record_id = f"Record #{idx + 1} ({rec.get('product_name', 'Unnamed')})"

            # Rule 0: Schema Completeness
            missing = [f for f in REQUIRED_FIELDS if f not in rec]
            if missing:
                self.errors.append({
                    "rule": "MISSING_FIELDS",
                    "record": record_id,
                    "message": f"Missing required fields: {missing}"
                })

            # Rule 1: HSN Format & Hierarchy
            hsn = rec.get("hsn_code")
            level = rec.get("hsn_level")
            chapter = rec.get("chapter")
            heading = rec.get("heading")
            subheading = rec.get("subheading")

            if not isinstance(hsn, str) or not re.match(r"^\d{2}(\d{2})?(\d{2})?(\d{2})?$", str(hsn)):
                self.errors.append({
                    "rule": "INVALID_HSN_FORMAT",
                    "record": record_id,
                    "message": f"HSN code '{hsn}' must be a string of 2, 4, 6, or 8 digits."
                })
            else:
                hsn_len = len(str(hsn))
                expected_level = f"{hsn_len}-digit"
                if level != expected_level:
                    self.errors.append({
                        "rule": "HSN_LEVEL_MISMATCH",
                        "record": record_id,
                        "message": f"HSN '{hsn}' length ({hsn_len}) does not match level '{level}'."
                    })
                
                # Check hierarchy prefixes
                if chapter != str(hsn)[:2]:
                    self.errors.append({
                        "rule": "HSN_HIERARCHY_MISMATCH",
                        "record": record_id,
                        "message": f"Chapter '{chapter}' does not match HSN prefix '{str(hsn)[:2]}'."
                    })
                if hsn_len >= 4 and heading != str(hsn)[:4]:
                    self.errors.append({
                        "rule": "HSN_HIERARCHY_MISMATCH",
                        "record": record_id,
                        "message": f"Heading '{heading}' does not match HSN prefix '{str(hsn)[:4]}'."
                    })
                if hsn_len >= 6 and subheading != str(hsn)[:6]:
                    self.errors.append({
                        "rule": "HSN_HIERARCHY_MISMATCH",
                        "record": record_id,
                        "message": f"Subheading '{subheading}' does not match HSN prefix '{str(hsn)[:6]}'."
                    })

            # Rule 2: Duplicate HSN Detection
            if hsn in seen_hsn_codes:
                self.warnings.append({
                    "rule": "DUPLICATE_HSN",
                    "record": record_id,
                    "message": f"HSN code '{hsn}' appears multiple times in dataset."
                })
            else:
                seen_hsn_codes.add(hsn)

            # Rule 3: Description Completeness
            p_desc = rec.get("product_description", "")
            t_desc = rec.get("technical_description", "")
            if not p_desc or len(str(p_desc).strip()) < 10:
                self.errors.append({
                    "rule": "MISSING_DESCRIPTION",
                    "record": record_id,
                    "message": "product_description must be at least 10 characters."
                })
            if not t_desc or len(str(t_desc).strip()) < 5:
                self.errors.append({
                    "rule": "MISSING_DESCRIPTION",
                    "record": record_id,
                    "message": "technical_description is missing or too short."
                })

            # Rule 4: Tax Math Rate Consistency
            gst = rec.get("gst_rate")
            cgst = rec.get("cgst_rate")
            sgst = rec.get("sgst_rate")
            igst = rec.get("igst_rate")

            if None in (gst, cgst, sgst, igst):
                self.errors.append({
                    "rule": "NULL_TAX_RATES",
                    "record": record_id,
                    "message": "Tax rates (gst_rate, cgst_rate, sgst_rate, igst_rate) cannot be null."
                })
            else:
                if round(cgst + sgst, 4) != round(gst, 4):
                    self.errors.append({
                        "rule": "INCONSISTENT_TAX_RATES",
                        "record": record_id,
                        "message": f"CGST ({cgst}) + SGST ({sgst}) = {cgst + sgst}, which does not equal GST ({gst})."
                    })
                if round(igst, 4) != round(gst, 4):
                    self.errors.append({
                        "rule": "INCONSISTENT_TAX_RATES",
                        "record": record_id,
                        "message": f"IGST ({igst}) does not equal GST ({gst})."
                    })

            # Rule 5: Provenance & Source Audit
            src_doc = rec.get("source_document")
            src_url = rec.get("source_url")
            src_type = rec.get("source_type")
            status = rec.get("validation_status")

            if not src_doc or not src_url:
                self.errors.append({
                    "rule": "MISSING_SOURCE",
                    "record": record_id,
                    "message": "source_document and source_url are required."
                })
            if src_type not in VALID_SOURCE_TYPES:
                self.errors.append({
                    "rule": "INVALID_SOURCE_TYPE",
                    "record": record_id,
                    "message": f"Invalid source_type '{src_type}'. Must be one of {VALID_SOURCE_TYPES}."
                })
            if status not in VALID_STATUSES:
                self.errors.append({
                    "rule": "INVALID_VALIDATION_STATUS",
                    "record": record_id,
                    "message": f"Invalid validation_status '{status}'. Must be one of {VALID_STATUSES}."
                })

            # Rule 6: Duplicate Source Record Check
            p_name = rec.get("product_name")
            n_num = rec.get("notification_number")
            source_key = (p_name, n_num)
            if source_key in seen_source_records:
                self.errors.append({
                    "rule": "DUPLICATE_SOURCE_RECORD",
                    "record": record_id,
                    "message": f"Duplicate record for product '{p_name}' under notification '{n_num}'."
                })
            else:
                seen_source_records.add(source_key)

            # Rule 7: Date Conflicts
            eff_from = rec.get("effective_from")
            eff_to = rec.get("effective_to")
            if eff_from:
                try:
                    dt_from = datetime.strptime(eff_from, "%Y-%m-%d")
                    if eff_to:
                        dt_to = datetime.strptime(eff_to, "%Y-%m-%d")
                        if dt_from > dt_to:
                            self.errors.append({
                                "rule": "DATE_CONFLICT",
                                "record": record_id,
                                "message": f"effective_from ({eff_from}) is after effective_to ({eff_to})."
                            })
                except ValueError as ve:
                    self.errors.append({
                        "rule": "INVALID_DATE_FORMAT",
                        "record": record_id,
                        "message": f"Date parsing error: {ve}"
                    })

        return len(self.errors), len(self.warnings)


def main():
    target_files = [
        "data/processed/hsn_master_normalized.json",
        "data/samples/sample_test_products.json"
    ]

    total_errors = 0
    total_warnings = 0

    print("==========================================================")
    print("      SMART GST DATASET INTEGRITY VALIDATION RUNNER       ")
    print("==========================================================")

    for file_path in target_files:
        print(f"\n[+] Validating file: {file_path}")
        validator = DatasetValidator(file_path)
        if not validator.load():
            print(f"  [-] Failed to load {file_path}")
            for err in validator.errors:
                print(f"      ERROR [{err['rule']}]: {err['message']}")
            total_errors += len(validator.errors)
            continue

        num_errors, num_warnings = validator.validate()
        total_errors += num_errors
        total_warnings += num_warnings

        print(f"  [*] Total records inspected: {len(validator.records)}")
        print(f"  [*] Errors found: {num_errors}")
        print(f"  [*] Warnings found: {num_warnings}")

        if validator.errors:
            print("  [-] ERRORS:")
            for err in validator.errors:
                rec_str = f" [{err['record']}]" if "record" in err else ""
                print(f"      - {err['rule']}{rec_str}: {err['message']}")

        if validator.warnings:
            print("  [!] WARNINGS:")
            for warn in validator.warnings:
                rec_str = f" [{warn['record']}]" if "record" in warn else ""
                print(f"      - {warn['rule']}{rec_str}: {warn['message']}")

        if num_errors == 0:
            print("  [✓] FILE PASSED VALIDATION")

    print("\n----------------------------------------------------------")
    print(f"SUMMARY: Total Errors = {total_errors}, Total Warnings = {total_warnings}")
    print("----------------------------------------------------------")

    if total_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
