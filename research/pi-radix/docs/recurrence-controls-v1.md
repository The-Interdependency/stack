# Cross-base recurrence controls v1

Standing: **COMPUTATION**

Question: is the observed recurrence count exceptional under the fixed controls?

| Control | Profile | Pi | Mean | Median | Central 95% range | >= Pi | Upper-tail rank |
|---|---|---:|---:|---:|---|---:|---|
| shared_number | fixed500 | 12 | 11.116 | 11 | 5–18 | 95/199 | 96/200 |
| shared_number | matched2400 | 8 | 7.975 | 8 | 3–14 | 110/199 | 111/200 |
| histogram_shuffle | fixed500 | 12 | 12.432 | 12 | 6–19 | 119/199 | 120/200 |
| histogram_shuffle | matched2400 | 8 | 9.422 | 9 | 5–15 | 148/199 | 149/200 |

## Interpretation

Pi has 8 shared primes; the primary control median is 8. The observed count is inside the empirical central 95% range.
The primary upper-tail rank is 111/200. This is a model-relative exploratory comparison, not a theorem or a confirmatory test.
The shared-number control retains dependencies between bases by encoding the same
8192-bit dyadic interval in all seven radices; interval-boundary checks certify
that any real in that interval has the reported prefixes. SHAKE256 generates
reproducible pseudorandom draws; ideal uniform draws are the modeling assumption.
The shuffle control preserves each pi profile's exact digit frequencies but
destroys order and common-number consistency. It is a separate sensitivity check.

## Scope and reproduction

Primary statistic: distinct prime values present in >=2 bases, lengths 2–4,
canonical nonzero leading symbols, 2400-bit resolution horizon. Fixed-500 is
secondary. Values are deduplicated within each base. The exact eight previously
observed primes were not treated as a preselected significance target.
All replicate counts and interval numerators are recorded in the JSON receipt.

```bash
python research/pi-radix/pi_radix.py scan
python research/pi-radix/recurrence_controls.py
python -m unittest discover -s research/pi-radix/tests -v
```

Receipt payload SHA-256: `046721c8a25ead20c22984b6de752fa861150ea0f138be0a5a062d7b217ec6ef`

## hmmm

A frequent pattern can still be useful. Its frequency alone does not distinguish
pi from the comparison ensemble; a proposed invariant needs its own executable rule.
