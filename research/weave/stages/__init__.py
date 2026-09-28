"""Explicit registry for the proposed complete data path; no dynamic imports.
Usage: STEPS is forward order; reversal is performed only by assembly.Pipeline.
"""
from .gonol import STEP as GONOL
from .bind import STEP as BIND
from .split import STEP as SPLIT
from .corpus import STEP as CORPUS
from .inter import STEP as INTER
from .join import STEP as JOIN
from .whole import STEP as WHOLE
from .auth import STEP as AUTH

STEPS = (GONOL, BIND, SPLIT, CORPUS, INTER, JOIN, WHOLE, AUTH)
