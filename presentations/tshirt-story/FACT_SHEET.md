# Fact sheet: The Story of a T-Shirt

Every number in the deck comes from these five sources. Numbers in brackets match the small reference numbers on the slides and the References slide.

**How the facts were checked:** the sandbox's network policy blocked direct page loads for all five publishers (worldwildlife.org, nasa.gov, worldbank.org, ellenmacarthurfoundation.org, usda.gov). Each fact was confirmed through web-search results limited to that publisher's own domain, which return the page's own text. Before you submit, **open each URL once** and check the wording yourself (marked ☐).

| # | Fact | Number used | Ref | Where it is stated | ☐ |
|---|---|---|---|---|---|
| 1 | Water to grow the cotton for one T-shirt | **2,700 L** (713 gal) | [1] | WWF, *World Wildlife Magazine*, Spring 2014, "Handle with Care": https://www.worldwildlife.org/magazine/issues/spring-2014/articles/handle-with-care | ☐ |
| 2 | Drinking-water comparison | ≈ one person's needs for **~900 days ≈ 2.5 years** | [1] | same page. The search index paraphrased this line, so confirm it says *drinking* water | ☐ |
| 3 | Uzbekistan's rank | **7th-largest** cotton producer, **2.8%** of world output, ≈3.45 M bales (2025/26) | [5] | USDA FAS, Cotton production by country: https://www.fas.usda.gov/data/production/2631000 (ranking updates monthly) | ☐ |
| 4 | Aral Sea's former size | once one of the world's **4 largest** lakes | [2] | NASA Earth Observatory, *World of Change: Shrinking Aral Sea*: https://science.nasa.gov/earth/earth-observatory/world-of-change/aral-sea/ (old URL: earthobservatory.nasa.gov/world-of-change/AralSea) | ☐ |
| 5 | Cause | 1960s Soviet diversion of the **Amu Darya & Syr Darya** to irrigate cotton | [2] | same page | ☐ |
| 6 | Eastern basin | eastern lobe of the South Aral **completely dry in 2014** | [2] | same page | ☐ |
| 7 | Satellite series | starts **2000**; latest image **2018** (confirmed) | [2] | same page.  | ☐ |
| 8 | Textile dyeing | dyeing & treatment ≈ **20%** of industrial water pollution | [3] | World Bank / PaCT, *Cleaner Production Case Study: RFT Improvement… Evince Textiles*: https://documents1.worldbank.org/curated/en/720341627042851108/pdf/Cleaner-Production-Case-Study-Right-First-Time-RFT-Improvement-Through-Process-Optimization-Evince-Textiles-Limited.pdf | ☐ |
| 9 | Clothing production | approximately **doubled** in 15 years (2000 → 2015) | [4] | Ellen MacArthur Foundation (2017), *A New Textiles Economy*: https://www.ellenmacarthurfoundation.org/a-new-textiles-economy | ☐ |
| 10 | Wears per garment | utilisation down **36%** vs 15 years earlier | [4] | same report | ☐ |
| 11 | Landfill / burning | **one garbage truck** of textiles every **second** | [4] | same report | ☐ |
| 12 | Recycling | **< 1%** of clothing material recycled into new clothing | [4] | same report | ☐ |

## Dropped (not supported by the 5 sources)
- **Aral Sea surface area in the two satellite years.** NASA's World of Change page gives no km² figure for specific years, so I replaced it with verified captions ("eastern basin still holds water" / "dry since 2014").
- **"88% of area / 92% of volume lost since 1960."** This is real NASA EO text (a Philip Micklin quote), but it's on a *different* EO article. Adding it would make a 6th reference.
- **"Clothing production doubled 2000–2014."** The report's wording is "the last 15 years" with data to 2015, so the deck uses 2000 → 2015.

## Satellite images (in the deck: your NASA EO screenshots, aligned and cropped identically)
Usage: NASA Earth Observatory images are free to reuse with credit. The slide credits "IMAGES: NASA EARTH OBSERVATORY".
1. Open https://science.nasa.gov/earth/earth-observatory/world-of-change/aral-sea/
2. Download the full-size **2000** image and the **latest-year** image from the series slider.
3. Optional: `python3 scripts/prepare_aral.py <2000.jpg> <latest.jpg> images` crops both identically (no warm tone), then run `scripts/build_all.sh` to drop them into slide 3. Or, in Canva, drag each into its placeholder: both frames are the same size, so they compare 1:1.
