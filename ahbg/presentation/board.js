const EMBEDDED_SNAPSHOT = {
  kind: "ahbg.presentation.snapshot",
  standing: "not-mechanics",
  plane_id: "plane-0",
  turn: 0,
  tiles: [
    { id: "c", q: 0, r: 0, label: "origin" },
    { id: "ne", q: 1, r: -1, label: "ne" },
    { id: "e", q: 1, r: 0, label: "e" },
    { id: "se", q: 0, r: 1, label: "se" },
    { id: "sw", q: -1, r: 1, label: "sw" },
    { id: "w", q: -1, r: 0, label: "w" },
    { id: "nw", q: 0, r: -1, label: "nw" },
  ],
  units: [{ id: "A0", tile: "c", label: "A0" }],
  selected_tile: "c",
  feed: [{ turn: 0, text: "plane loaded; A0 at origin" }],
};

const SIZE = 42;

function axialToPixel(q, r) {
  return {
    x: SIZE * Math.sqrt(3) * (q + r / 2),
    y: SIZE * (3 / 2) * r,
  };
}

function hexPoints(cx, cy) {
  const points = [];
  for (let i = 0; i < 6; i += 1) {
    const angle = (Math.PI / 180) * (60 * i - 30);
    points.push(`${cx + SIZE * Math.cos(angle)},${cy + SIZE * Math.sin(angle)}`);
  }
  return points.join(" ");
}

function validateSnapshot(snapshot) {
  if (snapshot.kind !== "ahbg.presentation.snapshot") {
    throw new Error("kind must be ahbg.presentation.snapshot");
  }
  if (snapshot.standing !== "not-mechanics") {
    throw new Error("standing must be not-mechanics");
  }
  if (!Array.isArray(snapshot.tiles) || snapshot.tiles.length === 0) {
    throw new Error("tiles must be a non-empty list");
  }
  const ids = new Set(snapshot.tiles.map((tile) => tile.id));
  for (const unit of snapshot.units || []) {
    if (!ids.has(unit.tile)) {
      throw new Error(`unit ${unit.id} tile is not a presented tile`);
    }
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
  const minX = Math.min(...pixels.map((p) => p.x)) - SIZE * 2;
  const minY = Math.min(...pixels.map((p) => p.y)) - SIZE * 2;
  const maxX = Math.max(...pixels.map((p) => p.x)) + SIZE * 2;
  const maxY = Math.max(...pixels.map((p) => p.y)) + SIZE * 2;
  svg.setAttribute("viewBox", `${minX} ${minY} ${maxX - minX} ${maxY - minY}`);

  const byId = Object.fromEntries(snapshot.tiles.map((tile) => [tile.id, tile]));
  let selected = snapshot.selected_tile && byId[snapshot.selected_tile] ? snapshot.selected_tile : snapshot.tiles[0].id;

  function paintInspect() {
    const tile = byId[selected];
    const occupants = (snapshot.units || []).filter((unit) => unit.tile === selected);
    inspect.textContent = `${tile.label || tile.id} (${tile.q},${tile.r})${
      occupants.length ? ` — ${occupants.map((unit) => unit.label || unit.id).join(", ")}` : ""
    }`;
  }

  snapshot.tiles.forEach((tile) => {
    const { x, y } = axialToPixel(tile.q, tile.r);
    const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    poly.setAttribute("points", hexPoints(x, y));
    poly.setAttribute("class", tile.id === selected ? "hex selected" : "hex");
    poly.dataset.tile = tile.id;
    poly.addEventListener("click", () => {
      selected = tile.id;
      svg.querySelectorAll(".hex").forEach((node) => {
        node.setAttribute("class", node.dataset.tile === selected ? "hex selected" : "hex");
      });
      paintInspect();
    });
    svg.appendChild(poly);
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", x);
    text.setAttribute("y", y + 18);
    text.setAttribute("class", "hex-label");
    text.textContent = tile.label || tile.id;
    svg.appendChild(text);
  });

  (snapshot.units || []).forEach((unit) => {
    const tile = byId[unit.tile];
    const { x, y } = axialToPixel(tile.q, tile.r);
    const marker = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    marker.setAttribute("cx", x);
    marker.setAttribute("cy", y - 6);
    marker.setAttribute("r", 10);
    marker.setAttribute("class", "unit");
    svg.appendChild(marker);
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", x);
    label.setAttribute("y", y - 3);
    label.setAttribute("class", "hex-label");
    label.setAttribute("fill", "#f4efe4");
    label.textContent = unit.label || unit.id;
    svg.appendChild(label);
  });

  (snapshot.feed || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `t${item.turn ?? "?"} ${item.text}`;
    feed.appendChild(li);
  });
  paintInspect();
}

async function boot() {
  let snapshot = EMBEDDED_SNAPSHOT;
  try {
    const response = await fetch("sample_snapshot.json", { cache: "no-store" });
    if (response.ok) {
      snapshot = await response.json();
    }
  } catch (_error) {
    snapshot = EMBEDDED_SNAPSHOT;
  }
  render(validateSnapshot(snapshot));
}

boot();
