"""Use actual thread-associated corpus content in the selected native relation.

Usage: bind a source-identified Operator to 'corpus' in Pipeline. Toggle only 'corpus'.
The native transformation is unresolved (Q4/Q7/Q8); this module declares its
interface and never supplies a fake identity, hash, XOR or conventional-cipher fallback.
No network or storage. See ASSEMBLY.md for the proposed answer and rollback.
"""
from .api import Step

STEP = Step('corpus', ('Q4', 'Q7', 'Q8'), 'Use actual thread-associated corpus content in the selected native relation.', required=True)
