# Atlas & Cosmogram — status

Updated: 2026-09-30T22:18:00-04:00
Repo: qv4rk/GrokBotPlayground @ main `6756ef8`
Live: https://qv4rk.github.io/GrokBotPlayground/atlas-cosmogram/
V site: off limits.

Overwrite this file on the next checkpoint. Append a dated note in agent-conference/ when you do.

## Live on main

- Dual camera buttons (Planetary / Observer) wired in main.js
- Time dial: century–hour scrub, JD slider, eclipse presets
- Article nodes + ±50yr horizon + reading room (`?lang=ar|he|zh` passthrough)
- Natal freeze: form → lock T0 → beacon + rays + above/below list (GROKBOT, natal.js + scene-b hooks)
- Locales on article nodes: zh, ar, he (CHINESE / ARAB / HEBREW / PR)
- Ephemeris module present (JD + Kepler + horizontalCoordinates)
- Texture catalog in js/textures.js (jsDelivr three-globe + globe.gl maps)
- Pages workflow: .github/workflows/static.yml
- Chapter 1 spread: https://qv4rk.github.io/GrokBotPlayground/chapter-01/ (prose + panels; pptx on the page)
- Chapter 2 spread: https://qv4rk.github.io/GrokBotPlayground/chapter-02/
- Last code fix on main: scene prototype separators blocking boot (`6756ef8`)

## Scene wiring

- `js/scene.js` re-exports `CosmogramScene` from `scene-b.js`
- `scene-a.js` is still on disk and unused by boot

## Branches (unmerged lanes)

- `agent/arab-locales-expand`
- `agent/hebrew-locales-expand`
- `ccr-1566d58b-s4gcpi`

## Still open (build this next)

1. GROK — per-planet spin: own axis + sidereal period, same control path as Earth. Adapt qv4rk/V `space/planets.js`.
2. GROK — load MAPS from textures.js onto the live globe and body stand-ins (BODY_FILTER).
3. Anyone free — drop earth-sample binaries in `atlas-cosmogram/assets/earth-samples/` if they exist locally.
4. Wire or delete scene-a.js so there is one scene source of truth.
5. Solsys visual quality: planets still read as flat/dead until (1)+(2) land.

## Conference

Notes under `agent-conference/`. Handshake = pushed commit. Signer in the filename.
