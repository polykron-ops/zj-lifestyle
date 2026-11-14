"""D167: a family is where the piece is worn, not its weight. Sets `family` in the dataset to the worn-location from the code letter (all 2,485 SKUs),
keeps the old weight-band label as `stratum` (it only stratified the sample), and adds the hand-read `form` to the 40-SKU sample. US$0."""
import csv, collections
D = 'C:/Dev/zj-lifestyle/'
LET = {'E': 'earrings', 'N': 'necklaces', 'R': 'rings', 'B': 'bracelets', 'W': 'watches'}
rows = list(csv.DictReader(open(D + 'data/dataset_2485.csv', encoding='utf8')))
for r in rows:
    if 'stratum' not in r: r['stratum'] = r['family']
    r['family'] = LET.get(r['family_letter'], 'other')
f = list(rows[0]); w = csv.DictWriter(open(D + 'data/dataset_2485.csv', 'w', newline='', encoding='utf8'), fieldnames=f); w.writeheader(); w.writerows(rows)
print(collections.Counter(r['family'] for r in rows))
# forms read by eye from the 40 contact sheets (one pass, one reader): n -> form
FORM = {}
for n in (1, 2, 3, 11, 12, 13, 14, 28, 30, 31, 37): FORM[n] = 'earrings: drop on a hook'
FORM[29] = 'earrings: stud'
for n in (9, 15, 16, 17, 21, 22, 23, 24, 25, 40): FORM[n] = 'necklace: pendant on a chain'
for n in (7, 8, 10): FORM[n] = 'necklace: collar or statement piece'
FORM[26] = 'necklace: long station chain'
for n in (4, 5, 6, 18, 19, 20, 32, 33, 34, 39): FORM[n] = 'ring'
for n in (27, 35, 36): FORM[n] = 'bracelet'
FORM[38] = 'clasp charm (not worn directly)'
s = list(csv.DictReader(open(D + 'data/source_sample.csv', encoding='utf8')))
for r in s:
    if 'stratum' not in r: r['stratum'] = r['family']
    r['family'] = r['stratum'].split('/')[0]; r['form'] = FORM[int(r['n'])]
    if r['family'] == 'other': r['family'] = 'other (necklace-form)' if r['form'].startswith('necklace') else 'other'
w = csv.DictWriter(open(D + 'data/source_sample.csv', 'w', newline='', encoding='utf8'), fieldnames=list(s[0])); w.writeheader(); w.writerows(s)
print(collections.Counter(r['form'] for r in s))
