"""Bridges for running Grok's a0 regulatory layer against foreign AHBG boards.

The calibration produced three independent realizations:
- Grok (this tree): a0/ + ahbg/
- Codex: stack-codex/ahbg/codex/
- DeepCode: stack-deepcode/ahbg/deepseek/

This package lets Grok's Vessel + choose_relocate (the "a0" decision surface)
operate on a Codex or DeepCode "board" (their ahbg world + turn mechanics)
without modifying the frozen implementations.

Usage pattern (from stack/ahbg/grok):

    from bridges.codex import CodexBoardDriver
    from a0.selfhood import Vessel
    from a0.will import choose_relocate

    driver = CodexBoardDriver(seed=101)
    vessel = Vessel.instantiate(salt="bridge-demo")
    # ... drive turns using driver.empty_neighbors(unit), driver.submit_choice(...)

The adapters normalize tile ids and observation shape while preserving each
board's collision and replay semantics (War remains UnresolvedHmmm / ClosedUnknown).
"""

from .codex import CodexBoardDriver
from .deepcode import DeepCodeBoardDriver

# Viewer support (pygame optional at import time)
from .viewer import Viewer, make_driver

__all__ = ["CodexBoardDriver", "DeepCodeBoardDriver", "Viewer", "make_driver"]
