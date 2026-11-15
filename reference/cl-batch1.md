# cl — items 15 and 16: the eligibility curve and batch 1 (2026-11-15)

US$0, no network. Scripts: `scripts/cl_curve.py` (table and batch-1 check), `scripts/cl_template_plan.py [skus.txt]` (now takes an optional SKU list; the no-argument run is unchanged and still sums to 2,485; with the batch-1 list it sums to 528, and the sum assertion fired on a broken first version). Data: `data/cl_eligibility_curve.csv`, `data/batch1_skus.txt`, chart `reference/cl-eligibility-curve.png`.

## Item 15: eligible SKUs by cutoff (date_used within N years of 2026-11-15; 2,481 dated)
| yrs | earrings | necklaces | rings | bracelets | other | watches | **total** | added vs previous year |
|---|---|---|---|---|---|---|---|---|
| 1 | 85 | 17 | 4 | 0 | 19 | 0 | **125** | 125 |
| 2 | 146 | 54 | 21 | 3 | 21 | 0 | **245** | 120 |
| 3 | 249 | 132 | 94 | 10 | 21 | 0 | **506** | 261 |
| 4 | 249 | 148 | 95 | 11 | 21 | 0 | **524** | 18 |
| 5 | 255 | 166 | 96 | 16 | 21 | 0 | **554** | 30 |
| 6 | 265 | 170 | 102 | 16 | 21 | 0 | **574** | 20 |
| 7 | 329 | 209 | 115 | 24 | 21 | 0 | **698** | 124 |
| 8 | 353 | 252 | 136 | 46 | 21 | 0 | **808** | 110 |
| 9 | 431 | 291 | 159 | 53 | 21 | 0 | **955** | 147 |
| 10 | 525 | 349 | 194 | 65 | 21 | 3 | **1,157** | 202 |
| 12 | 550 | 391 | 224 | 76 | 21 | 3 | **1,265** | 80 |
| 15 | 700 | 581 | 437 | 187 | 29 | 37 | **1,971** | 185 |
(Years 11, 13, 14 are in the CSV.)

**Where it turns.** Sharply at 3 years (+261 in the third year, 506 in all). Then a **plateau from 3 to 6 years: +68 SKUs in three years** (524, 554, 574). From 7 years it climbs again at 80 to 280 SKUs a year with no second knee, to 1,971 at 15. So it is not flat: widening to 6 buys almost nothing, and widening past 6 buys a lot, but of a different kind. Of the 850 SKUs dated 2012 to 2016, **813 rest on a zip date alone** (low confidence; 37 have EXIF), against 3 in 4 of the 2017 to 2020 band resting on EXIF (383 of 545). The late climb is mostly old stock carrying file dates, not demonstrated recent products.

**Recommendation, accept or reject in a word: keep 3 years.** At 3 years the pool is 506 (batch 1: 528), inside the PLAN's 400 to 600 recommended range and well over its 200 minimum, and 4 compositions (ear, neckline, hand, wrist) cover 98% of it. Widening to 6 adds 68; widening further adds SKUs whose recency nobody can vouch for. The 500-SKU candidate sheet (item 17) is the way to test that last point with ZJ. Bracelets (10) and watches (0) are too few at any cutoff under 9 years to be a family in this programme; they would be stills or dropped.

## Item 16: batch 1
**Count verified: 528 distinct new codes, not 534.** `New 2024` 319, `2025` 87, `2026` 126 (sum 532); 4 codes are filed in two top folders, giving 528. cp's 534 is a sum of per-folder tallies (New 2024's four subfolders 190 + 98 + 19 + 14 = 321, of which 2 are in two subfolders, plus 87 + 126). The `whatch` folder's SKU, R12583, is **already** one of the 528 (filed in a batch folder too), so it adds nothing. Against the 3-year measured pool: **504 of the 528 are in the 506**, 24 are not (their own files date 2002 to 2020 or 2023 by EXIF and zip, though they sit in a recent folder), and 2 of the 506 are not in batch 1. Batch 1 is the 528 as David defined it; the 24 are the ones to look at if fidelity to "recent" matters.

**Family split (528):** earrings 260 (49.2%), necklaces 141 (26.7%), rings 96 (18.2%), other 21 (4.0%), bracelets 10 (1.9%), watches 0. Against 2,485 earrings fall 34% to 49%, rings 21% to 18%, wrists 10% to 2%.

**Templates, same method (cs's 220 reads, extrapolated within family, N=528):**
| Form | est. SKUs | share |
|---|---|---|
| ear: drop on hook | 238 | 45.1% |
| neck: pendant on chain | 103 | 19.5% |
| hand: ring | 96 | 18.1% |
| neck: collar/statement | 25 | 4.7% |
| neck: station chain | 20 | 3.7% |
| ear: stud, hoop, post with drop | 12 each | 2.3% each |
| wrist: bracelet / cuff / watch | 8 / 2 / 0 | 1.6% / 0.4% / 0% |
| still: loose pendant or charm | 1 | 0.2% |
Forms needed: **3 cover 82.7%, 5 cover 91.1%, 7 cover 95.6%, 9 cover 99.4%** (against 6, 9 for 90% and 95% on the full 2,485). **By composition: ear 51.9%, + neckline 79.8%, + hand 97.9%; the wrist composition adds 2% and still life 0.2%.** The template count falls from 8 to 9 to **about 5 forms for 90%, or 3 compositions for 98%**. Ranges are sampling-only; stud, hoop and post still rest on 4 or fewer reads each.

**Pilot allocation, 28 images, re-weighted** (largest remainder): earrings 14, necklaces 7, rings 5, bracelets 1, other 1, watches 0 (unrounded 13.8 / 7.5 / 5.1 / 0.5 / 1.1). By form: hook 13, pendant 5, ring 5, collar 1, station 1, stud 1, hoop 1, post 1. cs's allocation was 9, 8, 6, 3, 1, 1; the change is more earrings, fewer bracelets, no watch. Still too thin for a per-family pass rate (about 43 judged images a family for ±15 points): at 528 only earrings and necklaces could ever reach that; rings are borderline; bracelets and watches cannot be piloted at all.

**Cost model.** `cost_per_approved = (price + QA cost per attempt) / pass rate` does not depend on the population or the cap, so **the per-image cost model is unchanged**. What changes is the total, which is images times that. Images are templates times variants: 5 forms at 10 / 25 / 50 variants = 50 / 125 / 250 images for 91%; 7 forms = 70 / 175 / 350 for 96%. The PLAN's 200-image minimum is reached by 4 compositions at 50 variants or 5 forms at 40. The 28-image pilot is now 5.3% of the pool (1.1% of 2,485), so it is a bigger share of what a programme would make; a price from David drops into `pilot_harness.py cost`.

**The three art directions.** Concept C (scene in context: rings, bracelets, watches) **no longer suits** batch 1: it carries about 20% against 52% earrings. A (object study) and B (worn crop, about 98% of batch 1 by ear, neckline and hand) still suit; no regeneration done.

**Not covered:** the 24 batch-1 SKUs whose own dates are old; form shares rest on one reader's 220 reads; wrist forms rest on 10 SKUs; whether recency by folder is what ZJ would call recent.
