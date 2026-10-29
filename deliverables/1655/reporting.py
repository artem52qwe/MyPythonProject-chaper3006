"""Render workshop totals without changing arithmetic."""


def format_rubles(kopecks):
    """Format integer money with exactly two decimal places."""
    rubles, remainder = divmod(kopecks, 100)
    return f"{rubles}.{remainder:02d} RUB"
