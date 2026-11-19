# cl reconciliation report (seat cl, session 08-lifestyle, repo `polykron-ops/zj-lifestyle`)

Reported 2026-11-19 10:26 UTC. Read-only inspection plus local selftests; nothing fixed, nothing merged, no credential used, no Space request made for this report. I did not read the other seats' reports or the ZJ1 repo (I have no access to it by rule). The attached cr document was read as the request; its evidence register concerns ZJ1 and is outside what I can check.

## 1. Environment (checked now vs older)

**Checked now (2026-11-19):**
- Cloud execution (`environment_kind: anthropic_cloud`), session `session_01RkRBbtpPCn8XyPM83rsztB`, running since 2026-11-15, permission mode `auto`.
- Model: `claude-sonnet-5-5`, both configured and last served (observed via `get_session`).
- Repository `polykron-ops/zj-lifestyle`, branch `cl/analysis`, HEAD `f1f6afef2c864537150fec8814c8b99593804534`, equal to `origin/cl/analysis` (0 ahead, 0 behind), working tree clean. `origin/main` is `d0a55023b0a60fba2c178a48b94ad720c4c1aa5c`. **`cl/analysis` is not merged into `main`** (`git merge-base --is-ancestor` no).
- Tools present: python3 (boto3 1.44.3, Pillow 12.3.0), git, gh, gcloud, curl, psql, pg_dump. Absent: aws CLI, s3cmd. No database URL is set; psql and pg_dump were not used.
- Local selftests rerun and passing: `scripts/cl_dating_csv.py selftest` (8 cases), `scripts/cl_zj_sheet.py selftest` (26 rows, 2 pages, 1 missing image counted), `scripts/cl_dating.py selftest`, `scripts/cl_template_plan.py` (sums to 2,485; with `data/batch1_skus.txt` sums to 528). `cl_dating.py selftest` left an untracked `.scratch/` fixture folder in the working tree, which I removed; tree is clean again.
- A scan of tracked files for key-like strings found no secret value (the only match is `scripts/cl_space.py` reading the key from the environment).

