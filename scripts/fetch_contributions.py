import json
import re
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "ThomasSmith125"
OUT = ROOT / "data" / "contributions.json"


def main() -> None:
    request = Request(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "ThomasSmith125-profile-readme"},
    )
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    days = []
    # GitHub places each accessible tooltip immediately after its calendar cell.
    for cell, tooltip in re.findall(r"(<td[^>]*ContributionCalendar-day[^>]*></td>)\s*<tool-tip[^>]*>([^<]*)</tool-tip>", html):
        date_match = re.search(r'data-date="([^"]+)"', cell)
        if not date_match:
            continue
        match = re.search(r"(\d+) contribution", tooltip)
        days.append({"date": date_match.group(1), "count": int(match.group(1)) if match else 0})
    if not days:
        raise RuntimeError("GitHub returned no contribution calendar days.")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"username": USERNAME, "updated": date.today().isoformat(), "days": days}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
