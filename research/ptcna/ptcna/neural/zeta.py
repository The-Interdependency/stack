# ratios: loc_comments=241:76 imports_exports=11:1 calls_definitions=75:19
# 198:61

"""

ZetaEngine — Zeta Function Alpha Echo

ZFAE can learn from an explicitly supplied external measurement provider.

PTCNA does not implement EDCM. A caller-owned provider supplies metrics,
producing a coherence

score that drives PCNA phi/psi/omega reward backprop.

Naming: a0(zeta fun alpha echo) {provider}

- zeta = the observer function

- fun = the phi ring coherence transform

- alpha = the learning rate parameter

- echo = the feedback signal returned to the ring

When no provider is configured, evaluation returns a typed suspended event and
does not nudge the neural engine. PTCNA itself performs no external API calls.

Resolution:

Each directory path can carry its own resolution level (1–5). The most

specific matching prefix wins; the global level applies when nothing matches.

Level 1 = minimal/lightweight observation. Level 5 = maximum depth.

Example: global=3, /system=5 means system-root paths are observed at full depth.

"""

# === MODULE_BUILD ===
# id: pcna_zeta
#   module_name: zeta
#   module_kind: engine
#   summary: ZFAE evaluator that consumes explicitly injected external metrics and nudges PCNAEngine.phi without implementing or importing EDCM.
#   owner: Erin Spencer
#   public_surface: ZetaEngine, _zeta_engine
#   internal_surface: _get_default_pcna, ZetaEngine._coherence_from_metrics, ZetaEngine._sigma_nudge_factors, ZetaEngine._theta_gate_factor
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: hmmm
#   user_data_boundary: read
#   admin_only: false
#   tests: ptcna/neural/tests/test_zeta.py
#   rollout: default_enabled
#   rollback: remove import and call sites
#   requires: pcna_pcna, pcna_sigma
#   since: 0.1.1
#   unresolved: callback network behavior belongs to the caller and is not introspectable by PTCNA
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: zeta_requires_external_measurement_provider
#   given: evaluate is called without an injected measurement provider
#   then: a measurement_suspended event is returned and no neural nudge occurs
#   class: safety
#
# id: zeta_never_imports_shadow_edcm
#   given: evaluation runs with or without an injected provider
#   then: PTCNA does not import or call ptcna.neural.edcm and treats supplied metrics as external evidence
#   class: safety
#
# id: zeta_consumes_explicit_metrics
#   given: an injected provider returns the required bounded metric mapping
#   then: Zeta computes coherence, nudges Phi, and records an external_measurement event
#   class: correctness
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: zeta_external_measurement_boundary
#   summary: reads caller-supplied response text and invokes an injected callback whose network behavior is outside PTCNA authority
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: hmmm
#   user_data_boundary: read
#   admin_only: false
#   pii: possible
#   secrets: none
#   owner: Erin Spencer
#   since: 0.1.1
# === END BOUNDARIES ===

import time

from collections import deque
from collections.abc import Callable, Mapping

from typing import Optional

MetricProvider = Callable[[str, str], Mapping[str, float]]

_DEFAULT_RESOLUTION = 3

_MIN_RES = 1

_MAX_RES = 5


