# UCNS attachment replay, 2026-11-12

This replay integrates the UCNS-only portion of Stack #42
(`57874ce0945cc89de16e0eb01b1f16469b0a1f33`) on Stack main
`77f57c1a8d7fb5978d346e79246ff7d313d1d769`.

The original JSON and Markdown in the parent directory remain byte-for-byte
unchanged. The sole JSON payload difference is
`source_identities.rooted_rotation_receipt_sha256`:

- Historical input: `d8ce28b8e183123f0c5ecc2cd04a5783fb6c476524b6491665bba85c3d67de89`.
- Current integration: `6cef59f9942a4259af9d386c8ff79a4e61f39600dfe71671eb186c880baec5a6`.

All mathematical results, candidate assumptions, controls and verdicts match.
This is a new source-bound replay, not a new geometric or security result.

## Usage

From the repository root, with tracked `libs/ucns/` and `libs/metapat/` present:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  research.ucns.tests.test_rooted_rotation_closure_constructor \
  research.ucns.tests.test_native_attachment_target_stabilizer -v
python3 tools/check_stack_consistency.py
```

Reproduce candidate receipts into a new directory outside the checkout:

```bash
python3 research/ucns/native_attachment_target_stabilizer.py \
  --write-receipts /tmp/ucns-attachment-replay
diff -u research/ucns/receipts/replay-20261112/native-attachment-target-stabilizer-v0.json \
  /tmp/ucns-attachment-replay/native-attachment-target-stabilizer-v0.json
```

`hmmm`: intrinsic attachment selection and a surviving cryptographic relation
remain unresolved. PCEA material and general research governance have separate PRs.
