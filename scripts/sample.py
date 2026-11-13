"""Families derived from the data, the 40-SKU source sample, and contact sheets for a visual difficulty read. US$0, read-only.
Family = code letter x weight band (tertiles of gross_g inside the letter; weight is the best stand-in the data holds for studs vs hoops, small vs statement). Sample = stratified by family, largest source image per SKU."""
import csv, collections, random, os, statistics
from PIL import Image, ImageDraw
D = 'C:/Dev/zj-lifestyle/'
rows = list(csv.DictReader(open(D + 'data/dataset_2485.csv', encoding='utf8')))
LET = {'E': 'earrings', 'N': 'necklaces', 'R': 'rings', 'B': 'bracelets', 'W': 'watches'}
byl = collections.defaultdict(list)
for r in rows:
    if r['gross_g']: byl[r['family_letter']].append(float(r['gross_g']))
cut = {l: (statistics.quantiles(v, n=3) if len(v) >= 9 else None) for l, v in byl.items()}
for r in rows:
    l = r['family_letter']; g = r['gross_g']; name = LET.get(l, 'other')
    if not g or not cut.get(l): band = 'unweighed' if not g else 'all'
    else: g = float(g); band = 'light' if g <= cut[l][0] else 'mid' if g <= cut[l][1] else 'heavy'
    r['family'] = f'{name}/{band}'
w = csv.DictWriter(open(D + 'data/dataset_2485.csv', 'w', newline='', encoding='utf8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
fam = collections.Counter(r['family'] for r in rows)
print('families', len(fam)); [print(' ', k, v, '%.1f%%' % (100 * v / len(rows))) for k, v in sorted(fam.items(), key=lambda x: -x[1])]
print('weight cuts (g):', {l: [round(x, 1) for x in c] for l, c in cut.items() if c})
# sample: proportional with a floor of 1 per family that has >=20 SKUs, seed fixed
random.seed(13); N = 40
inv = list(csv.DictReader(open('C:/Dev/ZJ1-repo/reference/new-products-2024/inventory.csv', encoding='utf-8-sig')))
best = {}
for i in inv:
    k = i['code']; a = int(i['width'] or 0) * int(i['height'] or 0)
    if k not in best or a > best[k][0]: best[k] = (a, i)
elig = [r for r in rows if r['origin'] == 'new_2024' and r['sku'] in best]
fs = collections.Counter(r['family'] for r in elig); alloc = {f: max(1, round(N * n / len(elig))) for f, n in fs.items() if n >= 20}
while sum(alloc.values()) > N: alloc[max(alloc, key=alloc.get)] -= 1
while sum(alloc.values()) < N: alloc[max(fs, key=lambda f: fs[f] / (alloc.get(f, 0) + 1))] = alloc.get(max(fs, key=lambda f: fs[f] / (alloc.get(f, 0) + 1)), 0) + 1
pick = []
for f, n in alloc.items():
    pool = [r for r in elig if r['family'] == f]; pick += random.sample(pool, min(n, len(pool)))
print('sample', len(pick), dict(alloc))
S = '/c/Dev/ZJ1/261111_additional_images_unzipped/'.replace('/c/', 'C:/')
out = csv.writer(open(D + 'data/source_sample.csv', 'w', newline='', encoding='utf8')); out.writerow(['n', 'sku', 'family', 'zip', 'file', 'long_px', 'gross_g'])
os.makedirs(D + '.scratch', exist_ok=True)
for k in range(0, len(pick), 10):
    sheet = Image.new('RGB', (5 * 320, 2 * 340), 'white'); d = ImageDraw.Draw(sheet)
    for j, r in enumerate(pick[k:k + 10]):
        a, i = best[r['sku']]; p = S + i['zip'] + '/' + i['folder'] + '/' + i['file']
        out.writerow([k + j + 1, r['sku'], r['family'], i['zip'], i['file'], max(int(i['width']), int(i['height'])), r['gross_g']])
        try:
            im = Image.open(p).convert('RGB'); im.thumbnail((310, 300)); sheet.paste(im, ((j % 5) * 320 + 5, (j // 5) * 340 + 30))
        except Exception as e: d.text(((j % 5) * 320 + 5, (j // 5) * 340 + 150), 'ERR ' + str(e)[:30], fill='red')
        d.text(((j % 5) * 320 + 5, (j // 5) * 340 + 5), f'{k + j + 1} {r["sku"]} {r["family"]}', fill='red')
    sheet.save(D + f'.scratch/sample{k // 10}.png')
