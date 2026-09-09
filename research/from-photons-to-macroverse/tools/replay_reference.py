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
PROTOCOL_VERSION = "0.5.0"
DIRECT_ARITIES = (2, 3, 5, 6, 7, 8)
NESTED_ARITIES = DIRECT_ARITIES
NOISE_MILLI = (10, 50, 100)
NAMESPACE_SIGMA_MILLI = 10
TOKEN = re.compile(r"^[a-z0-9_./-]+$")
PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
)
OPEN_UNIT_MAX = float.fromhex("0x1.fffffffffffffp-1")

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

CANDIDATE_TYPES = {
    "state": ("token", "uint"),
    "edge": ("token", "token", "token"),
    "carrier": ("token",),
    "summand": ("token", "token", "token"),
    "recovery": ("token", "uint"),
}

INTERVENTION_TARGET_KINDS = {
    1: "state_target",
    2: "edge_target",
    3: "carrier_target",
    4: "summand_target",
    5: "recovery_target",
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
    "stability_probe_index": ["attempt", "probe_episode", "phase", "phase_time", "carrier_id", "coordinate"],
    "initializer_index": ["model_id", "restart", "tensor_name", "all_parameter_axes_in_row_major_order"],
    "initializer_values": "glorot_initializer_value and rho_initializer_value in this executable",
    "initializer_sigma_namespace": NAMESPACE_SIGMA_MILLI,
    "open_uniform_binary64_top": "0x1.fffffffffffffp-1 when exact rational conversion rounds to 1.0",
    "intervention_plan_role": "schedule",
    "resampling_outer_fields": {
        "seed": 0,
        "sigma_milli": NAMESPACE_SIGMA_MILLI,
        "role": "sealed_aggregate",
        "arity": "arity suffix in hypothesis_id; h_7 uses 7",
    },
    "candidate_types": CANDIDATE_TYPES,
    "candidate_registry": "canonical_candidate_lists in this executable",
    "model_partition_populations": {
        "arbitrary/<n>": "scalar-coordinate indices 0..2*n-1",
        "label-shuffle/<n>": "carrier indices 0..n-1",
        "arbitrary/tree/<n>": "leaf indices 0..sum(child_arities(n))-1",
        "label-shuffle/tree/<n>": "outer-carrier indices 0..n-1",
    },
    "backward_primitives": [
        "binary_multiply_adjoint",
        "binary_divide_adjoint",
        "serial_sum_adjoint",
        "serial_product_adjoint",
        "tanh_adjoint",
        "softplus_adjoint",
        "variance_head_value",
        "variance_head_adjoint",
        "gaussian_nll_term",
        "gaussian_nll_adjoint",
    ],
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


def open_uniform_word(word: int) -> float:
    """Map one uint64 word to the nearest admitted open binary64 value."""

    if isinstance(word, bool) or not isinstance(word, int) or not 0 <= word < 2**64:
        raise ValueError("word must be an unsigned 64-bit integer")
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        value = f64((Decimal(word) + Decimal("0.5")) / (Decimal(2) ** 64))
    return OPEN_UNIT_MAX if value >= 1.0 else value


def open_uniform(payload: bytes, lane: int = 0) -> float:
    if lane not in range(4):
        raise ValueError("lane must be 0..3")
    return open_uniform_word(digest_words(payload)[lane])


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


def deterministic_softplus_inverse(value: float) -> float:
    """Inverse softplus under the reference Decimal-to-binary64 contract."""

    if value <= 0:
        raise ValueError("softplus inverse input must be positive")
    with localcontext() as ctx:
        ctx.prec = 96
        ctx.rounding = ROUND_HALF_EVEN
        x = _decimal(value)
        return f64((x.exp() - Decimal(1)).ln())


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
        ("nested/", "wrong-tree/", "outer-cut/")
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
        sigma_milli=NAMESPACE_SIGMA_MILLI,
        domain="model_initializers",
        role="parameter",
        indices=[family_id, _uint(restart, "restart"), tensor_name, *axes],
    )


