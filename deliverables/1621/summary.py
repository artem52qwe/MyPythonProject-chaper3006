"""Validate and project API metadata into a small report."""
import math


def summarize(data):
    """Preserve factual counters and calculate a labelled derived metric."""
    if not isinstance(data, dict):
        raise ValueError("Expected an object")
    name = data.get("full_name")
    stars, forks = data.get("stargazers_count"), data.get("forks_count")
    if not isinstance(name, str) or not name:
        raise ValueError("Missing repository name")
    if any(type(x) is not int or x < 0 for x in [stars, forks]):
        raise ValueError("Invalid counters")
    return {"repository": name, "stars": stars, "forks": forks,
            "log10_stars_plus_one": round(math.log10(stars + 1), 4)}
