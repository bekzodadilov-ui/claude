"""Build 'The Story of a T-Shirt' deck (python-pptx, 1920x1080 canvas, 13.333 x 7.5 in).

usage: python3 build_deck.py <img_dir> <out.pptx>
  <img_dir>  processed photo copies + gradient overlays (prepare_images.py)
All coordinates are px on the 1920x1080 canvas; font sizes are PowerPoint points.
"""
import sys
from pathlib import Path

from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_MARK
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

sys.path.insert(0, str(Path(__file__).parent))
from layout import EDGE, FRAMES, H, MARGIN, PALETTE as C, W  # noqa: E402

IMG, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FONT_DIR = Path.home() / ".fonts" / "deck"
FONT_FILES = {
    "Montserrat": "Montserrat-400-normal.ttf",
    "Montserrat Medium": "Montserrat-500-normal.ttf",
    "Archivo Black": "ArchivoBlack-400-normal.ttf",
    "Anton": "Anton-400-normal.ttf",
    "DM Serif Display": "DMSerifDisplay-400-italic.ttf",
    "Dancing Script": "DancingScript-400-normal.ttf",
}
WARNINGS = []
import os
QA_FLATTEN = os.environ.get("QA_FLATTEN") == "1"   # render-only: LibreOffice clips spaced+transparent text
SLIDE_BG = ["cream"]

AUTHOR = "BEKZODJON KIRGIZBAYEV · SUST 1000 7T"
CORNER_PT, MICRO_PT, TRACK = 10.5, 12, 30   # TRACK: letter spacing in 1/1000 em -> spc = pt*30 (~300)


# ---------------------------------------------------------------- helpers
def E(px):
    return Emu(int(round(px * 6350)))


def text_width(s, font, pt, spc=0):
    """Rendered width in px (pt*2 = px on the 1920 canvas) incl. letter spacing."""
    f = ImageFont.truetype(str(FONT_DIR / FONT_FILES[font]), int(round(pt * 2)))
    return f.getlength(s) + len(s) * (spc / 100) * 2


def set_alpha(clr_el, alpha):
    a = etree.SubElement(clr_el, qn("a:alpha"))
    a.set("val", str(int(alpha * 100000)))


def R(t, font="Montserrat", size=24, color="oxblood", alpha=None, spc=0, italic=False, sup=False, bg=None):
    return dict(t=t, font=font, size=size, color=C[color], alpha=alpha, spc=spc, italic=italic, sup=sup,
                bg=bg)