def glorot_initializer_value(
    *,
    seed: int,
    arity: int,
    family_id: str,
    restart: int,
    tensor_name: str,
    axes: Sequence[int],
    fan_in: int,
    fan_out: int,
) -> float:
    """Return one exact Glorot-uniform initialized matrix scalar."""

    if _uint(fan_in, "fan_in") == 0 or _uint(fan_out, "fan_out") == 0:
        raise ValueError("Glorot fan sizes must be positive")
    payload = initializer_key(
        seed=seed,
        arity=arity,
        family_id=family_id,
        restart=restart,
        tensor_name=tensor_name,
        axes=axes,
    )
    bound = deterministic_sqrt(fdiv(6.0, fadd(fan_in, fan_out)))
    centered = fsub(fmul(2.0, open_uniform(payload)), 1.0)
    return fmul(centered, bound)


def rho_initializer_value(sigma_milli: int) -> float:
    """Return the exact raw diagonal-variance initializer for one noise level."""

    if sigma_milli not in NOISE_MILLI:
        raise ValueError("sigma_milli must be 10, 50, or 100")
    sigma = fdiv(sigma_milli, 1000)
    target = max(fsub(fmul(sigma, sigma), 1e-6), 1e-12)
    return deterministic_softplus_inverse(target)


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


def stability_probe_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    system_kind: str,
    attempt: int,
    probe_ordinal: int,
    phase: str,
    phase_time: int,
    carrier_id: str,
    coordinate: int,
    outer: int | None = None,
) -> bytes:
    """Emit one complete stability initial-state or noise scalar key."""

    if not 0 <= probe_ordinal < 16:
        raise ValueError("probe_ordinal must be 0..15")
    if phase == "initial":
        if phase_time != 0:
            raise ValueError("stability initial state exists only at time 0")
    elif phase == "noise":
        if not 0 <= phase_time <= 31:
            raise ValueError("stability noise time must be 0..31")
    else:
        raise ValueError("stability phase must be initial or noise")
    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="stability_probe",
        role=coefficient_role(system_kind, attempt, outer),
        indices=[attempt, f"stability/{probe_ordinal:02d}", phase, phase_time, carrier_id, coordinate],
    )


def initial_state_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    system_kind: str,
    attempt: int,
    episode_id: str,
    carrier_id: str,
    coordinate: int,
    outer: int | None = None,
) -> bytes:
    """Emit one complete accepted-generator episode initial-state key."""

    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="initial_state",
        role=coefficient_role(system_kind, attempt, outer),
        indices=[episode_id, carrier_id, coordinate],
    )


def hypothesis_id(kind: str, arity: int | None = None) -> str:
    if kind == "h_7" and arity is None:
        return "h_7"
    if kind in {"h_a", "h_r"} and arity in DIRECT_ARITIES:
        result = f"{kind}/{arity}"
        if result in HYPOTHESIS_IDS:
            return result
    raise ValueError("hypothesis has no canonical identifier")


def _hypothesis_arity(canonical_hypothesis_id: str) -> int:
    if canonical_hypothesis_id == "h_7":
        return 7
    try:
        kind, arity_text = canonical_hypothesis_id.split("/", 1)
        arity = int(arity_text)
    except (ValueError, TypeError):
        raise ValueError("hypothesis has no canonical arity") from None
    if hypothesis_id(kind, arity) != canonical_hypothesis_id:
        raise ValueError("hypothesis has no canonical arity")
    return arity


def bootstrap_key(
    canonical_hypothesis_id: str,
    bootstrap_index: int,
    draw_index: int,
) -> bytes:
    """Emit one sealed-aggregate bootstrap draw key."""

    if not 0 <= bootstrap_index < 65536 or not 0 <= draw_index < 32:
        raise ValueError("bootstrap indices are outside the frozen range")
    return stream_bytes(
        seed=0,
        arity=_hypothesis_arity(canonical_hypothesis_id),
        sigma_milli=NAMESPACE_SIGMA_MILLI,
        domain="bootstrap",
        role="sealed_aggregate",
        indices=[canonical_hypothesis_id, bootstrap_index, draw_index],
    )


def permutation_key(
    canonical_hypothesis_id: str,
    permutation_index: int,
    sealed_seed_index: int,
) -> bytes:
    """Emit one sealed-aggregate sign-permutation key."""

    if not 0 <= permutation_index < 65536 or not 0 <= sealed_seed_index < 32:
        raise ValueError("permutation indices are outside the frozen range")
    return stream_bytes(
        seed=0,
        arity=_hypothesis_arity(canonical_hypothesis_id),
        sigma_milli=NAMESPACE_SIGMA_MILLI,
        domain="permutation",
        role="sealed_aggregate",
        indices=[canonical_hypothesis_id, permutation_index, sealed_seed_index],
    )


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


