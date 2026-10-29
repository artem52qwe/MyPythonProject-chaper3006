"""Transform measurements without modifying the input."""
import json
from pathlib import Path
from collections import Counter


def transform(values):
    """Apply the operation selected for this exercise."""
    return dict(Counter(values))


def save_result(path, result):
    """Write JSON with a temporary file and atomic replacement."""
    target = Path(path)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(
        result, ensure_ascii=False), encoding="utf-8")
    temporary.replace(target)
