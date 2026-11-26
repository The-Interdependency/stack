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
