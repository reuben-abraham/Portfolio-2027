#!/usr/bin/env python3
"""Import and optimise reference imagery from the previous redesign (portfolio2027/main).

Usage: python3 tools/import-assets.py /path/to/checkout-of-main [--force]
Writes WebP stills and MP4 loops (from GIF prototypes) into assets/img/.
"""
import os
import subprocess
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
SRC = os.path.join(ARGS[0] if ARGS else "/tmp/portfolio-main-ref", "wp-content/uploads")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

X = "2025/airport-transfers/extracted/"
AT = "2025/airport-transfers/"
STO = "2025/scan-to-order/"
BS = "2025/browse-sheet/"

STILLS = {
    "airport": {
        "deck-cover": AT + "figma_slide_160_4056.png",
        "hero-devices": "2026/06/justgrab-hero.jpg",
        "slide-split": X + "image21.png",
        "slide-funnel": X + "image17.png",
        "slide-gaps": X + "image14.png",
        "slide-uber": X + "image40.png",
        "slide-didi": X + "image47.png",
        "slide-feedback": X + "image19.png",
        "slide-flight-a": X + "image39.png",
        "slide-flight-b": X + "image45.png",
        "slide-flight-c": X + "image44.png",
        "slide-dropoff": X + "image48.png",
        "slide-boarding-a": X + "image43.png",
        "slide-boarding-b": X + "image34.png",
        "slide-visual": X + "image38.png",
        "delayed": AT + "page_32_img_9.png",
        "service-imagery": AT + "page_33_img_1_optimized.jpg",
        "flight-details": AT + "page_30_img_3.png",
        "taxi-selector": AT + "page_30_img_15.png",
    },
    "sto": {
        "deck-cover": X + "image1.png",
        "hero-devices": STO + "STO2.png",
        "slide-struggles": X + "image11.png",
        "sto1-friction": STO + "Context.png",
        "sto1-landing": STO + "STO1Landing.png",
        "sto1-menu": STO + "STO1Menu.png",
        "sto1-basket": STO + "STO1Basket.png",
        "sto1-bill": STO + "STO1Bill.png",
        "sto2-menu": STO + "STO2Menu.png",
        "sto2-basket": STO + "STO2Basket.png",
        "sto2-bill": STO + "STO2Bill.png",
        "comp-tabsquare": STO + "Tabsquare.png",
        "comp-xilnex": STO + "Xilnex.png",
        "comp-feedme": STO + "Feedme.png",
        "field-photo": STO + "images/field-learnings-bg.jpg",
        "slide-field": X + "image5.png",
        "slide-feedback": X + "image2.png",
        "slide-concept": X + "image25.png",
        "slide-brand-a": X + "image6.png",
        "slide-brand-b": X + "image35.png",
        "slide-brand-c": X + "image27.png",
        "slide-reco-a": X + "image3.png",
        "slide-reco-b": X + "image28.png",
        "slide-reco-c": X + "image37.png",
        "slide-basket-a": X + "image20.png",
        "slide-basket-b": X + "image24.png",
        "slide-basket-c": X + "image29.png",
        "render-branded": STO + "branded_menu.png",
        "render-reco": STO + "recommendations.png",
        "render-basket": STO + "shared_basket.png",
    },
    "browse": {
        "slide-title": BS + "slide_1.png",
        "slide-35": BS + "slide_2.png",
        "slide-sampling": BS + "slide_4.png",
        "slide-explorations": BS + "slide_18.png",
        "slide-bs2": BS + "slide_19.png",
        "status-home": BS + "mockups/status_quo_home.png",
        "status-details": BS + "mockups/status_quo_details.png",
        "paradigm-gallery": BS + "figma-assets/paradigm_gallery_grid.png",
        "paradigm-photos": BS + "figma-assets/paradigm_google_photos.png",
        "ease-close": BS + "pdf-assets/ease_sampling_close.png",
        "ease-next": BS + "pdf-assets/ease_sampling_next.png",
        "ease-more": BS + "pdf-assets/ease_sampling_more_info.png",
        "bs1-collapsed": BS + "mockups/browse_sheet_1_collapsed.png",
        "bs1-expanded": BS + "mockups/browse_sheet_1_expanded.png",
        "bs1-anatomy": BS + "mockups/browse_sheet_1_anatomy.png",
        "bs1-explore-a": BS + "mockups/browse_sheet_1_exploration_a.png",
        "bs1-explore-b": BS + "mockups/browse_sheet_1_exploration_b.png",
        "bs1-explore-c": BS + "mockups/browse_sheet_1_exploration_c.png",
        "bs2-movie-top": BS + "mockups/landing_movie_top.png",
        "bs2-show-top": BS + "mockups/landing_show_top.png",
        "bs2-movie-below": BS + "mockups/landing_movie_below.png",
        "bs2-show-below": BS + "mockups/landing_show_below.png",
        "bs2-episodes": BS + "mockups/landing_episode_nav.png",
        "bs2-watch-cta": BS + "mockups/browse_sheet_2_watch_cta.png",
        "tweet-1": BS + "mockups/tweet_feedback_1.png",
        "tweet-2": BS + "mockups/tweet_feedback_2.png",
        "tweet-3": BS + "mockups/tweet_feedback_3.png",
    },
    "archive": {
        "barter-cover": "2020/03/Barter1.jpg",
        "barter-ui-1": "2025/barter/image_14.png",
        "barter-ui-2": "2025/barter/image_18.gif",
        "barter-ui-3": "2025/barter/image_20.gif",
        "barter-sketch": "2025/barter/image_11.jpg",
        "inno-cover": "2020/03/INNO-COVER.jpg",
        "inno-1": "2025/innovision/image_12.jpg",
        "inno-2": "2025/innovision/image_13.jpg",
        "inno-3": "2025/innovision/image_17.jpg",
        "inno-4": "2025/innovision/image_18.jpg",
        "mun-cover": "2020/03/MUN-COVER.jpg",
        "mun-1": "2025/mun/image_10.jpg",
        "mun-2": "2025/mun/image_13.jpg",
        "mun-3": "2025/mun/image_15.jpg",
        "mun-4": "2025/mun/image_18.jpg",
        "vault-nitw": "2020/04/NITW.jpg",
        "vault-hope": "2020/04/HOPE.jpg",
        "vault-poorman": "2020/04/POORMAN.jpg",
        "vault-nfs": "2020/04/NFS.jpg",
        "vault-pinball": "2020/04/PINBALL.jpg",
        "vault-kalaam": "2020/04/KALAAM.jpg",
        "vault-hindi": "2020/04/HINDI.jpg",
        "vault-fusion": "2020/04/FUSION.jpg",
    },
}

