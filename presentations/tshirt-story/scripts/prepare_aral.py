"""Crop the two NASA Earth Observatory Aral Sea images IDENTICALLY (no warm tone).

usage: python3 prepare_aral.py <early_image> <latest_image> <images_dir> [crop_fraction]
Both images come from the same World of Change series (same framing). The second is
resized to the first's pixel size if needed, then the same centred square crop is
applied to both. Writes aral_before.jpg and aral_after.jpg; rerun build_all.sh afterwards.
"""
import sys
from pathlib import Path

from PIL import Image

a, b, out = Image.open(sys.argv[1]).convert("RGB"), Image.open(sys.argv[2]).convert("RGB"), Path(sys.argv[3])
frac = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0   # <1.0 zooms in, same for both
if b.size != a.size:
    b = b.resize(a.size, Image.LANCZOS)
w, h = a.size
side = int(min(w, h) * frac)
box = ((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side)
for img, name in [(a, "aral_before.jpg"), (b, "aral_after.jpg")]:
    img.crop(box).save(out / name, quality=92)
print("crop box", box, "applied to both")
