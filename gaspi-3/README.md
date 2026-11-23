# GASPI 3.0 · territory viewer (pilot: Puerto Rico)

Live: https://qv4rk.github.io/GrokBotPlayground/gaspi-3/

A static page (HTML, CSS, plain JavaScript) with no build step. All content comes from
JSON, so a new territory is a new data file. You don't need to change the code.

## Folder layout

```
gaspi-3/
  index.html                 app shell: map on the left, one panel on the right (bottom sheet on phones)
  css/app.css                all styles; perspective colours are hues of equal weight with no red/green pairing
  js/app.js                  renders the panel, source-chain drawer, bottom sheet and map
  data/territories.json      list of territories the viewer knows about
  data/puerto-rico.json      the Puerto Rico record (schema gaspi-3.0/territory)
  data/puerto-rico.geojson   boundary geometry, class administrative_boundary (U.S. Census Bureau)
```

Open another territory with `?t=<id>`, for example `index.html?t=puerto-rico`. The viewer
loads `data/<id>.json` and `data/<id>.geojson`. Panel state is kept in the URL hash, for example
`#tab=modules&m=M2` or `#tab=perspectives&p=compare:A-PNP~A-PIP`.

## Data model (`schema: gaspi-3.0/territory`)

| Key | What it holds | Rule |
| --- | --- | --- |
| `territory` | name, summary, map focus, geometry files, named places | `focus` is a camera target only and is never drawn as a boundary |
| `core` | the nine universal indicators: population, administering actors, legislative voice, citizenship, international status, legal determinations, armed forces, displacement, status process | each value names its producer and date; when producers disagree, both values are kept |
| `modules` | 3 to 7 territory-specific topics, each with `tags` (mechanism vocabulary), a `chain` of steps, and optional `table` and `notes` | used only for issues the parties themselves raise |
| `actors` | every named party | no Side A or Side B |
| `perspectives` | each actor's own statements: `original`, `lang`, `literal`, `contextual`, `translator`, `context` | **only that actor's words**. Critiques belong to the actor who makes them |
| `findings` | court rulings and UN resolutions | kept apart from perspectives, with binding status |
| `disputes` | one question with each producer's answer side by side | never averaged |
| `timeline` | dated events | |
| `sources` | `S01` to `Snn`, with title, publisher, date, URL, type, language and access date | every `source_ids` reference must resolve. Citation numbers follow this order |

There is no composite score or ranking. Territories are compared through shared `tags` on modules.

## Adding a territory

1. Copy `data/puerto-rico.json` to `data/<id>.json` and replace the content.
2. Add `data/<id>.geojson`. Each feature needs `properties.class` set to one of `administrative_boundary`,
   `claimed_boundary`, `controlled_area`, `disputed_boundary`, `source_defined` or `approximate`.
   Only `administrative_boundary` has a style so far. Add a layer in `initMap` for the others.
3. Add the territory to `data/territories.json`.
4. Check that every `source_ids` entry exists in `sources` (the generator script used for Puerto Rico
   asserts this before writing the file).

## Moving it to the V site

The folder is self-contained and uses relative paths, so you can copy `gaspi-3/` anywhere.
It loads two things from outside: MapLibre GL 4.7.1 from unpkg and the OpenFreeMap "positron"
basemap. The panel still works if the map fails to load.

## Copyright

Quotations are short, attributed, and used for commentary. Full texts are linked, not copied.
Translations from Spanish are GASPI working translations and are labelled as such.
