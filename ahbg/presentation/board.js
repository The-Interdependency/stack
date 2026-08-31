// === MODULE_BUILD ===
// id: ahbg_presentation_browser_board
//   module_name: board
//   module_kind: ui_panel
//   summary: renders strict presentation snapshots using source-supplied UCNS center coordinates, accessible tile inspection, resolved motion traces, and nonoverlapping unit markers
//   owner: AHBG presentation
//   public_surface: browser board UI
//   internal_surface: validateSnapshot, render, sourceToPixel, offsetFor, boot
//   auth_boundary: none
//   storage_boundary: none
//   network_boundary: internal
//   user_data_boundary: read
//   admin_only: false
//   tests: ahbg/presentation/tests/test_presentation.py; node --check ahbg/presentation/board.js
//   rollout: static presentation page only
//   rollback: remove ahbg/presentation browser files without changing mechanics
//   requires: ahbg_presentation_snapshot_contract; UCNS-derived x/y and geometry_source carried by snapshot
//   since: 2026-08-31
//   unresolved: live engine-to-observation adapter remains outside presentation
// === END MODULE_BUILD ===

const UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64";
const SQRT3_HALF = Math.sqrt(3) / 2;
const EMBEDDED_SNAPSHOT = {
  kind: "ahbg.presentation.snapshot",
  standing: "not-mechanics",
  plane_id: "plane-0",
  turn: 1,
  geometry_source: {
    repository: "The-Interdependency/ucns",
    commit: UCNS_COMMIT,
    module: "src/ucns/mobius_seed.py",
    schema_id: "ucns.mobius-seed-of-life",
    schema_version: "0.1.0",
    projection_id: "seed-of-life-seven-equal-circles",
    selection_effect: "none",
  },
  tiles: [
    { id: "CENTER", source_slot: "CENTER", x: 0, y: 0, label: "origin" },
    { id: "RING_0", source_slot: "RING_0", x: 1, y: 0, label: "ring 0" },
    { id: "RING_1", source_slot: "RING_1", x: 0.5, y: SQRT3_HALF, label: "ring 1" },
    { id: "RING_2", source_slot: "RING_2", x: -0.5, y: SQRT3_HALF, label: "ring 2" },
    { id: "RING_3", source_slot: "RING_3", x: -1, y: 0, label: "ring 3" },
    { id: "RING_4", source_slot: "RING_4", x: -0.5, y: -SQRT3_HALF, label: "ring 4" },
    { id: "RING_5", source_slot: "RING_5", x: 0.5, y: -SQRT3_HALF, label: "ring 5" },
  ],
  units: [{ id: "A0", tile: "RING_0", label: "A0" }],
  selected_tile: "RING_0",
  motions: [{ unit: "A0", from: "CENTER", to: "RING_0" }],
  feed: [
    { turn: 0, text: "plane loaded; A0 at origin" },
    { turn: 1, text: "A0 trace CENTER to RING_0" },
  ],
};

const RADIUS = 64;
const TILE_POINT = 6;
const UNIT_RADIUS = 11;
const ROOT_FIELDS = new Set(["kind", "standing", "plane_id", "turn", "geometry_source", "tiles", "units", "selected_tile", "feed", "motions"]);
const GEOMETRY_FIELDS = new Set(["repository", "commit", "module", "schema_id", "schema_version", "projection_id", "selection_effect"]);
const TILE_FIELDS = new Set(["id", "label", "source_slot", "x", "y"]);
const UNIT_FIELDS = new Set(["id", "tile", "label"]);
const FEED_FIELDS = new Set(["turn", "text"]);
const MOTION_FIELDS = new Set(["unit", "from", "to"]);

function sourceToPixel(tile) {
  return { x: RADIUS * tile.x, y: -RADIUS * tile.y };
}

function exactText(value) {
  return typeof value === "string" && value.length > 0;
}

