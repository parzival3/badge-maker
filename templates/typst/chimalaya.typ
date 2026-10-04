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
// Organisation details, as printed on Chimalaya's own flyers and listed on
// chimalayanepal.org. Kept here so every document quotes the same values.
#let org-details = (
  name: "Chimalaya Charity Nepal",
  nepali: "चिमालय च्यारिटी नेपाल",
  tagline: "Improving maternal and child health",
  address: "Bode, Madhyapur Thimi-8, Bhaktapur, Nepal",
  phone: "+977-01-6631122",
  mobile: "9862579490",
  email: "chimalayanepal2014@gmail.com",
  web: ("chimalayacharity.com", "chimalayanepal.org"),
  facebook: "facebook.com/chimalayacharity",
  regd: "Regd. No. 87/072/073",
  swc: "SWC Regd. No. 44059",
)

#let body-font = ("Inter", "Liberation Sans")

#let chimalaya-doc(
  title: none,
  subtitle: none,
  author: none,
  date: none,
  logo: "../assets/chimalaya-logo.png",
  watermark: true,
  mark: "../assets/chimalaya-mark-faded.svg",
  org: "Chimalaya Charity",
  tagline: org-details.tagline,
  cover: true,
  body,
) = {
  set document(title: if title == none { "Document" } else { title }, author: if author == none { "" } else { author })

  set page(
    paper: "a4",
    margin: (top: 28mm, bottom: 24mm, left: 24mm, right: 24mm),
    // The mark carries its own opacity (Typst has no image-opacity property),
    // and bleeds off the bottom-right corner so it never sits behind a line of
    // text at full strength.
    background: if watermark {
      place(bottom + right, dx: 52mm, dy: 44mm, image(mark, width: 128mm))
    },
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
    block(width: 100%, {
      // the body is justified; a justified cover title stretches its words
      // across the measure, so the cover sets its own ragged-right paragraphs
      set par(justify: false, leading: 0.4em)
      image(logo, width: 58mm)
      if tagline != none {
        v(4mm)
        text(size: 8.5pt, weight: 600, fill: brand.crimson,
             tracking: 0.14em, upper(tagline))
      }
      v(5mm)
      if title != none {
        text(size: 30pt, weight: 700, fill: brand.navy, title)
        v(4mm)
      }
      if subtitle != none {
        text(size: 14pt, fill: brand.muted, subtitle)
        v(6mm)
      }
      line(length: 32mm, stroke: 3pt + brand.crimson)
      v(6mm)
      set text(10pt, fill: brand.muted)
      set par(leading: 0.65em)
      if author != none [#author \ ]
      if date != none [#date.display("[day] [month repr:long] [year]")]
    })
    v(8mm)
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


// The full organisation imprint. Nepali documents are normally expected to
// carry the registration numbers, so they are part of the block rather than
// an afterthought.
#let imprint(details: org-details) = block(
  width: 100%,
  above: 1.4em,
  {
    line(length: 100%, stroke: 0.5pt + brand.rule)
    v(3mm)
    set text(size: 8.5pt, fill: brand.muted, hyphenate: false)
    set par(justify: false, leading: 0.6em)
    grid(
      columns: (1.25fr, 1fr, auto),
      gutter: 8mm,
      [
        #text(weight: 650, fill: brand.navy, details.name) \
        #details.nepali \
        #details.address
      ],
      [
        #details.phone · #details.mobile \
        #link("mailto:" + details.email)[#details.email] \
        #details.web.map(w => link("https://" + w)[#w]).join([ · ])
      ],
      align(right)[
        #details.regd \
        #details.swc \
        #link("https://" + details.facebook)[#details.facebook]
      ],
    )
  },
)

// A row of partner logos, as the flyers carry (Rotary, Inner Wheel, ...).
// Pass image paths: #partners("../assets/rotary.png", "../assets/iw.png")
#let partners(..paths, height: 13mm, caption: none) = block(
  width: 100%,
  above: 1.4em,
  {
    line(length: 100%, stroke: 0.5pt + brand.rule)
    v(4mm)
    if caption != none {
      text(size: 8pt, fill: brand.muted, tracking: 0.1em, upper(caption))
      v(3mm)
    }
    grid(
      columns: paths.pos().len() * (1fr,),
      gutter: 8mm,
      ..paths.pos().map(p => align(center + horizon, image(p, height: height))),
    )
  },
)
