"""Read and validate finite measurement values."""
import csv
import math
from pathlib import Path


def read_values(path):
    """Read the value column of a UTF-8 CSV file."""
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["value"]:
            raise ValueError("Expected one column: value")
        values = [float(row["value"]) for row in reader]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("All values must be finite")
    return values
