// Chimalaya flyer for the Chimalaya shelf at Elephant House, Kathmandu.
// A5, double-sided: the front says who Chimalaya is, the back what it does.
// Compile from the repository root:
//   typst compile --root . documents/chimalaya-flyer-a5.typ
//   typst compile --root . --input bleed=3 documents/chimalaya-flyer-a5.typ chimalaya-flyer-a5-print.pdf
//
// The bleed input adds that many millimetres of bleed on every side, for a
// print shop that trims. chimalaya-flyer-a5-2up-a4.typ imports `front` and
// `back` to put two flyers on one A4 sheet, for printing in the office.
//
// Facts are from chimalayanepal.org (About CC, Services, Bag4Life); figures
// are from chimalaya-data/output/metrics.json, register to 31 August 2026.
#import "../templates/typst/chimalaya.typ": brand, org-details
#import "@preview/tiaoma:0.3.0"

#let W = 148mm
#let H = 210mm
#let pad = 12mm
#let bleed = float(sys.inputs.at("bleed", default: "0")) * 1mm

// Elephant House's mark, recoloured and cropped to the elephant itself: the
// file's canvas has a wide margin and a stray speck above the artwork.
#let elephant(fill: black, width: auto, height: auto) = image(
  bytes(
    read("../assets/Elephant_house.svg")
      .replace("#010101", fill.to-hex())
      .replace("viewBox=\"0 0 960 742\"", "viewBox=\"76 43 822 638\"")
      .replace("width=\"960\"", "width=\"822\"")
      .replace("height=\"742\"", "height=\"638\"")
  ),
  format: "svg", width: width, height: height,
)

#let flyer-text(body) = {
  set text(font: ("Inter", "Liberation Sans"), size: 8.5pt, fill: brand.ink, hyphenate: false)
  set par(justify: false, leading: 0.55em, spacing: 0.9em)
  body
}

#let eyebrow(body) = text(size: 7pt, weight: 600, fill: brand.crimson, tracking: 0.14em, upper(body))

// Full-bleed elements are placed in trim coordinates and run out by `bleed`.
#let full-width(dy, body) = place(top + left, dx: -bleed, dy: dy, body)

#let front = flyer-text({
  // The Chimalaya Nepal logo carries the tagline itself. Its lettering is
  // outlined, since Typst is not given Montserrat (see build-elephant-house-banner.py).
  place(top + left, dx: pad, dy: 9mm, image("../assets/cc_nepal_logo-outlined.svg", width: 78mm))

  full-width(34mm, image("assets/flyer-cover-mother-baby.jpg",
    width: W + 2 * bleed, height: 84mm, fit: "cover"))

  place(top + left, dx: pad, dy: 127mm, block(width: W - 2 * pad, {
    text(size: 19pt, weight: 800, fill: brand.navy, tracking: -0.01em)[A better start in life \ for mothers and newborns]
    v(1mm)
    line(length: 18mm, stroke: 2pt + brand.crimson)
    v(1mm)
    [Chimalaya Charity is a Danish–Nepali NGO, founded in 2010 by
     psychotherapist Pia Torp to empower mothers and fight dangerous
     malnutrition in newborns.]
    parbreak()
    [Since 2013 we have run a mother-and-child clinic in Bode, Madhyapur
     Thimi, near Kathmandu, together with Nepali doctors and nurses. The
     clinic serves about 25,000 people, in an area of carpet and brick
     factories where many women do hard physical work.]
  }))

  full-width(H - 26mm, rect(width: W + 2 * bleed, height: 26mm + bleed, fill: brand.crimson))
  place(top + left, dx: pad, dy: H - 20mm, elephant(fill: white, height: 14mm))
  place(top + left, dx: pad + 24mm, dy: H - 19.5mm, block(width: W - 2 * pad - 24mm,
    text(fill: white, size: 9pt, {
      text(weight: 700, size: 10.5pt)[Thank you for shopping at Elephant House.]
      linebreak()
      [Sales from the Chimalaya shelf support this work.]
    })))
})

