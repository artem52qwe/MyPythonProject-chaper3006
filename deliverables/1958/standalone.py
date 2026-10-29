import json
from pathlib import Path
"""Validate console measurements."""
import math


def parse_values(text):
    """Parse whitespace-separated finite values; reject empty input."""
    values = [float(token) for token in text.split()]
    if not values or not all(math.isfinite(v) for v in values):
        raise ValueError("Enter at least one finite number")
    return values


"""Pure minutes transformation."""


def calculate(values):
    """Return a result for a validated, nonempty input sequence."""
    return [round(v / 60, 3) for v in values]


"""Console input -> validation -> transformation -> JSON."""


def main():
    """Report validation and write failures without a traceback."""
    try:
        values = parse_values(input("Values separated by spaces: "))
        result = calculate(values)
        output = Path(__file__).with_name("result.json")
        output.write_text(json.dumps(
            result, allow_nan=False), encoding="utf-8")
    except (ValueError, OSError, EOFError) as exc:
        print(f"Error: {exc}")
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
