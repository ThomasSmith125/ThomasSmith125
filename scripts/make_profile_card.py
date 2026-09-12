import sys
from html import escape
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-card.svg"
RAMP = " .`:-=+*#%@"
COLS, ROWS = 54, 38

PROFILE_ROWS = [
    ("NAME", "Thomas Smith"),
    ("ROLE", "Student & Entrepreneur"),
    ("UNIVERSITY", "Université Paris-Saclay · UVSQ"),
    ("LOCATION", "Paris, France"),
    ("", ""),
    ("EDUCATION", "BSc Mathematics & Physics — in progress"),
    ("INTERESTS", "Artificial Intelligence · Web Development"),
    ("", "Computer Science · Cybersecurity"),
]


def portrait_rows(source: Path) -> str:
    if source.exists():
        image = Image.open(source).convert("L")
        image = ImageOps.autocontrast(image, cutoff=1)
        image = ImageOps.fit(image, (COLS, ROWS), Image.Resampling.LANCZOS, centering=(0.5, 0.42))
        image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))
        image = ImageEnhance.Contrast(image).enhance(1.2)
        ascii_rows = [
            "".join(RAMP[int(image.getpixel((x, y)) / 256 * len(RAMP))] for x in range(COLS))
            for y in range(ROWS)
        ]
    else:
        # Reuse the already-generated portrait when the original local photo is unavailable.
        previous = ElementTree.parse(ROOT / "assets" / "thomas-ascii.svg")
        ascii_rows = [node.text or "" for node in previous.findall("{http://www.w3.org/2000/svg}text") if node.get("class") == "ascii"]
    rows = []
    for y, chars in enumerate(ascii_rows):
        rows.append(f'<text x="42" y="{145 + y * 5}" class="ascii" xml:space="preserve">{escape(chars)}</text>')
    return "".join(rows)


def info_rows() -> str:
    output = []
    for index, (label, value) in enumerate(PROFILE_ROWS):
        if not label and not value:
            continue
        y = 137 + index * 27
        prefix = label.ljust(12) if label else "//          "
        output.append(
            f'<text x="420" y="{y}" class="line"><tspan fill="#b79ae6">{escape(prefix)}</tspan><tspan fill="#e9e5f2">  {escape(value)}</tspan></text>'
        )
    return "".join(output)


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.png"
    OUT.parent.mkdir(exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="400" viewBox="0 0 900 400" role="img" aria-label="Thomas Smith profile card">
  <style>
    .ascii {{ font: 7px/5px 'SFMono-Regular', Consolas, monospace; letter-spacing: -.25px; fill: #c4adef; }}
    .line {{ font: 13px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
    .title {{ font: 700 16px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; letter-spacing: 1px; }}
    .micro {{ font: 10px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; letter-spacing: 1px; }}
  </style>
  <defs>
    <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#2b2437" stroke-width=".6"/></pattern>
    <pattern id="fineGrid" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0H0V12" fill="none" stroke="#2b2437" stroke-width=".5"/></pattern>
  </defs>
  <path d="M16 2H868L898 32V368L868 398H16L2 384V16Z" fill="#111018" stroke="#5b4a75" stroke-width="1.4"/>
  <path d="M16 11H862L889 38M889 362L862 389H16M11 384V16" fill="none" stroke="#7b61a8" stroke-width="1" opacity=".8"/>
  <rect x="16" y="55" width="868" height="326" fill="url(#grid)" opacity=".52"/>
  <path d="M25 86h98l10 10h135M875 86h-96l-10 10h-117M25 353h108M745 353h130" fill="none" stroke="#a58ad6" stroke-width="1.15"/>
  <text x="25" y="32" fill="#b79ae6" class="micro">THS // PROFILE INTERFACE</text>
  <text x="875" y="32" text-anchor="end" fill="#a399b4" class="micro">PARIS · FRANCE</text>
  <text x="25" y="74" fill="#e9e5f2" class="title">THOMAS SMITH</text>
  <text x="875" y="74" text-anchor="end" fill="#b79ae6" class="micro">PROFILE / 01</text>
  <rect x="25" y="110" width="345" height="225" fill="#151221" stroke="#44375a"/>
  <rect x="34" y="119" width="327" height="207" fill="url(#fineGrid)" opacity=".42"/>
  <path d="M25 110h62l9 9h64M370 110h-46l-9 9h-52M25 335h64M306 335h64" fill="none" stroke="#7b61a8" stroke-width="1"/>
  <text x="42" y="132" fill="#b79ae6" class="micro">PORTRAIT / ASCII</text>
  {portrait_rows(source)}
  <path d="M396 110H875M396 335H875" stroke="#44375a" stroke-width="1"/>
  <path d="M396 110h76l9 9h100M875 110h-76l-9 9h-82" fill="none" stroke="#a58ad6" stroke-width="1.15"/>
  <text x="420" y="132" fill="#e9e5f2" class="title">IDENTITY / DATA CARD</text>
  <text x="850" y="132" text-anchor="end" fill="#b79ae6" class="micro">ONLINE</text>
  {info_rows()}
  <rect x="405" y="300" width="450" height="27" fill="#1b1724" stroke="#44375a"/>
  <circle cx="424" cy="314" r="5" fill="#9b7bd1"/><circle cx="424" cy="314" r="2" fill="#efe9ff"/>
  <text x="439" y="318" fill="#c5bbd4" class="micro">STATUS: BUILDING / LEARNING / EXPLORING</text>
  <path d="M25 378h100M715 378h160" stroke="#b79ae6" stroke-width="2"/>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
