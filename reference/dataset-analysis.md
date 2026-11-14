# Dataset and analysis (cs, 2026-11-13). US$0, no generation, no paid call.

Pool: **2,485 eligible** (2,478 new codes + 7 legacy 2023). Dated by photo folder, not by an introduction date (caveat from L3). `data/dataset_2485.csv`, one row per SKU, rebuilt by `scripts/dataset.py` then `scripts/sample.py`.

## Families (D167: where the piece is worn; supersedes L4's weight bands)
| Family | SKUs | Share |
|---|---|---|
| Earrings | 843 | 33.9% |
| Necklaces | 759 | 30.5% |
| Rings | 534 | 21.5% |
| Bracelets | 241 | 9.7% |
| Watches | 49 | 2.0% |
| Other (S, A, P, M, C codes) | 59 | 2.4% |

**Six families is all the records support.** No type, description, metal or stone field exists for the new codes (`supplier_description` is empty for all 2,485) and the shop's own categories stop at Earrings, Necklaces and so on, so studs vs hoops, pendant vs chain are **not in the data**. The form split below is read from pictures: 40 SKUs, one reader, one pass. Weight is an attribute (`gross_g`), not a family; the old weight band stays as `stratum` in the CSV only because it stratified the sample.
Forms seen in the 40: earrings, drop on a hook 11 of 12, stud 1, hoop 0, huggie 0; necklaces, pendant on a chain 10 of 14, collar or statement piece 3, long station chain 1; rings 10; bracelets 3; a clasp charm that is not worn directly 1 (BC7047). So the sample suggests about 8 to 9 templates, not 13, and the catalogue is mostly hook drops, pendants and rings; a stud or hoop template would serve a small minority. To size the forms across the 2,485 needs an image pass over all of them, which is paid and a stop-list item (US$0 here).

Weight is present for 2,238 of 2,478 new codes; the 7 legacy SKUs have no weight, image or price here. No type, metal or stone field exists for the new codes, so studs vs hoops, silver vs gold and stone type are **not** derivable from the data: only from images.

## Source sample: 40 SKUs, seed 13, stratified on the earlier finer stratum (family x weight band), which still sums to the worn-location families (`data/source_sample.csv`), largest source image each. Looked at all 40.
Visual difficulty (my read, one pass, not a second reader): **easy 15 (38%)** rigid, compact, opaque; **medium 10 (25%)** stones, enamel or glass set in rigid pieces; **hard 15 (38%)** fine chains and long drape (13 of the 14 necklaces in the sample), transparency, a leather cord with charms. All 40 are silver pieces on a plain or slightly tinted white; none is gold, none is on a model, backgrounds range from clean white to a grey or teal cast (R7521) and a few have a floor shadow. Best source long edge: 286 to 4,608 px, median 1,600; 853 of 2,478 under 1,500 px.

## Pilot allocation: 28 images, weighted on the eligible population
Earrings 9, necklaces 8, rings 6, bracelets 3, watches 1, other 1 (unrounded 9.5 / 8.6 / 6.0 / 2.7 / 0.6 / 0.7). **Too thin to read as a result:** 28 images over 6 families is about 5 per family, and over the 8 to 9 forms about 3 each, and the sample has 15 hard pieces of which 13 are necklaces; a pass rate on 8 necklaces carries no confidence interval worth quoting. It tests whether the approach works at all, not how often. Make the pilot's necklace and ring picks come from the hard and easy poles of the sample, so the failure modes show.

## Expected cost per accepted image (vendor published prices, **unverified**, from memory, not checked this session)
Assumption: 3 generations per accepted image (guessed; the pilot measures it). Excludes human review time.
| Model (published per-image price) | Per generation | Per accepted | 200 | 400 | 600 |
|---|---|---|---|---|---|
| Google Gemini 2.5 Flash Image (~US$0.039) | 0.04 | 0.12 | 23 | 47 | 70 |
| OpenAI gpt-image-1, medium, 1024 (~US$0.04 plus image input) | 0.05 | 0.15 | 30 | 60 | 90 |
| OpenAI gpt-image-1, high, 1024 (~US$0.17 plus image input) | 0.19 | 0.57 | 114 | 228 | 342 |
The first two sit under the US$10 gate for a pilot of 28 (about US$3 to 4 at 3 attempts); anything past the pilot needs David's approval first.

## Two risks, one line each
- **Reuse misrepresentation:** a model shot shows a piece worn at a size, shine and drape the real one may not have; shown beside the photograph it must read as an illustration, and the product page cannot imply a model photographed it.
- **AI-model disclosure:** a generated person is an AI-generated image; EU/UK advertising and platform rules lean toward labelling it, so the label (where, what words) is decided before the first image ships, not after.