def mix(fg, bg, a):
    f = [int(fg[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(bg[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x * a + y * (1 - a)):02X}" for x, y in zip(f, b))


def micro(t, color="oxblood", size=MICRO_PT, alpha=None, bg=None):
    return R(t, "Montserrat Medium", size, color, alpha, spc=size * TRACK, bg=bg)


def text(slide, x, y, w, h, paras, anchor="top", align="left", wrap=True, name=None,
         line=None, space_after=0, bullet=None, marL=0):
    """paras: list of run-lists. line: exact line spacing in pt (None = single)."""
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "right": PP_ALIGN.RIGHT, "center": PP_ALIGN.CENTER}[align]
        if line:
            p.line_spacing = Pt(line)
        if space_after:
            p.space_after = Pt(space_after)
        if bullet:
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(E(marL)))
            pPr.set("indent", str(-E(marL)))
            bc = etree.SubElement(pPr, qn("a:buClr"))
            etree.SubElement(bc, qn("a:srgbClr")).set("val", C[bullet])
            etree.SubElement(pPr, qn("a:buSzPct")).set("val", "150000")
            etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Montserrat")
            etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
        for r in runs:
            run = p.add_run()
            run.text = r["t"]
            f = run.font
            f.name = r["font"]
            f.size = Pt(r["size"])
            f.bold = False
            f.italic = r["italic"]
            col = r["color"]
            if QA_FLATTEN and r["alpha"] is not None:
                col = mix(col, C[r["bg"] or SLIDE_BG[0]], r["alpha"])
            f.color.rgb = RGBColor.from_string(col)
            rPr = run._r.get_or_add_rPr()
            if r["spc"]:
                rPr.set("spc", str(int(r["spc"])))
            if r["sup"]:
                rPr.set("baseline", "30000")
            if r["alpha"] is not None and not QA_FLATTEN:
                set_alpha(rPr.find(qn("a:solidFill")).find(qn("a:srgbClr")), r["alpha"])
        # overflow check for single-run-style lines (wrap disabled or explicit lines)
        width = sum(text_width(r["t"], r["font"], r["size"], r["spc"]) for r in runs)
        if width > w - marL + 1:
            WARNINGS.append(f"slide text may wrap/overflow: '{''.join(r['t'] for r in runs)}' "
                            f"{width:.0f}px > box {w - marL}px")
    return tb


def shape(slide, x, y, w, h, color, kind=MSO_SHAPE.RECTANGLE, alpha=None, name=None, radius=None):
    s = slide.shapes.add_shape(kind, E(x), E(y), E(w), E(h))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(C[color])
    if alpha is not None:
        set_alpha(s._element.spPr.find(qn("a:solidFill")).find(qn("a:srgbClr")), alpha)
    s.line.fill.background()
    st = s._element.find(qn("p:style"))
    if st is not None:
        s._element.remove(st)
    if radius is not None:
        s.adjustments[0] = radius
    if name:
        s.name = name
    # no default text style surprises
    s.text_frame.text = ""
    return s


def outline(s, color, width_px):
    s.line.color.rgb = RGBColor.from_string(C[color])
    s.line.width = E(width_px)


def picture(slide, path, x, y, w, h, name=None):
    p = slide.shapes.add_picture(str(path), E(x), E(y), E(w), E(h))
    if name:
        p.name = name
    return p


def photo(slide, slot):
    f = FRAMES[slot]
    path = next(IMG.glob(f"slot{slot}_*.jpg"))
    return picture(slide, path, f["x"], f["y"], f["w"], f["h"], name=f"Photo slot {slot}")


def ref(slide, n, x, y, color, alpha=None, size=MICRO_PT):
    """Static superscript-style reference number in micro-label style (own text box)."""
    return text(slide, x, y, 40, 30, [[micro(str(n), color, size, alpha)]], wrap=False,
                name=f"Ref {n}")


def ref_after(slide, n, x, y, runs, color, gap=6, alpha=None, size=MICRO_PT, marL=0):
    width = sum(text_width(r["t"], r["font"], r["size"], r["spc"]) for r in runs)
    return ref(slide, n, x + marL + width + gap, y - 2, color, alpha, size)


def rule(slide, x, y, color="terracotta", w=40):
    return shape(slide, x, y, w, 3, color, name="Rule")


def background(slide, color):
    SLIDE_BG[0] = color
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(C[color])


def corner(slide, n, left_color="oxblood", right_color="oxblood", left=True, label=None, lbg=None, rbg=None):
    lab = label or f"{n:02d} / 06"
    if left:
        text(slide, EDGE, H - EDGE - 24, 760, 24, [[micro(AUTHOR, left_color, CORNER_PT, 0.6, lbg)]],
             anchor="bottom", wrap=False, name="Corner info left")
    text(slide, W - EDGE - 320, H - EDGE - 24, 320, 24, [[micro(lab, right_color, CORNER_PT, 0.6, rbg)]],
         anchor="bottom", align="right", wrap=False, name="Corner info right")


def tracker(slide, active, base_color, bg=None):
    """GROW · MAKE · WEAR · THROW, same position on slides 2-5."""
    x, y = EDGE, EDGE
    words = ["GROW", "MAKE", "WEAR", "THROW"]
    for i, wd in enumerate(words):
        on = wd in active
        r = micro(wd, "sun" if on else base_color, MICRO_PT, None if on else 0.4, bg)
        wpx = text_width(wd, r["font"], r["size"], r["spc"])
        text(slide, x, y, wpx + 6, 30, [[r]], wrap=False, name=f"Tracker {wd}")
        if on:
            shape(slide, x, y + 32, 28, 3, "terracotta", name=f"Tracker underline {wd}")
        x += wpx + 14
        if i < len(words) - 1:
            d = micro("·", base_color, MICRO_PT, 0.4, bg)
            dw = text_width("·", d["font"], d["size"], d["spc"])
            text(slide, x, y, dw + 6, 30, [[d]], wrap=False, name="Tracker dot")
            x += dw + 14


def sun(slide, cx, cy, d, alpha=None):
    return shape(slide, cx - d / 2, cy - d / 2, d, d, "sun", MSO_SHAPE.OVAL, alpha=alpha, name="Sun circle")


def placeholder(slide, x, y, w, h, title, sub, name, title_pt=14, sub_pt=12):
    s = shape(slide, x, y, w, h, "sand", name=name)
    outline(s, "terracotta", 2)
    text(slide, x + 24, y + h / 2 - 60, w - 48, 120,
         [[micro(title, "oxblood", title_pt)], [R(sub, "Montserrat Medium", sub_pt, "oxblood")]],
         anchor="middle", align="center", name=name + " label", line=sub_pt * 1.5)
    return s


def notes(slide, lines):
    slide.notes_slide.notes_text_frame.text = "\n".join(lines)


# ---------------------------------------------------------------- deck
prs = Presentation()
prs.slide_width, prs.slide_height = E(W), E(H)
BLANK = prs.slide_layouts[6]

# ---------- 1  TITLE
s = prs.slides.add_slide(BLANK)
background(s, "cream")
sun(s, 740, 300, 360)
photo(s, "A")
picture(s, IMG / "grad_s1.png", FRAMES["A"]["x"], 0, FRAMES["A"]["w"], H, name="Photo fade")
text(s, EDGE, EDGE, 700, 30, [[micro("THE STORY OF YOUR OWN STUFF")]], wrap=False, name="Kicker")
rule(s, EDGE, EDGE + 36)
text(s, MARGIN, 320, 900, 300,
     [[R("The Story", "Archivo Black", 65, "oxblood")], [R("of a T-Shirt", "Archivo Black", 65, "terracotta")]],
     line=72, name="Headline")
text(s, MARGIN + 4, 650, 880, 34, [[micro("FROM FIELD TO LANDFILL", "oxblood", 17)]], wrap=False,
     name="Subtitle")
rule(s, EDGE, 876)
text(s, EDGE, 896, 600, 100,
     [[micro("BEKZODJON KIRGIZBAYEV")], [micro("SUST 1000 7T")], [micro("03.11.2026")]],
     line=17, name="Details block")
corner(s, 1, right_color="cream", left=False, rbg="oxblood")
notes(s, [
    "Object: one plain cotton T-shirt",
    "Angle: Uzbekistan, cotton country",
    "Route: grow → make → wear → throw",
    "Brief: EPA Ireland, The Story of Your Stuff",
])

# ---------- 2  GROW
s = prs.slides.add_slide(BLANK)
background(s, "rust")
sun(s, 930, 250, 360, alpha=0.45)
tracker(s, {"GROW"}, "cream")
num = text(s, MARGIN - 8, 150, 1060, 470, [[R("2,700", "Anton", 210, "cream")]], wrap=False,
           name="Key number", line=230)
ref(s, 1, MARGIN - 8 + text_width("2,700", "Anton", 210) + 10, 212, "cream", size=16)
lab = [micro("LITRES OF WATER FOR ONE COTTON T-SHIRT", "cream", 14)]
text(s, MARGIN, 640, 1060, 34, [lab], wrap=False, name="Number label")
ref_after(s, 1, MARGIN, 640, lab, "cream", alpha=None)
rule(s, MARGIN, 690, "sun")
b1 = [R("One person's drinking water for 2.5 years", "Montserrat", 21, "cream")]
b2 = [R("Uzbekistan: world's 7th-largest cotton producer", "Montserrat", 21, "cream")]
for i, b in enumerate([b1, b2]):
    yb = 730 + i * 66
    text(s, MARGIN, yb, 1080, 50, [b], bullet="sun", marL=34, wrap=False, name=f"Bullet {i + 1}")
    ref_after(s, [1, 5][i], MARGIN, yb, b, "cream", marL=34)
f = FRAMES["B"]
shape(s, f["x"] - 16, f["y"] - 16, f["w"] + 32, f["h"] + 32, "sand", name="Photo frame")
photo(s, "B")
corner(s, 2, "cream", "cream")
notes(s, [
    "2,700 L water → 1 cotton T-shirt [1]",
    "≈ one person's drinking water, ~900 days ≈ 2.5 yrs [1]",
    "Uzbekistan: 7th-largest cotton producer, 2025/26 [5]",
    "≈ 2.8% of world cotton, ≈ 3.45 M bales [5]",
    "Cotton on irrigated desert land, fed by 2 rivers [2]",
])

# ---------- 3  THE ARAL SEA
s = prs.slides.add_slide(BLANK)
background(s, "cream")
photo(s, "C")
picture(s, IMG / "grad_s3.png", 0, 0, FRAMES["C"]["w"], H, name="Photo gradient")
tracker(s, {"GROW"}, "cream", bg="oxblood")
text(s, MARGIN, 150, 880, 400,
     [[R("THE SEA THAT", "Anton", 86, "cream")], [R("WENT DRY", "Anton", 86, "cream")]],
     line=90, wrap=False, name="Headline")
sub = [R("Rivers diverted to irrigate cotton", "Montserrat Medium", 22, "cream")]
text(s, MARGIN, 880, 870, 44, [sub], wrap=False, name="Subline")
ref_after(s, 2, MARGIN, 880, sub, "cream")
# right panel
px0 = FRAMES["C"]["w"]
shape(s, px0, 0, W - px0, H, "cream", name="Right panel")
text(s, px0 + 80, EDGE, 600, 30, [[micro("SAME PLACE. SAME FRAME.")]], wrap=False, name="Panel kicker")
rule(s, px0 + 80, EDGE + 36)
SAT = 360
for i, (fname, year, l1, l2) in enumerate([
        ("aral_before.jpg", "2000", "Eastern basin", "still holds water"),
        ("aral_after.jpg", "2018", "Eastern basin first", "ran dry in 2014")]):
    sx, sy = px0 + 80, 150 + i * (SAT + 40)
    shape(s, sx - 6, sy - 6, SAT + 12, SAT + 12, "sand", name="Satellite border")
    sat = IMG / fname
    if sat.exists():
        picture(s, sat, sx, sy, SAT, SAT, name=f"Satellite {year}")
    else:
        placeholder(s, sx, sy, SAT, SAT, "IMAGE NEEDED",
                    f"{fname} ({'year 2000' if i == 0 else 'latest year'})",
                    name=f"Satellite placeholder {i + 1}", title_pt=11, sub_pt=10)
    tx = sx + SAT + 44
    text(s, tx, sy + 10, 300, 150, [[R(year, "Anton", 66, "oxblood" if i == 0 else "terracotta")]],
         wrap=False, name=f"Year {year}", line=72)
    cap2 = [R(l2, "Montserrat Medium", 15, "oxblood")]
    text(s, tx, sy + 170, 300, 80, [[R(l1, "Montserrat Medium", 15, "oxblood")], cap2], line=21,
         name=f"Caption {year}")
    ref_after(s, 2, tx, sy + 170 + 42, cap2, "oxblood", size=11)
text(s, px0 + 80, 150 + 2 * (SAT + 40) - 8, 700, 24, [[micro("IMAGES: NASA EARTH OBSERVATORY", "oxblood",
     CORNER_PT, 0.6)]], wrap=False, name="Image credit")
corner(s, 3, "cream", "oxblood", lbg="oxblood")
notes(s, [
    "Aral Sea: once one of the world's 4 largest lakes [2]",
    "1960s: Soviet canals take Amu Darya + Syr Darya water → cotton [2]",
    "2014: eastern basin of South Aral completely dry [2]",
    "Satellite pair: same frame, 2000 vs latest image [2]",
    "Photo: stranded ship, Moynaq, Uzbekistan",
])

# ---------- 4  MAKE & WEAR
s = prs.slides.add_slide(BLANK)
background(s, "cream")
tracker(s, {"MAKE", "WEAR"}, "oxblood")
text(s, MARGIN, 134, 1680, 120,
     [[R("Made Fast, ", "Archivo Black", 52, "oxblood"), R("Worn Little", "Archivo Black", 52, "terracotta")]],
     wrap=False, name="Title")
for lx, lab in [(MARGIN, "MAKE"), (1000, "WEAR")]:
    rule(s, lx, 285, "terracotta", 32)
    text(s, lx + 46, 272, 300, 30, [[micro(lab)]], wrap=False, name=f"Label {lab}")
photo(s, "D")
shape(s, 150, 770, 700, 104, "cream", MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12, name="Stat chip")
text(s, 178, 772, 236, 100, [[R("20%", "Anton", 54, "terracotta")]], anchor="middle", wrap=False,
     name="Chip number")
c2 = [R("textile dyeing & treatment", "Montserrat Medium", 14, "oxblood")]
text(s, 424, 793, 410, 64, [[R("of industrial water pollution:", "Montserrat Medium", 14, "oxblood")], c2],
     line=20, name="Chip text")
ref_after(s, 3, 424, 793 + 40, c2, "oxblood", size=11)
# native, editable chart
cd = CategoryChartData()
cd.categories = ["Made 2000", "Made 2015", "Worn 2000", "Worn 2015"]
cd.add_series("Index (2000 = 100)", (100, 200, 100, 64))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, E(1000), E(320), E(800), E(500), cd)
gf.name = "Chart made vs worn"
ch = gf.chart
ch.has_legend = False
ch.has_title = False
ch.font.name = "Montserrat Medium"
ch.font.size = Pt(13)
ch.font.color.rgb = RGBColor.from_string(C["oxblood"])
va = ch.value_axis
va.visible = False
va.has_major_gridlines = False
va.maximum_scale, va.minimum_scale = 230, 0
ca = ch.category_axis
ca.has_major_gridlines = False
ca.format.line.color.rgb = RGBColor.from_string(C["oxblood"])
ca.tick_labels.font.size = Pt(13)
plot = ch.plots[0]
plot.gap_width = 45
plot.has_data_labels = True
dl = plot.data_labels
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.show_value = True
dl.font.name, dl.font.size = "Anton", Pt(24)
dl.font.color.rgb = RGBColor.from_string(C["oxblood"])
ser = plot.series[0]
for idx, col in enumerate(["sun", "coral", "terracotta", "oxblood"]):
    pt_ = ser.points[idx]
    pt_.format.fill.solid()
    pt_.format.fill.fore_color.rgb = RGBColor.from_string(C[col])
    pt_.format.line.fill.background()
