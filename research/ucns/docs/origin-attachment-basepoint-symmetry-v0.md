# Origin-attachment basepoint symmetry v0

**Standing:** stack-local pre-ratification symmetry obstruction. Not UCNS
canon, not an origin attachment, and not a downstream constructor result.

## Question

Can the missing map

```text
iota: {o} -> V(T),  iota(o) = v0
```

select a unique unframed `v0` from current pinned UCNS geometry without adding
a mark or breaking symmetry?

## Exact candidate T

The Public Gonol carrier has no canonical traversal operation, and the full
recursive structure is absent. The smallest pinned-canon structure that is
actually traversable is therefore the unframed visible quotient of the native
Mobius root loop.

Using the exact rational state domain implemented by `direct_mobius.py`:

```text
Obj(T) = Q/Z
Mor(T) = {([q], d) : [q] in Q/Z, d in Q}

s([q], d) = [q]
t([q], d) = [q+d]

([q], d) then ([q+d], e) = ([q], d+e)
```

The frame is forgotten only for this object-level basepoint test. Rational
displacement remains attached to each path, so one-turn and two-turn paths are
not erased. Structural Null is not an object of `T`; current canon supplies no
incident path from it into `T`.

The exact symbolic enumeration is:

```text
V(T) = {a/b : b > 0, 0 <= a < b, gcd(a,b)=1}
```

Every phase class is admissible. None is marked or excluded by current
geometry.

## Automorphism group

Require an automorphism to preserve every signed rational displacement label.
For each `[c] in Q/Z`, define:

```text
tau_c([q])    = [q+c]
tau_c([q], d) = ([q+c], d)
```

These translations preserve source, target, identity, inverse, and
composition. They form `Q/Z` under addition.

They are all the label-preserving automorphisms. If `F` is one such
automorphism and `[c] = F([0])`, equivariance gives:

```text
F([q]) = F([0]+q) = F([0])+q = [c+q].
```

Therefore:

```text
Aut_Q(T) is isomorphic to Q/Z.
```

Allowing a larger symmetry that also reverses displacement sign would not help
select a point; the translation subgroup alone is already transitive.

## Orbit partition

For arbitrary `[x]` and `[y]`, the unique translation with
`[c] = [y-x]` sends `[x]` to `[y]`. Hence the action is free and transitive:

```text
V(T) / Aut_Q(T) = { Q/Z }
```

There is exactly one orbit and no unique object within it. The quotient has no
canonical object-valued section.

The fixed-point obstruction is explicit:

```text
tau_[1/2]([q]) = [q+1/2] != [q]  for every [q] in Q/Z.
```

In particular, phase zero is moved to phase one-half while every admitted
unframed relation is preserved. Phase zero is therefore a coordinate/API
representative, not an intrinsic `v0`.

## Apparent alternatives

- Public Gonol's exact 157-position carrier is not `T`: canon defines no
  traversal or incidence on those positions.
- The non-null directed carrier has transitive angular shells, but Structural
  Null selects no positive breadth and is incident to no shell.
- The stack-local subdivided return bouquet would have a unique high-valence
  center for rank at least two. It does not qualify: that center is created by
  the candidate's shared positive-basepoint attachment, whose geometric
  authorization is the unresolved fact under test. Importing it would be
  circular.

## Outcome

```text
status                   = TRANSITIVE_SYMMETRY
secondary classification = UNIQUE_ORBIT_NOT_OBJECT
unique orbit             = true
unique object            = false
iota                     = null
tangent/chirality        = not evaluated
downstream fields        = not evaluated
```

No `iota` is implemented.

## Minimum additional structure

Within this `T`, the smallest structural kind that suffices is one
geometry-derived distinguished unframed zero-cell, or an equivalent unique
singularity or boundary incidence. Marking `b` restricts translations to:

```text
{tau_c : tau_c(b)=b} = {tau_0}
```

because the action is free. Current canon supplies no such mark. A future full
recursive `T` could instead derive a unique branch, valence, singularity,
boundary incidence, or unique invariant extremum, but that would be new
geometry and must be ratified independently.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/origin_attachment_basepoint_symmetry.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_origin_attachment_basepoint_symmetry.py -v
```

Frozen identities are recorded in the machine-readable receipt:
[`../receipts/origin-attachment-basepoint-symmetry-v0.json`](../receipts/origin-attachment-basepoint-symmetry-v0.json).

```text
UCNS commit                         = 1975fe70cf4e0826a8020c2da3047569e277af64
UCNS tree                           = 06c2fe6cf2e148d610808c6f00f4a26e85f43d62
origin-gap receipt payload          = f0f2a4a127e7a83c26291b94f58543b6881f7e1eda52940c7df3c14b121ad0f4
ordered-groupoid receipt payload    = cf61151f9e9ce1479b6d7eb95ff51bb2a683045de292243e1f14a9b3dd050f69
symmetry audit module sha256         = 6728b2cac11caa5c5ca26efb40a1bf01f6856be08a38796c952648c38397d214
symmetry test module sha256          = 71048b9aaccdfc8e511a46f5294b79a33998927cb12a73ab707ea3b14ef531e5
canonical receipt payload            = 5b38d70047ec62ba4c269b13f0f41f3e0c5f661d9f9b317bf8cf8c2b61cda197
formatted receipt file sha256        = 95b244c662b0442f99865ef24cbdd6f86e8e09b6bc9b2bb2565746821c98f21b
```

## hmmm

The current wall is homogeneous. It contains no intrinsic place for a door.
Someone must add a genuine geometric mark, singularity, or incidence before
one point can become the canonical attachment object.
