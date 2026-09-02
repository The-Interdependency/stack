# AHBG submission package

Pass 5 shipping material. The source-side, buildable parts live in the repo;
everything that requires a live external account is listed in
[`SUBMISSION_BLOCKERS.md`](SUBMISSION_BLOCKERS.md).

| Asset | File |
|---|---|
| **Galaxy Store publication runbook** | `GALAXY_STORE_RUNBOOK.md` |
| Store listing copy | `STORE_LISTING.md` |
| Privacy declaration | `PRIVACY_POLICY.md` |
| ≤2-minute device demo | `DEMO_STORYBOARD.md` |
| Devpost material | `DEVPOST.md` |
| RevenueCat production provisioning | `REVENUECAT_PROVISIONING.md` |
| Remaining external blockers | `SUBMISSION_BLOCKERS.md` |

## Shipping path

**Galaxy first** (Shipaton accepts a published Galaxy Store URL; no Samsung
publishing fee and no Play 12-tester/14-day gate). RevenueCat is upgraded to
`10.19.1` with the `purchases-store-galaxy` backend in this line.

## Current release identity

- App id: `org.interdependency.ahbg`
- versionCode `2`, versionName `0.2.0`
- Production runtime endpoint: `https://ahbg.interdependentway.org`
- Entitlement: `benchmark_lab` (RevenueCat `10.19.1` + Galaxy backend)
- Construction authority: `ucns.mobius-seed-construction@0.1.0`
  (The-Interdependency/ucns, merged `828c0b8`)