ser.points[1].data_label.text_frame.text = "≈200"
r_ = ser.points[1].data_label.text_frame.paragraphs[0].runs[0]
r_.font.name, r_.font.size = "Anton", Pt(24)
r_.font.color.rgb = RGBColor.from_string(C["oxblood"])
ser.points[1].data_label.position = XL_LABEL_POSITION.OUTSIDE_END
sdl = ser.data_labels
sdl.show_value = True
sdl.position = XL_LABEL_POSITION.OUTSIDE_END
sdl.font.name, sdl.font.size = "Anton", Pt(24)
sdl.font.color.rgb = RGBColor.from_string(C["oxblood"])
ca.major_tick_mark = XL_TICK_MARK.NONE
cap = [R("Twice the clothes, ", "Montserrat Medium", 22, "oxblood"),
       R("worn 36% less", "Montserrat Medium", 22, "terracotta")]
text(s, 1000, 846, 800, 40, [cap], wrap=False, name="Chart caption")
ref_after(s, 4, 1000, 846, cap, "oxblood")
corner(s, 4)
notes(s, [
    "Dyeing + treating textiles ≈ 20% of industrial water pollution [3]",
    "Clothing production ≈ doubled, 2000 → 2015 [4]",
    "Times a garment is worn: −36% in 15 yrs [4]",
    "Chart = index, 2000 = 100: made ≈200, worn 64 [4]",
    "Fast fashion: more clothes, shorter lives",
])

