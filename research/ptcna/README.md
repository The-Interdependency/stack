# PTCNA research workspace

Stack-local research against the pinned canonical PTCNA view in [`../../libs/ptcna/`](../../libs/ptcna/).

Standing: **research, not canon**. Canonical PTCNA authority remains `The-Interdependency/ptcna` at the exact commit recorded in [`BASE.json`](BASE.json) and the root stack manifest.

## Usage guidance

1. Read `BASE.json` before beginning work.
2. Treat `../../libs/ptcna/` as read-only imported canon.
3. Put experiments, candidate changes, measurements, and notes here rather than editing `libs/`.
4. If work changes PTCNA itself, route the accepted change upstream; after merge, refresh `libs/ptcna/` and this workspace's base commit.
5. If work becomes a distinct composed project, keep its authority separate rather than silently promoting this workspace.

## hmmm

No active PTCNA-specific stack research has been materialized here yet.
