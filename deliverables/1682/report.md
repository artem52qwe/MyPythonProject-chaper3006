# Медиана измерений

Макаров Артем Александрович · 3427А

Запуск: `python main.py`. reader.py отвечает за формат и проверку, processor.py — за чистое преобразование и запись, main.py — за координацию через import, параметры и возвращаемое значение. Вход: `input.json`, значения 12, −3, 12, 8, 25. Выход: `output.json`. Пустая последовательность обрабатывается явно. Файлы в UTF-8. Сортировка O(n log n), остальные проходы линейны, кроме вычисления медианы.

## main.py
```python
"""Coordinate file reading, processing and output."""
from pathlib import Path
from reader import read_values
from processor import save_result, transform


def main():
    """Resolve data paths relative to this script."""
    base = Path(__file__).resolve().parent
    try:
        result = transform(read_values(base / "input.json"))
        save_result(base / "output.json", result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Input/output error: {exc}")
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## processor.py
```python
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
```

## reader.py
```python
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
```

## test_app.py
```python
"""Exercise real file boundaries and processing edge cases."""
import tempfile
import unittest
from pathlib import Path
from reader import read_values
from processor import transform, save_result


class MeasurementTests(unittest.TestCase):
    def test_transform(self):
        self.assertEqual(transform([12, -3, 12, 8, 25]), 12)

    def test_empty(self):
        self.assertEqual(transform([]), None)

    def test_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "input.json"
            file.write_text('[true]', encoding="utf-8")
            with self.assertRaises(ValueError):
                read_values(file)
            with self.assertRaises(OSError):
                read_values(Path(directory) / "missing")

    def test_output(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "out.json"
            save_result(file, [3, 7])
            self.assertEqual(file.read_text(), "[3, 7]")


if __name__ == "__main__":
    unittest.main()
```

## Проверка
```text
test_empty (test_app.MeasurementTests.test_empty) ... ok
test_invalid_file (test_app.MeasurementTests.test_invalid_file) ... ok
test_output (test_app.MeasurementTests.test_output) ... ok
test_transform (test_app.MeasurementTests.test_transform) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.017s

OK
12

flake8: 0 замечаний.
```
