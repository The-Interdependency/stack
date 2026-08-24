"""Engine error types.

All engine failures derive from :class:`EngineError` so callers can catch the
whole family. ``UnresolvedHmmm`` is the fail-closed marker for mechanics that
canonical rules have not fixed yet.
"""

from __future__ import annotations


class EngineError(Exception):
    """Base class for every AHBG engine error."""


class ValidationError(EngineError):
    """A plane, event, or declaration failed structural validation."""


class UnresolvedHmmm(EngineError):
    """A requested surface touches an unresolved ``hmmm`` rule.

    The engine fails closed instead of inventing mechanics. When canonical
    rules land, the guarded surface becomes an implementation instead of a
    raise.
    """


class ReplayMismatch(EngineError):
    """Persisted state does not match the event log replay."""