class ZetaEngine:

    """

    Non-LLM real-time learning engine with per-directory resolution control.

    Consumes caller-supplied measurements and drives PCNA backprop.

    """

    AGENT_NAME = "a0(zeta fun alpha echo)"

    def __init__(
        self,
        buffer_size: int = 50,
        metric_provider: Optional[MetricProvider] = None,
    ):

        self.echo_buffer: deque = deque(maxlen=buffer_size)

        self.eval_count = 0

        self.created_at = time.time()

        self.metric_provider = metric_provider

        self.resolution_config: dict = {

            "global": _DEFAULT_RESOLUTION,

            "directories": {},

        }

    def set_metric_provider(
        self,
        metric_provider: Optional[MetricProvider],
    ) -> None:

        """Replace or suspend the caller-owned measurement provider."""

        self.metric_provider = metric_provider

    def get_resolution(self, path: str = "") -> int:

        """Return the resolution level for the given path."""

        config = self.resolution_config

        dirs = config.get("directories", {})

        if not path or not dirs:

            return config.get("global", _DEFAULT_RESOLUTION)

        normalized = path.rstrip("/")

        best_level: Optional[int] = None

        best_len = -1

        for dir_path, level in dirs.items():

            dp = dir_path.rstrip("/")

            if normalized == dp or normalized.startswith(dp + "/"):

                if len(dp) > best_len:

                    best_level = level

                    best_len = len(dp)

        return best_level if best_level is not None else config.get("global", _DEFAULT_RESOLUTION)

    def set_global_resolution(self, level: int) -> dict:

        self.resolution_config["global"] = max(_MIN_RES, min(_MAX_RES, level))

        return dict(self.resolution_config)

    def set_directory_resolution(self, path: str, level: int) -> dict:

        self.resolution_config.setdefault("directories", {})[path] = max(_MIN_RES, min(_MAX_RES, level))

        return dict(self.resolution_config)

    def remove_directory_resolution(self, path: str) -> dict:

        self.resolution_config.get("directories", {}).pop(path, None)

        return dict(self.resolution_config)

    def load_resolution_config(self, config: dict) -> None:

        if not isinstance(config, dict):

            return

        self.resolution_config = {

            "global": max(_MIN_RES, min(_MAX_RES, int(config.get("global", _DEFAULT_RESOLUTION)))),

            "directories": {

                k: max(_MIN_RES, min(_MAX_RES, int(v)))

                for k, v in config.get("directories", {}).items()

                if isinstance(k, str) and isinstance(v, (int, float))

            },

        }

    def _coherence_from_metrics(self, metrics: dict) -> float:

        cm = metrics.get("cm", 0.0)

        da = metrics.get("da", 0.0)

        int_val = metrics.get("int_val", 0.0)

        drift = metrics.get("drift", 0.0)

        coherence = (cm * 0.35 + da * 0.25 + int_val * 0.25 + (1.0 - drift) * 0.15)

        return round(max(0.0, min(1.0, coherence)), 4)

    def _sigma_nudge_factors(self) -> tuple[float, float]:

        change_boost = 1.0

        substrate_factor = 1.0

        try:

            from .sigma import get_sigma

        except ImportError:

            return change_boost, substrate_factor

        try:

            sig = get_sigma()

            drained = sig.drain_content_changed_events()

            if drained:

                change_boost = 1.2

                substrate_factor = round(0.8 + sig.ring_coherence * 0.4, 4)

        except Exception as exc:

            print(f"[zfae:sigma_factors] error reading Sigma factors: {exc}")

        return change_boost, substrate_factor

    def _theta_gate_factor(self) -> float:

        try:

            theta = _get_default_pcna().theta

            open_frac = float(theta.gate_open.mean())

            return round(0.8 + open_frac * 0.4, 4)

        except Exception as exc:

            print(f"[zfae:gate_factor] error reading Theta gate factor: {exc}")

            return 1.0

    async def evaluate(

        self,

        assistant_text: str,

        provider: str,

        user_text: str = "",

        path: str = "",

    ) -> dict:

        resolution = self.get_resolution(path)

        if self.metric_provider is None:

            event = {

                "agent": self.AGENT_NAME,

                "provider": provider,

                "status": "measurement_suspended",

                "reason": (
                    "no external measurement provider configured; "
                    "PTCNA does not implement EDCM"
                ),

                "resolution": resolution,

                "path": path or None,

                "ts": time.time(),

            }

            self.echo_buffer.append(event)

            return event

        try:

            metrics = dict(self.metric_provider(assistant_text, user_text))

            coherence = self._coherence_from_metrics(metrics)

            base_lr = 0.025

            gate_factor = self._theta_gate_factor()

            change_boost, substrate_factor = self._sigma_nudge_factors()

            effective_lr = base_lr * gate_factor * change_boost * substrate_factor

            try:

                pcna = _get_default_pcna()

                pcna.phi.nudge(coherence, lr=effective_lr)

            except Exception:

                pass

            self.eval_count += 1

            event = {

                "agent": self.AGENT_NAME,

                "provider": provider,

                "status": "external_measurement",

                "coherence": coherence,

                "cm": metrics.get("cm"),

                "da": metrics.get("da"),

                "drift": metrics.get("drift"),

                "int_val": metrics.get("int_val"),

                "resolution": resolution,

                "path": path or None,

                "base_lr": base_lr,

                "gate_factor": gate_factor,

                "change_boost": change_boost,

                "substrate_factor": substrate_factor,

                "effective_lr": round(effective_lr, 6),

                "ts": time.time(),

            }

            self.echo_buffer.append(event)

            suffix = f" path={path}" if path else ""

            print(

                f"[zfae:echo] provider={provider} coherence={coherence}"

                f" lr={effective_lr:.4f}"

                f" gate={gate_factor} boost={change_boost} sub={substrate_factor}"

                f" resolution={resolution}{suffix}"

            )

            return event

        except Exception as e:

            print(f"[zfae:echo] error: {e}")

            event = {

                "agent": self.AGENT_NAME,

                "provider": provider,

                "status": "measurement_error",

                "reason": str(e),

                "resolution": resolution,

                "path": path or None,

                "ts": time.time(),

            }

            self.echo_buffer.append(event)

            return event

    def set_sigma_resolution(self, level: int) -> dict:

        try:

            from .sigma import get_sigma

            get_sigma().set_resolution(level)

            event = {"type": "sigma_resolution", "level": level, "ts": time.time()}

            self.echo_buffer.append(event)

            print(f"[zfae:sigma] resolution set to {level}")

            return event

        except Exception as exc:

            print(f"[zfae:sigma] set_resolution error: {exc}")

            return {}

    def sigma_watch_file(self, path: str) -> dict:

        try:

            from .sigma import get_sigma

            get_sigma().add_content_watch(path)

            event = {"type": "sigma_watch_add", "path": path, "ts": time.time()}

            self.echo_buffer.append(event)

            print(f"[zfae:sigma] watching {path}")

            return event

        except Exception as exc:

            print(f"[zfae:sigma] watch_file error: {exc}")

            return {}

    def sigma_unwatch_file(self, path: str) -> dict:

        try:

            from .sigma import get_sigma

            get_sigma().remove_content_watch(path)

            event = {"type": "sigma_watch_remove", "path": path, "ts": time.time()}

            self.echo_buffer.append(event)

            print(f"[zfae:sigma] unwatched {path}")

            return event

        except Exception as exc:

            print(f"[zfae:sigma] unwatch_file error: {exc}")

            return {}

    def set_sigma_structural_interval(self, seconds: float) -> dict:

        try:

            from .sigma import get_sigma

            get_sigma().structural_interval = max(1.0, seconds)

            event = {"type": "sigma_structural_interval", "seconds": seconds, "ts": time.time()}

            self.echo_buffer.append(event)

            print(f"[zfae:sigma] structural interval → {seconds}s")

            return event

        except Exception as exc:

            print(f"[zfae:sigma] set_structural_interval error: {exc}")

            return {}

    def set_sigma_content_interval(self, seconds: float) -> dict:

        try:

            from .sigma import get_sigma

            get_sigma().content_interval = max(1.0, seconds)

            event = {"type": "sigma_content_interval", "seconds": seconds, "ts": time.time()}

            self.echo_buffer.append(event)

            print(f"[zfae:sigma] content interval → {seconds}s")

            return event

        except Exception as exc:

            print(f"[zfae:sigma] set_content_interval error: {exc}")

            return {}

    def state(self) -> dict:

        return {

            "agent": self.AGENT_NAME,

            "eval_count": self.eval_count,

            "echo_buffer_len": len(self.echo_buffer),

            "uptime_s": round(time.time() - self.created_at, 1),

            "resolution": self.resolution_config,

        }


_zeta_engine = ZetaEngine()

_default_pcna = None


def _get_default_pcna():
    global _default_pcna
    if _default_pcna is None:
        from .pcna import PCNAEngine
        _default_pcna = PCNAEngine()
    return _default_pcna

# 198:61
# ratios: loc_comments=241:76 imports_exports=11:1 calls_definitions=75:19
