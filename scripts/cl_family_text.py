"""cl item 3, text half. US$0. The repo holds no title or description text (supplier_description, supplier_colour empty for all 2,485), and no SKU lacks a family_letter.
The only text signal is category_code. Its first letter is the family letter; for the 59 'other' SKUs (letters A,S,P,M,C) the LAST letter of the code often names the worn-location (AEZ, SN, ANZ...).
Rule proposed: A*/S* codes -> E=earrings, N=necklaces, R=rings, B=bracelets by the second letter; P/PG -> loose pendant (no chain, stays 'other'); the rest unresolved.
Validated against cs's 6 reads of 'other' SKUs. Does NOT edit the dataset. Usage: python3 -I scripts/cl_family_text.py [--selftest]"""
import csv, sys, collections
W = {'E': 'earrings', 'N': 'necklaces', 'R': 'rings', 'B': 'bracelets'}
def rule(code):
    if code[0] in 'AS' and len(code) > 1 and code[1] in W: return W[code[1]]
    if code[0] == 'P': return 'loose pendant'
    return 'unresolved'
if '--selftest' in sys.argv:
    assert rule('AEZ') == 'earrings' and rule('ZZ') == 'unresolved' and rule('SX') == 'unresolved'
    assert rule('AEZ') != 'necklaces'; print('selftest ok'); sys.exit()
rows = [r for r in csv.DictReader(open('data/dataset_2485.csv', encoding='utf8')) if r['family'] == 'other']
c = collections.Counter(rule(r['category_code']) for r in rows); print('other', len(rows), dict(c))
reads = {}
for f in ('data/source_sample.csv', 'data/source_sample2.csv'):
    for s in csv.DictReader(open(f, encoding='utf8')): reads[s['sku']] = s['form']
agree = tot = 0
for r in rows:
    if r['sku'] in reads:
        p, f = rule(r['category_code']), reads[r['sku']]; ok = (p == 'loose pendant' and 'loose pendant' in f) or (p != 'loose pendant' and f.startswith(p[:-1] if p.endswith('s') else p))
        tot += 1; agree += ok; print(' ', r['sku'], r['category_code'], '->', p, '| read:', f, '|', 'AGREE' if ok else 'DISAGREE')
print('agree', agree, 'of', tot)
