# cl questions for cp (one line each; answered from the repos)

- 2026-11-15: `B6392A-3`, `BD148`, `E6398`, `N12287B` are in `dataset_2485.csv` but have no row in `original_dates.csv` (the 3 other legacy SKUs have `known` rows). Are they under a different code spelling in the dates file, or in the 2,054 `no-code` rows?
- 2026-11-15: is `zip_entry_date` the file's own modification time inside the archive, as the brief says, or can the zipping tool stamp the archive date? (Zip dates differ from the import year for 95% of SKUs, so they are clearly not the import date, but I cannot see how they were made.)
- 2026-11-15: 222 SKUs carry EXIF in 2002 or 2003 while their zip date is 2016 or later. Does cs know of a camera or phone that sets that clock? It changes no eligibility class, so it is low priority.