#let card(photo, title, body) = block(width: 100%, {
  photo
  v(2.2mm)
  text(size: 9.5pt, weight: 700, fill: brand.navy, title)
  v(0.6mm)
  text(size: 7.5pt, body)
})

#let photo(path) = image(path, width: 100%, height: 27mm, fit: "cover")

#let figure-cell(number, label) = align(center, {
  text(size: 17pt, weight: 800, fill: white, number)
  v(-2.6mm)
  par(leading: 0.4em, text(size: 6.5pt, fill: white.transparentize(15%), label))
})

#let back = flyer-text({
  place(top + left, dx: pad, dy: 11mm, block(width: W - 2 * pad, {
    eyebrow[What we do]
    v(-1mm)
    text(size: 15pt, weight: 800, fill: brand.navy)[Care that reaches mothers at home]
    v(1.5mm)
    grid(columns: (1fr, 1fr), column-gutter: 6mm, row-gutter: 5mm,
      card(photo("assets/flyer-newborn-exam.jpg"), [Home visits after birth])[
        Our nurses visit newborns at home in their first days, with
        follow-ups up to six months: a head-to-toe check, danger signs,
        and help with breastfeeding.],
      card(
        block(width: 100%, height: 27mm, fill: brand.wash, inset: 1.5mm,
          align(center + horizon, image("assets/flyer-bag4life.jpg", height: 100%))),
        [Bag4Life])[
        Every family gets a changing bag at the first visit: towel, mat,
        reusable nappies, thermometer, and yak-milk soap and massage oil
        handmade in Nepal.],
      card(photo("assets/flyer-mother-group.jpg"), [Mothers' groups])[
        Twice a week, mothers of children from 6 months to 2 years meet at
        the clinic for growth checks and advice on feeding, play and sleep.],
      card(photo("assets/flyer-outreach-brick-factory.jpg"), [Outreach camps])[
        We screen for illness and malnutrition at brick and carpet
        factories, with food for pregnant and breastfeeding mothers when
        needed.],
    )
  }))

  full-width(137mm, rect(width: W + 2 * bleed, height: 24mm, fill: brand.navy))
  place(top + left, dx: pad, dy: 141mm, block(width: W - 2 * pad,
    grid(columns: 4 * (1fr,), column-gutter: 3mm,
      figure-cell[1,815][newborns visited \ at home since 2017],
      figure-cell[93.5%][of them received \ a Bag4Life bag],
      figure-cell[88.6%][had all three \ newborn visits],
      figure-cell[25,000][people in the \ clinic's area],
    )))

  place(top + left, dx: pad, dy: 167mm, block(width: W - 2 * pad,
    grid(columns: (1fr, auto), column-gutter: 6mm, {
      text(size: 11pt, weight: 800, fill: brand.navy)[How you can help]
      v(0.5mm)
      set list(marker: text(fill: brand.crimson)[•], spacing: 0.7em)
      set text(size: 8pt)
      list(
        [Buy from the Chimalaya shelf here at Elephant House],
        [Follow *\@chimalayacharity* on Facebook and Instagram],
        [Learn more, or volunteer with us, at *chimalayanepal.org*],
      )
    }, align(center, {
      tiaoma.qrcode("https://chimalayanepal.org", width: 21mm)
      v(-1mm)
      text(size: 6pt, fill: brand.muted)[Scan to visit us]
    }))))

  place(top + left, dx: pad, dy: H - 13mm, block(width: W - 2 * pad, {
    line(length: 100%, stroke: 0.5pt + brand.rule)
    v(-1mm)
    set text(size: 6.5pt, fill: brand.muted)
    grid(columns: (1fr, auto),
      [#text(weight: 700, fill: brand.navy, org-details.name) · #org-details.address \
       #org-details.phone · #org-details.email],
      align(right)[#org-details.swc \ #org-details.regd],
    )
  }))
})

#set document(title: "Chimalaya Charity – flyer for Elephant House", author: "Chimalaya Charity")
#set page(width: W + 2 * bleed, height: H + 2 * bleed, margin: 0mm)

#let side(body) = place(top + left, dx: bleed, dy: bleed, box(width: W, height: H, body))

#side(front)
#pagebreak()
#side(back)
