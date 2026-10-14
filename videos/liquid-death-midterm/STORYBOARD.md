---
format: 1920x1080
duration: 6m25s
message: "Liquid Death did not create the need for water. It changed the meaning associated with buying water."
arc: Hook → Category baseline → Brand reveal → Mechanism → Consumer shift → Meaning change → Critical reflection → Thesis close → References
audience: University marketing professor and students (midterm)
mode: collaborative
---

# Liquid Death — How Marketing Made Water Cool · storyboard v1

## Decisions

- **Message:** Liquid Death changed what buying water *means*, not the need for water.
- **Format:** 1920×1080, about 6:10 of content plus a 15 s reference card (6:25 total).
  Voice: **live narration by the presenter** (script in NARRATION.md). On-screen text is
  short and carries the argument's skeleton; the narration carries the detail.
  Music: a restrained, synthesized instrumental bed with sparse SFX.
- **Spine:** *the evidence tag.* Every claim on screen wears a small mono chip
  (`VERIFIED FACT` silver · `COMPANY CLAIM` dark-red outline · `ANALYSIS` white outline)
  plus a one-line source. It keeps the film a documentary rather than an advert,
  and it delivers the brief's fact/claim/interpretation split visually.
- **Hero prop:** a tall black can, drawn in code (no real logo artwork: the wordmark is
  set in type, and the skull is an abstract silver mark). It appears in S1, S3, S5, S6 and S8.
  S8 is the callback to S1's slow push.
- **Palette:** bg `#0C0C0E` charcoal-black · panel `#17181B` · ink `#ECEBE7` ·
  silver `#A7ABB1` (metallic gradient on the can only) · accent dark red `#9E1C20`,
  used on ≤1 element per frame · S7 drops red entirely (grayscale).
- **Type:** League Gothic (condensed display, all caps) for statements ·
  Montserrat 400/700 for body · IBM Plex Mono for tags, sources and labels.
  Three registers: statement / explanation / evidence.
- **Texture:** grain overlay (registry `grain-overlay`) at low strength on every frame;
  a radial spotlight on the can; no full-screen linear gradients.
- **Glitch budget:** two uses only (S1 → S2 cut, S4 entry), registry `rgb-glitch-text`.
- **Seams:** one direction rule. Content exits left; slow crossfade-to-black between acts;
  hard cuts only inside S4's montage.
- **Held frame:** S8 "IT SELLS MEANING.": 4 s with nothing moving.
- **Bans:** no imitation of real ads or footage, no fake product photos, no invented
  numbers, quotes or testimonials, no "everyone/all customers", no causal arrows
  without the "conceptual model" label, no slideshow (each scene keeps one persistent
  object), no screensaver motion (every move points at a claim).
- **Truthfulness line:** the can is an illustration; ads are cited as text cards,
  not reproduced. Facts are listed in SOURCES.md.

## Locked

The user said "do everything as you see fit", so the recommended defaults were taken:

- Plan v1 approved as written; the sketch pass was skipped and the build went straight from the plan.
- INSEAD case not found; the St. Gallen 2024 teaching case is used instead (swap it if the INSEAD reference turns up).
- Music: procedural bed + SFX (tools/make-music.mjs), about −28.5 LUFS integrated so it sits under a live voice.
- Length: 6:25, with the references card after the 6:10 conclusion.

## Build notes (changes from v1)

- S4 Q3 card 4 retitled "Back-sweat taste test · 2023" so it fits the panel.
- S6 milestone spacing tightened so the pan ends on 2022–2024 fully in frame.
- References list grew to 14 (Modern Retail added for the 2022/2023 expansion dates).

## Frame 1 — Hook (0:00–0:35, 35s)

- scene: "IT'S JUST WATER." → plain bottle in flat light → black can in a spotlight → "THEN WHY DOES IT LOOK LIKE THIS?"
- duration: 35s
- transition_in: cut
- src: compositions/s1-hook.html
- status: animated
- motion: kinetic-type-beats (statement build) + titlecard-reveal (held question); slow push-in on the can

Beats: 0–3 s black. 3–8 s "IT'S JUST WATER." types in white, centered (the one centered
statement, deliberately). 8–14 s a generic clear plastic bottle silhouette on a flat light-grey
field (bright, clinical). 14 s hard cut to black. 14.5–24 s the tall black can rises into a top-down
spotlight, slow 1.00→1.06 push; a metallic hit at 14.5 s. 24 s "THEN WHY DOES IT LOOK LIKE THIS?"
slams in (League Gothic, 150 px, headline-slam) left-anchored. 29–35 s the question line holds and the
sub-line fades in: "How can marketing make an ordinary product feel culturally different?" (Montserrat).
Seam out: brief RGB glitch on the type (glitch use 1 of 2), then cut. No logo artwork, no tagline yet.
Why: the hook asks the exam question in outcome language.

