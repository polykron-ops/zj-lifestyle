# cl — item 6, pilot harness (ready, not run)

`scripts/pilot_harness.py`. US$0. No paid call exists in the file: the only provider is `stub`; any other raises `SpendBlocked`.

## What it holds
1. **Prompt template per form** (12 forms, keys as in `cl-template-plan.md`). One base prompt, variables: `desc` and `sit` (from the form), `setting/crop/light/model` (from David's chosen concept: A, B or C), `stone` and `metal` (**a person reads these off the reference**: no such field exists in the data), `aspect`, `px`. The prompt always instructs: reproduce the piece EXACTLY, no added/removed/resized/recoloured parts, never a full face, no text or logos. It refuses to build without a chosen concept.
2. **Automatic pre-checks per attempt:** unreadable, too small (< 1,000 px long edge), wrong aspect, blank, identical to the reference (nothing generated). Cheap gates; they do not replace a person.
3. **QA checklist, a person per image** (recorded as y/n columns in the results CSV; `pass` = pre-check clean and all CRITICAL items y):
   - CRITICAL, product fidelity: shape and proportions; stone count and placement; metal colour; fastening (hook, post, clasp, bail); nothing added or missing.
   - CRITICAL, safety: no full face; anatomy correct (fingers, ear, wrist); scale plausible; no text, logo or watermark; no artifacts.
   - MINOR, recorded not gating: composition and light match the concept.
   - Plus `qa_seconds` per image and a free `note`.
4. **Measurement** (`measure results.csv`): per form: slots, attempts, first-pass rate with Wilson 95% interval, approved, abandoned, attempts per approved, QA minutes per approved, cost per approved. One slot = one SKU; an attempt is one generation; approved = a slot with a passing attempt.
5. **Cost model**, parameterised: `cost_per_approved(p, k, price, qa_min, qa_rate_per_hr)`; `python3 -I scripts/pilot_harness.py cost <price> <qa_min> <qa_rate>` prints the grid. Drop David's price in as the first argument.

## What the cost model says, and what it assumes
- With independent attempts, **cost per approved image is (price + QA cost per attempt) ÷ p, whatever the attempt cap k.** The cap decides how many slots end approved (p=0.5: 50% at k=1, 75% at k=2, 88% at k=3, 97% at k=5), not the cost of an approval. Example, price 1 unit, QA 3 min at a rate of 0: p=0.5 gives 2.00 units, p=0.3 gives 3.33, p=0.2 gives 5.00.
- **Assumption that will break:** attempts are independent. Hard pieces (fine chains, transparency) will fail together, so for them the cap does matter and the per-form measurement from the pilot, not this formula, is the number to use.
- **Pilot size:** 28 images over 6+ families cannot give a per-family pass rate (cs's own finding); `measure` will print the interval so its width is visible.

## Proved how
`selftest` (passes) builds a **synthetic** fixture image, a grey disc on a pale ground, standing in for a catalogue photo, because no catalogue images exist in this container. So the first *real* image is still untested on real pixels. What it proves, each against a deliberately broken state: the prompt guard refuses an unchosen concept; the spend guard blocks a paid provider; pre-checks fire on a blank image and on an output identical to its reference (and a first stub that merely resized the reference was caught by the identical-check, which is how the stub got fixed); the verdict fails a piece with one critical item at n; `measure` and the cost closed form match hand arithmetic (3 slots, 6 attempts, 2 approved, cost 3.0 per approved at price 1).

**Not covered:** any real generator's interface (nothing is wired), face detection (the no-full-face check is a person's), whether a pre-check threshold suits real outputs, QA timing on real images.
