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
    y = 82 + index * 36
    delay = 0.35 + index * 0.14
    if not key and not value:
        return ""
    label = f'<tspan fill="#55d68a">{escape(key)}</tspan>  ' if key else '<tspan fill="#55d68a">&gt;</tspan>          '
    return f'''<g opacity="0" transform="translate(-8 0)">
      <text x="34" y="{y}" class="line">{label}<tspan fill="#e6edf3">{escape(value)}</tspan></text>
      <animate attributeName="opacity" values="0;0;1" keyTimes="0;{delay};{delay + 0.12}" dur="2s" fill="freeze" />
      <animateTransform attributeName="transform" type="translate" values="-8 0;-8 0;0 0" keyTimes="0;{delay};{delay + 0.12}" dur="2s" fill="freeze" />
    </g>'''


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    rows = "\n".join(row_svg(i, key, value) for i, (key, value) in enumerate(ROWS))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="390" viewBox="0 0 490 390" role="img" aria-label="Thomas Smith profile information">
  <style>
    .line {{ font: 15px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
    .title {{ font: 600 15px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
  </style>
  <rect width="490" height="390" rx="12" fill="#15191d" stroke="#30363d" />
  <rect width="490" height="43" rx="12" fill="#20252b" />
  <rect y="31" width="490" height="12" fill="#20252b" />
  <circle cx="25" cy="22" r="6" fill="#ff5f57" /><circle cx="45" cy="22" r="6" fill="#febc2e" /><circle cx="65" cy="22" r="6" fill="#28c840" />
  <text x="245" y="27" text-anchor="middle" fill="#b7c0c9" class="title">thomas@github:~</text>
  {rows}
  <g opacity="0"><text x="34" y="366" class="line" fill="#55d68a">$ <tspan fill="#8b949e">_</tspan></text><animate attributeName="opacity" values="0;0;1" keyTimes="0;.93;1" dur="2s" fill="freeze" /></g>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
