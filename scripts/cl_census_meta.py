"""cl item 1, metadata half. US$0, local, reads only data/ in this repo. Census over the 2,485 eligible SKUs of what the CSVs already carry about the best source:
long/short px, aspect, source counts, cutout flag (pool_2478). Pixel measures (background, cast, alpha, subject share) need the files, which are not in this container.
Usage: python3 -I scripts/cl_census_meta.py [--selftest]"""
import csv, sys, collections, statistics as st
def load(p): return list(csv.DictReader(open(p, encoding='utf8')))
def validate(r):
    """Return list of problems for one row; used on real data and on a deliberately broken row."""
    p = []
    try: l, s = int(r['best_long_px']), int(r['best_short_px'])
    except Exception: return ['non-numeric dims']
    if l <= 0 or s <= 0: p.append('zero dim')
    if s > l: p.append('short>long')
    if l and s and l / s > 4: p.append('aspect>4')
    return p
if '--selftest' in sys.argv:
    bad = {'best_long_px': '100', 'best_short_px': '900'}
    assert validate(bad) == ['short>long'], validate(bad); assert validate({'best_long_px': '', 'best_short_px': '5'}); print('selftest ok: broken rows flagged'); sys.exit()
ds = load('data/dataset_2485.csv'); pool = {r['sku']: r for r in load('data/pool_2478.csv')}
probs = collections.Counter(); n_ok = 0; L = []; A = []; band = collections.Counter(); byfam = collections.defaultdict(list); nodim = 0
for r in ds:
    if not r['best_long_px']: nodim += 1; continue
    pr = validate(r)
    for x in pr: probs[x] += 1
    if pr: continue
    n_ok += 1; l, s = int(r['best_long_px']), int(r['best_short_px']); L.append(l); A.append(l / s); byfam[r['family']].append(l)
    band['<1000' if l < 1000 else '1000-1499' if l < 1500 else '1500-2499' if l < 2500 else '>=2500'] += 1
cut = collections.Counter(pool[r['sku']]['cutout_present'] if r['sku'] in pool else 'not_in_pool' for r in ds)
print('rows', len(ds), 'with dims', n_ok, 'no dims', nodim, 'problems', dict(probs))
q = lambda v, p: sorted(v)[int(p * (len(v) - 1))]
print('long px  min/p10/p50/p90/max', min(L), q(L, .1), q(L, .5), q(L, .9), max(L), '| under 1500:', sum(l < 1500 for l in L))
print('aspect   p10/p50/p90', *(round(q(A, p), 2) for p in (.1, .5, .9)))
print('bands', dict(band)); print('cutout_present (pool)', dict(cut))
print('by family n / median long / %<1500:')
for f, v in sorted(byfam.items(), key=lambda x: -len(x[1])): print(f'  {f:10s} {len(v):5d} {st.median(v):7.0f} {100*sum(x<1500 for x in v)/len(v):5.1f}%')
print('origins', dict(collections.Counter(r['origin'] for r in ds)))
