# cl — item 4, template plan (metadata-only)

Script `scripts/cl_template_plan.py` (asserts the form counts sum to 2,485; it failed at 2,465 before a bug was fixed, so the check fires). US$0.

**Basis and its limits.** Form shares are cs's 220 reads (one reader, one pass), extrapolated within each code-letter family to the 2,485; `other` is resolved by the L201 proposal (category_code). Ranges are Wilson 95% on sampling only: reader error is not in them. Bracelet-letter strays (necklace-forms, loose pendants, clasp charms) are carried through at their read rate (5 of 24), n is small. Pixels could change any row.

| Form | est. SKUs | 95% range | share | composition |
|---|---|---|---|---|
| ear: drop on hook | 756 | 683–803 | 30.4% | C1 ear profile |
| neck: pendant on chain | 562 | 444–687 | 22.6% | C2 neckline |
| hand: ring | 526 | 470–537 | 21.1% | C3 hand |
| wrist: bracelet | 155 | 96–252 | 6.2% | C4 wrist |
| neck: collar/statement | 132 | 71–227 | 5.3% | C2 neckline |
| neck: station chain | 113 | 53–242 | 4.5% | C2 neckline |
| wrist: cuff/bangle | 50 | 22–98 | 2.0% | C4 wrist |
| wrist: watch | 49 | 28–49 | 2.0% | C4 wrist |
| ear: stud / hoop / post with drop | 38 each | 15–93 each | 1.5% each | C1 ear profile |
| still: loose pendant or clasp charm | 28 | 14–71 | 1.1% | C5 still life |
| unresolved (MW, CAF) | 2 | | 0.1% | none |

**Minimum templates for a coverage level** (greedy by count):

| Coverage | By form (12 forms) | By composition (5) |
|---|---|---|
| ≥ 75% | 4 forms (80.4%) | 3 compositions (88.6%) |
| ≥ 90% | 6 forms (90.2%) | 4 compositions (98.8%) |
| ≥ 95% | 9 forms (95.7%) | 4 compositions (98.8%) |
| ≥ 99% | 11 forms (98.8%) | 5 compositions (99.9%) |

Compositions carry: C1 ear profile 869 SKUs (35.0%), C2 neckline 806 (32.4%), C3 hand 526 (21.1%), C4 wrist 254 (10.2%), C5 still life 28 (1.1%).

**Can one composition carry the form?** Ear profile: yes for drop, post-with-drop, stud and hoop, with scale as a variable; stud and hoop are small and fine-detail. Neckline: one crop carries pendant and collar only with a different drop height; **station chains are a separate, hard drape** (4.5%, range 2–10%). Hand: rings, yes. Wrist: bracelet, cuff and watch share a pose but the watch face and cuff width need their own variable. Still life: the only home for pieces not worn directly.

**The number, settled or not.** cs's 8–9 templates against a guess of 13: by form, **9 templates cover 95.7%** and 6 cover 90.2%, so 8–9 holds on this population, with the hoop/stud/post/loose-pendant rows resting on 4 or fewer reads each. Settling it needs pixels on all 2,485 or a second reader on the 220. By composition it is 4 for 98.8%.

**Images is templates times variants, not templates alone.** Variants per template are not decided here. Arithmetic only: 6 form-templates at 10, 25 or 50 variants is 60, 150 or 300 images; 9 is 90, 225 or 450; 4 compositions is 40, 100 or 200. No claim is made about programme size.
