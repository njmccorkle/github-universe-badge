#!/usr/bin/env python3
"""Render the Relativity app's PNG assets, and icon from brand SVGs.

Requires: pip install pymupdf pillow
"""

from io import BytesIO
from pathlib import Path

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/relativity"
APP = ROOT / "badge/apps/relativity"
ORANGE = "#ef5f11"
WHITE = "#fcfdfe"

# name -> (svg file, width in px, fill)
LOGOS = {
    "logo_orange": ("Relativity_rgb.svg", 280, ORANGE),
    "r_white": ("R.svg", 90, WHITE),
    "rel_orange": ("Rel.svg", 200, ORANGE),
    "ty_orange": ("ty.svg", 240, ORANGE),
}


def render(svg_name, width, fill):
    doc = pymupdf.open(SOURCE / svg_name)
    page = doc[0]
    scale = width / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=True)
    shape = Image.open(BytesIO(pix.tobytes("png"))).convert("RGBA")
    # pymupdf ignores CSS class fills, so keep only the alpha and tint it.
    tinted = Image.new("RGBA", shape.size, fill)
    tinted.putalpha(shape.getchannel("A"))
    return tinted


def build_logos():
    assets = APP / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for name, (svg_name, width, fill) in LOGOS.items():
        img = render(svg_name, width, fill)
        img.save(assets / f"{name}.png", optimize=True)
        print(f"{name}.png {img.size}")


def build_icon():
    icon = Image.new("RGBA", (48, 48), ORANGE)
    mark = render("R.svg", 26, WHITE)
    icon.alpha_composite(mark, ((48 - mark.width) // 2, (48 - mark.height) // 2))
    icon.convert("RGB").save(APP / "icon.png", optimize=True)


if __name__ == "__main__":
    build_logos()
    build_icon()
