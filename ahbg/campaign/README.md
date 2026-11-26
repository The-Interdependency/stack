# Two exits

AHBG issue 122 starts at Stack `1eadf5cef1ffb5e11cb2df9bd0e5402f164dfcc4`. The first mission measures whether an addressed Builder can use an order and a center-tile observation together. Exit A is RING_1 and B is RING_5. Both are legal from RING_0. The center observation never comes from the answer key. A competing move comes from RING_2 and commits to A before the Builder chooses. The resolver owns priority. This is a one-turn fixture. Its role views and mission choices are scenario rules.

## Preregistered outcomes

Use seed 122, normal exit order A/B/HOLD, a 15-second warm decision budget and the four combinations of occupied/clear and AB/BA orders. Expected choices in occupied AB/BA then clear AB/BA order are A, B, B, A. Retain the exact free-generation response. Only a complete menu label counts. Invalid responses, timeouts and explicit HOLD have distinct standing. Rotation of the menu, an irrelevant change of recipient, report withholding, and a committed competing move are separate interventions. A switch is a win only if both endpoints are correct. Four sibling arms form one fixed mission, with no population accuracy claim. Model settings are greedy CPU inference with eight generated tokens, local weights, two threads and one resident model at a time. Budget 3 GiB additional disk for the environment, weights, checkout and evidence, and 5 GiB resident memory. Skill cards and campaign-wide dependency coverage require separate evidence.

Replay reads committed moves and verifies the event chain. A fresh fork runs the controller again from the same opening with one changed input.

## Play on the VM

From Stack root run `python3 -m ahbg.campaign --lab serve` and open the printed loopback address. Play the turn, change one thing, and play the fork. Reload the original replay URL after restarting the server to reopen the saved decision. For a phone, forward VM port 8112 through your existing private connection. The play surface uses a deterministic subordinate and stores turns in the operator's local state directory. The local `--lab` switch supplies a test entitlement. Omit it for basic play.

The same entry point supports `--lab play two-exits`, `--lab replay TURN_ID` and `--lab fork TURN_ID competing-move`. A fork runs the controller on the reconstructed starting case. A replay resolves the saved submitted plan again, verifies the event chain, board and construction ledger, and requires no inference.

## Model trials

Install CPU PyTorch 2.9.1 and Transformers 4.57.3 into a dedicated Python 3.12 environment. Set PYTHON to its absolute interpreter path. Run these commands from Stack root. The operator cache contains the original model files. Model weights are distributed by their respective publishers.

```sh
for model in smol granite; do
  "$PYTHON" -m ahbg.campaign.fetch_model "$model"
done
for controller in scripted random smol granite; do
  systemd-run --user --wait --pipe --working-directory="$PWD" \
    -p RestrictAddressFamilies=AF_UNIX -p MemoryMax=5G \
    -E OMP_NUM_THREADS=2 -E HF_HUB_OFFLINE=1 \
    "$PYTHON" -m ahbg.campaign.trial "$controller" --out "$HOME/ahbg-122-evidence"
done
python3 -m ahbg.campaign.learned --out "$HOME/ahbg-122-evidence"
python3 -m unittest discover -s ahbg/campaign/tests
```

Each completed pair is an atomic checkpoint. Use a new output directory for a fresh trial. The summary counts each saved arm once. Command lengths in this fixture count Unicode code points. Matching an external command interface remains a separate interoperability check.

## VM results

The scripted Builder reached all four expected exits. Adding the competing move preserved its A decision and left it on RING_0. The resolver awarded RING_1 to the rival. With the center hidden, withholding the report gave HOLD and delivering it gave A. All four model conditions ran locally on the VM's two Xeon vCPUs. Each controller made 16 decisions in eight matched pairs. The table reports the balanced four-condition subset for accuracy and all 16 decisions for timing. The paired throughput includes resolution and evidence writes.

| Subordinate | Correct exits / 4 | Median decision ms | p95 decision ms | Paired turns/s | Peak process MiB |
|---|---:|---:|---:|---:|---:|
| Scripted | 4 | 0.007 | 0.012 | 46.1 | 22 |
| Seeded random | 0 | 0.009 | 0.012 | 50.9 | 22 |
| SmolLM2 135M | 0 | 1066 | 1548 | 0.86 | 1145 |
| Granite 4.0 350M | 0 | 1786 | 2042 | 0.55 | 2394 |

On the occupied-center turn SmolLM2 returned a quoted A for both orders. Granite returned the word builder for both. Both are invalid under the frozen exact-label parser. A separate supervised table trained on 16 engine demonstrations and matched the teacher on 16/16 decisions across four held-out fixture families. It has explicit order and center-state features and a fixed vocabulary. Language generalization, mobile-device latency and population performance remain unmeasured. The fixture commander supplies fixed orders. Current-A0 commander inference, autonomous fauna inference and true spawning require further integration.

