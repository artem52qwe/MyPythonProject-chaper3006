# Консольное преобразование: minutes

Макаров Артем Александрович · 3427А

Отдельные модули валидации и вычисления связывает main.py. span — размах температур; rms — среднеквадратичная величина; fahrenheit — перевод °C в °F; minutes — перевод секунд в минуты. В этой работе используется только операция, указанная в заголовке. Запуск `python main.py`, разделитель — пробел. 1958 дополнительно имеет автономный standalone.py. Некорректный ввод завершает программу с кодом 1 и не записывает новый результат.

## calculation.py
```python
"""Pure minutes transformation."""


def calculate(values):
    """Return a result for a validated, nonempty input sequence."""
    return [round(v / 60, 3) for v in values]
```

## main.py
```python
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
```

## standalone.py
```python
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
```

## validation.py
```python
"""Validate console measurements."""
import math


def parse_values(text):
    """Parse whitespace-separated finite values; reject empty input."""
    values = [float(token) for token in text.split()]
    if not values or not all(math.isfinite(v) for v in values):
        raise ValueError("Enter at least one finite number")
    return values
```

## Проверка
```text
INPUT '3 4'
Values separated by spaces: [0.05, 0.067]
INPUT '-10 0 20'
Values separated by spaces: [-0.167, 0.0, 0.333]
INPUT ''
Values separated by spaces: Error: Enter at least one finite number
INPUT 'NaN'
Values separated by spaces: Error: Enter at least one finite number
INPUT 'hello'
Values separated by spaces: Error: could not convert string to float: 'hello'

flake8: 0 замечаний.
```
