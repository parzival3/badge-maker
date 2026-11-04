# Builds the cream version of the 100 x 25 cm shelf header for the Chimalaya
# shelf at Elephant House, Kathmandu: a warm background, a large faded roundel
# behind the message, and the logo's tagline set light and apart from the
# wordmark. 1 user unit = 1 mm. The original white version is built by
# build-elephant-house-banner.py and is left as it is.
#
#   nix-shell -p "python3.withPackages (p: [p.qrcode])" \
#     --run "python3 banner/build-elephant-house-banner-cream.py"
#
# Writes the design SVG at trim size and a print SVG with 3 mm bleed, both with
# live text in Inter and Montserrat, so the print shop needs those fonts to open
# them. When Inkscape is on PATH it also writes a print PDF with the fonts
# embedded, which opens anywhere. Only the logo's wordmark is outlined, as it
# comes from the logo artwork.
import re, os, shutil, subprocess
import qrcode

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Outlined and cropped copy of cc_nepal_logo.svg; see build-elephant-house-banner.py
CHIMALAYA = os.path.join(REPO, 'assets', 'cc_nepal_logo-outlined.svg')
MARK = os.path.join(REPO, 'assets', 'logo.svg')   # the roundel, for the faded backdrop
ELEPHANT = os.path.join(REPO, 'assets', 'Elephant_house.svg')
OUT = os.path.join(REPO, 'banner', 'elephant-house-shelf-banner-100x25cm-cream')

W, H = 1000, 250               # trim size
BLEED = 3
NAVY, DEEP, CRIMSON = '#123f6b', '#0b2a49', '#e50046'
INK, MUTED = '#16233a', '#5b6b80'
CREAM = '#faf6f1'
# the backdrop roundel, drawn in tints of the cream rather than at low opacity,
# so it stays warm instead of turning grey-blue
TINT_DISC, TINT_STAR, TINT_CORE = '#f4ece6', '#f9f4ef', '#f6e6e4'
URL = 'https://chimalayanepal.org'
SOCIAL = '@chimalayacharity'         # the same handle on Facebook and Instagram
EH_EMAIL = 'elephanthousestore@gmail.com'
EH_SOCIAL = '@elephanthousenepal'       # the same handle on Facebook and Instagram

def inline(path):
    s = open(path).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'<sodipodi:namedview.*?(/>|</sodipodi:namedview>)', '', s, flags=re.S)
    return re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1).strip()

# Roundel and CHIMALAYA NEPAL only: the tagline words are the paths filled
# crimson inline (the roundel's own crimson comes from a class, so it stays).
# What is left measures 831 x 160.5 in the logo's units, the wordmark from x 242.
chim = re.sub(r'<path\s+style="[^"]*fill:#e50046"[^>]*/>', '', inline(CHIMALAYA))
CHIM_ROUNDEL, CHIM_TEXT_X = 160.5, 242

mark_paths = re.findall(r'<path[^>]*/>', inline(MARK))[:3]
tinted = ''.join(re.sub(r'class="[^"]*"', f'fill="{c}"', p)
                 for p, c in zip(mark_paths, (TINT_DISC, TINT_STAR, TINT_CORE)))

# The elephant is one path; its first subpath is a stray speck (see the other script).
eleph = inline(ELEPHANT).replace('m 77,39 v 1 h 3 l -3,-1 m 802,387', 'M 879,426', 1)
assert 'M 879,426' in eleph, 'Elephant_house.svg changed; update the speck fix'
EL_X, EL_Y, EL_W, EL_H = 76.2, 43.5, 821.1, 637.2

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
# left column: logo, light tagline, then the QR with its label
chim_x, chim_y = 37, 46
chim_s = 35 / CHIM_ROUNDEL                  # a 35 mm roundel
tag_x = chim_x + CHIM_TEXT_X * chim_s       # tagline aligned with the wordmark
qr_x, qr_y, qr_size = 69, 176, 62

# centre column, over the backdrop roundel
TX = 562
BACK_D = 392

