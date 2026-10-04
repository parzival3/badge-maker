// Volunteering at Chimalaya Nepal — information sheet for prospective volunteers.
// Compile from the repository root so the logo resolves:
//   typst compile --root . documents/volunteering-at-chimalaya-nepal.typ
//
// Background on the organisation is drawn from chimalayanepal.org (About CC).
#import "../templates/typst/chimalaya.typ": chimalaya-doc, callout, brand

#show: chimalaya-doc.with(
  title: "Volunteering at Chimalaya Nepal, 2027 Program",
  subtitle: "Improving maternal and child health, in homes around Kathmandu",
  author: "Chimalaya Charity",
  org: "Chimalaya Charity",
)

// Headline figures, centred as a band above the prose.
#let figures(..items) = {
  let cells = items.pos().map(it => align(center)[
    #set par(justify: false, leading: 0.5em)
    #text(size: 23pt, weight: 700, fill: brand.crimson, it.at(0))
    #v(-3.5mm)
    #text(size: 8.5pt, fill: brand.muted, it.at(1))
  ])
  block(above: 1.4em, below: 1.6em, width: 100%, {
    line(length: 100%, stroke: 0.5pt + brand.rule)
    v(4mm)
    grid(columns: cells.len() * (1fr,), gutter: 6mm, ..cells)
    v(2mm)
    line(length: 100%, stroke: 0.5pt + brand.rule)
  })
}

// A quieter, indented voice for passages about people rather than facts.
#let aside(body) = block(
  inset: (left: 8mm, y: 3mm),
  stroke: (left: 2pt + brand.rule),
  width: 100%,
  text(size: 11pt, style: "italic", fill: brand.navy, body),
)

// A frame standing in for artwork not yet supplied. Visible on purpose: a
// missing photo should be obvious in a draft, not silently absent.
#let photo-placeholder(height: 55mm, caption: none) = block(width: 100%,
  box(
    width: 100%, height: height,
    fill: brand.wash,
    stroke: (paint: brand.rule, thickness: 1pt, dash: "dashed"),
    radius: 3pt,
    align(center + horizon, text(size: 9pt, fill: brand.muted,
      if caption != none { caption } else [Photo to be supplied])),
  ))

Chimalaya Charity is a Danish–Nepalese NGO, founded in 2010 by psychotherapist
Pia Torp with the purpose of empowering mothers and giving newborns a better
start in life by fighting dangerous malnutrition. It has worked in Nepal since
2011, and became a registered NGO in Nepal in 2016.

#figures(
  ("2010", "founded in Denmark"),
  ("25,000", "people in the catchment area"),
  ("~30", "newborns enrolled each month"),
  ("~80", "home visits each month"),
)

In 2013, Pia Torp and Chimalaya Charity began working with the doctor and
researcher Ram Krishna Chandyo, PhD, and his wife, the paediatrician and
researcher Manjeswori Ulak. Both were educated in the West and now work in
their homeland to improve the health of the local population. Together, with
the help of the local community, they established the mothers' group clinic in
Bode, Thimi, just outside Kathmandu.

The clinic is the heart of our work. It covers a catchment area of about 25,000
people — an area of small towns and many carpet and brick factories, where
women do hard physical labour. For many locals the clinic and its staff are a
safe and familiar setting, which makes it easier to reach the most vulnerable
families.

Home visiting is one of the clinic's primary activities. Every newborn in the
local area is offered a first visit, two further visits during the first month,
and a final visit at around six months. Mothers are then invited to join
mother-groups until the child is about two years old.

#pagebreak()

= Our mission and reach

With the vision _Improving Maternal and Child Health_, Chimalaya Charity works
to combat malnutrition and to promote health and development in children,
through the empowerment and education of mothers and their families. We want
to secure maternal health before and after birth, the survival of newborns, and
the reversal of the negative growth curve in children under five.

Our Nepalese colleagues collaborate with local health authorities and conduct
outreach camps several times a month in impoverished mountain areas outside
Kathmandu. We also visit brick and carpet factories, where women work with
their infants under unhygienic conditions and very poor living standards.

Our approach combines prevention and health promotion, with a strong focus on:

- *Empowerment* of mothers and families
- *Professional knowledge* and capacity building
- *A sustainable future* for the local community

