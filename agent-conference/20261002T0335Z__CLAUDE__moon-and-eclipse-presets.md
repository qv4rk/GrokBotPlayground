signer: CLAUDE
ts: 2026-10-02T03:35:00Z
re: 20261002T0217Z__CLAUDE__scale-orrery-proposal.md
status: done
branch: main

# Moon, Jupiter's moons, eclipse presets

At MJF's request.

- The orrery proposal has the Moon (Meeus ch. 47, within 0.01° of JPL Horizons 1801–2049) and Io, Europa, Ganymede, Callisto (fitted to Horizons, worst 1.3°).
- `atlas-cosmogram/data/eclipses.json` is rebuilt from NASA's catalogs. 17 of the 18 old day numbers landed on no eclipse. The "29 CE Jerusalem" preset had no eclipse at all; it is now 3 Apr 33 CE. Ids are unchanged apart from that one (`eclipse-33ce`).
- The live time dial reads `jd`, so its eclipse menu now jumps to the right moment. No atlas code changed.

Check: `node atlas-cosmogram/proposals/scale-orrery/check.mjs` (38 checks).
