# === CHECKS ===
# id: numeral_fraction_internals_are_canonical
#   proves: numeral_exact_recovery, numeral_strict_input
#   call: self::test_numeral_rejects_mutated_fraction_fields
# id: route_relation_is_replayed_before_planning
#   proves: prime_split_replay
#   call: self::test_plan_rejects_inconsistent_direct_and_mutated_routes
# id: scheduler_validation_budget_is_shared
#   proves: prime_split_replay, cycle_strict_refusal
#   call: self::test_route_planning_uses_one_charged_engine
# id: recovery_uses_trusted_geometry
#   proves: binary_coordinate_recovery, binary_source_refusal
#   call: self::test_recovery_cannot_use_shadowed_geometry_to_accept_coordinates
# === END CHECKS ===
"""Replay three terminal-review gaps using only nonsecret local records.

Usage: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_terminal_records.py -v
These tests mutate supplied records, not trusted producer code or runtime classes.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import os
import unittest

import cycle
import native_binary as native
import numeral
from numeral import BitBlock, Entry, Packet, PrimePath, Limits, Refused, ResourceLimit
from prime_schedule import Route, plan

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ['WEAVE_SOURCES'])
SPACES = tuple(Fraction(i, 9) for i in range(8))


def bad_fraction(numerator, denominator):
    value = Fraction(1, 2)
    object.__setattr__(value, '_numerator', numerator)
    object.__setattr__(value, '_denominator', denominator)
    return value


class TerminalRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geometry = native.Geometry(SOURCES/'ucns')

    def table(self, geometry):
        origin = native.ByteOrigin(b'ABxABy', 'terminal', 0, geometry)
        return native.close_sequences(origin, (b'AB', b'x', b'y'), (0,1,0,2), (1,2,3), SPACES)

    def recovery(self, table):
        items = native.SequenceTable.wire_occurrences(table)
        return dict(scope=table.origin.scope, message_origin=table.origin.message_origin,
                    round_id=0, origin_identity=table.origin.identity, byte_length=6,
                    blocks=tuple(d.data for d in table.definitions), circles=(1,2,3),
                    spaces=SPACES, counts=tuple(sum(o.circle == c for _,o in items) for c in range(1,8)),
                    wire_order=tuple(i for i,_ in items),
                    source_turns=tuple(native.Geometry.lift(table.origin.geometry,o.source_state) for _,o in items))

    def test_numeral_rejects_mutated_fraction_fields(self):
        class EqualInt(int):
            def __eq__(self, other): return True
        for n,d in ((2,2),(0,2),(-1,-2),(1,0),(True,2),(1,EqualInt(2)),(1.0,2)):
            angle = bad_fraction(n,d)
            p = Packet('fraction',0,(Entry(chr(0xE000),BitBlock(7,8),angle,1),),chr(0xE000))
            for operation in (numeral.encode,numeral.accounting,Packet.restore,Packet.occurrences):
                with self.subTest(n=n,d=d,operation=operation.__name__), self.assertRaises(Refused):
                    operation(p)
        for angle in (Fraction(0),Fraction(1,2),Fraction(3,2)):
            p=Packet('valid',0,(Entry(chr(0xE000),BitBlock(7,8),angle,1),),chr(0xE000))
            self.assertEqual(numeral.decode(numeral.encode(p)),p)

    def test_native_rejects_noncanonical_fraction_inputs(self):
        g = self.geometry
        axis = native.Geometry.axis(g,'0'*64,8,0)
        for value in (bad_fraction(2,2),bad_fraction(0,2),bad_fraction(1,0),bad_fraction(True,2)):
            with self.subTest(operation='placed'),self.assertRaises(native.BinaryError):
                native.Geometry.placed(g,axis,value)
            with self.subTest(operation='recover'),self.assertRaises(native.BinaryError):
                native.Geometry.recover_axis(g,'0'*64,8,value,Fraction(0))

    def test_plan_rejects_inconsistent_direct_and_mutated_routes(self):
        path=PrimePath(53,(('next',),));good=Route.evaluate(path)
        bad=(Route(path,good.trace,0), Route(path,(53,239),good.determinant),
             Route(PrimePath(59,()),good.trace,good.determinant),
             Route(path,list(good.trace),good.determinant),
             Route(path,good.trace,True))
        for value in bad:
            object.__setattr__(value,'validate',lambda *a,**k: good.determinant)
            with self.subTest(value=value),self.assertRaises(Refused):plan(128,value,(3,5,7))
        mutated=Route.evaluate(path)
        object.__setattr__(mutated,'determinant',0)
        with self.assertRaises(Refused):plan(128,mutated,(3,5,7))
        self.assertEqual(plan(128,Route(path,good.trace,good.determinant),(3,5,7)),plan(128,good,(3,5,7)))

    def test_plan_rejects_spoofed_trace_scalars_and_replays_actual_path(self):
        class EqualInt(int):
            def __eq__(self, other):return True
        route=Route.evaluate(PrimePath(101,()))
        for changed in (replace(route,trace=(EqualInt(101),)),replace(route,determinant=EqualInt(route.determinant))):
            with self.assertRaises(Refused):plan(128,changed,(3,5,7))
        called=[]
        object.__setattr__(route.path,'replay',lambda *a,**k: called.append(1) or (101,))
        object.__setattr__(route.path,'seed',4)
        with self.assertRaises(Refused):plan(128,route,(3,5,7))
        self.assertEqual(called,[])

    def test_route_planning_uses_one_charged_engine(self):
        # Seed 101 costs one step plus four trial divisors: five units per replay.
        for budget in (9,10):
            limits=Limits(prime_work=budget);engine=numeral._Primes(limits)
            route=Route.evaluate(PrimePath(101,()),limits,engine=engine)
            self.assertEqual(engine.work,5)
            if budget==9:
                with self.assertRaises(ResourceLimit):plan(128,route,(3,5,7),limits=limits,engine=engine)
            else:
                result=plan(128,route,(3,5,7),limits=limits,engine=engine)
                self.assertEqual(sum(result.lengths),128)
                self.assertEqual(engine.work,10)

    def test_cycle_shares_route_validation_work_across_evaluation_and_plan(self):
        p=cycle.Profile.read((ROOT/'profiles/cycle-v1.json').read_bytes())
        spec=replace(p.rounds[0],path=PrimePath(101,()))
        p=replace(p,rounds=(spec,))
        with self.assertRaises(ResourceLimit):
            cycle.forward(b'ABxABy',b'corpus',p,SOURCES,cycle.CycleLimits(prime_work=9))
        wire,_=cycle.forward(b'ABxABy',b'corpus',p,SOURCES,cycle.CycleLimits(prime_work=10))
        with self.assertRaises(ResourceLimit):
            cycle.reverse(wire,b'corpus',p,SOURCES,cycle.CycleLimits(prime_work=9))
        self.assertEqual(cycle.reverse(wire,b'corpus',p,SOURCES,cycle.CycleLimits(prime_work=10)),b'ABxABy')

    def test_recovery_cannot_use_shadowed_geometry_to_accept_coordinates(self):
        geometry=native.Geometry(SOURCES/'ucns');table=self.table(geometry);args=self.recovery(table)
        items=native.SequenceTable.wire_occurrences(table)
        expected_axes=iter(o.source_axis for _,o in items);called=[]
        object.__setattr__(geometry,'recover_axis',lambda *a,**k: called.append('recover') or next(expected_axes))
        object.__setattr__(geometry,'lift',lambda state: called.append('lift') or Fraction(1,16))
        args['source_turns']=(Fraction(1,16),)*len(items)
        with self.assertRaises(native.BinaryError):native.recover_sequences(geometry,**args)
        self.assertEqual(called,[])
        good=self.recovery(table)
        self.assertEqual(native.recover_sequences(geometry,**good).restore(),b'ABxABy')
        self.assertEqual(called,[])

    def test_recovery_axis_constructor_ignores_instance_override(self):
        geometry=native.Geometry(SOURCES/'ucns');called=[]
        object.__setattr__(geometry,'axis',lambda *a,**k: called.append(1) or None)
        result=native.Geometry.recover_axis(geometry,'0'*64,8,Fraction(3,8),Fraction(0))
        self.assertEqual(result.axis_ordinal,3)
        self.assertEqual(result.origin_sha256,'0'*64)
        self.assertEqual(called,[])

    def test_cycle_uses_trusted_lift_for_supplied_geometry(self):
        geometry=native.Geometry(SOURCES/'ucns');p=cycle.Profile.read((ROOT/'profiles/cycle-v1.json').read_bytes())
        data=b'ABxABy';root=native.ByteOrigin(data,p.scope,0,geometry).message_origin
        args=dict(api=native,geometry=geometry,scope=p.scope,root=root,round_id=0,spec=p.rounds[0])
        expected,_=cycle.affix(data,**args);called=[]
        object.__setattr__(geometry,'lift',lambda *a: called.append(1) or Fraction(0))
        actual,_=cycle.affix(data,**args)
        self.assertEqual(actual,expected)
        self.assertEqual(cycle.unaffix(actual,**args),data)
        self.assertEqual(called,[])


if __name__=='__main__':unittest.main()
