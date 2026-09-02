"""Entitlement boundary for AHBG premium features.

One clean entitlement: ``benchmark_lab``.

* Basic gameplay and external harness connectivity are always available.
* ``benchmark_lab`` unlocks advanced scenarios, saved/replayed run comparison,
  and adversarial benchmark packs.

The runtime only *checks* an entitlement claim. Entitlement verification
(RevenueCat receipt validation) happens on the client; a runtime that receives
an unverified claim must treat it as absent unless the deployment explicitly
configures a trusted verifier. This keeps the runtime honest without embedding
store SDK keys.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

ENTITLEMENT_BENCHMARK_LAB = "benchmark_lab"
FREE_ENTITLEMENTS = ("basic",)

# Features gated behind the single entitlement.
GATED_FEATURES = (
    "advanced_scenarios",
    "saved_run_comparison",
    "adversarial_benchmark_packs",
)


class EntitlementError(PermissionError):
    """A premium feature was requested without the Benchmark Lab entitlement."""


@dataclass(frozen=True)
class EntitlementGate:
    entitlements: frozenset[str] = frozenset(FREE_ENTITLEMENTS)

    @classmethod
    def from_claims(cls, claims: Iterable[str]) -> "EntitlementGate":
        return cls(frozenset(FREE_ENTITLEMENTS) | frozenset(claims))

    def has(self, entitlement: str) -> bool:
        return entitlement in self.entitlements

    def has_benchmark_lab(self) -> bool:
        return self.has(ENTITLEMENT_BENCHMARK_LAB)

    def require(self, feature: str) -> None:
        if feature not in GATED_FEATURES:
            raise ValueError(f"unknown gated feature {feature!r}")
        if not self.has_benchmark_lab():
            raise EntitlementError(
                f"feature {feature!r} requires entitlement {ENTITLEMENT_BENCHMARK_LAB!r}"
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "entitlements": sorted(self.entitlements),
            "benchmark_lab": self.has_benchmark_lab(),
            "free_features": ["basic_play", "external_harness"],
        }
