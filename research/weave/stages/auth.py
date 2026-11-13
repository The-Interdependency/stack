"""Optional integrity/replay relation, separate from confidentiality.

Usage: bind a source-identified Operator to 'auth' in Pipeline. Toggle only 'auth'.
The native transformation is unresolved (Q10); this module declares its
interface and never supplies a fake identity, hash, XOR or conventional-cipher fallback.
No network or storage. See ASSEMBLY.md for the proposed answer and rollback.
"""
from .api import Step

STEP = Step('auth', ('Q10',), 'Optional integrity/replay relation, separate from confidentiality.', required=False)
