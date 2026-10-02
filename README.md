# Badge Maker

Generate printable **A4 sheets of name badges** — organization logo plus each
person's name — straight from your browser. No server, no sign-up, no upload of
your name list anywhere: everything runs locally in the page.

**→ https://parzival3.github.io/badge-maker/**

## How to use it

1. Paste your names into the box, one per line. Add a role after a comma:

   ```
   Jane Doe, Volunteer
   Ram Thapa
   Sita Gurung, Coordinator
   ```

   …or upload a spreadsheet (`.xlsx`, `.xls`, `.csv`, `.ods`) instead — see below.

2. Pick the badge size:

   | Size | Per sheet | Grid | Sheet margins |
   |---|---|---|---|
   | 85 × 54 mm | 10 | 2 × 5 | 20 mm sides, 13.5 mm top/bottom |
   | 90 × 54 mm | 10 | 2 × 5 | 15 mm sides, 13.5 mm top/bottom |
   | 70 × 37 mm | 24 | 3 × 8 | **none at the sides**, 0.5 mm top/bottom |
   | Custom | your choice | your choice | calculated and shown as you type |

   The 70 × 37 preset suits A4 sticker sheets cut 3 × 8 edge to edge: three
   70 mm columns span the full 210 mm exactly, and eight 37 mm rows leave
   0.5 mm top and bottom. **Custom** takes a width, height, column and row
   count, reports the resulting margins, and warns you if the grid will not
   fit on A4.

3. Set a **Top margin** if the first row comes out clipped. Left blank, the
   grid is centred on the sheet. Given a number, the grid hangs from that
   margin instead — the fix when a dense grid pushes the top row into the strip
   your printer physically cannot reach, which on most inkjets and lasers is
   the outer 3–5 mm of the paper. The margins in use are shown under the box as
   you type.

   Note that this moves *everything* down, so you lose at the bottom what you
   gain at the top. On a pre-cut sticker sheet the printing must line up with
   the die, so if the top row cannot be printed in full, the answer is a
   shorter badge height (which shifts content inward on every sticker), not a
   top margin.

4. Click **Print / Save as PDF**.

5. Cut along the dashed lines. Badges are laid out edge to edge, so each cut
   line is shared between two badges — one pass of the guillotine per line.

### Print settings

The page declares the paper and margins itself
(`@page { size: A4 portrait; margin: 0 }`), so the browser defaults are already
correct — verified by printing with headers, footers and background graphics
left at their defaults, which produces byte-identical geometry.

The one setting a web page is not allowed to control is **Scale**. It defaults
to 100 %, but if it ever reads "Fit to page" the whole sheet shrinks by a few
percent and the badges stop matching your badge holders.

So each sheet prints a **100 mm reference bar** at its foot. Hold a ruler
against it once: if it measures 100 mm, every badge on the sheet is correct.
Untick "Print a 100 mm scale check" to leave it off.

## Spreadsheet format

The **first sheet** of the file is read.

- If the first row contains a header cell matching `Name` (or `Full Name`,
  `Nome`, `Nom`, `Naam`), that column is used for names, and a column headed
  `Role` / `Title` / `Position` / `Department` / `Team` is used for the second
  line.
- Otherwise column **A** is the name and column **B** the role.

Loaded rows are written into the text box, so you can edit them before printing.

## Swapping the logo

Replace `assets/logo.svg` with your own file and commit. Keep it an SVG (or a
transparent PNG named `logo.svg`'s replacement — then update the `src` in
`js/app.js` and the `<link rel="icon">` in `index.html`). A wide, horizontal
logo works best; it is scaled to fit 52 × 12 mm at the top of each badge.

The badge text colour is `--brand` style `#123f6b` in `css/print.css`
(`.badge-name`) — change it to match your own logo.

## Caveats

- A name containing a comma (`Doe, Jane`) is split into name + role. Use the
  spreadsheet upload for those; commas in the name column are stripped there.
