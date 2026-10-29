"""Read a validated JSON array."""
import json
import math
from pathlib import Path


def read_values(path):
    """Reject booleans, strings, infinity and non-array input."""
    values = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(values, list):
        raise ValueError("Expected an array")
    if not all(type(v) in (int, float) and math.isfinite(v) for v in values):
        raise ValueError("Expected finite numbers")
    return values
