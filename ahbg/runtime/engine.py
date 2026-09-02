"""Load the frozen Grok engine and A0 package by file path.

The canonical engine lives at ``ahbg/grok/ahbg/`` and is imported under the
name ``ahbg`` by its own runner. The production runtime lives at
``ahbg/runtime/`` and must import the engine without depending on which
``ahbg`` parent package wins on ``sys.path``. Loading by file path keeps the
frozen engine authoritative while letting ``ahbg.runtime`` remain a separate
namespace sibling.

Nothing here reimplements engine behavior; it only binds the frozen modules.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

_GROK_ROOT = Path(__file__).resolve().parents[1] / "grok"
_AHBG_DIR = _GROK_ROOT / "ahbg"
_A0_DIR = _GROK_ROOT / "a0"

_ENGINE_MODULES = ("patch", "chain", "keep", "round")
_A0_MODULES = ("selfhood", "will")


def _load(package_name: str, name: str, path: Path) -> ModuleType:
    full_name = f"{package_name}.{name}"
    spec = importlib.util.spec_from_file_location(full_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {full_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    return module


def load_engine() -> tuple[ModuleType, ModuleType, ModuleType, ModuleType]:
    """Return ``(patch, chain, keep, round)`` frozen engine modules."""
    return tuple(  # type: ignore[return-value]
        _load("_ahbg_frozen_engine", name, _AHBG_DIR / f"{name}.py")
        for name in _ENGINE_MODULES
    )


def load_a0() -> tuple[ModuleType, ModuleType]:
    """Return ``(selfhood, will)`` frozen A0 modules."""
    return tuple(  # type: ignore[return-value]
        _load("_ahbg_frozen_a0", name, _A0_DIR / f"{name}.py")
        for name in _A0_MODULES
    )
