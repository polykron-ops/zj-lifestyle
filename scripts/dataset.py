"""SKU-level dataset for the eligible pool (2,485): one row per SKU, all from existing records, US$0.
New codes: reference/new-products-2024 (codes/inventory/manifest) + Medusa payload where present. Legacy 2023 SKUs: eligibility.csv + production.csv."""
import csv, re, collections, json, glob
R='C:/Dev/ZJ1-repo/reference/new-products-2024/'
rd=lambda p:list(csv.DictReader(open(p,encoding='utf-8-sig')))
codes={r['code']:r for r in rd(R+'codes.csv')}; inv=rd(R+'inventory.csv'); pool=rd('C:/Dev/zj-lifestyle/data/pool_2478.csv')
byc=collections.defaultdict(list)
for i in inv: byc[i['code']].append(i)
rows=[]
for p in pool:
    c=p['sku']; r=codes[c]; im=byc[c]
    w=[float(i['gross_g']) for i in im if i['gross_g'] not in('',None)]
    rows.append(dict(sku=c,origin='new_2024',intro_basis='photo folder / import batch',family_letter=p['family_letter'],category_code=p['category_code'],
      source_images=p['source_image_count'],unique_images=p['unique_images'],best_long_px=p['best_source_long_px'],best_short_px=p['best_source_short_px'],
      first_folder=r['first_folder'],gross_g=max(w) if w else '',supplier_colour=r['supplier_colour'],supplier_description=r['supplier_description'],
      proposed_price=r['proposed_price'],price_basis=r['price_basis'],created_in_medusa=p['created_in_medusa']))
el=[r for r in rd('C:/Dev/zj-lifestyle/data/eligibility.csv') if r['intro_date'].startswith('2023')]
for e in el:
    c=e['sku']; m=re.match(r'[A-Z]+',c.upper()); cat=m.group(0) if m else ''
    rows.append(dict(sku=c,origin='legacy_'+e['catalogue'],intro_basis=e['intro_source']+' '+e['intro_date'],family_letter=cat[:1],category_code=cat,source_images='',unique_images='',best_long_px='',best_short_px='',first_folder='',gross_g='',supplier_colour='',supplier_description='',proposed_price='',price_basis='',created_in_medusa=''))
w=csv.DictWriter(open('C:/Dev/zj-lifestyle/data/dataset_2485.csv','w',newline='',encoding='utf8'),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows),collections.Counter(r['origin'] for r in rows))
d=[r['supplier_description'] for r in rows if r['supplier_description']]; print('with description',len(d),'| with weight',sum(1 for r in rows if r['gross_g']!=''),'| with price',sum(1 for r in rows if r['proposed_price']))
print(collections.Counter(w for x in d for w in re.findall(r'[a-z]+',x.lower())).most_common(40))
