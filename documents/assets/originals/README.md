# Original image assets

Full-resolution, background-removed sources, kept so they can be reused in
other documents without redoing the cutouts. The images actually used by
`volunteering-at-chimalaya-nepal.typ` live one level up and are downscaled and
compressed for that document — take from here instead when starting something
new.

| File | What it is |
|---|---|
| `bag4life-bag.png` | the Bag4Life bag, 1086 × 1448 |
| `bag-contents-textiles.png` | blanket, towel and cloth nappies together |
| `bag-contents-soap-and-oil.png` | yak milk soap and baby massage oil together |
| `bag-contents-thermometer-and-cotton.png` | thermometer and cotton wool together |
| `textiles-trimmed.png` | the textiles, cropped to their bounding box |
| `red_towel.png` | separated, cropped |
| `changing_mat.png` | separated, cropped |
| `reusable_diapers.png` | separated, cropped |
| `bag-contents-row.png` | all seven items in one wide row — the source for the strip in the document |
| `baby-massage-oil.png` | separated, cropped |
| `yak-milk-soap.png` | separated, cropped |
| `cotton-wool.png` | separated, cropped |
| `digital-thermometer.png` | separated, cropped |

All have a real alpha channel, so they drop onto any background. The four
separated objects were split out of the grouped photographs by looking for
gaps in the alpha profile, then cropped to their own bounding box.

The textiles are a towel, a changing mat and reusable nappies — worth noting,
since from the photographs alone the first two read as blankets.

**Scale is not consistent between the grouped photographs.** The textiles were
shot from further back than the other items, so at native pixel size a bar of
soap comes out larger than a folded blanket. `build-map.py`'s sibling layout in
the document scales the textiles to about 55 % to compensate; do the same if
you place them side by side.

The two photographs from visits (`role-mother.jpg`, `role-handover.jpg`, one
level up) are already at their supplied resolution of 1200 × 675.
