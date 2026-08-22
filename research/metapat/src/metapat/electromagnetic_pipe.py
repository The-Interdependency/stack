"""Catalog-bound three-phase nested electromagnetic-pipe engineering record."""

# === MODULE_BUILD ===
# id: metapat_electromagnetic_pipe_application
#   module_name: metapat.electromagnetic_pipe
#   module_kind: schema
#   summary: preserves the three-phase nested electromagnetic-pipe handoff as a strict catalog-bound engineering application and design record without claiming device performance
#   owner: The Interdependency
#   public_surface: pipe application and design schema constants, WindingLayerSpec, AlloyCandidate, ElectromagneticPipeDesign, electromagnetic_pipe_application_module, electromagnetic_pipe_design, electromagnetic_pipe_design_digest
#   internal_surface: source declarations, binding specifications, canonical JSON and digest helpers
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: public engineering handoff and provenance only
#   admin_only: false
#   tests: tests.test_electromagnetic_pipe
#   rollout: public package exports and deterministic fixture in metapat 0.7.0
#   rollback: remove electromagnetic-pipe exports and fixture while preserving the generic application schema and semantic catalog
#   requires: metapat_application_module_schema, metapat_semantic_catalog
#   since: 2026-07-21
#   unresolved: frequency, current, target field, shielding, phase shift, attractor geometry, thermal limits, protection distance, and alloy performance remain empirical frontiers
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_electromagnetic_pipe_docs
#   summary: preserves geometry, six-vector control topology, mobile-attractor distinction, alloy search, instrumentation, fault objectives, and empirical boundaries
#   audience: developer, electrical engineer, materials engineer, safety reviewer, agent
#   source: docs/applications/three-phase-electromagnetic-pipe.md
#   covers: electromagnetic_pipe_application_module, electromagnetic_pipe_design, catalog bindings, source integrity, engineering evidence boundary
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_electromagnetic_pipe_fixture
#   summary: emits one deterministic catalog-bound engineering application and typed device-design record for the nested three-phase pipe system
#   exposes: metapat.electromagnetic_pipe_design
#   inputs: canonical semantic catalog v2
#   outputs: strict engineering application, typed topology and material-search record, deterministic digest
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:public engineering handoff only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_electromagnetic_pipe_boundary
#   summary: engineering proposal and optimization structure only; no electromagnetic, materials, insulation, thermal, fault, spacecraft, measurement, UCNS topology, or theorem-status validity claim
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: public engineering handoff only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_pipe_control_topology_exact
#   given: the electromagnetic-pipe design record is constructed
#   then: three radial layers, two handednesses, three phases per handedness, eighteen phase circuits, and six three-phase control systems remain exact and internally reconciled
#   class: schema_contract
#
# id: metapat_pipe_winding_layers_exact
#   given: the winding layers are inspected
#   then: outer 12 AWG at 6 turns per inch, middle 16 AWG at 12, and inner 20 AWG at 18 remain ordered and exact
#   class: provenance_contract
#
# id: metapat_pipe_attractors_not_bearings
#   given: the mobile-element fields are inspected
#   then: the objects remain ceramic-coated magnetic eddy-current attractors and are never typed as bearings
#   class: boundary_contract
#
# id: metapat_pipe_alloy_search_bounded
#   given: the alloy candidates are inspected
#   then: every candidate is atomic percent, totals 100, preserves Fe plus Co plus Ni at 75, Cr at 15, Mn at 10, and remains a search candidate rather than an ideal-alloy claim
#   class: materials_boundary
#
# id: metapat_pipe_application_catalog_bound
#   given: the pipe application is constructed
#   then: every METAPAT use is bound to an exact catalog module identity, digest, and claim status
#   class: integration_contract
#
# id: metapat_pipe_source_current
#   given: the constructor and handoff source are checked together
#   then: control topology, geometry, winding, attractor, alloy, instrumentation, fault, high-voltage, next-work, evidence, and hmmm statements remain source-current
#   class: provenance_contract
#
# id: metapat_pipe_performance_firewall
#   given: the design record and application are inspected
#   then: electromagnetic, materials, insulation, thermal, mechanical, spacecraft, measurement, topology, theorem-transfer, and METAPAT validity claims remain false
#   class: boundary_contract
#
# id: metapat_pipe_roundtrip_strict
#   given: a valid design record is serialized and reconstructed
#   then: every nested field and digest survive while unknown, missing, malformed, or tampered fields fail closed
#   class: schema_contract
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

from .application import MetapatApplicationModule, bind_catalog_module, validate_application_against_catalog
from .catalog import MetapatSemanticCatalog, canonical_semantic_catalog, semantic_module_by_id

