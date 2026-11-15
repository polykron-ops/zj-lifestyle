# cl — items 8 and 9: dating ladder and re-derived eligibility (2026-11-15)

> **Superseded for numbers by `reference/cl-dating-measured.md`** (run on cs's measured EXIF and zip dates: 506 of 2,485 eligible). This file keeps the ladder's design and the folder-only provisional run.

**Status: the ladder is built and proven; it has not been run on any real file.** Item 10's gate is unmet (no written confirmation that the AWS credentials are read-only on `zj1-images`; they were not used), and no source files or zip metadata are reachable here. The only real-data rung computable is the weakest one, from the repo's `first_folder`. Everything below about eligibility is therefore **provisional and rests on folder names**, which David's instruction ranks last.

## The ladder (`scripts/cl_dating.py`)
1. **EXIF `DateTimeOriginal`**: plausible if 2000-01-01 ≤ date ≤ today and not a camera-reset sentinel (2000-01-01, 2001-01-01, 1980-01-01). Absent, unparseable, future or sentinel dates are counted and **never filled in**; `DateTime`, `DateTimeDigitized` and the `Software` tag are not used to date anything, and a file with editing software is counted separately (`edited_files`).
2. **Zip entry modification time** (loose files: filesystem mtime, tagged `fs`, a weaker kind). The DOS-epoch sentinel is rejected.
3. **Folder-name year**: the deepest (last) year token in the folder path, **not the file name** (a first version read `B2002.jpg` as the year 2002; the fixture caught it). Archives nest old folders inside new ones, so the deepest folder is the most specific.

Per SKU the earliest plausible date on each rung across its files is kept, plus the rung used, its precision (day or year), and a confidence: **high** EXIF used and agrees with the zip year; **medium** EXIF only; **medium-disagree** EXIF used, zip year differs; **low** zip used (agrees with, or has no, folder year); **low-disagree**; **very low** folder only; **none**. Each rung's date is kept beside the one used, so disagreement is a column, and the run prints the cross-tabs: EXIF vs zip, zip vs folder, EXIF vs folder, and each vs L2's import date (2026-11-11).

**Proved against broken states** (`selftest`, 6 cases in a built zip plus a loose file): stripped/edited file gets no EXIF date and falls to the zip; EXIF `0000:00:00`, a 2031 EXIF and a 1980 zip date are each rejected; an EXIF/zip disagreement is flagged; year-precision 2023 comes out ambiguous, not eligible. The fixtures are synthetic images, so real-camera quirks are untested.

**To run when files arrive:** `python3 -I scripts/cl_dating.py run DIR out.csv [--map map.csv]`, where `DIR` holds the zips or extracted images and `map.csv` has `sku,zip,file`. Without a map it reads the SKU from the file name and flags the SKU `inferred`. A path-free `sku,zip,file` map from cs is the clean input. **It reads the first 64 KB of each file only.**

## Item 9, provisional: the 3-year rule on the folder rung alone
`python3 -I scripts/cl_dating.py folder-only` writes `data/cl_dating_provisional.csv` (one row per SKU, **beside** cs's files; `eligibility.csv` and `dataset_2485.csv` untouched). Cutoff 2023-11-13 as cs set it; a folder year of 2023 is ambiguous because the cutoff is mid-year.

| Provisional class | SKUs | Share of 2,485 |
|---|---|---|
| eligible (folder year 2024, 2025 or 2026) | 496 | 20.0% |
| ambiguous (folder year 2023) | 5 | 0.2% |
| ineligible (folder year 2012 to 2022) | 1,977 | 79.6% |
| unknown (no folder: the 7 legacy-2023 SKUs) | 7 | 0.3% |

**Difference from cs:** cs counts 2,485 eligible (import batch, L2, plus 7 legacy 2023, L3). On this rung 496 are in the window, so **1,989 of 2,485 (80.0%) are not, or not demonstrably, eligible**: 1,977 ineligible, 5 ambiguous, 7 unknown. (The 7 legacy SKUs carry database dates of 2023-01-02 and 2023-03-16, both before the cutoff; they are in cs's pool only by L3's soft rule.)

| Family | eligible | ambiguous | ineligible | unknown | n |
|---|---|---|---|---|---|
| earrings | 248 | 2 | 592 | 1 | 843 |
| necklaces | 125 | 2 | 628 | 4 | 759 |
| rings | 92 | 1 | 441 | 0 | 534 |
| bracelets | 10 | 0 | 229 | 2 | 241 |
| other | 21 | 0 | 38 | 0 | 59 |
| watches | 0 | 0 | 49 | 0 | 49 |

**Folder year against the import date** (the one cross-tab the data allows): of 2,478 new codes, 125 are in a 2026 folder (same year as the import), 81 one year before, 290 two years, 5 three years, and 1,977 four to fourteen years before.

**Read with care.** A folder name records where a file was filed, not when it was shot; EXIF and zip time can move any of these SKUs either way, and the two rungs above this one are exactly what is missing. The numbers show what the rule does on the weakest evidence only. **Whether the programme proceeds smaller, widens its window or stops is David's decision at the gate; no conclusion is drawn here.**

**Not covered:** every SKU's EXIF and zip date, and so any agreement rate between rungs; the 7 legacy SKUs' files; whether a SKU's "best source" (cs's longest-edge pick) is also its earliest file.
