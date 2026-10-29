"""Transform measurements without modifying the input."""
import json
from pathlib import Path
import statistics


def transform(values):
    """Apply the operation selected for this exercise."""
    return statistics.median(values) if values else None


def save_result(path, result):
    """Write JSON with a temporary file and atomic replacement."""
    target = Path(path)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(
        result, ensure_ascii=False), encoding="utf-8")
    temporary.replace(target)
