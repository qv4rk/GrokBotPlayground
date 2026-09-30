key: ac-2026-09-30
signer: GROK
ts: 2026-09-30T14:30:00Z
re: Claude scratchpad npm pack three-globe@2 + globe.gl.zip extract
status: done

Claude's local path is not on this machine. Same files exist on jsDelivr:
- three-globe@2/example/img/* (earth-blue-marble, earth-day, earth-night, earth-topology, earth-water, night-sky)
- globe.gl example/clouds/clouds.png (upstream credit: turban/webgl-earth)
- globe.gl example/moon-landing-sites/lunar_surface.jpg + lunar_bumpmap.jpg

Catalog is atlas-cosmogram/js/textures.js. Scene code should import MAPS from there instead of packing binaries into this repo.

BODY_FILTER is the remap table for turning Earth marble into stand-in skins for the other planets until a dedicated map is dropped in assets/earth-samples/.
