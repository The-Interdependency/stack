# Pi radix prime scan v1

Classification: **BASE_DEPENDENT_STRUCTURE_MEASURED**

Standing: **COMPUTATION**

Base-independent digit law: **NOT_ESTABLISHED**

The first 500 fractional symbols of pi were generated twice at the recorded
decimal precisions. Every symbol agreed before analysis. Each digit `d` in
base `b` is also the exact unit-circle symbol
`exp(2*pi*i*d/b)`; degrees and radians are derived coordinates, not identity.

## Results

| Base | Factorization | phi(base) | Prime-valued symbols / prime digit-values | L1 eligible / prime | L2 eligible / prime | L3 eligible / prime | L4 eligible / prime | Resolution bits |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 30 | 2 * 3 * 5 | 8 | 175 / 10 | 481 / 175 | 123 / 74 | 123 / 48 | 125 / 37 | 2453.445297804260 |
| 60 | 2^2 * 3 * 5 | 16 | 142 / 17 | 491 / 142 | 140 / 70 | 142 / 43 | 140 / 36 | 2953.445297804260 |
| 359 | 359 | 358 | 96 / 71 | 499 / 96 | 497 / 48 | 496 / 34 | 495 / 24 | 4243.920016911526 |
| 360 | 2^3 * 3^2 * 5 | 96 | 78 / 72 | 500 / 78 | 117 / 42 | 117 / 21 | 117 / 19 | 4245.926548164837 |
| 361 | 19^2 | 342 | 102 / 72 | 499 / 102 | 468 / 41 | 467 / 32 | 466 / 21 | 4247.927513443585 |
| 720 | 2^4 * 3^2 * 5 | 192 | 80 / 128 | 500 / 80 | 117 / 24 | 117 / 19 | 117 / 20 | 4745.926548164837 |
| 2880 | 2^6 * 3^2 * 5 | 768 | 67 / 417 | 500 / 67 | 128 / 25 | 128 / 24 | 128 / 17 | 5745.926548164837 |

For multi-symbol values, the terminal digit gives an exact sieve:
`gcd(value, base) = gcd(last_digit, base)`. A block whose terminal digit
shares a factor with the base is composite in this domain. The contrast
between 359, 360, and 361 therefore measures base factorization rather than
merely alphabet size.

## Cross-base observations

- Decoded prime values recurring in at least two bases, using configured canonical blocks of length >= 2: **12**.
- Aligned positions with exactly equal reduced unit-circle phase in at least two bases: **9**.

### Recurrent decoded primes

| Prime | Occurrences `(base, position, length)` |
|---:|---|
| 61 | (30, 108, 2), (60, 362, 2) |
| 71 | (30, 443, 2), (60, 482, 2) |
| 107 | (30, 46, 2), (60, 464, 2) |
| 347 | (30, 113, 2), (30, 439, 2), (60, 193, 2) |
| 373 | (30, 315, 2), (60, 114, 2) |
| 443 | (30, 365, 2), (60, 31, 2) |
| 523 | (30, 66, 2), (360, 144, 2) |
| 587 | (30, 206, 2), (60, 397, 2) |
| 701 | (30, 429, 2), (60, 483, 2) |
| 809 | (30, 362, 2), (60, 337, 2) |
| 3529 | (30, 290, 3), (60, 149, 2) |
| 118907 | (360, 255, 2), (720, 405, 2) |

### Aligned exact angular phases

| Position | Turn | Symbols `(base:digit)` |
|---:|---:|---|
| 1 | 2/15 | 30:4, 60:8 |
| 4 | 0 | 30:0, 60:0 |
| 42 | 14/15 | 30:28, 60:56 |
| 51 | 11/60 | 60:11, 360:66 |
| 175 | 19/30 | 30:19, 720:456 |
| 182 | 1/5 | 30:6, 60:12 |
| 189 | 3/10 | 720:216, 2880:864 |
| 201 | 1/6 | 30:5, 60:10 |
| 500 | 1/3 | 30:10, 60:20 |

## Common information-horizon profile

This profile uses the longest whole-symbol prefix at or below **2400 bits** in every base.

| Base | Symbols used | Resolution bits | L1 eligible / prime | L2 eligible / prime | L3 eligible / prime | L4 eligible / prime |
|---:|---:|---:|---:|---:|---:|---:|
| 30 | 489 | 2399.469501252566 | 470 / 173 | 121 / 73 | 121 / 47 | 123 / 37 |
| 60 | 406 | 2398.197581817059 | 398 / 114 | 114 / 55 | 117 / 36 | 114 / 29 |
| 359 | 282 | 2393.570889538100 | 281 / 46 | 279 / 30 | 278 / 23 | 277 / 12 |
| 360 | 282 | 2394.702573164968 | 282 / 49 | 70 / 30 | 70 / 14 | 70 / 14 |
| 361 | 282 | 2395.831117582182 | 281 / 63 | 263 / 22 | 262 / 16 | 261 / 9 |
| 720 | 252 | 2391.946980275078 | 252 / 45 | 58 / 12 | 58 / 10 | 58 / 7 |
| 2880 | 208 | 2390.305444036572 | 208 / 30 | 55 / 6 | 55 / 8 | 55 / 4 |

- Recurrent decoded primes within the common information horizon: **8**.

| Prime | Occurrences `(base, position, length)` |
|---:|---|
| 61 | (30, 108, 2), (60, 362, 2) |
| 347 | (30, 113, 2), (30, 439, 2), (60, 193, 2) |
| 373 | (30, 315, 2), (60, 114, 2) |
| 443 | (30, 365, 2), (60, 31, 2) |
| 523 | (30, 66, 2), (360, 144, 2) |
| 587 | (30, 206, 2), (60, 397, 2) |
| 809 | (30, 362, 2), (60, 337, 2) |
| 3529 | (30, 290, 3), (60, 149, 2) |

## Interpretation

Primality belongs to each decoded integer independently of its notation.
Its occurrence as a selected block belongs to that radix representation.
A recurrence across bases is therefore a valid observation and a candidate
for a later law, not the law itself. Exact angular equality similarly shows
shared circle position without making the surrounding digit streams identical.

The fixed 500-symbol scans span different resolution depths. The common
2,400-bit profile changes the prefix length by base and keeps that second
comparison separate. Neither profile supplies a sampling theorem.
Resolution bits describe radix cell width, not measured entropy of pi.

## Reproduction

```bash
python research/pi-radix/pi_radix.py scan
python -m unittest discover -s research/pi-radix/tests -v
```

Receipt SHA-256: `b9dcf6c89a4e67eacd8b8dc1d62281b050055c83d1f4b368d551fe0b091a13c6`

## hmmm

A base-independent segmentation rule remains the next test. The same prime
arriving through two doors is a witness;
it has not yet testified that the doors share an architect.
