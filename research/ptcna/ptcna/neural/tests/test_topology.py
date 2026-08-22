import pytest
from ptcna.neural.topology import PCNATopology, SeedRole


def test_meta_router_count_and_positions():
    topo = PCNATopology()
    meta_router_ids = [sid for sid, s in topo.seeds.items() if s.role == SeedRole.META]
    assert len(meta_router_ids) == topo.n_metas

    # meta router ids should be >= 5 (we start allocating at 5)
    assert all(mid >= 5 for mid in meta_router_ids)


def test_compute_neighbors_are_global_ids_and_within_meta():
    topo = PCNATopology()
    # pick first meta router
    first_meta_router = topo.get_meta_router_id(1)
    assert first_meta_router is not None
    # compute ids for meta 1 are consecutive after the meta router id
    compute_ids = [first_meta_router + i for i in range(1, topo.seeds_per_meta + 1)]
    # check neighbors for each compute are inside the same range
    for cid in compute_ids:
        seed = topo.seeds[cid]
        assert seed.role.name.lower() == "compute"
        for n in (seed.neighbors or []):
            assert n in compute_ids


def test_sentinel_scan_path_maps_to_meta_routers():
    topo = PCNATopology()
    path = topo.get_sentinel_scan_path(1)
    assert len(path) == topo.n_metas
    # each entry should be a known meta router id
    for mid in path:
        assert mid in topo.seeds
        assert topo.seeds[mid].role == SeedRole.META


def test_route_uses_meta_routers():
    topo = PCNATopology()
    # pick a compute seed from meta 1 and route to meta 2
    meta1_router = topo.get_meta_router_id(1)
    assert meta1_router is not None
    compute_in_meta1 = meta1_router + 1
    path = topo.route(compute_in_meta1, 2)
    # Expect path to include source and target meta router
    assert compute_in_meta1 in path
    target_router = topo.get_meta_router_id(2)
    assert target_router in path
