"""cl item 15 + batch-1 verification (item 16 input). US$0, no network. Usage: python3 -I scripts/cl_curve.py
Curve: SKUs whose best-evidence date (data/cl_dating_measured.csv, date_used) is within N years of 2026-11-15, N=1..15, by family. Batch 1: distinct new codes in import top folders New 2024 / 2025 / 2026 (data/original_dates.csv)."""
import csv, collections, datetime as dt
ASOF = dt.date(2026, 11, 15)
m = list(csv.DictReader(open('data/cl_dating_measured.csv', encoding='utf-8')))
fams = ['earrings', 'necklaces', 'rings', 'bracelets', 'other', 'watches']
def cut(n): return ASOF.replace(year=ASOF.year - n)
rows = []
for n in range(1, 16):
    c = cut(n).isoformat(); r = {'years': n, 'cutoff': c}
    for f in fams: r[f] = sum(1 for x in m if x['family'] == f and x['date_used'] >= c)
    r['total'] = sum(r[f] for f in fams); rows.append(r)
for i, r in enumerate(rows): r['added_vs_prev'] = r['total'] - (rows[i - 1]['total'] if i else 0)
w = csv.DictWriter(open('data/cl_eligibility_curve.csv', 'w', newline='', encoding='utf-8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('| yrs | cutoff | ' + ' | '.join(fams) + ' | total | +vs prev |'); print('|---' * (len(fams) + 4) + '|')
for r in rows: print(f"| {r['years']} | {r['cutoff']} | " + ' | '.join(str(r[f]) for f in fams) + f" | {r['total']} | {r['added_vs_prev']} |")
print('dated SKUs', len(m), '| date_used range', min(x['date_used'] for x in m), max(x['date_used'] for x in m))
yc = collections.Counter(x['date_used'][:4] for x in m); print('SKUs by date_used year:', dict(sorted(yc.items())))
# batch 1
od = [x for x in csv.DictReader(open('data/original_dates.csv', encoding='utf-8')) if x['status'] == 'new']
top = lambda f: f.split('/')[0]
B = {'New 2024', '2025', '2026'}
in_b = collections.defaultdict(set); in_other = set(); allc = set()
for x in od:
    allc.add(x['code'])
    (in_b[top(x['folder'])] if top(x['folder']) in B else in_other).add(x['code'])
b1 = set().union(*in_b.values())
print('batch 1 by top folder:', {k: len(v) for k, v in in_b.items()}, '=', len(b1), '| also filed in another folder:', len(b1 & in_other), '| in no batch folder', len(allc - b1))
wh = {x['code'] for x in od if top(x['folder']) == 'whatch'}; print('whatch SKUs', wh, 'in batch1?', bool(wh & b1))
byk = {x['sku']: x for x in m}
print('batch1 SKUs dated', sum(1 for s in b1 if s in byk), '| eligible at 3y (cl 506 pool):', sum(1 for s in b1 if s in byk and byk[s]['eligibility_cl'] == 'eligible'), '| the 506 not in batch1:', sum(1 for s in byk if byk[s]['eligibility_cl'] == 'eligible' and s not in b1))
dsf = {x['sku']: x for x in csv.DictReader(open('data/dataset_2485.csv', encoding='utf-8'))}
print('batch1 by family:', dict(collections.Counter(dsf[s]['family'] for s in b1 if s in dsf)), 'not in dataset', sum(1 for s in b1 if s not in dsf))
print('batch1 date_used year:', dict(sorted(collections.Counter(byk[s]['date_used'][:4] for s in b1 if s in byk).items())))
open('data/batch1_skus.txt', 'w').write('\n'.join(sorted(b1)) + '\n')
