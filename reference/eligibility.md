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

## After L1 (David, 2026-11-13: keep the rule)

The pool is the **2,478 new codes** of the 2024-onwards import (`data/pool_2478.csv`; all 2,478 created in Medusa, every one has at least one source image).

| Measure | Value |
|---|---|
| By code letter (earrings E, necklaces N, rings R, bracelets B, watches W, other) | E 842, N 755, R 534, B 239, W 49, S 28, A 21, P 8, M 1, C 1 |
| Source images per code | 1: 1,484; 2: 530; 3: 222; 4: 128; 5: 60; 6+: 54 |
| Best source long edge (px) | median 1,600; min 286; max 4,608; under 1,500: 853; under 2,000: 1,711 |
| Folder the code first appears in | 2023: 1,982; "New 2024": 290; 2026: 125; 2025: 81 |

**A caveat that changes the eligible count:** the pool is defined by the import ("2024-onwards"), not by a date field. 1,982 codes first appear in zips named 2023 (e.g. "New July 2023"), so up to 1,982 of the 2,478 may have been introduced before the 2023-11-13 cutoff. There is no introduction-date column for them; the photo folder name is the only evidence, and it is a photography date. Until a real date is found (the supplier sheet, file modified times, the Hebrew folder names month by month) the eligible count for this pool is **between about 500 and 2,478**, not 2,478. Not yet done: families beyond the code letter (E/N/R/B only separate earrings, necklaces, rings, bracelets, not studs from hoops), difficulty, the 30 to 50 source sample, the pilot allocation, and the price table.
