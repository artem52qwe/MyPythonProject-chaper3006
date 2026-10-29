"""Pure span transformation."""


def calculate(values):
    """Return a result for a validated, nonempty input sequence."""
    return max(values) - min(values)
