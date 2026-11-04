# Builds the 100 x 25 cm shelf header for the Chimalaya shelf at Elephant House,
# Kathmandu. 1 user unit = 1 mm.
#
#   nix-shell -p "python3.withPackages (p: [p.qrcode])" \
#     --run "python3 banner/build-elephant-house-banner.py"
#
# Writes the design SVG at trim size and a print SVG with 3 mm bleed, both with
# live text in Inter, so the print shop needs Inter to open them. When Inkscape
# is on PATH it also writes a print PDF with the font embedded, which opens
# anywhere. Only the logo's lettering is outlined, as it comes from the logo
# artwork.
import re, os, shutil, subprocess
import qrcode

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The Chimalaya Nepal logo, with its Montserrat lettering already converted to
# outlines and the canvas cropped to the artwork. Regenerate it after editing
# cc_nepal_logo.svg:
#   inkscape assets/cc_nepal_logo.svg --export-text-to-path \
#     --export-area-drawing --export-plain-svg -o assets/cc_nepal_logo-outlined.svg
CHIMALAYA = os.path.join(REPO, 'assets', 'cc_nepal_logo-outlined.svg')
CHIM_W, CHIM_H = 1370.1583, 305.9491   # its viewBox
MARK = os.path.join(REPO, 'assets', 'logo.svg')   # the roundel, for the faded watermark
ELEPHANT = os.path.join(REPO, 'assets', 'Elephant_house.svg')
OUT = os.path.join(REPO, 'banner', 'elephant-house-shelf-banner-100x25cm')

W, H = 1000, 250               # trim size
BLEED = 3
NAVY, CRIMSON = '#123f6b', '#e50046'
INK, MUTED, GOLD, RULE = '#16233a', '#5b6b80', '#f0a81e', '#d7dee7'
URL = 'https://chimalayanepal.org'
SOCIAL = '@chimalayacharity'         # the same handle on Facebook and Instagram

def inline(path):
    s = open(path).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'<sodipodi:namedview.*?(/>|</sodipodi:namedview>)', '', s, flags=re.S)
    return re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1).strip()

chim = inline(CHIMALAYA)
chim_mark = ''.join(re.findall(r'<path[^>]*/>', inline(MARK))[:3])

# The elephant is one path. Its first subpath is a stray three-pixel speck in
# the top-left corner, which would throw off the bounding box: drop it and make
# the move to the next subpath absolute (77+802, 39+387).
eleph = inline(ELEPHANT)
eleph = eleph.replace('m 77,39 v 1 h 3 l -3,-1 m 802,387', 'M 879,426', 1)
assert 'M 879,426' in eleph, 'Elephant_house.svg changed; update the speck fix'
EL_X, EL_Y, EL_W, EL_H = 76.2, 43.5, 821.1, 637.2   # artwork bounds within its 960 x 742 canvas

def qr_path(data):
    """The QR code as one path in module units, each row's dark runs merged."""
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(data)
    q.make(fit=True)
    m = q.get_matrix()
    d = []
    for y, row in enumerate(m):
        x = 0
        while x < len(row):
            if row[x]:
                start = x
                while x < len(row) and row[x]:
                    x += 1
                d.append(f'M{start},{y}h{x-start}v1h{start-x}z')
            else:
                x += 1
    return ''.join(d), len(m)

qr_d, qr_n = qr_path(URL)

# --- layout -----------------------------------------------------------------
TOPBAR = 7
MID = TOPBAR + (H - TOPBAR) / 2             # optical centre below the bar

# Left column: the logo, and under it the QR to the website with its label
# alongside, the pair centred as one block.
chim_w = 270
chim_h = chim_w * CHIM_H / CHIM_W
qr_size, QR_GAP = 48, 12
chim_x, chim_y = 34, MID - (chim_h + QR_GAP + qr_size) / 2
qr_x, qr_y = chim_x, chim_y + chim_h + QR_GAP

DIV1, DIV2 = 340, 790                       # hairlines between the three zones
TX = (DIV1 + DIV2) / 2                      # centre column

el_w = 118
el_h = el_w * EL_H / EL_W
el_cx = (DIV2 + W) / 2
el_y = MID - (el_h + 36) / 2            # elephant plus its two lines, centred
el_s = el_w / EL_W

# Facebook and Instagram glyphs ahead of the handle, the row centred on TX.
# The handle's width is an estimate for Inter SemiBold at this size.
soc_y, soc_size = 221, 10.5
soc_text_w = 0.555 * soc_size * len(SOCIAL)
soc_x = TX - (2 * 9 + 3 + 4 + soc_text_w) / 2
ICON = 9

