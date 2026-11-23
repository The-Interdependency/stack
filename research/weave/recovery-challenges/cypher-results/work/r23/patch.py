s=open('kport3.py').read()
s=s.replace("# Round 21: kissat404","# Round 23 (Nov 23 daily): adds 'nearK' mode = planted wires with K random wire bits flipped (near-miss negative).\n# Round 21: kissat404")
old="""if mode == 'rand':
    rng = random.Random(2000+seed); wl = [[rng.randrange(2) for _ in l] for l in wl]"""
assert old in s
s=s.replace(old, old+"""
elif mode.startswith('near'):
    K = int(mode[4:]); rng = random.Random(3000+seed); wl = [list(l) for l in wl]
    pos = [(i, j) for i, l in enumerate(wl) for j in range(len(l))]
    for i, j in rng.sample(pos, K): wl[i][j] ^= 1""")
open('kport3.py','w').write(s)
