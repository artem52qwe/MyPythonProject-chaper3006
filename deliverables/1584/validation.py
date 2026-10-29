"""Validate console measurements."""
import math


def parse_values(text):
    """Parse whitespace-separated finite values; reject empty input."""
    values = [float(token) for token in text.split()]
    if not values or not all(math.isfinite(v) for v in values):
        raise ValueError("Enter at least one finite number")
    return values
