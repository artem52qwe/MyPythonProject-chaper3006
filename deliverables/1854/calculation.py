"""Pure rms transformation."""
import math


def calculate(values):
    """Return a result for a validated, nonempty input sequence."""
    return math.hypot(*values) / math.sqrt(len(values))
