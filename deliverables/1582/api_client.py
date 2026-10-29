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
