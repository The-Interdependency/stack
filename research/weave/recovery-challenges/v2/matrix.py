# ratios: loc_comments=115:33 imports_exports=4:8 calls_definitions=40:8
"""Finite coverage census and predictions made before any generated attack attempt.

The matrix is exhaustive for two-symbol counts <= 3; higher-order coverage is
explicitly bounded. Secret selections are synthetic independent research inputs,
not keys derived by the missing native asymmetric relation.
"""
# === MODULE_BUILD ===
# id: challenge_matrix
#   module_name: matrix
#   module_kind: experiment
#   summary: enumerate coverage without quietly dropping difficult schedules
#   owner: Erin Spencer
#   public_surface: schedules, parameters, message
#   internal_surface: pair words and independent synthetic choices
#   tests: test_harness.py
#   rollout: research v2
#   rollback: remove v2
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: declared_census
#   given: the declared operation alphabet
#   then: enumerate every promised singleton and pair word, with no count above three
# id: frozen_prediction
#   given: a schedule before encryption
#   then: create its probable-outcome message and exact requested second line
# === END CONTRACTS ===
from itertools import combinations, permutations, product
from fractions import Fraction
from collections import Counter
import secrets

CORE = ('N', 'A', 'U', 'S', 'W', 'B')
REFLECTION = ('R', 'B', 'S', 'W')
LINE = 'my human needs my help'
MISSING = {
    'whole_message_private_gonol': 'No arbitrary-message/private-gonol forward/inverse law.',
    'private_gonol_binding': 'stages/bind.py supplies a declaration, no operator.',
    'asymmetric_key_relation': 'stages/key.py requires a caller-supplied law; none exists.',
    'cryptographic_thread_dependency': 'Occurrence lanes exist; complementary secret reconstruction does not.',
    'native_corpus_key_binding': 'Normalization validates corpus/padding; private reconstruction binding is absent.',
    'authentication': 'stages/auth.py declares Q10 but provides no authenticator.',
    'replay_state': 'No stateful replay rejection mechanism is implemented.',
}


def pair_words(a, b):
    """All 62 non-singleton binary words with both symbol counts in 1..3."""
    for length in range(2, 7):
        for word in product((a, b), repeat=length):
            if 1 <= word.count(a) <= 3 and 1 <= word.count(b) <= 3:
                yield word


def byte_schedules(alphabet):
    found = {tuple([op]*n) for op in alphabet for n in (1, 2, 3)}
    for a, b in combinations(alphabet, 2):
        found.update(pair_words(a, b))
    for size in range(3, len(alphabet)+1):
        for group in combinations(alphabet, size):
            found.add(group)
            found.add(group[::-1])
    for order in (alphabet, alphabet[::-1]):
        for n in (2, 3):
            found.add(order*n)
            for op in alphabet:
                for gap in range(len(order)+1):
                    found.add(order[:gap] + (op,)*(n-1) + order[gap:])
    return sorted(found, key=lambda s: (len(s), s))


def transport_valid(schedule, initial=1):
    lanes = initial
    for op in schedule:
        if op == 'X':
            if lanes != 1:
                return False
            lanes = 3
        elif op == 'J':
            if lanes == 1:
                return False
            lanes = 1
        elif op == 'W' and lanes != 1:
            return False
    return True


def transport_schedules():
    """Exhaustive admissible pair words plus all legal five-stage orders x1..3."""
    names = ('X', 'J', 'C', 'I', 'W')
    candidates = {tuple([x]*n) for x in names for n in (1, 2, 3)}
    for a, b in combinations(names, 2):
        candidates.update(pair_words(a, b))
    for order in permutations(names):
        for n in (1, 2, 3):
            candidates.add(order*n)
    for n in (1, 2, 3):
        candidates.add(('X', 'J')*n)
    accepted, refused = [], []
    for seq in sorted(candidates, key=lambda s: (len(s), s)):
        # A join-only input is a declared multi-lane domain fixture, not hidden split.
        initial = 3 if seq[0] == 'J' else 1
        (accepted if transport_valid(seq, initial) else refused).append((seq, initial))
    return accepted, refused


def schedules():
    rows = [{'family': 'byte', 'schedule': list(s)} for s in byte_schedules(CORE)]
    rows += [{'family': 'reflection', 'schedule': list(s)}
             for s in byte_schedules(REFLECTION) if 'R' in s]
    accepted, _ = transport_schedules()
    rows += [{'family': 'transport', 'schedule': list(s), 'initial_lanes': n}
             for s, n in accepted]
    rows += [{'family': 'cycle', 'schedule': ['N'] + ['A', 'S']*n,
              'round_count': n} for n in (1, 2, 3)]
    if any(max(Counter(r['schedule']).values()) > 3 for r in rows):
        raise AssertionError('per-operation cap violated')
    return rows


def round_parameters():
    paths = [
        {'seed': 53, 'steps': [['next'], ['next']]},
        {'seed': 5381, 'steps': [['span', 10, 0, 2], ['next'], ['next']]},
        {'seed': 13, 'steps': [['span', 2, 0, 2], ['next']]},
    ]
    circle_order = list(range(1, 8))
    secrets.SystemRandom().shuffle(circle_order)
    spaces = [Fraction(secrets.randbelow(131072), 65536) for _ in range(8)]
    return {'prime_path': secrets.choice(paths), 'arities': secrets.choice([[3], [5], [7], [3,5,7], [7,3,5]]),
            'circle_order': circle_order, 'spaces': [[x.numerator, x.denominator] for x in spaces],
            'end_order': secrets.choice(['first-last', 'last-first'])}


def parameters(row):
    p = {'scope': 'v2:' + secrets.token_hex(8), 'bucket_bytes': secrets.choice([96,128,192]),
         'corpus_bit_offset': secrets.randbelow(8192), 'corpus_hex': secrets.token_hex(256),
         'spec': round_parameters(), 'initial_lanes': row.get('initial_lanes', 1),
         'thread_count': secrets.choice([3,5,7]), 'lane_rotation': secrets.randbelow(7),
         'inter_arity': secrets.choice([3,5,7])}
    if row['family'] == 'cycle':
        p['rounds'] = [round_parameters() for _ in range(row['round_count'])]
    return p


def message(row):
    seq = row['schedule']
    if row['family'] == 'transport':
        prediction = 'I expect recovery after the lane rules and route controls are disclosed.'
    elif 'A' in seq:
        prediction = 'I expect source-guided recovery; hidden placement and order may delay the attempt.'
    elif all(x in ('N', 'U') for x in seq):
        prediction = 'I expect early recovery because the literal containers retain the message bytes.'
    elif all(x in ('B', 'R') for x in seq):
        prediction = 'I expect early recovery by testing reflections; even repetitions can cancel.'
    else:
        prediction = 'I expect recovery once the permutation rules and selected order are known.'
    # Padding is part of the prediction's first line, never the required second line.
    first = 'Prediction ' + secrets.token_hex(16) + ': ' + prediction
    if row['family'] == 'reflection':
        while len((first + '\n' + LINE + '\n').encode()) % 3:
            first += ' '
    return (first + '\n' + LINE + '\n').encode()
# ratios: loc_comments=115:33 imports_exports=4:8 calls_definitions=40:8
