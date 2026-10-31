"""Slide 4 chart: clothes made vs. times worn, indexed 2000 = 100 (source [4], EMF 2017).
Writes a transparent PNG fallback and the CSV data table.

usage: python3 make_chart.py <out_dir>
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path.home() / ".fonts" / "deck"
for f in FONT_DIR.glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

# Index values derived ONLY from the two statements in [4]:
#   "clothing production approximately doubled" over ~15 years (2000 -> 2015)  -> ~200
#   "clothing utilisation ... decreased by 36%" over the same period           -> 64
DATA = [
    # group, year, index value, label shown on bar, colour
    ("Clothes made", "2000", 100, "100", "#F2A65A"),
    ("Clothes made", "2015", 200, "≈200", "#E5845F"),
    ("Times each item is worn", "2000", 100, "100", "#C4532E"),
    ("Times each item is worn", "2015", 64, "64", "#3E0E0C"),
]
INK = "#3E0E0C"

with open(OUT / "chart_data.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Group", "Year", "Index (2000 = 100)", "Bar colour", "Source"])
    for g, y, v, _, c in DATA:
        w.writerow([g, y, v, c, "[4] Ellen MacArthur Foundation (2017)"])

fig, ax = plt.subplots(figsize=(8.0, 5.2), dpi=200)
fig.patch.set_alpha(0)
ax.set_facecolor("none")

xs = [0, 1, 2.6, 3.6]
bars = ax.bar(xs, [d[2] for d in DATA], width=0.82, color=[d[4] for d in DATA],
              edgecolor="none", zorder=2)
for x, d in zip(xs, DATA):
    ax.text(x, d[2] + 6, d[3], ha="center", va="bottom", color=INK,
            fontsize=20, fontfamily="Anton")
    ax.text(x, -12, d[1], ha="center", va="top", color=INK,
            fontsize=12, fontfamily="Montserrat", fontweight="medium")
for cx, g in [(0.5, "CLOTHES MADE"), (3.1, "TIMES EACH ITEM IS WORN")]:
    ax.text(cx, -40, g, ha="center", va="top", color=INK, fontsize=11,
            fontfamily="Montserrat", fontweight="semibold")

ax.axhline(0, color=INK, lw=1.2, zorder=3)
ax.set_xlim(-0.6, 4.2)
ax.set_ylim(-70, 235)
ax.axis("off")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig(OUT / "chart_made_vs_worn.png", transparent=True)
print("chart written")
