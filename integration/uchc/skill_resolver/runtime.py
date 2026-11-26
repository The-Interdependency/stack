# ratios: loc_comments=110:3 imports_exports=9:2 calls_definitions=41:12
"""Resolve pinned skill definitions through a native UCHC construction or graph control."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from .catalog import CatalogError, load_catalog, resolve

_HERE = Path(__file__).resolve().parent
_STACK = _HERE.parents[2]


def _json(path):
    return json.loads(path.read_bytes())


def digest(value):
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256(data.encode("utf-8")).hexdigest()


class SkillResolver:
    def __init__(self, catalog_root: Path, *, ucns_source_root=None, experiment="uchc"):
        if experiment not in {"uchc", "control"}:
            raise ValueError("unknown skill resolver experiment")
        lock = _json(_HERE / "source.json")
        participants = _json(_STACK / "stack-manifest.json")["research_participants"]
        pins = [p for p in participants if p["participant_id"] == "skill-resolver-catalog"
                and p["workspace"] == "integration/uchc/"]
        if (len(pins) != 1 or pins[0]["repository"] != lock["catalog"]["repo"]
                or pins[0]["commit"] != lock["catalog"]["commit"]):
            raise CatalogError("catalog and Stack work graph disagree")
        self._catalog = load_catalog(catalog_root, source_commit=pins[0]["commit"])
        if self._catalog.source != lock["catalog"]:
            raise CatalogError("catalog identity differs from the pilot lock")

        self.experiment = experiment
        self._native = {"ucns_source_root": ucns_source_root}
        self._packets = {}
        self._records = {}
        self.activation_packet = None
        if experiment == "uchc":
            from . import geometry
            module = geometry.halving
            if (version("uchc") != lock["uchc"]["version"]
                    or sha256(Path(module.__file__).read_bytes()).hexdigest()
                    != lock["uchc"]["halving_module_sha256"]
                    or module.authority()["commit"] != lock["uchc"]["ucns_commit"]):
                raise CatalogError("ordinal-halving producer differs from the pilot lock")
            self._geometry = geometry

    @property
    def source(self):
        return self._catalog.source

    @property
    def ucns_source_root(self):
        return self._native["ucns_source_root"]

    @property
    def declared_runners(self):
        return tuple((name, row["runner"]) for name, row in self._catalog.records.items()
                     if "runner" in row)

    def get(self, name):
        if self.experiment == "control":
            return self._catalog.get(name)
        if name not in self._records:
            original = self._catalog.get(name)
            packet = self._geometry.encode_record(original, **self._native)
            restored = self._geometry.decode_record(packet, **self._native)
            if restored != original:
                raise CatalogError(f"skill construction changed its source record: {name}")
            self._packets[name] = packet
            self._records[name] = restored
        return deepcopy(self._records[name])

    def read_body(self, name):
        return self._catalog.read_body(name)

    def resolve(self, roots):
        self.activation_packet = None
        decision = resolve(self._catalog, roots, get_record=self.get)
        if self.experiment == "control":
            return decision
        manifest = {"source": self.source, "decision": decision}
        packet = self._geometry.compose_bundle(
            [self._packets[name] for name in decision["order"]], manifest, **self._native)
        recovered = self.replay_activation(packet, expected_roots=decision["roots"])
        self.activation_packet = packet
        return recovered

    def save_activation(self, out_dir: Path):
        """Persist the verified native packet by its construction identity on the host."""
        if self.activation_packet is None:
            return None
        root = self.activation_packet["graph"]["root"]
        directory = Path(out_dir) / "skill-activations"
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / f"{root}.json"
        with NamedTemporaryFile(dir=directory, delete=False) as staged:
            temporary = Path(staged.name)
        try:
            temporary.write_text(json.dumps(self.activation_packet, ensure_ascii=False,
                                           sort_keys=True, separators=(",", ":")), encoding="utf-8")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
        return root

    def replay_activation(self, packet, *, expected_roots):
        """Recover the decision from the packet and check every reason against pinned source."""
        if self.experiment != "uchc":
            raise CatalogError("native activation replay requires the UCHC resolver")
        records, manifest = self._geometry.replay_bundle(packet, **self._native)
        if set(manifest) != {"source", "decision"} or manifest["source"] != self.source:
            raise CatalogError("foreign activation source")
        by_name = {record["name"]: record for record in records}
        def lookup(name):
            if name not in by_name:
                raise CatalogError(f"missing skill in activation: {name}")
            return by_name[name]
        decision = resolve(self._catalog, expected_roots, get_record=lookup)
        if (manifest["decision"] != decision
                or [record["name"] for record in records] != decision["order"]):
            raise CatalogError("activation does not match the requested, source-derived plan")
        return decision
# ratios: loc_comments=110:3 imports_exports=9:2 calls_definitions=41:12
