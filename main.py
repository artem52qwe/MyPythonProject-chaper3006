"""Print a formatted workshop estimate."""
from pricing import batch_cost
from reporting import format_rubles


if __name__ == "__main__":
    print(format_rubles(batch_cost(2750, 4)))
