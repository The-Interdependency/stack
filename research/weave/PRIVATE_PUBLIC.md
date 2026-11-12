# Native-shift polynomial candidate v1

This replaces the earlier input-partition-only experiment, which did not fulfill
the construction task. Scope: a new, explicitly proposed public/private binding
after the merged native Weave cycle. The candidate may fail; no result transfers
to intended Weave as a whole.

## Defined relation (frozen before execution)

Generate 256 private material bytes. Construct their actual Stack `ByteOrigin`
using the unchanged, source-locked UCNS geometry. For circle i=0..7, select native
byte axis `material[i]` and complete frame `material[8+i] & 1`. Its complete turn
`t_i` includes the 360/720 distinction. Define integer displacement
`a_i = 1 + 256*t_i`, in 1..512. These are explicit candidate choices, not UCNS laws.

The private eight-circle candidate consists of that source-bearing origin and
its eight native axes/states. It is Stack research, not a claim to have completed
UCNS's general higher-dimensional gonol construction. All eight states affect the
binding; six are withheld as individual geometric records.
This key-origin is separate from the cycle's retained message-origin; it does not
replace message identity or its sequential byte-occurrence axes.

For the six hidden displacements:

    F_0(x) = x
    F_j(x) = (F_(j-1)(x) + a_(j+1))^2,  j=1..6

Publish the 65 exact integer coefficients of degree-64 `F_6`, the whole-circle
state 0 and occurrence-circle state 1, origin identity, corpus, existing cycle
profile and native-source identity. The coefficient payload is explicitly counted
as additional public evaluation information attached to the public view. It must
be attacked; calling a record “whole-plus-one” does not hide its disclosures.

Sender: run the real merged sequence cycle, interpret its exact length-bearing
record as integer x, and emit `y = F_6(x+a_0)+a_1`, plus key identity and record
length. The sender has only public artifacts, message and code.

Recipient: rebuild the private native states from private material; check the
public/private binding; subtract a_1; repeatedly take an **exact** nonnegative
integer square root and subtract a_7 through a_2; subtract a_0; restore exactly
the recorded byte length; run the unchanged cycle inverse. No plaintext copy,
encoder trace or sender callback is available to recovery.

This is scalar algebra on an exact integer representation of an already-native
cycle record. It does not redefine UCNS geometry, replace sequence/occurrence
construction, reintroduce per-bit circles, alter prime routes, or import a
conventional cryptosystem. It is an explicit candidate for the previously missing
binding relation, not a ratified answer to Q2/Q7/Q12.

## Falsification criterion and attack

Required: public-only sending, exact private recovery, and failure of attempted
public-only recovery. Wrong/missing private input must be rejected by the private
API, but that refusal never establishes private necessity.

Preregistered attack: coefficient decomposition. For degree d, coefficient
`[x^(d-1)]F = d*a_2` reveals the first hidden displacement. Substitute
`x = z-a_2`; all odd powers vanish. Replace `z^2` with a new variable and repeat
on the degree-d/2 polynomial. This peels all six displacements using **only the
public key**. Then perform exact recovery without the private material.

Prediction: this candidate is FALSIFIED by that attack. The implementation must
nevertheless demonstrate the actual public sender/private receiver composition
and produce the counterexample. A successful public attack is not recast as an
interface success or a failure of intended Weave. If decomposition instead fails,
report the failure and preserve the exact case; do not infer security.

The full private material need not be recovered: an equivalent inverse is enough
to falsify recipient-private necessity. The effective hidden inverse space is at
most 512^6 choices; the larger material origin does not confer additional inverse
entropy. The algebraic attack avoids enumerating that space.

## Artifacts, boundaries and usage

`keygen(profile, corpus, sources)` returns public and private serialized bytes.
The public artifact has two native complete turns plus all public evaluation
coefficients; the private artifact has the original private material. `send` takes
no private argument. `recover` requires private material. `public_recover` performs
the coefficient attack directly, without calling `recover` or `keygen`.

```sh
cd research/weave
python private_public.py --sources /checkouts
python private_public.py --sources /checkouts --require-distinction
WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_private_public.py -v
WEAVE_SOURCES=/checkouts python test.py --receipt /tmp/weave-check.json
```

The first command emits observed evidence. The second exits 1 on a successful
public recovery attack; malformed inputs/infrastructure errors exit 2. Regression
success does not mean the candidate survived. The demo uses explicitly disclosed
fixture material for reproducibility; ordinary keygen uses fresh system randomness.

Sender, private receiver and public attacker run as separate fresh processes in
an allowlisted source bundle, with only their declared serialized inputs. This is
an information-flow test, not an OS sandbox. All packet/key bytes are counted.
Limits: 256 plaintext bytes, at most three existing cycle rounds, a 16 KiB cycle
round budget, and six algebraic layers. Source integrity and exact-square checks
are not authentication. No network or production integration is introduced.

Resource preflight: degree-64 polynomial arithmetic, six integer square roots and
a finite existing regression suite fit the available CPU/memory/disk. Stop at the
exact construction/recovery/attack results, not an invented elapsed-time cutoff.
Rollback: remove this candidate, tests and CI links; merged-cycle code and source
pins remain unchanged. A surviving candidate would proceed to additional attacks;
a failed one remains scoped evidence and is not enabled as encryption.

Observed result: [evidence/private-public-v1.json](evidence/private-public-v1.json)
records public-only sending, exact private recovery and exact public recovery by
coefficient decomposition: **FALSIFIED for this candidate**. The demo counts
5,904 inner-cycle bytes, 377,885 packet bytes, 8,091 public-artifact bytes and 572
private-artifact bytes. No compression or fixed doubling is claimed. All 196
Weave tests passed with zero failures/errors/skips; suite source SHA-256
`b43b7329099175e54d0ac2eb7a6850bbe870e7ddd898027243fb6e6fa609a0f3`.
The three-process test also runs with fresh system-random private material.

Domain claim: `weave.research.native-shift-polynomial/v1` is a provisional Stack
scalar-binding experiment. “Private gonol” here denotes the source-bearing eight-
state candidate described above, not canonical UCNS general gonol completion or
an established cryptographic primitive. No term collision licenses either claim.
Consulted skill-lib `38c64332b840b2bbe1c07e53aeee8996644548e9` and METAPAT
`86415a5368c1a1417c2b6731f19967a6b1fce6bb`; their authority does not establish
cryptographic validity.

## hmmm

The candidate is expected to fail. A surviving native asymmetric relation,
confidentiality, authentication, replay handling and the broader private-corpus
binding remain open. Failure of this explicit algebraic candidate says nothing
about every possible private/public gonol construction.
