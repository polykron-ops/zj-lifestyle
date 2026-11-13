"""Eligibility of the 11,694 production SKUs (C:/Dev/zj1-manifests/production.csv) under the rule 'introduced in the last 3 years' (cutoff = today minus 3 years).
Introduction date: tamirzuman products.creation_date by SKU; saphirim wp_posts.post_date by WordPress post ID (via the payload's external_id for that SKU); else Unknown."""
import csv, re, json, glob, collections, datetime
CUT = datetime.date(2023, 11, 13)  # 2026-11-13 minus 3 years
TZ = 'C:/Dev/ZJ1/261001_tamirzuman/tamirzuman-website/database/tamirzuman.sql'
SP = 'C:/Dev/ZJ1/260924_saphirim/databases/saphlkib_up.sql'
RX_TZ = re.compile(r"\((\d+),'((?:[^'\\]|\\.)*)','(\d{4}-\d\d-\d\d)[ 0-9:]*','")
RX_SP = re.compile(r"\((\d+),\d+,'(\d{4}-\d\d-\d\d)[ 0-9:]*','")
tz = {}
for line in open(TZ, encoding='utf8', errors='replace'):
    if line.startswith('INSERT INTO `products` VALUES'):
        for m in RX_TZ.finditer(line): tz[m.group(2).strip().upper()] = m.group(3)
sp = {}
for line in open(SP, encoding='utf8', errors='replace'):
    if line.startswith('INSERT INTO `wp_posts` VALUES'):
        for m in RX_SP.finditer(line): sp[int(m.group(1))] = m.group(2)
sku_post = {}
for f in glob.glob('C:/Dev/ZJ1-repo/inventory/medusa_payload/products_saphirim_*.json'):
    for p in json.load(open(f, encoding='utf8')):
        for v in p.get('variants', []): sku_post[(v.get('sku') or '').strip().upper()] = p['metadata'].get('source_id')
prod = list(csv.DictReader(open('C:/Dev/zj1-manifests/production.csv', encoding='utf8')))
res = collections.Counter(); by = collections.Counter(); late = []
out = csv.writer(open('C:/Dev/zj-lifestyle/data/eligibility.csv', 'w', newline='', encoding='utf8')); out.writerow(['sku', 'catalogue', 'type_used', 'intro_date', 'intro_source', 'eligible_last_3_years'])
for r in prod:
    sku = r['sku'].strip(); cat = r['catalogue']; d = ''; src = ''
    if cat == 'tamirzuman' and sku.upper() in tz: d = tz[sku.upper()]; src = 'products.creation_date'
    elif cat == 'saphirim' and sku_post.get(sku.upper()) in sp: d = sp[sku_post[sku.upper()]]; src = 'wp_posts.post_date'
    if d.startswith('0000'): d = ''; src = ''
    if not d: e = 'Unknown'
    else: e = 'Eligible' if datetime.date.fromisoformat(d) >= CUT else 'Ineligible'
    res[(cat, e)] += 1; by[(cat, d[:4] or 'unknown')] += 1
    if e == 'Eligible': late.append((sku, d))
    out.writerow([sku, cat, r['type_used'], d, src, e])
print('cutoff', CUT, '| SKUs', len(prod))
for k in sorted(res): print(k, res[k])
tot = collections.Counter()
for (c, e), n in res.items(): tot[e] += n
print('TOTAL', dict(tot)); print('eligible SKUs:', late[:20])
print('by year', sorted(by.items()))