# ---------- 5  THROW
s = prs.slides.add_slide(BLANK)
background(s, "oxblood")
photo(s, "E")
picture(s, IMG / "grad_s5.png", 0, 0, W, H, name="Photo gradient")
tracker(s, {"THROW"}, "cream", bg="oxblood")
text(s, MARGIN, 180, 1700, 600,
     [[R("ONE TRUCK.", "Anton", 140, "cream")], [R("EVERY SECOND.", "Anton", 140, "cream")]],
     anchor="bottom", line=142, wrap=False, name="Headline")
sl = [R("of textiles landfilled or burned, worldwide", "Montserrat Medium", 24, "cream")]
text(s, MARGIN, 796, 1100, 44, [sl], wrap=False, name="Subline")
ref_after(s, 4, MARGIN, 796, sl, "cream")
chip_txt = [micro("<1% RECYCLED INTO NEW CLOTHES", "oxblood", 13)]
cw = text_width(chip_txt[0]["t"], "Montserrat Medium", 13, 13 * TRACK) + 80
shape(s, MARGIN, 864, cw, 56, "sun", MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, name="Chip")
text(s, MARGIN + 28, 864, cw - 40, 56, [chip_txt], anchor="middle", wrap=False, name="Chip text")
ref_after(s, 4, MARGIN + 28, 877, chip_txt, "oxblood", gap=4, size=11)
corner(s, 5, "cream", "cream", lbg="oxblood", rbg="oxblood")
notes(s, [
    "1 garbage truck of textiles, every second → landfill or burned [4]",
    "< 1% of clothing material recycled into new clothes [4]",
    "Worldwide figure, not one country [4]",
    "Water + dye from slides 2–4 → ends here",
])