function numeric(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function plainInteger(value) {
  return Number.isInteger(value);
}

function rejectUnknown(value, allowed, surface) {
  const unknown = Object.keys(value).filter((key) => !allowed.has(key)).sort();
  if (unknown.length) throw new Error(`${surface} has undeclared fields: ${unknown.join(", ")}`);
}

function validateSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== "object" || Array.isArray(snapshot)) {
    throw new Error("snapshot must be an object");
  }
  rejectUnknown(snapshot, ROOT_FIELDS, "snapshot");
  if (snapshot.kind !== "ahbg.presentation.snapshot") throw new Error("kind must be ahbg.presentation.snapshot");
  if (snapshot.standing !== "not-mechanics") throw new Error("standing must be not-mechanics");
  if (!exactText(snapshot.plane_id)) throw new Error("plane_id must be exact non-empty text");
  if (!plainInteger(snapshot.turn) || snapshot.turn < 0) throw new Error("turn must be a non-negative integer");

  const geometry = snapshot.geometry_source;
  if (!geometry || typeof geometry !== "object" || Array.isArray(geometry)) throw new Error("geometry_source must be an object");
  rejectUnknown(geometry, GEOMETRY_FIELDS, "geometry_source");
  for (const field of GEOMETRY_FIELDS) {
    if (!exactText(geometry[field])) throw new Error(`geometry_source.${field} must be exact non-empty text`);
  }
  if (!/^[0-9a-f]{40}$/.test(geometry.commit)) throw new Error("geometry_source.commit must be a lowercase 40-hex commit");

  if (!Array.isArray(snapshot.tiles) || snapshot.tiles.length === 0) throw new Error("tiles must be a non-empty list");
  const ids = new Set();
  const sourceSlots = new Set();
  const positions = new Set();
  for (const tile of snapshot.tiles) {
    if (!tile || typeof tile !== "object" || Array.isArray(tile)) throw new Error("each tile must be an object");
    rejectUnknown(tile, TILE_FIELDS, "tile");
    if (!exactText(tile.id)) throw new Error("tile id must be exact non-empty text");
    if (ids.has(tile.id)) throw new Error(`tile id repeats: ${tile.id}`);
    if (!exactText(tile.source_slot)) throw new Error(`tile ${tile.id} source_slot must be exact non-empty text`);
    if (sourceSlots.has(tile.source_slot)) throw new Error(`UCNS source slot repeats: ${tile.source_slot}`);
    if (!numeric(tile.x) || !numeric(tile.y)) throw new Error(`tile ${tile.id} x,y must be finite numbers`);
    const position = `${tile.x},${tile.y}`;
    if (positions.has(position)) throw new Error(`tile source position repeats: ${position}`);
    if (tile.label !== undefined && !exactText(tile.label)) throw new Error(`tile ${tile.id} label must be exact non-empty text when present`);
    ids.add(tile.id);
    sourceSlots.add(tile.source_slot);
    positions.add(position);
  }

  if (!Array.isArray(snapshot.units)) throw new Error("units must be a list");
  const unitIds = new Set();
  const unitById = new Map();
  for (const unit of snapshot.units) {
    if (!unit || typeof unit !== "object" || Array.isArray(unit)) throw new Error("each unit must be an object");
    rejectUnknown(unit, UNIT_FIELDS, "unit");
    if (!exactText(unit.id)) throw new Error("unit id must be exact non-empty text");
    if (unitIds.has(unit.id)) throw new Error(`unit id repeats: ${unit.id}`);
    if (!exactText(unit.tile) || !ids.has(unit.tile)) throw new Error(`unit ${unit.id} tile is not a presented tile`);
    if (unit.label !== undefined && !exactText(unit.label)) throw new Error(`unit ${unit.id} label must be exact non-empty text when present`);
    unitIds.add(unit.id);
    unitById.set(unit.id, unit);
  }

  if (snapshot.selected_tile !== undefined && snapshot.selected_tile !== null) {
    if (!exactText(snapshot.selected_tile) || !ids.has(snapshot.selected_tile)) throw new Error("selected_tile must name a presented tile");
  }
  if (!Array.isArray(snapshot.feed)) throw new Error("feed must be a list");
  for (const item of snapshot.feed) {
    if (!item || typeof item !== "object" || Array.isArray(item)) throw new Error("each feed item must be an object");
    rejectUnknown(item, FEED_FIELDS, "feed item");
    if (!exactText(item.text)) throw new Error("each feed item must have exact non-empty text");
    if (item.turn !== undefined && (!plainInteger(item.turn) || item.turn < 0)) throw new Error("feed turn must be a non-negative integer when present");
  }

  let motions = [];
  if (Object.prototype.hasOwnProperty.call(snapshot, "motions")) {
    if (!Array.isArray(snapshot.motions)) throw new Error("motions must be a list when present");
    motions = snapshot.motions;
  }
  const motionUnits = new Set();
  for (const motion of motions) {
    if (!motion || typeof motion !== "object" || Array.isArray(motion)) throw new Error("each motion must be an object");
    rejectUnknown(motion, MOTION_FIELDS, "motion");
    if (!exactText(motion.unit) || !unitById.has(motion.unit)) throw new Error(`motion unit ${motion.unit} is not a presented unit`);
    if (motionUnits.has(motion.unit)) throw new Error(`motion repeats unit ${motion.unit}`);
    if (!exactText(motion.from) || !ids.has(motion.from)) throw new Error(`motion from ${motion.from} is not a presented tile`);
    if (!exactText(motion.to) || !ids.has(motion.to)) throw new Error(`motion to ${motion.to} is not a presented tile`);
    if (motion.from === motion.to) throw new Error(`motion for ${motion.unit} must change tiles`);
    if (unitById.get(motion.unit).tile !== motion.to) throw new Error(`motion destination for ${motion.unit} must match its presented tile`);
    motionUnits.add(motion.unit);
  }
  return snapshot;
}

