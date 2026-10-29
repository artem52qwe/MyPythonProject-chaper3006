# События консоли: учёт возврата инструментов

Макаров Артем Александрович · 3427А

Событие — строка, введённая пользователем. Цикл диспетчеризации ждёт input, handler возвращает новое состояние и признак завершения. add, reset, show, quit имеют разные обработчики-ветви. Неизвестная команда не меняет счётчик. Вариант консольный, что допускается условием; интерфейс tkinter не требуется.

## events.py
```python
"""A console event dispatcher for a workshop counter."""


def handle(command, count):
    """Process one keyboard event and return state, message and stop flag."""
    if command == "add":
        return count + 1, "One tool returned", False
    if command == "reset":
        return 0, "Counter cleared", False
    if command == "show":
        return count, f"Tools returned: {count}", False
    if command == "quit":
        return count, "Session finished", True
    return count, "Unknown command: add, reset, show or quit", False


def main():
    """Read events until quit or end of input."""
    count = 0
    while True:
        try:
            command = input("> ").strip().lower()
        except EOFError:
            break
        count, message, stop = handle(command, count)
        print(message)
        if stop:
            break


if __name__ == "__main__":
    main()
```

## Проверка
```text
> One tool returned
> One tool returned
> Tools returned: 2
> Counter cleared
> Tools returned: 0
> Unknown command: add, reset, show or quit
> Session finished
Event state assertions: PASS

flake8: 0 замечаний.
```
