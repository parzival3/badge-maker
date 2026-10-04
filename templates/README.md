# Chimalaya templates

Branded starting points for documents and presentations, using the colours and
logo from `assets/logo.svg`.

| File | Use |
|---|---|
| `chimalaya-document.docx` | Word — reports, letters, concept notes |
| `chimalaya-presentation.pptx` | PowerPoint — 16:9, four slide designs |
| `typst/chimalaya.typ` | Typst — reports typeset from plain text |
| `typst/example-report.typ` | a worked example using the Typst template |
| `build-office-templates.py` | regenerates the .docx and .pptx |

## Brand values

| Role | Hex | Where |
|---|---|---|
| Navy | `#123f6b` | headings, logo wordmark, dark panels |
| Crimson | `#e50046` | accent rules, links, list markers |
| Ink | `#16233a` | body text |
| Muted | `#5b6b80` | subtitles, captions, footers |
| Rule | `#d7dee7` | hairlines |

Typeface is **Inter** throughout, matching the logo and the printed banner.
Install it from [rsms.me/inter](https://rsms.me/inter/) — without it, Word and
PowerPoint silently substitute their default, and the templates still work but
stop matching the other materials.

## Word and PowerPoint

Open, then **File → Save As** under a new name. The Word file carries real
named styles (Title, Subtitle, Heading 1–3, Normal, Table Grid with a navy
header), so use the style gallery rather than formatting by hand and the
document stays consistent as it grows.

The deck has four slides to copy: title, dark section divider, content, and a
closing slide.

To change the branding, edit `build-office-templates.py` and re-run it:

```sh
pip install python-docx python-pptx
python3 templates/build-office-templates.py
```

## Typst

[Typst](https://typst.app) typesets a report from a plain-text file — good for
anything version-controlled or generated.

```sh
typst compile --root . templates/typst/example-report.typ report.pdf
```

The `--root .` matters: the template loads the logo from `templates/assets/`,
which is outside the `.typ` file's own directory.

```typ
#import "chimalaya.typ": chimalaya-doc, callout, brand

#show: chimalaya-doc.with(
  title: "Document title",
  subtitle: "Project name",
  author: "Chimalaya Charity",
)

= First heading
Body text.

#callout(title: "Note")[A tinted box for key findings.]
```

A faded Chimalaya mark sits in the page background by default. Pass
`watermark: false` to drop it, or `mark:` to point at different artwork. The
opacity lives in the SVG itself (`assets/chimalaya-mark-faded.svg`, currently
5 %) because Typst has no image-opacity property — edit the `opacity`
attribute there to change it. The mark is monochrome navy on purpose: at this
strength the brand crimson reads as a pink blotch behind body text.

`chimalaya-doc` takes `title`, `subtitle`, `author`, `date`, `org`, `logo`,
`watermark`, `mark` and
`cover` (set `cover: false` for a short note with no cover page). Colours are
exposed as `brand.navy`, `brand.crimson` and so on.

## The clinic locator map

`documents/build-map.py` draws `documents/assets/clinic-map.svg` from
OpenStreetMap data: ward 8 of Madhyapur Thimi shaded as the working area, the
clinic marked, dashed rings for distance, and a scale bar.

```sh
python3 documents/build-map.py              # redraw from the cached data
python3 documents/build-map.py --refresh    # re-fetch from Overpass first
```

The OSM response is cached in `documents/assets/osm-cache.json` so the build
works offline and the map does not change under you.

The clinic is at **27.690562, 85.389687**, decoded from the plus code
`7MV7M9RQ+6V` (`M9RQ+6V Madhyapur Thimi`) — a 14 m cell, verified to fall
inside the ward 8 boundary. The working area is OSM relation 16113837,
"Madhyapur Thimi-08".

### Satellite inset (optional)

An inset of the clinic's immediate surroundings (about 245 m across) can be
drawn into the top-left of the map. It needs a Mapbox access token, because
there is no open-licence alternative worth printing: Sentinel-2 is free but
10 m per pixel, which over this area works out at roughly 60 dpi.

```sh
MAPBOX_TOKEN=pk.xxxxx python3 documents/build-map.py
```

build-map.py writes two maps, so you can pick:  (drawn map
with a small satellite inset) and  (satellite
imagery of the whole area with the ward outlined). The document shows both,
labelled Version A and Version B; delete the block you do not want.

The ward overlay on the satellite version is projected with the same Web
Mercator transform Mapbox renders with, not the equirectangular one used for
the drawn map, so the boundary lands exactly on the imagery.

The fetched image is cached at `assets/clinic-satellite.png` and git-ignored;
delete it to re-fetch. Without a token the inset is skipped and the script
says so. Using the imagery adds "satellite © Mapbox © Maxar" to the credit
line, which must stay visible.

Do **not** substitute Google Maps or Google Earth imagery: their terms do not
cover reuse in a printed leaflet that gets distributed.

**The attribution is not optional.** OSM data is ODbL; "© OpenStreetMap
contributors" is drawn into the map and must stay legible wherever it is
published.

## Organisation details

`org-details` in `typst/chimalaya.typ` holds the name, Nepali name, tagline,
address, phone, email, both websites, Facebook, and the registration numbers
(Regd. No. 87/072/073, SWC Regd. No. 44059) — taken from Chimalaya's printed
flyers and chimalayanepal.org. Quote them from there rather than retyping, and
correct them in one place if they change.

- `#imprint()` renders the full block, rules and all. Nepali documents are
  normally expected to show the registration numbers, so they are included.
- `#partners("a.png", "b.png", caption: "In partnership with")` renders a row
  of partner logos, as the flyers do for Rotary and Inner Wheel. You need to
  supply those logo files.
- The cover prints the tagline under the logo. Pass `tagline: none` to omit it,
  and avoid repeating it in the subtitle.

## A note on the logo

These use the **CHIMALAYA NEPAL** lockup, the only vector logo available from
chimalayanepal.org. If Chimalaya Charity has its own lockup, replace
`assets/chimalaya-logo.png` (and `chimalaya-logo-reverse.png`, the white
version for dark backgrounds) and re-run the build script.

`chimalaya.org` is **not** the charity — the domain now serves unrelated spam.

## Documents built on the template

- [`documents/volunteering-at-chimalaya-nepal.typ`](../documents/volunteering-at-chimalaya-nepal.typ)
  — information sheet for prospective volunteers.

Build it with the Nix shell in that folder, which pins Typst and supplies the
Inter and Noto Sans Devanagari fonts without installing anything system-wide:

```sh
cd documents
nix-shell --run build      # every .typ here -> .pdf
nix-shell --run watch      # recompile on save
```

Or directly, if you have Typst and the fonts already:

```sh
typst compile --root . documents/volunteering-at-chimalaya-nepal.typ out.pdf
```

The `--root` matters: documents load the template and logo from `templates/`,
outside their own directory. The generated PDFs are git-ignored.
