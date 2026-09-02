# AHBG production runtime

Canonical runnable AHBG: one production implementation that repeatedly
completes the minimum loop.

```text
UCNS plane -> observe -> plan -> simultaneous resolution
-> move/collision effects -> persist -> next turn
```

## Modules

- `protocol.py` — observe/plan/act schemas and the capability vocabulary.
- `harness.py` — `AgentHarness` contract; `A0Harness` (reference agent via the
  canonical `a0` package) and `SubprocessHarness` (external JSON-lines client).
- `runtime.py` — `run_plane()` production loop using the frozen Grok engine
  (`Field`, `Cycle`, war_v3, `Chain` persistence).
- `server.py` — thin HTTP bridge serving the presentation board and the same
  observe/plan/act contract for mobile/embedded clients.
- `entitlements.py` — one entitlement, `benchmark_lab`; basic play and harness
  connectivity are free.
- `engine.py` — binds the frozen engine modules by file path so
  `ahbg.runtime` and `ahbg.grok` never fight over the `ahbg` package name.

## Capability bound

Advertised capabilities: `observe`, `plan`, `relocate`. `construct`/build is
regulatory in the frozen engine — recorded as deferred, never emitted as an
executable intent. The runtime rejects any intent outside an agent's advertised
capabilities. A0 uses exactly this interface; there is no privileged A0 path.

## Usage guidance

```bash
# play with A0 through the standard harness interface
PYTHONPATH=.:libs/ucns/src python -m ahbg.runtime play --agent a0 --turns 8 --out /tmp/ahbg-run

# drive the loop from an external conforming harness subprocess
PYTHONPATH=.:libs/ucns/src python -m ahbg.runtime play \
    --agent-subprocess "python3,my_harness.py" --turns 5 --out /tmp/ahbg-run

# HTTP bridge for the Android surface / any JSON client
PYTHONPATH=.:libs/ucns/src python -m ahbg.runtime.server --port 8765

# tests
python -m unittest discover -s ahbg/runtime/tests -q
```

## Subprocess harness protocol

One JSON line per turn in; one JSON line out.

```text
{"type":"observe","observation":{...}}
{"type":"plan","plan":{"session_id":"...","turn":0,"intents":[...]}}
```

## Entitlement boundary

`benchmark_lab` gates advanced scenarios, saved/replayed run comparison, and
adversarial benchmark packs. The runtime checks claims only; RevenueCat
verification happens on the Android client. Unverified claims are treated as
absent.

## hmmm

- UCNS construction authority: `construct` remains regulatory until UCNS
  defines construction state; the loop records defer effects and never builds.
- Store publication signing, submission assets, and a release HTTPS runtime
  URL remain outside this pass.
