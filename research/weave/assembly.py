"""Switchable full-scope assembly; missing native laws never become identities.

Usage: Pipeline(switches, operators).encrypt(value, PublicContext(...)). Transport
operators remain explicitly classified even if combined with native operators.
Native state stays inside selected operations. The trace contains no stage payloads.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Mapping
from stages import STEPS
from stages.api import Blocked, Operator, PrivateContext, PublicContext, Transition

DEFAULTS = {'key': True, **{s.name: s.required for s in STEPS}}


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
        if self.switches['key'] and (context is None or context.public_key is None):
            problems.append('key: Q2/Q7/Q8, native public/private relation/key input missing')
        if type(context) is PrivateContext and self.switches['key'] and context.private_key is None:
            problems.append('key: private key missing for inverse')
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

    def recipe(self):
        return (('proposal', 'assembly-v2'), ('key', self.switches['key']), *(
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

    def decrypt(self, encrypted: Run, context: PrivateContext):
        if type(context) is not PrivateContext:
            raise TypeError('decrypt requires explicit PrivateContext')
        if not isinstance(encrypted, Run) or encrypted.direction != 'encrypt':
            raise TypeError('supply the encrypted lab result')
        if encrypted.recipe != self.recipe():
            raise ValueError('inverse profile/operator identities differ from forward lab recipe')
        return self._run(encrypted.payload, context, reverse=True)

    def _run(self, value, context, *, reverse):
        problems = self.problems(context)
        if problems:
            raise Blocked('; '.join(problems))
        if not self.switches['key']:
            context = (replace(context, public_key=None, private_key=None)
                       if type(context) is PrivateContext else replace(context, public_key=None))
        if not self.switches['corpus']:
            context = (replace(context, public_material={}, private_material={})
                       if type(context) is PrivateContext else replace(context, public_material={}))
        events, fixture, transport = [], False, False
        for step in reversed(STEPS) if reverse else STEPS:
            if not self.switches[step.name]:
                events.append((step.name, 'OFF'))
                continue
            op = self.operators[step.name]
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
        return Run(value, self.recipe(), classification, tuple(events),
                   'decrypt' if reverse else 'encrypt')
