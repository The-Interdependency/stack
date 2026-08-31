# No External Runtime Dependencies

**Status:** PCEA runtime policy.

## Rule

PCEA runtime modules listed in `pcea.contract.RUNTIME_MODULES` depend on nothing outside the Python standard library and other explicitly approved The Interdependency runtime components.

**Allowed at runtime:**
- Python standard library, including `hashlib`, `hmac`, `secrets`, and `os.urandom` where required.
- Other The Interdependency repositories only when the PCEA runtime contract explicitly admits them.
- Static test vectors shipped as repository data.

**Not allowed at runtime without an explicit contract change:**
- `cryptography`, PyNaCl, libsodium, OpenSSL wrapper packages, Signal-protocol packages, or external services required to encrypt/decrypt.

Build/test tooling such as `pytest` is not a runtime dependency.

## UCNS and research boundary

PCEA's current runtime does not rely on UCNS inversion, catalogue, factor-search, or research APIs. UCNS-assisted cryptographic and gonol/state experiments are mutating research and live in `The-Interdependency/stack/research/pcea/`.

The historical source-tree proving ground was removed from PCEA after migration. `pcea-ucns/README.md` remains only to redirect old links; it is not runtime code or an active research location.

## Exit gate

- `pyproject.toml` declares no runtime package dependencies.
- The runtime package remains importable without UCNS or external cryptography packages.
- `tests/test_contract_spec.py` verifies that the runtime does not import or call forbidden UCNS inverse/catalogue symbols.
- README states the dependency and research boundaries accurately.

## hmmm

Zero external dependencies is an implementation constraint, not evidence that a cryptographic construction is safe. Independent cryptographic review remains a separate requirement.
