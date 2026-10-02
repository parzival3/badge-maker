// Volunteering at Chimalaya Nepal — information sheet for prospective volunteers.
// Compile from the repository root so the logo resolves:
//   typst compile --root . documents/volunteering-at-chimalaya-nepal.typ
#import "../templates/typst/chimalaya.typ": chimalaya-doc, callout, brand

#show: chimalaya-doc.with(
  title: "Volunteering at Chimalaya Nepal",
  subtitle: "Maternal and child health, in homes around Kathmandu",
  author: "Chimalaya Nepal",
  org: "Chimalaya Nepal",
)

// A row of headline figures, for the facts worth seeing before the prose.
#let figures(..items) = {
  let cells = items.pos().map(it => align(left)[
    #text(size: 22pt, weight: 700, fill: brand.crimson, it.at(0))
    #v(-3mm)
    #text(size: 9pt, fill: brand.muted, it.at(1))
  ])
  block(above: 1em, below: 1.6em, grid(
    columns: cells.len() * (1fr,),
    gutter: 8mm,
    ..cells,
  ))
}

// A quieter, indented voice for the passage about the people themselves.
#let aside(body) = block(
  inset: (left: 8mm, y: 3mm),
  stroke: (left: 2pt + brand.rule),
  width: 100%,
  text(size: 11pt, style: "italic", fill: brand.navy, body),
)

Chimalaya is a Danish non-profit organisation that has worked in Nepal since
2011, focusing on maternal and child health. We operate a clinic where one of
the primary activities is conducting home visits.

#figures(
  ("2011", "working in Nepal since"),
  ("~30", "newborns enrolled each month"),
  ("~80", "home visits each month"),
)

We offer home visits to all newborns in the clinic's local area — approximately
30 new cases per month. This is followed by two additional visits during the
first month and a final visit when the child is around six months old.
Afterward, mothers are invited to join mother-groups until the child is
approximately two years old.

= Our mission and reach

Our Nepalese colleagues collaborate with local health authorities and conduct
outreach camps several times a month in impoverished mountain areas outside
Kathmandu. We also visit brick and carpet factories, where women work with
their infants under unhygienic conditions and very poor living standards.

Our approach combines prevention and health promotion, with a strong focus on:

- *Empowerment* of mothers and families
- *Professional knowledge* and capacity building
- *A sustainable future* for the local community

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

As a volunteer, you will get straight to the heart of Nepalese homes. You will
use your professional skills to promote health and prevent illness among
infants and mothers.

#aside[
  You will meet some of the warmest, most welcoming people who, despite
  widespread poverty and limited resources, carry themselves with immense
  dignity, spirituality, and hospitality.
]

= Clinical activities and programmes

== Home visits

The clinic performs approximately 80 home visits per month, following each
family through the child's first six months.

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
  columns: (auto, auto, 1fr),
  table.header[Stay][Fee][Approximately],
  [1 week], [25,000 NPR], [1,100 DKK / 150 EUR],
  [1 month], [90,000 NPR], [4,000 DKK / 535 EUR],
)

The clinic provides lunch, tea, and coffee for volunteers.

== Accommodation

The clinic can arrange accommodation:

- *Bed and breakfast*
- *Homestays with the clinic staff*, allowing you to experience the local
  culture firsthand
