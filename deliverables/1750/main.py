"""Coordinate file reading, processing and output."""
from pathlib import Path
from reader import read_values
from processor import save_result, transform


def main():
    """Resolve data paths relative to this script."""
    base = Path(__file__).resolve().parent
    try:
        result = transform(read_values(base / "input.csv"))
        save_result(base / "output.json", result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Input/output error: {exc}")
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
