# cl — items 8 and 9 on measured dates (2026-11-15)

Input: `data/original_dates.csv` (cs's measured EXIF and zip entry dates; copied in by cp per brief items 12 and 13). Script: `scripts/cl_dating_csv.py` (selftest 8 cases; proven to fail when the `0000:00:00` placeholder is let through as a date). Output: `data/cl_dating_measured.csv`, one row per SKU, **beside** cs's files; `eligibility.csv` and `dataset_2485.csv` untouched. No Space access, no images, 0 requests. Cutoff 2023-11-13 as cs set it; ladder as `cl-dating.md` (earliest plausible date per rung per SKU).

## Coverage
2,481 of the 2,485 dataset SKUs have rows (4,429 files: 4,423 new-code + 6 legacy). **Not in the file: `B6392A-3`, `BD148`, `E6398`, `N12287B`** (counted unknown, not dated). Zip date present and plausible on all 4,429 files; the 57 undated DEC25 sheet rows belong to no pool SKU (0 here).

## EXIF state, by file (4,429)
| ok | implausible (`0000:00:00`, pre-2000, sentinel) | absent | unreadable | editing software |
|---|---|---|---|---|
| 1,703 | 2,020 | 706 | 0 | **not measurable** (file has no Software tag) |
By SKU: 1,163 have an ok EXIF date; 1,318 have none (886 implausible-only, 432 all-absent) and fall to the zip date. Nothing was filled in.

## Source used and confidence (2,481 SKUs)
exif 1,163 / zip 1,318. High 899 (EXIF and zip same year), medium-disagree 264, low 925, low-disagree 393. No SKU needed folder-only.

## Cross-tabs (same calendar year)
| Pair | n | same year |
|---|---|---|
| EXIF vs zip | 1,163 | 899 (77%) |
| zip vs folder year | 2,481 | 1,680 (68%) |
| EXIF vs folder year | 1,163 | 569 (49%) |
| EXIF vs import (2026) | 1,163 | 111 (10%) |
| zip vs import | 2,481 | 125 (5%) |
EXIF runs *earlier* than zip by 13 to 14 years in 184 SKUs; 222 SKUs have EXIF in 2002 or 2003, and 180 of those have a zip date of 2016 or later (a camera clock never set is the likely cause; not proved). None of them changes a class: both dates are before the cutoff.

## Item 9: re-derived eligibility (3-year rule, best evidence)
**506 of 2,485 eligible (20.4%); 1,975 not; 4 unmeasured.** cs: 2,485. Difference **−1,979 (79.6%)**. The folder-only provisional run said 496; measured dates add 10.
| Family | eligible | not | n (dated) |
|---|---|---|---|
| earrings | 249 | 593 | 842 |
| necklaces | 132 | 626 | 758 |
| rings | 94 | 440 | 534 |
| other | 21 | 38 | 59 |
| bracelets | 10 | 229 | 239 |
| watches | 0 | 49 | 49 |
By origin: 504 new-code, 2 legacy. No SKU is "ambiguous": both rungs carry day precision.

**How much it depends on the rung.** Zip alone: 498 eligible. EXIF alone (1,163 SKUs): 270. Among SKUs with both, EXIF and zip agree on eligibility for 1,155 of 1,163; the 8 that differ are EXIF-eligible, zip-older. Using each SKU's *latest* file date instead of its earliest: 515. **The count sits at about 500 to 515 whichever rung or rule is used.**

**What the numbers do not say.** A zip entry date is the file's modification time, which can be a copy or edit date rather than a shoot date, and a camera clock can be wrong; neither is checkable here. cs's dataset keys the rule to the import batch (L2); the measured dates say the batch was mostly old stock. Whether the programme proceeds smaller, widens its window or stops is David's decision at the gate; no conclusion is drawn.

**Not covered:** the 4 missing SKUs; editing-software evidence; whether zip dates equal shoot dates; the 3,283 `known` and 2,054 `no-code` rows (outside the pool).
