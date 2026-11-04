// Two copies of the A5 flyer on each side of an A4 sheet, for printing in the
// office: print double-sided (flip on short edge), then cut down the middle.
// Compile from the repository root:
//   typst compile --root . documents/chimalaya-flyer-a5-2up-a4.typ
#import "chimalaya-flyer-a5.typ": front, back, W, H

#set document(title: "Chimalaya Charity – flyer for Elephant House, 2-up A4", author: "Chimalaya Charity")
#set page(paper: "a4", flipped: true, margin: 0mm)

// Short ticks at the top and bottom of the centre line show where to cut,
// without printing a line across the artwork.
#let sheet(side) = {
  place(top + left, box(width: W, height: H, clip: true, side))
  place(top + left, dx: W, box(width: W, height: H, clip: true, side))
  for dy in (0mm, H - 4mm) {
    place(top + left, dx: W, dy: dy, line(length: 4mm, angle: 90deg, stroke: 0.3pt + gray))
  }
}

#sheet(front)
#pagebreak()
#sheet(back)
