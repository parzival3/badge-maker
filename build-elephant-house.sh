#!/usr/bin/env bash
# Rebuilds everything for the Chimalaya shelf at Elephant House:
#   banner/elephant-house-shelf-banner-100x25cm{,-print}.{svg,pdf}
#   banner/elephant-house-shelf-banner-100x25cm-cream{,-print}.{svg,pdf}
#   documents/chimalaya-flyer-a5.pdf, -print.pdf (3 mm bleed), -2up-a4.pdf
#
#   ./build-elephant-house.sh
#
# Needs nix and Inkscape (for the banner PDFs). Run from anywhere.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"

banner_python='python3.withPackages (p: [p.qrcode])'
for script in banner/build-elephant-house-banner.py banner/build-elephant-house-banner-cream.py; do
  echo "== $script"
  nix-shell -p "$banner_python" --run "python3 $script"
done

echo "== flyer"
cd documents
nix-shell --run '
  set -e
  build chimalaya-flyer-a5.typ chimalaya-flyer-a5-2up-a4.typ
  echo "typst: chimalaya-flyer-a5.typ -> chimalaya-flyer-a5-print.pdf (3 mm bleed)"
  typst compile --root .. --input bleed=3 chimalaya-flyer-a5.typ chimalaya-flyer-a5-print.pdf
'