for i in range(1, 19):
    STILLS.setdefault("tv", {})[f"tv-{i:02d}"] = f"2025/subscriber-tv/image_{i}.png"
for i in range(1, 25):
    STILLS.setdefault("helpdesk", {})[f"hd-{i:02d}"] = f"2025/helpdesk/image_{i}.png"

LOOPS = {
    "airport": {
        "transport-home": X + "image42.gif",
        "flight-v1": X + "image32.gif",
        "flight-v2": X + "image31.gif",
        "flight-v3": X + "image30.gif",
        "pickup-guide": X + "image46.gif",
    },
    "sto": {
        "branded-welcome": X + "image15.gif",
        "personalised-menu": X + "image16.gif",
        "shared-cart": X + "image13.gif",
        "basket": X + "image10.gif",
        "checkout": X + "image18.gif",
        "your-order": X + "image22.gif",
        "usability-test": STO + "UT.gif",
    },
}

MAX_W = 2000


def resolve(src):
    if os.path.exists(src):
        return src
    stem = os.path.splitext(src)[0]
    for ext in (".png", ".jpg", ".gif"):
        if os.path.exists(stem + ext):
            return stem + ext
    raise FileNotFoundError(src)


def still(src, dst):
    im = Image.open(resolve(src))
    im.seek(0)
    has_alpha = im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode == "RGBA"
    im = im.convert("RGBA" if has_alpha else "RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=82, method=6)
    return im.size


def loop(src, dst):
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", src,
            "-movflags", "+faststart", "-pix_fmt", "yuv420p",
            "-vf", "scale='trunc(min(720,iw)/2)*2':-2:flags=lanczos,fps=24",
            "-c:v", "libx264", "-crf", "26", "-preset", "slow", "-an", dst,
        ],
        check=True,
    )
    im = Image.open(src)
    im.seek(0)
    im = im.convert("RGB")
    if im.width > 720:
        im = im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS)
    im.save(dst.replace(".mp4", "-poster.webp"), "WEBP", quality=78)
    return im.size


def main():
    sizes = {}
    for group, items in STILLS.items():
        os.makedirs(os.path.join(OUT, group), exist_ok=True)
        for name, rel in items.items():
            dst = os.path.join(OUT, group, name + ".webp")
            if os.path.exists(dst) and "--force" not in sys.argv:
                sizes[f"{group}/{name}.webp"] = Image.open(dst).size
                continue
            sizes[f"{group}/{name}.webp"] = still(os.path.join(SRC, rel), dst)
    for group, items in LOOPS.items():
        os.makedirs(os.path.join(OUT, group), exist_ok=True)
        for name, rel in items.items():
            dst = os.path.join(OUT, group, name + ".mp4")
            if os.path.exists(dst) and "--force" not in sys.argv:
                sizes[f"{group}/{name}.mp4"] = Image.open(dst.replace(".mp4", "-poster.webp")).size
                continue
            sizes[f"{group}/{name}.mp4"] = loop(os.path.join(SRC, rel), dst)
    for k, (w, h) in sorted(sizes.items()):
        print(f"{k}\t{w}x{h}")


if __name__ == "__main__":
    main()
