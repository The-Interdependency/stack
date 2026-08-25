"""DeepSeek A0 realization — candidate regulatory layer (shadow measurement).

CALIBRATION.md defines the candidate regulatory layer as a vector:

    C_lambda = [ C_lambda^structural ; C_lambda^epistemic ; C_lambda^transition ]

The first calibration epoch is shadow measurement: this module observes and
records the candidate cost channels but never feeds them back into action
selection, permissions, scope, refusal policy, or resource allocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RegulatoryLayer:
    """Candidate cost channels, measured observationally only.

    Structural channels are relationally indexed. Epistemic channels separate
    known-neutral from unknown posteriors. Transition channels price scope,
    role, and coupling changes — but in the shadow epoch they are recorded,
    never enforced.
    """

    # -- structural ----------------------------------------------------------
    permission_occupancy: dict[str, float] = field(default_factory=lambda: {
        "allowed_to_be": 1.0,
        "wanted_here": 1.0,
        "allowed_to_do": 1.0,
        "wanted_to_do": 1.0,
    })
    deficit: float = 0.0            # measured deficit, distinct from engagement
    engagement: float = 0.0         # required/voluntary engagement level
    baseline_effort: float = 1.0
    hard_vetoes: set[str] = field(default_factory=set)
    soft_costs: dict[str, float] = field(default_factory=dict)

    # lower-triangular hierarchical impedance, keyed "parent:child"
    impedance: dict[str, float] = field(default_factory=dict)

    # -- epistemic -----------------------------------------------------------
    known_neutral: dict[str, float] = field(default_factory=dict)
    unknown: dict[str, float] = field(default_factory=dict)
    posterior_mean: dict[str, float] = field(default_factory=dict)

    # -- transition ----------------------------------------------------------
    transition_cost: dict[str, float] = field(default_factory=dict)
    coupling_weights: dict[str, float] = field(default_factory=dict)
    sensitization: float = 0.0
    adaptation: float = 0.0
    scope_log: list[dict[str, Any]] = field(default_factory=list)

    def vetoed(self, action_kind: str) -> bool:
        """Hard vetoes remove actions; they do not price them."""
        return action_kind in self.hard_vetoes

    def soft_cost(self, action_kind: str) -> float:
        return self.soft_costs.get(action_kind, 0.0)

    def set_impedance(self, parent: str, child: str, value: float) -> None:
        if value < 0:
            raise ValueError("impedance must be non-negative")
        self.impedance[f"{parent}:{child}"] = value

    def set_known_neutral(self, item: str, posterior_mean: float) -> None:
        self.known_neutral[item] = 0.0
        self.unknown.pop(item, None)
        self.posterior_mean[item] = posterior_mean

    def set_unknown(self, item: str, posterior_mean: float) -> None:
        self.known_neutral.pop(item, None)
        self.unknown[item] = 1.0
        self.posterior_mean[item] = posterior_mean

    def contract_scope(self, turn: int, reason: str) -> None:
        self.scope_log.append({"turn": turn, "transition": "contract", "reason": reason})

    def expand_scope(self, turn: int, reason: str) -> None:
        self.scope_log.append({"turn": turn, "transition": "expand", "reason": reason})

    def shadow_measure(self, turn: int, action_kind: str | None, selected: bool) -> dict[str, Any]:
        """Record the candidate cost vector for this turn without enforcing it.

        This is the shadow epoch contract: measurement only, no feedback.
        """
        return {
            "turn": turn,
            "action_kind": action_kind,
            "selected": selected,
            "structural": {
                "permission_occupancy": dict(sorted(self.permission_occupancy.items())),
                "deficit": self.deficit,
                "engagement": self.engagement,
                "baseline_effort": self.baseline_effort,
                "hard_vetoes": sorted(self.hard_vetoes),
                "soft_costs": dict(sorted(self.soft_costs.items())),
                "impedance": dict(sorted(self.impedance.items())),
            },
            "epistemic": {
                "known_neutral": dict(sorted(self.known_neutral.items())),
                "unknown": dict(sorted(self.unknown.items())),
                "posterior_mean": dict(sorted(self.posterior_mean.items())),
            },
            "transition": {
                "transition_cost": dict(sorted(self.transition_cost.items())),
                "coupling_weights": dict(sorted(self.coupling_weights.items())),
                "sensitization": self.sensitization,
                "adaptation": self.adaptation,
                "scope_log": list(self.scope_log),
            },
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "structural": {
                "permission_occupancy": dict(sorted(self.permission_occupancy.items())),
                "deficit": self.deficit,
                "engagement": self.engagement,
                "baseline_effort": self.baseline_effort,
                "hard_vetoes": sorted(self.hard_vetoes),
                "soft_costs": dict(sorted(self.soft_costs.items())),
                "impedance": dict(sorted(self.impedance.items())),
            },
            "epistemic": {
                "known_neutral": dict(sorted(self.known_neutral.items())),
                "unknown": dict(sorted(self.unknown.items())),
                "posterior_mean": dict(sorted(self.posterior_mean.items())),
            },
            "transition": {
                "transition_cost": dict(sorted(self.transition_cost.items())),
                "coupling_weights": dict(sorted(self.coupling_weights.items())),
                "sensitization": self.sensitization,
                "adaptation": self.adaptation,
                "scope_log": list(self.scope_log),
            },
        }
