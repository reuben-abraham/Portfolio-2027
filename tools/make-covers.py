"""Compose case-study covers from real product screens.

Usage: python3 tools/make-covers.py
Writes assets/img/covers/<name>.webp at 2400x1500 (16:10).
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
OUT = IMG / "covers"
W, H = 2400, 1500
WELL = (230, 230, 228)
EDGE = (0, 0, 0, 22)


def rounded(im, radius):
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius, fill=255)
    im.putalpha(mask)
    edge = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius, outline=EDGE, width=2)
    return Image.alpha_composite(im, edge)


def fit_width(im, width):
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def phones(name, files, width=640, gap=96, top=230):
    canvas = Image.new("RGBA", (W, H), WELL + (255,))
    total = len(files) * width + (len(files) - 1) * gap
    x = (W - total) // 2
    for f in files:
        p = rounded(fit_width(Image.open(IMG / f), width), radius=round(width * 0.075))
        canvas.alpha_composite(p, (x, top))
        x += width + gap
    save(canvas, name)


def crops(name, src, boxes, scale, gap=96, top=None):
    im = Image.open(IMG / src).convert("RGB")
    parts = []
    for box in boxes:
        c = im.crop(box)
        parts.append(c.resize((round(c.width * scale), round(c.height * scale)), Image.LANCZOS))
    canvas = Image.new("RGBA", (W, H), WELL + (255,))
    total = sum(p.width for p in parts) + gap * (len(parts) - 1)
    x = (W - total) // 2
    tallest = max(p.height for p in parts)
    for p in parts:
        y = top if top is not None else (H - tallest) // 2
        canvas.alpha_composite(rounded(p, radius=14), (x, y))
        x += p.width + gap
    save(canvas, name)


def save(canvas, name):
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / f"{name}.webp", "WEBP", quality=86, method=6)
    print("wrote", OUT / f"{name}.webp")


phones("airport", ["airport/flight-details.webp", "airport/delayed.webp", "airport/pickup-guide-poster.webp"])
phones("scan-to-order", ["sto/sto2-menu.webp", "sto/sto2-basket.webp", "sto/sto2-bill.webp"])
phones("browse-sheet", ["browse/bs2-movie-top.webp", "browse/bs2-show-top.webp", "browse/bs2-episodes.webp"])
crops("subscriber-tv", "tv/tv-12.webp", [(40, 8, 660, 357), (726, 8, 1346, 357)], scale=1.82, gap=48)
crops("helpdesk", "helpdesk/hd-16.webp", [(252, 218, 1279, 1030), (1312, 218, 1747, 1030)], scale=1.4, top=380)
