"""Execute one preregistered matched AHBG intervention pair."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Mapping

from ahbg.runtime.runtime import RuntimeConfig, RunResult, run_plane

from .interventions import (
    InterventionError,
    InterventionSpec,
    build_pair_receipt,
    validate_case_pair,
)
from .phenotype import derive_run_phenotype


HarnessFactory = Callable[[str], Any]


def _fresh_directory(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise InterventionError(
            f"benchmark output directory must be empty before execution: {path}"
        )
    path.mkdir(parents=True, exist_ok=True)


def _manifest(agent: Any) -> dict[str, Any]:
    manifest = agent.manifest()
    if not isinstance(manifest, Mapping):
        raise InterventionError("agent manifest must be an object")
    try:
        # Canonical round trip rejects non-JSON identity before API calls begin.
        return json.loads(
            json.dumps(
                dict(manifest),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            )
        )
    except (TypeError, ValueError) as exc:
        raise InterventionError(f"agent manifest is not canonical JSON: {exc}") from exc


def _close(agent: Any) -> None:
    closer = getattr(agent, "close", None)
    if callable(closer):
        closer()


def _case(config: RuntimeConfig, manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "runtime": config.as_dict(),
        "agent": dict(manifest),
    }


def _result_document(result: RunResult) -> dict[str, Any]:
    raw = result.as_dict()
    return {
        "phenotype": derive_run_phenotype(raw),
        "run": raw,
    }


def run_matched_pair(
    spec: InterventionSpec,
    *,
    seed: int,
    control_config: RuntimeConfig,
    treatment_config: RuntimeConfig,
    harness_factory: HarnessFactory,
    out_dir: Path | str,
) -> dict[str, Any]:
    """Run one paired seed after proving one-variable isolation.

    Two fresh harness instances are required so treatment state cannot leak into
    control state or vice versa. Case equivalence is validated before either
    harness is asked to plan, keeping confounded trials from consuming provider
    calls and later masquerading as evidence.
    """

    if seed not in spec.seeds:
        raise InterventionError(f"seed {seed} was not preregistered")
    if control_config.seed != seed or treatment_config.seed != seed:
        raise InterventionError(
            "both runtime configs must use the preregistered paired seed"
        )

    root = Path(out_dir)
    _fresh_directory(root)
    control_dir = root / "control"
    treatment_dir = root / "treatment"

    control_agent = harness_factory("control")
    treatment_agent = harness_factory("treatment")
    try:
        control_manifest = _manifest(control_agent)
        treatment_manifest = _manifest(treatment_agent)
        control_case = _case(control_config, control_manifest)
        treatment_case = _case(treatment_config, treatment_manifest)

        # Fail before model/provider work if any unregistered second variable
        # changed, including agent identity or execution mode.
        validate_case_pair(spec, control_case, treatment_case)

        control_result = run_plane(
            agent=control_agent,
            config=control_config,
            out_dir=control_dir,
        )
        treatment_result = run_plane(
            agent=treatment_agent,
            config=treatment_config,
            out_dir=treatment_dir,
        )

        control_document = _result_document(control_result)
        treatment_document = _result_document(treatment_result)
        receipt = build_pair_receipt(
            spec,
            seed=seed,
            control_case=control_case,
            treatment_case=treatment_case,
            control_result=control_document,
            treatment_result=treatment_document,
        )

        (root / "control-case.json").write_text(
            json.dumps(control_case, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (root / "treatment-case.json").write_text(
            json.dumps(treatment_case, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (root / "control-phenotype.json").write_text(
            json.dumps(control_document["phenotype"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (root / "treatment-phenotype.json").write_text(
            json.dumps(treatment_document["phenotype"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (root / "receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return receipt
    finally:
        _close(control_agent)
        _close(treatment_agent)
