"""Complete native plaintext construction and exact recovery.

Usage: bind a source-identified Operator to 'gonol' in Pipeline. Toggle only 'gonol'.
The native transformation is unresolved (Q1); this module declares its
interface and never supplies a fake identity, hash, XOR or conventional-cipher fallback.
No network or storage. See ASSEMBLY.md for the proposed answer and rollback.
"""
from .api import Step

STEP = Step('gonol', ('Q1',), 'Complete native plaintext construction and exact recovery.', required=True)
