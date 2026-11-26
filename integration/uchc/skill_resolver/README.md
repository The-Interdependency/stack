# UCHC skill resolution pilot

AHBG can use UCHC as the working representation of a skill catalog. A session names its task roots, visible skills and runner grants. The planner receives discovery descriptions and exact instructions for the activated closure. Each selected skill appears once with every direct reason for its inclusion.

## What owns each decision

The skill-lib revision in [source.json](source.json) owns names, descriptions, instructions and directed relations. The loader verifies the index and each instruction file against that Git tree. Source bytes remain available by path and digest. The control resolves typed records directly. The UCHC arm constructs named fields, typed relations and ordered occurrences as nested operands using the released ordinal-halving producer. It reads each skill back from its verified native construction for traversal. A completed activation contains the closed skill interiors, the pinned source identity, the task roots, the order and the reasons. On replay, the resolver checks these against the caller’s requested roots and the trusted catalog.

A prerequisite has to be available before its dependent. A directed `load_with` brings the target into the same activation. Either participant can be requested independently according to its own declarations. All admitted co-loads reach the planner together in one view. Only hard-prerequisite cycles invalidate a plan. Missing, retired or conflicting skill identities cause refusal. Relations that appear solely as free text still require a source-owner declaration to participate in resolution. Task selection in this pilot is explicit.

The operator defines the discovery scope and grants disclosure of exact source-declared runner paths. Discovery withholds descriptions that contain an ungranted path. If a required instruction contains one, activation fails before the agent receives it. Full activations preserve the original instructions. The policy covers the catalog's explicit runner identifiers. It provides no confidentiality guarantee for paraphrases or independently available public files. Tool execution remains under the host's existing permissions.

## Run a session

Use Python 3.12 from Stack with the [hash-pinned UCHC wheel](../halving-requirements.txt) installed. Supply the UCNS checkout named in [source.json](source.json) and the exact skill-lib checkout named there. The existing [release workflow](../../../.github/workflows/uchc-halving.yml) installs these and runs the complete acceptance.

```bash
export AHBG_SKILL_CATALOG=/path/to/pinned/skill-lib
export AHBG_SKILL_UCNS_SOURCE=/path/to/pinned/ucns
export UCHC_HALVING_UCNS_ROOT="$AHBG_SKILL_UCNS_SOURCE"
export PYTHONPATH=.:libs/ucns/src
python -m ahbg.runtime play --turns 1 --out /tmp/skill-pilot \
  --skill-catalog "$AHBG_SKILL_CATALOG" --skill-ucns-source "$AHBG_SKILL_UCNS_SOURCE" \
  --visible-skills distributed-publication interdependent-work-graph typed-meta-frontend meta-module-build doc-build msdmd \
  --activate-skills distributed-publication typed-meta-frontend \
  --disclose-runner msdmd=msdmd/collect.py
```

Use `--skill-experiment control` and a separate output directory for the graph arm. Omitting activation yields a discovery view. The native turn receipt in `result.json` identifies a packet in `skill-activations/<activation_root>.json`. An independent reader can pass the decoded packet and the expected task roots to `SkillResolver.replay_activation` to verify the decision. The packet stays in the host's output directory. The planner receives the scoped view.

## Reproduce the evidence

```bash
python -m unittest discover -s integration/uchc/skill_resolver -p 'test_*.py'
python -m unittest discover -s ahbg/integration/tests -p '*skill*.py'
python -m integration.uchc.skill_resolver.acceptance "$AHBG_SKILL_CATALOG" "$AHBG_SKILL_UCNS_SOURCE"
```

The installed harness test sends both task roots to an external JSON-lines planner. That process checks the six instruction bodies, both relation types and the runner grant, then returns the hash of the view it actually received. A third session with the runner withheld must fail before planning. Structural tests distinguish groupings with equal additive vectors and refuse a natively valid packet whose reasons contradict its source. The [comparison receipt](comparison.json) records separate single-root decisions and a controlled revision of one shared prerequisite.

| Task root | Active skills | Planner view, both arms | Graph record | UCHC record |
|---|---:|---:|---:|---:|
| distributed-publication | 2 | 33,438 bytes | 2,177 bytes | 95,142 bytes |
| typed-meta-frontend | 4 | 53,011 bytes | 3,272 bytes | 136,442 bytes |

Sizes use compact UTF-8 JSON for each representation. The typed graph and UCHC arms use the same decision policy and source facts. The fixed-lock revision probe changes the body digest in memory, checks both representations’ affected roots, and verifies rejection against the original source. A real global pin change can also change activation identities.

**hmmm** — Both cases delivered identical planner views. The geometric records cost more bytes in both. A benefit for larger catalogs or repeated partial replay remains unmeasured.
