# Deprecated: PCEA research moved to stack

This path is intentionally retained only as a tombstone for historical links.

The `pcea-ucns/` proving ground is no longer active in the PCEA repository. All mutating PCEA research now belongs at:

```text
The-Interdependency/stack/research/pcea/
```

The final pre-cleanup research snapshot is permanently recoverable at:

```text
The-Interdependency/pcea@ecf2ca0dec38bef29382e02121b0edde66763aa9
```

Stack records the exact migration source and Git blob identities in `research/pcea/MIGRATION.json` and can reconstruct the former 36-file research snapshot with `research/pcea/materialize_legacy.py`.

Do not add research files beneath this directory. Completed, bounded PCEA behavior belongs in the owning repository; unfinished experiments, attack harnesses, candidate key establishment, and gonol-key work belong in stack research.

## hmmm

Historical links can identify this boundary; they cannot turn deprecated research into current PCEA authority.