def _candidate_payload(kind: str, *identity: str | int) -> bytes:
    field_types = CANDIDATE_TYPES.get(kind)
    if field_types is None or len(identity) != len(field_types):
        raise ValueError("candidate identity does not match its frozen shape")
    if kind == "summand" and identity[0] not in {"w", "product"}:
        raise ValueError("summand kind must be w or product")
    normalized: list[str | int] = []
    for position, (value, field_type) in enumerate(zip(identity, field_types)):
        if field_type == "token" and isinstance(value, str):
            normalized.append(_token(value, f"candidate[{position}]"))
        elif field_type == "uint" and isinstance(value, int) and not isinstance(value, bool):
            normalized.append(_uint(value, f"candidate[{position}]"))
        else:
            raise ValueError(f"candidate[{position}] must be a {field_type}")
    return canonical_json([kind, *normalized])


def ordered_candidates(candidates: Iterable[bytes]) -> tuple[bytes, ...]:
    result = tuple(sorted(candidates))
    if len(result) != len(set(result)):
        raise ValueError("schedule candidates must be unique")
    return result


def child_arities(arity: int) -> tuple[int, ...]:
    """Return the sole admitted depth-two child-arity vector."""

    if arity not in NESTED_ARITIES:
        raise ValueError("nested arity is not admitted")
    pattern = (2, 3, 5)
    return tuple(pattern[index % len(pattern)] for index in range(arity))


def canonical_candidate_lists(
    system_kind: str,
    arity: int,
) -> dict[str, tuple[bytes, ...]]:
    """Enumerate every target identity admitted for one generator."""

    if arity not in DIRECT_ARITIES:
        raise ValueError("candidate arity is not admitted")
    if system_kind == "direct":
        observed = tuple(f"carrier/{index}" for index in range(arity))
        carriers = observed
        edges = tuple(
            ("w", target, source)
            for target in carriers
            for source in carriers
            if source != target
        )
        product_targets = carriers
    elif system_kind == "nested":
        carriers = tuple(f"outer/{index}" for index in range(arity))
        observed = tuple(
            f"outer/{outer}/leaf/{leaf}"
            for outer, child_arity in enumerate(child_arities(arity))
            for leaf in range(child_arity)
        )
        leaf_edges = tuple(
            (
                "w",
                f"outer/{outer}/leaf/{target}",
                f"outer/{outer}/leaf/{source}",
            )
            for outer, child_arity in enumerate(child_arities(arity))
            for target in range(child_arity)
            for source in range(child_arity)
            if source != target
        )
        outer_edges = tuple(
            ("w", target, source)
            for target in carriers
            for source in carriers
            if source != target
        )
        edges = (*leaf_edges, *outer_edges)
        product_targets = (*observed, *carriers)
    else:
        raise ValueError("system_kind must be direct or nested")
    result = {
        "state": tuple(
            _candidate_payload("state", target, coordinate)
            for target in observed
            for coordinate in range(2)
        ),
        "edge": tuple(_candidate_payload("edge", *edge) for edge in edges),
        "carrier": tuple(
            _candidate_payload("carrier", carrier) for carrier in carriers
        ),
        "summand": (
            *tuple(_candidate_payload("summand", *edge) for edge in edges),
            *tuple(
                _candidate_payload("summand", "product", target, "none")
                for target in product_targets
            ),
        ),
        "recovery": tuple(
            _candidate_payload("recovery", target, coordinate)
            for target in observed
            for coordinate in range(2)
        ),
    }
    return {kind: ordered_candidates(items) for kind, items in result.items()}


def candidate_bytes(
    system_kind: str,
    arity: int,
    kind: str,
    *identity: str | int,
) -> bytes:
    """Return one candidate only when it belongs to the complete registry."""

    payload = _candidate_payload(kind, *identity)
    if payload not in canonical_candidate_lists(system_kind, arity).get(kind, ()):
        raise ValueError("candidate identity is outside the canonical registry")
    return payload


