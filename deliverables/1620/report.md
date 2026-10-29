# Контролируемая обработка ошибок 1620

Макаров Артем Александрович · 3427А

Несколько независимых try/except позволяют показать все исключения в одном запуске. finally выполняется и при ошибке; ресурсы временного каталога освобождает контекстный менеджер. Ошибки не скрываются общим except Exception. safe_ratio показывает предварительную проверку в обычном пути. Запуск: python exceptions_demo.py.

## exceptions_demo.py
```python
"""Demonstrate independent exception handlers and guaranteed cleanup."""
from pathlib import Path
import tempfile


def demonstrations():
    """Produce controlled errors without touching any user's files."""
    messages = []
    try:
        try:
            int("not-a-number")
        except ValueError:
            messages.append("ValueError: integer conversion rejected")
        try:
            len(25)
        except TypeError:
            messages.append("TypeError: length requires a collection")
        try:
            ["hammer"][2]
        except IndexError:
            messages.append("IndexError: position outside collection")
        try:
            9 / 0
        except ZeroDivisionError:
            messages.append("ZeroDivisionError: divisor must be nonzero")
        with tempfile.TemporaryDirectory() as directory:
            try:
                Path(directory, "missing.txt").read_text()
            except FileNotFoundError:
                messages.append("FileNotFoundError: input does not exist")
    finally:
        messages.append("Finished: cleanup ran")
    return messages


def safe_ratio(text):
    """Validate before division in the normal application path."""
    denominator = float(text)
    if denominator == 0:
        raise ValueError("Denominator must not be zero")
    return 9 / denominator


if __name__ == "__main__":
    print("\n".join(demonstrations()))
```

## Проверка
```text
ValueError: integer conversion rejected
TypeError: length requires a collection
IndexError: position outside collection
ZeroDivisionError: divisor must be nonzero
FileNotFoundError: input does not exist
Finished: cleanup ran
Messages and valid calculation: PASS

flake8: 0 замечаний.
```