PIPE_APPLICATION_VERSION = "three-phase-electromagnetic-pipe-application-v2"
PIPE_DESIGN_SCHEMA_ID = "metapat.electromagnetic-pipe-design"
PIPE_DESIGN_SCHEMA_VERSION = "1.0.0"
WINDING_LAYER_SCHEMA_ID = "metapat.electromagnetic-pipe-winding-layer"
WINDING_LAYER_SCHEMA_VERSION = "1.0.0"
ALLOY_CANDIDATE_SCHEMA_ID = "metapat.electromagnetic-pipe-alloy-candidate"
ALLOY_CANDIDATE_SCHEMA_VERSION = "1.0.0"
SOURCE_DOCUMENT = "docs/applications/three-phase-electromagnetic-pipe.md"


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _integer(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _number(value: Any, name: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if result < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return result


def _strings(value: Any, name: str, *, minimum: int = 0) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be an array of strings")
    result = tuple(value)
    if len(result) < minimum or any(not isinstance(item, str) or not item.strip() for item in result):
        raise ValueError(f"{name} must contain at least {minimum} non-empty strings")
    return result


def _false(value: Any, name: str) -> bool:
    if value is not False:
        raise ValueError(f"{name} must remain false")
    return False


def _hex(value: Any, name: str) -> str:
    text = _text(value, name).lower()
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise ValueError(f"{name} must be a lowercase hexadecimal SHA-256 digest")
    return text


@dataclass(frozen=True, slots=True)
class WindingLayerSpec:
    layer_name: str
    radial_order: int
    wire_awg: int
    turns_per_inch: int
    clockwise_phase_count: int = 3
    widdershins_phase_count: int = 3
    schema_id: str = WINDING_LAYER_SCHEMA_ID
    schema_version: str = WINDING_LAYER_SCHEMA_VERSION
    layer_digest: str = ""

    def __post_init__(self) -> None:
        if self.layer_name not in {"outer", "middle", "inner"}:
            raise ValueError("layer_name must be outer, middle, or inner")
        _integer(self.radial_order, "radial_order", minimum=1)
        _integer(self.wire_awg, "wire_awg", minimum=1)
        _integer(self.turns_per_inch, "turns_per_inch", minimum=1)
        if self.clockwise_phase_count != 3 or self.widdershins_phase_count != 3:
            raise ValueError("each layer must contain three clockwise and three widdershins phases")
        if self.schema_id != WINDING_LAYER_SCHEMA_ID or self.schema_version != WINDING_LAYER_SCHEMA_VERSION:
            raise ValueError("unsupported winding-layer schema")
        expected = _digest(self._payload())
        if self.layer_digest and self.layer_digest != expected:
            raise ValueError("layer_digest mismatch")
        object.__setattr__(self, "layer_digest", expected)

    @property
    def phase_circuit_count(self) -> int:
        return self.clockwise_phase_count + self.widdershins_phase_count

    @property
    def three_phase_system_count(self) -> int:
        return 2

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "layer_name": self.layer_name,
            "radial_order": self.radial_order,
            "wire_awg": self.wire_awg,
            "turns_per_inch": self.turns_per_inch,
            "clockwise_phase_count": self.clockwise_phase_count,
            "widdershins_phase_count": self.widdershins_phase_count,
            "phase_circuit_count": self.phase_circuit_count,
            "three_phase_system_count": self.three_phase_system_count,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "layer_digest": self.layer_digest}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WindingLayerSpec":
        expected = {
            "schema_id", "schema_version", "layer_name", "radial_order", "wire_awg",
            "turns_per_inch", "clockwise_phase_count", "widdershins_phase_count",
            "phase_circuit_count", "three_phase_system_count", "layer_digest",
        }
        if not isinstance(data, Mapping):
            raise ValueError("winding layer must be a mapping")
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown or missing:
            raise ValueError(f"invalid winding-layer fields: unknown={sorted(unknown)!r}, missing={sorted(missing)!r}")
        result = cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            layer_name=_text(data["layer_name"], "layer_name"),
            radial_order=_integer(data["radial_order"], "radial_order", minimum=1),
            wire_awg=_integer(data["wire_awg"], "wire_awg", minimum=1),
            turns_per_inch=_integer(data["turns_per_inch"], "turns_per_inch", minimum=1),
            clockwise_phase_count=_integer(data["clockwise_phase_count"], "clockwise_phase_count", minimum=1),
            widdershins_phase_count=_integer(data["widdershins_phase_count"], "widdershins_phase_count", minimum=1),
            layer_digest=_hex(data["layer_digest"], "layer_digest"),
        )
        if data["phase_circuit_count"] != result.phase_circuit_count:
            raise ValueError("phase_circuit_count mismatch")
        if data["three_phase_system_count"] != result.three_phase_system_count:
            raise ValueError("three_phase_system_count mismatch")
        return result


