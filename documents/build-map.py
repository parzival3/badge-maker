"""Draws the clinic locator map as an SVG, from OpenStreetMap data.

Geometry is fetched once with Overpass and cached next to this script; re-run
with --refresh to pull it again. Output: assets/clinic-map.svg

Data (c) OpenStreetMap contributors, ODbL. The attribution is drawn into the
map and must stay visible wherever the map is published.
"""
import base64, json, math, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'assets', 'osm-cache.json')
OUT = os.path.join(HERE, 'assets', 'clinic-map.svg')
OUT_SAT = os.path.join(HERE, 'assets', 'clinic-map-satellite.svg')
SAT_CACHE = os.path.join(HERE, 'assets', 'area-satellite.jpg')
UA = 'chimalaya-doc-map/1.0 (+https://chimalayanepal.org)'

# The clinic, from its plus code 7MV7M9RQ+6V (M9RQ+6V Madhyapur Thimi),
# which decodes to a ~14 m cell and falls inside the ward 8 boundary.
CLINIC = (27.690562, 85.389687)
WARD_REL = 16113837          # OSM relation "Madhyapur Thimi-08"

# map window: 4.8 km x 3.2 km around the ward
CX, CY = 85.3905, 27.6935
CLINIC_VIEW = (27.6945, 85.3905)
KM_W, KM_H = 3.9, 2.6
W, H = 900, 600

NAVY, CRIMSON, INK, MUTED = '#123f6b', '#e50046', '#16233a', '#5b6b80'

# Optional satellite inset of the clinic's immediate surroundings.
# Needs a Mapbox access token:  MAPBOX_TOKEN=pk.xxx python3 build-map.py
# Free satellite imagery (Sentinel-2) is 10 m per pixel, which at this scale
# prints as mush, so there is no open-licence fallback worth drawing.
MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN', '')
INSET_PX = 232          # size of the inset box on the map canvas
INSET_ZOOM = 17         # ~1.06 m/px at this latitude -> about 245 m across
INSET_CACHE = os.path.join(HERE, 'assets', 'clinic-satellite.png')


def satellite_tile():
    """Fetch (and cache) a satellite image centred on the clinic."""
    if os.path.exists(INSET_CACHE):
        return open(INSET_CACHE, 'rb').read()
    if not MAPBOX_TOKEN:
        return None
    lat, lon = CLINIC
    url = (f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/'
           f'{lon},{lat},{INSET_ZOOM},0/{INSET_PX}x{INSET_PX}@2x'
           f'?access_token={MAPBOX_TOKEN}&attribution=false&logo=false')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        png = r.read()
    open(INSET_CACHE, 'wb').write(png)
    return png


def inset_svg(x, y):
    """The inset box, or a note saying why it is not there."""
    png = satellite_tile()
    size = INSET_PX
    out = []
    if png is None:
        return [], False
    # Mapbox serves JPEG for satellite styles regardless of the requested
    # extension, so sniff the magic bytes rather than assume PNG.
    mime = 'image/jpeg' if png[:2] == b'\xff\xd8' else 'image/png'
    b64 = base64.b64encode(png).decode()
    out.append(f'<g>')
    out.append(f'<clipPath id="insetclip"><rect x="{x}" y="{y}" width="{size}" '
               f'height="{size}" rx="3"/></clipPath>')
    out.append(f'<image x="{x}" y="{y}" width="{size}" height="{size}" '
               f'clip-path="url(#insetclip)" preserveAspectRatio="xMidYMid slice" '
               f'href="data:{mime};base64,{b64}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" '
               f'fill="none" stroke="{NAVY}" stroke-width="2"/>')
    # the clinic sits at the centre of the fetched image by construction
    cxi, cyi = x + size / 2, y + size / 2
    out.append(f'<circle cx="{cxi}" cy="{cyi}" r="9" fill="none" stroke="#ffffff" '
               f'stroke-width="2.5" opacity="0.95"/>')
    out.append(f'<circle cx="{cxi}" cy="{cyi}" r="4" fill="{CRIMSON}" '
               f'stroke="#ffffff" stroke-width="1.5"/>')
    # scale: metres per pixel at this zoom and latitude
    mpp = 156543.03392 * math.cos(math.radians(CLINIC[0])) / (2 ** INSET_ZOOM)
    bar_m = 100
    bar_px = bar_m / mpp
    out.append(f'<rect x="{x+10}" y="{y+size-16}" width="{bar_px:.1f}" height="3.5" '
               f'fill="#ffffff" opacity="0.9"/>')
    out.append(f'<text x="{x+10+bar_px/2:.1f}" y="{y+size-20}" fill="#ffffff" '
               f'font-size="11" text-anchor="middle" opacity="0.95">{bar_m} m</text>')
    out.append(f'<text x="{x}" y="{y-7}" fill="{NAVY}" font-size="13" '
               f'font-weight="650">Around the clinic</text>')
    out.append('</g>')
    return out, True

