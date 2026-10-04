"""Draws the clinic locator map as an SVG, from OpenStreetMap data.

Geometry is fetched once with Overpass and cached next to this script; re-run
with --refresh to pull it again. Output: assets/clinic-map.svg

Data (c) OpenStreetMap contributors, ODbL. The attribution is drawn into the
map and must stay visible wherever the map is published.
"""
import json, math, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'assets', 'osm-cache.json')
OUT = os.path.join(HERE, 'assets', 'clinic-map.svg')
UA = 'chimalaya-doc-map/1.0 (+https://chimalayanepal.org)'

# The clinic, from its plus code 7MV7M9RQ+6V (M9RQ+6V Madhyapur Thimi),
# which decodes to a ~14 m cell and falls inside the ward 8 boundary.
CLINIC = (27.690562, 85.389687)
WARD_REL = 16113837          # OSM relation "Madhyapur Thimi-08"

# map window: 4.8 km x 3.2 km around the ward
CX, CY = 85.3905, 27.6935
KM_W, KM_H = 3.9, 2.6
W, H = 900, 600

NAVY, CRIMSON, INK, MUTED = '#123f6b', '#e50046', '#16233a', '#5b6b80'

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

    # required attribution
    out.append(f'<text x="{W-10}" y="{H-10}" fill="{MUTED}" font-size="11" '
               f'text-anchor="end" opacity="0.85">© OpenStreetMap contributors</text>')

    out.append('</svg>')
    open(OUT, 'w').write('\n'.join(out))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
