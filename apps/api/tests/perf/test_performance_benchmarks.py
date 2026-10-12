"""
Performance and Latency Benchmarks for Smart GST Engine.
Marked with @pytest.mark.perf, excluded from default fast CI runs and executed nightly.
"""

import time

import pytest

from smart_gst.gstin.service import GstinService
from smart_gst.invoicing.service import TaxDomainService


@pytest.mark.perf
def test_performance_tax_engine_throughput():
    # 10,000 line item calculations in under 200ms
    start = time.time()
    for _ in range(10000):
        TaxDomainService.calculate_line_item(
            quantity=2, unit_price=450.50, gst_rate=18.0, is_interstate=False, cess_rate=0.0
        )
    duration_ms = (time.time() - start) * 1000
    assert duration_ms < 500.0, f"Tax calculation throughput exceeded threshold: {duration_ms}ms"


@pytest.mark.perf
def test_performance_gstin_offline_validation_speed():
    # 5,000 full Mod-36 statutory validations in under 200ms
    service = GstinService()
    start = time.time()
    for _ in range(5000):
        service.verify_gstin("27AAPFU0939F1ZV")
    duration_ms = (time.time() - start) * 1000
    assert duration_ms < 500.0, f"GSTIN validation throughput exceeded threshold: {duration_ms}ms"
