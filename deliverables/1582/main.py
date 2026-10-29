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