Not done: any image view beyond the 40; no per-stone or metal classification; prices not checked against the vendors.

## Added 2026-11-13 night: source sizes, coverage, what sample supports a per-family claim (US$0, computed from `data/dataset_2485.csv`)
- Best source long edge, new codes (2,478): under 1,000 px 338; 1,000-1,499 515; 1,500-1,999 858; 2,000-2,999 484; 3,000+ 283. Every code has at least one source image (0 without).
- Cutout vs original: no cutouts exist for these codes (`cutout_present` false for all); every source is the original photograph, so a lifestyle pass starts from originals and any cutout would be a paid step first. 1,996 of 2,485 carry a proposed price; all 2,478 new codes exist in Medusa (published state not separately counted here).
- Per-family claim (D167, 6 families, smallest 49 SKUs): a pass rate within +/-15 points at 95% needs about 43 judged images per family, about 260 for 6 families, about 390 for 9 forms; the 28-image pilot (about 5 per family, 3 per form) supports no per-family rate. Pilot first, then a 260-image run is the smallest that would.

## Published vs unpublished, and the pilot by form (2026-11-14, US$0; read from the deployed admin's price-cohort lists)
- **Of the 2,485 eligible, 2,478 are draft (unpublished) and 7 are published** (the legacy 2023 SKUs, cohort A). The 2,478 new codes sit in cohort B 1,996 (priced), C 240 (no price and no weight) and D 242 (refused by the per-gram floor), so **none of them is live**, and 482 of them have no price. By family, published: earrings 1, necklaces 4, bracelets 2, rings 0, watches 0, other 0; the rest are draft.
- **Pilot, 28 images, by form** (family share of the eligible population, split inside each family by the forms seen in the 40-SKU read): earrings 9 = 8 hook drops + 1 stud; necklaces 8 = 6 pendants on a chain + 1 collar or statement piece + 1 long station chain; rings 6; bracelets 3; watches 1; other 1 (a necklace-form piece). Hoops and huggies get **no slot**: none appeared in 40, so the pilot cannot say anything about them, and an assumption that they are a family would be wrong on this data. Pick within each form from the easy and hard poles of the 40-SKU difficulty read, so the failure modes show.
- Every figure about forms is an extrapolation from 40 SKUs by one reader; the 2,485 form split is not measured and would take a paid image pass (stop-list).

## The source read raised to 220 (cs, 2026-11-14, brief item 5)

**Number used: 220 pieces read by eye** (the first 40, one random draw seed 13, plus 180 more, seed 29, drawn inside each worn-location, 9 contact sheets of 20; one reader, one pass; `scripts/sample2.py`, `scripts/forms2.py`, `data/source_sample2.csv`). US$0.

| Worn-location (code letter) | Read | Forms seen |
|---|---|---|
| earrings | 92 | drop on a hook 80, hoop 4, stud 4, post with drop 4 |
| necklaces | 53 | pendant on a chain 37, collar or statement 9, station chain 7 |
| rings | 40 | ring 39, one that is a bangle |
| bracelets | 24 | bracelet 14, cuff or bangle 5, **necklace-form 3, loose pendant 1, clasp charm 1** |
| watches | 5 | watch 5 |
| other | 6 | pendant on a chain 3, drop earrings 1, loose pendant or brooch 2 |

**Present or absent.** Hoops: **present, about 4% of earrings** (4 of 92). Huggies: **not seen in 92 earrings, so below 3.3% at 95%** (rule of three); absent for the template set, not proven zero. Studs 4 of 92, posts with a drop 4 of 92: both small, both present. Long station chains and beaded wire necklaces are one form (7 of 53 necklaces).

**Where the data overrules D167.** The code letter is not always the worn-location: **5 of 24 pieces in the bracelet letter are not bracelets** (3 necklace-form, 1 loose pendant, 1 clasp charm), 1 of 40 in the ring letter is a bangle, and 4 of 6 in the "other" letters are earrings or necklaces. So "family from the code letter" is a good first cut for earrings, necklaces and rings, **weak for bracelets (about 1 in 5 wrong)**; the template set should be chosen by form, and the 241 bracelet-letter SKUs cannot be assumed to be bracelets.

**Sizing.** About 43 judged pieces per family gives ±15 points at 95%: met for earrings (92) and necklaces (53), just short for rings (40), not met for bracelets (24), watches (5), other (6). Not sufficient for per-form claims inside a family beyond the big forms (drop 87% of earrings, pendant 70% of necklaces).

**Pilot of 28.** Unchanged in shape: earrings 9 (8 drop on a hook, 1 hoop in place of the stud; hoops are 4% so one slot is generous), necklaces 8 (6 pendant, 1 collar, 1 station chain), rings 6, bracelets 3 (pick by eye, not by letter), watches 1, other 1.
