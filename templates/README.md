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

`chimalaya-doc` takes `title`, `subtitle`, `author`, `date`, `org`, `logo` and
`cover` (set `cover: false` for a short note with no cover page). Colours are
exposed as `brand.navy`, `brand.crimson` and so on.

## A note on the logo

These use the **CHIMALAYA NEPAL** lockup, the only vector logo available from
chimalayanepal.org. If Chimalaya Charity has its own lockup, replace
`assets/chimalaya-logo.png` (and `chimalaya-logo-reverse.png`, the white
version for dark backgrounds) and re-run the build script.

`chimalaya.org` is **not** the charity — the domain now serves unrelated spam.

## Documents built on the template

- [`documents/volunteering-at-chimalaya-nepal.typ`](../documents/volunteering-at-chimalaya-nepal.typ)
  — information sheet for prospective volunteers.

```sh
typst compile --root . documents/volunteering-at-chimalaya-nepal.typ out.pdf
```
