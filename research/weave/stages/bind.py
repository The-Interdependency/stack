"""Native public operation and private-gonol recovery relation.

Usage: bind a source-identified Operator to 'bind' in Pipeline. Toggle only 'bind'.
The native transformation is unresolved (Q2/Q7/Q8); this module declares its
interface and never supplies a fake identity, hash, XOR or conventional-cipher fallback.
No network or storage. See ASSEMBLY.md for the proposed answer and rollback.
"""
from .api import Step

STEP = Step('bind', ('Q2', 'Q7', 'Q8'), 'Native public operation and private-gonol recovery relation.', required=True)
