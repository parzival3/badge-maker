// Chimalaya document template.
//
//   #import "chimalaya.typ": chimalaya-doc, callout, brand
//   #show: chimalaya-doc.with(title: "...", subtitle: "...", author: "...")
//
// Brand colours are taken from the logo artwork in assets/logo.svg.

#let brand = (
  navy: rgb("#123f6b"),
  crimson: rgb("#e50046"),
  ink: rgb("#16233a"),
  muted: rgb("#5b6b80"),
  rule: rgb("#d7dee7"),
  wash: rgb("#f4f7fa"),
)

// Inter matches the logo and the printed materials. Typst falls back to its
// default sans if Inter is not installed, which still reads correctly.
#let body-font = ("Inter", "Liberation Sans")

#let chimalaya-doc(
  title: none,
  subtitle: none,
  author: none,
  date: datetime.today(),
  logo: "../assets/chimalaya-logo.png",
  org: "Chimalaya Charity",
  cover: true,
  body,
) = {
  set document(title: if title == none { "Document" } else { title }, author: if author == none { "" } else { author })

  set page(
    paper: "a4",
    margin: (top: 28mm, bottom: 24mm, left: 24mm, right: 24mm),
    header: context {
      // the cover carries its own masthead, so skip the running header there
      if cover and here().page() == 1 { return }
      set text(9pt, fill: brand.muted)
      grid(
        columns: (1fr, auto),
        align(left + horizon)[#image(logo, width: 34mm)],
        align(right + horizon)[#if title != none { title }],
      )
      v(-2mm)
      line(length: 100%, stroke: 0.5pt + brand.rule)
    },
    footer: context {
      set text(8.5pt, fill: brand.muted)
      line(length: 100%, stroke: 0.5pt + brand.rule)
      v(1mm)
      grid(
        columns: (1fr, auto),
        align(left)[#org],
        align(right)[#counter(page).display("1 / 1", both: true)],
      )
    },
  )

  set text(font: body-font, size: 10.5pt, fill: brand.ink, lang: "en")
  set par(justify: true, leading: 0.72em, spacing: 1.1em)

  show heading: set text(fill: brand.navy)
  // heading and its rule must be separate blocks, or the rule renders inline
  // and reads as an underline struck through the heading
  show heading.where(level: 1): it => {
    block(above: 1.5em, below: 0.45em, text(size: 16pt, weight: 700, it.body))
    block(above: 0em, below: 1em, line(length: 18mm, stroke: 2pt + brand.crimson))
  }
  show heading.where(level: 2): set text(size: 12.5pt, weight: 650)
  show heading.where(level: 3): set text(size: 11pt, weight: 600)

  show link: set text(fill: brand.crimson)
  set table(stroke: (x, y) => if y == 0 { (bottom: 1pt + brand.navy) } else { (bottom: 0.5pt + brand.rule) })
  show table.cell.where(y: 0): set text(weight: 650, fill: brand.navy)

  set list(marker: text(fill: brand.crimson)[•])
  set enum(numbering: n => text(fill: brand.crimson, weight: 650)[#n.])

  if cover {
    // masthead
    image(logo, width: 58mm)
    v(22mm)
    if title != none {
      text(size: 30pt, weight: 700, fill: brand.navy, title)
      v(3mm)
    }
    if subtitle != none {
      text(size: 14pt, fill: brand.muted, subtitle)
      v(5mm)
    }
    line(length: 32mm, stroke: 3pt + brand.crimson)
    v(6mm)
    set text(10pt, fill: brand.muted)
    if author != none [#author \ ]
    if date != none [#date.display("[day] [month repr:long] [year]")]
    v(14mm)
  }

  body
}

// A tinted box for notes, key findings or warnings.
#let callout(title: none, accent: brand.crimson, body) = block(
  fill: brand.wash,
  stroke: (left: 3pt + accent),
  inset: (x: 12pt, y: 10pt),
  radius: (right: 3pt),
  width: 100%,
  {
    if title != none {
      text(weight: 650, fill: brand.navy, title)
      linebreak()
    }
    body
  },
)
