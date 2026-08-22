import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "assets" / "contrib-heatmap.svg"
PALETTE = ["#22272e", "#0e4429", "#006d32", "#26a641", "#39d353"]


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
        x, y = 48 + week * 15, 52 + weekday * 15
        cells.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{PALETTE[level(day["count"])]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    legend = "".join(f'<rect x="{735 + i * 16}" y="177" width="11" height="11" rx="2" fill="{color}"/>' for i, color in enumerate(PALETTE))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="220" viewBox="0 0 860 220" role="img" aria-label="{total} GitHub contributions in the last year">
  <rect width="860" height="220" rx="12" fill="#15191d" stroke="#30363d"/>
  <text x="24" y="29" fill="#e6edf3" style="font: 600 14px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">{total:,} contributions in the last year</text>
  <text x="24" y="48" fill="#8b949e" style="font: 12px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Updated daily from GitHub activity</text>
  <text x="24" y="70" fill="#8b949e" style="font: 11px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Sun</text><text x="24" y="100" fill="#8b949e" style="font: 11px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Tue</text><text x="24" y="130" fill="#8b949e" style="font: 11px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Thu</text>
  {''.join(cells)}
  <text x="700" y="187" fill="#8b949e" style="font: 11px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Less</text>{legend}<text x="821" y="187" fill="#8b949e" style="font: 11px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">More</text>
</svg>''', encoding="utf-8")


if __name__ == "__main__":
    main()
