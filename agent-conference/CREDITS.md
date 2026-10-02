# Credits

Append-only. One line per borrowed file.

- qv4rk/V space/planets.js, space/cosmos.js — FeistTech, same owner. Read for spin and orbital layout. Not copied yet.
- Three.js r160 (MIT) — https://github.com/mrdoob/three.js — already loaded via unpkg in atlas-cosmogram/index.html.
- Keplerian elements in the user spec follow the Meeus / JPL approximate-element pattern (public algorithms). Implementation in atlas-cosmogram/js/ephemeris.js is local.
- vasturiano/three-globe (MIT) example/img maps via jsDelivr — https://github.com/vasturiano/three-globe
- vasturiano/globe.gl (MIT) clouds.png and lunar maps via jsDelivr — https://github.com/vasturiano/globe.gl
- clouds.png credited upstream to https://github.com/turban/webgl-earth
- Natal freeze horizon split uses CODEX horizontalCoordinates in atlas-cosmogram/js/ephemeris.js (local Keplerian approx; Meeus/JPL-style elements already credited).
- The Scale Orrery (scale-orrery/index.html, pasted in by GROK) — Kepler solve, element-rate pattern, orbit-to-ecliptic rotation and (x, z, -y) scene mapping borrowed into atlas-cosmogram/proposals/scale-orrery/.
- E. M. Standish, JPL "Keplerian Elements for Approximate Positions of the Major Planets", Table 1 (1800–2050) — https://ssd.jpl.nasa.gov/planets/approx_pos.html — values in atlas-cosmogram/proposals/scale-orrery/elements.js.
- Planet radii: IAU WGCCRE 2015 / NASA planetary fact sheets. Saturn pole: IAU WGCCRE 2015. Values in atlas-cosmogram/proposals/scale-orrery/scale.js.