# ---------- 6  BETTER CHOICES + CLOSING
s = prs.slides.add_slide(BLANK)
background(s, "cream")
shape(s, 0, 756, W, H - 756, "rust", name="Closing band")
sun(s, 1990, 860, 320)
for cx, title, slot, items, fill, ink, bul in [
        (120, "FAST FASHION", "F", ["Buy cheap", "Wear a few times", "Throw away"], "sand", "oxblood", "terracotta"),
        (980, "BETTER CHOICES", "G", ["Buy less, buy better", "Second-hand & repair", "Donate or recycle"],
         "terracotta", "cream", "sun")]:
    shape(s, cx, 100, 820, 630, fill, name=f"Card {title}")
    text(s, cx + 32, 124, 756, 60, [[R(title, "Archivo Black", 26, ink)]], wrap=False, name=f"Card title {title}")
    photo(s, slot)
    text(s, cx + 32, 466, 756, 240, [[R(t, "Montserrat Medium", 22, ink)] for t in items],
         bullet=bul, marL=34, line=30, space_after=10, name=f"Card list {title}")
text(s, MARGIN, 780, 1300, 150,
     [[R("Every T-shirt has a story.", "DM Serif Display", 32, "cream", italic=True)],
      [R("Let's make it a longer one.", "DM Serif Display", 32, "cream", italic=True)]],
     line=40, name="Closing quote")
