"""
Unit tests for PaginationParams and PaginatedResponse.
"""

from smart_gst.common.pagination import PaginatedResponse, PaginationParams


def test_pagination_offset_and_pages():
    params = PaginationParams(page=3, page_size=10)
    assert params.offset == 20

    items = ["item1", "item2"]
    resp = PaginatedResponse.create(items=items, total=25, params=params)

    assert resp.total == 25
    assert resp.page == 3
    assert resp.page_size == 10
    assert resp.total_pages == 3
    assert len(resp.items) == 2


def test_pagination_zero_items():
    params = PaginationParams(page=1, page_size=20)
    resp = PaginatedResponse.create(items=[], total=0, params=params)
    assert resp.total_pages == 1
    assert resp.items == []
