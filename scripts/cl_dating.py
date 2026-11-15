"""cl items 8-9: dating ladder. US$0, read-only, never touches the network. Takes a DIRECTORY of zips and/or loose images, so it runs unchanged when the files arrive.
Ladder (best evidence wins): (1) EXIF DateTimeOriginal; (2) zip entry mtime (loose files: filesystem mtime, tagged 'fs'); (3) folder-name year. A file without a plausible EXIF original date gets none: it is never filled in
from DateTime/Digitized/Software tags (those are recorded as evidence of editing only). Per SKU the EARLIEST plausible date on each rung across its files is used (introduction ~ first photography).
Usage: python3 -I scripts/cl_dating.py run DIR OUT.csv [--map map.csv] | folder-only | selftest [DIR]
  map.csv columns: sku,zip,file   (zip = archive file name or stem; file = entry basename). Without a map the SKU is read from the file name (flagged inferred)."""
import sys, os, re, io, csv, zipfile, datetime as dt, collections
from PIL import Image
ASOF = dt.date(2026, 11, 15); CUTOFF = dt.date(2023, 11, 13)   # cutoff = cs's (eligibility.md); asof = today per the session
SENTINEL = {dt.date(2000, 1, 1), dt.date(2001, 1, 1), dt.date(1980, 1, 1)}
IMG = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')
SKU_RE = re.compile(r'[A-Z]{1,3}\d{3,6}[A-Z]{0,3}')
def plausible(d): return d is not None and dt.date(2000, 1, 1) <= d <= ASOF and d not in SENTINEL
def parse_exif(s):
    try: return dt.datetime.strptime(str(s).strip()[:19], '%Y:%m:%d %H:%M:%S').date()
    except Exception: return None
def exif_info(data):
    """-> (state, date, edited). state: ok | implausible | absent | unreadable. Reads only the header bytes it is given."""
    try: im = Image.open(io.BytesIO(data)); ex = im.getexif()
    except Exception: return 'unreadable', None, False
    raw = ex.get_ifd(0x8769).get(36867); sw = str(ex.get(305, '')).lower()
    edited = any(w in sw for w in ('photoshop', 'lightroom', 'gimp', 'snapseed', 'canva'))
    if not raw: return 'absent', None, edited
    d = parse_exif(raw); return ('ok' if plausible(d) else 'implausible'), d, edited
def folder_year(path):
    ys = [int(y) for y in re.findall(r'(?<!\d)(20[0-2]\d)(?!\d)', path)]; return ys[-1] if ys else None   # last (deepest) year token: archives nest old folders inside new ones
def scan(root, mapping=None):
    """yield dicts per image file: zip, entry, sku, inferred, exif_state, exif_date, edited, zip_date, mtime_kind, folder_year"""
    def emit(zipname, entry, data, zdate, kind):
        base = os.path.basename(entry); stem = os.path.splitext(base)[0]
        sku = mapping.get((os.path.splitext(zipname)[0], base)) if mapping else None; inferred = False
        if not sku: m = SKU_RE.search(stem); sku = m.group(0) if m else ''; inferred = True
        st, d, ed = exif_info(data)
        yield dict(zip=zipname, entry=entry, sku=sku, inferred=inferred, exif_state=st, exif_date=d, edited=ed, zip_date=zdate, mtime_kind=kind, folder_year=folder_year(os.path.dirname(entry)))  # folders only: a SKU like B2002 must not read as the year 2002
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            p = os.path.join(dp, f); rel = os.path.relpath(p, root)
            if f.lower().endswith('.zip'):
                with zipfile.ZipFile(p) as z:
                    for zi in z.infolist():
                        if zi.is_dir() or not zi.filename.lower().endswith(IMG): continue
                        try: zd = dt.date(*zi.date_time[:3])
                        except Exception: zd = None
                        yield from emit(f, zi.filename, z.open(zi).read(65536), zd, 'zip')
            elif f.lower().endswith(IMG):
                with open(p, 'rb') as fh: head = fh.read(65536)
                yield from emit('', rel, head, dt.date.fromtimestamp(os.path.getmtime(p)), 'fs')
