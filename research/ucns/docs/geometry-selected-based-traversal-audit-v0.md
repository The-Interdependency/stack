# Geometry-selected based traversal audit v0

**Standing:** stack-local target-free geometry-selection obstruction audit.
Not UCNS canon, not an attaching-word constructor, and not an arithmetic
readout.

## Question

The ordered return groupoid can represent:

```text
g1 g2 g3 != g2 g3 g1 != g1 g3 g2
```

Representation does not select one word. This audit asks whether current
Public Gonol and recursive UCNS geometry supply the marks needed to choose one
based, oriented complete-return traversal without using:

- carrier tuple order;
- API or local-frame defaults;
- caller-supplied coupling order;
- recursive construction ordinals;
- seed-event order without a recursive attachment;
- ids, hashes, or arithmetic observations.

A canonical choice must be preserved by every symmetry of the admitted
geometric structure. If a symmetry preserves that structure while moving a
proposed word, the structure does not select the word.

## Origin is not yet attachment

Pinned canon does contain an exact distinguished carrier origin:

```text
Public Gonol position = 0
direct Structural Null carrier position = 0
```

This evidence is retained. It is not discarded as arbitrary indexing.
However, canonical carrier Structural Null is coordinate-free, and current
UCNS defines no map from it to the non-null promoted return-groupoid object:

```text
Public Gonol / Structural Null origin
    -- missing geometric attachment -->
promoted positive-frame groupoid base object
```

The groupoid therefore has a model base object, but not a Public-Gonol-selected
basepoint. Glyph meaning is not used.

## Direction is not selected

Write a native Mobius state as one lifted coordinate `u mod 2`, where the two
unit intervals encode the positive and reversed local frames. The exact map:

```text
rho(u) = -u mod 2
```

fixes the phase-zero positive state and satisfies:

```text
rho(state.advance(d)) = rho(state).advance(-d)
```

The audit checks this exactly for 35 state/displacement pairs. At integer
turns, positive and negative complete-return traces are identical:

```text
0 ->  1 ->  2 : positive, reversed, positive
0 -> -1 -> -2 : positive, reversed, positive
```

A directed carrier attachment or chirality could break this symmetry, but no
Public-Gonol-to-recursive-return attachment currently transports such a
direction. Positive displacement in the local API is not enough.

## Triality has no selected permutation

At rank three, the current unmarked return shape has:

- one shared model base vertex;
- three relation-specific degree-two midpoint vertices;
- three identical local return traces;
- no geometric loop labels;
- no rotation system or marked outgoing dart;
- no cross-generator relators or monodromy.

Every loop renaming in `S3` preserves those data. Acting on one once-each word
produces the full orbit:

```text
g1 g2 g3    g1 g3 g2
g2 g1 g3    g2 g3 g1
g3 g1 g2    g3 g2 g1
```

Orbit size is six. No once-each word is fixed by all six actions. Every word
still has homology vector `(1,1,1)`.

Recursive ordinals and relation ids can label the loops, but they are
construction provenance and addresses. No geometric path currently visits
the loops in ordinal order, reverse ordinal order, or any other order.

## Exact missing object

A future geometry-selected based traversal must supply all five marks with
replayable geometric provenance:

1. An attachment from an intrinsic Public Gonol point to one groupoid object.
2. A directed tangent, chirality, or equivalent orientation at that attachment.
3. An oriented rotation or successor system on incident return germs.
4. A geometrically marked outgoing dart that chooses the word's start.
5. A complete-return closure rule that declares the resulting word an
   attaching or monodromy word.

An oriented rotation system without a marked dart still leaves cyclic
conjugacy. A marked basepoint without orientation still leaves reversal. All
five fields are currently null.

## Result

```text
STATUS = STOP_NO_GEOMETRY_SELECTED_BASED_TRAVERSAL

geometry-selected basepoint       = null
geometry-selected orientation     = null
geometry-selected traversal word  = null
geometry-selected attaching word  = null
global monodromy                   = null
arithmetic readout                 = null
numerical successor               = null
```

This is the requested stop condition. The next research object is not a prime,
determinant, or guessed word. It is the missing geometric attachment and
marked oriented rotation structure.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/geometry_selected_based_traversal_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_geometry_selected_based_traversal_audit.py -v
```

Frozen identities:

```text
geometry_selected_based_traversal_audit.py sha256 = f3c8cc74fe209d9849e5aff77647928e0798be64c9040dc57759b4351ba1e684
test module sha256                                  = 8ac29772854e5ddddb7c932bb13293d34737098c82c99d7b7a0f260c4c3f31dc
canonical receipt payload sha256                    = 4c4f06aae237fd4ce771dc7849738617b0cbc9ab3cc5bd6685ffec84b2921a09
formatted receipt file sha256                        = f331c5a9f2479251c19dd6c77c593724b61b3a3a45c2e14e73f131ff653b368e
```

## hmmm

- Does full Public Gonol geometry attach Structural Null to a non-null return
  state, or is another intrinsic point the actual basepoint?
- What geometric tangent, chirality, or directed germ survives that
  attachment?
- What incidence supplies a rotation system among retained return loops?
- What marks the first outgoing dart so cyclic rotations remain distinct?
- What closure turns the selected path into an attaching or monodromy word?