# right column
el_w = 123
el_h = el_w * EL_H / EL_W
el_cx, el_y = 897, 64
el_s = el_w / EL_W

soc_y, soc_size, ICON = 226, 11, 9.5
soc_text_w = 0.555 * soc_size * len(SOCIAL)  # estimate for Inter SemiBold
soc_x = TX - (2 * ICON + 3 + 4 + soc_text_w) / 2

# Elephant House contact rows under its name: a small icon, then the text, the pair centred on el_cx
EH_SIZE, EH_ICON = 9.5, 8.5
def eh_row(y, text, icons=1):
    w = icons * EH_ICON + (icons - 1) * 3 + 3.5 + 0.55 * EH_SIZE * len(text)   # estimate for Inter Medium
    return el_cx - w / 2, y, w

eh_mail_x, eh_mail_y, _ = eh_row(220, EH_EMAIL)
eh_fb_x, eh_fb_y, _ = eh_row(236, EH_SOCIAL, icons=2)

def body(bleed):
    """Artwork in trim coordinates; the background runs into the bleed."""
    b = bleed
    return f'''
<rect x="{-b}" y="{-b}" width="{W+2*b}" height="{H+2*b}" fill="{CREAM}"/>

<g clip-path="url(#frame)">
  <use href="#backmark" x="{TX-BACK_D/2}" y="{H/2-BACK_D/2}" width="{BACK_D}" height="{BACK_D}"/>
</g>

<!-- left: Chimalaya Nepal, its tagline, and the QR to the website -->
<g transform="translate({chim_x},{chim_y}) scale({chim_s:.6f})">{chim}</g>
<g font-family="Montserrat" font-size="19" font-weight="400" letter-spacing="0.4" fill="{INK}">
  <text x="{tag_x:.2f}" y="118">IMPROVING MATERNAL</text>
  <text x="{tag_x:.2f}" y="141">AND CHILD HEALTH</text>
</g>
<g transform="translate({qr_x},{qr_y}) scale({qr_size/qr_n:.6f})">
  <path d="{qr_d}" fill="{DEEP}"/>
</g>
<text x="{qr_x+qr_size+12}" y="203" font-size="10" font-weight="600"
      letter-spacing="2" fill="{CRIMSON}">SCAN TO VISIT</text>
<text x="{qr_x+qr_size+12}" y="221" font-size="15" font-weight="600"
      fill="{DEEP}">chimalayanepal.org</text>

<!-- centre: the message -->
<text x="{TX}" y="53" text-anchor="middle" font-size="10" font-weight="600"
      letter-spacing="2.8" fill="{CRIMSON}">SHOP FOR A GOOD CAUSE</text>
<rect x="{TX-31}" y="63" width="62" height="3.2" fill="{CRIMSON}"/>
<text x="{TX}" y="108" text-anchor="middle" font-size="32" font-weight="800"
      letter-spacing="-0.4" fill="{DEEP}">Every purchase helps</text>
<text x="{TX}" y="145" text-anchor="middle" font-size="32" font-weight="800"
      letter-spacing="-0.4" fill="{DEEP}">mothers &amp; newborns</text>
<text x="{TX}" y="184" text-anchor="middle" font-size="12" font-weight="500"
      fill="{INK}">Sales of these products support Chimalaya Charity</text>
<text x="{TX}" y="201" text-anchor="middle" font-size="12" font-weight="500"
      fill="{INK}">and its health work in Bode, Bhaktapur</text>

<!-- Facebook and Instagram, then the handle they share -->
<g transform="translate({soc_x:.2f},{soc_y-ICON+1})">
  <circle cx="{ICON/2}" cy="{ICON/2}" r="{ICON/2}" fill="{DEEP}"/>
  <text x="{ICON/2+0.3}" y="{ICON-1.2}" text-anchor="middle" font-size="8.4" font-weight="800" fill="{CREAM}">f</text>
  <g transform="translate({ICON+3},0)" fill="none" stroke="{DEEP}" stroke-width="1.1">
    <rect x="0.55" y="0.55" width="{ICON-1.1}" height="{ICON-1.1}" rx="2.7"/>
    <circle cx="{ICON/2}" cy="{ICON/2}" r="2.2"/>
    <circle cx="{ICON-2.5}" cy="2.5" r="0.6" fill="{DEEP}" stroke="none"/>
  </g>
</g>
<text x="{soc_x+2*ICON+3+4:.2f}" y="{soc_y}" font-size="{soc_size}" font-weight="600"
      fill="{DEEP}">{SOCIAL}</text>

<!-- right: Elephant House -->
<g transform="translate({el_cx-el_w/2-EL_X*el_s:.2f},{el_y-EL_Y*el_s:.2f}) scale({el_s:.6f})">{eleph}</g>
<text x="{el_cx}" y="182" text-anchor="middle" font-size="16" font-weight="700"
      fill="{NAVY}">Elephant House</text>
<text x="{el_cx}" y="196" text-anchor="middle" font-size="9" font-weight="500"
      letter-spacing="0.3" fill="{MUTED}">proudly supports Chimalaya</text>
<rect x="{el_cx-26}" y="206" width="52" height="0.8" fill="{CRIMSON}"/>

<!-- Elephant House contact: email, then Facebook and Instagram -->
<g transform="translate({eh_mail_x:.2f},{eh_mail_y-EH_ICON+1.2:.2f})" fill="none" stroke="{DEEP}" stroke-width="1">
  <rect x="0.5" y="1.2" width="{EH_ICON-1}" height="{EH_ICON-2.9}" rx="1"/>
  <path d="M0.8,1.8 L{EH_ICON/2},{EH_ICON/2-0.2} L{EH_ICON-0.8},1.8"/>
</g>
<text x="{eh_mail_x+EH_ICON+3.5:.2f}" y="{eh_mail_y}" font-size="{EH_SIZE}" font-weight="500"
      fill="{DEEP}">{EH_EMAIL}</text>
<g transform="translate({eh_fb_x:.2f},{eh_fb_y-EH_ICON+1.2:.2f})">
  <circle cx="{EH_ICON/2}" cy="{EH_ICON/2}" r="{EH_ICON/2}" fill="{DEEP}"/>
  <text x="{EH_ICON/2+0.3}" y="{EH_ICON-1.1}" text-anchor="middle" font-size="7.8" font-weight="800" fill="{CREAM}">f</text>
</g>
<g transform="translate({eh_fb_x+EH_ICON+3:.2f},{eh_fb_y-EH_ICON+1.2:.2f})" fill="none" stroke="{DEEP}" stroke-width="1">
  <rect x="0.5" y="0.5" width="{EH_ICON-1}" height="{EH_ICON-1}" rx="2.4"/>
  <circle cx="{EH_ICON/2}" cy="{EH_ICON/2}" r="2"/>
  <circle cx="{EH_ICON-2.3}" cy="2.3" r="0.55" fill="{DEEP}" stroke="none"/>
</g>
<text x="{eh_fb_x+2*EH_ICON+6.5:.2f}" y="{eh_fb_y}" font-size="{EH_SIZE}" font-weight="500"
      fill="{DEEP}">{EH_SOCIAL}</text>
'''

def document(bleed):
    b = bleed
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W+2*b}mm" height="{H+2*b}mm"
     viewBox="{-b} {-b} {W+2*b} {H+2*b}" font-family="Inter">
<title>Chimalaya at Elephant House - shelf banner 100 x 25 cm, cream</title>
<defs>
  <symbol id="backmark" viewBox="0 0 124.04 124.04">{tinted}</symbol>
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
    # live text, with Inter and Montserrat embedded in the PDF
    subprocess.run([inkscape, OUT + '-print.svg', '--export-type=pdf', '-o', OUT + '-print.pdf'],
                   check=True, stderr=subprocess.DEVNULL)
    print(f'{OUT}-print.pdf: {W+2*BLEED} x {H+2*BLEED} mm incl. {BLEED} mm bleed, fonts embedded')
else:
    print('inkscape not found: skipped the print PDF')
