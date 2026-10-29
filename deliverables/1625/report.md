# Отладка расчёта счёта мастерской

Макаров Артем Александрович · 3427А

На странице 1761 приведён корректный add(5,3), отдельного дефектного исходника нет. Для исследования явно создан учебный faulty-пример: total ошибочно вычисляет среднее и падает на пустом списке. pdb показал prices=[12,8], sum=20, len=2: деление лишнее. Pyflakes нашёл только неиспользуемый import math и не обнаруживает эту бизнес-ошибку. Тесты проверяют контракт суммы; исправление использует Decimal.

| Исходный код | Исправленный код |
|---|---|
| [12,8] → 10.0 | [12,8] → 20.00 |
| [] → ZeroDivisionError | [] → 0.00 |
| Некорректные цены принимаются | TypeError/ValueError |

Исходник с намеренной ошибкой:
```python
"""Deliberately faulty educational price module."""
import math


def total(prices):
    return sum(prices) / len(prices)


def invoice(prices):
    return round(total(prices), 2)


if __name__ == "__main__":
    print(invoice([12, 8]))
```

## prices.py
```python
"""Validated invoice calculation for a workshop."""
from decimal import Decimal


def total(prices):
    """Sum finite nonnegative Decimal prices; empty invoice totals zero."""
    if any(not isinstance(p, Decimal) for p in prices):
        raise TypeError("Decimal prices required")
    if any(not p.is_finite() or p < 0 for p in prices):
        raise ValueError("Finite nonnegative prices required")
    return sum(prices, Decimal(0))


def invoice(prices):
    """Format exact money rather than converting through binary float."""
    return total(prices).quantize(Decimal("0.01"))
```

## test_prices.py
```python
"""Check business totals and rejected values."""
import unittest
from decimal import Decimal
from prices import invoice


class PriceTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(invoice([Decimal(12), Decimal(8)]), Decimal("20.00"))

    def test_empty(self):
        self.assertEqual(invoice([]), Decimal("0.00"))

    def test_fraction(self):
        self.assertEqual(invoice([Decimal("0.1"), Decimal("0.2")]),
                         Decimal("0.30"))

    def test_invalid(self):
        for value in [Decimal(-1), Decimal("NaN"), Decimal("Infinity")]:
            with self.assertRaises(ValueError):
                invoice([value])
        with self.assertRaises(TypeError):
            invoice([1.2])


if __name__ == "__main__":
    unittest.main()
```

## Проверка
```text
broken.py:2:1: 'math' imported but unused
Breakpoint 1 at c:\users\chips\documents\chatgpt\учеба\solutions-chaper3006\1625\broken.py:5
[12, 8]
20
2
test_empty (test_prices.PriceTests.test_empty) ... ok
test_fraction (test_prices.PriceTests.test_fraction) ... ok
test_invalid (test_prices.PriceTests.test_invalid) ... ok
test_total (test_prices.PriceTests.test_total) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK

flake8: 0 замечаний.
```
