"""Twin-ray carrier encryption engine (candidate).

Public face: the 38 twin-supporting residues mod 360.
Private key: short prime-ordinal seed expanded to radius indices.
Encoding: message byte low bit selects Möbius frame; remaining bits are payload
on the private radius layer.

This is a research prototype of the asymmetry discussed; it is not a
production cryptosystem. Hardness, formal key derivation, and side-channel
rules remain open.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List, Optional, Sequence

# Full public carrier
TWIN_RAYS: tuple[int, ...] = (
    3, 5, 11, 17, 29, 41, 47, 59, 71, 77, 89, 101, 107, 119,
    131, 137, 149, 161, 167, 179, 191, 197, 209, 221, 227, 239,
    251, 257, 269, 281, 287, 299, 311, 317, 329, 341, 347, 359,
)
CARRIER_SIZE = len(TWIN_RAYS)  # 38


class Frame:
    A = 1
    B = -1


@dataclass(frozen=True)
class Record:
    index: int
    residue: int
    frame: int
    payload: int
    radius: int
    byte: Optional[int]  # None for padding


class TwinRayEngine:
    """Candidate encryption engine on the twin-ray carrier."""

    def __init__(self, seed_ordinals: Sequence[int], radius_layers: int = 8):
        if not seed_ordinals:
            raise ValueError("seed_ordinals must be non-empty")
        if radius_layers < 2:
            raise ValueError("radius_layers must be >= 2")
        self.seed_ordinals = tuple(seed_ordinals)
        self.radius_layers = radius_layers
        self.radii = self._expand_seed()

    def _expand_seed(self) -> List[int]:
        """Deterministic expansion of the prime-ordinal seed to CARRIER_SIZE radii."""
        state = hashlib.sha256(str(self.seed_ordinals).encode()).digest()
        radii: List[int] = []
        for i in range(CARRIER_SIZE):
            h = hashlib.sha256(state + i.to_bytes(4, "big")).digest()
            radii.append(1 + (h[0] % self.radius_layers))
            state = h
        return radii

    def encrypt(self, message: bytes) -> List[Record]:
        """Encode message bytes onto the carrier. Returns the full set of records
        (public face is the residue list; private data is frame/payload/radius).
        """
        if len(message) > CARRIER_SIZE:
            raise ValueError(f"message length {len(message)} exceeds carrier size {CARRIER_SIZE}")

        records: List[Record] = []
        for i, b in enumerate(message):
            frame = Frame.A if (b & 1) == 0 else Frame.B
            payload = b >> 1
            records.append(Record(
                index=i,
                residue=TWIN_RAYS[i],
                frame=frame,
                payload=payload,
                radius=self.radii[i],
                byte=b,
            ))
        # pad so the public face is always the complete carrier
        for i in range(len(message), CARRIER_SIZE):
            records.append(Record(
                index=i,
                residue=TWIN_RAYS[i],
                frame=Frame.A,
                payload=0,
                radius=self.radii[i],
                byte=None,
            ))
        return records

    def public_face(self, records: List[Record]) -> List[int]:
        """The observable ciphertext: ordered residues (always the full carrier)."""
        return [r.residue for r in records]

    def decrypt(self, records: List[Record]) -> bytes:
        """Recover the original message using the private radii."""
        if len(records) != CARRIER_SIZE:
            raise ValueError("records must cover the full carrier")

        recovered: List[int] = []
        for rec, expected_radius in zip(records, self.radii):
            if rec.byte is None:
                break
            if rec.radius != expected_radius:
                raise ValueError("radius mismatch — incorrect seed")
            if rec.residue != TWIN_RAYS[rec.index]:
                raise ValueError("residue mismatch")
            low = 0 if rec.frame == Frame.A else 1
            byte = (rec.payload << 1) | low
            recovered.append(byte)
        return bytes(recovered)


def self_test() -> None:
    """Run a concrete round-trip test."""
    engine = TwinRayEngine(seed_ordinals=[7, 17], radius_layers=8)
    message = b"UCNS twin-ray engine test!!"
    assert len(message) <= CARRIER_SIZE

    records = engine.encrypt(message)
    face = engine.public_face(records)
    recovered = engine.decrypt(records)

    print(f"carrier size:    {CARRIER_SIZE}")
    print(f"seed:            {engine.seed_ordinals}")
    print(f"first 8 radii:   {engine.radii[:8]}")
    print(f"message length:  {len(message)}")
    print(f"public face:     {face[:6]} ... {face[-4:]}")
    print(f"original:        {message!r}")
    print(f"recovered:       {recovered!r}")
    print(f"match:           {recovered == message}")

    # negative test: wrong seed must fail
    wrong = TwinRayEngine(seed_ordinals=[7, 19])
    try:
        wrong.decrypt(records)
        print("ERROR: wrong seed succeeded")
    except ValueError as e:
        print(f"wrong seed rejected: {e}")


if __name__ == "__main__":
    self_test()
