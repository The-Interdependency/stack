# METAPAT → UCNS Phi fork policy

## Purpose

METAPAT owns the semantic decision that several children are simultaneous constitutive components of one parent. UCNS owns the payload geometry. EDCM or another integration repository must verify that the authorization still matches the encoded object.

The default mapping remains `external-provenance`. A UCNS payload fork acquires METAPAT constitutive meaning only through an explicit, canon-bound `UCNSForkAuthorization`.

No UCNS theorem or domain status is transferred into METAPAT validity or EDCM measurement validity by this policy.

## Create an authorization

```python
import metapat

parent = metapat.root_spine_module_envelope()
authorization = metapat.authorize_constitutive_fork(
    parent,
    child_module_ids=(
        "metapat.child.alpha",
        "metapat.child.beta",
    ),
    source_statement_refs=(parent.source_statement_refs[0],),
    unresolved_constraints=(
        "hmmm: downstream integration must bind child ids to exact payload hashes",
    ),
)

wire_record = authorization.to_json()
```

The child order is identity-bearing. Reversing the children is not the same authorization.

## Required relation

The only authorized relation kind is:

```text
constitutive-simultaneous
```

The policy refuses to silently reinterpret any of these as payload containment:

```text
temporal-successor
adjacency
provenance
alternative
fiq-connectivity
external-symmetry-action
arbitrary-association
```

Those relations remain on their own external surfaces.

## Record contract

`UCNSForkAuthorization` carries:

```text
schema id and version
parent module id
ordered child module ids
relation kind
exact source statement references
encoding-policy version
METAPAT canon digest
unresolved constraints
theorem_status_transfer = false
metapat_validity_claim = false
authorization digest
```

The authorization digest is SHA-256 over canonical JSON of every field except the digest itself. Unknown, missing, coerced, reordered, or tampered fields fail closed.

## Validate against current authority

```python
validated = metapat.validate_fork_authorization(
    authorization,
    envelope=parent,
    child_module_ids=(
        "metapat.child.alpha",
        "metapat.child.beta",
    ),
)
```

Validation requires exact parent identity, child order, canon digest, source references, policy version, and relation kind.

## Downstream integration rule

This producer record is necessary but not sufficient for accepting an encoded fixture. The integration layer must additionally bind:

```text
exact UCNS parent object identity
payload-bearing cell or path
ordered child module ids
ordered actual child UCNS stable hashes
METAPAT authorization digest
encoding-policy version
```

A missing declaration, child-order drift, object-hash drift, canon drift, external-edge-as-containment substitution, or unresolved semantic default must invalidate the fixture rather than produce a warning.

## Limits

- This policy does not alter METAPAT canon text.
- It does not construct or multiply UCNS objects.
- It does not infer constitutive meaning from the existence of payloads.
- It does not authorize single-child provenance nesting.
- It does not validate EDCM readouts or empirical claims.

## hmmm

The first complete fixture still requires a downstream topology-binding schema and fail-closed linter over actual `ucns.UCNSObject` payload paths. The authorization record intentionally does not pretend that semantic child ids can be recovered from geometry alone.
