"""Hand-read forms for the 180 pieces of source_sample2.csv (contact sheets s2_0..s2_8, one pass, one reader), then the combined tally over all 220 read pieces."""
import csv, collections
D = 'C:/Dev/zj-lifestyle/'
DROP, HOOP, STUD, POSTD = 'earrings: drop on a hook', 'earrings: hoop', 'earrings: stud', 'earrings: post with drop'
PEND, COLL, STAT = 'necklace: pendant on a chain', 'necklace: collar or statement piece', 'necklace: station chain'
F = {}
def put(form, *ns):
    for n in ns: F[n] = form
put('ring', 46, 63, 69, 74, 80, 87, 90, 96, 101, 107, 110, 114, 116, 120, 124, 125, 126, 127, 130, 137, 142, 144, 155, 167, 168, 181, 182, 208, 218)
put('bracelet', 41, 56, 98, 118, 122, 141, 151, 184, 187, 192, 197, 217)
put('bracelet: cuff or bangle', 45, 177, 183, 209, 219)
put('watch', 109, 117, 154, 194, 196)
put(DROP, 42, 43, 44, 48, 49, 50, 51, 52, 55, 58, 59, 61, 62, 64, 65, 66, 68, 71, 72, 73, 76, 77, 81, 82, 83, 84, 85, 86, 89, 94, 97, 99, 100,
    102, 103, 104, 105, 111, 112, 113, 121, 128, 129, 132, 140, 146, 153, 156, 159, 164, 166, 169, 170, 172, 173, 175, 176, 186, 189, 193, 195, 199, 200, 202, 203, 206, 210, 213, 215, 220)
put(HOOP, 53, 91, 165, 214)
put(STUD, 171, 190, 198)
put(POSTD, 78, 79, 106, 204)
put(PEND, 47, 54, 57, 67, 70 - 70, 75, 88, 92, 93, 95, 119, 123, 134, 135, 136, 138, 139, 143, 145, 147, 149, 157, 158, 163, 178, 179, 180, 185, 191, 201, 211, 212, 216)
put(COLL, 70, 108, 148, 150, 161, 188)
put(STAT, 60, 115, 133, 160, 162, 174, 207)
put('other: loose pendant or brooch', 131, 152, 205)
F.pop(0, None)
rows = list(csv.DictReader(open(D + 'data/source_sample2.csv', encoding='utf8')))
miss = [r['n'] for r in rows if int(r['n']) not in F]
assert not miss, miss
for r in rows: r['form'] = F[int(r['n'])]
w = csv.DictWriter(open(D + 'data/source_sample2.csv', 'w', newline='', encoding='utf8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
first = list(csv.DictReader(open(D + 'data/source_sample.csv', encoding='utf8')))
for r in first:
    if r['form'] == 'necklace: long station chain': r['form'] = STAT
allr = [(r['family'].split(' ')[0], r['form']) for r in first + rows]
print(len(first), '+', len(rows), '=', len(allr), 'read')
bad = [(r['n'], r['family'], r['form']) for r in rows if (r['form'].split(':')[0].split(' ')[0] not in r['family'].rstrip('s') + 's' and not r['family'].startswith(r['form'].split(':')[0]))]
t = collections.Counter(allr)
for (fam, form), n in sorted(t.items()): print(f'  {fam:10} {form:40} {n}')
print('per family:', dict(collections.Counter(f for f, _ in allr)))
