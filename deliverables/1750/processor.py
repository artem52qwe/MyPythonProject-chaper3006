"""Transform measurements without modifying the input."""
import json
from pathlib import Path


def transform(values):
    """Apply the operation selected for this exercise."""
    return sorted(values, reverse=True)


def save_result(path, result):
    """Write JSON with a temporary file and atomic replacement."""
    target = Path(path)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(
        result, ensure_ascii=False), encoding="utf-8")
    temporary.replace(target)
