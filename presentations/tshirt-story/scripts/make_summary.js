// Case summary: The Story of a T-Shirt (Word, A4)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType,
  WidthType, ShadingType, BorderStyle, LevelFormat, Footer, PageNumber, HeadingLevel,
} = require("docx");

const OX = "3E0E0C", TC = "C4532E", SAND = "EAD3BF", CREAM = "F4E6D8";
const FONT = "Arial";
const W = 9026; // A4 content width in DXA with 1" margins

const t = (text, o = {}) => new TextRun({ text, font: FONT, ...o });
const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 120, line: 288 }, ...o });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(text)] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(text)] });
const bullet = (runs) => new Paragraph({ numbering: { reference: "bul", level: 0 }, children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 80, line: 276 } });
const ref = (n) => t(` [${n}]`, { color: TC, size: 18 });

const border = { style: BorderStyle.SINGLE, size: 4, color: SAND };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows) {
  return new Table({
    width: { size: W, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0,
      children: r.map((c, j) => new TableCell({
        borders,
        width: { size: widths[j], type: WidthType.DXA },
        shading: i === 0 ? { fill: TC, type: ShadingType.CLEAR, color: "auto" }
                         : (i % 2 === 0 ? { fill: CREAM, type: ShadingType.CLEAR, color: "auto" } : undefined),
        margins: { top: 70, bottom: 70, left: 110, right: 110 },
        children: [new Paragraph({ children: i === 0
            ? [new TextRun({ text: c, font: FONT, bold: true, color: "FFFFFF", size: 19 })]
            : (Array.isArray(c) ? c : [t(c)]),
          spacing: { after: 0 } })],
      })),
    })),
  });
}
const cell = (text, n, o = {}) => (n ? [t(text, { size: 19, ...o }), ref(n)] : [t(text, { size: 19, ...o })]);

const refs = [
  ["World Wildlife Fund. (2014, Spring). Handle with care. ", ["World Wildlife Magazine"], ". https://www.worldwildlife.org/magazine/issues/spring-2014/articles/handle-with-care"],
  ["NASA Earth Observatory. (n.d.). ", ["World of change: Shrinking Aral Sea"], ". National Aeronautics and Space Administration. Retrieved November 4, 2026, from https://science.nasa.gov/earth/earth-observatory/world-of-change/aral-sea/"],
  ["World Bank Group. (n.d.). ", ["Cleaner production case study: Right first time (RFT) improvement through process optimization – Evince Textiles Limited"], ". Partnership for Cleaner Textile (PaCT). https://documents1.worldbank.org/curated/en/720341627042851108/pdf/Cleaner-Production-Case-Study-Right-First-Time-RFT-Improvement-Through-Process-Optimization-Evince-Textiles-Limited.pdf"],
  ["Ellen MacArthur Foundation. (2017). ", ["A new textiles economy: Redesigning fashion’s future"], ". https://www.ellenmacarthurfoundation.org/a-new-textiles-economy"],
  ["U.S. Department of Agriculture, Foreign Agricultural Service. (2026). ", ["Cotton"], " [Production by country, 2025/26]. Retrieved November 4, 2026, from https://www.fas.usda.gov/data/production/2631000"],
  ["U.S. Environmental Protection Agency. (n.d.). ", ["Textiles: Material-specific data"], ". Retrieved November 4, 2026, from https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/textiles-material-specific-data"],
  ["European Environment Agency. (n.d.). ", ["EU exports of used textiles in Europe’s circular economy"], ". Retrieved November 4, 2026, from https://www.eea.europa.eu/en/analysis/publications/eu-exports-of-used-textiles"],
  ["European Environment Agency. (n.d.). ", ["What happens to our used textile products such as discarded clothing or shoes?"], " Retrieved November 4, 2026, from https://www.eea.europa.eu/en/about/contact-us/faqs/what-happens-to-our-used-textile-products-such-as-discarded-clothing-or-shoes"],
  ["European Environment Agency. (n.d.). ", ["Circularity of the EU textiles value chain in numbers"], ". Retrieved November 4, 2026, from https://www.eea.europa.eu/en/analysis/publications/circularity-of-the-eu-textiles-value-chain-in-numbers"],
];

