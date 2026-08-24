# ratios: loc_comments=17:9 imports_exports=2:1 calls_definitions=0:0
"""Imported platonic agent package.

Files in this package are verbatim imports from The-Interdependency/a0 @
f9470a74138da89a2d075ecf6c3241aac63923f1:

- platonic.py           python/agents/platonic.py
- platonic_regions.py   python/agents/platonic_regions.py
- zfae.py               python/agents/zfae.py

They retain their a0 canonical ratios seals; this package only re-exports the
public surface for the a0min harness.
"""

from .platonic import (
    AgentDimension,
    AgentProjection,
    AgentSemanticRegion,
    PlatonicAgent,
    candidate_platonic_agent,
)
from .zfae import ZFAE_AGENT_DEF, compose_name

__all__ = [
    "AgentDimension",
    "AgentSemanticRegion",
    "AgentProjection",
    "PlatonicAgent",
    "candidate_platonic_agent",
    "ZFAE_AGENT_DEF",
    "compose_name",
]
# ratios: loc_comments=17:9 imports_exports=2:1 calls_definitions=0:0