@dataclass(frozen=True, slots=True)
class AlloyCandidate:
    label: str
    iron: float
    cobalt: float
    nickel: float
    chromium: float
    manganese: float
    basis: str = "atomic percent"
    schema_id: str = ALLOY_CANDIDATE_SCHEMA_ID
    schema_version: str = ALLOY_CANDIDATE_SCHEMA_VERSION
    candidate_digest: str = ""

    def __post_init__(self) -> None:
        _text(self.label, "label")
        values = {
            "iron": _number(self.iron, "iron"),
            "cobalt": _number(self.cobalt, "cobalt"),
            "nickel": _number(self.nickel, "nickel"),
            "chromium": _number(self.chromium, "chromium"),
            "manganese": _number(self.manganese, "manganese"),
        }
        for name, value in values.items():
            object.__setattr__(self, name, value)
        if self.basis != "atomic percent":
            raise ValueError("alloy basis must remain atomic percent")
        if round(sum(values.values()), 8) != 100.0:
            raise ValueError("alloy composition must total 100 atomic percent")
        if round(values["iron"] + values["cobalt"] + values["nickel"], 8) != 75.0:
            raise ValueError("Fe + Co + Ni must equal 75 atomic percent")
        if values["chromium"] != 15.0 or values["manganese"] != 10.0:
            raise ValueError("Cr must equal 15 and Mn must equal 10 atomic percent")
        if self.schema_id != ALLOY_CANDIDATE_SCHEMA_ID or self.schema_version != ALLOY_CANDIDATE_SCHEMA_VERSION:
            raise ValueError("unsupported alloy-candidate schema")
        expected = _digest(self._payload())
        if self.candidate_digest and self.candidate_digest != expected:
            raise ValueError("candidate_digest mismatch")
        object.__setattr__(self, "candidate_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "label": self.label,
            "iron": self.iron,
            "cobalt": self.cobalt,
            "nickel": self.nickel,
            "chromium": self.chromium,
            "manganese": self.manganese,
            "basis": self.basis,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "candidate_digest": self.candidate_digest}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AlloyCandidate":
        expected = {
            "schema_id", "schema_version", "label", "iron", "cobalt", "nickel",
            "chromium", "manganese", "basis", "candidate_digest",
        }
        if not isinstance(data, Mapping):
            raise ValueError("alloy candidate must be a mapping")
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown or missing:
            raise ValueError(f"invalid alloy-candidate fields: unknown={sorted(unknown)!r}, missing={sorted(missing)!r}")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            label=_text(data["label"], "label"),
            iron=_number(data["iron"], "iron"),
            cobalt=_number(data["cobalt"], "cobalt"),
            nickel=_number(data["nickel"], "nickel"),
            chromium=_number(data["chromium"], "chromium"),
            manganese=_number(data["manganese"], "manganese"),
            basis=_text(data["basis"], "basis"),
            candidate_digest=_hex(data["candidate_digest"], "candidate_digest"),
        )


PIPE_BINDING_SPECS = (
    ("metapat.axiom.0.root_untouchable", "domain-restraint", "METAPAT organizes the question and does not replace electromagnetic, materials, thermal, insulation, or spacecraft evidence."),
    ("metapat.axiom.1.legible_difference", "distinction", "Every phase circuit, handedness, radial layer, iron pipe, ceramic boundary, attractor, gap, and field state remains separately legible."),
    ("metapat.axiom.2.boundary", "boundary-simplex", "Ceramic shells, iron pipes, gaps, winding geometry, end geometry, and attractor constraints alter passage, delay, filtering, phase, direction, and transformation."),
    ("metapat.axiom.4.tensor", "control-tensor", "The simultaneous arrangement contains six three-phase vectors, direct-current biases, frequency, current limits, voltage compliance, winding handedness, radial layer, attractor positions, alloy state, temperature, magnetic history, and mechanical gaps."),
    ("metapat.axiom.5.energy_state", "energy-state", "Phase-current, magnetic-field, magnetization, motion, eddy-current, and thermal conditions are distinct energy-state surfaces."),
    ("metapat.axiom.6.relation", "relation", "Layer, handedness, phase order, spatial displacement, pipe geometry, attractor position, and material state configure which transformations are possible."),
    ("metapat.axiom.7.gradient", "gradient", "Readable differences include field amplitude, field phase, position, temperature, magnetization, force, leakage, and shielding response."),
    ("metapat.axiom.8.transformation", "feedback-transformation", "Current changes field; field changes attractor magnetization and motion; attractor redistribution changes the boundary and therefore the next field cycle."),
    ("metapat.axiom.9.time", "sequential-field-state", "Alternating phase progression, settling, hysteresis, magnetic history, and fault evolution are sequential tensor alterations."),
    ("metapat.axiom.10.registration", "instrumentation", "Registration measures electrical, magnetic, thermal, mechanical, distribution, hysteresis, settling, and leakage states."),
    ("metapat.axiom.11.question", "unresolved-design-state", "Frequency, current, target field, shielding, phase shift, attractor geometry, temperature, and protection distance remain bounded unresolved states."),
    ("metapat.postulate.2.explicationary_use", "engineering-restraint", "METAPAT vocabulary clarifies the device but does not replace Maxwell-field simulation, circuit models, materials measurements, or qualification tests."),
    ("metapat.postulate.6.validation_by_boundary_change", "boundary-test", "A claimed boundary effect must be tested by changing boundary state while holding declared source and target conditions as constant as practicable."),
    ("metapat.theorem.1.boundary_earns_its_keep", "boundary-evidence", "Ceramic, iron, gap, end-return, and attractor boundaries earn model force only when their controlled change alters measured direction, delay, filtering, propagation, shielding, or transformation."),
    ("metapat.theory.2.boundary_mediated_transformation", "boundary-mediated-transformation", "Mobile attractor redistribution is treated as a changing boundary state that may alter shielding amplitude, phase delay, loss, and force gradients."),
    ("metapat.theory.5.relational_gradient_selection", "force-selection", "Direction and motion are asked through the full relation among phase order, winding displacement, pipe state, attractor state, and magnetic gradient rather than field difference alone."),
    ("metapat.theory.6.time_as_sequential_tensor_alteration", "cycle-history", "Phase progression, hysteresis, settling, and thermal accumulation are distinct sequential alterations rather than mere timestamps."),
    ("metapat.theory.7.registration_and_observer_roles", "sensor-registration", "Sensors and logs earn observer role only by preserving, expressing, or transmitting the relevant sequence."),
    ("metapat.theory.8.questions_as_bounded_unresolved_energy_state", "optimization-question", "Each unresolved operating bound is retained as a named question rather than silently guessed into the design."),
    ("metapat.theory.11.cross_domain_question_forms", "cross-domain-question-form", "Electromagnetics, power electronics, magnetic materials, thermal behavior, mechanics, insulation, and spacecraft integration may share a question-form without becoming one domain."),
)

