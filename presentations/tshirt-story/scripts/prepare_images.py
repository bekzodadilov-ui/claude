"""Crop the user's photo COPIES to their slide frames, apply one identical warm tone,
and generate transparent oxblood gradient overlays. Originals are only read, never written.

usage: python3 prepare_images.py <source_photos_dir> <out_dir>
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from layout import FRAMES, PALETTE, W, H  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

# One warm-tone recipe, applied identically to every chosen photo copy.
GAIN = np.array([1.04, 1.00, 0.91])          # lift reds, pull blues
TINT = np.array([0xF2, 0xA6, 0x5A]) / 255.0  # sun orange
TINT_MIX = 0.06


def warm(img: Image.Image) -> Image.Image:
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0
    a = np.clip(a * GAIN, 0, 1)
    a = a * (1 - TINT_MIX) + TINT * TINT_MIX
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))


def crop_to(img, w, h, cx, cy):
    """Largest crop with aspect w/h centred on (cx, cy), clamped to the image."""
    sw, sh = img.size
    target = w / h
    if sw / sh > target:
        ch, cw = sh, round(sh * target)
    else:
        cw, ch = sw, round(sw / target)
    x0 = min(max(round(cx * sw - cw / 2), 0), sw - cw)
    y0 = min(max(round(cy * sh - ch / 2), 0), sh - ch)
    return img.crop((x0, y0, x0 + cw, y0 + ch)), (cw, ch)


report = []
for slot, f in FRAMES.items():
    img = ImageOps.exif_transpose(Image.open(SRC / f["src"]))
    cropped, (cw, ch) = crop_to(img, f["w"], f["h"], f["cx"], f["cy"])
    # export at up to 2x the frame size, never upscaling beyond what is needed for 1x
    scale = min(2.0, max(1.0, cw / f["w"]))
    out_size = (round(f["w"] * scale), round(f["h"] * scale))
    res = cropped.resize(out_size, Image.LANCZOS)
    warm(res).save(OUT / f"slot{slot}_{Path(f['src']).stem}.jpg", quality=90, optimize=True)
    report.append(f"{slot}: {f['src']} {img.size} crop {cw}x{ch} -> frame {f['w']}x{f['h']} "
                  f"(source covers {cw / f['w']:.0%} of frame width)")


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w, h, stops, name):
    """Vertical oxblood gradient PNG; stops = [(pos 0..1, alpha 0..1), ...]."""
    ys = np.linspace(0, 1, h)
    pos, al = zip(*stops)
    alpha = np.interp(ys, pos, al)
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., :3] = hexrgb(PALETTE["oxblood"])
    arr[..., 3] = (alpha[:, None] * 255).astype(np.uint8)
    Image.fromarray(arr, "RGBA").save(OUT / name)


# Slide 1: soft fade at the bottom of the T-shirt photo so the page number reads.
gradient(FRAMES["A"]["w"], 1080, [(0, 0), (0.72, 0), (1, 0.7)], "grad_s1.png")
# Slide 3: top band for the stage tracker, heavy bottom for the headline.
gradient(FRAMES["C"]["w"], 1080, [(0, 0.7), (0.3, 0.45), (0.5, 0.1), (0.72, 0.35), (1, 0.92)], "grad_s3.png")
# Slide 5: full bleed, same recipe.
gradient(W, H, [(0, 0.55), (0.18, 0.2), (0.4, 0.15), (0.65, 0.6), (1, 0.92)], "grad_s5.png")

print("\n".join(report))
