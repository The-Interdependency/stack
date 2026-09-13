# PTCNA research workspace

Stack-local research retains its exact historical source in [`BASE.json`](BASE.json).
The current canonical PTCNA view is [`../../libs/ptcna/`](../../libs/ptcna/);
its 2026-09-13 refresh does not rebase this workspace or regenerate its receipts.

Standing: **research, not canon**. Canonical PTCNA authority remains `The-Interdependency/ptcna` at the exact commit recorded in [`BASE.json`](BASE.json) and the root stack manifest.

## Usage guidance

1. Read `BASE.json` before beginning work.
2. Treat `../../libs/ptcna/` as read-only imported canon.
3. Put experiments, candidate changes, measurements, and notes here rather than editing `libs/`.
4. If work changes PTCNA itself, route the accepted change upstream; after merge, refresh `libs/ptcna/` and this workspace's base commit.
5. If work becomes a distinct composed project, keep its authority separate rather than silently promoting this workspace.

## hmmm

No active PTCNA-specific stack research has been materialized here yet.