function render(snapshot) {
  const svg = document.getElementById("board");
  const feed = document.getElementById("feed-list");
  const inspect = document.getElementById("inspect");
  svg.replaceChildren();
  feed.replaceChildren();

  const pixels = snapshot.tiles.map(sourceToPixel);
  const minX = Math.min(...pixels.map((p) => p.x)) - RADIUS * 1.2;
  const minY = Math.min(...pixels.map((p) => p.y)) - RADIUS * 1.2;
  const maxX = Math.max(...pixels.map((p) => p.x)) + RADIUS * 1.2;
  const maxY = Math.max(...pixels.map((p) => p.y)) + RADIUS * 1.2;
  svg.setAttribute("viewBox", `${minX} ${minY} ${maxX - minX} ${maxY - minY}`);

  const byId = Object.fromEntries(snapshot.tiles.map((tile) => [tile.id, tile]));
  let selected = snapshot.selected_tile && byId[snapshot.selected_tile] ? snapshot.selected_tile : snapshot.tiles[0].id;
  const hitByTile = new Map();
  let selectionRing = null;

  function paintInspect() {
    const tile = byId[selected];
    const occupants = snapshot.units.filter((unit) => unit.tile === selected);
    inspect.textContent = `tile ${tile.label || tile.id} — UCNS ${tile.source_slot} @ (${tile.x}, ${tile.y})${occupants.length ? ` — ${occupants.map((unit) => unit.label || unit.id).join(", ")}` : ""}`;
  }

  function paintSelection() {
    svg.querySelectorAll(".tile-point").forEach((node) => {
      node.setAttribute("class", node.dataset.tile === selected ? "tile-point selected" : "tile-point");
    });
    for (const [tileId, node] of hitByTile.entries()) node.setAttribute("aria-pressed", tileId === selected ? "true" : "false");
    if (selectionRing) {
      const { x, y } = sourceToPixel(byId[selected]);
      selectionRing.setAttribute("cx", x);
      selectionRing.setAttribute("cy", y);
    }
    paintInspect();
  }

  snapshot.tiles.forEach((tile) => {
    const { x, y } = sourceToPixel(tile);
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x);
    circle.setAttribute("cy", y);
    circle.setAttribute("r", RADIUS);
    circle.setAttribute("class", "seed-circle");
    svg.appendChild(circle);
  });

  (snapshot.motions || []).forEach((motion) => {
    const from = sourceToPixel(byId[motion.from]);
    const to = sourceToPixel(byId[motion.to]);
    const path = document.createElementNS("http://www.w3.org/2000/svg", "line");
    path.setAttribute("x1", from.x);
    path.setAttribute("y1", from.y);
    path.setAttribute("x2", to.x);
    path.setAttribute("y2", to.y);
    path.setAttribute("class", "motion-path");
    svg.appendChild(path);
  });

  snapshot.tiles.forEach((tile) => {
    const { x, y } = sourceToPixel(tile);
    const point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    point.setAttribute("cx", x);
    point.setAttribute("cy", y);
    point.setAttribute("r", TILE_POINT);
    point.setAttribute("class", tile.id === selected ? "tile-point selected" : "tile-point");
    point.dataset.tile = tile.id;
    svg.appendChild(point);

    const hit = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    hit.setAttribute("cx", x);
    hit.setAttribute("cy", y);
    hit.setAttribute("r", RADIUS * 0.28);
    hit.setAttribute("class", "tile-hit");
    hit.setAttribute("tabindex", "0");
    hit.setAttribute("role", "button");
    hit.setAttribute("aria-label", `Inspect tile ${tile.label || tile.id}`);
    hit.setAttribute("aria-pressed", tile.id === selected ? "true" : "false");
    const selectTile = () => { selected = tile.id; paintSelection(); };
    hit.addEventListener("click", selectTile);
    hit.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectTile(); }
    });
    hitByTile.set(tile.id, hit);
    svg.appendChild(hit);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", x);
    text.setAttribute("y", y + RADIUS * 0.38);
    text.setAttribute("class", "tile-label");
    text.textContent = tile.label || tile.id;
    svg.appendChild(text);
  });

  const motionByUnit = Object.fromEntries((snapshot.motions || []).map((motion) => [motion.unit, motion]));
  const tileGroups = new Map();
  snapshot.units.forEach((unit) => {
    const group = tileGroups.get(unit.tile) || [];
    group.push(unit.id);
    tileGroups.set(unit.tile, group);
  });

  function offsetFor(unit) {
    const group = tileGroups.get(unit.tile) || [unit.id];
    if (group.length === 1) return { x: 0, y: 0 };
    const index = group.indexOf(unit.id);
    const angle = (Math.PI * 2 * index) / group.length - Math.PI / 2;
    const minimumChord = UNIT_RADIUS * 2 + 4;
    const spread = Math.max(UNIT_RADIUS * 1.35, minimumChord / (2 * Math.sin(Math.PI / group.length)));
    return { x: Math.cos(angle) * spread, y: Math.sin(angle) * spread };
  }

  snapshot.units.forEach((unit) => {
    const offset = offsetFor(unit);
    const center = sourceToPixel(byId[unit.tile]);
    const dest = { x: center.x + offset.x, y: center.y + offset.y };
    const motion = motionByUnit[unit.id];
    const fromCenter = motion ? sourceToPixel(byId[motion.from]) : center;
    const origin = { x: fromCenter.x + offset.x, y: fromCenter.y + offset.y };

    const marker = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    marker.setAttribute("cx", origin.x); marker.setAttribute("cy", origin.y); marker.setAttribute("r", UNIT_RADIUS); marker.setAttribute("class", "unit");
    svg.appendChild(marker);
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", origin.x); label.setAttribute("y", origin.y + 4); label.setAttribute("class", "unit-label"); label.textContent = unit.label || unit.id;
    svg.appendChild(label);

    if (motion) {
      const dur = "0.8s";
      [["cx", origin.x, dest.x, marker], ["cy", origin.y, dest.y, marker], ["x", origin.x, dest.x, label], ["y", origin.y + 4, dest.y + 4, label]].forEach(([name, from, to, node]) => {
        const animate = document.createElementNS("http://www.w3.org/2000/svg", "animate");
        animate.setAttribute("attributeName", name); animate.setAttribute("from", from); animate.setAttribute("to", to); animate.setAttribute("dur", dur); animate.setAttribute("fill", "freeze"); node.appendChild(animate);
      });
    }
  });

  selectionRing = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  selectionRing.setAttribute("r", UNIT_RADIUS + 6); selectionRing.setAttribute("class", "selection-ring"); svg.appendChild(selectionRing);
  snapshot.feed.forEach((item) => { const li = document.createElement("li"); li.textContent = `t${item.turn ?? "?"} ${item.text}`; feed.appendChild(li); });
  paintSelection();
}

async function boot() {
  let snapshot = EMBEDDED_SNAPSHOT;
  try {
    const response = await fetch("sample_snapshot.json", { cache: "no-store" });
    if (response.ok) snapshot = await response.json();
  } catch (_error) {
    snapshot = EMBEDDED_SNAPSHOT;
  }
  render(validateSnapshot(snapshot));
}

boot();
