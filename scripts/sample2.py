"""Raise the source read to a defensible size (brief item 5). US$0, read-only. 180 more eligible SKUs drawn at random inside each worn-location (seed 29), excluding the 40 already read,
laid out 20 to a contact sheet (5 x 4, numbered 41 onward). The reader fills `form` in data/source_sample2.csv by eye. Rule of three: if a form is seen 0 times in n pieces of a family, its share is below 3/n at 95%."""
import csv, collections, random, os
from PIL import Image, ImageDraw
D = 'C:/Dev/zj-lifestyle/'
rows = list(csv.DictReader(open(D + 'data/dataset_2485.csv', encoding='utf8')))
done = {r['sku'] for r in csv.DictReader(open(D + 'data/source_sample.csv', encoding='utf8'))}
inv = list(csv.DictReader(open('C:/Dev/ZJ1-repo/reference/new-products-2024/inventory.csv', encoding='utf-8-sig')))
best = {}
for i in inv:
    k = i['code']; a = int(i['width'] or 0) * int(i['height'] or 0)
    if k not in best or a > best[k][0]: best[k] = (a, i)
elig = [r for r in rows if r['origin'] == 'new_2024' and r['sku'] in best and r['sku'] not in done]
random.seed(29)
NEED = {'earrings': 80, 'necklaces': 40, 'rings': 30, 'bracelets': 20, 'watches': 5, 'other': 5}
pick = []
for f, n in NEED.items():
    pool = [r for r in elig if r['family'] == f]; pick += random.sample(pool, min(n, len(pool)))
random.shuffle(pick)  # mixed on the sheets so the reader is not primed by a family
S = 'C:/Dev/ZJ1/261111_additional_images_unzipped/'
os.makedirs(D + '.scratch', exist_ok=True)
w = csv.writer(open(D + 'data/source_sample2.csv', 'w', newline='', encoding='utf8')); w.writerow(['n', 'sku', 'family', 'zip', 'file', 'long_px', 'gross_g', 'form'])
for k in range(0, len(pick), 20):
    sheet = Image.new('RGB', (5 * 260, 4 * 280), 'white'); d = ImageDraw.Draw(sheet)
    for j, r in enumerate(pick[k:k + 20]):
        a, i = best[r['sku']]; p = S + i['zip'] + '/' + i['folder'] + '/' + i['file']; n = 41 + k + j
        w.writerow([n, r['sku'], r['family'], i['zip'], i['file'], max(int(i['width']), int(i['height'])), r['gross_g'], ''])
        x, y = (j % 5) * 260, (j // 5) * 280
        try: im = Image.open(p).convert('RGB'); im.thumbnail((250, 250)); sheet.paste(im, (x + 5, y + 24))
        except Exception as e: d.text((x + 5, y + 120), 'ERR ' + str(e)[:30], fill='red')
        d.text((x + 5, y + 5), f'{n}', fill='red')
    sheet.save(D + f'.scratch/s2_{k // 20}.png')
print(len(pick), collections.Counter(r['family'] for r in pick), 'sheets', -(-len(pick) // 20))
