# cl — Scope A access log, zj1-images (2026-11-15)

Grant cited: David, 2026-11-15, in session ("read-only … Scope: A, dating only, items 8 and 9 … stop on the first 403 or any prefix not in it, range reads only, nothing written"). Credentials used: SPACE_KEY_ID / SPACE_KEY_SECRET only. No 403 met.

## Requests (exact)
| # | Kind | Target | Result |
|---|---|---|---|
| 1 | list | root, Delimiter `/` | 8 prefixes: `alphas/ archive/ bundles/ new-2024/ records/ runs/ sources/ staging/`; no root keys |
| 2 | list | `sources/`, max 5 | `image-sku-map.csv` (891,480 B), `manifest.csv` (1,414,886 B), then `sp-NNNN.jpg` (~215-320 KB each) |
| 3 | list | `new-2024/`, max 5 | folders `n24-<12 hex>/`, not SKU-named |
| 4 | list | `new-2024/n24-003d040d1e4a/`, max 10 | `320.jpg` 9,228 B, `640.jpg` 25,611 B, `master.jpg` 219,301 B; all LastModified 2026-11-12 |

**Totals: list 4, get 0, bytes fetched 0** (listing responses only). Nothing written. Prefixes opened beyond the root: `sources/`, `new-2024/` (both logged under L207); `alphas/ archive/ bundles/ records/ runs/ staging/` not opened.

## What it says for Scope A
- **The new codes' originals are not in the Space as loose objects.** `new-2024/` is the only prefix matching the new-code batch (cs's `origin = new_2024`), and what it holds is a delivery set per hashed ID: 320 px, 640 px and a `master.jpg` of ~219 KB, uploaded 2026-11-12. Against 3,400 px sources, 219 KB is a re-encoded derivative, not a camera original. `sources/` is the legacy `sp-NNNN` photo map, not the 2,478.
- **Not tested, so not claimed:** whether `master.jpg` retains EXIF (a derivative re-encode usually strips it; one 64 KB range read would settle it); how a hashed ID maps to a SKU (no map seen: `sources/image-sku-map.csv` and `manifest.csv` are under `sources/`, and which of them, if either, covers `n24-` is unknown).
- Even if EXIF survived, `LastModified` is the upload time (2026-11-12) and zip entry mtime (rung 2) cannot come from object storage. So from the Space the ladder would have at most rung 1 and rung 3.
- Answer to the access-spec question 1: **no, not the originals.** Scope A as designed (EXIF from originals) needs the zips; the Space cannot supply them.
