# Dataset and analysis (cs, 2026-11-13). US$0, no generation, no paid call.

Pool: **2,485 eligible** (2,478 new codes + 7 legacy 2023). Dated by photo folder, not by an introduction date (caveat from L3). `data/dataset_2485.csv`, one row per SKU, rebuilt by `scripts/dataset.py` then `scripts/sample.py`.

## Families (derived, L4)
| Letter | SKUs | Share |
|---|---|---|
| Earrings E | 843 | 33.9% (light 272 / mid 250 / heavy 265 / unweighed 56) |
| Necklaces N | 759 | 30.5% |
| Rings R | 534 | 21.5% |
| Bracelets B | 241 | 9.7% |
| Watches W | 49 | 2.0% |
| Other | 59 | 2.4% |

Weight is present for 2,238 of 2,478 new codes; the 7 legacy SKUs have no weight, image or price here. No type, metal or stone field exists for the new codes, so studs vs hoops, silver vs gold and stone type are **not** derivable from the data: only from images.

## Source sample: 40 SKUs, seed 13, stratified on family (`data/source_sample.csv`), largest source image each. Looked at all 40.
Visual difficulty (my read, one pass, not a second reader): **easy 15 (38%)** rigid, compact, opaque; **medium 10 (25%)** stones, enamel or glass set in rigid pieces; **hard 15 (38%)** fine chains and long drape (13 of the 14 necklaces in the sample), transparency, a leather cord with charms. All 40 are silver pieces on a plain or slightly tinted white; none is gold, none is on a model, backgrounds range from clean white to a grey or teal cast (R7521) and a few have a floor shadow. Best source long edge: 286 to 4,608 px, median 1,600; 853 of 2,478 under 1,500 px.

## Pilot allocation: 28 images, weighted on the eligible population
Earrings 9, necklaces 8, rings 6, bracelets 3, watches 1, other 1 (unrounded 9.5 / 8.6 / 6.0 / 2.7 / 0.6 / 0.7). **Too thin to read as a result:** 28 images over 24 families is about one per family, and the sample has 15 hard pieces of which 13 are necklaces; a pass rate on 8 necklaces carries no confidence interval worth quoting. It tests whether the approach works at all, not how often. Make the pilot's necklace and ring picks come from the hard and easy poles of the sample, so the failure modes show.

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
