# zj-lifestyle

The ZJ lifestyle image programme: a shared set of AI-generated lifestyle images for the legacy catalogue, reused across visual product families. ZJ's existing ~12k SKUs have one angle each and will not be re-photographed; this is catalogue enrichment, not campaign photography.

**Separate from ZJ1 on purpose** (David, 2026-11-13). ZJ1 is the storefront rebuild and keeps its own repo, PLAN and decisions. Nothing here edits ZJ1, and ZJ1's PLAN carries no phase for this.

## Working method

`polykron-ops/zj1/AGENTS.md` governs how we work and applies here unchanged: the four-line report form, real before done, a check proven to fire against a broken state, token discipline, estimates with an ETA and a confidence tag, the spend rule, continuous work, the blast radius and the unprompted anomaly sweep, briefs read from `origin/<default branch>`, and the close procedure. Do not restate it here; read it there.

What differs in this repo:

- **Decision numbers are L1, L2, L3…** — never ZJ1's D-range, in either direction.
- **Spend is US$0 until David has the numbers and has chosen an art direction** (David, 2026-11-13). No paid API call, no trial generation, not one image. The spend rule's US$10 threshold does not apply: the limit here is zero until he says otherwise.
- **Art direction is a gate.** Three materially distinct concepts, David picks one, and no pilot production happens before he has.
- **Product fidelity is the constraint.** An image shown against a SKU must not materially misrepresent the jewellery. Models may be fully AI-generated; full faces are not shown.

## Roles

David decides. cp plans. cs executes. Same seats as ZJ1 (cp Opus 5 medium, cs and cc Sonnet 5.5 medium).

## Layout

- `PLAN.md` — scope, State, Next.
- `briefs/inbox.md` routes to `briefs/for-side.md` (cs). David pastes the inbox path, or says "bim".
- `reference/` — findings, datasets, decisions log.
- `data/` — the SKU-level CSVs. Large derived data is regenerable; do not commit what a script can rebuild.
