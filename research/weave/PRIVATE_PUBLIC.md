# Private/public recovery experiment v1

Scope: the merged sequence cycle at Stack
`ccf707f933a9611d7b7fe13a0417378d8b453a14`. This experiment tests whether splitting
its existing reconstruction inputs establishes the requested distinction. It does
not invent the still-undefined native public-evaluation/private-recovery law.

## Frozen acceptance criteria

1. The sender receives message bytes, public artifact, public corpus and locked
   source code only. No recipient-private artifact, callback or encoder trace.
2. A separate recipient recovers every byte using the transmitted record and
   recipient-private artifact, without the original plaintext.
3. Attempt public-only recovery with the same disclosed inputs. An exact public
   recovery is a counterexample to private-state necessity. An API refusing a
   missing argument is not evidence of mathematical necessity.
4. Keep the intended whole-plus-one exposure and private-gonol relation explicit.
   Publishing extra reconstruction data is a control, not satisfaction of Q2/Q12.

All four are required. This experiment can return **BLOCKED** or **FALSIFIED**;
it cannot establish cryptographic security. Passing regression tests establish
that the experiment reports these outcomes honestly, not that asymmetry works.

## Artifacts and the tested relation

`partition()` accepts an existing exact cycle profile and actual corpus. It is an
input partitioner, **not asymmetric key generation**.

| Artifact | Contents | Available to sender |
|---|---|---|
| Public, whole-plus-one | All non-space profile fields; whole-circle space 0 and one selected occurrence-circle space in each round; actual corpus bytes; native-source-lock identity | Yes |
| Private, reconstruction input | Full eight-space cycle profile and the public-artifact digest | No |
| Public, full-profile control | Full profile, corpus and native-source-lock identity; explicitly labeled as an overdisclosed control | Control only |
| Packet | Unmodified `cycle.forward` record, with all native occurrences, numeral definitions, framing and prime-derived interleaving | Yes |

The six undisclosed spaces per round are JSON `null`, never guessed as zero and
never silently retrieved from a profile file. The private artifact is an existing
native-cycle configuration. It is **not claimed to be the missing private gonol**.
The selected public occurrence circle is an explicit experimental parameter;
circle 1 is the default, not a new universal placement law.

The fixed cycle forward and reverse both require a complete `Profile`. Therefore:

- Whole-plus-one projection: the sender has no defined way to compute the six
  missing spaces or an alternative public operation. The experiment must report
  **BLOCKED: native public evaluation law missing** before invoking the cycle.
- Full-profile control: the sender operates in a fresh process with only public
  inputs; the recipient's private-path decoder recovers exactly. A separate
  public-only process also runs the existing inverse and recovers exactly.
  Private-state necessity is **FALSIFIED for this control**.

Neither observation falsifies the intended Weave cryptosystem. No earlier
per-bit/star encoder or attack is restored. Prime routes remain public
deterministic schedule derivations, not a trapdoor. The actual native UCNS
geometry, complete 720-degree state, seven occurrence streams, corpus bits and
merged wire format remain unchanged.

## Plan, boundaries and stopping rule

Decision: can input partitioning alone close Q7 while retaining Q2/Q12?
Minimal action: run the two disclosed cases above on the real merged cycle.
Maximal closure would require a specified native private-gonol constructor,
public projection/evaluation law and private inverse, followed by adversarial
recovery work. That mathematical construction is not supplied by this patch.

Positive outcome for a future law: public sender and private exact recovery
work, and the named public attack fails; continue to broader attacks, keeping the
result bounded to the tested attack. Negative: preserve the exact public recovery
counterexample and reject that candidate. Unresolved prerequisite: report BLOCKED,
identify the missing operation, and do not infer a design-wide impossibility.

Resource preflight: one small message through the existing profile and a finite
set of fresh-process calls; standard library only, no search or network in the
experiment. Existing suite includes finite enumerations and a 65,536-byte cycle
case. Available local CPU, memory and disk suffice; no artificial timeout is used.
Stop when both controls and the regression suite finish.

Code/runtime source files are copied by an explicit allowlist into a fresh
temporary directory. Child processes use a clean environment and `-S -B -E`.
The sender and attacker receive no private bytes; receiver receives no plaintext.
The input manifest and source hashes are recorded. This checks data flow, not
an OS sandbox or resistance to arbitrary hostile Python code. No network,
authentication, private storage service or production integration is added.

Rollout: explicit experiment CLI and existing Weave research CI only. Rollback:
remove `private_public.py`, its tests and documentation/CI links. No source pins,
authority, geometry, prime-route logic or existing cycle format change.

## Usage

From `research/weave`, with the locked UCNS checkout at `/checkouts/ucns`:

```sh
python private_public.py --sources /checkouts
python private_public.py --sources /checkouts --require-distinction
WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_private_public.py -v
WEAVE_SOURCES=/checkouts python test.py --receipt /tmp/weave-check.json
```

The first command emits a source-bound JSON report and exits zero when the
experiment executes. The second emits the same report and exits **1** because
the requested distinction is not established. Infrastructure/admission errors
exit **2**, separately from a scientific counterexample. The demo uses disclosed
test data, not user secrets. Reports contain no private artifact or plaintext.

Programmatic use: `public, private = partition(profile, corpus, circle=1)`;
`send(message, public, sources)` refuses the unresolved projection;
`recover(packet, public, private, sources)` uses the admitted private profile.
`full_profile_control(public, private)` explicitly constructs the overdisclosed
control; `public_recover(packet, control, sources)` supplies the real counterexample.

Observed execution is retained in [evidence/private-public-v1.json](evidence/private-public-v1.json)
with source hashes and full artifact byte counts. The complete Weave suite passed
196 tests (176 existing and 20 new), with zero failures, errors or skips; source
snapshot SHA-256 `1d71264a9e61b76289a77deb301f0f1916b67fcfb7920207bae01937aa87d0cb`.
The separate distinction gate exited 1 as specified. This is evidence of a working
experiment with an unclosed result, not an asymmetric implementation.

Governance consulted: skill-lib `38c64332b840b2bbe1c07e53aeee8996644548e9`
(`the-interdependency`, `action-calibration`, `meta-module-build`, `msdmd`,
`test-build`, `ratios`); METAPAT `86415a5368c1a1417c2b6731f19967a6b1fce6bb`
axioms, postulates and domain restraint. Semantic/geometry resemblance does not
transfer cryptographic evidence. This is consultation provenance, not a runtime
dependency or change to Stack's pinned authorities.

## hmmm

The missing construction is an explicit `PublicEval(public, message, sender_state)`
and `PrivateRecover(private_gonol, packet)` relation whose sender needs no hidden
recipient inputs and whose public description does not simply supply the existing
inverse. The current experiment exposes that boundary; it does not close it.
Computational recovery advantage, randomness, authentication and replay remain open.
