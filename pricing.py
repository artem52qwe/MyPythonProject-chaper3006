"""Compute workshop material costs in integer kopecks."""


def batch_cost(unit_price,quantity):
    """Reject invalid prices and quantities before multiplying."""
    if type(unit_price) is not int or type(quantity) is not int:
        raise TypeError("Integer arguments required")
    if unit_price < 0 or quantity < 0:
        raise ValueError("Nonnegative arguments required")
    return unit_price*quantity