def per_sku(files):
    by = collections.defaultdict(list)
    for r in files: by[r['sku']].append(r)
    out = []
    for sku, v in sorted(by.items()):
        ex = [r['exif_date'] for r in v if r['exif_state'] == 'ok']; zp = [r['zip_date'] for r in v if plausible(r['zip_date'])]; fy = [r['folder_year'] for r in v if r['folder_year']]
        e = min(ex) if ex else None; z = min(zp) if zp else None; f = min(fy) if fy else None
        if e: used, d, prec = 'exif', e, 'day'
        elif z: used, d, prec = 'zip', z, 'day'
        elif f: used, d, prec = 'folder', dt.date(f, 7, 1), 'year'
        else: used, d, prec = 'none', None, ''
        agree_ez = (e.year == z.year) if e and z else None; agree_zf = (z.year == f) if z and f else None
        conf = ('high' if used == 'exif' and agree_ez else 'medium-disagree' if used == 'exif' and agree_ez is False else 'medium' if used == 'exif' else
                'low' if used == 'zip' and agree_zf in (True, None) else 'low-disagree' if used == 'zip' else 'very low' if used == 'folder' else 'none')
        out.append(dict(sku=sku, files=len(v), inferred_sku=any(r['inferred'] for r in v), exif_files_ok=len(ex), exif_files_absent=sum(r['exif_state'] == 'absent' for r in v),
                        exif_files_implausible=sum(r['exif_state'] == 'implausible' for r in v), exif_files_unreadable=sum(r['exif_state'] == 'unreadable' for r in v), edited_files=sum(r['edited'] for r in v),
                        exif_date=e or '', zip_date=z or '', zip_kind=v[0]['mtime_kind'], folder_year=f or '', date_used=d or '', source_used=used, precision=prec, confidence=conf,
                        exif_vs_zip_agree='' if agree_ez is None else agree_ez, zip_vs_folder_agree='' if agree_zf is None else agree_zf))
    return out
def eligible(row):
    """3-year rule at cs's cutoff. Year-precision 2023 is AMBIGUOUS (cutoff is mid-November); none/blank is unknown."""
    d = row['date_used']
    if not d: return 'unknown'
    d = dt.date.fromisoformat(str(d))
    if row['precision'] == 'year': return 'ambiguous (2023)' if d.year == 2023 else 'eligible' if d.year > 2023 else 'ineligible'
    return 'eligible' if d >= CUTOFF else 'ineligible'
def crosstab(rows, a, b, label):
    pairs = [(r[a], r[b]) for r in rows if r[a] != '' and r[b] != '']; n = len(pairs)
    if not n: print(f'  {label}: n=0 (no SKU has both)'); return
    def yr(x): return x.year if isinstance(x, dt.date) else int(x[:4]) if isinstance(x, str) and len(x) >= 4 else int(x)
    d = collections.Counter(yr(x) - yr(y) for x, y in pairs); same = d[0]
    print(f'  {label}: n={n}, same year {same} ({100*same/n:.0f}%), year gap (first minus second) {dict(sorted(d.items()))}')
def summary(rows):
    print('SKUs', len(rows), '| source used', dict(collections.Counter(r['source_used'] for r in rows)), '| confidence', dict(collections.Counter(r['confidence'] for r in rows)))
    print('EXIF state (files): ok', sum(r['exif_files_ok'] for r in rows), 'absent', sum(r['exif_files_absent'] for r in rows), 'implausible', sum(r['exif_files_implausible'] for r in rows),
          'unreadable', sum(r['exif_files_unreadable'] for r in rows), '| files with editing software', sum(r['edited_files'] for r in rows))
    print('cross-tabs (same calendar year; "import" = L2 import date 2026-11-11):')
    imp = [dict(r, imp=dt.date(2026, 11, 11)) for r in rows]
    crosstab(rows, 'exif_date', 'zip_date', 'EXIF vs zip'); crosstab(rows, 'zip_date', 'folder_year', 'zip vs folder year'); crosstab(rows, 'exif_date', 'folder_year', 'EXIF vs folder year')
    for k in ('exif_date', 'zip_date', 'date_used'): crosstab(imp, k, 'imp', f'{k} vs import')
    print('eligibility on date_used:', dict(collections.Counter(eligible(r) for r in rows)))
