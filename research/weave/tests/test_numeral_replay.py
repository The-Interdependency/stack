# === CHECKS ===
# id: numeral_equal_limits_roundtrip
#   proves: numeral_exact_recovery, numeral_recipe_replay, numeral_strict_input
#   call: self::test_single_recipe_roundtrip_at_exact_encode_budget
# id: numeral_decode_one_replay_per_definition
#   proves: numeral_recipe_replay, numeral_strict_input
#   call: self::test_multiple_recipes_share_budget_without_second_replay
# id: numeral_replay_does_not_replace_structural_validation
#   proves: numeral_strict_input
#   call: self::test_recipe_packets_still_reject_invalid_structure
# id: numeral_decode_does_not_grant_mutable_validation_capability
#   proves: numeral_recipe_replay, numeral_strict_input
#   call: self::test_decoded_packets_are_revalidated_after_mutation
# === END CHECKS ===
"""Run: python -m unittest discover -s tests -p test_numeral_replay.py -v.

One exact recipe evaluation per definition during decode; typed structure is
still validated. No persistent validation flag is attached to decoded objects.
Only nonsecret in-memory fixtures. This tests recovery, not cryptographic secrecy.
"""
from dataclasses import replace
from fractions import Fraction
from unittest.mock import patch
import unittest

import numeral
from numeral import (BitBlock, Entry, Packet, PrimePath, Limits, Refused,
                     ResourceLimit, encode, decode, _uint, _blob)

A, B = chr(0xE000), chr(0xE001)


class NumeralReplayTests(unittest.TestCase):
    def packet(self):
        return Packet('replay', 0, (Entry(A, BitBlock(101,16), Fraction(1,7),
                                             1, PrimePath(101, ())),), A)

    def test_single_recipe_roundtrip_at_exact_encode_budget(self):
        packet = self.packet()
        limits = Limits(prime_work=5)
        wire = encode(packet, limits)
        decoded = decode(wire, limits)
        self.assertEqual(decoded, packet)
        self.assertEqual(Packet.restore(decoded, limits), BitBlock(101,16))
        with self.assertRaises(ResourceLimit): encode(packet, Limits(prime_work=4))
        with self.assertRaises(ResourceLimit): decode(wire, Limits(prime_work=4))

    def test_multiple_recipes_share_budget_without_second_replay(self):
        first = self.packet().entries[0]
        second = Entry(B, BitBlock(103,16), Fraction(2,7), 2, PrimePath(103, ()))
        packet = Packet('aggregate',0,(first,second),A+B+A)
        limits = Limits(prime_work=10)
        encoder = numeral._Primes(limits)
        wire = encode(packet, limits, _engine=encoder)
        self.assertEqual(encoder.work,10)
        decoder = numeral._Primes(limits)
        seen = []
        replay = PrimePath.replay
        def record(path,*args,**kwargs):
            seen.append(path)
            return replay(path,*args,**kwargs)
        with patch.object(PrimePath,'replay',record):
            restored = decode(wire, limits, _engine=decoder)
        self.assertEqual(restored,packet)
        self.assertEqual(seen,[first.recipe,second.recipe])
        self.assertEqual(decoder.work,encoder.work)
        with self.assertRaises(ResourceLimit): encode(packet, Limits(prime_work=9))
        with self.assertRaises(ResourceLimit): decode(wire, Limits(prime_work=9))

    def test_recipe_packets_still_reject_invalid_structure(self):
        # Construct deliberately invalid wire without asking the encoder to accept it.
        # Each valid recipe evaluates to 101; every other constraint remains checked.
        def definition(symbol=A,n=1,d=7,circle=1,length=16):
            return (_blob(symbol.encode()) + _uint(n)+_uint(d)+_uint(circle)+_uint(length)
                    + b'\x01'+_uint(101)+_uint(0))
        def wire(rows, symbols=A, declared=16, origin=b'replay'):
            return (numeral.MAGIC + _blob(origin)+_uint(0)+_uint(declared)
                    + _uint(len(rows))+b''.join(rows)+_blob(symbols.encode()))
        invalid = (
            wire([definition(circle=0)]), wire([definition(circle=8)]),
            wire([definition(n=2,d=1)]), wire([definition(length=0)]),
            wire([definition()],origin=b''), wire([definition()],declared=17),
            wire([definition()],symbols=B),
            wire([definition(),definition(n=2)],declared=16),
            wire([definition(),definition(symbol=B)],symbols=A+B,declared=32),
        )
        for i,data in enumerate(invalid):
            with self.subTest(case=i),self.assertRaises(Refused) as failure:
                decode(data,Limits(prime_work=100))
            self.assertNotIsInstance(failure.exception,ResourceLimit)
        self.assertEqual(decode(wire([definition()]),Limits(prime_work=5)), self.packet())

    def test_decoded_packets_are_revalidated_after_mutation(self):
        packet = decode(encode(self.packet()))
        # A successful earlier decode is not authority over changed fields.
        bad = replace(packet, entries=(replace(packet.entries[0],recipe=PrimePath(103,())),))
        for operation in (encode,numeral.accounting,Packet.restore,Packet.occurrences):
            with self.subTest(operation=operation.__name__),self.assertRaises(Refused):
                operation(bad)
        object.__setattr__(packet.entries[0].recipe,'seed',4)
        object.__setattr__(packet,'validate',lambda *args,**kwargs:16)
        object.__setattr__(packet,'_validate_fields',lambda *args,**kwargs:16)
        for operation in (encode,numeral.accounting,Packet.restore,Packet.occurrences):
            with self.subTest(operation=operation.__name__),self.assertRaises(Refused):
                operation(packet)


if __name__=='__main__': unittest.main()
