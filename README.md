# Spain & Portugal 2026 trip map

The public page is [`spain-portugal-2026.html`](spain-portugal-2026.html). GitHub Pages serves it from `main` at [the live trip map](https://hetrick22.github.io/Spain_Trip_Map/spain-portugal-2026.html).

## Maintained sources

- `template.html`: page layout, map, filters, and restaurant guide UI.
- `raw.json`: itinerary, reservations, restaurants, sights, and notes recovered from the previously published page. The workbook named in the old footer is not present in this checkout.
- `pois_geo.json`: original geocoded map places recovered from the previously published page.
- `san_sebastian_guide.json`: researched San Sebastián venue details, sources, dates checked, and coordinates. This file enriches matching restaurant rows and supplies new rows and pins during the build.

The older `_build_pois.py` and `_merge_geo.py` reference unavailable scratch files and are archival. The current build uses the three JSON sources above.

## Build and check

From the repository root:

```powershell
python _build_app.py
node _verify.js
```

The build writes `spain-portugal-2026.html` in place. The verification script checks the generated JavaScript, map/restaurant links, travel dates, and booking statuses without extra packages.

Venue hours, menus, and prices can change. The guide identifies estimates and items needing direct confirmation. Its suggested dinners are not reservations. The listed coordinates come from OpenStreetMap Nominatim or the original map data; approximate matches are marked in the guide and map.
