# cl — item 1, source census (metadata half)

Script: `scripts/cl_census_meta.py` (self-test proves the validator flags a broken row). Reads `data/dataset_2485.csv` and `data/pool_2478.csv` only. US$0.

| Best-source long edge | SKUs |
|---|---|
| < 1000 px | 338 |
| 1000–1499 | 515 |
| 1500–2499 | 1,131 |
| ≥ 2500 | 494 |

2,478 of 2,485 have dimensions (7 are `legacy_tamirzuman`, no dims). Under 1,500 px: **853 of 2,478 (34.4%)**, which reproduces cs's number on the census. Median long edge 1,600 px; p10 860, p90 3,088. Aspect median 1.14 (p10 1.01, p90 1.33): sources are near-square, so a landscape lifestyle crop is not a straight reuse.

Under 1,500 by family: rings 49.6% (n=534), earrings 37.4% (842), bracelets 28.9% (239), necklaces 21.7% (755), watches 8.2% (49), other 61.0% (59).

**Cutouts:** `cutout_present` is False for all 2,478 pool SKUs. If that flag is right, none of the eligible SKUs has one of the 11,694 cutout PNGs, so every composite starts from a photo background. Unverified against the Space; see open-decisions.

**Not measured (needs pixels):** background uniformity and cast, alpha usability, subject share of frame. The source files are not in this container (cs's machine, `C:/Dev/ZJ1/261111_additional_images_unzipped/`, or the `zj1-images` Space), and the path inventory is in the ZJ1 repo, which this repo may not read.
