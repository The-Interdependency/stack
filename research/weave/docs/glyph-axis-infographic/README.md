# Whole glyphs. New axes.

GPT generated; context, prompt Erin Spencer.

This infographic records Erin's clarification, **“each is a glyph (ucns objects)”**, in the eight-position stacking discussion. Each occupied cell carries a whole native participant and its distinct occurrence address. Changing the arrangement preserves the participant instead of replacing it with a Unicode encoding byte.

Standing: **construction illustration, exact combinatorial counts, and a checked 64-occurrence address permutation**. This documentation does not select a new UCNS carrier, implement higher-dimensional native closure, or alter Weave's executable cycle.

![Whole glyphs retain their native objects while a clockwise square rotation moves a highlighted row into the rightmost column. The exact position, line and slice counts increase through eight axes. Three cube views retain the same occurrence and its row, column and fixed-coordinate addresses.](glyph-axis-infographic.png)

## Use the figure

- [PNG](glyph-axis-infographic.png): phone viewing and sharing.
- [SVG](glyph-axis-infographic.svg): scalable, editable vector artwork. Letterforms are paths for consistent rendering; this page supplies accessible text.
- [PDF](glyph-axis-infographic.pdf): zooming and print.
- [Evidence](evidence.json): exact producer identity, operation checks, counts and export digests.
- [Work graph](work-graph.json): source roles and the non-transfer boundary.

The figure is a companion to this page. Treat the numbered cell labels as **occurrence ordinals**, not carrier angles or cryptographic key values. The glyph marks remain upright as reading labels; the operation rotates array addresses and does not invent internal UCNS orientation transport.

## The arrangement and its invariant

For an 8 × 8 array `A`, with zero-based row and column coordinates, clockwise rotation is:

```text
B[c, 7-r] = A[r, c]
```

The exact same occurrence wrapper and native participant move together. The highlighted top row becomes the rightmost column. Occurrence #2, carrying Ω, moves from `(0,2)` to `(2,7)`. Four applications recover all original addresses and object references.

The rendering fixture uses the explicitly declared ordered carrier `('A', 'é', 'Ω', 'Ж', 'λ', 'π', 'ß', '→')`. Each row repeats those eight participants, with occurrence ordinals `8*r+c`. This is an illustrative fixture, not a frequency sample of natural language or the canonical 157-position Public Gonol. Equal glyph identities in different rows retain distinct occurrence ordinals. The native participants in this fixture are primitives; the diagram's retained-interior rule is not a new test of closed recursive interiors.

## Exact counts

With eight positions on every axis, a complete `d`-axis array has:

- `8**d` occupied positions, counting occurrences, not distinct glyph identities;
- `d * 8**(d-1)` distinct axis-aligned 8-cell lines;
- `choose(d,2) * 8**(d-2)` distinct axis-aligned 8 × 8 slices.

For a line, choose its varying axis and fix all other coordinates. For a slice, choose its two varying axes and fix the rest. Each physical line or plane is counted once. Diagonals and arbitrary oblique slices are outside these counts.

| Axes | Glyph occurrences | 8-cell axis lines | 8 × 8 slices |
|---:|---:|---:|---:|
| 2 | 64 | 16 | 1 |
| 3 | 512 | 192 | 24 |
| 4 | 4,096 | 2,048 | 384 |
| 5 | 32,768 | 20,480 | 5,120 |
| 6 | 262,144 | 196,608 | 61,440 |
| 7 | 2,097,152 | 1,835,008 | 688,128 |
| 8 | 16,777,216 | 16,777,216 | 7,340,032 |

These are mathematical counts for the declared arrangement. They do not report that 16,777,216 native glyph objects were instantiated or that eight-dimensional UCNS closure was verified.

## Preserve the column information

The cube example uses `P=(x=2,y=5,z=3)`:

| View | Fixed coordinate | Row coordinate | Column coordinate | Position of P |
|---|---|---|---|---|
| x–y plane | z=3 | y | x | row 5, column 2 |
| x–z plane | y=5 | z | x | row 3, column 2 |
| y–z plane | x=2 | z | y | row 3, column 5 |

Every slice needs its varying-axis pair and all fixed coordinates. A row/column number alone is insufficient. In this example the highlighted columns of the second and third views are two views of the **same z-directed physical line**; they must not be added as separate lines. The exact line-count formula already removes that double-counting.

The drawing establishes a coordinate view, not a universal selection, sequencing or deletion rule. The earlier FF/00 operation applies to declared binary interiors. A test for repeated whole glyphs or a shared structural feature needs its own explicitly named predicate. No conversion from one predicate to another is assumed.

## Source and authority

| Source | Exact revision | Role |
|---|---|---|
| [UCNS](https://github.com/The-Interdependency/ucns/tree/3f97f5292b0bd2dab911540062ccf79dea2be1bf) | `3f97f5292b0bd2dab911540062ccf79dea2be1bf` | Native `Carrier` and `Participant` producer |
| [Stack](https://github.com/The-Interdependency/stack/tree/37e493d194651ca45c7bc3fbd6327f653df6879e) | `37e493d194651ca45c7bc3fbd6327f653df6879e` | Existing Weave workspace and publication base |
| [skill-lib](https://github.com/The-Interdependency/skill-lib/tree/6a16302f0b7ad6e2ed5331ee1423fcc0939e1d57) | `6a16302f0b7ad6e2ed5331ee1423fcc0939e1d57` | Source-preservation and information-design discipline |

The producer is [`src/ucns/ordinal_affixiation.py`](https://github.com/The-Interdependency/ucns/blob/3f97f5292b0bd2dab911540062ccf79dea2be1bf/src/ucns/ordinal_affixiation.py), Git blob `9fa84ef20f19fe0c04df680f49b50ea307e6d624`. The renderer refuses any other source bytes. UCNS retains construction authority; this Stack document owns its illustration and observed check only. Current [UCNS canon](https://github.com/The-Interdependency/ucns/blob/3f97f5292b0bd2dab911540062ccf79dea2be1bf/CANON.md) and [attachment contract](https://github.com/The-Interdependency/ucns/blob/3f97f5292b0bd2dab911540062ccf79dea2be1bf/docs/ATTACHMENT_STACK.md) remain authoritative for their own geometry and unresolved boundaries.

## Reproduce

Use Python 3.12+ with Matplotlib and Pillow. From the Stack root, supply the exact producer source obtained from the UCNS revision above:

```bash
python research/weave/docs/glyph-axis-infographic/render.py \
  --ucns-source /checkouts/ucns/src/ucns/ordinal_affixiation.py \
  --output /tmp/glyph-axis-replay
```

The script verifies the producer's Git blob, constructs the eight native participants, checks all 64 moves and four-turn identity, derives the full 2–8 axis table, then exports the figure and evidence. It does not fetch sources, modify UCNS or execute a cipher. `--output` writes the named exports in that directory; select a new directory when retaining an earlier run. Rendering versions are recorded because export bytes can depend on Matplotlib and fonts. Geometry/count checks are exact and independent of display rounding.

The figure labels supply color-independent distinctions: BEFORE/AFTER, coordinate ordinals, occurrence #2, P, and all axis/fixed-coordinate labels. The publication review includes text contrast, grayscale, color-vision-deficiency simulation and a semantic check. Automated contrast is a rendering check, not a claim of universal perceptual accessibility.

## hmmm

The exact whole-glyph matching/deletion predicate, retained-interior bit predicate, and higher-axis native closure remain separately scoped research. This figure supplies an inspectable arrangement and its addresses; it makes no Unicode-wide frequency or cryptographic-hardness claim.