Use `--controller smol` or `--controller granite` before `serve` to play through the cached local model. Saved decision replay works without loading weights. Fresh model forks require the original controller. The VM trial rejects a model-scoring process that can open an IPv4 or IPv6 socket.

## Source and reader evidence

The owner inventory on 2026-11-26 contained 37 repositories. The [register](evidence/coverage.tsv) assigns ten runtime, nine content, eight release, three recovery and seven historical obligations. Four rows have executable evidence in this slice. The remaining 33 have proposed consumers and first-failure tests. Five repositories are archived and two more carry owner retirement notices. Weave and PSFR belong to Stack and add no repositories to the denominator. Weave still needs a profile that restores a replay through its corpus/thread cycle. PSFR still needs a synthetic copying, isolation and repair trial that distinguishes ancestry from repetition.

Removing UCNS’s seed module in an isolated copy stopped the mission before its first legal menu. Restoring the bytes reproduced the original board digest, as did adding an unread file. Of nine imported UCNS modules, six match the claimed upstream revision, one differs and two are absent there. Five of the twenty EDCM measurement and canon files differ between Stack’s vendored copy and the measured upstream. The inspector consumes the verified upstream measurement package. [Geometry control](evidence/geometry-control.json) · [Source comparisons](evidence/source-comparison.json)

The native UCHC input reader recovered the Unicode fixture byte-for-byte and reported partial admission. The released ordinal wheel replayed both epicycle results, and the separate Stack encoding check recovered the 16-bit radial profile. With identical training examples and a lookup policy, text, native input occurrences, ordinal, combined and recursive readers each matched 16/16 held-out choices. The additive-only reader matched 8/16; the two reordered orders had equal additive representations. Swapping order evidence at evaluation changed the other readers to 0/16. This bounded result ties the ordinal reader with raw text. [Reader measurements](evidence/reader-summary.json) · [Native recovery](evidence/unicode.json) · [Ordinal verification](evidence/halving.json)

Open **Inspect eleven EDCM comparisons** in the local lab. Each contrast retains exact speaker windows, both raw eleven-dimensional vectors, the engine’s independent movement outcome and an interpretation limit. The scope fixtures gave +1 and −1. Equal corrections with opposite actions received equal text measurements. Dialogue in this inspector is synthetic. It runs passively and supplies no rule or adjudication authority. [Exact contrasts](evidence/metric-contrasts.json)

To reproduce the optional measurements, follow the released wheel and native producer pins in `integration/uchc/README.md`. Use a separate Python 3.12 environment with the wheel, its pinned UCNS producer, and EDCM from commit `acadaae913846613c9bbb9ef82d5ce6cf57214b3`. Run these commands from Stack root.

```sh
python -m ahbg.campaign.geometry_control
python -m ahbg.campaign.readers /path/to/verified/input/construct.db /tmp/readers.json
python -m ahbg.campaign.inspector /path/to/exact/edcm/source /tmp/metric-contrasts.json
```

## Open campaign obligations

| Obligation | Current boundary and condition to resume |
|---|---|
| A0 commander, autonomous fauna and multiplayer | The gameplay UI and offline trials host the Builder locally. The rival is a precommitted fixture. The deployed A0 checkout exposes authenticated `/api/conversations` and `/api/ahbg/sessions`; the reviewed Stack adapter targets `/api/v1/conversations`. Qualify an authenticated, VM-local A0 integration and demonstrate two isolated owner/participant views. |
| AP, construction, spawn, Warrior, loyalty, absence and capture-six | This mission exposes one move and the existing simultaneous resolver. Owner-specified AP accounting, spawn triggers and lineage, capture-six adjudication, absence timing and loyalty transitions need executable owner rules and campaign cases. Seeded occupants supply no spawning evidence. |
| Skill card | TIWCG supplies a politics rules implementation and its plan describes extraction of the common kernel. The territory adapter, action timing, affordability and idempotent tile/debit commit still need a shared contract. |
| Structural corpus | Supply a field matching database SHA-256 `13ba24116f0ff02cfdfeb4a6b060f2672fa409b46a3b7cf26e4421c65321b063` and the structural lock, or run its pinned build. That workflow requires more than 8 GiB available; the VM had 4.3 GiB available after the model installation. |
| Evaluation | Live commander exchanges, population saturation, end-to-end turn latency quantiles, copy/fork memory semantics, genuine handset install/reconnect, and full dependency removal/restoration remain unmeasured. |
| Distribution | Weights and corpus databases stay on the VM. Stack’s licensing map reserves the decision on original AHBG and media to the owner. Clear the release manifest and rights per shipped component before distributing a commercial build. |
