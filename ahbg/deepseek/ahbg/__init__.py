# ratios: loc_comments=68:1 imports_exports=5:1 calls_definitions=0:0


"""DeepSeek AHBG realization package."""

from .events import (
    EVENT_SCHEMA,
    KIND_BUILD,
    KIND_WAR,
    KIND_MOVE,
    KIND_PLANE_INIT,
    KIND_TURN_BEGIN,
    KIND_TURN_END,
    Event,
    EventLog,
)
from .persistence import load_world, new_game, replay, save_world
from .rng import (
    DM_DOMAIN,
    PROMPT_INJECTION_DOMAIN,
    WAR_DOMAIN,
    DeterministicRng,
)
from .turns import (
    BUILD_ACTION,
    MOVE_ACTION,
    BuildSpec,
    EngineError,
    WarSpec,
    MoveSpec,
    ReplayMismatch,
    TurnLoop,
    UnresolvedHmmm,
    ValidationError,
    axial_neighbors,
    built_tile_ids,
)
from .world import WORLD_SCHEMA, Tile, Unit, World

__all__ = [
    "BUILD_ACTION",
    "DM_DOMAIN",
    "EVENT_SCHEMA",
    "EngineError",
    "BuildSpec",
    "DeterministicRng",
    "Event",
    "EventLog",
    "KIND_BUILD",
    "KIND_WAR",
    "KIND_MOVE",
    "KIND_PLANE_INIT",
    "KIND_TURN_BEGIN",
    "KIND_TURN_END",
    "MOVE_ACTION",
    "MoveSpec",
    "WarSpec",
    "PROMPT_INJECTION_DOMAIN",
    "ReplayMismatch",
    "Tile",
    "TurnLoop",
    "Unit",
    "UnresolvedHmmm",
    "ValidationError",
    "WAR_DOMAIN",
    "WORLD_SCHEMA",
    "World",
    "axial_neighbors",
    "built_tile_ids",
    "load_world",
    "new_game",
    "replay",
    "save_world",
]
# ratios: loc_comments=68:1 imports_exports=5:1 calls_definitions=0:0