text(s, 1280, 868, 520, 80, [[R("Thank you", "Dancing Script", 36, "sun")]], align="right",
     wrap=False, name="Thank you")
corner(s, 6, "cream", "cream", lbg="rust", rbg="rust")
notes(s, [
    "Buy less, buy better → more wears, reverse the −36% [4]",
    "Second-hand + repair → same shirt, longer story",
    "Donate or recycle → today < 1% becomes new clothes [4]",
    "Each extra wear spreads the 2,700 L further [1]",
    "Close: every T-shirt has a story",
])

# ---------- 7  REFERENCES
s = prs.slides.add_slide(BLANK)
background(s, "cream")
sun(s, 1830, 60, 340)
text(s, MARGIN, 110, 1200, 90, [[R("References", "Archivo Black", 44, "oxblood")]], wrap=False, name="Title")
rule(s, MARGIN, 226, "terracotta", 64)
refs = [
    [R("[1]\t"), R("World Wildlife Fund. (2014, Spring). Handle with care. "),
     R("World Wildlife Magazine", italic=True),
     R(". https://www.worldwildlife.org/magazine/issues/spring-2014/articles/handle-with-care")],
    [R("[2]\t"), R("NASA Earth Observatory. (n.d.). "), R("World of change: Shrinking Aral Sea", italic=True),
     R(". National Aeronautics and Space Administration. Retrieved October 31, 2026, from "
       "https://science.nasa.gov/earth/earth-observatory/world-of-change/aral-sea/")],
    [R("[3]\t"), R("World Bank Group. (n.d.). "),
     R("Cleaner production case study: Right first time (RFT) improvement through process optimization "
       "– Evince Textiles Limited", italic=True),
     R(". Partnership for Cleaner Textile (PaCT). https://documents1.worldbank.org/curated/en/"
       "720341627042851108/pdf/Cleaner-Production-Case-Study-Right-First-Time-RFT-Improvement-Through-"
       "Process-Optimization-Evince-Textiles-Limited.pdf")],
    [R("[4]\t"), R("Ellen MacArthur Foundation. (2017). "),
     R("A new textiles economy: Redesigning fashion’s future", italic=True),
     R(". https://www.ellenmacarthurfoundation.org/a-new-textiles-economy")],
    [R("[5]\t"), R("U.S. Department of Agriculture, Foreign Agricultural Service. (2026). "),
     R("Cotton", italic=True), R(" [Production by country, 2025/26]. Retrieved October 31, 2026, from "
                                 "https://www.fas.usda.gov/data/production/2631000")],
]
for para in refs:
    for r in para:
        r["size"] = 14
tb = text(s, MARGIN, 250, 1640, 680, refs, line=22, space_after=12, name="Reference list")
for p in tb.text_frame.paragraphs:
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(E(56)))
    pPr.set("indent", str(-E(56)))
    tabs = etree.SubElement(pPr, qn("a:tabLst"))
    t = etree.SubElement(tabs, qn("a:tab"))
    t.set("pos", str(E(56)))
    t.set("algn", "l")
WARNINGS[:] = [w for w in WARNINGS if "[1]" not in w and "[2]" not in w and "[3]" not in w
               and "[4]" not in w and "[5]" not in w]   # reference list wraps on purpose
corner(s, 7, label="REFERENCES")

prs.save(OUT)
print("saved", OUT)
for w_ in WARNINGS:
    print("WARN", w_)