DOMAINS = (
    "electromagnetics", "power electronics", "magnetic materials",
    "thermal engineering", "mechanical dynamics",
    "vacuum high-voltage insulation", "spacecraft systems",
)
SELECTED_SCALES = (
    "phase-circuit", "three-phase-vector", "winding-layer", "pipe-boundary",
    "mobile-attractor", "three-meter-assembly", "spacecraft-environment",
)
DOMAIN_STATEMENTS = (
    "The natural control object is one three-phase vector per handedness per radial layer.",
    "The system contains eighteen phase circuits naturally organized as six independently isolatable three-phase systems.",
    "The drives are current-controlled; voltage is compliance rather than the magnetic command variable.",
    "The internal objects are ceramic-coated magnetic eddy-current attractors, not bearings.",
    "Copper remains solid during normal operation and molten copper containment is only a catastrophic-overheating fault objective.",
    "The ideal alloy remains a composition-search problem rather than a selected formula until operating and measurement bounds are registered.",
)
SHARED_QUESTION_FORM = (
    "current tensor", "→ magnetic gradient", "→ attractor magnetization and movement",
    "→ altered boundary state", "→ changed shielding amplitude and phase",
    "→ changed force gradient",
)
TRANSFERS = (
    "A three-phase vector can be treated as one control object while its three physical phase circuits remain separately measurable and isolatable.",
    "Boundary state may be varied and tested for effects on field direction, delay, filtering, shielding, loss, force, and transformation.",
    "Attractor redistribution may be treated as feedback into the next field cycle without assuming that the proposed behavior has already been demonstrated.",
    "Alloy candidates may be organized as a bounded Fe-Co-Ni composition search while preserving fixed chromium and manganese constraints.",
)
DOES_NOT_TRANSFER = (
    "Eighteen phase circuits are eighteen unrelated control objects.",
    "The internal ceramic-coated magnetic eddy-current attractors are bearings.",
    "Voltage is the primary magnetic command variable.",
    "The candidate alloy list establishes an ideal alloy or operating heat treatment.",
    "Ceramic coating guarantees fault containment, insulation life, or vacuum partial-discharge performance.",
    "METAPAT terminology replaces electromagnetic simulation, circuit analysis, materials testing, thermal analysis, or experiment.",
)
WORKING_QUESTION = (
    "What phase geometry, current tensor, boundary configuration, attractor distribution, alloy state, "
    "and thermal envelope produce the required field, shielding, phase, motion, and fault response "
    "without exceeding declared spacecraft limits?"
)
EVIDENCE_BOUNDARY = (
    "The geometry and control topology are specified as an engineering proposal. Claimed magnetic, "
    "shielding, phase-delay, fault-containment, thermal, high-voltage, mechanical, and materials "
    "performance remain answerable to electromagnetic simulation, circuit analysis, coupon "
    "characterization, vacuum insulation testing, thermal testing, fault testing, and instrumented prototypes."
)
EVIDENCE_REQUIREMENTS = (
    "Define whether physical phase displacement is circumferential, axial, or helical.",
    "Define voltage as peak, RMS, or direct-current-link value and bound circuit-to-circuit differential and overshoot.",
    "Bound operating frequency, maximum phase current, target field amplitude, shielding attenuation, and desired phase shift.",
    "Define attractor size, shape, coating, allowed motion, containment geometry, and repeatability requirements.",
    "Define normal and fault temperatures for copper, iron, ceramic, attractors, feedthroughs, and nearby spacecraft systems.",
    "Simulate the six coupled three-phase systems including end leakage, return paths, saturation, eddy currents, losses, and moving boundaries.",
    "Produce and characterize alloy coupons across the declared Fe-Co-Ni composition search under fixed chromium and manganese constraints.",
    "Measure complex permeability, saturation, coercivity, resistivity, heating, hysteresis, settling, phase response, leakage field, and mechanical motion.",
    "Qualify insulation and feedthrough behavior under vacuum, intermediate pressure, overshoot, partial discharge, leakage, and fault energy.",
    "Build a short instrumented section before attempting the full three-meter assembly.",
)
UNRESOLVED = (
    "hmmm: phase geometry remains unresolved among circumferential, axial, and helical displacement.",
    "hmmm: voltage remains unresolved among peak, RMS, and direct-current-link specification.",
    "hmmm: operating frequency, maximum phase current, target field, shielding attenuation, desired phase shift, attractor dimensions, thermal limits, and protection distance remain unregistered.",
    "hmmm: the ideal alloy remains a composition-search problem until microstructure, heat treatment, frequency, geometry, temperature, loss, and phase-response requirements are measured.",
)

