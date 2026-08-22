import sys
from pathlib import Path
from html import escape

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "thomas-ascii.svg"
RAMP = " .`:-=+*#%@"
COLS, ROWS = 58, 39


def load_portrait(path: Path) -> Image.Image:
    image = Image.open(path).convert("L")
    image = ImageOps.autocontrast(image, cutoff=1)
    image = image.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))
    return ImageEnhance.Contrast(image).enhance(1.2)


def make_row(index: int, chars: str) -> str:
    y = 42 + index * 8
    return f'''<g>
      <text x="12" y="{y}" class="ascii" xml:space="preserve">{escape(chars)}</text>
    </g>'''


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.png"
    image = load_portrait(source)
    rows = []
    for y in range(ROWS):
        chars = "".join(RAMP[int(image.getpixel((x, y)) / 256 * len(RAMP))] for x in range(COLS))
        rows.append(make_row(y, chars))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="390" viewBox="0 0 370 390" role="img" aria-label="ASCII portrait of Thomas Smith">
  <style>.ascii {{ font: 8px/8px 'SFMono-Regular', Consolas, monospace; letter-spacing: .1px; fill: #80d6a0; }}</style>
  <rect width="370" height="390" rx="12" fill="#15191d" stroke="#30363d" />
  <text x="18" y="22" fill="#55d68a" style="font: 12px Consolas, monospace">portrait.ascii</text>
  {''.join(rows)}
</svg>''', encoding="utf-8")


if __name__ == "__main__":
    main()