def selftest(d):
    import shutil
    if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(d)
    def jpg(exif=None, software=None):
        im = Image.new('RGB', (64, 64), (120, 120, 120)); ex = Image.Exif()
        if exif: ex.get_ifd(0x8769)[36867] = exif
        if software: ex[305] = software
        b = io.BytesIO(); im.save(b, 'JPEG', exif=ex); return b.getvalue()
    cases = [  # sku, exif, software, zip_date, folder, expectation
     ('A1001', '2024:03:05 10:00:00', None, (2024, 3, 6), '2024/', ('exif', 'high')),
     ('B2002', None, 'Adobe Photoshop', (2022, 5, 1), 'x/2022/', ('zip', 'low')),                 # stripped/edited: no EXIF date may be invented
     ('C3003', '2019:01:01 09:00:00', None, (2025, 2, 2), 'a/2025/', ('exif', 'medium-disagree')),
     ('D4004', '0000:00:00 00:00:00', None, (2021, 6, 6), 'b/2021/', ('zip', 'low')),             # implausible EXIF
     ('E5005', None, None, (1980, 1, 1), 'c/2018/', ('folder', 'very low')),                      # DOS-epoch zip sentinel
     ('F6006', '2031:01:01 00:00:00', None, (2023, 1, 1), 'd/2023/', ('zip', 'low'))]             # future EXIF
    with zipfile.ZipFile(os.path.join(d, 't.zip'), 'w') as z:
        for sku, ex, sw, zd, fo, _ in cases: z.writestr(zipfile.ZipInfo(fo + sku + '.jpg', date_time=zd + (0, 0, 0)), jpg(ex, sw))
    rows = per_sku(scan(d)); by = {r['sku']: r for r in rows}
    for sku, ex, sw, zd, fo, (src, conf) in cases: assert (by[sku]['source_used'], by[sku]['confidence']) == (src, conf), (sku, by[sku]['source_used'], by[sku]['confidence'])
    assert by['B2002']['exif_date'] == '' and by['B2002']['exif_files_absent'] == 1 and by['B2002']['edited_files'] == 1
    assert by['D4004']['exif_files_implausible'] == 1 and by['F6006']['exif_files_implausible'] == 1 and by['E5005']['zip_date'] == ''
    assert eligible(by['A1001']) == 'eligible' and eligible(by['B2002']) == 'ineligible' and eligible(by['F6006']) == 'ineligible'
    assert eligible(dict(date_used='2023-07-01', precision='year')) == 'ambiguous (2023)'
    os.makedirs(os.path.join(d, 'loose', 'y2025')); open(os.path.join(d, 'loose', 'y2025', 'G7007.jpg'), 'wb').write(jpg('2025:01:02 03:04:05'))
    assert any(r['sku'] == 'G7007' and r['source_used'] == 'exif' for r in per_sku(scan(d))), 'loose file not read'
    print('selftest ok: 6 ladder cases, stripped file gets no EXIF date, implausible/future/sentinel dates rejected, loose files read'); summary(rows)
def folder_only():
    """Rung 3 only, from the repo's first_folder column. Provisional: weakest evidence, NOT the answer. Writes data/cl_dating_provisional.csv beside (not over) cs's files."""
    ds = list(csv.DictReader(open('data/dataset_2485.csv', encoding='utf8'))); rows = []
    for r in ds:
        fy = folder_year(r['first_folder']); fol = r['first_folder']
        rows.append(dict(sku=r['sku'], family=r['family'], origin=r['origin'], first_folder=fol, folder_year=fy or '', top_folder_year=(folder_year(fol.split('/')[0]) or ''),
                         date_used=dt.date(fy, 7, 1).isoformat() if fy else '', source_used='folder' if fy else 'none', precision='year' if fy else '', confidence='very low' if fy else 'none'))
    for r in rows: r['eligibility_provisional'] = eligible(r)
    w = csv.DictWriter(open('data/cl_dating_provisional.csv', 'w', newline='', encoding='utf8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print('folder-year rung only (deepest year token in the path); n =', len(rows)); c = collections.Counter(r['eligibility_provisional'] for r in rows); print('eligibility_provisional', dict(c))
    print('cs eligible = 2,485 (L2/L3: import batch + 7 legacy 2023). Deepest-year distribution:', dict(sorted(collections.Counter(r['folder_year'] for r in rows).items(), key=lambda x: str(x[0]))))
    fams = sorted({r['family'] for r in rows}); print('by family (eligible / ambiguous 2023 / ineligible / unknown of n):')
    for f in fams:
        cc = collections.Counter(r['eligibility_provisional'] for r in rows if r['family'] == f); print(f'  {f:10s} {cc["eligible"]:4d} / {cc["ambiguous (2023)"]:4d} / {cc["ineligible"]:4d} / {cc["unknown"]:3d} of {sum(cc.values())}')
    print('top-folder year vs deepest-folder year (same?):', sum(1 for r in rows if r['folder_year'] != '' and r['top_folder_year'] != '' and r['folder_year'] == r['top_folder_year']), 'of', sum(1 for r in rows if r['folder_year'] != '' and r['top_folder_year'] != ''))
if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'selftest': selftest(sys.argv[2] if len(sys.argv) > 2 else '.scratch/dating_fixture')
    elif c == 'folder-only': folder_only()
    elif c == 'run':
        mp = None
        if '--map' in sys.argv: mp = {(os.path.splitext(r['zip'])[0], os.path.basename(r['file'])): r['sku'] for r in csv.DictReader(open(sys.argv[sys.argv.index('--map') + 1], encoding='utf8'))}
        rows = per_sku(scan(sys.argv[2], mp)); w = csv.DictWriter(open(sys.argv[3], 'w', newline='', encoding='utf8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows); summary(rows)
    else: print(__doc__)
