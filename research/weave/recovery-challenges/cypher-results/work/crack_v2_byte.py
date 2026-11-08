#!/usr/bin/env python3
"""Exact-schedule inverter for v2 byte/reflection rows without A.
Schedules come from public matrix.py; S spec brute over the public catalog
(3 paths x 5 arities x 2 end orders), one spec shared by all S in a row
(operations.py:129-132 reads parameters['spec']). N inverse = slice
data[44:44+L] (cycle.py:290); the corpus checks (cycle.py:286-289) are skipped
because they only validate. Output
