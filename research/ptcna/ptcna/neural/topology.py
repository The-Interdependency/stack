# ratios: loc_comments=88:54 imports_exports=3:3 calls_definitions=22:10
"""
PCNA topology: stable mapping of seed ids and neighbor computation.

This implementation maps compute-shard neighbors to global seed IDs so the
rest of the system can route using absolute ids. It also provides simple
serialization for HTTP responses.
"""

# === MODULE_BUILD ===
# id: pcna_topology
#   module_name: topology
#   module_kind: engine
#   summary: Stable seed-id topology — maps compute-shard neighbors to global seed IDs, computes heptagram neighbors and sentinel scan paths, and serializes to JSON for HTTP responses.
#   owner: Erin Spencer
#   public_surface: PCNATopology, Seed, SeedRole
#   internal_surface: _initialize_topology, _heptagram_neighbors
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/tests_topology.py
#   rollout: default_enabled
#   rollback: remove import and call sites
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class SeedRole(Enum):
    COMPUTE = "compute"
    SENTINEL = "sentinel"
    META = "meta"
    GLOBAL = "global"


@dataclass
class Seed:
    id: int
    role: SeedRole
    meta_id: Optional[int] = None
    shard_id: Optional[int] = None
    neighbors: Optional[List[int]] = None


class PCNATopology:
    def __init__(self, n_metas: int = 7, seeds_per_meta: int = 7, sentinels: int = 4):
        self.n_metas = n_metas
        self.seeds_per_meta = seeds_per_meta
        self.sentinels = sentinels

        # seeds is a mapping global_id -> Seed
        self.seeds: Dict[int, Seed] = self._initialize_topology()

    def _initialize_topology(self) -> Dict[int, Seed]:
        seeds: Dict[int, Seed] = {}

        # 0 => Global router
        seeds[0] = Seed(id=0, role=SeedRole.GLOBAL)

        # Sentinels (1 .. sentinels)
        for i in range(1, self.sentinels + 1):
            seeds[i] = Seed(id=i, role=SeedRole.SENTINEL)

        # We'll allocate meta routers and compute seeds starting at id=5
        seed_counter = max(5, max(seeds.keys()) + 1)

        for meta_id in range(1, self.n_metas + 1):
            meta_seed_id = seed_counter
            seeds[meta_seed_id] = Seed(id=meta_seed_id, role=SeedRole.META, meta_id=meta_id)
            seed_counter += 1

            # Compute seeds for this meta: consecutive ids meta_seed_id+1 .. meta_seed_id+seeds_per_meta
            compute_base = meta_seed_id + 1
            for shard_idx in range(self.seeds_per_meta):
                compute_seed_id = compute_base + shard_idx
                neighbors = self._heptagram_neighbors(meta_seed_id, shard_idx)
                seeds[compute_seed_id] = Seed(
                    id=compute_seed_id,
                    role=SeedRole.COMPUTE,
                    meta_id=meta_id,
                    shard_id=shard_idx,
                    neighbors=neighbors,
                )

            seed_counter = compute_base + self.seeds_per_meta

        return seeds

    def _heptagram_neighbors(self, meta_seed_id: int, index: int) -> List[int]:
        """
        Compute heptagram neighbors for a compute seed within its meta.
        Returns global seed IDs for the neighbors.

        7:3 heptagram: each node connects to (index + 3) and (index - 3) mod 7
        """
        n = self.seeds_per_meta
        offsets = [((index + 3) % n), ((index - 3) % n)]
        # compute seeds start at meta_seed_id + 1
        return [meta_seed_id + 1 + o for o in offsets]

    def get_meta_router_id(self, meta_id: int) -> Optional[int]:
        """Return the global seed id of the meta router for the given meta_id"""
        for sid, seed in self.seeds.items():
            if seed.role == SeedRole.META and seed.meta_id == meta_id:
                return sid
        return None

    def get_sentinel_scan_path(self, sentinel_id: int) -> List[int]:
        """
        7:2 scan pattern for sentinels.
        Returns the list of meta-router global ids in the scan order.
        """
        if sentinel_id < 1 or sentinel_id > self.sentinels:
            # normalize but still produce a path
            sentinel_id = ((sentinel_id - 1) % self.sentinels) + 1

        start = (sentinel_id - 1) % self.n_metas
        path_meta_indexes = [(start + i * 2) % self.n_metas for i in range(self.n_metas)]
        # meta indexes are 0..n_metas-1, meta_id is 1..n_metas
        return [self.get_meta_router_id(m + 1) for m in path_meta_indexes]

    def route(self, source_id: int, target_meta: int) -> List[int]:
        """
        Route from source seed to target meta. Returns a list of seed ids which represent
        the expected hop sequence (best-effort).
        """
        if source_id == 0:
            meta_router = self.get_meta_router_id(target_meta)
            return [0, meta_router] if meta_router is not None else [0]

        source_seed = self.seeds.get(source_id)
        if source_seed is None:
            return []

        if source_seed.meta_id == target_meta:
            # intra-meta: direct to meta router or keep within compute neighborhood.
            meta_router = self.get_meta_router_id(target_meta)
            return [source_id, meta_router] if meta_router is not None else [source_id]

        # inter-meta: go source -> source's meta router -> target's meta router
        source_meta_router = self.get_meta_router_id(source_seed.meta_id)
        target_meta_router = self.get_meta_router_id(target_meta)
        path = [source_id]
        if source_meta_router is not None:
            path.append(source_meta_router)
        if target_meta_router is not None:
            path.append(target_meta_router)
        return path

    def to_dict(self) -> Dict[str, Dict]:
        """
        Serialize topology to a JSON-friendly dict:
          { "<id>": { "id": <int>, "role": "<role>", "meta_id": <>, "shard_id": <>, "neighbors": [...] } }
        """
        out = {}
        for sid, seed in self.seeds.items():
            out[str(sid)] = {
                "id": seed.id,
                "role": seed.role.value,
                "meta_id": seed.meta_id,
                "shard_id": seed.shard_id,
                "neighbors": seed.neighbors or [],
            }
        return out
# ratios: loc_comments=88:54 imports_exports=3:3 calls_definitions=22:10
