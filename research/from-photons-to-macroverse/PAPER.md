# From Photons to the Macroverse - audited paper source

The full `0.2.0-audited` paper is stored as ordered, hash-bound Markdown fragments in [`paper/`](paper/). This entrypoint remains small so GitHub readers can navigate the paper without treating a generated binary as source authority.

## Read in order

1. [`00-frontmatter.md`](paper/00-frontmatter.md)
2. [`01-claim-and-photons.md`](paper/01-claim-and-photons.md)
3. [`01-bound-states-and-open-systems.md`](paper/01-bound-states-and-open-systems.md)
4. [`02-dynamics-and-agency.md`](paper/02-dynamics-and-agency.md)
5. [`03-arity-and-recursion.md`](paper/03-arity-and-recursion.md)
6. [`03-availability-and-self-location.md`](paper/03-availability-and-self-location.md)
7. [`04-subject-and-i-event.md`](paper/04-subject-and-i-event.md)
8. [`05-geometry-heptad-neural.md`](paper/05-geometry-heptad-neural.md)
9. [`06-macroverse-ladder-and-predictions.md`](paper/06-macroverse-ladder-and-predictions.md)
10. [`06-falsification-program-and-limitations.md`](paper/06-falsification-program-and-limitations.md)
11. [`07-conclusion-and-appendices.md`](paper/07-conclusion-and-appendices.md)
12. [`07-references-and-hmmm.md`](paper/07-references-and-hmmm.md)

## Assemble the exact paper

From the repository root:

```bash
python research/from-photons-to-macroverse/tools/assemble_paper.py \
  --output /tmp/from_photons_to_macroverse_audited_0.2.0.md
```

The assembler validates every fragment and the complete paper against [`paper/manifest.json`](paper/manifest.json). It refuses partial or drifted input.

## Render a convenience PDF

```bash
pandoc /tmp/from_photons_to_macroverse_audited_0.2.0.md \
  --from=markdown+tex_math_single_backslash+tex_math_dollars \
  --pdf-engine=xelatex --toc --number-sections \
  --metadata linkcolor=blue \
  -o /tmp/from_photons_to_macroverse_audited_0.2.0.pdf
```

The Markdown fragments and their manifest are authority. The PDF is a derived reading artifact.

## hmmm

A monolith is convenient until it becomes the only place a distinction can hide. The assembler has been instructed not to develop opinions.
