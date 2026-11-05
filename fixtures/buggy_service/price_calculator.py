"""Price calculator for checkout-service.

This file contains a DELIBERATE BUG for the hackathon demo:
the discount rounding uses ROUND_DOWN instead of ROUND_HALF_UP,
causing 1-cent mismatches on certain discount combinations.
"""

from decimal import Decimal, ROUND_DOWN  # BUG: should be ROUND_HALF_UP


def calculate_total(items: list[dict], discount_pct: float = 0.0) -> Decimal:
    """Calculate the order total after applying a percentage discount.

    Args:
        items: list of dicts with 'price' (float) and 'quantity' (int).
        discount_pct: discount percentage (0.0 to 100.0).

    Returns:
        Total after discount, rounded to 2 decimal places.
    """
    subtotal = Decimal("0.00")
    for item in items:
        price = Decimal(str(item["price"]))
        qty = item.get("quantity", 1)
        subtotal += price * qty

    if discount_pct > 0:
        discount = subtotal * Decimal(str(discount_pct)) / Decimal("100")
        # BUG: ROUND_DOWN causes 1-cent underpayment on certain totals
        discount = discount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        subtotal -= discount

    return subtotal.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

