"""Align and crop the two NASA Earth Observatory Aral Sea images IDENTICALLY (no warm tone).

usage: python3 prepare_aral.py <early_image> <latest_image> <images_dir>
Both images come from the same World of Change series (same scale). The translation
between them is measured by phase correlation, then the same geographic square is cut
from each. Writes aral_before.jpg, aral_after.jpg and aral_overlay_check.jpg.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

a_img = Image.open(sys.argv[1]).convert("RGB")
b_img = Image.open(sys.argv[2]).convert("RGB")
out = Path(sys.argv[3])

a = np.asarray(a_img.convert("L"), float)
b = np.asarray(b_img.convert("L"), float)
H, W = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])


def pad(x):
    p = np.zeros((H, W))
    p[:x.shape[0], :x.shape[1]] = x - x.mean()
    return p


R = np.fft.fft2(pad(a)) * np.conj(np.fft.fft2(pad(b)))
r = np.abs(np.fft.ifft2(R / (np.abs(R) + 1e-9)))
dy, dx = np.unravel_index(r.argmax(), r.shape)
dy = dy - H if dy > H / 2 else dy
dx = dx - W if dx > W / 2 else dx
# a(y, x) == b(y - dy, x - dx): the same place sits at (y - dy, x - dx) in image b
oy, ox = -dy, -dx

# largest square valid in both images
y0 = max(0, -oy)
x0 = max(0, -ox)
y1 = min(a.shape[0], b.shape[0] - oy)
x1 = min(a.shape[1], b.shape[1] - ox)
side = min(y1 - y0, x1 - x0)
cy, cx = (y0 + y1) // 2, (x0 + x1) // 2
ya, xa = cy - side // 2, cx - side // 2
box_a = (xa, ya, xa + side, ya + side)
box_b = (xa + ox, ya + oy, xa + ox + side, ya + oy + side)

ca, cb = a_img.crop(box_a), b_img.crop(box_b)
ca.save(out / "aral_before.jpg", quality=92)
cb.save(out / "aral_after.jpg", quality=92)
Image.blend(ca, cb, 0.5).save(out / "aral_overlay_check.jpg", quality=85)
print(f"offset (dy, dx) = ({oy}, {ox}), peak {r.max():.2f}; box early {box_a}, latest {box_b}")
