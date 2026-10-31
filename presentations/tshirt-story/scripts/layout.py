"""Shared layout constants for the T-shirt deck (units: px on a 1920x1080 canvas)."""

W, H = 1920, 1080
EDGE = 80          # corner info / stage tracker distance from slide edges
MARGIN = 120       # content margin

PALETTE = {
    "cream": "F4E6D8",
    "sand": "EAD3BF",
    "sun": "F2A65A",
    "coral": "E5845F",
    "terracotta": "C4532E",
    "rust": "9E3B22",
    "oxblood": "3E0E0C",
}

# Photo frames: slot -> (slide, x, y, w, h) and the source crop centre (fraction of source w/h)
FRAMES = {
    "A": dict(src="tshirt.jpg",             x=1056, y=0,   w=864, h=1080, cx=0.477, cy=0.48),
    "B": dict(src="cotton_field.jpg",       x=1240, y=190, w=560, h=720,  cx=0.50,  cy=0.50),
    "C": dict(src="aral_moynaq_ship.jpg",   x=0,    y=0,   w=1056, h=1080, cx=0.445, cy=0.50),
    "D": dict(src="textile_factory.jpg",    x=120,  y=316, w=820, h=584,  cx=0.55,  cy=0.50),
    "F": dict(src="fast_fashion_racks.jpg", x=152,  y=196, w=756, h=240,  cx=0.50,  cy=0.50),
    "G": dict(src="secondhand_market.jpg",  x=1012, y=196, w=756, h=240,  cx=0.50,  cy=0.52),
}
