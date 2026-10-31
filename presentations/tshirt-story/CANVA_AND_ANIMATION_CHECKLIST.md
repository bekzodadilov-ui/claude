# Canva import + animation checklist

## A. Import (Canva could not be reached from the build sandbox)
- [ ] Canva → **Create → Import file** (or drag `The-Story-of-a-T-Shirt.pptx` onto the Canva home page).
- [ ] Check the fonts. All of these exist in Canva: Anton, Archivo Black, DM Serif Display (italic), Dancing Script, Montserrat. If a text box shows "Montserrat Medium" as missing, select it → Montserrat → **Medium**.
- [ ] Check the **transparency**. Corner info (bottom) should be **60%**, and inactive stage-tracker words and dots (slides 2–5) **40%**. If Canva imported them at full strength, select them → Transparency → 60 / 40.
- [ ] Slide 3: drop the two NASA images into the sand placeholders (same size, so 1:1). Set the second year to the actual latest year if it isn't 2018.
- [ ] Slide 5: replace the sand placeholder with a clothing-landfill photo (landscape, ≥1920×1080). Then **Position → Backward** until it sits under the dark gradient.
- [ ] Slide 1: replace the T-shirt photo with the licensed (un-watermarked) version.
- [ ] Slide 4 chart: if Canva turns the native chart into a static image, delete it and rebuild with **Elements → Charts → Bar**, using the data below. Or place `chart/chart_made_vs_worn.png` (transparent).

**Chart data** (index, 2000 = 100, source [4]):

| Bar | Value | Colour |
|---|---|---|
| Clothes made · 2000 | 100 | #F2A65A |
| Clothes made · 2015 | ≈200 | #E5845F |
| Times each item is worn · 2000 | 100 | #C4532E |
| Times each item is worn · 2015 | 64 | #3E0E0C |

## B. Transitions
- [ ] 1 → 2: **Match & move** (the sun circle is the same element: it moves and resizes, solid → 45% opacity).
- [ ] All other transitions: **Dissolve**.

## C. Never animate
- [ ] Corner info, stage tracker (+ underlines), reference numbers. Each is its own text box, so leave them static.

## D. Element animations (calm, slow; no Bounce / Tumble / Pop)
- [ ] **S1:** headline → Rise (by word) · sun circle → Fade · photo → Pan (slow) · details block → Fade
- [ ] **S2:** "2,700" → Ascend · label "LITRES OF WATER…" → Baseline · photo + sand frame → Fade
- [ ] **S3:** left photo → Breathe (slow zoom) · headline → Clarify · then before image → Fade · then after image → Fade
- [ ] **S4:** left half (photo) → Fade · stat chip ("20%" + text + chip shape) → Baseline · then chart → Rise
- [ ] **S5:** photo → Breathe · headline → Typewriter · chip → Fade
- [ ] **S6:** left card → Shift (from left) · right card → Shift (from right) · then quote → Ascend · "Thank you" → Fade
- [ ] **S7:** no animation

Tip: on S4 and S6, group each card's or chip's pieces (shape + text + photo) before animating, so they move as one.
