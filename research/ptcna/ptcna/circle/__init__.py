# ratios: loc_comments=9:8 imports_exports=4:1 calls_definitions=1:0
"""Circle layer — non-differentiating neural-payload composition and audit.

Usage:

    from ptcna.circle import compose_circle

    circle = compose_circle(["neural:0", "neural:1"], identity="circle:0")

``CircleTensor`` is the standalone structural output consumed by
``ptcna.seed``. The existing theta audit remains available through
``circle_audit``.
"""

from .audit import circle_audit
from .compose import compose_circle, star_polygon_order
from .tensor import CircleTensor

__all__ = [
    "CircleTensor",
    "compose_circle",
    "star_polygon_order",
    "circle_audit",
]
# ratios: loc_comments=9:8 imports_exports=4:1 calls_definitions=1:0
