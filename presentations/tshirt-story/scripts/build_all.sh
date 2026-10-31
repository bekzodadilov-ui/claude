#!/usr/bin/env bash
# Rebuild everything: photo copies, chart, deck, preview renders.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/prepare_images.py source/photos images
python3 scripts/make_chart.py chart 2>/dev/null
python3 scripts/build_deck.py images "The-Story-of-a-T-Shirt.pptx"
# Preview render: LibreOffice clips letter-spaced text that has transparency, so the
# preview copy uses colour pre-blended to the same 60% / 40% look. The .pptx keeps real transparency.
mkdir -p build && rm -rf previews && mkdir previews
QA_FLATTEN=1 python3 scripts/build_deck.py images build/qa.pptx >/dev/null
soffice --headless --convert-to pdf --outdir build build/qa.pptx >/dev/null 2>&1
pdftoppm -r 144 -png build/qa.pdf previews/slide
ls previews
