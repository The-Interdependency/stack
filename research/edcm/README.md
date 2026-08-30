# EDCM research workspace

Stack-local research against the pinned canonical EDCM view in [`../../libs/edcm/`](../../libs/edcm/).

Standing: **research, not canon**. Canonical EDCM authority remains `The-Interdependency/edcm` at the exact commit recorded in [`BASE.json`](BASE.json) and the root stack manifest.

## Usage guidance

1. Read `BASE.json` before beginning work.
2. Treat `../../libs/edcm/` as read-only imported canon.
3. Put experiments, candidate changes, measurements, and notes here rather than editing `libs/`.
4. If work changes EDCM itself, route the accepted change upstream; after merge, refresh `libs/edcm/` and this workspace's base commit.
5. If work becomes a distinct composed project, keep its authority separate rather than silently promoting this workspace.

## hmmm

No active EDCM-specific stack research has been materialized here yet.
