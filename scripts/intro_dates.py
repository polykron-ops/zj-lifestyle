"""Recover introduction_date per SKU from the legacy databases (read-only).
tamirzuman: products.creation_date by product_name (= SKU). saphirim: wp_posts.post_date by the WordPress post ID carried in the Medusa payload (external_id saphirim:<id>).
Writes data/intro_dates.csv: sku,catalogue,intro_date,intro_source. Missing or zero dates are left empty (Unknown)."""
import csv, re, json, glob, collections
TZ = 'C:/Dev/ZJ1/261001_tamirzuman/tamirzuman-website/database/tamirzuman.sql'
SP = 'C:/Dev/ZJ1/260924_saphirim/databases/saphlkib_up.sql'
PAY = 'C:/Dev/ZJ1-repo/inventory/medusa_payload/products_*.json'
RX_TZ = re.compile(r"\((\d+),'((?:[^'\\]|\\.)*)','(\d{4}-\d\d-\d\d)[ 0-9:]*','")
RX_SP = re.compile(r"\((\d+),\d+,'(\d{4}-\d\d-\d\d)[ 0-9:]*','")
tz = {}
for line in open(TZ, encoding='utf8', errors='replace'):
    if line.startswith('INSERT INTO `products` VALUES'):
        for m in RX_TZ.finditer(line):
            tz[m.group(2).strip().upper()] = m.group(3)
print('tamirzuman products with a creation_date:', len(tz), '| zero-dated:', sum(1 for v in tz.values() if v.startswith('0000')))
sp = {}
for line in open(SP, encoding='utf8', errors='replace'):
    if line.startswith('INSERT INTO `wp_posts` VALUES'):
        for m in RX_SP.finditer(line):
            sp[int(m.group(1))] = m.group(2)
print('saphirim wp_posts dates:', len(sp))
rows = []
for f in sorted(glob.glob(PAY)):
    for p in json.load(open(f, encoding='utf8')):
        md = p.get('metadata', {}); cat = md.get('catalogue'); sid = md.get('source_id')
        for v in p.get('variants', []):
            sku = (v.get('sku') or '').strip()
            if cat == 'saphirim': d = sp.get(sid, ''); src = 'wp_posts.post_date'
            else: d = tz.get(sku.upper(), ''); src = 'products.creation_date'
            if d.startswith('0000'): d = ''
            rows.append((sku, cat, d, src if d else ''))
w = csv.writer(open('C:/Dev/zj-lifestyle/data/intro_dates.csv', 'w', newline='', encoding='utf8')); w.writerow(['sku', 'catalogue', 'intro_date', 'intro_source']); w.writerows(rows)
print('payload variants:', len(rows), '| with a date:', sum(1 for r in rows if r[2]))
c = collections.Counter((r[1], r[2][:4] or 'unknown') for r in rows)
for k in sorted(c): print(k, c[k])
