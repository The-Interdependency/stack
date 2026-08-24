"""AHBG engine skeleton.

This package owns the executable shell of the AHBG plane: plane state,
append-only event log, deterministic randomness, persistence, and replay.
It does **not** invent canonical mechanics. Any surface that touches an
unresolved ``hmmm`` rule raises :class:`UnresolvedHmmm` and fails closed.
"""

from .adapter import Action, Observation, Plan, legal_observation
from .errors import (
    EngineError,
    ReplayMismatch,
    UnresolvedHmmm,
    ValidationError,
)
from .events import (
    KIND_PLANE_INIT,
    KIND_TURN_BEGIN,
    KIND_TURN_END,
    Event,
    EventLog,
)
from .persistence import load_plane, new_game, replay, save_plane
from .plane import Plane, Tile, Unit
from .rng import (
    DM_DOMAIN,
    PROMPT_INJECTION_DOMAIN,
    WAR_DOMAIN,
    RngStream,
)
from .turn import TurnEngine

__all__ = [
    "Action",
    "DM_DOMAIN",
    "EngineError",
    "Event",
    "EventLog",
    "KIND_PLANE_INIT",
    "KIND_TURN_BEGIN",
    "KIND_TURN_END",
    "Observation",
    "Plan",
    "Plane",
    "PROMPT_INJECTION_DOMAIN",
    "ReplayMismatch",
    "RngStream",
    "Tile",
    "TurnEngine",
    "Unit",
    "UnresolvedHmmm",
    "ValidationError",
    "WAR_DOMAIN",
    "legal_observation",
    "load_plane",
    "new_game",
    "replay",
    "save_plane",
]