QUERY = f"""
[out:json][timeout:180];
(
  rel({WARD_REL});
  way["highway"~"^(motorway|trunk|primary|secondary)$"]({CY-0.025},{CX-0.03},{CY+0.025},{CX+0.03});
  node["place"~"^(town|suburb|village|neighbourhood)$"]({CY-0.025},{CX-0.03},{CY+0.025},{CX+0.03});
);
out geom;
"""


def fetch():
    req = urllib.request.Request(
        'https://overpass-api.de/api/interpreter',
        data=urllib.parse.urlencode({'data': QUERY}).encode(),
        headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def load():
    if os.path.exists(CACHE) and '--refresh' not in sys.argv:
        return json.load(open(CACHE))
    data = fetch()
    json.dump(data, open(CACHE, 'w'))
    return data


# ---- projection: equirectangular, good enough over a few kilometres --------
COS = math.cos(math.radians(CY))
DEG_W = (KM_W / 2) / (111.32 * COS)
DEG_H = (KM_H / 2) / 111.32
LON0, LON1 = CX - DEG_W, CX + DEG_W
LAT0, LAT1 = CY - DEG_H, CY + DEG_H


def px(lon, lat):
    return ((lon - LON0) / (LON1 - LON0) * W,
            (LAT1 - lat) / (LAT1 - LAT0) * H)


def ring_of(rel):
    """Stitch a boundary relation's outer ways into one closed ring."""
    segs = [m['geometry'] for m in rel['members']
            if m.get('role') in ('outer', '') and 'geometry' in m]
    ring, segs = segs[0][:], segs[1:]
    while segs:
        for i, sg in enumerate(segs):
            if abs(sg[0]['lat'] - ring[-1]['lat']) < 1e-9 and abs(sg[0]['lon'] - ring[-1]['lon']) < 1e-9:
                ring += sg[1:]; segs.pop(i); break
            if abs(sg[-1]['lat'] - ring[-1]['lat']) < 1e-9 and abs(sg[-1]['lon'] - ring[-1]['lon']) < 1e-9:
                ring += list(reversed(sg))[1:]; segs.pop(i); break
        else:
            break
    return ring


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def main():
    els = load()['elements']
    rel = next(e for e in els if e['type'] == 'relation')
    roads = [e for e in els if e['type'] == 'way' and 'highway' in e.get('tags', {})]
    places = [e for e in els if e['type'] == 'node']

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}" font-family="Inter, sans-serif">',
           f'<rect width="{W}" height="{H}" fill="#f7f9fb"/>']

    # roads, widest class first so junctions read correctly
    style = {'trunk': (5.0, '#bcc8d6'), 'motorway': (5.0, '#bcc8d6'),
             'primary': (3.4, '#c8d2dd'), 'secondary': (2.3, '#d4dce5')}
    for cls in ('trunk', 'motorway', 'primary', 'secondary'):
        for r in roads:
            if r['tags'].get('highway') != cls:
                continue
            pts = ' '.join('%.1f,%.1f' % px(p['lon'], p['lat']) for p in r['geometry'])
            w, col = style[cls]
            out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" '
                       f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    # distance rings around the clinic, purely as scale
    cx, cy = px(CLINIC[1], CLINIC[0])
    per_km = W / KM_W
    for km in (0.5, 1.0, 1.5):
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{km*per_km:.1f}" fill="none" '
                   f'stroke="{NAVY}" stroke-width="1" stroke-dasharray="3 5" opacity="0.28"/>')
        out.append(f'<text x="{cx:.1f}" y="{cy - km*per_km + 13:.1f}" fill="{NAVY}" '
                   f'opacity="0.55" font-size="13" text-anchor="middle">{km:g} km</text>')

    # ward 8: the area Chimalaya works in
    ring = ring_of(rel)
    pts = ' '.join('%.1f,%.1f' % px(p['lon'], p['lat']) for p in ring)
    out.append(f'<polygon points="{pts}" fill="{CRIMSON}" fill-opacity="0.10" '
               f'stroke="{CRIMSON}" stroke-width="2.4" stroke-linejoin="round"/>')

    # place labels, skipping any that would sit on top of the clinic marker
    shown = {'Madhyapur Thimi', 'Sano Thimi', 'Nagdesh', 'Sirutar', 'Duwakot',
             'Mulpani', 'Gatthaghar', 'Balkumari', 'Radhe Radhe', 'Magar Gaun'}
    for n in places:
        name = n['tags'].get('name:en') or n['tags'].get('name', '')
        if name not in shown:
            continue
        x, y = px(n['lon'], n['lat'])
        if not (12 < x < W - 12 and 16 < y < H - 30) or math.hypot(x - cx, y - cy) < 46:
            continue
        big = n['tags'].get('place') in ('town', 'suburb')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{MUTED}" opacity="0.7"/>')
        out.append(f'<text x="{x:.1f}" y="{y - 7:.1f}" fill="{INK}" text-anchor="middle" '
                   f'font-size="{16 if big else 14}" font-weight="{600 if big else 400}" '
                   f'opacity="0.85">{esc(name)}</text>')

    # the clinic
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="#ffffff" opacity="0.9"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7.5" fill="{CRIMSON}" '
               f'stroke="#ffffff" stroke-width="2.5"/>')
    out.append(f'<text x="{cx:.1f}" y="{cy - 20:.1f}" fill="{NAVY}" text-anchor="middle" '
               f'font-size="17" font-weight="700">Chimalaya clinic, Bode</text>')

    # scale bar
    bx, by, bar = 26, H - 30, per_km
    out.append(f'<rect x="{bx}" y="{by}" width="{bar:.1f}" height="4" fill="{NAVY}" opacity="0.75"/>')
    out.append(f'<rect x="{bx}" y="{by}" width="{bar/2:.1f}" height="4" fill="#ffffff" opacity="0.75"/>')
    out.append(f'<rect x="{bx}" y="{by}" width="{bar:.1f}" height="4" fill="none" '
               f'stroke="{NAVY}" stroke-width="1" opacity="0.75"/>')
    out.append(f'<text x="{bx}" y="{by - 6}" fill="{MUTED}" font-size="12">0</text>')
    out.append(f'<text x="{bx+bar:.1f}" y="{by - 6}" fill="{MUTED}" font-size="12" '
               f'text-anchor="middle">1 km</text>')

    # north arrow
    nx, ny = W - 40, 52
    out.append(f'<path d="M{nx} {ny-26} L{nx+7} {ny} L{nx} {ny-6} L{nx-7} {ny} Z" '
               f'fill="{NAVY}" opacity="0.65"/>')
    out.append(f'<text x="{nx}" y="{ny+15}" fill="{MUTED}" font-size="12" '
               f'text-anchor="middle">N</text>')

    # satellite inset, top-left where the vector map is emptiest
    inset, has_inset = inset_svg(22, 34)
    out += inset

    # required attribution — Mapbox imagery adds its own, and it is not optional
    credit = ('© OpenStreetMap contributors · satellite © Mapbox © Maxar'
              if has_inset else '© OpenStreetMap contributors')
    out.append(f'<text x="{W-10}" y="{H-10}" fill="{MUTED}" font-size="11" '
               f'text-anchor="end" opacity="0.85">{credit}</text>')
    if not has_inset:
        print('note: no MAPBOX_TOKEN set, so the satellite inset was skipped')

    out.append('</svg>')
    open(OUT, 'w').write('\n'.join(out))
    print('wrote', OUT)



