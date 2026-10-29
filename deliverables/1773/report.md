# PEP 8: проверка предоставленного примера

Макаров Артем Александрович · 3427А

Отдельного файла преподавателя нет. Проверен показанный на странице пример, восстановленный с обычными отступами. flake8 не выявил нарушений; добавлена документация функции. Отсутствие ошибки нельзя заменять вымышленным замечанием.

| Номер строки | Строка кода | Результат инспекции |
|---|---|---|
| 4 | def example_function(arg1, arg2): | snake_case, пробел после запятой соблюдены |
| 6 | result = arg1 + arg2 | Отступ 4 пробела, операторы отделены пробелами |
| 7 | return result | Отступ согласован с телом |

Рекомендация: сохранить короткую функцию, добавить понятный контракт и тесты. Источник правил: https://peps.python.org/pep-0008/

## example.py
```python
"""The additive example supplied on the exercise page."""


def example_function(arg1, arg2):
    """Return the sum without changing the supplied contract."""
    result = arg1 + arg2
    return result
```

## Проверка
```text
Positive and zero sum: PASS

flake8: 0 замечаний.
```