LAYER_SPECS = (
    WindingLayerSpec("outer", 1, 12, 6),
    WindingLayerSpec("middle", 2, 16, 12),
    WindingLayerSpec("inner", 3, 20, 18),
)
ALLOY_CANDIDATES = (
    AlloyCandidate("A-anchor", 42.5, 22.5, 10, 15, 10),
    AlloyCandidate("B", 37.5, 22.5, 15, 15, 10),
    AlloyCandidate("C", 32.5, 17.5, 25, 15, 10),
    AlloyCandidate("D", 45, 15, 15, 15, 10),
    AlloyCandidate("E", 35, 30, 10, 15, 10),
)
DRIVE_MODES = (
    "alternating current", "direct-current bias", "reversed polarity",
    "independently controlled amplitude and phase",
)
PHASE_GEOMETRY_OPTIONS = (
    "circumferential displacement → rotation",
    "axial displacement → translation",
    "helical displacement → simultaneous rotation and translation",
)
MOBILE_ELEMENT_EFFECTS = (
    "shielding amplitude", "magnetic phase delay", "field gradients",
    "settling behavior", "local permeability", "local eddy-current losses",
    "field-history response",
)
MOBILE_ELEMENT_BEHAVIORS = (
    "move", "cluster", "chain", "redistribute", "rotate", "occupy field maxima",
)
MEASUREMENT_REQUIREMENTS = (
    "phase current and voltage", "field magnitude", "field phase",
    "attractor distribution", "temperature", "hysteresis", "settling time",
    "leakage field", "mechanical motion",
)
NORMAL_OPERATION_CONSTRAINTS = (
    "copper remains solid",
    "iron remains below magnetic degradation temperatures",
    "ceramic provides insulation and containment",
    "six three-phase systems remain independently isolatable",
)
EXTREME_FAULT_OBJECTIVES = (
    "current controller limits or disconnects",
    "fuse isolates the failed phase",
    "locally molten copper remains inside its ceramic winding channel",
    "no conductive spray, welded rotor, inter-turn short, or spacecraft fire occurs",
    "failed copper resolidifies as an isolated circuit",
)
HIGH_VOLTAGE_REQUIREMENTS = (
    "account for circuit-to-circuit differential voltage",
    "account for inductive overshoot",
    "use void-free ceramic encapsulation",
    "use sealed ceramic-to-metal feedthroughs",
    "avoid sharp terminals",
    "provide clamping or energy recovery",
    "test partial discharge under vacuum and intermediate pressure",
    "monitor insulation leakage",
    "isolate each phase independently",
)
IMMEDIATE_NEXT_WORK = (
    "Define whether phase geometry is circumferential, axial, or helical.",
    "Define voltage as peak, RMS, or DC-link value.",
    "Bound operating frequency range.",
    "Bound maximum phase current.",
    "Define target field amplitude.",
    "Define required shielding attenuation and phase shift.",
    "Define attractor size and allowed motion.",
    "Define operating and fault temperatures.",
    "Simulate the six coupled three-phase systems.",
    "Produce and characterize alloy coupons across the Fe–Co–Ni composition simplex.",
    "Measure complex permeability, saturation, coercivity, resistivity, heating, and phase response.",
    "Build a short instrumented section before attempting the full three-meter system.",
)


def _source_pairs() -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = [
        ("application-identity", "Status: **EMPIRICAL-FRONTIER / engineering application**"),
        ("application-identity", "Root impact: **none**"),
        ("canon-correction", "|∆|The natural control object is one three-phase vector per handedness per radial layer.|∆|"),
        ("canon-correction", "The system is not eighteen unrelated currents and the internal alloy objects are not bearings."),
        ("windings", "- 18 phase circuits total;"),
        ("windings", "- naturally organized as |∆|six three-phase systems|∆|."),
        ("windings", "The drives should be current-controlled. Voltage is compliance, not the magnetic command variable."),
        ("mobile-internal-elements", "The internal objects are |∆|not bearings|∆|."),
        ("protection-distance-status", "No fixed protection distance is established yet."),
        ("evidence-boundary", EVIDENCE_BOUNDARY),
    ]
    pairs.extend(
        ("catalog-bindings", f"| `{module_id}` | {role} | {statement} |")
        for module_id, role, statement in PIPE_BINDING_SPECS
    )
    return tuple(pairs)


