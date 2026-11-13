"""The eligible pool after L1 (keep the 3-year rule): the 2,478 new codes of the 2024-onwards import.
Reads ZJ1's reference/new-products-2024 (codes.csv, inventory.csv, manifest.csv) read-only and writes data/pool_2478.csv (one row per new code) and prints the counts."""
import csv, collections, re, statistics
R = 'C:/Dev/ZJ1-repo/reference/new-products-2024/'
codes = {r['code']: r for r in csv.DictReader(open(R + 'codes.csv', encoding='utf-8-sig'))}
inv = list(csv.DictReader(open(R + 'inventory.csv', encoding='utf-8-sig')))
man = list(csv.DictReader(open(R + 'manifest.csv', encoding='utf-8-sig')))
made = {m['external_id'].split(':', 1)[1] for m in man if m['kind'] == 'product'}
new = {c: r for c, r in codes.items() if r['status'] == 'new'}
print('codes', len(codes), '| new', len(new), '| known', sum(1 for r in codes.values() if r['status'] == 'known'), '| created in Medusa (manifest product rows, incl. reverted runs):', len(made))
imgs = collections.defaultdict(list)
for r in inv: imgs[r['code']].append(r)
rows = []
for c, r in new.items():
    im = imgs.get(c, [])
    px = [min(int(i['width'] or 0), int(i['height'] or 0)) for i in im if i['width']]
    longpx = [max(int(i['width'] or 0), int(i['height'] or 0)) for i in im if i['width']]
    uniq = len({i['sha1'] for i in im})
    cat = re.match(r'[A-Z]+', c); cat = cat.group(0) if cat else ''
    rows.append(dict(sku=c, family_letter=cat[:1], category_code=cat, source_image_count=len(im), unique_images=uniq, best_source_long_px=max(longpx) if longpx else 0,
                     best_source_short_px=max(px) if px else 0, first_zip=r['first_zip'], has_price=bool(r['proposed_price']), created_in_medusa=c in made, cutout_present=False))
w = csv.DictWriter(open('C:/Dev/zj-lifestyle/data/pool_2478.csv', 'w', newline='', encoding='utf8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('with at least one image:', sum(1 for r in rows if r['source_image_count']), '| none:', sum(1 for r in rows if not r['source_image_count']))
print('by letter:', collections.Counter(r['family_letter'] for r in rows).most_common())
print('by category code (top 15):', collections.Counter(r['category_code'] for r in rows).most_common(15))
lp = [r['best_source_long_px'] for r in rows if r['best_source_long_px']]
print('best source long edge px: min %d median %d max %d' % (min(lp), statistics.median(lp), max(lp)), '| under 1500:', sum(1 for x in lp if x < 1500), '| under 2000:', sum(1 for x in lp if x < 2000))
print('images per code:', collections.Counter(min(r['source_image_count'], 6) for r in rows).most_common())
print('by first_zip:', collections.Counter(r['first_zip'][:4] for r in rows).most_common())
print('created in Medusa:', sum(1 for r in rows if r['created_in_medusa']))