def intervention_target_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    split: str,
    system_kind: str,
    intervention_class: int,
    candidate_index: int,
    block: int = 0,
) -> bytes:
    """Emit a target-ranking key with the one admitted schedule role."""

    if split not in {"train", "cal", "test"}:
        raise ValueError("intervention split must be train, cal, or test")
    choice_kind = INTERVENTION_TARGET_KINDS.get(intervention_class)
    if choice_kind is None:
        raise ValueError("target intervention class must be 1..5")
    candidate_kind = {
        1: "state",
        2: "edge",
        3: "carrier",
        4: "summand",
        5: "recovery",
    }[intervention_class]
    candidate_count = len(canonical_candidate_lists(system_kind, arity)[candidate_kind])
    if not 0 <= candidate_index < candidate_count:
        raise ValueError("candidate_index is outside the canonical target list")
    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="intervention_plan",
        role="schedule",
        indices=[f"schedule/{split}/{choice_kind}", intervention_class, candidate_index],
        block=block,
    )


def intervention_start_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    episode_id: str,
    intervention_class: int,
) -> bytes:
    """Emit a start-time key for class 1..4 or composed class 6."""

    if intervention_class not in {1, 2, 3, 4, 6}:
        raise ValueError("start-time intervention class must be 1..4 or 6")
    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="intervention_plan",
        role="schedule",
        indices=[episode_id, intervention_class, "start_time"],
    )


def model_partition_key(
    *,
    seed: int,
    arity: int,
    sigma_milli: int,
    family_id: str,
    candidate_index: int,
    block: int = 0,
) -> bytes:
    """Emit one model-partition ranking key."""

    _token(family_id, "family_id")
    population_size = model_partition_population_size(family_id, arity)
    if not 0 <= candidate_index < population_size:
        raise ValueError("model partition candidate is outside its frozen population")
    return stream_bytes(
        seed=seed,
        arity=arity,
        sigma_milli=sigma_milli,
        domain="intervention_plan",
        role=f"model_partition/{family_id}",
        indices=["schedule/model_partition", 0, candidate_index],
        block=block,
    )


def model_partition_population_size(family_id: str, arity: int) -> int:
    """Return the exact permutation population for one admitted family."""

    if arity not in DIRECT_ARITIES:
        raise ValueError("model partition arity is not admitted")
    if family_id == f"arbitrary/{arity}":
        return 2 * arity
    if family_id == f"label-shuffle/{arity}":
        return arity
    if family_id == f"arbitrary/tree/{arity}":
        return sum(child_arities(arity))
    if family_id == f"label-shuffle/tree/{arity}":
        return arity
    raise ValueError("family has no sealed model-partition permutation")


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


def binary_multiply_adjoint(
    left: float,
    right: float,
    upstream: float,
) -> tuple[float, float]:
    """Reverse one ``fmul(left, right)`` in operand order."""

    return fmul(upstream, right), fmul(upstream, left)


def binary_divide_adjoint(
    numerator: float,
    denominator: float,
    upstream: float,
) -> tuple[float, float]:
    """Reverse one ``fdiv(numerator, denominator)`` without reassociation."""

    numerator_adjoint = fdiv(upstream, denominator)
    denominator_squared = fmul(denominator, denominator)
    negative_numerator = fsub(0.0, numerator)
    denominator_adjoint = fmul(
        upstream,
        fdiv(negative_numerator, denominator_squared),
    )
    return numerator_adjoint, denominator_adjoint


def serial_sum_adjoint(length: int, upstream: float) -> tuple[float, ...]:
    """Reverse a serial sum; each ordered input receives the same adjoint."""

    _uint(length, "length")
    return tuple(f64(upstream) for _ in range(length))


def serial_product_adjoint(
    factors: Sequence[float],
    upstream: float,
) -> tuple[float, ...]:
    """Reverse the exact serial left-fold product recurrence."""

    prefixes = [1.0]
    for factor in factors:
        prefixes.append(fmul(prefixes[-1], factor))
    running = f64(upstream)
    gradients = [0.0] * len(factors)
    for index in range(len(factors) - 1, -1, -1):
        gradients[index] = fmul(running, prefixes[index])
        running = fmul(running, factors[index])
    return tuple(gradients)


def tanh_adjoint(value: float, upstream: float) -> float:
    """Reverse the executable tanh using one frozen local recurrence."""

    output = deterministic_tanh(value)
    local = fsub(1.0, fmul(output, output))
    return fmul(upstream, local)


