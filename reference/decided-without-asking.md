# Decided without asking (cl, L200+)

- **L200 — 2026-11-15.** Item 1 split into a metadata census (done, `scripts/cl_census_meta.py`) and a pixel census (blocked on file access). Did not use the ambient AWS credentials to reach the Space: nothing in the brief names them. Revert: delete the script and `reference/cl-source-census.md`.
- **L201 — 2026-11-15.** Item 3 text half: no title text and no missing letters exist, so derived the 59 'other' SKUs' worn-location from the category_code second letter instead (6 of 6 vs cs's reads). Proposal only, dataset untouched. Revert: delete `scripts/cl_family_text.py`, `reference/cl-families-text.md`.
