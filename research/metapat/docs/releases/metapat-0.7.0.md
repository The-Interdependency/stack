# METAPAT 0.7.0 — canon v2 rotation

## Identity

This release rotates the canon-bearing tensor clarification and Seventh Postulate through every dependent identity:

```text
package: 0.7.0
canon: metapat-canon-v2
canon digest: fd177e4f3d545005048d6352fbf6753a2f06e471231edd5fa8030b8bd1a1b14a
canon manifest digest: 8f6a4b6b961a47d823166a42a3111cb2c336143d1e1371f33c79ff3012765a83
root-spine envelope provenance: 5c8185f7bf26e6a7680ff613ef0df3544675dc6ca8ff4604e86a525562ec462f
catalog: metapat-semantic-catalog-v2
catalog digest: e2030c2758e56854736e606b81c6a7c8cc98c46dca081ffc1fdbaef2e10e4a37
quantum-magnetism application: quantum-magnetism-application-v2
quantum-magnetism digest: 70e77845f613d348202b6f3f62e845af1b6ce6d7e5fea9e8967b1457a5c013cc
electromagnetic-pipe application: three-phase-electromagnetic-pipe-application-v2
electromagnetic-pipe application digest: 025df951a6b70da1199cb8d55530a6f6b1d3c1ef18155a96cc472d6fabe13623
electromagnetic-pipe design digest: 4dc5b19b66ff684337fb7ba481276aae10e99124df5b87f79c08102ce73cb969
```

The Fourth Axiom root statement remains exactly:

```text
Tensor is primitive.
```

The new prose explains simultaneity, nesting, recursion, and possible domain representations. It remains subordinate to the root. Mathematical, physical, computational, linguistic, chess, and other tools may explicate or represent the tensor; they do not redefine the METAPAT root.

## Consumer migration

Consumers must:

1. reject records pinned to `metapat-canon-v1` when v2 is required;
2. bind the exact v2 canon digest, envelope provenance digest, catalog version and digest, application version and digest, and any consumer-local policy identity;
3. mint a new consumer-local epoch rather than silently rebinding an old epoch;
4. preserve separate METAPAT semantic, UCNS geometry/proof, and EDCM measurement authority.

METAPAT declares the rotation and required bindings. UCNS, EDCM, and other consumers own their local epoch names and migrations.

## Current generated fixtures

```text
metapat/fixtures/root-spine-envelope-v2.json
metapat/fixtures/semantic-module-catalog-v2.json
metapat/fixtures/quantum-magnetism-application-v2.json
metapat/fixtures/three-phase-electromagnetic-pipe-v2.json
```

Regenerate and verify them with:

```bash
python tools/generate_catalog.py
python tools/generate_application_fixtures.py
python tools/generate_catalog.py --check
python tools/generate_application_fixtures.py --check
```

The v1 generated fixtures are removed from the current package surface; their identities remain recoverable from the `0.6.0` source epoch.

## hmmm

The exact names and rollout timing of downstream UCNS and EDCM consumer-local epochs remain owned by those repositories. Silence is not migration.
