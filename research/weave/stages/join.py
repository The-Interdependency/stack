"""Interlace and recover threads under the exact selected route.

Usage: bind a source-identified Operator to 'join' in Pipeline. Toggle only 'join'.
The native transformation is unresolved (Q5/Q8); this module declares its
interface and never supplies a fake identity, hash, XOR or conventional-cipher fallback.
No network or storage. See ASSEMBLY.md for the proposed answer and rollback.
"""
from .api import Step

STEP = Step('join', ('Q5', 'Q8'), 'Interlace and recover threads under the exact selected route.', required=True)
