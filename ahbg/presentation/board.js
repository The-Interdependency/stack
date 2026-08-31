const EMBEDDED_SNAPSHOT = {
  kind: "ahbg.presentation.snapshot",
  standing: "not-mechanics",
  plane_id: "plane-0",
  turn: 1,
  tiles: [
    { id: "c", q: 0, r: 0, label: "origin" },
    { id: "ne", q: 1, r: -1, label: "ne" },
    { id: "e", q: 1, r: 0, label: "e" },
    { id: "se", q: 0, r: 1, label: "se" },
    { id: "sw", q: -1, r: 1, label: "sw" },
    { id: "w", q: -1, r: 0, label: "w" },
    { id: "nw", q: 0, r: -1, label: "nw" },
  ],
  units: [{ id: "A0", tile: "ne", label: "A0" }],
  selected_tile: "ne",
  motions: [{ unit: "A0", from: "c", to: "ne" }],
  feed: [
    { turn: 0, text: "plane loaded; A0 at origin" },
    { turn: 1, text: "A0 trace origin to ne" },
  ],
};

const RADIUS = 64;
const TILE_POINT = 6;
const UNIT_RADIUS = 11;

function axialToPixel(q, r) {
  return {
    x: RADIUS * (q + r / 2),
    y: RADIUS * (Math.sqrt(3) / 2) * r,
  };
}

function exactText(value) {
  return typeof value === "string" && value.length > 0;
}

function plainInteger(value) {
  return Number.isInteger(value);
}

function validateSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== "object" || Array.isArray(snapshot)) {
    throw new Error("snapshot must be an object");
  }
  if (snapshot.kind !== "ahbg.presentation.snapshot") {
    throw new Error("kind must be ahbg.presentation.snapshot");
  }
  if (snapshot.standing !== "not-mechanics") {
    throw new Error("standing must be not-mechanics");
  }
  if (!exactText(snapshot.plane_id)) {
    throw new Error("plane_id must be exact non-empty text");
  }
  if (!plainInteger(snapshot.turn) || snapshot.turn < 0) {
    throw new Error("turn must be a non-negative integer");
  }
  if (!Array.isArray(snapshot.tiles) || snapshot.tiles.length === 0) {
    throw new Error("tiles must be a non-empty list");
  }

  const ids = new Set();
  const coords = new Set();
  for (const tile of snapshot.tiles) {
    if (!tile || typeof tile !== "object" || Array.isArray(tile)) {
      throw new Error("each tile must be an object");
    }
    if (!exactText(tile.id)) {
      throw new Error("tile id must be exact non-empty text");
    }
    if (ids.has(tile.id)) {
      throw new Error(`tile id repeats: ${tile.id}`);
    }
    if (!plainInteger(tile.q) || !plainInteger(tile.r)) {
      throw new Error(`tile ${tile.id} q,r must be integers`);
    }
    const coord = `${tile.q},${tile.r}`;
    if (coords.has(coord)) {
      throw new Error(`tile coordinate repeats: ${coord}`);
    }
    if (tile.label !== undefined && !exactText(tile.label)) {
      throw new Error(`tile ${tile.id} label must be exact non-empty text when present`);
    }
    ids.add(tile.id);
    coords.add(coord);
  }

  if (!Array.isArray(snapshot.units)) {
    throw new Error("units must be a list");
  }
  const unitIds = new Set();
  const unitById = new Map();
  for (const unit of snapshot.units) {
    if (!unit || typeof unit !== "object" || Array.isArray(unit)) {
      throw new Error("each unit must be an object");
    }
    if (!exactText(unit.id)) {
      throw new Error("unit id must be exact non-empty text");
    }
    if (unitIds.has(unit.id)) {
      throw new Error(`unit id repeats: ${unit.id}`);
    }
    if (!exactText(unit.tile) || !ids.has(unit.tile)) {
      throw new Error(`unit ${unit.id} tile is not a presented tile`);
    }
    if (unit.label !== undefined && !exactText(unit.label)) {
      throw new Error(`unit ${unit.id} label must be exact non-empty text when present`);
    }
    unitIds.add(unit.id);
    unitById.set(unit.id, unit);
  }

  if (snapshot.selected_tile !== undefined && snapshot.selected_tile !== null) {
    if (!exactText(snapshot.selected_tile) || !ids.has(snapshot.selected_tile)) {
      throw new Error("selected_tile must name a presented tile");
    }
  }
  if (!Array.isArray(snapshot.feed)) {
    throw new Error("feed must be a list");
  }
  for (const item of snapshot.feed) {
    if (!item || typeof item !== "object" || Array.isArray(item) || !exactText(item.text)) {
      throw new Error("each feed item must have exact non-empty text");
    }
  }

  const motionUnits = new Set();
  for (const motion of snapshot.motions || []) {
    if (!motion || typeof motion !== "object" || Array.isArray(motion)) {
      throw new Error("each motion must be an object");
    }
    if (!exactText(motion.unit) || !unitById.has(motion.unit)) {
      throw new Error(`motion unit ${motion.unit} is not a presented unit`);
    }
    if (motionUnits.has(motion.unit)) {
      throw new Error(`motion repeats unit ${motion.unit}`);
    }
    if (!exactText(motion.from) || !ids.has(motion.from)) {
      throw new Error(`motion from ${motion.from} is not a presented tile`);
    }
    if (!exactText(motion.to) || !ids.has(motion.to)) {
      throw new Error(`motion to ${motion.to} is not a presented tile`);
    }
    if (motion.from === motion.to) {
      throw new Error(`motion for ${motion.unit} must change tiles`);
    }
    if (unitById.get(motion.unit).tile !== motion.to) {
      throw new Error(`motion destination for ${motion.unit} must match its presented tile`);
    }
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

  const pixels = snapshot.tiles.map((tile) => axialToPixel(tile.q, tile.r));
  const minX = Math.min(...pixels.map((p) => p.x)) - RADIUS * 1.2;
  const minY = Math.min(...pixels.map((p) => p.y)) - RADIUS * 1.2;
  const maxX = Math.max(...pixels.map((p) => p.x)) + RADIUS * 1.2;
  const maxY = Math.max(...pixels.map((p) => p.y)) + RADIUS * 1.2;
  svg.setAttribute("viewBox", `${minX} ${minY} ${maxX - minX} ${maxY - minY}`);

  const byId = Object.fromEntries(snapshot.tiles.map((tile) => [tile.id, tile]));
  let selected = snapshot.selected_tile && byId[snapshot.selected_tile]
    ? snapshot.selected_tile
    : snapshot.tiles[0].id;
  const hitByTile = new Map();
  let selectionRing = null;

  function paintInspect() {
    const tile = byId[selected];
    const occupants = snapshot.units.filter((unit) => unit.tile === selected);
    inspect.textContent = `tile ${tile.label || tile.id} center (${tile.q},${tile.r})${
      occupants.length ? ` — ${occupants.map((unit) => unit.label || unit.id).join(", ")}` : ""
    }`;
  }

  function paintSelection() {
    svg.querySelectorAll(".tile-point").forEach((node) => {
      node.setAttribute("class", node.dataset.tile === selected ? "tile-point selected" : "tile-point");
    });
    for (const [tileId, node] of hitByTile.entries()) {
      node.setAttribute("aria-pressed", tileId === selected ? "true" : "false");
    }
    if (selectionRing) {
      const tile = byId[selected];
      const { x, y } = axialToPixel(tile.q, tile.r);
      selectionRing.setAttribute("cx", x);
      selectionRing.setAttribute("cy", y);
    }
    paintInspect();
  }

  snapshot.tiles.forEach((tile) => {
    const { x, y } = axialToPixel(tile.q, tile.r);
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x);
    circle.setAttribute("cy", y);
    circle.setAttribute("r", RADIUS);
    circle.setAttribute("class", "seed-circle");
    svg.appendChild(circle);
  });

  (snapshot.motions || []).forEach((motion) => {
    const from = axialToPixel(byId[motion.from].q, byId[motion.from].r);
    const to = axialToPixel(byId[motion.to].q, byId[motion.to].r);
    const path = document.createElementNS("http://www.w3.org/2000/svg", "line");
    path.setAttribute("x1", from.x);
    path.setAttribute("y1", from.y);
    path.setAttribute("x2", to.x);
    path.setAttribute("y2", to.y);
    path.setAttribute("class", "motion-path");
    svg.appendChild(path);
  });

  snapshot.tiles.forEach((tile) => {
    const { x, y } = axialToPixel(tile.q, tile.r);
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
    const selectTile = () => {
      selected = tile.id;
      paintSelection();
    };
    hit.addEventListener("click", selectTile);
    hit.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectTile();
      }
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
    const spread = UNIT_RADIUS * 1.35;
    return { x: Math.cos(angle) * spread, y: Math.sin(angle) * spread };
  }

  snapshot.units.forEach((unit) => {
    const tile = byId[unit.tile];
    const offset = offsetFor(unit);
    const center = axialToPixel(tile.q, tile.r);
    const dest = { x: center.x + offset.x, y: center.y + offset.y };
    const motion = motionByUnit[unit.id];
    const fromCenter = motion ? axialToPixel(byId[motion.from].q, byId[motion.from].r) : center;
    const origin = { x: fromCenter.x + offset.x, y: fromCenter.y + offset.y };

    const marker = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    marker.setAttribute("cx", origin.x);
    marker.setAttribute("cy", origin.y);
    marker.setAttribute("r", UNIT_RADIUS);
    marker.setAttribute("class", "unit");
    svg.appendChild(marker);

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", origin.x);
    label.setAttribute("y", origin.y + 4);
    label.setAttribute("class", "unit-label");
    label.textContent = unit.label || unit.id;
    svg.appendChild(label);

    if (motion) {
      const dur = "0.8s";
      [
        ["cx", origin.x, dest.x, marker],
        ["cy", origin.y, dest.y, marker],
        ["x", origin.x, dest.x, label],
        ["y", origin.y + 4, dest.y + 4, label],
      ].forEach(([name, from, to, node]) => {
        const animate = document.createElementNS("http://www.w3.org/2000/svg", "animate");
        animate.setAttribute("attributeName", name);
        animate.setAttribute("from", from);
        animate.setAttribute("to", to);
        animate.setAttribute("dur", dur);
        animate.setAttribute("fill", "freeze");
        node.appendChild(animate);
      });
    }
  });

  selectionRing = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  selectionRing.setAttribute("r", UNIT_RADIUS + 6);
  selectionRing.setAttribute("class", "selection-ring");
  svg.appendChild(selectionRing);

  snapshot.feed.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `t${item.turn ?? "?"} ${item.text}`;
    feed.appendChild(li);
  });
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
