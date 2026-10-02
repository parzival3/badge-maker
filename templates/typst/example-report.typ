#import "chimalaya.typ": chimalaya-doc, callout, brand

#show: chimalaya-doc.with(
  title: "PNC home visit nurses training",
  subtitle: "Programme report — Bhaktapur district",
  author: "Chimalaya Charity",
  date: datetime(year: 2026, month: 10, day: 7),
)

= Background

This is the Chimalaya document template. Replace this text with your own.
Body copy is set in Inter at 10.5 pt with justified paragraphs. Links such as
#link("https://chimalayanepal.org")[chimalayanepal.org] pick up the brand
crimson.

== Objectives

- Train community nurses in postnatal home visiting
- Standardise the newborn assessment checklist
- Establish a referral path to the municipality hospital

#callout(title: "Key finding")[
  Coverage rose from 42 % to 68 % of registered births within three months of
  the first training round.
]

= Results

#table(
  columns: (1fr, auto, auto),
  table.header[Indicator][Baseline][Endline],
  [Home visits within 48 h], [42 %], [68 %],
  [Newborns weighed], [55 %], [91 %],
  [Referrals completed], [12], [37],
)

== Next steps

+ Extend the training to two further wards
+ Add a refresher session at six months
+ Publish the checklist in Nepali
