"""cl items 17-18: rank the 500 most-likely-recent SKUs from the 2023 folder for ZJ to confirm. US$0.
Usage: python3 -I scripts/cl_zj_sheet.py rank            -> data/zj_candidates_500.csv  (no network)
       python3 -I scripts/cl_zj_sheet.py build THUMBDIR OUT.zip   -> contact sheet PDF + CSV zipped (THUMBDIR/<n24_id>.jpg; no network)
       python3 -I scripts/cl_zj_sheet.py selftest
Fetching the thumbnails from the Space is NOT in this script: it needs David's confirmation that the key may be used for it.
Ranking: pool = new codes filed only in the 2023 folder (batch 1 excluded). Per SKU the date is, in this order of evidence: latest plausible EXIF DateTimeOriginal; else latest plausible zip entry date;
else the deepest folder-year token. SKUs are sorted by that date, newest first (ties: EXIF before zip before folder, then SKU). The image shown is the file that supplied the date."""
import sys, os, csv, io, collections, datetime as dt, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_dating as D, cl_dating_csv as C
N = 500
def rank():
    od = [x for x in csv.DictReader(open('data/original_dates.csv', encoding='utf-8')) if x['status'] == 'new']
    b1 = set(open('data/batch1_skus.txt').read().split()); fam = {r['sku']: r['family'] for r in csv.DictReader(open('data/dataset_2485.csv', encoding='utf-8'))}
    by = collections.defaultdict(list)
    for x in od: by[x['code']].append(x)
    pool = [s for s, v in by.items() if s not in b1 and all(x['folder'].split('/')[0] == 'תמונות 2023' for x in v)]
    out = []
    for s in pool:
        ex = []; zp = []; fy = []
        for x in by[s]:
            st, d = C.exif_row(x['exif_datetime_original']); z = C.zdate(x['zip_entry_date']); y = D.folder_year(x['folder'])
            if st == 'ok': ex.append((d, x))
            if D.plausible(z): zp.append((z, x))
            if y: fy.append((y, x))
        key = lambda t: (t[0], t[1]['file'])
        if ex: d, x = max(ex, key=key); rung, prec = 'exif', 'day'
        elif zp: d, x = max(zp, key=key); rung, prec = 'zip', 'day'
        elif fy: y, x = max(fy, key=key); d = dt.date(y, 7, 1); rung, prec = 'folder', 'year'
        else: continue
        out.append(dict(sku=s, family=fam.get(s, ''), date_used=d.isoformat(), rung=rung, precision=prec, n24_id=x['n24_id'], image_file=x['file'], n_files=len(by[s]), _r={'exif': 0, 'zip': 1, 'folder': 2}[rung]))
    out.sort(key=lambda r: (r['date_used'], -r['_r'], r['sku']), reverse=True)  # newest first; within a date, exif before zip before folder: reverse flips, so -_r keeps exif first
    top = out[:N]
    for i, r in enumerate(top, 1): r['rank'] = i; r['zj_confirms_recent'] = ''; r.pop('_r')
    cols = ['rank', 'sku', 'family', 'date_used', 'rung', 'precision', 'n24_id', 'image_file', 'n_files', 'zj_confirms_recent']
    w = csv.DictWriter(open('data/zj_candidates_500.csv', 'w', newline='', encoding='utf-8-sig'), fieldnames=cols); w.writeheader(); w.writerows([{k: r[k] for k in cols} for r in top])
    print('pool', len(pool), 'ranked', len(out), 'written', len(top))
    print('date range of the 500:', top[0]['date_used'], 'to', top[-1]['date_used'], '| rung', dict(collections.Counter(r['rung'] for r in top)), '| by year', dict(sorted(collections.Counter(r['date_used'][:4] for r in top).items())))
    print('family', dict(collections.Counter(r['family'] for r in top)), '| after the 500: next date', out[N]['date_used'] if len(out) > N else None, '| ranked pool by year', dict(sorted(collections.Counter(r['date_used'][:4] for r in out).items())))
    print('on or after cutoff 2023-11-13:', sum(r['date_used'] >= '2023-11-13' for r in top))