def body(bleed):
    """Artwork in trim coordinates; the bar and background run into the bleed."""
    b = bleed
    return f'''
<rect x="{-b}" y="{-b}" width="{W+2*b}" height="{H+2*b}" fill="#ffffff"/>

<g clip-path="url(#frame)">
  <!-- the roundel, faded and bled off the bottom edge under the centre column -->
  <use href="#chimmark" x="{TX-130}" y="{H-95}" width="260" height="260" opacity="0.05"/>
</g>

<rect x="{-b}" y="{-b}" width="{W*0.62+b:.1f}" height="{TOPBAR+b}" fill="{NAVY}"/>
<rect x="{W*0.62:.1f}" y="{-b}" width="{W*0.26:.1f}" height="{TOPBAR+b}" fill="{CRIMSON}"/>
<rect x="{W*0.88:.1f}" y="{-b}" width="{W*0.12+b:.1f}" height="{TOPBAR+b}" fill="{GOLD}"/>

<!-- left: Chimalaya Nepal, and the QR to the website -->
<g transform="translate({chim_x},{chim_y:.2f}) scale({chim_w/CHIM_W:.6f})">{chim}</g>
<g transform="translate({qr_x},{qr_y:.2f}) scale({qr_size/qr_n:.6f})">
  <path d="{qr_d}" fill="{INK}"/>
</g>
<text x="{qr_x+qr_size+10}" y="{qr_y+qr_size/2-3:.2f}" font-size="8" font-weight="600"
      letter-spacing="1.6" fill="{CRIMSON}">SCAN TO VISIT</text>
<text x="{qr_x+qr_size+10}" y="{qr_y+qr_size/2+10:.2f}" font-size="12" font-weight="600"
      fill="{NAVY}">chimalayanepal.org</text>

<line x1="{DIV1}" y1="52" x2="{DIV1}" y2="{H-45}" stroke="{RULE}" stroke-width="1.2"/>
<line x1="{DIV2}" y1="52" x2="{DIV2}" y2="{H-45}" stroke="{RULE}" stroke-width="1.2"/>

<!-- centre: the message -->
<text x="{TX}" y="58" text-anchor="middle" font-size="9.5" font-weight="600"
      letter-spacing="2.6" fill="{CRIMSON}">SHOP FOR A GOOD CAUSE</text>
<text x="{TX}" y="103" text-anchor="middle" font-size="31" font-weight="800"
      letter-spacing="-0.4" fill="{NAVY}">Every purchase helps</text>
<text x="{TX}" y="139" text-anchor="middle" font-size="31" font-weight="800"
      letter-spacing="-0.4" fill="{NAVY}">mothers &amp; newborns</text>
<rect x="{TX-30}" y="155" width="60" height="2.6" fill="{CRIMSON}"/>
<text x="{TX}" y="180" text-anchor="middle" font-size="11.5" font-weight="500"
      fill="{INK}">Sales from this shelf support Chimalaya Charity</text>
<text x="{TX}" y="197" text-anchor="middle" font-size="11.5" font-weight="500"
      fill="{INK}">and its health work in Bode, Bhaktapur</text>

<!-- Facebook and Instagram, then the handle they share -->
<g transform="translate({soc_x:.2f},{soc_y-ICON+1})">
  <circle cx="{ICON/2}" cy="{ICON/2}" r="{ICON/2}" fill="{NAVY}"/>
  <text x="{ICON/2+0.3}" y="{ICON-1.2}" text-anchor="middle" font-size="8" font-weight="800" fill="#ffffff">f</text>
  <g transform="translate({ICON+3},0)" fill="none" stroke="{NAVY}" stroke-width="1.1">
    <rect x="0.55" y="0.55" width="{ICON-1.1}" height="{ICON-1.1}" rx="2.6"/>
    <circle cx="{ICON/2}" cy="{ICON/2}" r="2.1"/>
    <circle cx="{ICON-2.4}" cy="2.4" r="0.55" fill="{NAVY}" stroke="none"/>
  </g>
</g>
<text x="{soc_x+2*ICON+3+4:.2f}" y="{soc_y}" font-size="{soc_size}" font-weight="600"
      fill="{NAVY}">{SOCIAL}</text>


<!-- right: Elephant House -->
<g transform="translate({el_cx-el_w/2-EL_X*el_s:.2f},{el_y-EL_Y*el_s:.2f}) scale({el_s:.6f})">{eleph}</g>
<text x="{el_cx}" y="{el_y+el_h+22:.1f}" text-anchor="middle" font-size="15" font-weight="700"
      fill="{INK}">Elephant House</text>
<text x="{el_cx}" y="{el_y+el_h+36:.1f}" text-anchor="middle" font-size="8.5" font-weight="500"
      letter-spacing="0.4" fill="{MUTED}">proudly supports Chimalaya</text>
'''

def document(bleed):
    b = bleed
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W+2*b}mm" height="{H+2*b}mm"
     viewBox="{-b} {-b} {W+2*b} {H+2*b}" font-family="Inter">
<title>Chimalaya at Elephant House - shelf banner 100 x 25 cm</title>
<defs>
  <symbol id="chimmark" viewBox="0 0 124.04 124.04">{chim_mark}</symbol>
  <clipPath id="frame"><rect x="{-b}" y="{-b}" width="{W+2*b}" height="{H+2*b}"/></clipPath>
</defs>
{body(bleed)}
</svg>
'''

open(OUT + '.svg', 'w').write(document(0))
print(f'{OUT}.svg: {W} x {H} mm')

open(OUT + '-print.svg', 'w').write(document(BLEED))
print(f'{OUT}-print.svg: {W+2*BLEED} x {H+2*BLEED} mm incl. {BLEED} mm bleed')

inkscape = shutil.which('inkscape')
if inkscape:
    # live text, with Inter embedded in the PDF
    subprocess.run([inkscape, OUT + '-print.svg', '--export-type=pdf', '-o', OUT + '-print.pdf'],
                   check=True, stderr=subprocess.DEVNULL)
    print(f'{OUT}-print.pdf: {W+2*BLEED} x {H+2*BLEED} mm incl. {BLEED} mm bleed, fonts embedded')
else:
    print('inkscape not found: skipped the print PDF')
