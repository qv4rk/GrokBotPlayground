/* GASPI 3.0 territory viewer. Plain JS, no build step.
   Data: data/<territory>.json (schema gaspi-3.0/territory). */
(function(){
  "use strict";
  const params = new URLSearchParams(location.search);
  const TID = (params.get("t") || "puerto-rico").replace(/[^a-z0-9-]/g, "");
  const TABS = [["core","Core"],["modules","Modules"],["perspectives","Perspectives"],["timeline","Timeline"],["sources","Sources"]];
  const HUES = ["--p1","--p2","--p3","--p4","--p5","--p6"];
  let D = null, SRC = {}, SNUM = {}, map = null;
  const state = { tab:"core", pmode:"all", pactor:null, pcompare:[], openMods:new Set(), year:null };

  // tiny DOM helper; text is always set with textContent
  function h(tag, attrs, ...kids){
    const el = document.createElement(tag);
    if (attrs) for (const [k,v] of Object.entries(attrs)){
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "text") el.textContent = v;
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else if (k === "style") el.setAttribute("style", v);
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()){
      if (kid == null || kid === false) continue;
      el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
    }
    return el;
  }
  const $ = (id) => document.getElementById(id);

  function cites(ids, claim, extra){
    return (ids || []).map(id => h("button", {class:"cite", type:"button", title: SRC[id] ? SRC[id].title : id,
      "aria-label": "Source " + SNUM[id], onclick: () => openChain(id, claim, extra)}, String(SNUM[id])));
  }
  function citesFooter(ids){
    const uniq = [...new Set(ids)].sort((a,b) => SNUM[a]-SNUM[b]);
    if (!uniq.length) return null;
    return h("details", {class:"cites"},
      h("summary", null, `Sources cited on this tab (${uniq.length})`),
      h("ol", {class:"srcs"}, uniq.map(id => srcLi(id))));
  }
  function srcLi(id){
    const s = SRC[id];
    return h("li", {value: SNUM[id]},
      s.author ? s.author + ". " : "", h("span", {class:"t"}, s.title), ". ", s.publisher, ", ", s.date, ". ",
      h("a", {href:s.url, target:"_blank", rel:"noopener"}, "Open"), " · ",
      h("button", {class:"cite", type:"button", onclick:() => openChain(id)}, "chain"));
  }
  function collect(o, out){
    if (Array.isArray(o)) o.forEach(x => collect(x, out));
    else if (o && typeof o === "object") for (const [k,v] of Object.entries(o)){
      if (k === "source_ids") out.push(...v); else collect(v, out);
    }
    return out;
  }
  const actor = (id) => D.actors.find(a => a.id === id);
  const hue = (actorId) => `var(${HUES[D.perspectives.findIndex(p => p.actor_id === actorId) % HUES.length]})`;

  // ---------- tabs ----------
  function renderTabs(){
    const t = $("tabs"); t.textContent = "";
    TABS.forEach(([id,label]) => t.append(h("button", {class:"tab", role:"tab", type:"button",
      "aria-selected": String(state.tab === id), onclick: () => { state.tab = id; syncHash(); render(); $("panelBody").scrollTop = 0; }}, label)));
  }
  function render(){
    renderTabs();
    const b = $("panelBody"); b.textContent = "";
    ({core:renderCore, modules:renderModules, perspectives:renderPerspectives, timeline:renderTimeline, sources:renderSources})[state.tab](b);
  }

  function renderCore(b){
    b.append(h("div", {class:"legend"}, h("i"), "Administrative boundary, U.S. Census Bureau 2023", ...cites(["S43"], "Map geometry: Puerto Rico boundary")));
    b.append(h("h2", null, "Universal core"));
    b.append(h("p", {class:"muted small"}, "The same nine facts are recorded for every GASPI territory. Each value names who produced it. Where producers differ, both values are shown."));
    D.core.forEach(c => {
      b.append(h("div", {class:"core-row"},
        h("div", {class:"core-label"}, c.label),
        c.values.map(v => h("div", {class:"val"}, v.value, ...cites(v.source_ids, c.label + ": " + v.value),
          h("span", {class:"prod"}, [v.producer, v.method, v.date].filter(Boolean).join(" · ")))),
        c.note ? h("div", {class:"note small"}, c.note) : null));
    });
    b.append(h("p", {class:"note"}, "GASPI 3.0 publishes no composite score or ranking. Comparison across territories works through shared mechanism tags on the modules."));
    b.append(citesFooter(collect(D.core, ["S43"])));
  }

  function renderModules(b){
    b.append(h("h2", null, "What this dispute is about"));
    b.append(h("p", {class:"muted small"}, "Modules are chosen for Puerto Rico because the parties themselves name these issues. Each one follows the chain from law to decision to each side's account."));
    D.modules.forEach(m => {
      const open = state.openMods.has(m.id);
      const card = h("article", {class:"mod" + (open ? " open" : ""), id:"mod-" + m.id});
      card.append(h("button", {class:"mod-head", type:"button", "aria-expanded": String(open), onclick: () => {
          open ? state.openMods.delete(m.id) : state.openMods.add(m.id); syncHash(); render();
          const el = $("mod-" + m.id); if (el) el.scrollIntoView({block:"nearest"}); }},
        h("span", {class:"chev", "aria-hidden":"true"}, "›"),
        h("div", {class:"mod-title"}, m.title),
        h("p", {class:"mod-sum"}, m.summary),
        h("div", {class:"tags"}, m.tags.map(t => h("span", {class:"tag"}, t.replace(/_/g," "))))));
      const body = h("div", {class:"mod-body"});
      if (m.table && m.table.columns.length > 3){
        body.append(h("div", {class:"rowcards"}, m.table.rows.map(r => h("div", {class:"rowcard"},
          h("div", {class:"rc-title"}, r.cells[0], ...cites(r.source_ids, r.cells.join(" · "))),
          m.table.columns.slice(1).map((c,i) => h("div", {class:"rc-line"}, h("span", {class:"rc-k"}, c), h("span", null, r.cells[i+1])))))));
      } else if (m.table){
        body.append(h("table", {class:"data"},
          h("thead", null, h("tr", null, m.table.columns.map(c => h("th", null, c)), h("th", null, ""))),
          h("tbody", null, m.table.rows.map(r => h("tr", null, r.cells.map(c => h("td", null, c)), h("td", null, cites(r.source_ids, r.cells.join(" · "))))))));
      }
      body.append(h("ol", {class:"chain"}, m.chain.map(c => h("li", null,
        h("div", {class:"step"}, c.step), h("div", {class:"step-text"}, c.text, ...cites(c.source_ids, c.text))))));
      (m.notes || []).forEach(n => body.append(h("div", {class:"side-note"}, h("b", null, n.title), h("p", null, n.text, ...cites(n.source_ids, n.text)))));
      const dmap = {M2:["D2"], M5:["D4"], M6:["D3"], M7:["D1"]}[m.id] || [];
      D.disputes.filter(d => dmap.includes(d.id)).forEach(d => body.append(renderDispute(d)));
      if (m.id === "M1" && map) body.append(h("button", {class:"fly", type:"button", onclick: () => flyHome()}, "Show Puerto Rico on the map"));
      card.append(body);
      b.append(card);
    });
    const vq = (D.territory.places || []).find(p => p.id === "vieques");
    if (vq && map) b.append(h("button", {class:"fly", type:"button", onclick: () => map.flyTo({center: vq.center, zoom: vq.zoom})}, "Zoom to Vieques (former naval training area)"));
    b.append(citesFooter(collect([D.modules, D.disputes], [])));
  }
  function renderDispute(d){
    return h("div", {class:"dispute"}, h("h4", null, "Dispute: " + d.question),
      d.positions.map(p => h("div", {class:"pos"}, h("div", {class:"who"}, p.holder), h("div", null, p.value, ...cites(p.source_ids, p.holder + ": " + p.value)))));
  }

  function renderPerspectives(b){
    b.append(h("h2", null, "Perspectives"));
    b.append(h("p", {class:"muted small"}, D.layer_rule));
    const sw = h("div", {class:"pswitch", role:"group", "aria-label":"Perspective view"});
    [["all","All"],["single","Single"],["compare","Compare"]].forEach(([k,l]) => sw.append(h("button", {type:"button", "aria-pressed": String(state.pmode === k),
      onclick: () => { state.pmode = k; if (k === "single" && !state.pactor) state.pactor = D.perspectives[0].actor_id;
        if (k === "compare" && state.pcompare.length < 2) state.pcompare = D.perspectives.slice(0,2).map(p => p.actor_id); syncHash(); render(); }}, l)));
    b.append(sw);
    if (state.pmode !== "all"){
      const chips = h("div", {class:"chips"});
      D.perspectives.forEach(p => {
        const a = actor(p.actor_id);
        const on = state.pmode === "single" ? state.pactor === p.actor_id : state.pcompare.includes(p.actor_id);
        chips.append(h("button", {class:"chip", type:"button", style:`--c:${hue(p.actor_id)}`, "aria-pressed": String(on), onclick: () => {
          if (state.pmode === "single") state.pactor = p.actor_id;
          else { const i = state.pcompare.indexOf(p.actor_id);
            if (i >= 0) { if (state.pcompare.length > 2) state.pcompare.splice(i,1); }
            else { state.pcompare.push(p.actor_id); if (state.pcompare.length > 3) state.pcompare.shift(); } }
          syncHash(); render(); }}, a.name_en || a.name));
      });
      b.append(chips);
      if (state.pmode === "compare") b.append(h("p", {class:"muted small"}, "Pick two or three. Statements are shown side by side as each actor made them; GASPI does not align or score them."));
    }
    let list = D.perspectives;
    if (state.pmode === "single") list = list.filter(p => p.actor_id === state.pactor);
    if (state.pmode === "compare") list = state.pcompare.map(id => list.find(p => p.actor_id === id)).filter(Boolean);
    const wrap = state.pmode === "compare" ? h("div", {class:"compare"}) : b;
    list.forEach(p => wrap.append(renderPersp(p)));
    if (wrap !== b) b.append(wrap);

    const f = h("section", {class:"findings"}, h("div", {class:"eyebrow"}, "Findings layer"),
      h("h2", null, "Court and UN determinations"),
      h("p", {class:"muted small"}, "These are rulings and resolutions by bodies with formal authority. They are kept apart from the actors above."));
    D.findings.forEach(x => f.append(h("div", {class:"finding"}, h("div", {class:"fh"}, x.title),
      h("div", {class:"fm"}, [x.body, x.date, x.binding].join(" · ")), h("p", null, x.text, ...cites(x.source_ids, x.title + ": " + x.text)))));
    b.append(f);
    b.append(citesFooter(collect([D.perspectives, D.findings], [])));
  }
  function renderPersp(p){
    const a = actor(p.actor_id);
    return h("section", {class:"persp", style:`--c:${hue(p.actor_id)}`},
      h("h3", null, a.name), h("div", {class:"pl"}, "Position: " + a.position_label),
      p.statements.map(s => h("blockquote", null,
        h("div", {class:"q", lang:s.lang}, "“" + s.original + "”", ...cites(s.source_ids, "Statement by " + s.speaker, s)),
        s.literal ? h("div", {class:"tr"}, h("b", null, "Literal"), s.literal) : null,
        s.contextual ? h("div", {class:"tr"}, h("b", null, "Contextual"), s.contextual) : null,
        h("div", {class:"who"}, "— " + s.speaker + (s.context ? ". " + s.context : "")))));
  }

  function renderTimeline(b){
    const years = D.timeline.map(t => parseInt(t.date.slice(0,4),10));
    const min = Math.min(...years), max = Math.max(...years);
    const y = state.year || max;
    b.append(h("h2", null, "Timeline"));
    const out = h("output", null, String(y));
    const rng = h("input", {type:"range", min, max, value:y, "aria-label":"Show events up to year", oninput: (e) => { state.year = +e.target.value; out.textContent = e.target.value; draw(); }});
    b.append(h("div", {class:"scrub"}, h("span", null, String(min)), rng, out));
    const ul = h("ul", {class:"tl"}); b.append(ul);
    function draw(){
      ul.textContent = "";
      D.timeline.filter(t => parseInt(t.date.slice(0,4),10) <= (state.year || max)).forEach(t =>
        ul.append(h("li", null, h("span", {class:"d"}, t.date), h("span", null, t.event, ...cites(t.source_ids, t.date + ": " + t.event)))));
    }
    draw();
    b.append(citesFooter(collect(D.timeline, [])));
  }

  function renderSources(b){
    b.append(h("h2", null, `Sources (${D.sources.length})`));
    b.append(h("p", {class:"muted small"}, "Every claim on this page links to one of these. Open a source chain to see the claim, the document, and any original-language text and translation."));
    b.append(h("ol", {class:"srcs"}, D.sources.map(s => srcLi(s.id))));
    b.append(h("p", {class:"footer"}, "Data: ", h("a", {href:`data/${TID}.json`}, `data/${TID}.json`), " · Geometry: ", h("a", {href:`data/${TID}.geojson`}, `data/${TID}.geojson`), ". Short quotations are used for commentary and are attributed; full texts are linked, not copied."));
  }

  // ---------- source chain drawer ----------
  function openChain(id, claim, st){
    const s = SRC[id]; const body = $("drawerBody"); body.textContent = "";
    const step = (k, v) => v ? h("div", {class:"chainstep"}, h("div", {class:"k"}, k), h("div", {class:"v"}, v)) : null;
    const relF = D.findings.filter(f => f.source_ids.includes(id));
    const relD = D.disputes.filter(d => d.positions.some(p => p.source_ids.includes(id)));
    body.append(...[
      step("Claim", claim || "All claims citing this source"),
      step("Source", h("span", null, `[${SNUM[id]}] `, s.author ? s.author + ". " : "", s.title, ". ", s.publisher, ", ", s.date, ". ", h("a", {href:s.url, target:"_blank", rel:"noopener"}, "Open document"))),
      step("Type and language", `${s.type} · ${s.lang} · accessed ${s.accessed}`),
      st && st.original ? step("Original", h("span", {lang: st.lang}, "“" + st.original + "”")) : null,
      st && st.literal ? step("Literal translation", st.literal) : null,
      st && st.contextual ? step("Contextual translation", st.contextual) : null,
      st && (st.translator || st.context) ? step("Notes", [st.translator, st.context].filter(Boolean).map(x => /[.!?]$/.test(x) ? x : x + ".").join(" ")) : null,
      s.note ? step("Source note", s.note) : null,
      relF.length ? step("Findings using this source", relF.map(f => f.title).join("; ")) : null,
      relD.length ? step("Disputes using this source", relD.map(d => d.question).join("; ")) : null].filter(Boolean));
    const dr = $("drawer"); dr.classList.add("open"); dr.setAttribute("aria-hidden","false");
    const p = $("panel"); if (window.matchMedia("(max-width: 820px)").matches && p.dataset.snap === "peek") p.dataset.snap = "mid";
    $("drawerBack").focus();
  }
  function closeChain(){ const dr = $("drawer"); dr.classList.remove("open"); dr.setAttribute("aria-hidden","true"); }
  $("drawerBack").addEventListener("click", closeChain);
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeChain(); });

  // ---------- bottom sheet (mobile) ----------
  (function sheet(){
    const p = $("panel"), hd = $("sheetHandle"); const order = ["peek","mid","full"];
    hd.addEventListener("click", () => { const i = order.indexOf(p.dataset.snap); p.dataset.snap = order[(i+1) % 3]; });
    let y0 = null, t0 = 0;
    hd.addEventListener("pointerdown", e => { y0 = e.clientY; t0 = Date.now(); hd.setPointerCapture(e.pointerId); });
    hd.addEventListener("pointerup", e => {
      if (y0 == null) return; const dy = e.clientY - y0; y0 = null;
      if (Math.abs(dy) < 12) return; // treated as click
      const i = order.indexOf(p.dataset.snap);
      p.dataset.snap = order[Math.max(0, Math.min(2, i + (dy < 0 ? 1 : -1)))];
    });
  })();

  // ---------- hash state ----------
  function syncHash(){
    const q = new URLSearchParams();
    q.set("tab", state.tab);
    if (state.openMods.size) q.set("m", [...state.openMods].join(","));
    if (state.tab === "perspectives" && state.pmode !== "all") q.set("p", state.pmode + ":" + (state.pmode === "single" ? state.pactor : state.pcompare.join("~")));
    history.replaceState(null, "", "#" + q.toString());
  }
  function readHash(){
    const q = new URLSearchParams(location.hash.slice(1));
    if (TABS.some(t => t[0] === q.get("tab"))) state.tab = q.get("tab");
    if (q.get("m")) q.get("m").split(",").forEach(m => state.openMods.add(m));
    const p = q.get("p");
    if (p){ const [mode, ids] = p.split(":"); if (mode === "single"){ state.pmode = "single"; state.pactor = ids; }
      if (mode === "compare"){ state.pmode = "compare"; state.pcompare = (ids || "").split("~").filter(Boolean); } }
  }

  // ---------- map ----------
  function flyHome(){ if (map) map.flyTo({center: D.territory.focus.center, zoom: D.territory.focus.zoom}); }
  function initMap(geo){
    const el = $("map");
    if (!window.maplibregl){ el.append(h("div", {class:"map-msg"}, "The map library did not load. All content is in the panel.")); return; }
    try {
      const desktop = window.matchMedia("(min-width: 821px)").matches;
      map = new maplibregl.Map({ container: el, style: "https://tiles.openfreemap.org/styles/positron",
        center: D.territory.focus.center, zoom: desktop ? D.territory.focus.zoom : D.territory.focus.zoom - 0.9,
        attributionControl: { compact: true }, cooperativeGestures: false });
      map.addControl(new maplibregl.NavigationControl({showCompass:false}), "top-left");
      map.on("load", () => {
        map.addSource("territory", {type:"geojson", data: geo});
        // class administrative_boundary: solid line (GASPI 3.0 geometry classes)
        map.addLayer({id:"terr-fill", type:"fill", source:"territory", paint:{"fill-color":"#1f5f74","fill-opacity":0.06}});
        map.addLayer({id:"terr-line", type:"line", source:"territory", filter:["==",["get","class"],"administrative_boundary"], paint:{"line-color":"#1f5f74","line-width":2}});
        if (!desktop) map.easeTo({padding:{bottom: window.innerHeight * 0.5}, duration:0});
        document.body.dataset.mapReady = "1";
      });
      map.on("error", (e) => { console.warn("map error", e && e.error); });
    } catch (err){
      el.append(h("div", {class:"map-msg"}, "The map could not start in this browser (WebGL unavailable). All content is in the panel."));
    }
  }

  // ---------- boot ----------
  Promise.all([fetch(`data/${TID}.json`).then(r => r.json()), fetch(`data/${TID}.geojson`).then(r => r.json()).catch(() => null)])
    .then(([data, geo]) => {
      D = data; D.sources.forEach((s,i) => { SRC[s.id] = s; SNUM[s.id] = i + 1; });
      document.title = `GASPI 3.0 · ${D.territory.name}`;
      $("tName").textContent = D.territory.name; $("tLede").textContent = D.territory.summary;
      readHash(); render(); if (geo) initMap(geo);
      document.body.dataset.ready = "1";
    })
    .catch(err => { $("panelBody").textContent = "Could not load territory data: " + err; });
})();
