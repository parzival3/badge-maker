# Builds an 8 x 4 ft flex banner as a single SVG. 1 user unit = 1 mm.
import re, sys, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHIMALAYA = os.path.join(REPO, 'assets', 'logo.svg')
NKFMH = os.path.join(REPO, 'assets', 'nkfmh-logo.svg')

W, H = 2438.4, 1219.2          # 8 ft x 4 ft
NAVY, CRIMSON = '#123f6b', '#e50046'
INK, MUTED, GOLD = '#16233a', '#5b6b80', '#f0a81e'

def inline(path, strip_title=False):
    s = open(path).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    if strip_title:
        s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    return re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1).strip()

chim = inline(CHIMALAYA)   # viewBox 0 0 636.06 124.04
# the roundel alone, without the wordmark: the first three paths of that file
chim_mark = ''.join(re.findall(r'<path[^>]*/>', chim)[:3])
hosp = inline(NKFMH, strip_title=True)                # viewBox 0 0 2048 2048

M      = 150
TOPBAR = 26
RULE_Y = H - 290
CXX    = W / 2
EMB    = 250

title_en = 'PNC home visit nurses training'
title_np = 'सुत्केरी गृहभ्रमण नर्स तालिम'
date_en  = '4&#8211;7 October 2026'
date_np  = 'आश्विन १८&#8211;२१, २०८३'
venue    = 'Chimalaya Charity Bode &#183; Nepal Korea Friendship Municipality Hospital'

chim_w = 790
chim_s = chim_w / 636.06
chim_y = H - 207

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm"
     viewBox="0 0 {W} {H}" font-family="Inter">
<title>PNC home visit nurses training - banner</title>
<defs>
  <symbol id="emblem" viewBox="0 0 2048 2048">{hosp}</symbol>
  <symbol id="chimmark" viewBox="0 0 124.04 124.04">{chim_mark}</symbol>
  <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
</defs>

<rect width="{W}" height="{H}" fill="#ffffff"/>

<g clip-path="url(#frame)">
  <!-- both marks bled off the side edges, balancing each other -->
  <use href="#chimmark" x="-700" y="-100" width="1300" height="1300" opacity="0.05"/>
  <use href="#emblem" x="{W-760}" y="-190" width="1480" height="1480" opacity="0.06"/>
</g>

<rect x="0" y="0" width="{W*0.62:.1f}" height="{TOPBAR}" fill="{NAVY}"/>
<rect x="{W*0.62:.1f}" y="0" width="{W*0.26:.1f}" height="{TOPBAR}" fill="{CRIMSON}"/>
<rect x="{W*0.88:.1f}" y="0" width="{W*0.12:.1f}" height="{TOPBAR}" fill="{GOLD}"/>

<text x="{CXX}" y="245" text-anchor="middle" font-size="46" font-weight="600"
      letter-spacing="14" fill="{CRIMSON}">TRAINING PROGRAMME</text>

<text x="{CXX}" y="430" text-anchor="middle" font-size="152" font-weight="700"
      fill="{NAVY}" letter-spacing="-2">{title_en}</text>

<text x="{CXX}" y="532" text-anchor="middle" font-size="68"
      font-family="Noto Sans Devanagari" fill="{INK}">{title_np}</text>

<rect x="{CXX-150}" y="608" width="300" height="7" fill="{CRIMSON}"/>

<text x="{CXX}" y="742" text-anchor="middle" font-size="86" font-weight="600"
      fill="{INK}">{date_en}</text>
<text x="{CXX}" y="824" text-anchor="middle" font-size="58"
      font-family="Noto Sans Devanagari" fill="{MUTED}">{date_np}</text>

<text x="{CXX}" y="918" text-anchor="middle" font-size="52" font-weight="500"
      fill="{MUTED}">{venue}</text>

<line x1="{M}" y1="{RULE_Y}" x2="{W-M}" y2="{RULE_Y}" stroke="#d7dee7" stroke-width="3"/>

<g transform="translate({M},{chim_y}) scale({chim_s:.6f})">{chim}</g>
<use href="#emblem" x="{W-M-EMB}" y="{H-285}" width="{EMB}" height="{EMB}"/>
</svg>
'''
open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'banner', 'pnc-training-banner-8x4ft.svg'), 'w').write(svg)
print(f'banner {W} x {H} mm written')
