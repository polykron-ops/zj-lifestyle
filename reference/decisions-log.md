# Decisions (L-range)

**L1. David, 2026-11-13. Keep the rule: only SKUs introduced in the last 3 years are eligible.** Consequence measured the same day: 0 of the 11,694 legacy production SKUs qualify (`reference/eligibility.md`), so the eligible pool is the 2024-onwards import, 2,478 new codes (`data/pool_2478.csv`, built by `scripts/pool_stats.py` from ZJ1 `reference/new-products-2024`). The 3,283 known codes that received images are legacy SKUs and stay out. Why: David's call, no reason given beyond "keep the rule". How to apply: every count that drives a decision uses the 2,478 pool; Unknown dates are excluded from such counts.

**L2. David, 2026-11-13. The pool is the last import batch** (the additional images added 2026-11-11, still to be processed with shadows): the 2,478 new codes, all eligible. Supersedes the dating doubt in L1's consequence; folder-name years are not introduction dates.
