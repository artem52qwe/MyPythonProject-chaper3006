"""Compare retained lists with a closed-form sum; no external services."""
import json
import statistics
import time
import tracemalloc


def before(rounds=80, size=3000):
    retained = []
    total = 0
    for _ in range(rounds):
        values = list(range(size))
        retained.append(values)
        total += sum(value * value for value in values)
    return total


def after(rounds=80, size=3000):
    return rounds * (size - 1) * size * (2 * size - 1) // 6


def measure(function):
    times = []
    peak = 0
    for _ in range(5):
        tracemalloc.start()
        start = time.perf_counter()
        result = function()
        times.append(time.perf_counter() - start)
        peak = max(peak, tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    return {"result": result, "median_seconds": statistics.median(times),
            "peak_bytes": peak}


if __name__ == "__main__":
    for n in (0, 1, 2, 19, 3000):
        assert before(3, n) == after(3, n)
    results = {"before": measure(before), "after": measure(after)}
    assert results["before"]["result"] == results["after"]["result"]
    print(json.dumps(results, indent=2))
