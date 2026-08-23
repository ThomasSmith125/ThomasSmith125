from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "info-card.svg"

ROWS = [
    ("name", "Thomas Smith"),
    ("role", "Student & Entrepreneur"),
    ("university", "Université Paris-Saclay · UVSQ"),
    ("location", "Paris, France"),
    ("", ""),
    ("education", "BSc Mathematics & Physics — in progress"),
    ("interests", "Artificial Intelligence · Web Development"),
    ("", "Computer Science · Cybersecurity"),
]


def row_svg(index: int, key: str, value: str) -> str:
    y = 128 + index * 27
    if not key and not value:
        return ""
    label = f'<tspan fill="#b79ae6">{escape(key).upper().ljust(12)}</tspan>  ' if key else '<tspan fill="#b79ae6">//</tspan>          '
    return f'''<g>
      <text x="34" y="{y}" class="line">{label}<tspan fill="#e9e5f2">{escape(value)}</tspan></text>
    </g>'''


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    rows = "\n".join(row_svg(i, key, value) for i, (key, value) in enumerate(ROWS))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="400" viewBox="0 0 500 400" role="img" aria-label="Thomas Smith profile information">
  <style>
    .line {{ font: 13px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
    .title {{ font: 700 14px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; letter-spacing: 1px; }}
    .micro {{ font: 10px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; letter-spacing: 1px; }}
  </style>
  <defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M 18 0 L 0 0 0 18" fill="none" stroke="#2b2437" stroke-width=".6" opacity=".55"/></pattern></defs>
  <path d="M16 2H468L498 32V368L468 398H16L2 384V16Z" fill="#111018" stroke="#5b4a75" stroke-width="1.4" />
  <path d="M16 11H462L489 38M489 362L462 389H16M11 384V16" fill="none" stroke="#7b61a8" stroke-width="1" opacity=".75" />
  <rect x="15" y="55" width="470" height="326" fill="url(#grid)" opacity=".58" />
  <path d="M22 86H478M22 336H478" stroke="#44375a" stroke-width="1" />
  <path d="M22 86h88l10 10h91M478 86h-55l-10 10h-78M22 336h72l10-10h100M478 336h-72l-10-10h-90" fill="none" stroke="#a58ad6" stroke-width="1.2" />
  <text x="24" y="32" fill="#b79ae6" class="micro">THS // PROFILE_01</text>
  <text x="476" y="32" text-anchor="end" fill="#a399b4" class="micro">UVSQ · PARIS</text>
  <text x="25" y="73" fill="#e9e5f2" class="title">IDENTITY / DATA CARD</text>
  <text x="475" y="73" text-anchor="end" fill="#b79ae6" class="micro">ONLINE</text>
  {rows}
  <rect x="24" y="350" width="452" height="29" fill="#1b1724" stroke="#44375a" />
  <circle cx="43" cy="365" r="5" fill="#9b7bd1"/><circle cx="43" cy="365" r="2" fill="#efe9ff"/>
  <text x="58" y="369" fill="#c5bbd4" class="micro">STATUS: BUILDING / LEARNING / EXPLORING</text>
  <path d="M24 378h78M398 378h78" stroke="#b79ae6" stroke-width="2"/>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
