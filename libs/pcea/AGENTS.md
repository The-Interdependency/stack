# PCEA agent guide

PCEA is the stable pure-Python symmetric state-transform repository. Mutating PCEA research belongs in `The-Interdependency/stack/research/pcea/`, not here.

## Authority

- PCEA decrypts/inverts through synchronized keys, not UCNS inverse operations.
- Runtime state is seed/circle/tensor addressed and depends on protected `last_state` synchronization.
- This repository owns completed PCEA runtime behavior, package metadata, runtime tests, and release boundaries.
- Stack research does not gain PCEA authority and does not transfer proof, measurement, or security standing back here.

## Boundaries

- Load relevant repo-local skills from `.agents/skills/` before changing behavior, metadata, tests, or cryptographic claims.
- Do not add experiments, candidate KEMs, attack notebooks/harnesses, speculative gonol key schedules, or open research lanes here. Put them in `The-Interdependency/stack/research/pcea/`.
- Do not claim cryptographic security from passing tests or external research harnesses alone.
- Do not couple runtime correctness to UCNS analytic-frontier assumptions.
- New behavior-bearing runtime modules require skill-lib metadata and tests exercising the declared contract.
- `pcea-ucns/README.md` is a migration tombstone only; do not rebuild a proving ground beneath it.

## Checks

```bash
python -m pytest -q
python -m pytest -q tests/test_cipher.py tests/test_codec.py tests/test_kdf.py tests/test_instance.py tests/test_contract_spec.py
```

## Promotion rule

Research may enter PCEA only after its mutable investigation is complete enough to state a bounded behavior and falsifiable contract. Promote the smallest completed behavior; preserve unfinished constraints as `hmmm` in stack rather than importing them as runtime assumptions.

## hmmm

- Independent cryptographic/security review remains distinct from repository correctness tests.
- The stack `libs/pcea` pinned view may lag this source until its separate fresh-making refresh completes; do not infer source freshness from that imported snapshot.
