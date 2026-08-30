# ratios: loc_comments=13:12 imports_exports=1:1 calls_definitions=4:1
"""Circle-layer auditing — neural tensors → circles.

Auditing/timing only; non-differentiable. Extracted from the neural engine
(`PCNAEngine._pcta_circle_audit`) so the circle layer owns its own audit
surface. Pure function over duck-typed objects — imports nothing from neural,
so no circular dependency.
"""

from __future__ import annotations


def circle_audit(theta, memory_l) -> dict:
    """Build the circle-layer report from the theta circle object.

    ``theta`` exposes ``circle_audit()`` (a list of per-node dicts with ``gate``
    and ``circles`` keys) and ``node_coherence`` (mean()-able). ``memory_l``
    exposes ``state()["avg_hub"]``. Keys preserved verbatim from the
    pre-consolidation engine.
    """
    g_audit = theta.circle_audit()
    open_nodes = [n for n in g_audit if n["gate"]]
    closed_nodes = [n for n in g_audit if not n["gate"]]
    return {
        "theta_nodes": len(g_audit),
        "gates_open": len(open_nodes),
        "gates_closed": len(closed_nodes),
        "avg_circles": round(sum(n["circles"] for n in g_audit) / len(g_audit), 2),
        "theta_coherence": round(float(theta.node_coherence.mean()), 4),
        "memory_l_hub_avg": memory_l.state()["avg_hub"],
    }
# ratios: loc_comments=13:12 imports_exports=1:1 calls_definitions=4:1
