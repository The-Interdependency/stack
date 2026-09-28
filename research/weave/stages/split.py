"""Generate the required logical thread streams without discarding cross-relations.

Usage: bind a source-identified Operator to 'split' in Pipeline. Toggle only 'split'.
The native transformation is unresolved (Q3); this module declares its
interface and never supplies a fake identity, hash, XOR or conventional-cipher fallback.
No network or storage. See ASSEMBLY.md for the proposed answer and rollback.
"""
from .api import Step

STEP = Step('split', ('Q3',), 'Generate the required logical thread streams without discarding cross-relations.', required=True)