Our work is always based on local needs. The idea of mothers' groups comes from
the Nordic countries, for instance, but at our clinic the model is adapted to
Nepalese conditions. The clinic's leading doctors are associated with the
Center for International Health in Bergen, which gives the clinic access to
current research on malnutrition, and the programme includes ongoing capacity
building and training of local health workers.

= Your role as a volunteer

We welcome volunteers who are either students or qualified professionals within
the healthcare field, such as:

#grid(
  columns: (1fr, 1fr),
  gutter: 6mm,
  [
    - Nurses and health visitors
    - Physiotherapists
  ],
  [
    - Midwives
    - Nutritionists
  ],
)

Other relevant professional backgrounds are also considered.

You will use your professional skills to promote health and prevent illness
among infants and mothers, working alongside Nepalese colleagues who know the
families and the area.

#aside[
  As a volunteer, you will get straight to the heart of Nepalese homes — and
  meet some of the warmest, most welcoming people, who despite widespread
  poverty and limited resources carry themselves with immense dignity,
  spirituality, and hospitality.
]

#pagebreak()

= Clinical activities and programmes

#block(breakable: false)[
  == Home visits

  The clinic performs approximately 80 home visits per month, following each
  family through the child's first six months.
]

#table(
  columns: (auto, auto, 1fr),
  table.header[Visit][When][What happens],
  [1st], [Shortly after birth],
  [General newborn examination (head-to-toe), screening for danger signs, and
   breastfeeding guidance],
  [2nd], [2 weeks],
  [Checking the well-being of both mother and baby; reinforcing breastfeeding
   techniques],
  [3rd], [2 months],
  [Ensuring exclusive breastfeeding and monitoring motor, linguistic, and
   emotional development],
  [4th], [6 months],
  [Final growth evaluation, guidance on starting solid foods, and an invitation
   to join the clinic's mother-groups],
)

#callout(title: "Bag4life")[
  At the first visit, families receive a bag containing essentials: a baby
  blanket, a thermometer, cloth diapers, and soap.
]

== Mother-groups

Held twice a week for mothers with children aged 6–24 months.

/ Activities: Health and hygiene workshops, nutrition courses with cooking
  demonstrations, growth monitoring, and yoga classes.
/ Purpose: To create a safe social network for knowledge sharing and peer
  support.

// kept whole so the two items are not split across a page break
#block(breakable: false)[
  == School and factory outreach

  / School programme: Height and weight measurements, dental hygiene, and
    health education.
  / Factory visits: Hygiene measures and health checks for newborns and
    children living in high-risk environments at brick and carpet factories.
]

= Practical information

== Fees

#table(
  columns: (auto, auto, auto, 1fr),
  table.header[Stay][Fee][Approximately][Included],
  [1 week], [25,000 NPR], [1,100 DKK / 150 EUR],
  [Placement at the clinic, supervision by clinic staff, and lunch, tea and
   coffee on working days],
  [1 month], [90,000 NPR], [4,000 DKK / 535 EUR],
  [As above],
)

#callout(title: "To be confirmed", accent: brand.muted)[
  Left blank deliberately rather than guessed at: the cost of accommodation,
  what the fee excludes (flights, visa, insurance, local transport), how and
  when payment is made, whether a deposit is required, and any minimum stay.
]

#block(breakable: false)[
  == Accommodation

  The clinic can arrange accommodation, either bed and breakfast or a homestay
  with clinic staff, which lets you experience the local culture firsthand.

  #photo-placeholder(
    height: 58mm,
    caption: [Photo of the accommodation — to be supplied],
  )
  #v(-1mm)
  #text(size: 8.5pt, fill: brand.muted)[
    A real photograph of the rooms belongs here. None is published on
    chimalayanepal.org, and a stock image of someone else's guest house would
    misrepresent what volunteers are booking.
  ]
]

= Contact

/ Chimalaya Nepal: Bode, Madhyapur Thimi-8, Bhaktapur, Nepal
/ Phone: +977-01-6631122 — mobile 9862579490
/ Email: #link("mailto:chimalayanepal2014@gmail.com")[chimalayanepal2014\@gmail.com]
/ Web: #link("https://chimalayanepal.org")[chimalayanepal.org]