def build(thumbs, outzip, rows=None):
    from PIL import Image, ImageDraw, ImageFont
    rows = rows or list(csv.DictReader(open('data/zj_candidates_500.csv', encoding='utf-8-sig')))
    try: F = ImageFont.truetype('DejaVuSans.ttf', 15); FB = ImageFont.truetype('DejaVuSans-Bold.ttf', 17); FH = ImageFont.truetype('DejaVuSans-Bold.ttf', 20)
    except Exception: F = FB = FH = ImageFont.load_default()
    cols, rws, tw, th, lh = 5, 4, 300, 300, 62; W = cols * (tw + 20) + 20; H = 60 + rws * (th + lh + 20) + 20; pages = []; per = cols * rws
    missing = 0
    for p0 in range(0, len(rows), per):
        pg = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(pg)
        d.text((20, 18), f'ZJ candidate sheet: rank {p0+1}-{min(p0+per, len(rows))} of {len(rows)}   (tick zj_confirms_recent in the CSV: yes / no)', fill='black', font=FH)
        for i, r in enumerate(rows[p0:p0 + per]):
            x = 20 + (i % cols) * (tw + 20); y = 60 + (i // cols) * (th + lh + 20); f = os.path.join(thumbs, r['n24_id'] + '.jpg')
            try: im = Image.open(f).convert('RGB'); im.thumbnail((tw, th)); pg.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
            except Exception: missing += 1; d.rectangle([x, y, x + tw, y + th], outline='red'); d.text((x + 10, y + 10), 'image missing', fill='red', font=F)
            d.text((x, y + th + 4), f"#{r['rank']}  {r['sku']}", fill='black', font=FB); d.text((x, y + th + 26), f"{r['date_used']}  via {r['rung']}" + (' (year only)' if r['precision'] == 'year' else ''), fill='#444', font=F)
        pages.append(pg)
    buf = io.BytesIO(); pages[0].save(buf, 'PDF', save_all=True, append_images=pages[1:], resolution=100)
    with zipfile.ZipFile(outzip, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('zj_candidates_sheet.pdf', buf.getvalue()); z.write('data/zj_candidates_500.csv', 'zj_candidates_500.csv') if rows is None or os.path.exists('data/zj_candidates_500.csv') else None
        z.writestr('README.txt', 'Each picture is labelled rank, SKU, the date used to rank it and where the date came from (exif = camera date, zip = file date, folder = folder year only).\nPlease fill the last column of zj_candidates_500.csv: yes if the piece is from the last 3 years (since Nov 2023), no if older.\n')
    print('pages', len(pages), 'missing images', missing, 'zip bytes', os.path.getsize(outzip)); return missing, len(pages)
def selftest():
    import tempfile
    from PIL import Image
    tmp = tempfile.mkdtemp(); rows = [dict(rank=str(i + 1), sku=f'S{i}', family='x', date_used='2025-01-01', rung='exif', precision='day', n24_id=f'n24-{i:012d}', image_file='a.jpg', n_files='1', zj_confirms_recent='') for i in range(26)]
    for r in rows[:25]: Image.new('RGB', (320, 240), (200, 180, 100)).save(os.path.join(tmp, r['n24_id'] + '.jpg'))   # 26th image deliberately absent
    m, p = build(tmp, os.path.join(tmp, 'o.zip'), rows); assert (m, p) == (1, 2), (m, p)
    with zipfile.ZipFile(os.path.join(tmp, 'o.zip')) as z: assert 'zj_candidates_sheet.pdf' in z.namelist()
    print('selftest ok: 26 rows -> 2 pages, the one missing image is counted and drawn as a red box, not silently skipped')
if __name__ == '__main__':
    a = sys.argv[1:2]
    if a == ['rank']: rank()
    elif a == ['build']: build(sys.argv[2], sys.argv[3])
    else: selftest()
