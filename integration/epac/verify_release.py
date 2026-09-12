"""Usage: CLEAN_ENV/bin/python integration/epac/verify_release.py WHEEL RECEIPT --phase candidate.

Install the hash-verified wheel and its pinned dependencies first. Run again with
--phase graduated after public reconsumption and retirement of forge source.
The emitted receipt covers composition and implementation provenance only.
"""
# === MODULE_BUILD ===
# id: stack_epac_release_consumption
#   module_name: verify_release
#   module_kind: instrument
#   summary: verifies the exact installed EPAC artifact through its public construction and replay surfaces
#   owner: The Interdependency
#   public_surface: command-line EPAC consumer verification
#   internal_surface: main
#   auth_boundary: none
#   storage_boundary: write
#   storage_notes: read candidate wheel; write caller-selected receipt
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: invoked before publication and after public artifact reconsumption
#   rollout: pre-publication and post-publication composition gates
#   rollback: retain the previously accepted immutable artifact
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: stack_epac_consumes_immutable_artifact
#   given: EPAC is installed from the identified candidate or published wheel
#   then: installed bytes match that wheel, public construction/replay composes with exact UCNS source, falsification standing remains, and graduated consumption has no forge-local implementation
#   class: provenance
# === END CONTRACTS ===
from __future__ import annotations

import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path
import sys
import zipfile


EXPECTED_STANDINGS = {
    "atomic_shells_as_sealed_shape_prediction": "FALSIFIED",
    "boundary_capacity_as_sealed_shape_prediction": "FALSIFIED",
    "charged_3_structure_as_sealed_shape_prediction": "FALSIFIED",
    "harmonic_survival_as_sealed_shape_prediction": "FALSIFIED",
    "lifted_spiral_as_sealed_shape_prediction": "FALSIFIED",
    "per_symbol_harmonic_survival_as_sealed_shape_prediction": "FALSIFIED",
    "periodic_element_boundary_capacity_as_sealed_shape_prediction": "FALSIFIED",
    "periodic_element_harmonic_survival_as_sealed_shape_prediction": "FALSIFIED",
    "periodic_element_lifted_spiral_as_sealed_shape_prediction": "FALSIFIED",
    "subatomic_boundary_capacity_as_sealed_shape_prediction": "FALSIFIED",
    "subatomic_harmonic_survival_as_sealed_shape_prediction": "FALSIFIED",
    "subatomic_lifted_spiral_as_sealed_shape_prediction": "FALSIFIED",
    "topology_3_structure_as_sealed_shape_prediction": "FALSIFIED",
    "ucns_mobius_as_sealed_shape_prediction": "FALSIFIED"
}


def main() -> None:
    if sys.flags.optimize:
        raise SystemExit("optimized Python mode cannot produce consumer evidence")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--phase", choices=("candidate", "reconsumed", "graduated"), required=True)
    args = parser.parse_args()
    stack = Path(__file__).resolve().parents[2]
    with zipfile.ZipFile(args.wheel) as archive:
        expected = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist()
                    if name.startswith("epac_") and not name.endswith("/")}
    distribution = metadata.distribution("interdependency-epac")
    installed = {str(path): Path(distribution.locate_file(path)).resolve() for path in distribution.files or ()
                 if str(path).startswith("epac_") and "__pycache__" not in path.parts}
    assert expected and set(installed) == set(expected)
    for name, path in installed.items():
        assert path.is_relative_to(Path(sys.prefix)) and not path.is_relative_to(stack), path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected[name], name
    from epac_public_gonol import construct_public_gonol, replay_public_gonol, PINNED_UCNS_COMMIT
    from epac_molecular import construct_declared_molecules, replay_molecule
    from epac_comparison import compare_after_construction
    from epac_subatomic.element_affixiation_candidate import affixiate_element, replay_element
    result = construct_public_gonol(source_id="stack.integration:oxygen", relation="epac.atomic.element",
                                   identity_glyph="O", carried_options=(("symbol", "O"), ("Z", "8")))
    replayed = replay_public_gonol(result)
    assert replayed.receipt_digest == result.receipt_digest
    assert result.geometry["ucns_commit"] == PINNED_UCNS_COMMIT != "hmmm"
    molecules = construct_declared_molecules()
    assert set(molecules) == {"H2", "H2O", "NH3", "CH4", "CO2", "H2S", "BF3", "PH3", "SiH4"}
    for molecule in molecules.values():
        assert replay_molecule(molecule).receipt_digest == molecule.receipt.receipt_digest
    element = affixiate_element("He")
    assert replay_element("He") == (True, element.receipt)
    assert element.source_commits["ucns"] == PINNED_UCNS_COMMIT
    standings = compare_after_construction()["standings"]
    assert standings == EXPECTED_STANDINGS
    origins = {name: Path(module.__file__).resolve() for name, module in sys.modules.items()
               if (name.startswith("epac_") or name == "ucns" or name.startswith("ucns.")) and getattr(module, "__file__", None)}
    assert all(path.is_relative_to(Path(sys.prefix)) and not path.is_relative_to(stack) for path in origins.values())
    if args.phase == "graduated":
        assert not list((stack / "research/epac").rglob("*.py")), "forge-local implementation must be retired"
    receipt = {"schema": "stack.epac-artifact-consumption", "version": 1, "phase": args.phase,
               "status": "passed", "artifact_sha256": hashlib.sha256(args.wheel.read_bytes()).hexdigest(),
               "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "python": sys.version, "epac_version": distribution.version, "ucns_source_commit": PINNED_UCNS_COMMIT,
               "installed_payload_sha256": expected,
               "imported_origins": {name: str(path.relative_to(Path(sys.prefix))) for name, path in origins.items()},
               "public_gonol_receipt": result.receipt_digest,
               "molecular_receipts": {name: value.receipt.receipt_digest for name, value in molecules.items()},
               "comparison_standings": standings, "empirical_status_transfer": False}
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("EPAC artifact consumption: passed (" + args.phase + ")")


if __name__ == "__main__":
    main()
