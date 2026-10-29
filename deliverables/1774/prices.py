"""Validated invoice calculation for a workshop."""
from decimal import Decimal


def total(prices):
    """Sum finite nonnegative Decimal prices; empty invoice totals zero."""
    if any(not isinstance(p, Decimal) for p in prices):
        raise TypeError("Decimal prices required")
    if any(not p.is_finite() or p < 0 for p in prices):
        raise ValueError("Finite nonnegative prices required")
    return sum(prices, Decimal(0))


def invoice(prices):
    """Format exact money rather than converting through binary float."""
    return total(prices).quantize(Decimal("0.01"))
