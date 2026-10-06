# === CHECKS ===
# id: check_numeral_all_8191_short_bitblocks
#   proves: numeral_exact_recovery
#   call: self::test_all_8191_short_bitblocks
#   mutates: none
#   cleanup: none
#
# id: check_numeral_leading_zeros_and_partial_byte_concatenation
#   proves: numeral_exact_recovery
#   call: self::test_leading_zeros_and_partial_byte_concatenation
#   mutates: none
#   cleanup: none
#
# id: check_numeral_large_integer_and_four_occurrences
#   proves: numeral_exact_recovery, numeral_accounting
#   call: self::test_large_integer_and_four_occurrences
#   mutates: none
#   cleanup: none
#
# id: check_numeral_origin_and_round_scope
#   proves: numeral_scoped_symbols
#   call: self::test_origin_and_round_scope
#   mutates: none
#   cleanup: none
#
# id: check_numeral_all_private_use_boundaries_and_utf8_width
#   proves: numeral_scoped_symbols
#   call: self::test_all_private_use_boundaries_and_utf8_width
#   mutates: none
#   cleanup: none
#
# id: check_numeral_prime_index_and_embedded_paths
#   proves: numeral_recipe_replay
#   call: self::test_prime_index_and_embedded_paths
#   mutates: none
#   cleanup: none
#
# id: check_numeral_prime_errors_and_budget_are_distinct
#   proves: numeral_recipe_replay, numeral_strict_input
#   call: self::test_prime_errors_and_budget_are_distinct
#   mutates: none
#   cleanup: none
#
# id: check_numeral_recipe_mismatch_does_not_fallback
#   proves: numeral_recipe_replay
#   call: self::test_recipe_mismatch_does_not_fallback
#   mutates: none
#   cleanup: none
#
# id: check_numeral_order_offsets_and_seven_occurrence_circles
#   proves: numeral_exact_recovery
#   call: self::test_order_offsets_and_seven_occurrence_circles
#   mutates: none
#   cleanup: none
#
# id: check_numeral_invalid_definitions_and_numeric_types
#   proves: numeral_strict_input
#   call: self::test_invalid_definitions_and_numeric_types
#   mutates: none
#   cleanup: none
#
# id: check_numeral_every_truncation_unknown_version_and_trailing_data
#   proves: numeral_strict_input
#   call: self::test_every_truncation_unknown_version_and_trailing_data
#   mutates: none
#   cleanup: none
#
# id: check_numeral_decoder_length_and_work_limits
#   proves: numeral_strict_input
#   call: self::test_decoder_length_and_work_limits
#   mutates: none
#   cleanup: none
#
# id: check_numeral_accounting_counts_every_byte
#   proves: numeral_accounting
#   call: self::test_accounting_counts_every_byte
#   mutates: none
#   cleanup: none
#
# id: check_numeral_fresh_process_recovery_and_no_overwrite
#   proves: numeral_exact_recovery
#   call: self::test_fresh_process_recovery_and_no_overwrite
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_numeral_fresh_process_prime_recipe
#   proves: numeral_recipe_replay
#   call: self::test_fresh_process_prime_recipe
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# === END CHECKS ===
"""Run: python -m unittest discover -s tests -p test_numeral.py -v.

Tests concern this representation and its exact replay, not native gonol geometry
or Weave security. No user data, network, or persistent writes outside tempdirs.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from numeral import (BitBlock, Entry, Packet, PrimePath, Limits, Refused,
                     ResourceLimit, encode, decode, accounting, _uint)

ROOT = Path(__file__).resolve().parents[1]
A, B = chr(0xE000), chr(0xE001)


def packet(block, symbol=A):
    return Packet("test-origin", 0, (Entry(symbol, block, Fraction(1, 7), 1),), symbol)


class NumeralTests(unittest.TestCase):
    def test_all_8191_short_bitblocks(self):
        checked = 0
        for length in range(13):
            for value in range(1 << length):
                block = BitBlock(value, length)
                p = packet(block) if length else Packet("empty", 0, (), "")
                restored = decode(encode(p)).restore()
                self.assertEqual(restored, block)
                self.assertEqual(BitBlock.from_bytes(block.to_bytes(), length), block)
                checked += 1
        self.assertEqual(checked, 8191)

    def test_leading_zeros_and_partial_byte_concatenation(self):
        self.assertNotEqual(BitBlock(5, 3), BitBlock(5, 8))
        rng = random.Random(71005)
        for _ in range(100):
            lengths = [rng.randrange(1, 65) for _ in range(12)]
            blocks = [BitBlock(rng.getrandbits(n), n) for n in lengths]
            entries = tuple(Entry(chr(0xE000+i), v, Fraction(i, 13), 1+i%7)
                            for i, v in enumerate(blocks))
            symbols = ''.join(e.symbol for e in entries)
            p = Packet("partials", 7, entries, symbols)
            expected = ''.join(format(v.value, f'0{v.length}b') for v in blocks)
            rebuilt = decode(encode(p)).restore()
            self.assertEqual(rebuilt, BitBlock(int(expected, 2), len(expected)))

    def test_large_integer_and_four_occurrences(self):
        data = bytes(range(256)) * 4096
        block = BitBlock.from_bytes(data)
        single = packet(block)
        p = replace(single, symbols=A * 4)
        wire = encode(p)
        self.assertEqual(decode(wire).restore().to_bytes(), data * 4)
        self.assertEqual(block.length, 8388608)
        self.assertLess(len(wire), len(data) * 2)
        self.assertGreater(len(encode(single)), len(data))
        # A small reference is real, but does not erase its definition cost.
        self.assertEqual(accounting(single)['symbol_utf8_bytes'], 3)
        self.assertGreater(accounting(single)['definition_bytes'], len(data))

    def test_origin_and_round_scope(self):
        p = packet(BitBlock(5, 8))
        q = replace(packet(BitBlock(9, 8)), origin="another-origin", round_id=2)
        self.assertEqual(p.symbols, q.symbols)
        self.assertNotEqual(decode(encode(p)).restore(), decode(encode(q)).restore())
        self.assertEqual(decode(encode(q)), q)

    def test_all_private_use_boundaries_and_utf8_width(self):
        for cp in (0xE000, 0xF8FF, 0xF0000, 0xFFFFD, 0x100000, 0x10FFFD):
            p = packet(BitBlock(7, 8), chr(cp))
            self.assertEqual(decode(encode(p)), p)
            self.assertEqual(accounting(p)['symbol_utf8_bytes'], 3 if cp < 0x10000 else 4)
        for symbol in ('', 'AB', '7', '\ud800', '\ufdd0', chr(0x10FFFF)):
            with self.assertRaises((Refused, UnicodeError)):
                encode(packet(BitBlock(7, 8), symbol))

    def test_prime_index_and_embedded_paths(self):
        recursion = PrimePath(2, (("next",),) * 8)
        self.assertEqual(recursion.replay(), (2, 3, 5, 11, 31, 127, 709, 5381, 52711))
        jump = PrimePath(5381, (("span", 10, 0, 2), ("next",), ("next",)))
        self.assertEqual(jump.replay(), (5381, 53, 241, 1523))
        binary = PrimePath(5381, (("span", 2, 0, 3), ("next",)))
        self.assertEqual(binary.replay(), (5381, 5, 11))
        # Both occurrences lead to 3, but the serialized route preserves which one.
        left = PrimePath(313, (("span", 10, 0, 1),))
        right = PrimePath(313, (("span", 10, 2, 1),))
        self.assertEqual(left.replay(), right.replay())
        self.assertNotEqual(left, right)
        for path in (jump, binary, left, right):
            value = path.replay()[-1]
            e = Entry(A, BitBlock(value, 32), Fraction(1, 7), 7, path)
            p = Packet("prime", 0, (e,), A * 3)
            self.assertEqual(decode(encode(p)), p)
            self.assertEqual(decode(encode(p)).restore(), p.restore())

    def test_prime_errors_and_budget_are_distinct(self):
        for path in (PrimePath(4, ()), PrimePath(True, ()),
                     PrimePath(5381, (("span", 10, 1, 2),)),
                     PrimePath(5381, (("span", 10, 3, 2),)),
                     PrimePath(5381, (("span", 2, 0, 0),)),
                     PrimePath(5381, (("span", True, 0, 1),)),
                     PrimePath(53, (("execute",),))):
            with self.assertRaises(Refused):
                path.replay()
        with self.assertRaises(ResourceLimit):
            PrimePath(101, (("next",),)).replay(Limits(prime_index=100))
        with self.assertRaises(ResourceLimit):
            PrimePath(101, ()).replay(Limits(prime_value=100))
        with self.assertRaises(ResourceLimit):
            PrimePath(101, (("next",),)).replay(Limits(sieve_bytes=16))
        with self.assertRaises(ResourceLimit):
            PrimePath(2, (("next",),) * 3).replay(Limits(recipe_steps=2))
        with self.assertRaises(ResourceLimit):
            PrimePath(101, ()).replay(Limits(prime_work=1))
        entries = (Entry(A, BitBlock(101, 16), Fraction(1, 7), 1, PrimePath(101, ())),
                   Entry(B, BitBlock(101, 16), Fraction(2, 7), 2, PrimePath(101, ())))
        p = Packet("aggregate-work", 0, entries, A+B)
        with self.assertRaises(ResourceLimit):
            encode(p, Limits(prime_work=8))
        with self.assertRaises(ResourceLimit):
            decode(encode(p), Limits(prime_work=8))

    def test_recipe_mismatch_does_not_fallback(self):
        entry = Entry(A, BitBlock(241, 16), Fraction(1, 7), 1, PrimePath(53, ()))
        with self.assertRaises(Refused):
            encode(Packet("mismatch", 0, (entry,), A))
        # Arbitrary composite values are fully admitted by literal representation.
        p = packet(BitBlock(2**1000-2, 1001))
        self.assertEqual(decode(encode(p)), p)

    def test_order_offsets_and_seven_occurrence_circles(self):
        entries = tuple(Entry(chr(0xE000+i), BitBlock(i, 16), Fraction(i, 8), i+1)
                        for i in range(7))
        symbols = ''.join(e.symbol for e in entries) * 3
        p = Packet("occurrences", 5, entries, symbols)
        occurrences = decode(encode(p)).occurrences()
        self.assertEqual(len(occurrences), 21)
        for i, (symbol, offset, ordinal, circle) in enumerate(occurrences):
            self.assertEqual((symbol, offset, ordinal, circle), (symbols[i], i*16, i//7, i%7+1))

    def test_invalid_definitions_and_numeric_types(self):
        p = packet(BitBlock(5, 8))
        bad = (replace(p, origin=""), replace(p, round_id=True),
               replace(p, entries=list(p.entries)), replace(p, symbols=B),
               replace(p, entries=p.entries * 2),
               replace(p, entries=(replace(p.entries[0], circle=0),)),
               replace(p, entries=(replace(p.entries[0], circle=True),)),
               replace(p, entries=(replace(p.entries[0], angle=0.5),)),
               replace(p, entries=(replace(p.entries[0], angle=Fraction(2)),)),
               replace(p, entries=(replace(p.entries[0], block=BitBlock(0, 0)),)))
        for item in bad:
            with self.assertRaises(Refused):
                encode(item)
        for value, length in ((True, 1), (0, False), (-1, 1), (8, 3), (0, -1)):
            with self.assertRaises(Refused):
                BitBlock(value, length)
        with self.assertRaises(Refused):
            BitBlock.from_bytes(b'\x01', 1)
        with self.assertRaises(Refused):
            BitBlock.from_bytes(b'\x00\x00', 1)

    def test_every_truncation_unknown_version_and_trailing_data(self):
        wire = encode(packet(BitBlock(5, 8)))
        for offset in range(len(wire)):
            with self.assertRaises(Refused):
                decode(wire[:offset])
        for corrupt in (b'bad!' + wire[4:], wire+b'\x00'):
            with self.assertRaises(Refused):
                decode(corrupt)
        # Origin-length varint widened noncanonically from one byte to two.
        with self.assertRaises(Refused):
            decode(wire[:4] + bytes([wire[4] | 128, 0]) + wire[5:])
        # A structurally valid modification need not be detected: no authentication claim.
        changed = encode(packet(BitBlock(6, 8)))
        self.assertEqual(decode(changed).restore(), BitBlock(6, 8))

    def test_decoder_length_and_work_limits(self):
        p = packet(BitBlock(5, 8))
        wire = encode(p)
        with self.assertRaises(ResourceLimit):
            decode(wire, Limits(output_bits=7))
        with self.assertRaises(ResourceLimit):
            decode(wire, Limits(wire_bytes=len(wire)-1))
        with self.assertRaises(ResourceLimit):
            encode(replace(p, symbols=A*2), Limits(occurrences=1))
        with self.assertRaises(ResourceLimit):
            encode(p, Limits(wire_bytes=3))
        # Byte-budget preflight precedes literal materialization.
        with patch.object(BitBlock, 'to_bytes', side_effect=AssertionError('allocated early')):
            with self.assertRaises(ResourceLimit):
                encode(p, Limits(wire_bytes=3))
        # Declared output mismatch, without changing the remainder of the packet.
        output_pos = 4 + 1 + len(p.origin.encode()) + 1
        wrong = wire[:output_pos] + _uint(9) + wire[output_pos+1:]
        with self.assertRaises(Refused):
            decode(wrong)

    def test_accounting_counts_every_byte(self):
        p = packet(BitBlock.from_bytes(b'\x00AB' * 32))
        for symbols in (A, A*7):
            candidate = replace(p, symbols=symbols)
            stats = accounting(candidate)
            self.assertEqual(stats['total_bytes'], len(encode(candidate)))
            self.assertEqual(stats['total_bytes'], stats['header_bytes']+
                             stats['definition_bytes']+stats['occurrence_bytes'])
            self.assertEqual(stats['source_bits'], candidate.restore().length)
        path = PrimePath(5381, (("span", 10, 0, 2), ("next",), ("next",)))
        e = Entry(A, BitBlock(1523, 16), Fraction(1, 7), 1, path)
        p = Packet("recipe-cost", 0, (e,), A)
        # The tested recipe is real but larger than storing this small block.
        self.assertGreater(accounting(p)['total_bytes'], 2)

    def test_fresh_process_recovery_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            src, wire, restored = root/'source', root/'packet', root/'restored'
            data = bytes(range(256))*8 + b'\x00\x00\xff'
            src.write_bytes(data)
            command = [sys.executable, str(ROOT/'numeral.py')]
            encoded = subprocess.run(command + ['bind', str(src), str(wire), '--origin',
                'process-test', '--angle', '1/7', '--circle', '3'], capture_output=True)
            self.assertEqual(encoded.returncode, 0, encoded.stderr)
            src.unlink()
            decoded = subprocess.run(command+['recover', str(wire), str(restored)], capture_output=True)
            self.assertEqual(decoded.returncode, 0, decoded.stderr)
            self.assertEqual(restored.read_bytes(), data)
            again = subprocess.run(command+['recover', str(wire), str(restored)], capture_output=True)
            self.assertEqual(again.returncode, 2)
            self.assertEqual(restored.read_bytes(), data)

    def test_fresh_process_prime_recipe(self):
        path = PrimePath(5381, (("span", 10, 0, 2), ("next",), ("next",)))
        p = Packet("prime-process", 0, (Entry(A, BitBlock(1523, 16), Fraction(1, 7), 3, path),), A)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wire, result = root/'recipe', root/'recovered'
            wire.write_bytes(encode(p))
            completed = subprocess.run([sys.executable, str(ROOT/'numeral.py'),
                'recover', str(wire), str(result)], capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(result.read_bytes(), b'\x05\xf3')


if __name__ == '__main__':
    unittest.main()
