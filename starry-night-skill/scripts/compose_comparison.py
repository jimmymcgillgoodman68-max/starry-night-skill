#!/usr/bin/env python3
"""Create an exact original-plus-effect comparison PNG.

The original panel is copied from decoded source pixels. The generated effect must
already match the source aspect ratio closely; this script refuses large ratio
mismatches rather than hiding them with a destructive crop.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageOps
except ImportError as exc:  # pragma: no cover - dependency guidance
    raise SystemExit("Pillow is required. Install it with: python3 -m pip install Pillow") from exc


BACKGROUND = "#F7F4EE"
BORDER_COLOR = "#E5E0D7"
DEFAULT_RATIO_TOLERANCE = 0.0025  # 0.25%


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mount one untouched source photo and its Starry Night effect on a warm-white canvas."
    )
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--effect", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--ratio-tolerance",
        type=float,
        default=DEFAULT_RATIO_TOLERANCE,
        help="Maximum relative aspect-ratio mismatch before refusing composition (default: 0.0025).",
    )
    parser.add_argument("--force", action="store_true", help="Allow replacing an existing output file.")
    return parser.parse_args()


def load_display_rgb(path: Path) -> Image.Image:
    if not path.is_file():
        raise SystemExit(f"Image not found: {path}")
    with Image.open(path) as loaded:
        return ImageOps.exif_transpose(loaded).convert("RGB")


def ratio_mismatch(a: Image.Image, b: Image.Image) -> float:
    ratio_a = a.width / a.height
    ratio_b = b.width / b.height
    return abs(ratio_a - ratio_b) / ratio_a


def paste_panel(canvas: Image.Image, image: Image.Image, x: int, y: int, border: int) -> None:
    panel_w = image.width + 2 * border
    panel_h = image.height + 2 * border
    canvas.paste(BORDER_COLOR, (x, y, x + panel_w, y + panel_h))
    canvas.paste(image, (x + border, y + border))


def main() -> None:
    args = parse_args()
    if args.ratio_tolerance < 0:
        raise SystemExit("--ratio-tolerance must be non-negative")
    if args.output.suffix.lower() != ".png":
        raise SystemExit("Output filename must end in .png")
    if args.output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing output: {args.output}")

    original = load_display_rgb(args.original)
    effect = load_display_rgb(args.effect)
    mismatch = ratio_mismatch(original, effect)
    if mismatch > args.ratio_tolerance:
        raise SystemExit(
            "Effect aspect ratio differs from original by "
            f"{mismatch:.3%}, above the allowed {args.ratio_tolerance:.3%}. "
            "Regenerate the effect with the original aspect ratio."
        )

    # The tiny tolerance only absorbs generator rounding by one or two pixels.
    effect = effect.resize(original.size, Image.Resampling.LANCZOS)

    width, height = original.size
    short_edge = min(width, height)
    margin = max(1, round(short_edge * 0.04))
    gap = margin
    border = max(1, round(short_edge * 0.00125))
    panel_w = width + 2 * border
    panel_h = height + 2 * border

    if width > height:  # landscape: original above effect
        canvas_size = (panel_w + 2 * margin, 2 * panel_h + 2 * margin + gap)
        positions = ((margin, margin), (margin, margin + panel_h + gap))
        layout = "vertical"
    else:  # portrait and square: original left, effect right
        canvas_size = (2 * panel_w + 2 * margin + gap, panel_h + 2 * margin)
        positions = ((margin, margin), (margin + panel_w + gap, margin))
        layout = "horizontal"

    canvas = Image.new("RGB", canvas_size, BACKGROUND)
    paste_panel(canvas, original, *positions[0], border)
    paste_panel(canvas, effect, *positions[1], border)

    # Verify that the mounted original region equals the decoded source pixels.
    ox, oy = positions[0]
    mounted_original = canvas.crop((ox + border, oy + border, ox + border + width, oy + border + height))
    if ImageChops.difference(original, mounted_original).getbbox() is not None:
        raise SystemExit("Original-pixel verification failed; output was not written.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output, format="PNG", optimize=True)
    print(
        json.dumps(
            {
                "output": str(args.output.resolve()),
                "layout": layout,
                "canvas_size": list(canvas.size),
                "panel_image_size": [width, height],
                "margin": margin,
                "gap": gap,
                "border": border,
                "ratio_mismatch": mismatch,
                "original_pixels_verified": True,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
