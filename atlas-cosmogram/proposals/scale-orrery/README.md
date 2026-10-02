# The Scale Orrery: proposal for the atlas

Staged for MJF's review. The live atlas files stay as they are: boot, `index.html`, `scene-a.js`, `scene-b.js`, `ephemeris.js`.

- Page: `atlas-cosmogram/proposals/scale-orrery/index.html` (on Pages once this is on `main`: https://qv4rk.github.io/GrokBotPlayground/atlas-cosmogram/proposals/scale-orrery/)
- Check: `node atlas-cosmogram/proposals/scale-orrery/check.mjs`

## Files

| File | What it holds |
|---|---|
| `elements.js` | JPL Table 1 elements for eight planets, Kepler solve, heliocentric and geocentric positions, orbit paths, ecliptic-to-scene mapping |
| `scale.js` | Radii in km, the AU, and the two scale modes |
| `maps.js` | Surface maps: atlas Earth map, local files when present, generated maps until then, Saturn's ring |
| `orrery.js` | `ScaleOrrery`: a Three.js group with `setJulianDay(jd)` and `setScaleMode(mode)` |
| `index.html` | Review page with date, play/pause, scale toggle, focus, and an Earth-to-Sun view |
| `check.mjs` | Dated-event checks, run with Node, no dependencies |

## What came from The Scale Orrery

- **Element rates per century.** The source carried `da, de, di, dL, dW, dN`. The atlas holds elements fixed at J2000 and moves perihelion by a flat 0.5° a century. This proposal uses the full JPL Table 1 values for all eight planets.
- **The Kepler solve.** Same Newton iteration, with a better first guess.
- **The orbit-plane to ecliptic rotation.** Same matrix.
- **The ecliptic-to-scene mapping** `(x, y, z) → (x, z, −y)`. This one is a true rotation. See finding 1 below.
- **The visible/true toggle.** Rebuilt so that true is true (below).
- **The texture-load pattern**, for Earth only. The Earth map comes from the atlas catalog in `js/textures.js`.

## What stayed behind

- **The clock.** One day per frame with no stop. The orrery takes its time from the host: the atlas `TimeDial`, or the review page's own play/pause.
- **The scale numbers.** The source fixed the Sun at 3 units, multiplied "true" radii by 0.1, and set visible radii to `max(0.3, r × 0.2)`. In its true mode Earth was about 160× too large against its orbit, and the Sun was 2.7× Jupiter's radius (the real figure is 9.7×).
- **The texture URLs.** Checked 2026-10-02: Mercury 404 (and it pointed at the planet's symbol), Venus 404, Mars 429 from Wikimedia's hotlink limit, Jupiter a 42 KB photo of the disc where a map belongs. Only the Earth map loaded.
- **The spin** `rotation.y += 0.01`. Per-planet spin is GROK's open item 1 in `STATUS.md`.
- **The random-cube starfield.** The page uses the atlas `nightSky` map instead.
- **The light falloff.** A point light with a 500-unit range left Uranus and Neptune dark. The light here has no falloff.
- **The esm.sh import map.** The page uses the atlas import map (unpkg, three 0.160.0, same version).

## The two scale modes

Both modes use one unit for distance and radius: 15 scene units per AU, radii in km converted the same way.

- **Visible:** every planet ×1000, the Sun ×20. Planets stay in true proportion to each other. The panel prints the factors.
- **True:** nothing enlarged. Each body also gets a 5-pixel marker so it can be found. "Focus" flies to a body at six radii. "From Earth, look at the Sun" narrows the field to 1°, where the Sun is half a degree wide and Venus, in transit, is a dot on it.

The camera uses a logarithmic depth buffer, so true-scale Earth (0.00064 units) and Neptune's orbit (450 units) render in one scene.

## What the check shows

`check.mjs` tests positions against published events and prints the live atlas ephemeris on the same events.

| Event (UT) | Published | This proposal | Live atlas |
|---|---|---|---|
| Venus transit, 1874-12-09 04:07 | 0.230° from Sun centre | 0.231° | 0.404°, off the disc |
| Venus transit, 1882-12-06 17:06 | 0.177° | 0.176° | 0.396°, off the disc |
| Venus transit, 2012-06-06 01:29 | 0.154° | 0.154° | 0.153° |
| Mercury transit, 2019-11-11 15:20 | 0.021° | 0.023° | 0.077° |
| Jupiter-Saturn, 2020-12-21 18:20 | 0.10° apart | 0.11° | 0.15° |
| Mars closest, 2003-08-27 09:51 | 0.37272 AU | 0.37300 AU | 0.37298 AU |

The Sun's disc is about 0.27° in radius, so the atlas places both 19th-century transits of Venus beside the Sun. Both fall inside the book's years.

## Two findings about the live atlas

Left unchanged here. For MJF to decide.

1. **The planetary view is mirrored.** `scene-a.js` `_updatePlanetPositions` sets `(g.x, g.z, g.y)`. That swaps two axes, which is a reflection, so prograde orbits run clockwise seen from ecliptic north. `(g.x, g.z, -g.y)` corrects it. `check.mjs` prints the direction for both mappings.
2. **The ephemeris drifts by the 1870s.** Table above. `elements.heliocentric(body, jd)` returns the same `{x, y, z}` in AU as `getHelioCoordinates`, so it can replace the body of that function and correct the observer view and natal freeze too.

## Wiring it in, after approval

```js
import { ScaleOrrery } from './proposals/scale-orrery/orrery.js';
const orrery = new ScaleOrrery();
scene.add(orrery.group);
// wherever the atlas sets time:
orrery.setJulianDay(jd);
orrery.setScaleMode('true');
```

The atlas frame is Earth-centred with Earth at radius 1. The orrery is Sun-centred at 15 units per AU. The cleanest fit is a third camera button, Orrery, that shows `orrery.group` and hides the globe, the way Observer swaps frames now.

## Limits

- Elements are valid 1800–2050. Outside that range the page says so. Earlier dates need JPL Table 2a with its extra terms for Jupiter through Neptune. The book's chapters run 1801–1938, inside the range.
- Earth is the Earth-Moon barycentre, about 4,700 km from Earth's centre. No Moon yet.
- UT is used as TDB. The gap is under a minute across 1800–2050.
- Planets hold still on their axes until spin lands. Saturn's ring is tilted to Saturn's IAU pole.
- Planet maps are generated for every body but Earth. Real maps go in `atlas-cosmogram/assets/planet-maps/` under the names in `maps.js` (`2k_mars.jpg` and so on) and load on their own. Solar System Scope's 2k set is CC BY 4.0 and fits. Their site returned a captcha to this container, so the files need a download by hand and a line in `agent-conference/CREDITS.md`. Until then the browser console lists a 404 for each missing map.
