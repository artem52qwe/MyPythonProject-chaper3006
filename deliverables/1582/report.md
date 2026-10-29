# Интеграция API: карточка открытого репозитория

Макаров Артем Александрович · 3427А

Использован публичный GitHub REST endpoint GET /repos/{owner}/{repo}: https://docs.github.com/en/rest/repos/repos#get-a-repository. Токен не требуется для публичных данных, возможны лимиты API. api_client отвечает за HTTPS и JSON, summary — за проверку схемы и математику, main — за ввод, вывод и файл. math и pathlib связывают вычисление и сохранение. Показатель log10(stars+1) — учебное преобразование, не оценка качества проекта. Счётчики являются снимком на момент запуска, не константами.

## api_client.py
```python
"""Read public repository metadata from GitHub without credentials."""
import json
import re
from urllib.request import Request, urlopen


def fetch_repository(full_name):
    """Validate owner/repo, restrict destination and limit response size."""
    pattern = r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*"
    if not re.fullmatch(pattern, full_name):
        raise ValueError("Expected owner/repository")
    request = Request("https://api.github.com/repos/" + full_name,
                      headers={"Accept": "application/vnd.github+json",
                               "User-Agent": "student-metadata-example"})
    with urlopen(request, timeout=15) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError("Response exceeds 2 MB")
    return json.loads(data)
```

## main.py
```python
"""Fetch, transform, save and print public repository metadata."""
import json
from pathlib import Path
from urllib.error import URLError
from api_client import fetch_repository
from summary import summarize


def main():
    try:
        name = input("Public owner/repository: ").strip()
        result = summarize(fetch_repository(name))
        Path(__file__).with_name("metadata.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    except (ValueError, OSError, URLError, EOFError) as exc:
        print(f"Unable to create report: {exc}")
        return 1
    for key, value in result.items():
        print(f"{key:25} | {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## summary.py
```python
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
```

## Проверка
```text
Public owner/repository: repository                | python/cpython
stars                     | 77697
forks                     | 37688
log10_stars_plus_one      | 4.8904
Fixture: PASS
Malformed response: PASS
Invalid name: PASS

flake8: 0 замечаний.
```
