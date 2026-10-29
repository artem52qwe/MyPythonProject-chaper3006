"""Console input -> validation -> transformation -> JSON."""
import json
from pathlib import Path
from calculation import calculate
from validation import parse_values


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
