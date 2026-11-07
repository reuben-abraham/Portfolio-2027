"""Compose case-study covers in the colour-field style.

Each cover is one flat project colour, the project name set edge to edge in
Geist, and real product screens overlapping the bottom of the wordmark and
bleeding off the bottom edge.

Usage: python3 tools/make-covers.py [path/to/Geist-Medium.ttf]
Writes assets/img/covers/<name>.webp at 2400x1500 (16:10).
The project colours must match the --field / --field-ink tokens in site.css.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
OUT = IMG / "covers"
FONT = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent / "Geist-Medium.ttf")
W, H = 2400, 1500
MARGIN = 120

PROJECTS = {
    "airport": ("#A9D1F5", "#0A2540"),
    "scan-to-order": ("#1E7A4C", "#EEF7F0"),
    "browse-sheet": ("#2E4BD6", "#F1F3FF"),
    "subscriber-tv": ("#F07A4A", "#2B0F05"),
    "helpdesk": ("#CBC4F3", "#1B1446"),
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def wordmark(canvas, text, ink, max_height=380):
    """Set text edge to edge between the margins; return its bottom y."""
    size = 400
    font = ImageFont.truetype(FONT, size)
    tracking = -0.045 * size
    probe = ImageDraw.Draw(canvas)
    width = int(sum(probe.textlength(c, font=font) + tracking for c in text) + size)
    layer = Image.new("L", (width, size * 2), 0)
    draw = ImageDraw.Draw(layer)
    x = size // 4
    for c in text:
        draw.text((x, size // 4), c, font=font, fill=255)
        x += draw.textlength(c, font=font) + tracking
    layer = layer.crop(layer.getbbox())
    scale = min((W - 2 * MARGIN) / layer.width, max_height / layer.height)
    layer = layer.resize((round(layer.width * scale), round(layer.height * scale)), Image.LANCZOS)
    solid = Image.new("RGBA", layer.size, ink + (255,))
    canvas.paste(solid, (MARGIN, MARGIN), layer)
    return MARGIN + layer.height


def rounded(im, radius, edge):
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius, fill=255)
    im.putalpha(mask)
    line = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(line).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius, outline=edge, width=2)
    return Image.alpha_composite(im, line)


def fit_width(im, width):
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def cover(name, title, parts, widths, gap=72, overlap=0.2, radius=0.075):
    field, ink = (hex_rgb(c) for c in PROJECTS[name])
    canvas = Image.new("RGBA", (W, H), field + (255,))
    bottom = wordmark(canvas, title, ink)
    top = int(bottom - overlap * (bottom - MARGIN))
    edge = ink + (40,)
    total = sum(widths) + gap * (len(widths) - 1)
    x = (W - total) // 2
    for part, width in zip(parts, widths):
        im = part if isinstance(part, Image.Image) else Image.open(IMG / part)
        p = rounded(fit_width(im, width), round(width * radius), edge)
        canvas.alpha_composite(p, (x, top))
        x += width + gap
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / f"{name}.webp", "WEBP", quality=86, method=6)
    print("wrote", OUT / f"{name}.webp")


def crop(src, box):
    return Image.open(IMG / src).convert("RGB").crop(box)


cover("airport", "Airport Transfers",
      ["airport/flight-details.webp", "airport/delayed.webp", "airport/pickup-guide-poster.webp"], [600] * 3)
cover("scan-to-order", "Scan to Order",
      ["sto/sto2-menu.webp", "sto/sto2-basket.webp", "sto/sto2-bill.webp"], [600] * 3)
cover("browse-sheet", "Browse Sheet",
      ["browse/bs2-movie-top.webp", "browse/bs2-show-top.webp", "browse/bs2-episodes.webp"], [600] * 3)
cover("subscriber-tv", "Subscriber TV",
      [crop("tv/tv-12.webp", (40, 8, 660, 357)), crop("tv/tv-12.webp", (726, 8, 1346, 357))],
      [1060, 1060], gap=56, overlap=0.18, radius=0.012)
cover("helpdesk", "Helpdesk",
      [crop("helpdesk/hd-16.webp", (252, 218, 1279, 1030)), crop("helpdesk/hd-16.webp", (1312, 218, 1747, 1030))],
      [1440, 610], gap=64, overlap=0.22, radius=0.02)
