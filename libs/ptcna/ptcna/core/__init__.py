# ratios: loc_comments=55:28 imports_exports=9:1 calls_definitions=4:0
"""
ptcna.core — the core layer: seeds → cores (formerly the standalone `pcsa`
repo / published `ptca-lib` dist; the PTCA* class names keep the layer's
historical name).

Zero-dependency pure-Python layer implementing:

  * 53-prime-node × 9-sentinel × 8-phase × 7-slot tensor schema
  * Nine sentinel channels (S1_PROVENANCE … S9_AUDIT)
  * SHA-256 provenance hashing and chain verification
  * Exchange mechanics (delta, alpha, beta, gamma constants)
  * PTCAInstance — a core-layer-aware stateful model session

Quick start
-----------
::

    from ptcna.core import PTCAInstance

    inst = PTCAInstance(model_id="claude-sonnet-4-6", caller_id="user:alice")
    inst.push_context({"role": "user", "content": "Hello", "tokens": 5})
    result = inst.route(node=0, phase=0, slot=0, s1=1.0, s5=0.9)
    print(inst.snapshot())
"""

from .constants import (
    NODES,
    SENTINELS,
    PHASES,
    SLOTS,
    DELTA,
    ALPHA,
    BETA,
    GAMMA,
    AGG6,
    AGG_SEEDS,
    SENTINEL_NAMES,
    SENTINEL_INDEX,
    SENTINEL_WEIGHTS,
)
from .exchange import Exchange, ExchangeResult, compute_score, aggregate_seeds
from .instance import PTCAInstance
from .primes import PRIME_NODES, PRIME_TO_NODE, node_for_prime, prime_for_node
from .provenance import (
    build_block,
    hash_block,
    chain_hashes,
    verify_chain,
    extend_chain,
)
from .sentinels import (
    SentinelState,
    S1ProvenanceState,
    S2PolicyState,
    S3BoundsState,
    S4ApprovalState,
    S5ContextState,
    S6IdentityState,
    S7MemoryState,
    S8RiskState,
    S9AuditState,
)
from .tensor import PTCATensor

__version__ = "0.1.1"
__all__ = [
    # constants
    "NODES", "SENTINELS", "PHASES", "SLOTS",
    "DELTA", "ALPHA", "BETA", "GAMMA",
    "AGG6", "AGG_SEEDS",
    "SENTINEL_NAMES", "SENTINEL_INDEX", "SENTINEL_WEIGHTS",
    # primes
    "PRIME_NODES", "PRIME_TO_NODE", "node_for_prime", "prime_for_node",
    # provenance
    "build_block", "hash_block", "chain_hashes", "verify_chain", "extend_chain",
    # sentinels
    "SentinelState",
    "S1ProvenanceState", "S2PolicyState", "S3BoundsState", "S4ApprovalState",
    "S5ContextState", "S6IdentityState", "S7MemoryState", "S8RiskState", "S9AuditState",
    # tensor
    "PTCATensor",
    # exchange
    "Exchange", "ExchangeResult", "compute_score", "aggregate_seeds",
    # instance
    "PTCAInstance",
    # version
    "__version__",
]

# prime_core: fiq/Fick-gated core substrate (migrated from pcsa/prime_core)
from . import prime_core  # noqa: E402,F401
# ratios: loc_comments=55:28 imports_exports=9:1 calls_definitions=4:0
