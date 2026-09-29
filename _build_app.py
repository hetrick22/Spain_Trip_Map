import json, datetime, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
raw = json.loads((ROOT / 'raw.json').read_text(encoding='utf-8'))
pois = json.loads((ROOT / 'pois_geo.json').read_text(encoding='utf-8'))
guide = json.loads((ROOT / 'san_sebastian_guide.json').read_text(encoding='utf-8'))

def normal(name):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFKD', name.casefold()) if c.isalnum())

existing_restaurants = {normal(r['Restaurant']): r for r in raw['restaurants']}
existing_pois = {normal(p['name']): p for p in pois}
for venue in guide:
    name = venue['name']
    key = normal(name)
    if key not in existing_restaurants:
        row = {'City': venue['city'], 'Restaurant': name, 'Category': venue['style'],
               'Signature / Why go': venue['why'] + ' Try: ' + venue['orders'],
               'Price': venue['price'], 'Reservation': venue['booking'],
               'Interested?': None}
        raw['restaurants'].append(row)
        existing_restaurants[key] = row
    elif key not in (normal('Martín Berasategui'), normal('Asador Etxebarri')):
        row = existing_restaurants[key]
        row['Signature / Why go'] = venue['why'] + ' Try: ' + venue['orders']
        row['Price'] = venue['price']
        row['Reservation'] = venue['booking']
    if key not in existing_pois:
        if 'lat' not in venue or 'lon' not in venue:
            raise ValueError(f'Missing coordinates for {name}')
        pin = {'name': name, 'city': venue['city'], 'category': 'food',
               'raw_category': venue['style'], 'query': venue['address'],
               'daytrip': venue['area'] in ('Hondarribia', 'Getaria', 'Axpe, Atxondo'),
               'area': False, 'sources': {'restaurant': existing_restaurants[key]},
               'lat': venue['lat'], 'lon': venue['lon'], 'matched': venue['coordinate_note'],
               'exact': venue['exact']}
        pois.append(pin)
        existing_pois[key] = pin

for pin in pois:
    row = existing_restaurants.get(normal(pin['name']))
    if row:
        pin['sources']['restaurant'] = row

# ---------- city anchors (for map fit + city list) ----------
CITY_COORD = {
 'Madrid': (40.4168, -3.7038),
 'Granada': (37.1773, -3.5986),
 'Seville': (37.3891, -5.9845),
 'Lisbon': (38.7223, -9.1393),
 'Porto': (41.1579, -8.6291),
 'Haro': (42.5772, -2.8470),
 'San Sebastian': (43.3183, -1.9812),
}
LEG_CITY = ['Madrid','Granada','Seville','Lisbon','Porto','Haro','San Sebastian','Madrid']

# ---------- day-by-day ----------
def d(s): return datetime.date.fromisoformat(s)
legs = raw['itinerary']
days = []
for leg in legs:
    a, dep = d(leg['Arrive']), d(leg['Depart'])
    city = leg['City'].replace(' (start)','').replace(' (end)','').replace(' (La Rioja)','')
    n = (dep - a).days
    for i in range(n):
        dt = a + datetime.timedelta(days=i)
        days.append({
            'date': dt.isoformat(),
            'city': city,
            'leg': leg['Leg'],
            'drive': (leg['Drive from previous'] if i==0 and leg['Drive from previous'] not in (None,'-') else None),
            'km': leg['Approx km'] if i==0 else None,
            'time': leg['Approx drive time'] if i==0 and leg['Approx drive time'] != '-' else None,
            'lodging': leg.get('Lodging'),
            'events': [],
        })
days.append({'date':'2026-10-06','city':'Madrid','leg':None,'drive':None,'km':None,'time':None,
             'lodging':None,'events':[{'what':'Fly home to Seattle','when':None,'kind':'travel'}],'depart':True})

by_date = {x['date']: x for x in days}
for r in raw['reservations']:
    dd = r.get('Dining Date')
    if dd and dd in by_date:
        by_date[dd]['events'].append({
            'what': r['Restaurant / Booking'],
            'when': r.get('Time'),
            'kind': 'booking',
            'status': r.get('Status'),
            'note': r.get('Notes'),
        })
for x in days:
    x['events'].sort(key=lambda e: (e.get('when') or 'zz'))

# ---------- payload ----------
payload = {
 'meta': {
   'title': 'Spain & Portugal 2026',
   'dates': 'September 19 – October 6, 2026',
   'nights': 17,
   'km': 2659,
   'drive': '26 hr 10 min',
 },
 'itinerary': legs,
 'reservations': raw['reservations'],
 'restaurants': raw['restaurants'],
 'sights': raw['sights'],
 'notes': raw['notes'],
 'pois': pois,
 'sanSebastianGuide': guide,
 'days': days,
 'route': [{'city': c, 'lat': CITY_COORD[c][0], 'lon': CITY_COORD[c][1],
            'leg': legs[i]['Leg'], 'km': legs[i]['Approx km'],
            'time': legs[i]['Approx drive time'], 'nights': legs[i]['Nights']}
           for i, c in enumerate(LEG_CITY)],
 'cityCoord': {k: list(v) for k, v in CITY_COORD.items()},
}

TPL = (ROOT / 'template.html').read_text(encoding='utf-8')
out = TPL.replace('/*__DATA__*/', json.dumps(payload, ensure_ascii=False))
(ROOT / 'spain-portugal-2026.html').write_text(out, encoding='utf-8')
print('wrote', len(out), 'bytes |', len(pois), 'pois |', len(days), 'days')
