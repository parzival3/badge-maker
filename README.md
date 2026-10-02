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

2. Pick the badge size: **85 × 54 mm** (credit-card size) or **90 × 54 mm**.
   Either way you get **10 badges per A4 sheet**, in 2 columns × 5 rows.

3. Click **Print / Save as PDF**.

4. Cut along the dashed lines. Badges are laid out edge to edge, so each cut
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
- Long names are automatically shrunk to fit (down to 8 pt) rather than wrapped.

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

The current sizes assume **full-sheet** paper or sticker paper that you cut
yourself: badges are laid out edge to edge with no gaps, centred on the page.
Die-cut label sheets (Avery and similar) instead have a fixed sheet margin
*and* a gap between labels, so they need those numbers too.

To add a size, three edits:

1. **`index.html`** — another radio next to the existing ones:
   ```html
   <label><input type="radio" name="size" value="99"> 99.1 × 57 mm</label>
   ```
2. **`css/print.css`** — the matching dimensions. The class name is
   `size-` plus the radio's `value`; `app.js` puts it on `<body>`:
   ```css
   .size-99 .sheet { --bw: 99.1mm; --bh: 57mm; }
   ```
   For a die-cut sheet, also set the sheet padding and grid gap for that size,
   e.g. `.size-99 .sheet { padding: 13mm 5.5mm; gap: 0 2.5mm; }` — take the
   margin and pitch straight off the label pack, and switch
   `justify-content` / `align-content` from `center` to `start` so the grid
   anchors to that margin instead of being re-centred.
3. **`js/app.js`** — nothing, as long as the grid still holds 10 badges.
   For a different count, change `PER_SHEET` (and make it per-size if your
   presets differ).

Verify any new size by printing to PDF and measuring, not by eye:

```sh
chromium --headless --no-pdf-header-footer --print-to-pdf=out.pdf index.html
pdfinfo out.pdf          # must say 594.96 x 841.92 pts (A4)
pdftotext -bbox out.pdf -  # compare word positions between columns/rows
```
