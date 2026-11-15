"""cl item 4, metadata-only. US$0. Population form counts = cs's 220 reads (one reader) extrapolated within each code-letter family; 'other' SKUs resolved by the L201 category_code proposal.
Intervals are Wilson 95% on the within-family read share, scaled to family size: they cover sampling only, not reader error. Usage: python3 -I scripts/cl_template_plan.py"""
import csv, collections, math, sys
L = lambda p: list(csv.DictReader(open('data/' + p, encoding='utf8')))
ds_all = L('dataset_2485.csv'); fam = {r['sku']: r['family'] for r in ds_all}   # fam from the FULL dataset: cs's reads are over the full pool
SEL = set(open(sys.argv[1]).read().split()) if len(sys.argv) > 1 else None   # optional: restrict the POPULATION to these SKUs (batch 1); the reads stay cs's 220
ds = [r for r in ds_all if SEL is None or r['sku'] in SEL]
MAP = {'earrings: drop on a hook': 'ear: drop on hook', 'earrings: post with drop': 'ear: post with drop', 'earrings: stud': 'ear: stud', 'earrings: hoop': 'ear: hoop',
       'necklace: pendant on a chain': 'neck: pendant on chain', 'necklace: collar or statement piece': 'neck: collar/statement', 'necklace: station chain': 'neck: station chain', 'necklace: long station chain': 'neck: station chain',
       'ring': 'hand: ring', 'bracelet': 'wrist: bracelet', 'bracelet: cuff or bangle': 'wrist: cuff/bangle', 'watch': 'wrist: watch',
       'other: loose pendant or brooch': 'still: loose pendant/charm', 'clasp charm (not worn directly)': 'still: loose pendant/charm', 'earrings: drop on a hook ': 'ear: drop on hook'}
reads = collections.defaultdict(list)
for r in L('source_sample.csv') + L('source_sample2.csv'):
    if fam[r['sku']] != 'other': reads[fam[r['sku']]].append(MAP[r['form'].strip()])
LET = {'E': 'earrings', 'N': 'necklaces', 'R': 'rings', 'B': 'bracelets', 'W': 'watches'}
size = collections.Counter(r['family'] for r in ds)
for r in ds:
    if fam[r['sku']] == 'other':
        c = r['category_code']; size['loose' if c[0] == 'P' else 'unres' if not (c[0] in 'AS' and c[1] in 'ENRB') else {'E': 'earrings', 'N': 'necklaces', 'R': 'rings', 'B': 'bracelets'}[c[1]]] += 1
size['other'] = 0
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - h) / d, (c + h) / d
est = {}
for f, v in reads.items():
    for form, k in collections.Counter(v).items():
        lo, hi = wilson(k, len(v)); est[form] = est.get(form, [0, 0, 0]); est[form][0] += k / len(v) * size[f]; est[form][1] += lo * size[f]; est[form][2] += hi * size[f]
s0 = est.setdefault('still: loose pendant/charm', [0, 0, 0]); s0[0] += size['loose']; s0[1] += size['loose']; s0[2] += size['loose']  # 8 by code + read-based strays from the bracelet letter
N = len(ds); tot = sum(v[0] for v in est.values()) + size['unres']
GROUP = {'ear': 'C1 ear profile', 'neck': 'C2 neckline', 'hand': 'C3 hand', 'wrist': 'C4 wrist', 'still': 'C5 still life'}
print('| Form | est. SKUs | 95% range | share | composition |\n|---|---|---|---|---|')
rows = sorted(est.items(), key=lambda x: -x[1][0])
for form, (e, lo, hi) in rows: print(f'| {form} | {e:.0f} | {lo:.0f}-{hi:.0f} | {100*e/N:.1f}% | {GROUP[form.split(":")[0]]} |')
print(f'| unresolved (MW, CAF) | {size["unres"]} | | {100*size["unres"]/N:.1f}% | none |'); print('total', round(tot), 'of', N); assert abs(tot - N) < 1, 'population does not sum to N'
cum = 0; print('\nforms, greedy by count:')
for i, (form, (e, _, _)) in enumerate(rows, 1):
    cum += e; print(f'  {i} forms: {100*cum/N:.1f}%')
g = collections.Counter()
for form, (e, _, _) in est.items(): g[GROUP[form.split(':')[0]]] += e
cum = 0; print('compositions:')
for i, (k, e) in enumerate(g.most_common(), 1): cum += e; print(f'  {i} {k}: {e:.0f} ({100*e/N:.1f}%) cumulative {100*cum/N:.1f}%')