def softplus_adjoint(value: float, upstream: float) -> float:
    """Reverse the executable softplus branch with stable sigmoid arithmetic."""

    if value > 40.0:
        local = 1.0
    elif value >= 0.0:
        local = fdiv(1.0, fadd(1.0, deterministic_exp(fsub(0.0, value))))
    else:
        exponential = deterministic_exp(value)
        local = fdiv(exponential, fadd(1.0, exponential))
    return fmul(upstream, local)


def variance_head_value(raw_rho: float) -> float:
    """Decode one variance head scalar in the sole admitted operation order."""

    return fadd(deterministic_softplus(raw_rho), 1e-6)


def variance_head_adjoint(raw_rho: float, upstream: float) -> float:
    """Reverse the variance-head softplus; the additive floor passes through."""

    return softplus_adjoint(raw_rho, upstream)


def gaussian_nll_term(observed: float, mean: float, variance: float) -> float:
    """Evaluate one diagonal-Gaussian NLL scalar in the sole operation order."""

    if not math.isfinite(variance) or variance < 1e-6:
        raise ValueError("variance must be finite and at least 1e-6")
    residual = fsub(observed, mean)
    squared = fmul(residual, residual)
    scaled_error = fdiv(squared, variance)
    two_pi = fmul(2.0, f64(PI))
    scaled_variance = fmul(two_pi, variance)
    log_term = deterministic_log(scaled_variance)
    return fmul(0.5, fadd(scaled_error, log_term))


