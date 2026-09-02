const fs = require('fs');
const { JSDOM } = require('jsdom');

const file = '/sessions/practical-festive-darwin/mnt/outputs/spain-portugal-2026.html';
const html = fs.readFileSync(file, 'utf8');

let fail = 0, pass = 0;
const ok  = (c, m) => { c ? (pass++, console.log('  PASS  ' + m)) : (fail++, console.log('  FAIL  ' + m)); };

console.log('\n=== 1. static checks ===');
ok(!html.includes('/*__DATA__*/'), 'data placeholder was substituted');
ok((html.match(/<script/g) || []).length === 3, 'expected 3 script tags (leaflet, cluster, app)');
ok(!/\/\*__|__\*\//.test(html), 'no leftover build markers');

// syntax check the inline app script
const appScript = html.split('<script>')[1].split('</script>')[0];
fs.writeFileSync('/tmp/trip/_app.js', appScript);
try { new (require('vm').Script)(appScript); ok(true, 'inline script parses (no syntax errors)'); }
catch (e) { ok(false, 'inline script parses -- ' + e.message); }

// data payload
const D = JSON.parse(appScript.match(/const D = ([\s\S]*?);\n/)[1]);
console.log('\n=== 2. data payload ===');
ok(D.pois.length === 106, 'pois: ' + D.pois.length + ' (expect 106)');
ok(D.pois.every(p => typeof p.lat === 'number' && typeof p.lon === 'number'), 'every poi has numeric coords');
ok(D.pois.every(p => p.lat >= 36 && p.lat <= 44 && p.lon >= -9.6 && p.lon <= -1.5), 'every poi inside the Iberian bounding box');
ok(D.itinerary.length === 8, 'itinerary legs: ' + D.itinerary.length + ' (expect 8)');
ok(D.reservations.length === 29, 'reservations: ' + D.reservations.length);
ok(D.restaurants.length === 45, 'restaurants: ' + D.restaurants.length);
ok(D.sights.length === 46, 'sights: ' + D.sights.length);
ok(D.notes.length === 14, 'notes: ' + D.notes.length);
ok(D.days.length === 18, 'days: ' + D.days.length + ' (Sep 19 - Oct 6)');
ok(D.itinerary.reduce((s, l) => s + l.Nights, 0) === 17, 'nights sum to 17');
ok(D.itinerary.reduce((s, l) => s + (l['Approx km'] || 0), 0) === D.meta.km, 'km sum matches header stat (' + D.meta.km + ')');

console.log('\n=== 3. day-by-day derivation ===');
ok(D.days[0].date === '2026-09-19' && D.days[0].city === 'Madrid', 'first day = Sep 19 in Madrid');
ok(D.days[D.days.length - 1].date === '2026-10-06', 'last day = Oct 6 (fly home)');
const dates = D.days.map(d => d.date);
ok(new Set(dates).size === dates.length, 'no duplicate dates');
let contiguous = true;
for (let i = 1; i < dates.length; i++) {
  const prev = new Date(dates[i-1] + 'T00:00'), cur = new Date(dates[i] + 'T00:00');
  if ((cur - prev) / 86400000 !== 1) contiguous = false;
}
ok(contiguous, 'dates are contiguous, no gaps');
const find = d => D.days.find(x => x.date === d);
ok(find('2026-09-20').city === 'Granada', 'Sep 20 sleeps in Granada (not Madrid) -- sleep-city rule');
ok(find('2026-09-28').city === 'Haro', 'Sep 28 sleeps in Haro');
ok(find('2026-10-02').city === 'San Sebastian', 'Oct 2 (birthday dinner) in San Sebastian');
ok(find('2026-10-05').city === 'Madrid', 'Oct 5 back in Madrid');
const drives = D.days.filter(d => d.drive);
ok(drives.length === 7, 'seven drive days flagged: ' + drives.map(d => d.date.slice(5)).join(', '));

console.log('\n=== 4. confirmed bookings land on the right day ===');
const ev = d => (find(d).events || []).map(e => e.what);
ok(ev('2026-09-20').some(w => /ALHAMBRA/i.test(w)), 'Alhambra on Sep 20');
ok(ev('2026-09-25').some(w => /Prado/.test(w)), 'Prado on Sep 25');
ok(ev('2026-10-02').some(w => /Berasategui/.test(w)), 'Martin Berasategui on Oct 2');
ok(find('2026-09-20').events.find(e => /ALHAMBRA/i.test(e.what)).when === '5:00 PM', 'Alhambra time 5:00 PM preserved');
ok(find('2026-10-02').events.find(e => /Berasategui/.test(e.what)).when === '9:15 PM', 'Berasategui time 9:15 PM preserved');
const totalEvents = D.days.reduce((s, d) => s + d.events.length, 0);
ok(totalEvents === 6, 'six dated events placed (5 bookings + fly home), got ' + totalEvents);

console.log('\n=== 5. render the page with Leaflet stubbed ===');
const stubL = `
  const _mk=(x)=>({addTo:()=>_mk(),bindPopup:()=>_mk(),getLatLng:()=>({lat:0,lng:0}),getChildCount:()=>1});
  window.__added=0;
  window.L={
    map:()=>({setView(){return this},fitBounds(){return this},invalidateSize(){},addLayer(){},removeLayer(){},on(){}}),
    tileLayer:()=>_mk(), polyline:()=>_mk(), marker:()=>_mk(), divIcon:()=>({}),
    layerGroup:()=>({addTo:()=>_mk()}), latLngBounds:()=>({pad:()=>({})}),
    markerClusterGroup:()=>({addTo:()=>({clearLayers(){},addLayers(a){window.__added=a.length}}),clearLayers(){},addLayers(a){window.__added=a.length}})
  };`;
const testHtml = html
  .replace(/<script src="[^"]*"><\/script>/g, '')
  .replace('<script>', '<script>' + stubL);

const errs = [];
const dom = new JSDOM(testHtml, { runScripts: 'dangerously', pretendToBeVisual: true });
dom.window.addEventListener('error', e => errs.push(e.message));
const w = dom.window, doc = w.document;

ok(errs.length === 0, 'no runtime errors' + (errs.length ? ': ' + errs.join(' | ') : ''));
ok(doc.querySelectorAll('#nav button').length === 7, 'seven tabs rendered');
ok(doc.querySelectorAll('#stats .stat').length === 5, 'five header stats');
ok(doc.querySelectorAll('#legs .leg').length === 8, 'itinerary: 8 leg cards');
ok(doc.querySelectorAll('#days .day').length === 18, 'day-by-day: 18 day cards');
ok(doc.querySelectorAll('#qs .q').length === 14, 'open questions: 14 cards');
ok(doc.querySelectorAll('#t-res tbody tr').length === 29, 'reservations table: 29 rows');
ok(doc.querySelectorAll('#t-rest tbody tr').length === 45, 'restaurants table: 45 rows');
ok(doc.querySelectorAll('#t-sight tbody tr').length === 46, 'sights table: 46 rows');
ok(doc.querySelectorAll('#mapcity .chip').length >= 9, 'city filter chips rendered (' + doc.querySelectorAll('#mapcity .chip').length + ')');
ok(w.__added === 106, 'all 106 markers added to the cluster layer, got ' + w.__added);

console.log('\n=== 6. every table row resolves to a map pin ===');
const names = new Set(D.pois.map(p => p.name.trim().toLowerCase()));
const unlinked = [];
D.restaurants.forEach(r => { if (!names.has(r.Restaurant.trim().toLowerCase())) unlinked.push('restaurant: ' + r.Restaurant); });
D.sights.forEach(r => { if (!names.has(r['Site / Activity'].trim().toLowerCase())) unlinked.push('sight: ' + r['Site / Activity']); });
D.reservations.forEach(r => { if (!names.has(r['Restaurant / Booking'].trim().toLowerCase())) unlinked.push('reservation: ' + r['Restaurant / Booking']); });
ok(unlinked.length === 0, 'every table row has a matching pin' + (unlinked.length ? ' -- missing: ' + unlinked.join('; ') : ''));

console.log('\n=== 7. links ===');
const links = [...doc.querySelectorAll('a[href^="http"]')];
ok(links.length > 100, links.length + ' external links rendered');
ok(links.every(a => a.target === '_blank' && /noopener/.test(a.rel)), 'all external links are target=_blank rel=noopener');
const dirs = [...doc.querySelectorAll('.maplink')];
ok(dirs.length === 120, 'map links on table rows: ' + dirs.length);
ok(dirs.filter(a => /approx/.test(a.textContent)).length > 0, 'approximate pins are labelled as such in tables');

console.log('\n=== 8. accessibility / responsive spot-checks ===');
ok(/viewport-fit=cover/.test(html) && /width=device-width/.test(html), 'mobile viewport meta present');
ok(/@media \(max-width:720px\)/.test(html), 'mobile breakpoint present');
ok(/overflow-x:auto/.test(html), 'wide tables scroll inside their own container');
ok(doc.querySelector('input[type=search]').getAttribute('aria-label') !== null, 'search inputs have aria-labels');

console.log('\n' + '='.repeat(46));
console.log(`  ${pass} passed, ${fail} failed`);
console.log('='.repeat(46));
process.exit(fail ? 1 : 0);
