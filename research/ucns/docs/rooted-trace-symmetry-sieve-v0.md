# Rooted trace symmetry sieve v0

**Standing:** stack-local post-observation falsification research. Not UCNS
canon, not a successor constructor, and not a PCEA or cryptographic claim.

## Question

The event/trace lift candidate exposes the third comparison state as:

```text
(54837698421 - 1) / 4 = 13709424605
```

If that integer is the number of complete connected construction orders of the
next rooted graph, what must be true of that graph before an exact constructor
is attempted?

## Divisibility theorem

Every rooted graph automorphism maps a valid complete construction order to
another valid order. The action is free: if an automorphism fixes a total order
of every nonroot vertex position by position, it fixes every vertex and is the
identity. Therefore:

```text
|rooted automorphism group| divides |complete construction orders|
```

This is a necessary condition, not a constructor.

## Seed replay

The pinned seven-band structural graph is the wheel graph with `CENTER` fixed.
Its rooted automorphism group is `D6`, of order `12`:

```text
seed construction traces = 720
rooted symmetry order     = 12
free trace orbits         = 60
```

This independently checks the divisibility law at the only graph whose
construction rule is currently executable. The numerical `720 = 6!` trace
count must remain distinct from the source's separately declared 720-degree
Möbius return; matching numerals do not establish matching units.

## Third-gate sieve

Exact trial factorization gives:

```text
13709424605 = 5 * 2741884921
```

It is odd and is not divisible by `3`, `6`, or `12`. Two bounded symmetry
classes therefore fail:

| candidate class | required rooted symmetry | frozen trace count | result |
|---|---:|---:|---|
| complete radius-two hex disk under unchanged adjacency | `12` | `97934946851520` | `FALSIFIED` |
| two identical seed faces coupled symmetrically to one origin | layer-swap `2` | `1779148800` | `FALSIFIED` |

The exact trace counts are witnesses, but they are not needed for the broad
elimination: divisibility alone rules out any complete-trace candidate retaining
those rooted symmetries.

## Surviving constraints

If the third quotient is a connected construction-trace count, the next-scale
mechanic cannot be bare `D6` adjacency. At least one of these distinctions must
be resolved before another constructor test:

- phase or chirality changes build admissibility and breaks the rooted symmetry;
- ordered coupling distinguishes otherwise interchangeable faces;
- an explicitly authorized symmetry quotient changes what is counted;
- the recursive state extractor is not a construction-trace count.

The last alternative remains live because `157 = 1 + 4*39` uses a projection
event count while `2881 = 1 + 4*720` uses a construction-trace count. No
unchanged extractor has yet connected those identities.

```text
FALSIFIED_SYMMETRY_CLASSES = 2
CONSTRUCTOR_SURVIVORS      = 0
NEXT_PREDICTION            = hmmm
```

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/rooted_trace_symmetry_sieve.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_rooted_trace_symmetry_sieve.py -v
```

Frozen producer identities:

```text
rooted_trace_symmetry_sieve.py sha256 = 2f4cea88bef33f2883127495f0283501589a00361c359f384fc2688803200b55
test module sha256                       = 0bba86aab3c07b23cf79f9fcac08e3bfa361474ed06867b03bea5b10eb14550a
canonical receipt payload sha256         = 00aade4e906b55f65854f4623a52820268b07b66752185576db77cc1353adfbf
formatted receipt file sha256            = 866aa32f50a846d0c9a93e9f6a6b874da8d9bf958289b515a14b6fbc270067ed
```

## hmmm

- The complete `2881`-gonol graph and its decorated phase/chirality state do
  not exist in current UCNS authority.
- Breaking a symmetry after observing the target would be tuning unless the
  asymmetry follows from independently declared geometry.
- Quotienting trace orbits would need an explicit UCNS equivalence relation;
  division by a symmetry order is not automatically a geometric operation.
- No next value can be frozen until one executable state extractor and one
  recursive graph construction survive both observed gates unchanged.
