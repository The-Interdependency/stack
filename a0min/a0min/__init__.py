# ratios: loc_comments=32:8 imports_exports=2:1 calls_definitions=0:0
"""a0min — minimal agent harness over the imported a0 platonic superpotential.

Public surface:
- PlatonicAgent, AgentDimension, AgentSemanticRegion, AgentProjection
  (imported verbatim from The-Interdependency/a0 @ f9470a74)
- candidate_platonic_agent — the open superpotential with current a0 regions
- Harness — creates any potential sub-agent by projecting a declared region
- SubAgent, PotentialSubAgent, SpawnCapExceeded
"""

from .harness import (
    SUPPORTED_CUT_MODES,
    SUPPORTED_ORCHESTRATION_MODES,
    Harness,
    PotentialSubAgent,
    SpawnCapExceeded,
    SubAgent,
)
from .platonic import (
    AgentDimension,
    AgentProjection,
    AgentSemanticRegion,
    PlatonicAgent,
    ZFAE_AGENT_DEF,
    candidate_platonic_agent,
    compose_name,
)

__all__ = [
    "AgentDimension",
    "AgentSemanticRegion",
    "AgentProjection",
    "PlatonicAgent",
    "candidate_platonic_agent",
    "ZFAE_AGENT_DEF",
    "compose_name",
    "Harness",
    "PotentialSubAgent",
    "SubAgent",
    "SpawnCapExceeded",
    "SUPPORTED_ORCHESTRATION_MODES",
    "SUPPORTED_CUT_MODES",
]
# ratios: loc_comments=32:8 imports_exports=2:1 calls_definitions=0:0
