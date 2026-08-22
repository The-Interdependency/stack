# Subatomic Affixiation Baseline — hydrogen → helium (provisional candidate)

- Status: **CROSS-DOMAIN-HYPOTHESIS / provisional research candidate**
- Root impact: **none**
- Owner of record: `The-Interdependency/stack` → `research/epac/` placeholder (no canonical epac
  repository exists yet — see `STACK_MANIFEST.md`)
- Canon class: **proposed** — nothing in this document is org canon. Established facts are
  cited from current METAPAT and UCNS sources and marked `implemented`; everything else is
  candidate or `hmmm`.

## 1. Domain claims (before any definition)

Per `domain-claims`, the operative senses are claimed before the construction uses them.

| Surface form | Term id | Claiming domain | Claimed sense | Scope | Type | Status |
|---|---|---|---|---|---|---|
| hydrogen | `physics.atomic.hydrogen` | physics | element with atomic number Z=1 | empirical element identity | native | ratified in physics |
| hydrogen (here) | `epac.subatomic_affixiation.hydrogen` | epac candidate | declared participant set: one proton participant on declared carrier positions | this construction only | specialized | provisional |
| helium | `physics.atomic.helium` | physics | element with atomic number Z=2 | empirical element identity | native | ratified in physics |
| helium (here) | `epac.subatomic_affixiation.helium` | epac candidate | declared participant set: two proton + two neutron participants (default instance He-4) affixiated over the Möbius parameter | this construction only | specialized | provisional |
| lithium (here) | `epac.subatomic_affixiation.lithium` | epac candidate | same construction form at Z=3 (default instance Li-7) | program target | specialized | provisional |
| carbon (here) | `epac.subatomic_affixiation.carbon` | epac candidate | same construction form at Z=6 (default instance C-12) | program target | specialized | provisional |
| affixiation | `metapat.affixiation_harmonics.affixiation` | METAPAT | identity-preserving higher-order declared relation; participants stay addressable; may integrate as object-whole at a declared native scale | cross-domain application | borrowed (unchanged) | CROSS-DOMAIN-HYPOTHESIS (per METAPAT application) |
| carrier position | `ucns.public_gonol.position` | UCNS | exact glyph identity at exact index on the 157-position Public Gonol carrier | UCNS geometry | borrowed (unchanged) | implemented |
| derivation (here) | `epac.subatomic_affixiation.derivation` | epac candidate | replay of the same declared construction form for another element | this document | specialized | provisional |

**Collision check:** physics owns the empirical senses of hydrogen/helium/lithium/carbon; the
epac senses are explicitly scoped to this construction and do not contest physics. No prior
hydrogen/helium/lithium claims exist in current metapat or ucns checkouts. Resolution: **clear**
(separate scopes, no overlap).

## 2. METAPAT consultation

- question: what relation organizes the hydrogen → helium baseline over the UCNS carrier?
- METAPAT standing: **application** — `metapat.application.affixiation_harmonics`
  (CROSS-DOMAIN-HYPOTHESIS, root impact none); not axiom, postulate, or theorem.
- relevant relation: affixiation (identity-preserving higher-order relation), time-agnostic
  recurrence and oscillation, harmonic correspondence and resonance as candidate language.
- transfers: the shared question form only —

  ```text
  addressable participants
  -> declared relation
  -> declared ordered parameter or parameters
  -> recurrent structure
  -> harmonic correspondence or non-correspondence
  -> possible native-scale integration
  -> recursively addressable whole
  ```

- does not transfer: element identity or empirical facts (physics), carrier/containment/geometry
  selection (UCNS), geometric operation of carrier positions (UCNS `hmmm`), measurement validity
  (EDCM), physical frequency or temporal periodicity.
- downstream consequence: a named, bounded epac candidate may proceed with a declared admission
  profile, the Möbius turn index as the time-agnostic ordered parameter, and explicit `hmmm` on
  every position operation.

## 3. UCNS established baseline (implemented surfaces only)

Cited from current UCNS at `1975fe70`:

- **Public Gonol carrier** (`implemented`): exactly 157 one-scalar glyph positions in fixed order;
  digest `55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5`; every glyph is a
  function position; no linguistic subclassing.
- **Structural Null origin** (`implemented`): fixed origin at carrier position `0` (glyph `" "`),
  singular, not ordinary numeric zero.
- **Native Möbius root loop** (`implemented`): quotient `(t, ε) ~ (t + n, (-1)^n ε)` with exact
  rational turns. One visible turn (t=1) returns to the same phase with the local frame reversed;
  two visible turns (t=2) restore the complete state.
- **Position operations** (`hmmm`, declared in `ucns/src/ucns/public_gonol.py` MODULE_BUILD):
  "the exact geometric operation expressed by each function position beyond its carrier identity"
  is unresolved. No construction here may invent one.

## 4. Candidate construction (named, bounded, provisional)

### 4.1 Admission profile (epac-owned candidate, instance-resolved)

- Element `E(Z, A)` is represented by `Z` proton-participant positions and `A − Z`
  neutron-participant positions on the Public Gonol carrier.
