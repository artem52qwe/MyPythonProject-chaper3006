"""Pure minutes transformation."""


def calculate(values):
    """Return a result for a validated, nonempty input sequence."""
    return [round(v / 60, 3) for v in values]
