// node atlas-cosmogram/proposals/scale-orrery/check.mjs
// Checks the proposal's positions against dated events, and prints the live
// atlas ephemeris on the same events for comparison. No dependencies.

import { geocentric, heliocentric, eclipticToScene } from './elements.js';
import { dateToJulianDay, getGeoCoordinates } from '../../js/ephemeris.js';

const RAD = 180 / Math.PI;
const SUN_RADIUS_DEG = 0.267; // apparent solar radius, roughly, near 1 AU

const sep = (a, b) => {
  const dot = a.x * b.x + a.y * b.y + a.z * b.z;
  const n = Math.hypot(a.x, a.y, a.z) * Math.hypot(b.x, b.y, b.z);
  return Math.acos(Math.max(-1, Math.min(1, dot / n))) * RAD;
};
const dist = (v) => Math.hypot(v.x, v.y, v.z);
const sunGeo = (jd) => {
  const e = heliocentric('earth', jd);
  return { x: -e.x, y: -e.y, z: -e.z };
};

// [label, jd, measure(geo, jd) -> number, limit, unit]
// Event times are UT from published transit and opposition tables.
const onDisc = (body) => (geo, jd) => sep(geo(body, jd), geo('sun', jd));
const atlasGeo = (body, jd) => getGeoCoordinates(body, jd);
const propGeo = (body, jd) => (body === 'sun' ? sunGeo(jd) : geocentric(body, jd));

const CASES = [
  ['Venus transit, greatest, 1874-12-09 04:07', dateToJulianDay(1874, 12, 9, 4, 7), onDisc('venus'), SUN_RADIUS_DEG, 'deg from Sun centre'],
  ['Venus transit, greatest, 1882-12-06 17:06', dateToJulianDay(1882, 12, 6, 17, 6), onDisc('venus'), SUN_RADIUS_DEG, 'deg from Sun centre'],
  ['Venus transit, greatest, 2012-06-06 01:29', dateToJulianDay(2012, 6, 6, 1, 29), onDisc('venus'), SUN_RADIUS_DEG, 'deg from Sun centre'],
  ['Mercury transit, greatest, 2019-11-11 15:20', dateToJulianDay(2019, 11, 11, 15, 20), onDisc('mercury'), SUN_RADIUS_DEG, 'deg from Sun centre'],
  ['Jupiter-Saturn conjunction 2020-12-21 18:20 (0.10 deg)', dateToJulianDay(2020, 12, 21, 18, 20),
    (geo, jd) => sep(geo('jupiter', jd), geo('saturn', jd)), 0.25, 'deg apart'],
  ['Mars closest approach 2003-08-27 09:51 (0.37272 AU)', dateToJulianDay(2003, 8, 27, 9, 51),
    (geo, jd) => Math.abs(dist(geo('mars', jd)) - 0.37272), 0.001, 'AU off']
];

let failed = 0;
for (const [label, jd, measure, limit, unit] of CASES) {
  const p = measure(propGeo, jd);
  const a = measure(atlasGeo, jd);
  const ok = p <= limit;
  if (!ok) failed++;
  console.log(
    `${ok ? 'PASS' : 'FAIL'}  ${label}\n` +
    `      proposal ${p.toFixed(4)} ${unit} (limit ${limit})   live atlas ${a.toFixed(4)}`
  );
}

// Handedness: Earth moves counter-clockwise seen from +Y in scene space.
const s0 = eclipticToScene(heliocentric('earth', 2451545));
const s1 = eclipticToScene(heliocentric('earth', 2451545 + 10));
// The y component of s0 x s1 is positive for a counter-clockwise turn about +Y.
const crossY = s0.z * s1.x - s0.x * s1.z;
const ccw = crossY > 0;
if (!ccw) failed++;
console.log(`${ccw ? 'PASS' : 'FAIL'}  Earth orbits counter-clockwise about +Y in scene space`);

// Same test on the live atlas mapping (x, z, y) from scene-a.js.
const a0 = heliocentric('earth', 2451545), a1 = heliocentric('earth', 2451545 + 10);
const atlasCrossY = a0.y * a1.x - a0.x * a1.y;
console.log(`info  live atlas mapping (x, z, y) turns ${atlasCrossY > 0 ? 'counter-clockwise' : 'clockwise'} about +Y`);

process.exit(failed ? 1 : 0);