# --------------------------------------------------------------------------
# Variant 2: the same area on satellite imagery, with the ward drawn over it.
#
# The overlay is projected with the Web Mercator transform Mapbox itself uses,
# not the equirectangular approximation above, so the boundary sits exactly
# where it belongs rather than a few metres out.
# --------------------------------------------------------------------------

SAT_W, SAT_H = 900, 600
SAT_ZOOM = 15


def merc(lon, lat, zoom):
    """Web Mercator pixel coordinates at a given zoom (256 px tiles)."""
    n = 256 * 2 ** zoom
    x = (lon + 180.0) / 360.0 * n
    r = math.radians(lat)
    y = (1.0 - math.log(math.tan(r) + 1.0 / math.cos(r)) / math.pi) / 2.0 * n
    return x, y


def satellite_area():
    if os.path.exists(SAT_CACHE):
        return open(SAT_CACHE, 'rb').read()
    if not MAPBOX_TOKEN:
        return None
    lat, lon = CLINIC_VIEW
    url = (f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/'
           f'{lon},{lat},{SAT_ZOOM},0/{SAT_W}x{SAT_H}@2x'
           f'?access_token={MAPBOX_TOKEN}&attribution=false&logo=false')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        img = r.read()
    open(SAT_CACHE, 'wb').write(img)
    return img