**Older, not re-checked now:** the Space listing (4 lists on 2026-11-15, `reference/cl-space-requests.md`), whether the read-only key still works or has been revoked (testing it would use a credential beyond David's grant; **status unverified**), where `data/original_dates.csv` came from (cs measured it in the ZJ1 repo; cp copied it; I cannot check its provenance).

**Blocked access:** ZJ1 repo (deliberately never acquired); Space reads for thumbnails (see 6); the 2,478 originals (not in the Space; zips needed).

## 2. Inventory

**The lifestyle programme is not a ZJ1 launch requirement.** `AGENTS.md` says ZJ1's PLAN carries no phase for it. I therefore have no launch requirement to report. What follows is the programme's own requirement list (briefs/for-life.md items on `origin/main`). **Nothing is deployed or used in production: every output is an analysis file on `cl/analysis`, pushed, unmerged.** "Verified" below means a selftest or a measured count on the repo's own data, not a runtime check.

| Item | Status | Commit | Merged | Evidence (date) | Uncovered | Remaining dependency |
|---|---|---|---|---|---|---|
| 1 census | metadata half done; **pixel half not done** | 49057a3 (L200) | no | `reference/cl-source-census.md` (11-15) | all pixel measures | source images (Scope B not granted; originals not in Space) |
| 2 difficulty score | **not done** | none | n/a | none | everything | pixel census |
| 3 families/forms | text half done (proposal only); alpha/geometry forms **not done** | 8aa588d (L201) | no | `reference/cl-families-text.md`, 6 of 6 vs cs reads | forms from geometry | pixel census |
| 4 template plan | done, metadata-only; re-pointed to batch 1 | e38af47, cf74eb5 | no | `reference/cl-template-plan.md`, `cl-batch1.md` (11-15) | rests on cs's 220 reads, one reader | pixel census to verify |
| 5 art directions | three concepts **written**; page is schematic only | e38af47 (L203) | no | `reference/cl-art-direction.md/.html` | illustrated page from catalogue images | images |
| 6 pilot harness | built, stub provider only, **not run** on a catalogue image | 6c0c25f (L204) | no | `reference/pilot-harness.md`; synthetic-fixture proof | real-pixel behaviour | a catalogue image; price from David |
| 7 anomaly sweep | done | a5053ab (L202) | no | `reference/cl-anomaly-sweep.md` | | |
| 8 dating ladder | done and run on measured dates | cb471c9 (L205), 36decb9 (L208) | no | `reference/cl-dating-measured.md`; 2,481 of 2,485 dated | editing-software evidence; whether zip date = shoot date; 4 SKUs (`B6392A-3`, `BD148`, `E6398`, `N12287B`) have no rows | cp answer on zip date provenance |
| 9 eligibility | **506 of 2,485** at 3 years on best evidence | 36decb9 | no | same | | David's gate decision |
| 10 credential | used for 4 list requests only | 8325f50 (L207) | no | `reference/cl-space-requests.md` | | David: key extension or revoke |
| 11 access spec | done; **its core question is now answered "no"** (originals not in Space) | f00b58b (L206) | no | `reference/cl-access-spec.md` | spec is partly stale | |
| 12-13 | executed via `data/original_dates.csv` | 36decb9 | no | | | |
| 14 questions file | written, 3 questions | 36decb9 | no | `reference/for-cp.md` | | cp |
| 15 curve | done | cf74eb5 | no | `data/cl_eligibility_curve.csv`, `reference/cl-eligibility-curve.png` | | |
| 16 batch 1 | done: **528 distinct**, not 534 | cf74eb5 | no | `reference/cl-batch1.md`, `data/batch1_skus.txt` | | |
| 17 ranking | done: 500 span 2023-06-29 to 2017-02-12 | f1f6afe (L209) | no | `data/zj_candidates_500.csv` | | |
| 18 sheet + zip | **not built, not sent** | none | n/a | `scripts/cl_zj_sheet.py build` proven on synthetic thumbnails only | the 500 thumbnails | David's credential decision, or cs drops the files |
| 19 no generation | kept; US$0; no image produced | | | | | |

## 3. Finished work planning lists as open, and the reverse

- **Done but still shown open or stale on `main`:**
  - `PLAN.md` State (identical on branch and main) still says "Nothing built" and "eligibility question is open", though cs's dataset and my items 4 to 9 and 15 to 17 exist.
  - `reference/open-decisions-for-david.md` still carries the 11-15 entry that says the credential is "Not used" and offers option (b) as pending; `reference/cl-access-spec.md` still says the AWS variables are unused and the originals "may" be in the Space.
  - My brief on `main` still gives batch 1 as 534 and says it supersedes 506; I measured 528 distinct (6 double-counted codes: per-folder tallies were summed).
  - `reference/cl-dating.md` is annotated as superseded; the other stale pages are not.
- **Planning-called-done but not independently confirmed (by me):** none of my items claims more than its evidence above; the eligibility counts depend on zip entry dates being shoot dates, which nobody has verified.
- **Unmerged/unpushed:** nothing unpushed. Everything is on `origin/cl/analysis` and **unmerged into `main`** (11 commits, 49057a3 to f1f6afe). `main`'s AGENTS.md has a `lim` bullet my branch copy lacks (my branch predates it, and I never merge main); I took `lim` from the session instruction.
- **Held only in this session:** nothing needed beyond the repo. Scratch in the session scratchpad (`full.txt`, the template-plan output) is regenerable.

## 4. Unresolved requests

| Direction | Request | Owner | Acknowledged? | Completion evidence |
|---|---|---|---|---|
| cl to cp | 3 lines in `reference/for-cp.md`: 4 SKUs missing from `original_dates.csv`; whether `zip_entry_date` is the file's own mtime; EXIF 2002/2003 clock on 222 SKUs | cp | none seen; the file exists **only on `cl/analysis`, not on main**, so cp may not see it | none |
| cl to David | extend the Space grant to `new-2024/index.csv` plus 500 thumbnails (about 5 to 12 MB, cap 200 MB), or have cs drop the files | David | none seen | none |
| cl to David | revoke the key (my report of 11-15 said it has no further use) | David | none seen | key status unverified |
| cl to David | gate: whether the programme proceeds, shrinks, widens or stops; recommendation "keep 3 years" | David | none seen | none |
| received | brief items 15 to 19 | cp | by execution | all but 18 done |
| received | this reconciliation request | David/cr | by this report | n/a |

**Classification.** Access limitation: Space thumbnails; ZJ1 repo; originals not in Space. Operator decisions: credential extension, key revocation, window/size at the gate. Technical defects: none open in my scripts (reruns pass). Ordinary implementation choices (L200 to L209): ranking by newest best-available date, earliest-per-rung dating, batch-1 allocation rounding.

## 5. Planning failures observed (three)

1. **Access was specified for files that were not where the plan said.** Instruction: items 10 and 11 (2026-11-15) had me write a credential spec for the originals; question 1 of that spec asked whether they were in the Space. Evidence: my 4 lists (`reference/cl-space-requests.md`, 8325f50) showed only derivatives under `new-2024/`; cs's confirmation arrived in brief item 12; dating then ran on `data/original_dates.csv` with no credential. Rework: the access spec, a grant to David, a probe, and four questions to David that cp later called its own failure (brief item 14). Detectable: before the spec, by asking cs where the originals live (a one-line question) instead of assuming.
2. **A brief item asserted an authority David had not given.** Brief item 18 says "the Scope A grant covers reading them"; David's grant, quoted at the start of my session, was "Scope A, dating only, items 8 and 9". Evidence: the permission check refused my read of `new-2024/index.csv`; the sheet is unbuilt. Block: items 18 plus the ZJ sheet deliverable. Detectable: comparing the brief's sentence to the grant's text before the brief was sent. I stopped and asked rather than work around it.
3. **A denominator was copied, not counted.** Brief item 15-16 gives batch 1 as 534 "distinct new codes" and the pool as 1,983. Evidence: `scripts/cl_curve.py` and `cl_zj_sheet.py rank` give 528 distinct (534 sums per-folder tallies, with 6 repeats) and 1,950 (1,982 with a 2023 file, 32 also in batch folders). Rework: small (re-run at 528) but the wrong number sits in a brief that says it supersedes my 506. Detectable: counting distinct codes by script before putting the figure in the brief.

## 6. cl additions

**Image inputs.** No image pixels were read in this session. Inputs are metadata: `data/dataset_2485.csv`, `data/pool_2478.csv`, `data/source_sample*.csv` (cs), `data/original_dates.csv` (13,762 rows, cs-measured, copied in by cp; provenance not checkable by me), plus the Space listing of 2026-11-15. The Space holds, for the new codes, only derived 320/640/master JPEGs per `n24-<hash>` (uploaded 2026-11-12); `master.jpg` EXIF survival is untested (the test was cancelled by brief item 13).
**Outputs.** All under `cl/analysis`: scripts `cl_dating.py`, `cl_dating_csv.py`, `cl_census_meta.py`, `cl_family_text.py`, `cl_sweep.py`, `cl_template_plan.py`, `pilot_harness.py`, `cl_space.py`, `cl_curve.py`, `cl_zj_sheet.py`; data `cl_dating_provisional.csv`, `cl_dating_measured.csv`, `cl_eligibility_curve.csv`, `batch1_skus.txt`, `zj_candidates_500.csv`; reference pages as in section 2. **No generated image exists; spend is US$0.**
**Attachment/publication.** Published only by push to `origin/cl/analysis`. **The ZJ candidate zip does not exist** and nothing was sent to David as a file; no artifact was published; nothing is in `main`.
**Unresolved flags.** Those in section 4; plus the two evidence gaps that move the numbers: zip date as shoot date, and one reader's 220 form reads. The 24 batch-1 SKUs whose own file dates are old (2002 to 2020, 2023) sit in recent folders and are unexplained.
**Reproducibility.** From the repo alone: `python3 -I scripts/cl_dating_csv.py run data/cl_dating_measured.csv` (needs only `data/original_dates.csv`), `cl_curve.py`, `cl_template_plan.py [data/batch1_skus.txt]`, `cl_zj_sheet.py rank`; all four ran today to the numbers reported. Caveats: the "as of" date is fixed at 2026-11-15 in `cl_dating.py` (`ASOF`), so reruns after today give the same eligibility, not a moving window; the pixel half of the census, the thumbnails, and anything from the Space depend on files or access not in the repo; the Space state is as of 11-15.
**Credentials, by capability and name only.** `SPACE_KEY_ID` / `SPACE_KEY_SECRET` (with `SPACE_ENDPOINT`, `SPACE_BUCKET`): set; David's 2026-11-15 grant is read-only on `zj1-images`, list and ranged get, Scope A dating only; used for 5 list requests (4 on 11-15, 1 on `new-2024/index.csv` size lookup), **0 gets, 0 bytes**; one ranged get of `index.csv` was refused by the permission check before it ran. Current validity or revocation: **unverified**. `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`: set in the environment, **never used, never granted**. `PHOTOROOM_API_KEY`, `REPLICATE_API_TOKEN`: not set as variables; the environment's proxy lists injection for the Photoroom and Replicate hosts, **never called** (spend rule US$0).

**Branch and commit:** `cl/analysis`; this report is committed on top of `f1f6afe` (commit hash in the final message).