def gaussian_nll_adjoint(
    observed: float,
    mean: float,
    variance: float,
    upstream: float,
) -> tuple[float, float, float]:
    """Reverse ``gaussian_nll_term`` without algebraic reassociation."""

    gaussian_nll_term(observed, mean, variance)
    residual = fsub(observed, mean)
    squared = fmul(residual, residual)
    two_pi = fmul(2.0, f64(PI))
    scaled_variance = fmul(two_pi, variance)
    summed_adjoint = fmul(upstream, 0.5)
    squared_adjoint = fdiv(summed_adjoint, variance)
    negative_squared = fsub(0.0, squared)
    variance_squared = fmul(variance, variance)
    variance_from_error = fmul(
        summed_adjoint,
        fdiv(negative_squared, variance_squared),
    )
    scaled_variance_adjoint = fdiv(summed_adjoint, scaled_variance)
    variance_from_log = fmul(scaled_variance_adjoint, two_pi)
    variance_adjoint = fadd(variance_from_error, variance_from_log)
    residual_adjoint = fadd(
        fmul(squared_adjoint, residual),
        fmul(squared_adjoint, residual),
    )
    observed_adjoint = residual_adjoint
    mean_adjoint = fsub(0.0, residual_adjoint)
    return observed_adjoint, mean_adjoint, variance_adjoint


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
        seed=32, arity=7, family_id="direct/7", restart=0,
        tensor_name="w", axes=[3, 5, 1, 0]
    )
    initializer_b = initializer_key(
        seed=32, arity=7, family_id="direct/7", restart=0,
        tensor_name="w", axes=[4, 5, 1, 0]
    )
    glorot_value = glorot_initializer_value(
        seed=32, arity=7, family_id="direct/7", restart=0,
        tensor_name="w", axes=[3, 5, 1, 0], fan_in=2, fan_out=2
    )
    probe_initial = stability_probe_key(
        seed=32, arity=7, sigma_milli=50, system_kind="direct", attempt=0,
        probe_ordinal=0, phase="initial", phase_time=0, carrier_id="3", coordinate=1
    )
    probe_noise = stability_probe_key(
        seed=32, arity=7, sigma_milli=50, system_kind="direct", attempt=0,
        probe_ordinal=0, phase="noise", phase_time=0, carrier_id="3", coordinate=1
    )
    episode_initial = initial_state_key(
        seed=32, arity=7, sigma_milli=50, system_kind="direct", attempt=0,
        episode_id="obs/test/000", carrier_id="3", coordinate=1
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
    direct_candidates = canonical_candidate_lists("direct", 7)
    nested_candidates = canonical_candidate_lists("nested", 7)
    state_candidate = candidate_bytes("direct", 7, "state", "carrier/0", 0)
    target_key = intervention_target_key(
        seed=32, arity=7, sigma_milli=50, split="test", system_kind="direct",
        intervention_class=1, candidate_index=0
    )
    start_key = intervention_start_key(
        seed=32, arity=7, sigma_milli=50,
        episode_id="int/1/test/000", intervention_class=1
    )
    partition_key = model_partition_key(
        seed=32, arity=7, sigma_milli=50,
        family_id="arbitrary/7", candidate_index=0
    )
    partition_last_scalar = model_partition_key(
        seed=32, arity=7, sigma_milli=50,
        family_id="arbitrary/7", candidate_index=13
    )
    partition_last_leaf = model_partition_key(
        seed=32, arity=7, sigma_milli=50,
        family_id="arbitrary/tree/7", candidate_index=21
    )
    bootstrap = bootstrap_key("h_7", 0, 0)
    permutation = permutation_key("h_7", 0, 0)
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
            "minimum_open_uniform_f64": f64_hex(open_uniform_word(0)),
            "maximum_open_uniform_f64": f64_hex(open_uniform_word(2**64 - 1)),
        },
        "initializer": {
            "complete_path_ascii": initializer_a.decode("ascii"),
            "complete_path_sha256": hashlib.sha256(initializer_a).hexdigest(),
            "different_carrier_sha256": hashlib.sha256(initializer_b).hexdigest(),
            "distinct": initializer_a != initializer_b,
            "glorot_f64": f64_hex(glorot_value),
            "rho_sigma_050_f64": f64_hex(rho_initializer_value(50)),
            "unnested_kind": family_kind("unnested/7"),
        },
        "stability_probe": {
            "initial_ascii": probe_initial.decode("ascii"),
            "noise_ascii": probe_noise.decode("ascii"),
            "distinct": probe_initial != probe_noise,
        },
        "initial_state": {"episode_ascii": episode_initial.decode("ascii")},
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
            "state_candidate_ascii": state_candidate.decode("ascii"),
            "class6_episode_0": class6_component_ordinals(0),
            "class6_episode_11": class6_component_ordinals(11),
            "target_key_ascii": target_key.decode("ascii"),
            "start_key_ascii": start_key.decode("ascii"),
            "partition_key_ascii": partition_key.decode("ascii"),
            "partition_last_scalar_ascii": partition_last_scalar.decode("ascii"),
            "partition_last_leaf_ascii": partition_last_leaf.decode("ascii"),
        },
        "candidate_registry": {
            system_kind: {
                kind: {
                    "count": len(items),
                    "sha256": hashlib.sha256(
                        canonical_json([item.decode("ascii") for item in items])
                    ).hexdigest(),
                }
                for kind, items in candidate_lists.items()
            }
            for system_kind, candidate_lists in (
                ("direct", direct_candidates),
                ("nested", nested_candidates),
            )
        },
        "adjoints": {
            "binary_multiply_f64": [
                f64_hex(value)
                for value in binary_multiply_adjoint(0.25, -0.5, 1.25)
            ],
            "binary_divide_f64": [
                f64_hex(value)
                for value in binary_divide_adjoint(0.25, -0.5, 1.25)
            ],
            "serial_sum_f64": [
                f64_hex(value) for value in serial_sum_adjoint(3, 1.25)
            ],
            "serial_product_f64": [
                f64_hex(value)
                for value in serial_product_adjoint([0.25, -0.5, 0.75], 1.25)
            ],
            "tanh_f64": f64_hex(tanh_adjoint(0.5, 1.25)),
            "softplus_f64": f64_hex(softplus_adjoint(-0.5, 1.25)),
            "variance_value_f64": f64_hex(variance_head_value(-0.5)),
            "variance_adjoint_f64": f64_hex(
                variance_head_adjoint(-0.5, 1.25)
            ),
            "nll_term_f64": f64_hex(gaussian_nll_term(0.75, 0.25, 0.5)),
            "nll_adjoint_f64": [
                f64_hex(value)
                for value in gaussian_nll_adjoint(0.75, 0.25, 0.5, 1.25)
            ],
        },
        "resampling": {
            "bootstrap_ascii": bootstrap.decode("ascii"),
            "permutation_ascii": permutation.decode("ascii"),
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
    declared_path = pin.get("reference_path")
    if not isinstance(declared_path, str) or Path(declared_path).is_absolute():
        raise RuntimeError("reference_path must be one relative path")
    if (pin_path.parent / declared_path).resolve() != here:
        raise RuntimeError("reference_path does not resolve to this executable")
    if pin.get("verification_command") != f"python {declared_path} verify":
        raise RuntimeError("verification_command does not invoke the pinned executable")
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