- Long names shrink to fit and wrap across lines when that buys a larger size.
  On a dense sheet this can leave near-identical names on different line counts,
  because a name containing a `1` is narrower than one without. Tick **Keep
  every name on one line** to shrink instead of wrap and level every badge to a
  single size — worth it at 24 per sheet.
- The 100 mm scale check needs a bottom margin to sit in, so it is unavailable
  at sizes whose grid reaches the edge of the sheet, such as 70 × 37 mm.

## Other assets in this repo

### `assets/nkfmh-logo.svg`

The Nepal Korea Friendship Municipality Hospital emblem, as vector. Traced from
a 2048 px raster: the flat artwork comes from an auto-trace, while the three
gradient regions (the sky-to-earth disc, the lotus petals and the crown) are
hand-authored SVG gradients, since tracers flatten gradients to a single muddy
colour. Verified by sampling matching pixels against the original — the petal
ramp matches to within a couple of RGB units. Transparent background.

Note the ring text is outlines, not live type, so it cannot be re-set. If the
hospital can supply their original vector file, prefer it over this trace.

### `banner/`

An 8 × 4 ft (2438.4 × 1219.2 mm) flex banner for the PNC home visit nurses
training, built from both logos.

- `pnc-training-banner-8x4ft.svg` — the artwork, 1 user unit = 1 mm
- `build-banner.py` — regenerates it from the two logos in `assets/`

```sh
python3 banner/build-banner.py                 # rewrites the SVG in place
rsvg-convert -f pdf -o banner.pdf banner/pnc-training-banner-8x4ft.svg
```

Fonts: **Inter** and **Noto Sans Devanagari**. Both must be installed for the
text to render; export to PDF (fonts embedded) before sending to a printer.

The Nepali date on the banner, आश्विन १८–२१, २०८३, is 4–7 October 2026
converted to Bikram Sambat and cross-checked with two independent libraries.
The Nepali title (सुत्केरी गृहभ्रमण नर्स तालिम) is a draft and should be
confirmed by a Nepali speaker before printing.

## Development

Static files, no build step:

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

| Path | What it is |
|---|---|
| `index.html` | the whole UI |
| `css/print.css` | A4 geometry and badge layout — the file that defines the printed result |
| `css/app.css` | on-screen controls and preview chrome |
| `js/app.js` | parsing, rendering, auto-shrink, localStorage |
| `js/vendor/xlsx.full.min.js` | [SheetJS](https://sheetjs.com), vendored so the page works offline |
| `assets/logo.svg` | the organization logo |

### Tests

Open `test/parse-test.html` in a browser (or
`firefox --headless --screenshot out.png test/parse-test.html`) — it exercises the
line and spreadsheet parsers and prints a pass/fail list.

## Changing the badge size / adding a label-sheet preset

For a one-off, use **Custom** in the page. To add a permanent preset, two edits:

1. **`js/app.js`** — an entry in the `SIZES` table:
   ```js
   '99x57': { w: 99.1, h: 57, cols: 2, rows: 5 },
   ```
2. **`index.html`** — a matching `<option value="99x57">` in the size `<select>`.

The grid is centred on the sheet, so the margins follow from the arithmetic and
there is nothing else to set.

**Die-cut label sheets are the exception.** They have a gap between labels as
well as a margin, which this layout does not model — it tiles badges edge to
edge. Supporting them needs a `gap` and an explicit `padding` on `.sheet` in
`css/print.css`, plus switching `justify-content` / `align-content` from
`center` to `start` so the grid anchors to the margin printed on the pack.

Verify any new size by printing to PDF and measuring, not by eye:

```sh
chromium --headless --no-pdf-header-footer --print-to-pdf=out.pdf index.html
pdfinfo out.pdf          # must say 594.96 x 841.92 pts (A4)
pdftotext -bbox out.pdf -  # compare word positions between columns/rows
```
