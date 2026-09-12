# Composed successor constructor v0

Status: FALSIFIED stack-local successor experiment, not UCNS canon.

Actor lane: A.

## Purpose

This pass resumes the successor experiment only after freezing the three
executable UCNS research mechanics:

```text
Public Gonol functional operations
affinization/coupling geometry
recursive-scale transition
```

The constructor is the smallest composition of those declared operations. It
does not add fitted constants, numerical recurrence terms, target-specific
branches, or interpolation-control logic.

## Frozen Mechanics

The mechanics were frozen before successor gate execution:

| Mechanic | Code sha256 | Receipt sha256 |
|---|---|---|
| `mechanic_1_public_gonol_functional_operations` | `bf81a18b9074ce10232e73afa42d23690f4172c9b60b0284a986abbf5738a1d3` | `351d91a1d27f9b29b4222325df0a359682c9c8dd0903fdfef8d4f73c13074194` |
| `mechanic_2_affinization_coupling_geometry` | `65c5bbee87fa1a5cb9119c19a8e186b62827e55a91b17c4111aa06b8df0ce21a` | `a59d291b77c0110ffc0c401dcc94d25ad63a3372c51eab26989a5b6acf9ff68d` |
| `mechanic_3_recursive_scale_transition` | `882b2defbc88c686011a3c66d1e7d080adc9623b219a91a4253c0378b69292f1` | `3297ced3efb9c127a01337d479ce8382b771ea9d2ab66faa7e79a0ec2a197496` |

Each producer code reference matched `sha256:<code_sha256>` at freeze time.

## Executable Constructor

Constructor identity:

```text
ucns.smallest-composed-successor.v0
```

For each input occurrence:

```text
1. apply Public Gonol cyclic participation
2. close one explicit ordered coupling of source and function output
3. promote the closed affinization into one recursive atomic participant
```

Then close the successor as one whole.

Layer count for input size `n`:

```text
input_participants = n
public_gonol_function_participations = n
closed_affinizations = n
recursive_atomic_participants = n
successor_closure_whole = 1
output_size = 4*n + 1
```

This count is a consequence of the frozen composition, not a fitted rule.

## Gate Result

External observation gate:

```text
157 -> 2881
2881 -> 54837698421
```

Actual constructor result:

```text
157 -> 629
```

Outcome:

```text
status = FALSIFIED
second_gate_executed = false
next_prediction_available = false
interpolation_control_comparison = not reached; first gate falsified
```

Because the first gate failed, the identical constructor was not run on the
second observation. No next prediction was produced. The interpolation control
was not compared.

## Falsification Conditions

This constructor/mechanics combination is falsified because the frozen
constructor maps the pinned starting observation to `629`, not to the external
comparator.

Do not tune this constructor toward the comparator. Any new attempt must change
mechanics only through their own executable definitions, tests, provenance, and
receipts, then run as a new frozen constructor.

## Receipt And Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/composed_successor_constructor.py 157 2881 54837698421
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_composed_successor_constructor.py
```

Frozen receipt:

```text
receipt_schema = the-interdependency.stack-research.ucns.composed-successor-constructor
receipt_version = 0.1.0
constructor_id = ucns.smallest-composed-successor.v0
producer_code_reference = sha256:05330f604f81402c3fa12e17f1c9d9c23f1510a9304b8c15631e13cf3fb3d2ce
receipt_sha256 = bc79dc748cccec6c71d658f3431a0cab5b3b0e8953e9851ce47de0a9a5cd3745
first_transition_aggregate_sha256 = 05040b86af8087aec6ec31fff73dea11ccd0eb4e7113a1d922a2e6dac632d63b
```

## Claims Supported

- The three mechanics can be frozen and composed deterministically.
- The composed constructor has executable replay evidence.
- The first observation gate falsifies this constructor/mechanics combination.
- The gate stops without tuning, second-gate execution, next-prediction
  freezing, or interpolation comparison.

## Claims Not Supported

This pass does not establish:

- UCNS canon;
- the selected gonol successor law;
- the next recursive gonol;
- PCEA runtime behavior or key research;
- cryptographic security, entropy, hardness, replay resistance, recovery, or
  public authenticity.

## hmmm

- The frozen smallest composition is not the observed successor constructor.
- The failure may sit in the operation choice, coupling geometry, recursive
  promotion, successor closure accounting, or another missing UCNS mechanic.
- The external observations remain validation data, not definition data.
- PCEA key research remains gated until UCNS yields a surviving successor
  constructor.

