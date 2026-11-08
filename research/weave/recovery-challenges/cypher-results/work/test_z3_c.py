import secrets, time
from collections import deque
from z3 import *

PREFIX = b'Prediction '
PRED = b'I expect recovery after the lane rules and route controls are disclosed.'
LINE = b'my human needs my help'
HEX_START = len(PREFIX)
HEX_END = HEX_START + 32
MSG_LEN = 141
N = MSG_LEN * 8
HEX_CHARS = list(range(ord('0'), ord('9') + 1)) + list(range(ord('a'), ord('f') + 1))
TEMPLATE = PREFIX + b'0' * 32 + b': ' + PRED + b'\n' + LINE + b'\n'
kb = [(b >> s) & 1 for b in TEMPLATE for s in range(7, -1, -1)]

def bits_of(data):
    return [(b >> s) & 1 for b in data for s in range(7, -1, -1)]

def pack(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        v = 0
        for k in range(8):
            v = (v << 1) | bits[i + k]
        out.append(v)
    return bytes(out)

def route(size, material, offset=0):
    rem = deque(range(size))
    out = []
    for i in range(size):
        p = (offset + i) % (8 * len(material))
        right = (material[p // 8] >> (7 - p % 8)) & 1
        out.append(rem.pop() if right else rem.popleft())
    return tuple(out)

def recover(wire, timeout_ms=120000):
    s = Solver()
    s.set('timeout', timeout_ms)
    msg = [Int(f'm{i}') for i in range(N)]
    for i in range(N):
        s.add(Or(msg[i] == 0, msg[i] == 1))
        if not (HEX_START * 8 <= i < HEX_END * 8):
            s.add(msg[i] == kb[i])
    for bi in range(HEX_START, HEX_END):
        base = bi * 8
        bval = Int(f'bv{bi}')
        s.add(bval == sum(msg[base + t] * (1 << (7 - t)) for t in range(8)))
        s.add(Or([bval == c for c in HEX_CHARS]))

    lo = [Int(f'lo{j}') for j in range(N + 1)]
    hi = [Int(f'hi{j}') for j in range(N + 1)]
    order = [Int(f'o{j}') for j in range(N)]
    s.add(lo[0] == 0, hi[0] == N - 1)
    msg_arr = Array('ma', IntSort(), IntSort())
    for i in range(N):
        s.add(msg_arr[i] == msg[i])
    for j in range(N):
        r = Bool(f'r{j}')
        s.add(If(r, order[j] == hi[j], order[j] == lo[j]))
        s.add(If(r,
                 And(hi[j + 1] == hi[j] - 1, lo[j + 1] == lo[j]),
                 And(lo[j + 1] == lo[j] + 1, hi[j + 1] == hi[j])))
        s.add(lo[j] <= hi[j])
        s.add(msg_arr[order[j]] == wire[j])

    t0 = time.time()
    res = s.check()
    dt = time.time() - t0
    print('check', res, 'in', round(dt, 2), 's', flush=True)
    if res != sat:
        return None
    m = s.model()
    return [m[msg[i]].as_long() for i in range(N)]

msg = PREFIX + secrets.token_hex(16).encode() + b': ' + PRED + b'\n' + LINE + b'\n'
mb = bits_of(msg)
wire = [mb[i] for i in route(N, secrets.token_bytes(256), 123)]
got = recover(wire)
print('ok', got is not None and pack(got) == msg)
