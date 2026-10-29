# Рефакторинг суммы: сокращение ручного цикла

Макаров Артем Александрович · 3427А

Исходник — функция calculate_sum из примера на странице. На целых числах она корректна; ошибки не выдумываются. Замена на sum уменьшает объём управляющего кода и использует встроенную операцию. Обе версии O(n), память O(1) сверх входа. Измерение ниже относится только к локальному набору и не гарантирует такое ускорение для всех типов. Контракт ограничен целыми числами: для float различия порядка округления требуют отдельного анализа.

## after.py
```python
"""Sum integer sensor counts using a built-in reduction."""


def calculate_sum(numbers):
    """Preserve the original integer-input contract, including empty input."""
    return sum(numbers)
```

## before.py
```python
def calculate_sum(numbers):
    result = 0
    for num in numbers:
        result += num
    return result
```

## Проверка
```text
[] expected 0 actual 0
[2, 4, 8] expected 14 actual 14
[-9, 4] expected -5 actual -5
[1000000000000000000000000000000, 1000000000000000000000000000000] expected 2000000000000000000000000000000 actual 2000000000000000000000000000000
Median-like minimum of 5 repeats, 100 calls:
before_seconds 0.028611100045964122
after_seconds 0.006012400146573782

flake8: 0 замечаний.
```
