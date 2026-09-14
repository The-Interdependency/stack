"""English Gonol construction package.

The full-corpus builder executes the exact committed UCNS ``public_gonol.py``
bytes rather than importing an ambient package. Python dataclasses resolve
postponed annotations through ``sys.modules`` while a class is being created,
so reserve the verified execution module name before that exact-byte execution.
This carries no geometry and supplies no construction data; it is only the
runtime namespace required for verification of the pinned source module.
"""

from __future__ import annotations

import sys
from types import ModuleType

_VERIFIED_PUBLIC_GONOL_MODULE = "_english_gonol_verified_public_gonol"

if _VERIFIED_PUBLIC_GONOL_MODULE not in sys.modules:
    sys.modules[_VERIFIED_PUBLIC_GONOL_MODULE] = ModuleType(
        _VERIFIED_PUBLIC_GONOL_MODULE
    )