## Frame 2 — Before the brand (0:35–1:15, 40s)

- scene: a desaturated shelf of near-identical bottle silhouettes; four category words
- duration: 40s
- transition_in: cut
- src: compositions/s2-category.html
- status: animated
- motion: grid-card-assemble (shelf builds in staggered cascade) + slow lateral parallax

Beats: 0–10 s a shelf of ~24 bottle silhouettes in three rows assembles left→right, desaturated,
slow parallax drift (front row faster). 10–30 s four words appear one per ~5 s on a right-hand rail:
"HYDRATION" "PRICE" "AVAILABILITY" "PACKAGING", each with a one-line Montserrat gloss
("the functional need", "the everyday trade-off", "where it is sold", "how it looks on the shelf").
30–40 s caption at bottom: "The need already existed. Brands competed for attention." + ANALYSIS tag;
small mono footnote: "Simplified. Many water brands already used distinctive marketing."
Seam out: shelf dims to black, leftward.
Constraint: silhouettes vary slightly in height and cap (no claim that brands were identical).
Why: sets the baseline that the need predates the brand.

## Frame 3 — Introducing Liquid Death (1:15–2:00, 45s)

- scene: spotlight reveal of the can; close-up crops; CONVENTIONAL vs LIQUID DEATH value contrast
- duration: 45s
- transition_in: crossfade
- src: compositions/s3-reveal.html
- status: animated
- motion: logo-assemble-lockup (wordmark set letter-by-letter on the can) → comparison-split

Beats: 0–8 s darkness, then a spotlight cone opens on the can (silver rim light).
8–20 s three macro crops (parallax): tall-can top rim · condensed wordmark "LIQUID DEATH" ·
abstract skull mark. Label chips in mono: "TALL ALUMINUM CAN" "HEAVY-METAL TYPOGRAPHY" "SKULL ICONOGRAPHY".
20–28 s fact card bottom-left: "Founded by Mike Cessario · first cans sold 2019"
[VERIFIED FACT · BeverageDaily 2024; TechCrunch]. 28–45 s comparison-split: left panel
"CONVENTIONAL WATER BRANDING → PURITY · NATURE · FRESHNESS" (cool grey), right panel
"LIQUID DEATH BRANDING → REBELLION · HUMOR · ATTITUDE" (one red rule under it); bottom line
"Not a new liquid. A new identity around it." [ANALYSIS].
Constraint: no reproduced logo art. Why: names the differentiator: identity, not product.

## Frame 4 — How the marketing works (2:00–3:00, 60s)

- scene: 2×2 quadrant grid, each quadrant animates in turn; connecting chain below
- duration: 60s
- transition_in: cut (glitch use 2 of 2)
- src: compositions/s4-mechanism.html
- status: animated
- motion: grid-card-assemble (quadrants) + fast hard-cut montage in Q3 + arrow draw-on chain

Beats (energy up, music rises): 0–4 s four quadrant frames draw on (hairline silver).
4–14 s Q1 VISUAL DIFFERENTIATION: the black can beside a light bottle silhouette.
14–24 s Q2 SHOCK AND HUMOR: "MURDER YOUR THIRST" kinetic slam [COMPANY CLAIM · slogan].
24–40 s Q3 ENTERTAINMENT-FIRST CONTENT: a fast hard-cut montage of evidence cards, ~3 s each:
"SUPER BOWL LVI · 2022 · kids 'chug' tallboys — 'Don't be scared. It's just water.'" ·
"GREATEST HATES · 2020 · a metal album made from hate comments" ·
"MARTHA STEWART · 2022 · Halloween collaboration" · "BETTER THAN BACK SWEAT? · 2023 · blind taste test"
(each card = [VERIFIED FACT · outlet, year]). 40–48 s Q4 IDENTITY AND CULTURE: abstract
concert-light silhouettes (crowd shapes, stage beams) with the can in hand; no faces, no quotes.
48–60 s quadrants shrink up; chain draws left→right below:
"PACKAGING → ATTENTION → BRAND RECALL → POSSIBLE PURCHASE PREFERENCE", labelled
"CONCEPTUAL MODEL: not a proven causal sequence" [ANALYSIS].
Why: the mechanism, i.e. how meaning is built.

## Frame 5 — The consumer behavior shift (3:00–3:50, 50s)

- scene: BEFORE/AFTER speech-line comparison; the can with four orbiting words
- duration: 50s
- transition_in: crossfade
- src: compositions/s5-consumer.html
- status: animated
- motion: kinetic-type-beats (line extends) + constellation-hub (words settle around the can)

