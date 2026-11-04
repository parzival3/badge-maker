// Single-sided A5 flyer for the Chimalaya shelf at Elephant House.
// Compile from the repository root:
//   typst compile --root . documents/chimalaya-flyer-a5-new.typ
#set page(width: 148mm, height: 210mm, margin: 0mm)
#set text(font: "Montserrat", fallback: true)

#let navy = rgb("#123F6B")
#let crimson = rgb("#E50046")
#let deep-navy = rgb("#0B2A49")

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

#grid(
  rows: (1fr, 25mm),

  // Top: full-bleed photo, navy gradient from the left, text block
  block(width: 100%, height: 100%, clip: true)[
    // The photo is portrait; shift it right so the mother sits beside the text, bag at the bottom
    #place(rect(width: 100%, height: 100%, fill: deep-navy))
    #place(bottom + left, dx: 30mm, dy: 0mm, image("example_pictures/1115323998025236.jpg", width: 140%))

    // Navy fade from the left, and a little extra at the top for the headline
    #place(rect(
      width: 100%, height: 100%,
      fill: gradient.linear(
        (deep-navy, 0%),
        (deep-navy, 35%),
        (deep-navy.transparentize(50%), 55%),
        (deep-navy.transparentize(100%), 100%),
        angle: 0deg,
      ),
    ))
    #place(rect(
      width: 100%, height: 60%,
      fill: gradient.linear(
        (deep-navy.transparentize(35%), 0%),
        (deep-navy.transparentize(100%), 100%),
        angle: 90deg,
      ),
    ))

    #pad(x: 9mm, top: 10mm)[
      #set text(fill: white)

      #text(size: 28pt, weight: "extrabold")[
        #set par(leading: 0.3em)
        A BETTER START IN LIFE \
        #text(fill: crimson)[FOR MOTHERS] \
        AND NEWBORNS
      ]

      #v(6mm)

      #block(width: 76mm)[
        #set par(leading: 0.6em)
        #text(size: 13pt)[
          Since 2013, Chimalaya's clinic in Bode, Bhaktapur has cared for
          mothers and babies in a community of *brick and carpet factory
          workers*.
        ]
      ]

      #v(6mm)

      #rect(fill: crimson, inset: (x: 4mm, y: 4mm), radius: 1mm, width: 56mm)[
        #align(center)[
          #text(size: 32pt, weight: "extrabold")[1,815] \
          #v(-1.5mm)
          #text(size: 8.5pt)[newborns visited at home \ by our nurses since 2017]
        ]
      ]
    ]
  ],

  // Bottom: white footer, set off from the photo by a crimson rule
  block(width: 100%, height: 100%, fill: white)[
    #place(top, rect(width: 100%, height: 1.2mm, fill: crimson, stroke: none))
    #align(horizon, pad(x: 9mm, top: 1.2mm)[
      #grid(
        columns: (auto, 1fr, auto, auto),
        align: horizon,
        column-gutter: 3mm,
        image("../assets/cc_nepal_logo-outlined.svg", height: 12mm),
        align(center, line(angle: 90deg, length: 12mm, stroke: 0.4pt + luma(200))),
        elephant(fill: black, height: 10mm),
        [
          #set text(fill: navy, size: 8pt)
          #set par(leading: 0.45em)
          #text(weight: "bold")[Thank you for shopping \ at Elephant House.] \
          Sales of these products \ support Chimalaya's work.
        ],
      )
    ])
  ],
)
