# PCEA — Prime Circular Encryption Algorithm

Pure-Python, zero-runtime-dependency library implementing the stable PCEA symmetric state transform.

## Scope

PCEA encrypts pre-quantized integer neural architecture state using synchronized prior state. Runtime state is a list of seeds; each seed is a `7×7` integer array: 7 circles × 7 tensors.

For each value at `(seed_idx, circle_idx, tensor_idx)`, PCEA selects a prime base from the fixed 53-prime circle, maps the signed value into a fixed-width unsigned Möbius-disk position, encodes it in fixed-width base-`p` digits, derives key digits from synchronized previous-state contributors plus the hierarchical address, shifts modulo `p`, and reconstructs the encrypted integer.

```text
encrypt: e_j = (v_j + k_j) mod p
decrypt: v_j = (e_j - k_j) mod p
```

Fixed-width encoding prevents output digit count from exposing the plaintext magnitude class. `word_bits` must be large enough for the caller's signed range and must match between sender and receiver.

## Usage

```python
from pcea import PCEAInstance, decrypt_state, encrypt_state

seed0 = [[0 for _ in range(7)] for _ in range(7)]
last_state = [seed0]

state1 = [[circle * 10 + tensor for tensor in range(7)] for circle in range(7)]
state2 = [[100 + circle * 10 + tensor for tensor in range(7)] for circle in range(7)]

encrypted = encrypt_state([state1], last_state)
assert decrypt_state(encrypted, last_state) == [state1]

enc = PCEAInstance(seed=last_state)
dec = PCEAInstance(seed=last_state)
assert dec.decrypt(enc.encrypt([state2])) == [state2]
```

## PCEA ↔ UCNS boundary

PCEA is specified to decrypt/invert **via keys** and not through UCNS inverse operations.

- PCEA consumes forward arithmetic substrate behavior only.
- **Security rests on key management**: synchronized/protected `last_state`, approved secret generation, and correct session handling.
- A mismatch in key state must fail recovery by design.
- No claim of cryptographic hardness is inherited from UCNS geometry, factorization, gonols, or research harnesses.

`tests/test_contract_spec.py` is the release gate for this boundary; `.github/workflows/contract-boundary.yml` runs it on pull requests and pushes to `main`.

## Research boundary

Mutable PCEA research no longer lives in this repository. The former `pcea-ucns/` proving ground, its research-only tests, and research record were deprecated here and replaced by the active workspace:

```text
The-Interdependency/stack/research/pcea/
```

`pcea-ucns/README.md` remains only as a tombstone for old links. Historical research remains recoverable from Git history at `pcea@ecf2ca0dec38bef29382e02121b0edde66763aa9`; stack records the exact migration provenance and blob identities.

Completed, bounded behavior may return to this repository only through an explicit source change with its own tests and review. Research survival does not transfer security standing.

## Verification

```bash
python -m pytest -q
python -m pytest -q tests/test_cipher.py tests/test_codec.py tests/test_kdf.py tests/test_instance.py tests/test_contract_spec.py
```

## Install

```bash
pip install .
pip install ".[dev]"
```

Python `>=3.9`; runtime dependencies: none.

## License

MIT. See `LICENSE`.
