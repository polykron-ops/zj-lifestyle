# cl brief — zj-lifestyle, the standing round to Wednesday 02:00

You are **cl**, session 08-lifestyle. Read this from `origin/main`, never from your own branch. Written by cp 2026-11-15 13:15 and sized to run to Wednesday 02:00 without coming back to anyone.

## What you are and are not

- You work **only** in `polykron-ops/zj-lifestyle`. You do not have the ZJ1 repo and you must not acquire it. If you find yourself opening a ZJ1 file, a ZJ1 brief or another agent's brief file, **halt and say so in one line**.
- **cs owns `main` in this repo.** You push to **`cl/analysis`** and nowhere else. Never push to `main`, never merge, never force-push. One clone, this one.
- Your brief file is this one, `briefs/for-life.md`. `briefs/for-side.md` is cs's: do not read it, do not edit it.
- Your decision numbers are **L200 and up**. cs uses L1 up; ZJ1's D-range is not yours in either direction.
- **US$0. Not one paid API call, not one generated image, no trial.** The spend rule's US$10 threshold does not apply here: the limit is zero until David chooses an art direction. If a step would cost anything, stop and write the line instead.
- `AGENTS.md` in this repo governs the method, and it points at ZJ1's `AGENTS.md`, which you cannot read. So the parts you need are restated once, here, and nowhere else: report on four lines (`MEASURED:` with numbers, `WHERE:` commit, `HOW MUCH:` N of M with the denominator, `NOT COVERED:` what you could not see), 150 words hard; a check is trusted only once proven to fire against a deliberately broken state; never read a whole CSV, log or payload into context, use a script that returns the summary; state an estimate before any task over 15 minutes as `execution / David's decision points / blocked / elapsed / confidence`; do not stop and wait when a task ends, start the next item and say which in one line.

## Where the work stands

cs has done the eligibility and dataset round: `reference/dataset-analysis.md`, `data/dataset_2485.csv`, 2,485 eligible SKUs, six worn-location families, a 40-SKU visual read, and a 28-image pilot allocation. **Do not redo any of it.** Your round starts where that one stopped, and every number it states is a denominator you inherit rather than re-derive, except where an item below says to check one.

Two of its open claims are the reason this round exists: the difficulty read is **one reader, one pass over 40 SKUs**, and sizing the forms across all 2,485 was called paid work. Both can be done better for nothing.

## The round, in order

1. **The full-population source pass, locally, US$0.** cs measured best-source long edge on a 40-SKU sample and found 853 of 2,478 under 1,500 px. Do it over the whole eligible population from the files themselves: per SKU, the best source's dimensions, aspect, file size, an estimate of background uniformity and cast, whether a cutout with usable alpha exists, and the subject's share of the frame. One script, one CSV, one summary table. This replaces a sample with a census and it is the single highest-leverage thing available without spend.
2. **Difficulty as a measured score, not one reader's opinion.** From the pass in 1, define difficulty from measurable properties — fine-chain or drape detected from alpha thinness and connectivity, transparency, cord or leather, subject share, source resolution. Calibrate it against cs's 40 reads: report how often your score agrees with its easy/medium/hard, and where it disagrees say which you believe and why. A score that cannot beat the sample is a finding, not a failure — report it as one.
3. **Families and forms without a paid image pass.** ZJ1's cs round carried an item to derive the families for SKUs whose code letter is missing, from title and category text, validated against its reads. **That item is now yours** and is to be done here. Then go further than it asked: from the alpha and the geometry, classify the form inside each family where the data supports it — hook drop against stud against hoop, pendant against collar against station chain, and say plainly which forms the measurements cannot separate. cs's sample suggested 8 to 9 templates against a guess of 13; settle that number on the population, or state what it would take to.
4. **The template plan.** One table: each form, its SKU count and share, whether one lifestyle composition can carry it, and the minimum set of templates that covers, say, 90% of the eligible population. This is what decides whether the programme is 200 images or 600, so show the count at a few coverage levels rather than picking one.
5. **Three art-direction concepts, written and illustrated from material we already own.** No generation. Each concept: the setting, the crop, the lighting, the model's presence or absence, how a piece sits in the frame, which forms it suits and which it cannot carry, and a page that shows it with existing catalogue images arranged as the composition would place them. **Three materially distinct directions, not one with variations** — if two read as the same idea at a glance, replace one. David picks one at a gate and nothing is produced before he has.
6. **The pilot harness, ready to run and not run.** The prompt template per form with its variables, the QA checklist a person applies per image, the pass-rate and retry measurement, and a cost model with the cost per approved image as a function of pass rate and retries, parameterised so a price David supplies later drops straight in. Prove the harness end to end on an image we already have, standing in for a generated one, so the first paid image is not also the first test of the pipeline.
7. **The anomaly sweep.** Close the round with the ranked list of what looks wrong that nobody asked about — in the dataset, the sources, cs's analysis, this repo's records. Nothing fixed, no permission sought. An empty list must say what was swept.

## Stop list — write the line in `reference/open-decisions-for-david.md` in this repo and move to the next item

Anything costing money; the art-direction choice; changing cs's dataset, eligibility rule or allocation rather than disputing it in your report; deleting anything but your own fixtures; any claim that the programme should grow or shrink. **You decide implementation freely** — scripts, scoring, how the pages are built — log it in `reference/decided-without-asking.md` with its revert.

## Close

Push to `cl/analysis` at every checkpoint and at the end. Your final report is the four lines plus at most three bullets for David. If every item is done before Wednesday, take item 1's census and extend it to the whole 11,695-SKU photo map rather than idling, and say that is what you have done.