def halo_text(x, y, txt, size, weight=400, anchor='middle', fill='#ffffff'):
    """Text legible over imagery: dark outline drawn under a light fill."""
    common = (f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
              f'text-anchor="{anchor}"')
    return [
        f'<text {common} fill="none" stroke="#0a1018" stroke-width="3.6" '
        f'stroke-linejoin="round" opacity="0.85">{esc(txt)}</text>',
        f'<text {common} fill="{fill}">{esc(txt)}</text>',
    ]


def build_satellite(els):
    img = satellite_area()
    if img is None:
        print('note: no MAPBOX_TOKEN and no cached imagery, skipping the '
              'satellite version of the map')
        return

    rel = next(e for e in els if e['type'] == 'relation')
    places = [e for e in els if e['type'] == 'node']

    # the transform Mapbox used: centre of the image is CLINIC_VIEW at SAT_ZOOM
    cx0, cy0 = merc(CLINIC_VIEW[1], CLINIC_VIEW[0], SAT_ZOOM)

    def P(lon, lat):
        x, y = merc(lon, lat, SAT_ZOOM)
        return (x - cx0) + SAT_W / 2, (y - cy0) + SAT_H / 2

    mime = 'image/jpeg' if img[:2] == b'\xff\xd8' else 'image/png'
    b64 = base64.b64encode(img).decode()

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SAT_W} {SAT_H}" '
           f'width="{SAT_W}" height="{SAT_H}" font-family="Inter, sans-serif">',
           f'<image x="0" y="0" width="{SAT_W}" height="{SAT_H}" '
           f'preserveAspectRatio="xMidYMid slice" href="data:{mime};base64,{b64}"/>']

    cx, cy = P(CLINIC[1], CLINIC[0])
    res = 156543.03392 * math.cos(math.radians(CLINIC_VIEW[0])) / (2 ** SAT_ZOOM)
    per_km = 1000.0 / res

    for km in (0.5, 1.0, 1.5):
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{km*per_km:.1f}" fill="none" '
                   f'stroke="#ffffff" stroke-width="1.1" stroke-dasharray="4 6" opacity="0.5"/>')
        out += halo_text(cx, cy - km * per_km + 14, f'{km:g} km', 12, 400)

    ring = ring_of(rel)
    pts = ' '.join('%.1f,%.1f' % P(p['lon'], p['lat']) for p in ring)
    out.append(f'<polygon points="{pts}" fill="{CRIMSON}" fill-opacity="0.18" '
               f'stroke="{CRIMSON}" stroke-width="3" stroke-linejoin="round"/>')

    shown = {'Madhyapur Thimi', 'Sano Thimi', 'Nagdesh', 'Sirutar', 'Duwakot',
             'Mulpani', 'Gatthaghar', 'Balkumari', 'Radhe Radhe', 'Magar Gaun'}
    for n in places:
        name = n['tags'].get('name:en') or n['tags'].get('name', '')
        if name not in shown:
            continue
        x, y = P(n['lon'], n['lat'])
        if not (14 < x < SAT_W - 14 and 18 < y < SAT_H - 34) or math.hypot(x - cx, y - cy) < 48:
            continue
        big = n['tags'].get('place') in ('town', 'suburb')
        out += halo_text(x, y - 7, name, 15 if big else 13, 650 if big else 400)

    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="none" '
               f'stroke="#ffffff" stroke-width="3"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="{CRIMSON}" '
               f'stroke="#ffffff" stroke-width="2"/>')
    out += halo_text(cx, cy - 22, 'Chimalaya clinic, Bode', 16, 700)

    bx, by = 26, SAT_H - 30
    out.append(f'<rect x="{bx}" y="{by}" width="{per_km:.1f}" height="4" fill="#ffffff" '
               f'opacity="0.9" stroke="#0a1018" stroke-width="0.8"/>')
    out += halo_text(bx + per_km / 2, by - 7, '1 km', 12, 400)

    nx, ny = SAT_W - 40, 50
    out.append(f'<path d="M{nx} {ny-24} L{nx+7} {ny} L{nx} {ny-6} L{nx-7} {ny} Z" '
               f'fill="#ffffff" stroke="#0a1018" stroke-width="0.8" opacity="0.9"/>')
    out += halo_text(nx, ny + 15, 'N', 12, 400)

    out += halo_text(SAT_W - 10, SAT_H - 10,
                     '© OpenStreetMap contributors · satellite © Mapbox © Maxar',
                     11, 400, anchor='end')
    out.append('</svg>')
    open(OUT_SAT, 'w').write('\n'.join(out))
    print('wrote', OUT_SAT)


if __name__ == '__main__':
    main()
    build_satellite(load()['elements'])
