# a0min — minimal agent harness over the platonic superpotential

`a0min` imports the **platonic agent** from
[`The-Interdependency/a0`](https://github.com/The-Interdependency/a0) and wraps
it in the smallest harness that can create any of the **potential sub-agents**
the superpotential declares, plus a minimal CLI.

## Provenance

| File | Imported from | Commit |
|---|---|---|
| `a0min/platonic/platonic.py` | `a0/python/agents/platonic.py` | `f9470a74138da89a2d075ecf6c3241aac63923f1` |
| `a0min/platonic/platonic_regions.py` | `a0/python/agents/platonic_regions.py` | `f9470a74138da89a2d075ecf6c3241aac63923f1` |
| `a0min/platonic/zfae.py` | `a0/python/agents/zfae.py` | `f9470a74138da89a2d075ecf6c3241aac63923f1` |

The imported files are copied **verbatim** and retain their a0 canonical ratios
seals. Cap semantics (depth / fanout / concurrent-live, tier fallbacks, env
overrides) mirror `a0/python/services/spawn_caps.py`.

## The superpotential and its options

`candidate_platonic_agent()` is the open superpotential
(`a0.agent.platonic`): 13 dimensions and 11 declared semantic regions. Each
region is one **potential sub-agent option**:

```
definition, instance, run, semantic_memory, ptcna_runtime_state,
run_artifacts, zfae_inference_binding, provider_relation,
privacy_projection, spawn_merge, resource_need_matching
```

Creating a sub-agent means projecting one region: selected, omitted, and
unresolved dimensions stay explicit; unknown regions and unknown dimensions
fail closed.

## Harness (library)

```python
from a0min import Harness, SpawnCapExceeded

harness = Harness(tier="free")                 # caps from a0 spawn_caps
options = harness.potential_sub_agents()       # the 11 potential sub-agents

sub = harness.create(
    "definition",
    {"identity": {"definition_id": "def-1"}},
    task="minimal definition",
    orchestration_mode="single",
    cut_mode="soft",
)
print(sub.sub_agent_id, sub.name, sub.unresolved)

harness.merge(sub.sub_agent_id)                # release concurrent-live slot
```

Caps: `A0MIN_MAX_SPAWN_DEPTH` / `A0MIN_MAX_SPAWN_FANOUT` /
`A0MIN_MAX_SPAWN_CONCURRENT_LIVE` env vars override tier defaults
(`free=2/5/2`, `seeker=3/5/4`, `operator=4/5/8`, `patron=5/5/12`,
`admin=5/5/20`).

## CLI

```bash
cd a0min
python3 -m a0min list                      # potential sub-agent options
python3 -m a0min create definition \
    --bind 'identity={"definition_id":"def-1"}' \
    --task "minimal definition" --mode single --cut soft
python3 -m a0min show a0z-12345678
python3 -m a0min merge a0z-12345678
python3 -m a0min superpotential            # dump the imported superpotential
python3 -m a0min caps --tier seeker
python3 -m a0min env                       # provider keys present (never values)
```

Every command accepts `--json` for machine-readable output.

## Provider keys

`a0min.env` reads provider API keys from a local `.env` file without hardcoding
them and without ever emitting key values:

```python
from a0min import load_provider_keys, provider_key, available_providers, presence

keys = load_provider_keys()          # {'openai': ..., 'deepseek': ..., 'xai': ...}
provider_key("openai")               # the key, or None
available_providers()                # ('openai', 'deepseek', 'xai') subset
presence()                           # {'openai': True, ...} — booleans only
```

Search order: `A0MIN_ENV_PATH`, then `./.env`, then `~/.env` (first match wins
per provider). Supported variables: `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`,
`XAI_API_KEY`. The `env` CLI command (and `presence()`) expose presence only —
key material is returned solely to in-process callers that ask for it.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Scope

The harness is intentionally **in-memory and stdlib-only**. It creates and
tracks sub-agent records; it does not execute inference, persistence, or
networking. Runtime realization (providers, PCNA forks, storage) is downstream
of the projection the harness produces.
