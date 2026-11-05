"""Tests for price_calculator — will FAIL until the rounding bug is fixed."""

from decimal import Decimal

from price_calculator import calculate_total


def test_no_discount():
    items = [{"price": 49.99, "quantity": 3}]
    assert calculate_total(items) == Decimal("149.97")


def test_ten_percent_discount():
    """This test exposes the ROUND_DOWN bug."""
    items = [{"price": 49.99, "quantity": 3}]
    result = calculate_total(items, discount_pct=10.0)
    # Correct: 149.97 * 0.10 = 14.997 -> rounds to 15.00 (HALF_UP)
    # Buggy:   14.997 -> rounds to 14.99 (DOWN) -> total 135.98 vs 134.97
    assert result == Decimal("134.97"), f"Got {result}, expected 134.97"


def test_zero_quantity_ignored():
    items = [{"price": 100.00, "quantity": 0}]
    assert calculate_total(items) == Decimal("0.00")


def test_multiple_items_with_discount():
    items = [
        {"price": 29.99, "quantity": 2},
        {"price": 9.99, "quantity": 1},
    ]
    result = calculate_total(items, discount_pct=15.0)
    # Subtotal: 69.97, 15% discount = 10.4955 -> HALF_UP = 10.50
    # Expected total: 59.47
    assert result == Decimal("59.47"), f"Got {result}, expected 59.47"

