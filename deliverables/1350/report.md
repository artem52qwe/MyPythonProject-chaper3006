# Алгоритм Евклида: структурная программа

Макаров Артем Александрович · 3427А

Выбран алгоритм НОД, поскольку конкретный обязательный алгоритм в условии не задан. Последовательность: проверить типы и взять модули. Ветвление: b=0 завершает обработку. Цикл: заменить пару (a,b) на (b,a%b). Остаток строго уменьшается, поэтому цикл заканчивается. Инвариант: НОД пары сохраняется. Отрицательные числа допустимы, НОД(0,0)=0 — явно выбранное соглашение. Схема и таблица приведены в PDF.

## euclid.py
```python
"""Calculate the greatest common divisor using a structured loop."""


def gcd(a, b):
    """Return a nonnegative GCD; gcd(0, 0) is defined here as 0."""
    if type(a) is not int or type(b) is not int:
        raise TypeError("Integer arguments required")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


if __name__ == "__main__":
    try:
        first, second = map(int, input("Two integers: ").split())
        print(gcd(first, second))
    except ValueError:
        print("Enter exactly two integers")
```

## Проверка
```text
48 18 expected 6 actual 6
-21 14 expected 7 actual 7
0 15 expected 15 actual 15
0 0 expected 0 actual 0
17 13 expected 1 actual 1

flake8: 0 замечаний.
```
