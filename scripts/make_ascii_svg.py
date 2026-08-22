import sys
from pathlib import Path
from html import escape

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "thomas-ascii.svg"
RAMP = " .`:-=+*#%@"
COLS, ROWS = 64, 43


def load_portrait(path: Path) -> Image.Image:
    image = Image.open(path).convert("L")
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageOps.fit(image, (COLS, ROWS), method=Image.Resampling.LANCZOS, centering=(0.5, 0.42))
    image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))
    return ImageEnhance.Contrast(image).enhance(1.2)


def make_row(index: int, chars: str) -> str:
    y = 82 + index * 7
    return f'''<g>
      <text x="26" y="{y}" class="ascii" xml:space="preserve">{escape(chars)}</text>
    </g>'''


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.png"
    image = load_portrait(source)
    rows = []
    for y in range(ROWS):
        chars = "".join(RAMP[int(image.getpixel((x, y)) / 256 * len(RAMP))] for x in range(COLS))
        rows.append(make_row(y, chars))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400" role="img" aria-label="ASCII portrait of Thomas Smith">
  <style>.ascii {{ font: 9px/7px 'SFMono-Regular', Consolas, monospace; letter-spacing: -.35px; fill: #92ebb1; }} .micro {{ font: 10px Consolas, monospace; letter-spacing: 1px; }}</style>
  <defs><pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#24372c" stroke-width=".6"/></pattern></defs>
  <path d="M16 2H368L398 32V368L368 398H16L2 384V16Z" fill="#101719" stroke="#3f7355" stroke-width="1.4" />
  <path d="M16 11H362L389 38M389 362L362 389H16M11 384V16" fill="none" stroke="#2cc26b" stroke-width="1" opacity=".8" />
  <rect x="16" y="56" width="368" height="316" fill="url(#grid)" opacity=".55"/>
  <path d="M22 57h83l10 10h80M378 57h-54l-10 10h-55M22 372h80M298 372h80" fill="none" stroke="#60e695" stroke-width="1.2"/>
  <text x="24" y="32" fill="#6fe6a0" class="micro">THS // VISUAL_ID</text>
  <text x="376" y="32" text-anchor="end" fill="#8ba692" class="micro">PORTRAIT</text>
  <text x="25" y="76" fill="#e6edf3" class="micro">ASCII SCAN / 01</text>
  {''.join(rows)}
</svg>''', encoding="utf-8")


if __name__ == "__main__":
    main()
