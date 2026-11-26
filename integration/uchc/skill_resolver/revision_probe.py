# ratios: loc_comments=78:8 imports_exports=4:1 calls_definitions=31:1
"""Compare content-level cache invalidation after a synthetic, in-memory body revision."""

from hashlib import sha256

from . import geometry
from .catalog import CatalogError
from .runtime import digest


def compare_revision(resolver):
    """Verify one shared definition edit against its consumers and an unrelated root.

    The synthetic edit never replaces a source file or catalog entry. The probe
    counts regenerated definitions and activation bundles. It makes no estimate
    of CPU savings or invalidation caused by changing a global source lock.
    """
    if resolver.experiment != "uchc":
        raise ValueError("the revision probe requires the pinned UCHC resolver")
    options = {"ucns_source_root": resolver.ucns_source_root}
    changed = "msdmd"
    roots = ("doc-build", "typed-meta-frontend", "distributed-publication")
    expected = {"doc-build", "typed-meta-frontend"}
    body = resolver.read_body(changed).encode("utf-8")
    changed_record = resolver.get(changed)
    original_digest = sha256(body).hexdigest()
    if changed_record["sha256"] != original_digest:
        raise ValueError("body does not match source record")
    suffix = b"\n<!-- skill-resolver revision probe -->\n"
    new_digest = sha256(body + suffix).hexdigest()
    changed_record["sha256"] = new_digest
    new_packet = geometry.encode_record(changed_record, **options)
    if geometry.decode_record(new_packet, **options) != changed_record:
        raise ValueError("changed definition did not replay")

    records, packets = {}, {}
    changed_roots = {"control": [], "uchc": []}
    rejected_by_source = []
    bundle_ids = {}
    for root in roots:
        decision = resolver.resolve([root])
        order = decision["order"]
        for name in order:
            if name not in records:
                records[name] = resolver.get(name)
                packets[name] = geometry.encode_record(records[name], **options)
        manifest = {"source": resolver.source, "decision": decision}
        graph_before = digest({"records": [records[name] for name in order], "manifest": manifest})
        native_before = resolver.activation_packet["graph"]["root"]

        # Independent full replay checks which bundles the one-record cache
        # would invalidate. Its verification work is reported separately below.
        selected = [changed_record if name == changed else records[name] for name in order]
        graph_after = digest({"records": selected, "manifest": manifest})
        children = [new_packet if name == changed else packets[name] for name in order]
        bundle = geometry.compose_bundle(children, manifest, **options)
        recovered, receipt = geometry.replay_bundle(bundle, **options)
        if recovered != selected or receipt != manifest:
            raise ValueError(f"revised native bundle changed the plan or source records: {root}")
        native_after = bundle["graph"]["root"]
        bundle_ids[root] = {"control": [graph_before, graph_after], "uchc": [native_before, native_after]}
        if graph_before != graph_after:
            changed_roots["control"].append(root)
        if native_before != native_after:
            changed_roots["uchc"].append(root)

        if root in expected:
            try:
                resolver.replay_activation(bundle, expected_roots=[root])
            except CatalogError as exc:
                if "differs from pinned source" not in str(exc):
                    raise
                rejected_by_source.append(root)
            else:
                raise ValueError(f"source validator accepted a synthetic body digest: {root}")
        elif resolver.replay_activation(bundle, expected_roots=[root]) != decision:
            raise ValueError(f"unrelated root changed: {root}")

    before_ids = {"control": digest(records[changed]), "uchc": packets[changed]["graph"]["root"]}
    after_ids = {"control": digest(changed_record), "uchc": new_packet["graph"]["root"]}
    if (any(before_ids[arm] == after_ids[arm] for arm in before_ids)
            or any(set(names) != expected for names in changed_roots.values())
            or set(rejected_by_source) != expected or resolver.get(changed) != records[changed]):
        raise ValueError("unexpected source mutation, definition identity, or invalidation set")
    return {
        "scope": "Counterfactual body-only revision at fixed source lock; affected bundles verified by full replay.",
        "source": resolver.source, "skill": changed, "append_utf8": suffix.decode(),
        "original_body_sha256": original_digest, "synthetic_body_sha256": new_digest,
        "definition_ids_before": before_ids, "definition_ids_after": after_ids, "bundle_ids": bundle_ids,
        "unique_definitions_in_scope": len(records), "verified_roots_per_arm": len(roots),
        "invalidated_per_arm": {arm: {"definitions": 1, "activation_bundles": len(names),
                                     "roots": sorted(names)} for arm, names in changed_roots.items()},
        "reused_definitions_per_arm": len(records) - 1,
        "unchanged_roots": sorted(set(roots) - expected),
        "synthetic_activations_rejected_by_pinned_source": sorted(rejected_by_source),
    }
# ratios: loc_comments=78:8 imports_exports=4:1 calls_definitions=31:1
