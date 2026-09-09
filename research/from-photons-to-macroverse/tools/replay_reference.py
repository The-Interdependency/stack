#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: arity_recursion_replay_reference
#   module_name: replay_reference
#   module_kind: experiment
#   summary: supplies the sole executable authority for deterministic replay semantics before sealed runs
#   owner: The-Interdependency/stack research package
#   public_surface: contract, vectors, verify
#   internal_surface: canonical streams, schedules, parameter addresses, deterministic math, optimizer recurrence
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/from-photons-to-macroverse/tests/test_contracts.py
#   rollout: pin this file and its vectors in replay_reference.json before any sealed run
#   rollback: remove the executable binding while run status remains not-run
# === END MODULE_BUILD ===
"""Deterministic replay authority for ``arity-recursion-synthetic-v6``.

This executable closes the byte-bearing choices that prose cannot safely make
normative.  It does not run the scientific experiment and opens no sealed seed.

Usage guidance::

    python tools/replay_reference.py contract
    python tools/replay_reference.py vectors
    python tools/replay_reference.py verify

``verify`` fails closed unless this file and its generated vectors match
``replay_reference.json``.  Run it before implementing or starting a sealed run.
All replayers execute this pinned reference for result-bearing primitives; a
port is admissible only after it reproduces every vector byte-for-byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import struct
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
from pathlib import Path
from typing import Iterable, Sequence


PROTOCOL_ID = "arity-recursion-synthetic-v6"
PROTOCOL_VERSION = "0.4.0"
DIRECT_ARITIES = (2, 3, 5, 6, 7, 8)
NESTED_ARITIES = DIRECT_ARITIES
NOISE_MILLI = (10, 50, 100)
TOKEN = re.compile(r"^[a-z0-9_./-]+$")
PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
)

HYPOTHESIS_IDS = tuple(
    [f"h_a/{arity}" for arity in DIRECT_ARITIES]
    + [f"h_r/{arity}" for arity in NESTED_ARITIES]
    + ["h_7"]
)

GENERATOR_ROLES = {
    "direct": "direct",
    "nested_outer": "nested_outer",
    "nested_leaf": "nested_leaf/{outer}",
}

# Axis ranks make a scalar address complete.  A missing carrier/source/target
# axis is rejected before a model-initializer stream key can be emitted.
PARAMETER_RANKS = {
    "direct": {"l": 3, "w": 4, "v": 3, "h": 2, "b": 2, "rho": 1},
    "nested": {
        "leaf/l": 4,
        "leaf/w": 5,
        "leaf/v": 4,
        "leaf/h": 3,
        "leaf/b": 3,
        "outer/w": 4,
        "outer/v": 3,
        "outer/h": 2,
        "rho": 1,
    },
    "dense": {"u": 2, "a": 1, "v": 2, "c": 1, "rho": 1},
}

CONTRACT = {
    "schema": "the-interdependency.arity-recursion-replay-reference",
    "version": "1.0.0",
    "protocol_id": PROTOCOL_ID,
    "protocol_version": PROTOCOL_VERSION,
    "status": "not-run",
    "authority": "result-bearing deterministic replay semantics",
    "prose_role": "scientific intent and non-use boundary; not an alternate byte-level implementation",
    "direct_arities": list(DIRECT_ARITIES),
    "nested_outer_arities": list(NESTED_ARITIES),
    "generator_roles": GENERATOR_ROLES,
    "model_id": "canonical family_id bytes",
    "hypothesis_ids": list(HYPOTHESIS_IDS),
    "process_noise_index": ["episode_id", "phase", "phase_time", "carrier_id", "coordinate"],
    "process_noise_phases": {"burn": [0, 31], "scored": [0, 127]},
    "initializer_index": ["model_id", "restart", "tensor_name", "all_parameter_axes_in_row_major_order"],
    "training_population_order": [
        "observational episode ordinal",
        "intervention class 1..4",
        "intervention episode ordinal",
        "transition 0..127",
    ],
    "training_population_size": 12288,
    "schedule_candidate_encoding": "canonical compact JSON array, sorted by UTF-8 bytes",
    "variance_head_space": "model output before the fixed observation decoder",
    "restart_tie_break": "lowest restart index",
    "recovery_baseline": "mode-matched unperturbed rollout x^(0,M,f)",
    "adam": {
        "step_origin": 1,
        "learning_rate": "0.001",
        "beta_1": "0.9",
        "beta_2": "0.999",
        "epsilon": "1e-8",
        "epsilon_placement": "outside sqrt(v_hat)",
        "bias_correction": "after updating m, v, beta_1_power, beta_2_power",
        "operation_order": "the adam_step function below, rounded to binary64 after every scalar operation",
    },
    "transcendentals": {
        "authority": "functions in this exact hash-pinned executable",
        "decimal_precision": 96,
        "decimal_rounding": "ROUND_HALF_EVEN",
        "normal": "fixed-pi decimal Box-Muller cosine lane, then binary64",
        "cdf_tail": "exact 0 below -8 and exact 1 above 8",
    },
    "label_shuffle_zero_difference": {
        "standing": "equivalent",
        "g": 0,
        "interval": [0, 0],
        "superiority_member": False,
    },
    "class_5_weights": {"full": "0.5", "cut": "0.5"},
    "class_6_pair_order": [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]],
}


def canonical_json(value: object) -> bytes:
    """Return the one admitted JSON byte encoding."""

    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


def _token(value: str, field: str) -> str:
    if not TOKEN.fullmatch(value):
        raise ValueError(f"{field} is not a canonical token: {value!r}")
    return value


def _uint(value: int, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be an unsigned integer")
    return value


def stream_bytes(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    domain: str,
    role: str,
    indices: Sequence[str | int],
    block: int = 0,
) -> bytes:
    """Serialize one complete counter-stream key."""

    _uint(seed, "seed")
    _uint(arity, "arity")
    if sigma_milli not in NOISE_MILLI:
        raise ValueError("sigma_milli must be 10, 50, or 100")
    _token(domain, "domain")
    _token(role, "role")
    normalized: list[str | int] = []
    for position, value in enumerate(indices):
        if isinstance(value, str):
            normalized.append(_token(value, f"indices[{position}]"))
        else:
            normalized.append(_uint(value, f"indices[{position}]"))
    _uint(block, "block")
    return canonical_json(
        [PROTOCOL_ID, seed, arity, sigma_milli, domain, role, normalized, block]
    )


def digest_words(payload: bytes) -> tuple[int, int, int, int]:
    digest = hashlib.sha256(payload).digest()
    return struct.unpack(">QQQQ", digest)


def f64(value: float | Decimal | int) -> float:
    return struct.unpack(">d", struct.pack(">d", float(value)))[0]


def f64_hex(value: float) -> str:
    return struct.pack(">d", f64(value)).hex()


def fadd(left: float, right: float) -> float:
    return f64(f64(left) + f64(right))


def fsub(left: float, right: float) -> float:
    return f64(f64(left) - f64(right))


def fmul(left: float, right: float) -> float:
    return f64(f64(left) * f64(right))


def fdiv(left: float, right: float) -> float:
    return f64(f64(left) / f64(right))


def open_uniform(payload: bytes, lane: int = 0) -> float:
    if lane not in range(4):
        raise ValueError("lane must be 0..3")
    word = digest_words(payload)[lane]
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        return f64((Decimal(word) + Decimal("0.5")) / (Decimal(2) ** 64))


def _decimal(value: float | Decimal | int | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal.from_float(f64(value))
    return Decimal(value)


def decimal_cos(value: Decimal) -> Decimal:
    """Deterministic cosine with fixed reduction and series termination."""

    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        two_pi = PI * 2
        x = value % two_pi
        if x > PI:
            x -= two_pi
        term = Decimal(1)
        total = Decimal(1)
        n = 0
        threshold = Decimal(1).scaleb(-92)
        while True:
            n += 1
            term = -(term * x * x) / Decimal((2 * n - 1) * (2 * n))
            updated = total + term
            if abs(term) < threshold or updated == total:
                return +updated
            total = updated


def deterministic_sqrt(value: float) -> float:
    if value < 0:
        raise ValueError("sqrt input must be nonnegative")
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        return f64(_decimal(value).sqrt())


def standard_normal(payload: bytes) -> float:
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        u0 = _decimal(open_uniform(payload, 0))
        u1 = _decimal(open_uniform(payload, 1))
        radius = (-Decimal(2) * u0.ln()).sqrt()
        return f64(radius * decimal_cos(Decimal(2) * PI * u1))


def deterministic_exp(value: float) -> float:
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        return f64(_decimal(value).exp())


def deterministic_log(value: float) -> float:
    if value <= 0:
        raise ValueError("log input must be positive")
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        return f64(_decimal(value).ln())


def deterministic_tanh(value: float) -> float:
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        x = _decimal(value)
        if x >= 24:
            return 1.0
        if x <= -24:
            return -1.0
        exp2x = (Decimal(2) * x).exp()
        return f64((exp2x - 1) / (exp2x + 1))


def deterministic_softplus(value: float) -> float:
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        x = _decimal(value)
        if x > 40:
            return f64(x)
        return f64((Decimal(1) + x.exp()).ln())


def gaussian_cdf(value: float) -> float:
    """Deterministic standard-normal CDF; tails are frozen at +/-8."""

    if value <= -8.0:
        return 0.0
    if value >= 8.0:
        return 1.0
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        x = _decimal(value) / Decimal(2).sqrt()
        term = x
        total = x
        n = 0
        threshold = Decimal(1).scaleb(-92)
        while True:
            n += 1
            term = -(term * x * x) / Decimal(n)
            addend = term / Decimal(2 * n + 1)
            updated = total + addend
            if abs(addend) < threshold or updated == total:
                erf = Decimal(2) * updated / PI.sqrt()
                return f64((Decimal(1) + erf) / Decimal(2))
            total = updated


def family_kind(family_id: str) -> str:
    _token(family_id, "family_id")
    if family_id.startswith("capacity-only/"):
        return "dense"
    if "/tree" in family_id or family_id.startswith(
        ("nested/", "wrong-tree/", "outer-cut/", "unnested/")
    ):
        return "nested"
    return "direct"


def parameter_path(family_id: str, tensor_name: str, axes: Sequence[int]) -> bytes:
    kind = family_kind(family_id)
    ranks = PARAMETER_RANKS[kind]
    if tensor_name not in ranks:
        raise ValueError(f"tensor {tensor_name!r} is not valid for {kind}")
    if len(axes) != ranks[tensor_name]:
        raise ValueError(
            f"{kind}/{tensor_name} requires {ranks[tensor_name]} axes; got {len(axes)}"
        )
    normalized = [_uint(axis, "parameter axis") for axis in axes]
    return canonical_json([PROTOCOL_ID, "parameter-mask", family_id, tensor_name, normalized])


def initializer_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    family_id: str,
    restart: int,
    tensor_name: str,
    axes: Sequence[int],
) -> bytes:
    # The actual axes, rather than a local row/column suffix, enter the stream.
    parameter_path(family_id, tensor_name, axes)
    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="model_initializers",
        role="parameter",
        indices=[family_id, _uint(restart, "restart"), tensor_name, *axes],
    )


def process_noise_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    role: str,
    episode_id: str,
    phase: str,
    phase_time: int,
    carrier_id: str,
    coordinate: int,
) -> bytes:
    bounds = {"burn": 31, "scored": 127}
    if phase not in bounds or not 0 <= phase_time <= bounds[phase]:
        raise ValueError("phase/time is outside the frozen process-noise range")
    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="process_noise",
        role=role,
        indices=[episode_id, phase, phase_time, carrier_id, coordinate],
    )


def coefficient_role(system_kind: str, attempt: int, outer: int | None = None) -> str:
    _uint(attempt, "attempt")
    if system_kind == "direct":
        base = GENERATOR_ROLES["direct"]
    elif system_kind == "nested_outer":
        base = GENERATOR_ROLES["nested_outer"]
    elif system_kind == "nested_leaf" and outer is not None:
        base = GENERATOR_ROLES["nested_leaf"].format(outer=_uint(outer, "outer"))
    else:
        raise ValueError("unknown or incomplete generator role")
    return f"{base}/attempt/{attempt}"


def hypothesis_id(kind: str, arity: int | None = None) -> str:
    if kind == "h_7" and arity is None:
        return "h_7"
    if kind in {"h_a", "h_r"} and arity in DIRECT_ARITIES:
        result = f"{kind}/{arity}"
        if result in HYPOTHESIS_IDS:
            return result
    raise ValueError("hypothesis has no canonical identifier")


def training_population() -> list[tuple[str, int]]:
    episodes = [f"obs/train/{ordinal:03d}" for ordinal in range(64)]
    episodes.extend(
        f"int/{intervention_class}/train/{ordinal:03d}"
        for intervention_class in range(1, 5)
        for ordinal in range(8)
    )
    return [(episode, transition) for episode in episodes for transition in range(128)]


def minibatch_key(
    *, seed: int, arity: int, sigma_milli: int, family_id: str, restart: int,
    update_index: int, draw_index: int
) -> tuple[bytes, tuple[str, int]]:
    population = training_population()
    payload = stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="minibatch_order",
        role="transition",
        indices=[family_id, restart, update_index, draw_index],
    )
    selected = math.floor(open_uniform(payload) * len(population))
    return payload, population[selected]


def candidate_bytes(kind: str, *identity: str | int) -> bytes:
    shapes = {
        "state": 2,       # observed identity, coordinate
        "edge": 3,        # level, target identity, source identity
        "carrier": 1,     # carrier identity
        "summand": 3,     # w|product, target identity, source identity|none
        "recovery": 2,    # observed identity, coordinate
    }
    if kind not in shapes or len(identity) != shapes[kind]:
        raise ValueError("candidate identity does not match its frozen shape")
    if kind == "summand" and identity[0] not in {"w", "product"}:
        raise ValueError("summand kind must be w or product")
    normalized: list[str | int] = []
    for position, value in enumerate(identity):
        normalized.append(
            _token(value, f"candidate[{position}]")
            if isinstance(value, str)
            else _uint(value, f"candidate[{position}]")
        )
    return canonical_json([kind, *normalized])


def ordered_candidates(candidates: Iterable[bytes]) -> tuple[bytes, ...]:
    result = tuple(sorted(candidates))
    if len(result) != len(set(result)):
        raise ValueError("schedule candidates must be unique")
    return result


def class6_component_ordinals(episode_ordinal: int) -> tuple[tuple[int, int], tuple[int, int]]:
    if not 0 <= episode_ordinal < 12:
        raise ValueError("class-6 episode ordinal must be 0..11")
    pairs = tuple(tuple(item) for item in CONTRACT["class_6_pair_order"])
    pair = pairs[episode_ordinal // 2]
    assigned = []
    for component in pair:
        prior = sum(
            component in pairs[previous // 2] for previous in range(episode_ordinal)
        )
        assigned.append((component, 8 + prior))
    return assigned[0], assigned[1]


def variance_head_paths(family_id: str, model_output_dimension: int) -> tuple[bytes, ...]:
    _uint(model_output_dimension, "model_output_dimension")
    if model_output_dimension == 0:
        raise ValueError("variance head cannot be empty")
    return tuple(
        parameter_path(family_id, "rho", [coordinate])
        for coordinate in range(model_output_dimension)
    )


def select_restart(calibration_nll: Sequence[float]) -> int:
    if len(calibration_nll) != 5 or any(not math.isfinite(value) for value in calibration_nll):
        raise ValueError("restart selection requires five finite NLL values")
    return min(range(5), key=lambda restart: (f64(calibration_nll[restart]), restart))


def serial_sum(values: Iterable[float]) -> float:
    total = 0.0
    for value in values:
        total = fadd(total, value)
    return total


def serial_mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean cannot be empty")
    return fdiv(serial_sum(values), len(values))


def class5_cdf(full: Sequence[bool], cut: Sequence[bool]) -> float:
    # Each mode receives half of one episode id's weight.
    return fadd(fmul(0.5, serial_mean([float(x) for x in full])),
                fmul(0.5, serial_mean([float(x) for x in cut])))


def recovery_baseline_id(mode: str, family_id: str) -> bytes:
    if mode not in {"full", "cut"}:
        raise ValueError("recovery mode must be full or cut")
    _token(family_id, "family_id")
    return canonical_json(["unperturbed", mode, family_id])


def label_shuffle_equivalence(differences: Sequence[float]) -> dict[str, object]:
    if not differences or any(not math.isfinite(value) or value != 0.0 for value in differences):
        return {"standing": "blocked", "g": "hmmm_undefined", "interval": "hmmm_undefined"}
    return {"standing": "equivalent", "g": 0, "interval": [0, 0]}


def adam_step(
    *, parameter: float, gradient: float, first_moment: float, second_moment: float,
    beta1_power: float, beta2_power: float
) -> tuple[float, float, float, float, float]:
    """One exact scalar Adam recurrence; powers enter at their pre-step values."""

    beta1 = 0.9
    beta2 = 0.999
    one_minus_beta1 = fsub(1.0, beta1)
    one_minus_beta2 = fsub(1.0, beta2)
    next_first = fadd(fmul(beta1, first_moment), fmul(one_minus_beta1, gradient))
    gradient_squared = fmul(gradient, gradient)
    next_second = fadd(
        fmul(beta2, second_moment), fmul(one_minus_beta2, gradient_squared)
    )
    next_beta1_power = fmul(beta1_power, beta1)
    next_beta2_power = fmul(beta2_power, beta2)
    first_hat = fdiv(next_first, fsub(1.0, next_beta1_power))
    second_hat = fdiv(next_second, fsub(1.0, next_beta2_power))
    denominator = fadd(deterministic_sqrt(second_hat), 1e-8)
    scaled = fmul(0.001, fdiv(first_hat, denominator))
    next_parameter = fsub(parameter, scaled)
    return next_parameter, next_first, next_second, next_beta1_power, next_beta2_power


def test_vectors() -> dict[str, object]:
    payload = stream_bytes(
        seed=32,
        arity=7,
        sigma_milli=50,
        domain="coefficients",
        role="direct/attempt/0",
        indices=["w", 3, 5, 1, 0],
    )
    initializer_a = initializer_key(
        seed=32, arity=7, sigma_milli=50, family_id="direct/7", restart=0,
        tensor_name="w", axes=[3, 5, 1, 0]
    )
    initializer_b = initializer_key(
        seed=32, arity=7, sigma_milli=50, family_id="direct/7", restart=0,
        tensor_name="w", axes=[4, 5, 1, 0]
    )
    burn = process_noise_key(
        seed=32, arity=7, sigma_milli=50, role="direct",
        episode_id="obs/test/000", phase="burn", phase_time=0,
        carrier_id="3", coordinate=1
    )
    scored = process_noise_key(
        seed=32, arity=7, sigma_milli=50, role="direct",
        episode_id="obs/test/000", phase="scored", phase_time=0,
        carrier_id="3", coordinate=1
    )
    candidates = ordered_candidates(
        [
            candidate_bytes("summand", "product", "outer/2", "none"),
            candidate_bytes("summand", "w", "outer/2", "outer/0"),
            candidate_bytes("summand", "w", "outer/2", "outer/1"),
        ]
    )
    minibatch_payload, minibatch_selected = minibatch_key(
        seed=32, arity=7, sigma_milli=50, family_id="direct/7", restart=0,
        update_index=0, draw_index=0
    )
    adam = adam_step(
        parameter=0.25,
        gradient=-0.125,
        first_moment=0.0,
        second_moment=0.0,
        beta1_power=1.0,
        beta2_power=1.0,
    )
    population = training_population()
    return {
        "schema": "the-interdependency.arity-recursion-replay-vectors",
        "version": "1.0.0",
        "protocol_id": PROTOCOL_ID,
        "stream": {
            "bytes_ascii": payload.decode("ascii"),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "words_hex": [f"{word:016x}" for word in digest_words(payload)],
            "uniform_0_f64": f64_hex(open_uniform(payload, 0)),
            "normal_f64": f64_hex(standard_normal(payload)),
        },
        "initializer": {
            "complete_path_ascii": initializer_a.decode("ascii"),
            "complete_path_sha256": hashlib.sha256(initializer_a).hexdigest(),
            "different_carrier_sha256": hashlib.sha256(initializer_b).hexdigest(),
            "distinct": initializer_a != initializer_b,
        },
        "noise_phase": {
            "burn_ascii": burn.decode("ascii"),
            "scored_ascii": scored.decode("ascii"),
            "distinct": burn != scored,
        },
        "identifiers": {
            "generator_roles": [
                coefficient_role("direct", 0),
                coefficient_role("nested_outer", 0),
                coefficient_role("nested_leaf", 0, outer=3),
            ],
            "model_id": "direct/7",
            "hypotheses": list(HYPOTHESIS_IDS),
            "nested_outer_arities": list(NESTED_ARITIES),
        },
        "schedule": {
            "ordered_candidates_ascii": [item.decode("ascii") for item in candidates],
            "class6_episode_0": class6_component_ordinals(0),
            "class6_episode_11": class6_component_ordinals(11),
        },
        "minibatch": {
            "population_size": len(population),
            "first": population[0],
            "observational_end": population[64 * 128 - 1],
            "intervention_start": population[64 * 128],
            "last": population[-1],
            "draw_key_sha256": hashlib.sha256(minibatch_payload).hexdigest(),
            "selected": minibatch_selected,
        },
        "variance": {
            "space": CONTRACT["variance_head_space"],
            "direct_5_count": len(variance_head_paths("adjacent/5", 10)),
            "first_path_ascii": variance_head_paths("adjacent/5", 10)[0].decode("ascii"),
        },
        "optimizer": {
            "adam_step_1_f64": [f64_hex(value) for value in adam],
            "tied_restart": select_restart([1.0, 0.5, 0.5, 0.75, 2.0]),
        },
        "transcendentals": {
            "sqrt_2_f64": f64_hex(deterministic_sqrt(2.0)),
            "exp_1_f64": f64_hex(deterministic_exp(1.0)),
            "log_2_f64": f64_hex(deterministic_log(2.0)),
            "tanh_half_f64": f64_hex(deterministic_tanh(0.5)),
            "softplus_half_f64": f64_hex(deterministic_softplus(0.5)),
            "cdf_half_f64": f64_hex(gaussian_cdf(0.5)),
        },
        "decision_edges": {
            "class5_cdf_f64": f64_hex(class5_cdf([True, False], [True, True])),
            "label_shuffle_zero": label_shuffle_equivalence([0.0, -0.0]),
            "full_baseline_ascii": recovery_baseline_id("full", "direct/7").decode("ascii"),
            "cut_baseline_ascii": recovery_baseline_id("cut", "direct/7").decode("ascii"),
            "serial_reduction_f64": f64_hex(serial_sum([1e16, 1.0, -1e16])),
        },
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(pin_path: Path) -> dict[str, object]:
    pin = json.loads(pin_path.read_text(encoding="utf-8"))
    here = Path(__file__).resolve()
    vectors = test_vectors()
    vectors_path = pin_path.parent / pin["vectors_path"]
    stored_vectors = json.loads(vectors_path.read_text(encoding="utf-8"))
    if canonical_json(stored_vectors) != canonical_json(vectors):
        raise RuntimeError("stored replay vectors differ from executable output")
    observed = {
        "protocol_id": PROTOCOL_ID,
        "protocol_version": PROTOCOL_VERSION,
        "reference_sha256": file_sha256(here),
        "contract_sha256": hashlib.sha256(canonical_json(CONTRACT)).hexdigest(),
        "vectors_sha256": hashlib.sha256(canonical_json(vectors)).hexdigest(),
    }
    for key, value in observed.items():
        if pin.get(key) != value:
            raise RuntimeError(f"replay reference pin mismatch for {key}: {pin.get(key)!r} != {value!r}")
    return observed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("contract", "vectors", "verify"))
    parser.add_argument(
        "--pin",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "replay_reference.json",
    )
    args = parser.parse_args(argv)
    if args.command == "contract":
        output: object = CONTRACT
    elif args.command == "vectors":
        output = test_vectors()
    else:
        output = verify(args.pin)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
