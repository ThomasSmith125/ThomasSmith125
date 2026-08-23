import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "assets" / "contrib-heatmap.svg"
PALETTE = ["#25222d", "#3b275d", "#563a85", "#7650ad", "#9b74d5"]


def level(count: int) -> int:
    if count == 0: return 0
    if count == 1: return 1
    if count <= 3: return 2
    if count <= 6: return 3
    return 4


def main() -> None:
    info = json.loads(DATA.read_text(encoding="utf-8"))
    days = info["days"][-371:]
    total = sum(day["count"] for day in days)
    cells = []
    first_sunday = datetime.strptime(days[0]["date"], "%Y-%m-%d").date()
    for day in days:
        parsed = datetime.strptime(day["date"], "%Y-%m-%d")
        week = (parsed.date() - first_sunday).days // 7
        weekday = (parsed.weekday() + 1) % 7
        x, y = 66 + week * 15, 65 + weekday * 15
        cells.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{PALETTE[level(day["count"])]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    legend = "".join(f'<rect x="{770 + i * 16}" y="182" width="11" height="11" rx="2" fill="{color}"/>' for i, color in enumerate(PALETTE))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="210" viewBox="0 0 900 210" role="img" aria-label="{total} GitHub contributions in the last year">
  <defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#2b2437" stroke-width=".55"/></pattern></defs>
  <path d="M16 2H868L898 32V178L868 208H16L2 194V16Z" fill="#111018" stroke="#5b4a75" stroke-width="1.4"/>
  <path d="M16 11H862L889 38M889 172L862 199H16M11 194V16" fill="none" stroke="#7b61a8" stroke-width="1" opacity=".8"/>
  <rect x="16" y="50" width="868" height="118" fill="url(#grid)" opacity=".42"/>
  <path d="M24 52h82l10 10h96M876 52h-72l-10 10h-88M24 168h90M786 168h90" fill="none" stroke="#a58ad6" stroke-width="1.1"/>
  <text x="25" y="32" fill="#b79ae6" style="font: 10px Consolas, monospace; letter-spacing: 1px">ACTIVITY // 53W</text>
  <text x="875" y="32" text-anchor="end" fill="#a399b4" style="font: 10px Consolas, monospace; letter-spacing: 1px">LIVE DATA</text>
  <text x="25" y="78" fill="#a399b4" style="font: 10px Consolas, monospace">SUN</text><text x="25" y="108" fill="#a399b4" style="font: 10px Consolas, monospace">TUE</text><text x="25" y="138" fill="#a399b4" style="font: 10px Consolas, monospace">THU</text>
  {''.join(cells)}
  <text x="24" y="190" fill="#e9e5f2" style="font: 600 13px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">{total:,} contributions / last 12 months</text>
  <text x="635" y="190" fill="#a399b4" style="font: 10px Consolas, monospace">LOW</text>{legend}<text x="857" y="190" fill="#a399b4" style="font: 10px Consolas, monospace">HIGH</text>
</svg>''', encoding="utf-8")


if __name__ == "__main__":
    main()
