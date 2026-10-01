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

### Print settings that matter

In the print dialog set:

| Setting | Value |
|---|---|
| Scale | **100 %** (not "Fit to page") |
| Margins | **None** |
| Background graphics | **On** |
| Paper | A4 |

With "Fit to page" the browser shrinks the sheet by a few percent and the badges
no longer match your badge holders. Measure one printed badge with a ruler the
first time.

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
