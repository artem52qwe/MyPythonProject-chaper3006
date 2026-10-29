"""Configurable CSV report for finite station measurements."""
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import median


def read_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["station", "temperature"]:
            raise ValueError("Columns must be station,temperature")
        rows = []
        for row in reader:
            value = float(row["temperature"])
            if not row["station"] or not math.isfinite(value):
                raise ValueError("Station and finite temperature required")
            rows.append((row["station"], value))
    return rows


def analyze(rows, minimum, descending=False):
    if not math.isfinite(minimum):
        raise ValueError("Minimum must be finite")
    chosen = sorted((r for r in rows if r[1] >= minimum),
                    key=lambda r: (r[1], r[0]), reverse=descending)
    return {"rows": chosen, "count": len(chosen),
            "median": median([r[1] for r in chosen]) if chosen else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--minimum", type=float, default=0)
    parser.add_argument("--descending", action="store_true")
    parser.add_argument("--output", type=Path,
                        default=Path("report.json"))
    args = parser.parse_args()
    try:
        result = analyze(read_rows(args.input), args.minimum, args.descending)
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
        args.output.write_text(rendered, encoding="utf-8")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
