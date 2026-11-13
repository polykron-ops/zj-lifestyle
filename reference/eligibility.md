# Eligibility: step 1 of the dataset round (cs, 2026-11-13)

Rule: only SKUs introduced in the last 3 years (cutoff 2023-11-13). `introduction_date` is recovered from the legacy databases, read-only, by `scripts/eligibility.py` (output `data/eligibility.csv`, one row per production SKU).

| Pool | SKUs | Eligible | Ineligible | Unknown |
|---|---|---|---|---|
| Legacy production set (`zj1-manifests/production.csv`, the 11,694 frozen images) | 11,694 | **0** | 11,671 | 23 |
| of which tamirzuman (`products.creation_date`) | 9,883 | 0 | 9,860 | 23 |
| of which saphirim (`wp_posts.post_date`) | 1,811 | 0 | 1,811 | 0 |

- **Latest legacy introduction date is in 2023 (7 SKUs, all before the cutoff); 2022 has 55, 2021 136.** 9,860 of 9,883 tamirzuman SKUs and all 1,811 saphirim SKUs have a recoverable date; 23 tamirzuman SKUs have no row in `products` and stay Unknown (excluded from any count that drives a decision).
- **The legacy set the programme was meant for is entirely outside the 3-year rule.** The eligible pool, if the rule stands, is the 2024-onwards import (`reference/new-products-2024/manifest.csv` in ZJ1: 2,478 new products and 3,972 images attached to existing SKUs), which was photographed, not the "never re-photographed" set. That contradiction is the finding: either the rule or the target set has to change before anything else is measured. Decision for David; not a thing to resolve here.
- Not yet done: the SKU-level dataset CSV, families, source sample, difficulty, pilot allocation, price table. They are measured against the pool David chooses, so they wait for his answer on this one line (see `reference/open-decisions` in ZJ1).

Reproduce: `python scripts/eligibility.py` (needs `C:/Dev/ZJ1/...` archives and `C:/Dev/zj1-manifests/production.csv`).
