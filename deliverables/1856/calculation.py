"""Pure fahrenheit transformation."""


def calculate(values):
    """Return a result for a validated, nonempty input sequence."""
    return [round(v * 9 / 5 + 32, 2) for v in values]
