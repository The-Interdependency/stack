# Möbius standing waves

These Stack-local candidates consume the UCNS package at
`828c0b8bbcfc267efb5701da714191c1f73a81ff`. The [root-loop model](docs/STANDING_WAVE_ROOT_LOOP.md)
measures endpoint values and derivatives across the two-turn seam. Its trace has
rank one for the constant mode and two once positive modes enter. The
[band model](docs/STANDING_WAVE_MOBIUS_BAND.md) samples a single physical
boundary with Neumann edge conditions. With 16 samples and cutoffs N=7, K=3,
the fixture has 60 interior modes and boundary rank 15. The embedded surface
operator and a general capacity theorem remain open.

The [source receipt](../receipts/ahbg-standing-wave-provenance-v1.json) records
the nine historical imports and the seven imports from the corrected package.
Stack commit `e3d05e5e4ee4a548e5f22ea43735fe38b4669be4` preserved both models
from a pre-sync working tree and exported them through the vendored initializer.
The original [AHBG comparison](https://github.com/The-Interdependency/stack/blob/311e921553a571c0a82fea1315b66d21d9d7c79a/ahbg/campaign/evidence/source-comparison.json)
records the bytes that campaign actually used. Earlier worktree authorship is
unresolved.

From Stack root, check the source tree and run both geometry suites with pytest:

```sh
python3 tools/check_stack_consistency.py
PYTHONPATH=libs/ucns/src python3 -m pytest -q research/ucns/standing_waves/tests libs/ucns/tests/test_geometry_public_surface.py
```

To repeat the November 26 campaign qualification in a disposable checkout,
run the commands below from the correction commit or its merge. The campaign
commit supplies the exact historical AHBG implementation, saved turn, and control.
The temporary checkout supplies the corrected UCNS package. The test uses
the recorded submitted plan and needs no model weights.

```sh
(
    set -eu
    campaign=311e921553a571c0a82fea1315b66d21d9d7c79a
    git cat-file -e "$campaign^{commit}" 2>/dev/null || git fetch origin "$campaign"
    tmp=$(mktemp -d)
    trap 'git worktree remove --force "$tmp/stack"; rm -d "$tmp"' EXIT
    git worktree add --quiet --detach "$tmp/stack" HEAD
    git -C "$tmp/stack" restore --source="$campaign" --staged --worktree -- ahbg
    git -C "$tmp/stack" diff --exit-code "$campaign" -- ahbg
    (cd "$tmp/stack" && python3 -B -m research.ucns.standing_waves.verify_ahbg && python3 -B -m unittest discover -s ahbg/campaign/tests)
)
```
