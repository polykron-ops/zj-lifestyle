"""cl items 8-9 on cs's MEASURED dates (data/original_dates.csv). No network, no images. Reuses cl_dating's plausibility, per-SKU ladder, eligibility and cross-tabs.
Usage: python3 -I scripts/cl_dating_csv.py selftest | run [OUT.csv]
"""
import sys, os, csv, collections, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_dating as D

def exif_row(s):
    """EXIF string -> (state, date). '' = absent; unparseable / 0000:00:00 / pre-2000 / future / sentinel = implausible. Never filled in."""
    s = (s or '').strip()
    if not s: return 'absent', None
    d = D.parse_exif(s)
    return ('ok', d) if D.plausible(d) else ('implausible', None)
def zdate(s):
    try: return dt.date.fromisoformat(s.strip()) if s and s.strip() else None
    except Exception: return None
def files_from(rows):
    for r in rows:
        st, d = exif_row(r['exif_datetime_original'])
        yield dict(zip=r['zip'], entry=r['file'], sku=r['code'], inferred=False, exif_state=st, exif_date=d, edited=False, zip_date=zdate(r['zip_entry_date']), mtime_kind='zip',
                   folder_year=D.folder_year(r['folder']))
def load(path='data/original_dates.csv', skus=None):
    rows = [r for r in csv.DictReader(open(path, encoding='utf-8')) if r['code'] and (skus is None or r['code'] in skus)]
    return rows

def selftest():
    base = dict(n24_id='n24-x', status='new', zip='2023-001', folder='תמונות 2023/x', file='a.jpg')
    def case(code, exif, z, folder=None):
        r = dict(base, code=code, exif_datetime_original=exif, zip_entry_date=z)
        if folder: r['folder'] = folder
        return r
    rows = [case('A1', '2024:03:05 10:00:00', '2024-03-06'),          # ok, agree        -> exif, high
            case('A2', '0000:00:00 00:00:00', '2019-11-26'),          # placeholder      -> zip, exif implausible
            case('A3', '1994:01:01 00:00:00', '2024-02-02'),          # pre-2000         -> zip
            case('A4', '2031:01:01 00:00:00', '2022-05-05'),          # future           -> zip
            case('A5', '', '2022-05-05', 'x/2020'),                   # absent           -> zip
            case('A6', '', '', 'x/2021'),                             # nothing but folder -> folder, very low
            case('A7', '', '', 'x/none'),                             # nothing at all    -> none, unknown
            case('A8', '2025:01:01 00:00:00', '2021-01-01')]          # disagree         -> medium-disagree
    out = {r['sku']: r for r in D.per_sku(list(files_from(rows)))}
    exp = {'A1': ('exif', 'high'), 'A2': ('zip', 'low-disagree'), 'A3': ('zip', 'low-disagree'), 'A4': ('zip', 'low-disagree'), 'A5': ('zip', 'low-disagree'), 'A6': ('folder', 'very low'), 'A7': ('none', 'none'), 'A8': ('exif', 'medium-disagree')}
    bad = {k: (out[k]['source_used'], out[k]['confidence']) for k, v in exp.items() if (out[k]['source_used'], out[k]['confidence']) != v}
    assert not bad, bad
    for k in ('A2', 'A3', 'A4'): assert out[k]['exif_files_implausible'] == 1 and out[k]['exif_date'] == ''
    assert D.eligible(out['A7']) == 'unknown' and D.eligible(out['A1']) == 'eligible' and D.eligible(out['A5']) == 'ineligible'
    print('selftest ok: 8 cases (placeholder, pre-2000, future, absent, nothing, disagreement all handled, none filled in)')

def main(out_path):
    ds = {r['sku']: r for r in csv.DictReader(open('data/dataset_2485.csv', encoding='utf-8'))}
    all_rows = load(skus=set(ds))
    got = {r['code'] for r in all_rows}
    print('dataset SKUs', len(ds), '| with rows in original_dates.csv', len(got & set(ds)), '| missing', sorted(set(ds) - got)[:10])
    st = collections.Counter(r['status'] for r in all_rows); print('file rows for these SKUs by status', dict(st), 'total', len(all_rows))
    files = list(files_from(all_rows))
    print('file-level EXIF state:', dict(collections.Counter(f['exif_state'] for f in files)), '| zip date missing', sum(1 for f in files if not f['zip_date']), '| zip date implausible (<2000)', sum(1 for f in files if f['zip_date'] and not D.plausible(f['zip_date'])))
    ys = collections.Counter(f['exif_date'].year for f in files if f['exif_state'] == 'ok'); print('EXIF ok, by year:', dict(sorted(ys.items())))
    rows = D.per_sku(files)
    for r in rows:
        r['family'] = ds[r['sku']]['family']; r['origin'] = ds[r['sku']]['origin']; r['eligibility_cl'] = D.eligible(r)
    D.summary(rows)
    # sensitivity: latest rather than earliest plausible date per rung
    by = collections.defaultdict(list)
    for f in files: by[f['sku']].append(f)
    sens = collections.Counter()
    for sku, v in by.items():
        ex = [f['exif_date'] for f in v if f['exif_state'] == 'ok']; zp = [f['zip_date'] for f in v if D.plausible(f['zip_date'])]
        d = max(ex) if ex else max(zp) if zp else None
        sens['eligible' if d and d >= D.CUTOFF else 'ineligible' if d else 'unknown'] += 1
    print('sensitivity, LATEST file date per SKU (instead of earliest), exif else zip:', dict(sens))
    fam = collections.defaultdict(collections.Counter)
    for r in rows: fam[r['family']][r['eligibility_cl'].split(' ')[0]] += 1
    print('by family (cl eligible/ineligible/ambiguous/unknown | n):')
    for k, c in sorted(fam.items()): print(' ', k, dict(c), sum(c.values()))
    w = csv.DictWriter(open(out_path, 'w', newline='', encoding='utf-8'), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows); print('wrote', out_path, len(rows))
if __name__ == '__main__':
    if sys.argv[1:2] == ['selftest']: selftest()
    else: main(sys.argv[2] if len(sys.argv) > 2 else 'data/cl_dating_measured.csv')
