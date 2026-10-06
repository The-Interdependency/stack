# Weave: superseded byte/star interpretation

**Historical only. The active cycle is [CYCLE.md](CYCLE.md).**

The one-bit-per-circle interpretation from PR #76 is superseded by the user's
later sequence/occurrence clarification. A selected multi-byte sequence is saved
at an angle on the eighth/origin circle. A circle among the seven records its
occurrences and order. This is not an eight-circle allocation for every byte.
The eight circle count does not establish a 16-bit output codeword or total 2x size.

The old `stages/eight_circle.py` and `stages/message_origin.py` structural records
and their 22 tests are removed. Native replacement is the Stack-owned binary-origin/sequence candidate
(`native_binary.py`), consumed by `cycle_native.py` and `cycle.py`. It uses
actual UCNS axis-circle and Mobius objects and performs exact coordinate recovery.
The associated bit-per-circle questions Q11/Q13/Q14 no longer control construction.

Retained architectural distinctions: one whole plus seven occurrence circles;
720-degree complete return; key/profile-specific space relationships; byte-occurrence
identity; and the intended whole-plus-one public exposure. The last remains an
asymmetric research objective, not a property claimed by the current cycle record.

## Evidence correction

PR #73's per-bit two-sheet encoder and PR #74's bit-axis feedback were wrong
implementations. Their public recovery attacks apply to those implementations,
not to the intended Weave construction. Changing data unavailable to a public
sender while holding every sender input fixed cannot demonstrate whether a private
key is necessary for recovery. That inference remains withdrawn.

Historical source identities:

- PR #73: `a3836f5632ed3babe1bc8c3dbebab60186c2bc78`;
- PR #74: `92ccda0620c06bc46654939c061ceb2d36476cb9`;
- PR #76 structural repair: `d0e76d58f832a5664578af39103cdd0697c091d3`.

These are historical provenance, not active capabilities or security evidence.

## Usage

Use `python cycle.py demo --sources /checkouts` and the commands in `CYCLE.md`.
Do not import the removed bit-per-circle records or restore them as a fallback.

## hmmm

The native sequence cycle is executable. Public/private key generation and a
computational recovery advantage remain separate construction work.