def electromagnetic_pipe_application_module(
    catalog: MetapatSemanticCatalog | None = None,
) -> MetapatApplicationModule:
    selected = catalog or canonical_semantic_catalog()
    bindings = tuple(
        bind_catalog_module(
            semantic_module_by_id(module_id, selected),
            application_role=role,
            application_statement=statement,
        )
        for module_id, role, statement in PIPE_BINDING_SPECS
    )
    pairs = _source_pairs()
    refs = tuple(
        f"{SOURCE_DOCUMENT}#{anchor}::statement-{index}"
        for index, (anchor, _statement) in enumerate(pairs, start=1)
    )
    application = MetapatApplicationModule(
        application_id="metapat.application.three_phase_electromagnetic_pipe",
        application_version=PIPE_APPLICATION_VERSION,
        title="Three-Phase Nested Electromagnetic Pipe System",
        claim_status="EMPIRICAL-FRONTIER",
        domains=DOMAINS,
        selected_scales=SELECTED_SCALES,
        source_document=SOURCE_DOCUMENT,
        source_statement_refs=refs,
        source_statements=tuple(statement for _anchor, statement in pairs),
        catalog_version=selected.catalog_version,
        catalog_digest=selected.catalog_digest,
        catalog_bindings=bindings,
        domain_statements=DOMAIN_STATEMENTS,
        shared_question_form=SHARED_QUESTION_FORM,
        transfers=TRANSFERS,
        does_not_transfer=DOES_NOT_TRANSFER,
        working_question=WORKING_QUESTION,
        evidence_boundary=EVIDENCE_BOUNDARY,
        evidence_requirements=EVIDENCE_REQUIREMENTS,
        unresolved_constraints=UNRESOLVED,
    )
    validate_application_against_catalog(application, selected)
    return application


