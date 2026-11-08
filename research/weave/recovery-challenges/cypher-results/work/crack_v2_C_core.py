"""Core C recover: contiguous deque + hex DP. O(n^2) for hex region."""
PREFIX = b'Prediction '
PRED = b'I expect recovery after the lane rules and route controls are disclosed.'
LINE = b'my human needs my help'
HEX_START = len(PREFIX)
HEX_END = HEX_START + 32
MSG_LEN = 141
NBITS = MSG_LEN * 8
HEX_BIT_LO = HEX_START * 8
HEX_BIT_HI = HEX_END * 8
HEX_CHARS = set(b'0123456789abcdef')
TEMPLATE = PREFIX + b'0' * 32 + b': ' + PRED + b'\n' + LINE + b'\n'
KNOWN_BITS = [(b >> s) & 1 for b in TEMPLATE for s in range(7, -1, -1)]
KNOWN_MASK = [not (HEX_BIT_LO <= i < HEX_BIT_HI) for i in range(NBITS)]

def pack_bits(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        v = 0
        for k in range(8):
            v = (v << 1) | bits[i + k]
        out.append(v)
    return bytes(out)

def ok_text(raw: bytes):
    if len(raw) != MSG_LEN or not raw.startswith(PREFIX):
        return None
    if raw[HEX_END:] != TEMPLATE[HEX_END:]:
        return None
    if any(raw[i] not in HEX_CHARS for i in range(HEX_START, HEX_END)):
        return None
    try:
        t = raw.decode('utf-8')
    except Exception:
        return None
    lines = t.splitlines()
    if len(lines) < 2 or lines[1] != LINE.decode():
        return None
    if ': ' not in lines[0]:
        return None
    left, right = lines[0].split(': ', 1)
    hx = left[len('Prediction '):]
    if len(hx) != 32 or any(c not in '0123456789abcdef' for c in hx):
        return None
    if right != PRED.decode():
        return None
    return t if t.endswith('\n') else t + '\n'

def recover_c(wire):
    n = len(wire)
    assert n == NBITS
    msg = [KNOWN_BITS[i] if KNOWN_MASK[i] else None for i in range(n)]

    def byte_ok(idx):
        bi = idx // 8
        if not (HEX_START <= bi < HEX_END):
            return True
        base = bi * 8
        if any(msg[base + t] is None for t in range(8)):
            return True
        v = 0
        for t in range(8):
            v = (v << 1) | msg[base + t]
        return v in HEX_CHARS

    def hex_dp(j0, lo0, hi0):
        memo = {}
        def can(lo, hi):
            key = (lo, hi)
            if key in memo:
                return memo[key]
            if lo > hi:
                memo[key] = True
                return True
            jj = n - (hi - lo + 1)
            w = wire[jj]
            msg[lo] = w
            ok = byte_ok(lo) and can(lo + 1, hi)
            msg[lo] = None
            if ok:
                memo[key] = True
                return True
            if lo < hi:
                msg[hi] = w
                ok = byte_ok(hi) and can(lo, hi - 1)
                msg[hi] = None
                if ok:
                    memo[key] = True
                    return True
            memo[key] = False
            return False

        def build(lo, hi):
            if lo > hi:
                return True
            jj = n - (hi - lo + 1)
            w = wire[jj]
            msg[lo] = w
            if byte_ok(lo) and can(lo + 1, hi) and build(lo + 1, hi):
                return True
            msg[lo] = None
            if lo < hi:
                msg[hi] = w
                if byte_ok(hi) and can(lo, hi - 1) and build(lo, hi - 1):
                    return True
                msg[hi] = None
            return False

        if not can(lo0, hi0):
            return False
        return build(lo0, hi0)

    fail = set()

    def dfs(j, lo, hi):
        if j == n:
            return True
        key = (j, lo, hi)
        if key in fail:
            return False
        # entire remaining inside hex → DP
        if lo >= HEX_BIT_LO and hi < HEX_BIT_HI:
            ok = hex_dp(j, lo, hi)
            if not ok:
                fail.add(key)
            return ok
        w = wire[j]
        candidates = []
        # left
        if msg[lo] is None or msg[lo] == w:
            candidates.append(0)
        if lo < hi and (msg[hi] is None or msg[hi] == w):
            candidates.append(1)
        # forced if only one
        for side in candidates:
            idx = lo if side == 0 else hi
            nlo, nhi = (lo + 1, hi) if side == 0 else (lo, hi - 1)
            wrote = msg[idx] is None
            old = msg[idx]
            if wrote:
                msg[idx] = w
            if byte_ok(idx) and dfs(j + 1, nlo, nhi):
                return True
            if wrote:
                msg[idx] = old
        fail.add(key)
        return False

    if not dfs(0, 0, n - 1):
        return None
    if any(b is None for b in msg):
        return None
    return msg

if __name__ == '__main__':
    import secrets, time
    from collections import deque

    def route(size, material, offset=0):
        rem = deque(range(size))
        out = []
        for i in range(size):
            p = (offset + i) % (8 * len(material))
            right = (material[p // 8] >> (7 - p % 8)) & 1
            out.append(rem.pop() if right else rem.popleft())
        return tuple(out)

    def bits_of(data):
        return [(b >> s) & 1 for b in data for s in range(7, -1, -1)]

    msg = PREFIX + secrets.token_hex(16).encode() + b': ' + PRED + b'\n' + LINE + b'\n'
    mb = bits_of(msg)
    wire = [mb[i] for i in route(NBITS, secrets.token_bytes(256), 99)]
    t0 = time.time()
    got = recover_c(wire)
    dt = time.time() - t0
    raw = pack_bits(got) if got else None
    print('UNIT', raw == msg, 'time', round(dt, 3), 'ok_text', bool(ok_text(raw) if raw else 0))