- Default isotope instances are declared per element — H-1, He-4, Li-7, C-12. Isotope choice is
  **instance-resolved**, not a law of the construction.
- Proton participants occupy the first `Z` carrier positions after the origin: positions
  `1 .. Z`. Neutron participants occupy the next `A − Z` positions: positions `Z+1 .. A`.
- Every assigned position is an **identity coordinate only**. No geometric operation is asserted
  for any position.

### 4.2 Baseline: hydrogen → helium

```text
hydrogen (H-1): participants {p0 @ position 1}
    relation: none (single participant)
    closure: participant-scale whole

helium (He-4): participants {p0 @1, p1 @2} ∪ {n0 @3, n1 @4}
    declared relation: affixiation
    ordered parameter: Möbius turn index t ∈ {0, 1, 2}   (time-agnostic)
      t=0: simultaneous tensor arrangement of participants (tensor-first)
      t=1: visible 360° return — local frame flips (distinguishable relational state)
      t=2: complete 720° return — full framed state restored
    recurrence: frame flip/restore is the recurrent structure over parameter t
    closure: affixiated helium-whole at the declared atomic native scale;
             constituents remain addressable with identity and provenance
```

The only geometry used is the established Möbius framing. The carrier positions supply identity;
they do not yet supply operations. Hydrogen and helium differ by participant set and affixiation
arity — nothing else is claimed.

### 4.3 Derivation of lithium, carbon, et al. (same construction form)

```text
lithium (Li-7): p @1,2,3 ; n @4..7    -> affixiate -> Möbius recurrence -> atomic-scale closure
carbon  (C-12): p @1..6  ; n @7..12   -> affixiate -> Möbius recurrence -> atomic-scale closure
```

Each further element is a **separate candidate instance** of the same construction form. "Derive"
in this document means **replay the same declared construction** for a different declared
participant set. It does not mean a physics derivation, a UCNS theorem, a chemical fact, or a
proof that one element emerges from another.

### 4.4 Deterministic receipt (replay contract)

For each closed element-whole, a receipt is the SHA-256 over canonical JSON of:

```text
element_id, isotope_instance, ordered proton positions, ordered neutron positions,
relation_id ("affixiation"), ordered parameter ("ucns.native-mobius-turn-index"),
t-state sequence (0 -> 1 -> 2), closure_scale ("atomic"), source_commits
```

Independent replay must reproduce the receipt byte-for-byte. A receipt establishes
reproducibility of the declared construction only — not geometry, physics, or measurement.

## 5. What this establishes — and what it does not

**Established (proposed candidate):** a source-bound, replayable baseline that binds current
METAPAT affixiation semantics to current UCNS carrier identity surfaces, using the native Möbius
turn index as the time-agnostic ordered parameter.

**Not established:** any Public Gonol position operation; any geometry between carrier positions;
any harmonic notation or resonance coupling; any physics or chemistry claim; any EDCM measurement
projection; any canon promotion in METAPAT, UCNS, or elsewhere.

## 6. Usage guidance

To replay by hand:

1. Pin sources: METAPAT `34d954a`, UCNS `1975fe7` (recorded above and in `STACK_MANIFEST.md`).
2. Read `metapat/docs/applications/affixiation-harmonics.md` for the semantic definitions used.
3. Read `ucns/src/ucns/public_gonol.py` and `ucns/src/ucns/direct_mobius.py` for the carrier and
   Möbius surfaces used.
4. Apply the admission profile in §4.1, run the construction in §4.2/§4.3, and verify the receipt
   in §4.4 against an independent replay.

To implement later (only after UCNS establishes position operations, or as a pure identity-profile
consumer):

```text
entry points: ucns.public_gonol_function(index)  # carrier identity position
              ucns.native_mobius_state(turns)    # established Möbius framing
```

Do not add local geometry, position-operation semantics, or physics status inside this candidate.

## 7. Next decisive step (action-calibration)

- decision: is the H→He affixiation baseline a usable identity-level candidate for the epac program?
- minimal decisive action: an executable H→He candidate that consumes only the two UCNS public
  surfaces above, produces the §4.4 receipt, and is independently replayed byte-identically.
- positive outcome → escalate to Li/C instances of the same constructor.
- negative outcome → the admission profile or receipt contract needs repair before any Li/C work.
- unresolved outcome → UCNS position operations remain `hmmm`; keep identity-only scope.
- frozen stop condition: receipt mismatch or any invented position operation fails the candidate.

## 8. hmmm

- The geometric operation of every Public Gonol position beyond carrier identity remains unresolved
  (UCNS-owned `hmmm`); this baseline deliberately does not fill it.
- No UCNS harmonic-resonance notation is selected (METAPAT-owned `hmmm`); phase/ratio/coupling
  fields remain candidates.
- Isotope defaults (H-1, He-4, Li-7, C-12) are instance-resolved, not canonical admission law.
- epac has no canonical source repository; this record lives in the stack placeholder and must
  migrate if `The-Interdependency/epac` is created.
- No EDCM measurement projection is declared; nothing here may become empirical validation.
- Promotion of affixiation from application terminology into METAPAT postulates/theories remains
  unresolved and is not advanced by this candidate.