const doc = new Document({
  creator: "Bekzodjon Kirgizbayev",
  title: "The Story of a T-Shirt – Case Summary",
  styles: {
    default: { document: { run: { font: FONT, size: 21, color: OX } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { font: FONT, size: 44, bold: true, color: OX }, paragraph: { spacing: { before: 0, after: 60 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 28, bold: true, color: TC }, paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 23, bold: true, color: OX }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 400, hanging: 260 } }, run: { color: TC } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [t("Bekzodjon Kirgizbayev · SUST 1000 7T · page ", { size: 16, color: "8A6A64" }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "8A6A64" })] })] }) },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [t("The Story of a T-Shirt"), t(": From Field to Landfill", { color: TC })] }),
      p([t("Case summary · SUST 1000 7T · The Story of Your Own Stuff (EPA Ireland)", { size: 19 })], { spacing: { after: 40 } }),
      p([t("Bekzodjon Kirgizbayev · Presented 03.11.2026", { size: 19 })], {
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: TC, space: 6 } }, spacing: { after: 200 } }),

      h1("1. The case in brief"),
      p([t("I followed one ordinary cotton T-shirt through its whole life (grow, make, wear, throw), told from the point of view of Uzbekistan, one of the world’s main cotton countries. The shirt looks simple, but it carries a large hidden cost: a lot of water to grow, one of the world’s worst environmental disasters (the Aral Sea), heavy water pollution in dyeing, and a very short life before most clothing is landfilled or burned. The key message: the longer we keep and reuse a T-shirt, the smaller its footprint per wear.")]),

      h1("2. The life cycle in numbers"),
      table([1500, 5426, 2100], [
        ["Stage", "Key fact", "Source"],
        [cell("Grow", 0, { bold: true }), cell("About 2,700 litres of water are needed to make one cotton T-shirt, roughly what one person drinks in 2.5 years."), cell("WWF", 1)],
        [cell("Grow", 0, { bold: true }), cell("Uzbekistan is the world’s 7th-largest cotton producer (≈2.8% of world output, 2025/26)."), cell("USDA FAS", 5)],
        [cell("Grow", 0, { bold: true }), cell("The Aral Sea, once one of the four largest lakes in the world, shrank after the Amu Darya and Syr Darya were diverted to irrigate cotton; its eastern basin first dried out completely in 2014."), cell("NASA EO", 2)],
        [cell("Make", 0, { bold: true }), cell("Textile dyeing and treatment cause about 20% of industrial water pollution."), cell("World Bank", 3)],
        [cell("Wear", 0, { bold: true }), cell("Clothing production roughly doubled in 15 years (2000–2015), while the number of times a garment is worn fell by 36%."), cell("EMF", 4)],
        [cell("Throw", 0, { bold: true }), cell("The equivalent of one garbage truck of textiles is landfilled or burned every second."), cell("EMF", 4)],
      ]),

      h1("3. End of life: what really happens to a T-shirt"),
      p([t("No official source publishes end-of-life figures for cotton T-shirts alone. The numbers below are for all clothing (or all textiles), which includes T-shirts. They answer three questions: how much is recycled, how much is reused, and how it is reused.", { italics: true })]),

      h2("How much is recycled? (global)"),
      table([5426, 1800, 1800], [
        ["Where clothing material ends up (world, 2015)", "Share", "Source"],
        [cell("Landfilled or incinerated"), cell("73%", 0, { bold: true }), cell("EMF", 4)],
        [cell("Recycled into lower-value products (“cascaded”): insulation, wiping cloths, mattress stuffing"), cell("12%", 0, { bold: true }), cell("EMF", 4)],
        [cell("Recycled into new clothing (closed loop)"), cell("< 1%", 0, { bold: true }), cell("EMF", 4)],
      ]),
      p([t("So even when clothes are “recycled”, they are almost never turned back into new clothes. Most recycling is downcycling.")], { spacing: { before: 120, after: 120 } }),

      h2("Example: the United States (clothing & footwear, 2018)"),
      table([5426, 1800, 1800], [
        ["Fate", "Amount", "Share"],
        [cell("Generated as waste"), cell("13.0 million t"), cell("100%")],
        [cell("Recycled"), cell("1.7 million t"), cell("13%", 0, { bold: true })],
        [cell("Burned with energy recovery"), cell("2.2 million t"), cell("≈17%", 0, { bold: true })],
        [cell("Landfilled"), cell("9.1 million t"), cell("≈70%", 0, { bold: true })],
      ]),
      p([t("Source: US EPA"), ref(6), t(". The EPA has no estimate for reuse (donations, second-hand shops), because reuse happens before an item becomes waste.")], { spacing: { before: 120, after: 120 } }),

      h2("How much is reused? (Europe)"),
      bullet([t("An average European throws away about "), t("16 kg", { bold: true }), t(" of textiles per year; only about "), t("one quarter (4.4 kg)", { bold: true }), t(" is collected separately for reuse and recycling. The rest goes into mixed household waste."), ref(9)]),
      bullet([t("Of the clothes people donate, only about "), t("10% are resold in the same country", { bold: true }), t(" and another "), t("10% in other EU countries", { bold: true }), t(". Most of the rest is exported to Africa and Asia."), ref(8)]),
      bullet([t("EU exports of used textiles "), t("tripled in two decades to almost 1.7 million tonnes", { bold: true }), t(" (2019): "), t("46% went to Africa and 41% to Asia", { bold: true }), t("."), ref(7)]),

      h2("How is it reused?"),
      bullet([t("Second-hand at home: ", { bold: true }), t("charity and second-hand shops resell the best items locally."), ref(8)]),
      bullet([t("Second-hand abroad: ", { bold: true }), t("in Africa, imported clothes mainly go to local second-hand markets, where there is demand for cheap used clothes. What cannot be sold often ends up in open landfills or informal waste streams."), ref(8)]),
      bullet([t("Sorting and downcycling: ", { bold: true }), t("in Asia, used textiles are mostly downcycled into industrial rags or filling, or re-exported for recycling or for reuse in Africa."), ref(8)]),
      bullet([t("Cascaded recycling: ", { bold: true }), t("worn-out cotton is shredded into insulation, wiping cloths and mattress stuffing (12% of clothing material worldwide)."), ref(4)]),
      bullet([t("Closed loop: ", { bold: true }), t("turning an old T-shirt back into fibre for a new one happens to less than 1% of clothing material."), ref(4)]),
      p([t("The EEA stresses that what happens to exported textiles is highly uncertain.", { italics: true }), ref(7)], { spacing: { before: 80, after: 120 } }),

      h1("4. Better choices"),
      bullet([t("Buy less, buy better: ", { bold: true }), t("more wears per shirt spread the 2,700 litres over a longer life.")]),
      bullet([t("Second-hand & repair: ", { bold: true }), t("keeping a shirt in use is better than any form of recycling.")]),
      bullet([t("Donate or recycle properly: ", { bold: true }), t("only clean, wearable items help second-hand markets; worn-out cotton should go to textile recycling, not general waste.")]),

      h1("References"),
      ...refs.map((r, i) => new Paragraph({
        indent: { left: 567, hanging: 567 }, spacing: { after: 100, line: 264 },
        children: [t(`[${i + 1}]\t`, { size: 18 }), t(r[0], { size: 18 }), t(r[1][0], { size: 18, italics: true }), t(r[2], { size: 18 })],
        tabStops: [{ type: "left", position: 567 }],
      })),
      p([t("Note: figures were checked against each publisher’s own website via search; please open the links once to confirm before submission.", { size: 16, italics: true, color: "8A6A64" })], { spacing: { before: 120 } }),
    ],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[2], b); console.log("written", process.argv[2]); });
