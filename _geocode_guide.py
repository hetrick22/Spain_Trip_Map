"""Refresh guide coordinates from OpenStreetMap Nominatim, one request per second.

Review approximate matches before publishing. This script is optional for builds.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
import unicodedata

def key(name):
    return ''.join(c for c in unicodedata.normalize('NFKD', name.casefold()) if c.isalnum())

path = Path('san_sebastian_guide.json')
guide = json.loads(path.read_text(encoding='utf-8'))
existing = {key(p['name']): p for p in json.loads(Path('pois_geo.json').read_text(encoding='utf-8'))}
queries = {'Bergara': 'Bar Bergara, Donostia', 'Atari': 'Atari Gastroteka, Donostia',
           'Casa Vergara': 'Casa Vergara, Donostia'}
for venue in guide:
    if 'lat' in venue:
        continue
    old = existing.get(key(venue['name']))
    if old:
        venue['lat'], venue['lon'] = old['lat'], old['lon']
        venue['exact'] = old['exact']
        venue['coordinate_note'] = old.get('matched', venue['address'])
        print(venue['name'], 'existing pin', flush=True)
        continue
    query = queries.get(venue['name'], venue['address'])
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(
        {'q': query, 'format': 'json', 'limit': 3})
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'SpainTripMapUpdater/1.0 (personal trip map)'})
        results = json.loads(urllib.request.urlopen(request, timeout=12).read())
        if results:
            match = next((r for r in results if venue['name'].casefold() in r.get('name', '').casefold()), results[0])
            venue['lat'] = float(match['lat'])
            venue['lon'] = float(match['lon'])
            venue['exact'] = venue['name'].casefold() in match.get('name', '').casefold()
            venue['coordinate_note'] = match['display_name']
            print(venue['name'], 'exact' if venue['exact'] else 'address / approximate', venue['lat'], venue['lon'], flush=True)
        else:
            print(venue['name'], 'NO MATCH', flush=True)
    except Exception as error:
        print(venue['name'], type(error).__name__, str(error), flush=True)
    path.write_text(json.dumps(guide, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    time.sleep(1.1)
