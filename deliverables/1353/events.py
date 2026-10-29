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
