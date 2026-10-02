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
        ascii_rows = [node.text or "" for node in previous.iter("{http://www.w3.org/2000/svg}text") if node.get("class") == "ascii"]
    rows = []
    for y, chars in enumerate(ascii_rows):
        rows.append(f'<text x="42" y="{155 + y * 6}" class="ascii" xml:space="preserve">{escape(chars)}</text>')
    return "".join(rows)


def info_rows() -> str:
    output = []
    for index, (label, value) in enumerate(PROFILE_ROWS):
        if not label and not value:
            continue
        y = 170 + index * 30
        prefix = label.ljust(12) if label else "//          "
        output.append(
            f'<text x="420" y="{y}" class="line"><tspan fill="#4fa3c7">{escape(prefix)}</tspan><tspan fill="#e1eff7">  {escape(value)}</tspan></text>'
        )
    return "".join(output)


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.png"
    OUT.parent.mkdir(exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="480" viewBox="0 0 900 480" role="img" aria-label="Thomas Smith profile card">
  <style>
    .ascii {{ font: 8px/6px 'SFMono-Regular', Consolas, monospace; letter-spacing: -.3px; fill: #8dcde8; }}
    .line {{ font: 13px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
    .title {{ font: 700 16px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; letter-spacing: 1px; }}
    .micro {{ font: 10px 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; letter-spacing: 1px; }}
  </style>
  <defs>
    <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#163346" stroke-width=".6"/></pattern>
    <pattern id="fineGrid" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0H0V12" fill="none" stroke="#163346" stroke-width=".5"/></pattern>
  </defs>
  <rect x="1" y="1" width="898" height="478" rx="10" fill="#071824" stroke="#28546d" stroke-width="1.4"/>
  <rect x="14" y="14" width="872" height="452" rx="6" fill="none" stroke="#163346" stroke-width="1"/>
  <rect x="16" y="55" width="868" height="406" fill="url(#grid)" opacity=".52"/>
  <path d="M25 86H875M25 430H875" fill="none" stroke="#28546d" stroke-width="1"/>
  <text x="25" y="32" fill="#4fa3c7" class="micro">THS // PROFILE</text>
  <text x="875" y="32" text-anchor="end" fill="#7897aa" class="micro">PARIS · FRANCE</text>
  <text x="25" y="74" fill="#e1eff7" class="title">THOMAS SMITH</text>
  <text x="875" y="74" text-anchor="end" fill="#4fa3c7" class="micro">PROFILE / 01</text>
  <rect x="25" y="110" width="345" height="300" rx="6" fill="#0a1d2b" stroke="#28546d"/>
  <rect x="34" y="119" width="327" height="282" fill="url(#fineGrid)" opacity=".42"/>
  <text x="42" y="132" fill="#4fa3c7" class="micro">PORTRAIT / ASCII</text>
  {portrait_rows(source)}
  <path d="M396 110V400M396 400H875" stroke="#28546d" stroke-width="1"/>
  <text x="420" y="132" fill="#e1eff7" class="title">IDENTITY / DATA CARD</text>
  <text x="850" y="132" text-anchor="end" fill="#4fa3c7" class="micro">ONLINE</text>
  {info_rows()}
  <rect x="405" y="420" width="450" height="28" rx="4" fill="#0a1d2b" stroke="#28546d"/>
  <circle cx="424" cy="434" r="5" fill="#4fa3c7"/><circle cx="424" cy="434" r="2" fill="#e1eff7"/>
  <text x="439" y="438" fill="#9db8c8" class="micro">STATUS: BUILDING / LEARNING / EXPLORING</text>
  <path d="M25 458h100M715 458h160" stroke="#4fa3c7" stroke-width="1.5"/>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