Beats: 0–14 s left: "BEFORE" / "I need water." Right: "AFTER" / "I need water, and I prefer a brand
that reflects my personality." The AFTER line extends from the BEFORE line (the first clause is
shared and the second clause writes on), showing that the need stays and meaning is added.
14–20 s an arrow "FUNCTIONAL PRODUCT → SYMBOLIC PRODUCT". 20–40 s the can centers; four words
spring to a ring: "IDENTITY" "HUMOR" "SELF-EXPRESSION" "CULTURAL ASSOCIATION", slow orbit.
40–50 s caption: "A plausible mechanism — not how every customer thinks." [ANALYSIS] +
"Symbolic consumption: products valued for what they signal" (concept label).
Why: the consumer-psychology core of the argument.

## Frame 6 — What changed? (3:50–4:35, 45s)

- scene: can transforms container → lifestyle object; equation diagram; thesis line; milestone rail
- duration: 45s
- transition_in: crossfade
- src: compositions/s6-meaning.html
- status: animated
- motion: kinetic-type-beats (equation build) + spatial-pan-stations (milestone rail)

Beats: 0–8 s the can's flat grey outline fills to black-and-silver (container → object).
8–20 s equation: "FUNCTIONAL VALUE + BRAND IDENTITY + ENTERTAINMENT" builds term by term.
20–28 s held line, large: "THE PRODUCT REMAINS WATER. THE PERCEIVED MEANING CHANGES."
28–45 s milestone rail pans left→right: "2019 first cans sold" · "2022 flavored sparkling" ·
"2023 iced tea · $263M retail sales (reported)" · "2024 valued at $1.4B (reported)", each
[VERIFIED FACT · source]. Footnote: "Reported figures; no market-share claims."
Why: differentiation that turned into business scale, stated with sourced milestones only.

## Frame 7 — Critical ethical reflection (4:35–5:40, 65s)

- scene: grayscale, slow; three questions; benefits vs concerns; aluminum lifecycle strip
- duration: 65s
- transition_in: slow fade through black (2 s)
- src: compositions/s7-ethics.html
- status: animated
- motion: titlecard-reveal chain (questions) → comparison-split → lifecycle arrows draw on

Beats (music drops low, no red anywhere): 0–21 s three questions, one at a time (~7 s each), serif-free
League Gothic in light grey: "1 · ARE CONSUMERS PAYING FOR THE PRODUCT OR ITS IMAGE?"
"2 · WHEN DOES EMOTIONAL PERSUASION BECOME MANIPULATION?"
"3 · DOES RECYCLABLE PACKAGING AUTOMATICALLY MEAN SUSTAINABILITY?"
21–40 s two columns: POTENTIAL BENEFITS (Creative differentiation · Entertaining advertising ·
A distinctive non-alcoholic beverage identity) | POTENTIAL CONCERNS (Paying a premium for brand
symbolism · Emotional influence on purchasing decisions · Environmental claims requiring independent evidence).
40–58 s lifecycle strip: "COLLECTION → RECYCLING → MANUFACTURING → TRANSPORT → DISPOSAL" with
"'Infinitely recyclable'" [COMPANY CLAIM] above it and "US 2018: 50.4% of aluminum beverage cans
recycled" [VERIFIED FACT · U.S. EPA] below it; small line: "Cans also carry a thin plastic liner"
[Packaging Digest]. 58–65 s "Recyclable ≠ automatically sustainable. Not inherently unethical,
but claims need evidence." [ANALYSIS].
Why: balanced critique that keeps facts and interpretation apart.

## Frame 8 — Conclusion (5:40–6:10, 30s)

- scene: callback to S1: can on black, slow zoom-out; two-line thesis; final question
- duration: 30s
- transition_in: slow fade through black
- src: compositions/s8-close.html
- status: animated
- motion: zoom-out (can recedes into darkness) + kinetic-type-beats + held frame

Beats: 0–8 s the can, 1.10→0.85 zoom-out, spotlight narrows. 8–13 s "MARKETING DOESN'T JUST SELL PRODUCTS."
13–17 s held black beat (nothing moves). 17–21 s "IT SELLS MEANING." (red rule beneath: the last red).
21–30 s "ARE WE BUYING WHAT A PRODUCT DOES — OR WHAT IT REPRESENTS?" holds, then fades to black.
Why: restates the thesis and returns the question to the audience.

## Frame 9 — References (6:10–6:25, 15s)

- scene: two-column reference list in IBM Plex Mono on black, slow upward drift
- duration: 15s
- transition_in: fade from black
- src: compositions/s9-references.html
- status: animated
- motion: titlecard-reveal (one move: slow rise)

13 references from SOURCES.md, plus "Can and ads shown as illustrations; no brand footage used."
