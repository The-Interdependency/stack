# Example: Chessboard Tensor

## Purpose

The chessboard example makes METAPAT's use of `tensor` concrete without importing a domain definition as root.

It shows simultaneity, scalar/vector/matrix readability, and nesting or recursion in an ordinary bounded system.

## Statement

A chessboard at one moment is a tensor: a simultaneous arrangement of bounded state-bearing positions and relations.

The board does not become a tensor only when pieces are placed on it. An empty board already retains a simultaneous arrangement of distinguished squares, files, ranks, adjacency, and boundaries.

## Simplexes and state

Each square is a bounded position-simplex within the board tensor.

A square may hold a state such as:

- empty;
- occupied;
- piece identity;
- side or color;
- other rule-relevant state when the chosen model requires it.

Pieces may themselves be modeled as simplexes with their own state and relations.

The whole board can therefore contain nested tensor structure while remaining one tensor at board scale.

## Scalar, vector, and matrix readability

A chosen board property may be read as a scalar state.

A move or directed influence may be read as vector-like state or transformation.

The complete board position may be represented as an `8 x 8` matrix or by richer higher-order structures.

These representations may clarify the tensor, but they do not define METAPAT tensorhood. METAPAT calls the board a tensor because the state is simultaneously arranged before any move is sequenced.

## Transformation and time

A legal move alters the current tensor state.

```text
board tensor at state B0
        |
        | move / transformation
        v
board tensor at state B1
```

A sequence of moves produces sequential tensor alteration:

```text
B0 -> B1 -> B2 -> ...
```

Under METAPAT, that sequence is time at the modeled game scale.

The board position is the simultaneous tensor-state; the move is transformation; the game history is sequential tensor alteration.

## Nesting and recursion

Tensor does not mean atomic.

At board scale, the full chess position is one tensor.

Within it:

- squares retain bounded state;
- pieces retain state and relational possibilities;
- local relations participate in larger board relations;
- the board may itself participate in a larger tournament, computational, social, or recorded tensor.

A tensor may therefore contain or participate in tensors at other scales without losing its own native-scale tensorhood.

## Domain restraint

Chess supplies an explanatory example, not the definition of tensor.

Likewise, representing a chessboard with a mathematical matrix or computational tensor does not transfer those domain definitions into the METAPAT root.

The example demonstrates the METAPAT distinction:

```text
tensor      = simultaneous arranged state
position    = current tensor-state
move        = transformation
game        = sequential tensor alteration
```

## Guardrail

Do not say:

```text
The chessboard is a METAPAT tensor because it is an 8 x 8 matrix.
```

Say:

```text
The chessboard is a METAPAT tensor because its bounded states and relations exist in simultaneous arrangement.
An 8 x 8 matrix is one possible representation of that arrangement.
```

## hmmm

Chess makes tensor structure unusually legible because the boundaries, simultaneous positions, nested states, transformations, and sequence are explicit. The same explanatory pattern should not be assumed to fit a less clearly bounded system until its distinctions, simplexes, and relations are actually identified.
