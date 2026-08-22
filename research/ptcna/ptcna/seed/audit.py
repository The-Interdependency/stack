# ratios: loc_comments=11:12 imports_exports=1:1 calls_definitions=9:1
"""Seed-layer auditing — circles → seeds.

Auditing/timing only; non-differentiable. Extracted from the neural engine
(`PCNAEngine._ptca_seed_audit`) so the seed layer owns its own audit surface.
Pure function over duck-typed core objects — imports nothing from neural, so
no circular dependency.
"""

from __future__ import annotations


def seed_audit(cores: dict, memory_s) -> dict:
    """Aggregate per-core seed audits into the seed-layer report.

    ``cores`` maps ring name -> core object exposing ``seed_audit()`` (a list of
    per-node dicts with a ``coherence`` key) and ``ring_coherence``. ``memory_s``
    exposes ``state()["avg_hub"]``. Keys are preserved verbatim from the
    pre-consolidation engine so `_coherence_score` keeps working.
    """
    result: dict = {}
    for name, core in cores.items():
        audit = core.seed_audit()
        result[f"{name}_nodes_audited"] = len(audit)
        result[f"{name}_coherence"] = round(core.ring_coherence, 4)
        result[f"{name}_top3"] = sorted(audit, key=lambda x: x["coherence"], reverse=True)[:3]
        result[f"{name}_bottom3"] = sorted(audit, key=lambda x: x["coherence"])[:3]
    result["memory_s_hub_avg"] = memory_s.state()["avg_hub"]
    return result
# ratios: loc_comments=11:12 imports_exports=1:1 calls_definitions=9:1
