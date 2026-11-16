"""Switchable full-scope assembly; missing native laws never become identities.

Usage: Pipeline(switches, operators).encrypt(value, PublicContext(...)). Transport
operators remain explicitly classified even if combined with native operators.
Native state stays inside selected operations. The trace contains no stage payloads.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Mapping
import hashlib
import json
import math
from stages import STEPS
from stages.api import Blocked, Operator, PrivateContext, PublicContext, Transition
from stages.key import relation

DEFAULTS = {'key': True, **{s.name: s.required for s in STEPS}}


def plan_identity(parameters):
    """Type-preserving plan digest; never serialize native objects by repr.

    Usage: independently derive the same controls for each inverse stage.
    Digests are research comparison metadata, not authentication or secrecy.
    """
    def encode(value):
        kind = type(value)
        if value is None or kind in (bool, int, str):
            return (kind.__name__, value)
        if kind is float and math.isfinite(value):
            return ('float', value.hex())
        if kind is bytes:
            return ('bytes', value.hex())
        if kind in (tuple, list):
            return (kind.__name__, [encode(v) for v in value])
        if isinstance(value, Mapping) and all(type(k) is str for k in value):
            return ('mapping', [(k, encode(value[k])) for k in sorted(value)])
        raise Blocked('transform plan requires explicit finite, serializable controls')
    return hashlib.sha256(json.dumps(encode(parameters), separators=(',', ':')).encode()).hexdigest()


@dataclass(frozen=True)
class Switches:
    values: Mapping[str, bool] = field(default_factory=dict)

    def __post_init__(self):
        source = dict(self.values)
        if set(source) - set(DEFAULTS):
            raise ValueError('unknown switch: ' + ','.join(sorted(set(source)-set(DEFAULTS))))
        if any(type(value) is not bool for value in source.values()):
            raise TypeError('switch values must be literal Booleans')
        object.__setattr__(self, 'values', MappingProxyType({**DEFAULTS, **source}))

    def __getitem__(self, name):
        return self.values[name]

    @property
    def complete(self):
        return self['key'] and all(self[s.name] for s in STEPS if s.required)


@dataclass(frozen=True)
class Run:
    """Experimental result; recipe/events are not a proposed cipher wire format."""
    payload: Any = field(repr=False)
    recipe: tuple
    classification: str
    events: tuple[tuple[str, str], ...]
    direction: str
    plan_identities: tuple = field(default=(), repr=False)


class Pipeline:
    def __init__(self, switches: Switches | None = None,
                 operators: Mapping[str, Operator] | None = None, *,
                 allow_fixtures: bool = False):
        self.switches = switches or Switches()
        supplied = dict(operators or {})
        names = {s.name for s in STEPS}
        if set(supplied) - names:
            raise ValueError('unknown operator binding')
        if any(not isinstance(op, Operator) for op in supplied.values()):
            raise TypeError('bindings must be Operator objects')
        for step in STEPS:
            if step.builtin is not None:
                if step.name in supplied:
                    raise ValueError('literal operation cannot be replaced: ' + step.name)
                supplied[step.name] = step.builtin
        self.operators = MappingProxyType(supplied)
        if type(allow_fixtures) is not bool:
            raise TypeError('allow_fixtures must be Boolean')
        self.allow_fixtures = allow_fixtures

    def problems(self, context=None):
        problems = []
        if self.switches['key']:
            try:
                key_relation = relation(context)
                if key_relation[2] and not self.allow_fixtures:
                    problems.append('key: wiring fixture is not a native law')
            except Blocked as exc:
                problems.append(str(exc))
        if self.switches['bind'] and not (self.switches['key'] and self.switches['gonol']):
            problems.append('bind: incompatible ablation; native binding requires key and gonol')
        for step in STEPS:
            if not self.switches[step.name]:
                continue
            op = self.operators.get(step.name)
            if op is None:
                problems.append(step.name + ': ' + '/'.join(step.questions) + ', native operator missing')
            elif op.fixture and not self.allow_fixtures:
                problems.append(step.name + ': wiring fixture is not a native law')
        return tuple(problems)

    def recipe(self, context=None):
        key_relation = relation(context) if self.switches['key'] else None
        return (('proposal', 'assembly-v3'), ('key', self.switches['key'], key_relation), *(
            (s.name, self.switches[s.name],
             self.operators[s.name].identity if self.switches[s.name] and s.name in self.operators else None)
            for s in STEPS))

    def plan(self):
        return {
            'status': 'BLOCKED' if self.problems() else 'ASSEMBLED',
            'complete_cipher_implemented': False,
            'profile': 'full proposed scope' if self.switches.complete else 'ablation',
            'switches': dict(self.switches.values),
            'forward_order': [s.name for s in STEPS if self.switches[s.name]],
            'inverse_order': [s.name for s in reversed(STEPS) if self.switches[s.name]],
            'missing': self.problems(),
            'note': 'IMPLEMENTED.md separates executable proposals from missing native laws.',
        }

    def encrypt(self, value, context: PublicContext):
        if type(context) is not PublicContext:
            raise TypeError('encrypt takes PublicContext only; never PrivateContext')
        return self._run(value, context, reverse=False)

    def decrypt(self, encrypted: Run, context: PrivateContext, *, inverse_plans=None):
        """Optional per-stage plans must be independently reconstructed by the caller.

        Use this when native forward operators derive controls through Transition.
        The encrypted Run contains only comparison identities, never those controls.
        """
        if type(context) is not PrivateContext:
            raise TypeError('decrypt requires explicit PrivateContext')
        if not isinstance(encrypted, Run) or encrypted.direction != 'encrypt':
            raise TypeError('supply the encrypted lab result')
        if encrypted.recipe != self.recipe(context):
            raise ValueError('inverse profile/operator identities differ from forward lab recipe')
        names = tuple(s.name for s in STEPS if self.switches[s.name])
        if (type(encrypted.plan_identities) is not tuple
                or any(type(row) is not tuple or len(row) != 2
                       or type(row[0]) is not str or type(row[1]) is not str
                       or len(row[1]) != 64 or any(c not in '0123456789abcdef' for c in row[1])
                       for row in encrypted.plan_identities)
                or tuple(row[0] for row in encrypted.plan_identities) != names):
            raise ValueError('missing or reordered transform plan identities')
        if inverse_plans is not None and (not isinstance(inverse_plans, Mapping)
                or set(inverse_plans) != set(names)
                or any(not isinstance(p, Mapping) for p in inverse_plans.values())):
            raise ValueError('independently derived inverse plans must cover every enabled stage')
        return self._run(encrypted.payload, context, reverse=True,
                         expected_plans=dict(encrypted.plan_identities), inverse_plans=inverse_plans)

    def _run(self, value, context, *, reverse, expected_plans=None, inverse_plans=None):
        problems = self.problems(context)
        if problems:
            raise Blocked('; '.join(problems))
        if not self.switches['key']:
            context = (replace(context, public_key=None, private_key=None)
                       if type(context) is PrivateContext else replace(context, public_key=None))
        if not self.switches['corpus']:
            context = (replace(context, public_material={}, private_material={})
                       if type(context) is PrivateContext else replace(context, public_material={}))
        recipe = self.recipe(context)
        events, plans, transport = [], [], False
        fixture = self.switches['key'] and relation(context)[2]
        for step in reversed(STEPS) if reverse else STEPS:
            if not self.switches[step.name]:
                events.append((step.name, 'OFF'))
                continue
            op = self.operators[step.name]
            if reverse and inverse_plans is not None:
                context = replace(context, parameters=inverse_plans[step.name])
            identity = plan_identity(context.parameters)
            if reverse and expected_plans.get(step.name) != identity:
                raise ValueError('inverse transform plan differs before stage: ' + step.name)
            plans.append((step.name, identity))
            fixture = fixture or op.fixture
            transport = transport or op.scope == 'transport'
            result = (op.inverse if reverse else op.forward)(value, context)
            if isinstance(result, Transition):
                value = result.payload
                context = replace(context, parameters={**context.parameters, **result.parameters})
            else:
                value = result
            events.append((step.name, 'EXECUTED'))
        classification = ('WIRING_ONLY' if fixture else 'TRANSPORT_CANDIDATE' if transport else
                          'FULL_PROFILE_EXPERIMENT' if self.switches.complete else 'ABLATION_ONLY')
        return Run(value, recipe, classification, tuple(events),
                   'decrypt' if reverse else 'encrypt',
                   tuple(reversed(plans)) if reverse else tuple(plans))