@dataclass(frozen=True, slots=True)
class ElectromagneticPipeDesign:
    application: MetapatApplicationModule
    assembly_length_m: float
    outer_pipe_diameter_in: float
    radial_layer_count: int
    handednesses: tuple[str, ...]
    phases_per_handedness: int
    winding_layers: tuple[WindingLayerSpec, ...]
    control_object: str
    current_command_variable: str
    voltage_role: str
    drive_modes: tuple[str, ...]
    phase_geometry_options: tuple[str, ...]
    mobile_element_designation: str
    prohibited_mobile_element_designation: str
    mobile_element_effects: tuple[str, ...]
    mobile_element_behaviors: tuple[str, ...]
    alloy_candidates: tuple[AlloyCandidate, ...]
    measurement_requirements: tuple[str, ...]
    normal_operation_constraints: tuple[str, ...]
    extreme_fault_objectives: tuple[str, ...]
    high_voltage_requirements: tuple[str, ...]
    protection_distance_status: str
    immediate_next_work: tuple[str, ...]
    unresolved_constraints: tuple[str, ...]
    electromagnetic_validity_claim: bool = False
    alloy_validity_claim: bool = False
    insulation_validity_claim: bool = False
    fault_containment_validity_claim: bool = False
    spacecraft_safety_validity_claim: bool = False
    schema_id: str = PIPE_DESIGN_SCHEMA_ID
    schema_version: str = PIPE_DESIGN_SCHEMA_VERSION
    design_digest: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.application, MetapatApplicationModule):
            raise TypeError("application must be a MetapatApplicationModule")
        object.__setattr__(self, "assembly_length_m", _number(self.assembly_length_m, "assembly_length_m", minimum=0.001))
        object.__setattr__(self, "outer_pipe_diameter_in", _number(self.outer_pipe_diameter_in, "outer_pipe_diameter_in", minimum=0.001))
        if self.radial_layer_count != 3:
            raise ValueError("radial_layer_count must remain 3")
        handednesses = _strings(self.handednesses, "handednesses", minimum=2)
        if handednesses != ("clockwise", "widdershins"):
            raise ValueError("handednesses must remain clockwise and widdershins")
        if self.phases_per_handedness != 3:
            raise ValueError("phases_per_handedness must remain 3")
        layers = tuple(self.winding_layers)
        if tuple((x.layer_name, x.radial_order, x.wire_awg, x.turns_per_inch) for x in layers) != (
            ("outer", 1, 12, 6), ("middle", 2, 16, 12), ("inner", 3, 20, 18),
        ):
            raise ValueError("winding layer order or specification mismatch")
        if self.control_object != "one three-phase vector per handedness per radial layer":
            raise ValueError("control_object mismatch")
        if self.current_command_variable != "phase current" or self.voltage_role != "compliance":
            raise ValueError("current command or voltage role mismatch")
        if self.mobile_element_designation != "ceramic-coated magnetic eddy-current attractors":
            raise ValueError("mobile elements must remain ceramic-coated magnetic eddy-current attractors")
        if self.prohibited_mobile_element_designation != "bearings":
            raise ValueError("prohibited mobile-element designation must remain bearings")
        candidates = tuple(self.alloy_candidates)
        if len(candidates) != 5 or any(not isinstance(x, AlloyCandidate) for x in candidates):
            raise ValueError("exactly five alloy candidates are required")
        tuple_fields = (
            "drive_modes", "phase_geometry_options", "mobile_element_effects",
            "mobile_element_behaviors", "measurement_requirements",
            "normal_operation_constraints", "extreme_fault_objectives",
            "high_voltage_requirements", "immediate_next_work", "unresolved_constraints",
        )
        for name in tuple_fields:
            object.__setattr__(self, name, _strings(getattr(self, name), name, minimum=1))
        object.__setattr__(self, "handednesses", handednesses)
        object.__setattr__(self, "winding_layers", layers)
        object.__setattr__(self, "alloy_candidates", candidates)
        _text(self.protection_distance_status, "protection_distance_status")
        for name in (
            "electromagnetic_validity_claim", "alloy_validity_claim",
            "insulation_validity_claim", "fault_containment_validity_claim",
            "spacecraft_safety_validity_claim",
        ):
            _false(getattr(self, name), name)
        if self.schema_id != PIPE_DESIGN_SCHEMA_ID or self.schema_version != PIPE_DESIGN_SCHEMA_VERSION:
            raise ValueError("unsupported pipe-design schema")
        expected = _digest(self._payload())
        if self.design_digest and self.design_digest != expected:
            raise ValueError("design_digest mismatch")
        object.__setattr__(self, "design_digest", expected)

    @property
    def phase_circuit_count(self) -> int:
        return self.radial_layer_count * len(self.handednesses) * self.phases_per_handedness

    @property
    def three_phase_system_count(self) -> int:
        return self.radial_layer_count * len(self.handednesses)

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "application": self.application.to_dict(),
            "assembly_length_m": self.assembly_length_m,
            "outer_pipe_diameter_in": self.outer_pipe_diameter_in,
            "radial_layer_count": self.radial_layer_count,
            "handednesses": list(self.handednesses),
            "phases_per_handedness": self.phases_per_handedness,
            "phase_circuit_count": self.phase_circuit_count,
            "three_phase_system_count": self.three_phase_system_count,
            "winding_layers": [layer.to_dict() for layer in self.winding_layers],
            "control_object": self.control_object,
            "current_command_variable": self.current_command_variable,
            "voltage_role": self.voltage_role,
            "drive_modes": list(self.drive_modes),
            "phase_geometry_options": list(self.phase_geometry_options),
            "mobile_element_designation": self.mobile_element_designation,
            "prohibited_mobile_element_designation": self.prohibited_mobile_element_designation,
            "mobile_element_effects": list(self.mobile_element_effects),
            "mobile_element_behaviors": list(self.mobile_element_behaviors),
            "alloy_candidates": [candidate.to_dict() for candidate in self.alloy_candidates],
            "measurement_requirements": list(self.measurement_requirements),
            "normal_operation_constraints": list(self.normal_operation_constraints),
            "extreme_fault_objectives": list(self.extreme_fault_objectives),
            "high_voltage_requirements": list(self.high_voltage_requirements),
            "protection_distance_status": self.protection_distance_status,
            "immediate_next_work": list(self.immediate_next_work),
            "unresolved_constraints": list(self.unresolved_constraints),
            "electromagnetic_validity_claim": self.electromagnetic_validity_claim,
            "alloy_validity_claim": self.alloy_validity_claim,
            "insulation_validity_claim": self.insulation_validity_claim,
            "fault_containment_validity_claim": self.fault_containment_validity_claim,
            "spacecraft_safety_validity_claim": self.spacecraft_safety_validity_claim,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "design_digest": self.design_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ElectromagneticPipeDesign":
        expected = {
            "schema_id", "schema_version", "application", "assembly_length_m",
            "outer_pipe_diameter_in", "radial_layer_count", "handednesses",
            "phases_per_handedness", "phase_circuit_count", "three_phase_system_count",
            "winding_layers", "control_object", "current_command_variable", "voltage_role",
            "drive_modes", "phase_geometry_options", "mobile_element_designation",
            "prohibited_mobile_element_designation", "mobile_element_effects",
            "mobile_element_behaviors", "alloy_candidates", "measurement_requirements",
            "normal_operation_constraints", "extreme_fault_objectives",
            "high_voltage_requirements", "protection_distance_status",
            "immediate_next_work", "unresolved_constraints",
            "electromagnetic_validity_claim", "alloy_validity_claim",
            "insulation_validity_claim", "fault_containment_validity_claim",
            "spacecraft_safety_validity_claim", "design_digest",
        }
        if not isinstance(data, Mapping):
            raise ValueError("pipe design must be a mapping")
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ValueError(f"unknown pipe-design fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing pipe-design fields: {sorted(missing)!r}")
        result = cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            application=MetapatApplicationModule.from_dict(data["application"]),
            assembly_length_m=_number(data["assembly_length_m"], "assembly_length_m"),
            outer_pipe_diameter_in=_number(data["outer_pipe_diameter_in"], "outer_pipe_diameter_in"),
            radial_layer_count=_integer(data["radial_layer_count"], "radial_layer_count"),
            handednesses=_strings(data["handednesses"], "handednesses", minimum=2),
            phases_per_handedness=_integer(data["phases_per_handedness"], "phases_per_handedness"),
            winding_layers=tuple(WindingLayerSpec.from_dict(x) for x in data["winding_layers"]),
            control_object=_text(data["control_object"], "control_object"),
            current_command_variable=_text(data["current_command_variable"], "current_command_variable"),
            voltage_role=_text(data["voltage_role"], "voltage_role"),
            drive_modes=_strings(data["drive_modes"], "drive_modes", minimum=1),
            phase_geometry_options=_strings(data["phase_geometry_options"], "phase_geometry_options", minimum=1),
            mobile_element_designation=_text(data["mobile_element_designation"], "mobile_element_designation"),
            prohibited_mobile_element_designation=_text(data["prohibited_mobile_element_designation"], "prohibited_mobile_element_designation"),
            mobile_element_effects=_strings(data["mobile_element_effects"], "mobile_element_effects", minimum=1),
            mobile_element_behaviors=_strings(data["mobile_element_behaviors"], "mobile_element_behaviors", minimum=1),
            alloy_candidates=tuple(AlloyCandidate.from_dict(x) for x in data["alloy_candidates"]),
            measurement_requirements=_strings(data["measurement_requirements"], "measurement_requirements", minimum=1),
            normal_operation_constraints=_strings(data["normal_operation_constraints"], "normal_operation_constraints", minimum=1),
            extreme_fault_objectives=_strings(data["extreme_fault_objectives"], "extreme_fault_objectives", minimum=1),
            high_voltage_requirements=_strings(data["high_voltage_requirements"], "high_voltage_requirements", minimum=1),
            protection_distance_status=_text(data["protection_distance_status"], "protection_distance_status"),
            immediate_next_work=_strings(data["immediate_next_work"], "immediate_next_work", minimum=1),
            unresolved_constraints=_strings(data["unresolved_constraints"], "unresolved_constraints", minimum=1),
            electromagnetic_validity_claim=_false(data["electromagnetic_validity_claim"], "electromagnetic_validity_claim"),
            alloy_validity_claim=_false(data["alloy_validity_claim"], "alloy_validity_claim"),
            insulation_validity_claim=_false(data["insulation_validity_claim"], "insulation_validity_claim"),
            fault_containment_validity_claim=_false(data["fault_containment_validity_claim"], "fault_containment_validity_claim"),
            spacecraft_safety_validity_claim=_false(data["spacecraft_safety_validity_claim"], "spacecraft_safety_validity_claim"),
            design_digest=_hex(data["design_digest"], "design_digest"),
        )
        if data["phase_circuit_count"] != result.phase_circuit_count:
            raise ValueError("phase_circuit_count mismatch")
        if data["three_phase_system_count"] != result.three_phase_system_count:
            raise ValueError("three_phase_system_count mismatch")
        return result

    @classmethod
    def from_json(cls, value: str) -> "ElectromagneticPipeDesign":
        if not isinstance(value, str):
            raise ValueError("pipe design JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ValueError("pipe design JSON must decode to an object")
        return cls.from_dict(decoded)


def electromagnetic_pipe_design(
    catalog: MetapatSemanticCatalog | None = None,
) -> ElectromagneticPipeDesign:
    selected = catalog or canonical_semantic_catalog()
    return ElectromagneticPipeDesign(
        application=electromagnetic_pipe_application_module(selected),
        assembly_length_m=3.0,
        outer_pipe_diameter_in=3.0,
        radial_layer_count=3,
        handednesses=("clockwise", "widdershins"),
        phases_per_handedness=3,
        winding_layers=LAYER_SPECS,
        control_object="one three-phase vector per handedness per radial layer",
        current_command_variable="phase current",
        voltage_role="compliance",
        drive_modes=DRIVE_MODES,
        phase_geometry_options=PHASE_GEOMETRY_OPTIONS,
        mobile_element_designation="ceramic-coated magnetic eddy-current attractors",
        prohibited_mobile_element_designation="bearings",
        mobile_element_effects=MOBILE_ELEMENT_EFFECTS,
        mobile_element_behaviors=MOBILE_ELEMENT_BEHAVIORS,
        alloy_candidates=ALLOY_CANDIDATES,
        measurement_requirements=MEASUREMENT_REQUIREMENTS,
        normal_operation_constraints=NORMAL_OPERATION_CONSTRAINTS,
        extreme_fault_objectives=EXTREME_FAULT_OBJECTIVES,
        high_voltage_requirements=HIGH_VOLTAGE_REQUIREMENTS,
        protection_distance_status=(
            "No fixed protection distance is established yet; end leakage, return paths, "
            "frequency, field limits, saturation, and attractor state remain determinant."
        ),
        immediate_next_work=IMMEDIATE_NEXT_WORK,
        unresolved_constraints=UNRESOLVED,
    )


def electromagnetic_pipe_design_digest() -> str:
    return electromagnetic_pipe_design().design_digest


__all__ = [
    "ALLOY_CANDIDATE_SCHEMA_ID",
    "ALLOY_CANDIDATE_SCHEMA_VERSION",
    "PIPE_APPLICATION_VERSION",
    "PIPE_BINDING_SPECS",
    "PIPE_DESIGN_SCHEMA_ID",
    "PIPE_DESIGN_SCHEMA_VERSION",
    "WINDING_LAYER_SCHEMA_ID",
    "WINDING_LAYER_SCHEMA_VERSION",
    "AlloyCandidate",
    "ElectromagneticPipeDesign",
    "WindingLayerSpec",
    "electromagnetic_pipe_application_module",
    "electromagnetic_pipe_design",
    "electromagnetic_pipe_design_digest",
]
