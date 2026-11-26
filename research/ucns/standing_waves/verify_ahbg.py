# ratios: loc_comments=42:14 imports_exports=6:1 calls_definitions=26:1
# === MODULE_BUILD ===
# id: stack_ucns_ahbg_replay
#   summary: qualify the November 26 saved turn with the pinned UCNS package
#   storage_boundary: read frozen evidence; the AHBG controls use temporary directories
#   network_boundary: none
#   requires: exact historical AHBG checkout and this Stack UCNS projection
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: ucns_campaign_replays_with_seven_pinned_imports
#   given: the archived campaign and corrected UCNS package are present
#   then: replay reproduces the contested turn, separate construction record, four control arms and seven import identities
#   class: evidence
# === END CONTRACTS ===
"""Qualify the pinned UCNS import set using the archived campaign. See README.md."""

import hashlib
import json
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    receipt = json.loads((root / "research/ucns/receipts/ahbg-standing-wave-provenance-v1.json").read_bytes())
    comparison = root / receipt["audit"]["path"]
    if not comparison.is_file():
        raise SystemExit("Prepare the frozen AHBG checkout as described in standing_waves/README.md")
    if hashlib.sha256(comparison.read_bytes()).hexdigest() != receipt["audit"]["sha256"]:
        raise ValueError("historical AHBG source comparison differs")

    from ahbg.campaign.geometry_control import run
    from ahbg.campaign.mission import replay

    evidence = receipt["replay"]
    fixture = root / evidence["fixture"]
    result = replay(fixture)
    if result["state_digest"] != evidence["contested_state_digest"]:
        raise ValueError("contested-turn state differs")
    ledger = json.loads((fixture / "construction.json").read_bytes())
    if json.loads((fixture / "result.json").read_bytes())["construction"] != ledger:
        raise ValueError("saved construction ledger differs")
    expected = {row["module"]: row for row in receipt["corrected_imports"]}
    loaded = {name: module for name, module in sys.modules.items() if name == "ucns" or name.startswith("ucns.")}
    if loaded.keys() != expected.keys():
        raise ValueError(f"UCNS replay import set differs: {sorted(loaded.keys() ^ expected.keys())}")
    for name, module in loaded.items():
        path = Path(module.__file__).resolve()
        if path != root / "libs/ucns" / expected[name]["upstream_path"]:
            raise ValueError(f"unexpected import origin for {name}: {path}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected[name]["sha256"]:
            raise ValueError(f"source digest differs for {name}")
    control = run()
    if control != json.loads((root / evidence["control"]).read_bytes()):
        raise ValueError("geometry control differs from the recorded four arms")
    if control["normal"]["result"] != evidence["normal_restored_irrelevant_state_digest"]:
        raise ValueError("geometry control state differs from the source receipt")
    if control["removed"]["result"] != f"ModuleNotFoundError: No module named '{evidence['removed_seed']}'":
        raise ValueError("geometry control removed a different dependency")
    print(f"{len(loaded)} pinned UCNS imports; contested {result['state_digest']}; control {control['normal']['result']}")


if __name__ == "__main__":
    main()
# ratios: loc_comments=42:14 imports_exports=6:1 calls_definitions=26:1
