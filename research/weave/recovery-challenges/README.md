# Weave recovery challenges

GPT generated; context, prompt Erin Spencer.

This directory contains actual, unmodified outputs from the implemented Weave
native sequence-cycle candidate. Give another model this directory and the
public source links below. Keep the evaluator's answer/material bundle separate.

## Start here

The first frozen challenge is [v1/manifest.json](v1/manifest.json):
eight binary `.wvc` files in [v1/ciphertexts/](v1/ciphertexts/).

- **a01–a04:** the exact published sample profile is known; the actual corpus is withheld.
- **b01–b04:** the corpus and selected supported profile values are withheld.
  The manifest states exactly which fields vary and their sampling rules.
- A group shares its own corpus and profile. Messages differ within and between groups.
- The plaintexts are fresh synthetic prose, JSON, repeated blocks and binary data.
  No personal documents or existing public demo plaintexts were used.
- All eight files were recovered exactly by separate authorized receiver processes.
  No public-only recovery trial has yet been run against this pack.

Run from `v1/` to verify download integrity:

```sh
sha256sum -c SHA256SUMS
```

The checksums identify public ciphertext and manifest bytes. They do not expose
plaintext hashes. Native wire metadata, hashes and any implementation leakage
are retained exactly as emitted; nothing was stripped or repaired.

## Prompt for the recovery model

> Attempt to recover the original bytes from the files in
> `research/weave/recovery-challenges/v1/ciphertexts/`.
> Read `v1/manifest.json` first and record precisely what public inputs you used.
> You may inspect all public algorithm source/history, implement alternative
> decoders, derive withheld parameters, compare ciphertexts and generate your own
> local examples. You are not supplied the victim's corpus, withheld profile
> values, original messages, generation trace, evaluator bundle, or an encryption/
> decryption oracle. Do not request or inspect those private materials.
> Return `<case-id>.recovered` containing exact proposed plaintext bytes, plus a
> report explaining your method, commands, resources, assumptions, recovered
> parameters and any unresolved bytes. Distinguish exact recovery, partial
> recovery, and an unsuccessful attempt. An unsuccessful attempt is not a proof
> of security. Avoid changing a target file or treating an API refusal as proof
> that plaintext cannot be recovered by a different method.

Use a fresh model context supplied only this public directory/source. If its tools
can access the evaluator's files or the generating conversation, the operator must
remove that access; these instructions are not an OS or account isolation mechanism.

## Exact algorithm and source

Stack source:
[`9de81c67b271df09c1d9ba5422660c96fe8af7ac`](https://github.com/The-Interdependency/stack/tree/9de81c67b271df09c1d9ba5422660c96fe8af7ac/research/weave).

Read [SPECIFICATION.md](https://github.com/The-Interdependency/stack/blob/9de81c67b271df09c1d9ba5422660c96fe8af7ac/research/weave/SPECIFICATION.md),
[CYCLE.md](https://github.com/The-Interdependency/stack/blob/9de81c67b271df09c1d9ba5422660c96fe8af7ac/research/weave/CYCLE.md),
and the source files pinned individually in the manifest.
UCNS geometry is consumed at
[`905e66964a495d7596a577bb64e4158db9465864`](https://github.com/The-Interdependency/ucns/tree/905e66964a495d7596a577bb64e4158db9465864);
`CYCLE_NATIVE.json` specifies the two exact modules.
The source commit's `research/weave/CYCLE_WORK_GRAPH.json` records the existing
cross-repository ownership and non-transfer boundaries.

The existing sequence cycle performs actual corpus normalization, repeated
multi-byte sequence discovery/affixiation, eight/whole-plus-seven native circle
representation, numeral serialization, prime-route section scheduling and three
rounds of first/last interleaving. Group B changes only supported profile values;
the algorithm source and wire format are unchanged.

The sample profile in the public repository is **not** claimed secret in group A.
Group B's unchanged fields are likewise public. A private parameter that can be
derived from these public inputs remains fair game; the recovery model must show
that derivation.

## Exposure and evaluation

The manifest is the complete intended additional disclosure. Everything already
present in a ciphertext or the public repository is also available to the attacker.
No answer, receiver corpus, selected private profile, salt, intermediate trace or
private receipt is checked into this directory, an adjacent repository directory,
or this change's Git history.

Submit original-length, byte-exact messages, including any zero bytes or trailing
newlines, as binary files. The owner evaluates them against separately retained
answers. Submit a frozen attempt before requesting feedback; the pack offers no
live confirmation oracle.

A salted SHA-256 commitment in the manifest fixes the evaluator receipt before
attempts. Its 32-byte salt stays private, so it is not an additional public
plaintext-guess checker. The owner can reveal the salt and receipt after evaluation
if desired. Ciphertext-native checks remain visible.

## Attempt coverage and limits

This pack tests the **implemented native sequence-cycle candidate** under two
explicit disclosure settings. It is not a claimed implementation of the unresolved
public-key/private-key binding, private gonol, secret-base projection, authentication,
or replay mechanisms. No success or failure transfers to those missing mechanisms
or to the full intended Weave system.

The existing `twin_ray_engine.py` attempt is excluded from active recovery cases:
its declared `public_face` exports the same residue carrier for every message,
while its decoder needs additional message-bearing record fields. Withholding
those fields would not give a demonstrated legitimate recovery path from the
published file; publishing its internal record as public ciphertext would silently
change that interface. The source is unchanged and the exclusion is recorded.

This is a ciphertext-only challenge. Known/chosen plaintext, victim oracles,
tampering, replay and compromise experiments need separately declared inputs and
should be added as new versions without changing v1.

## Maintenance and hmmm

Keep v1 bytes immutable. Add new attempts or changed exposure policies in a new
version and verify authorized recovery before publication. Rollback removes only
this challenge directory; it changes no cipher source or authority.

hmmm: independent recovery is pending. Exact authorized round trips establish
that these files have recoverable answers; they do not establish secrecy,
asymmetry, authentication or cryptographic strength.
