"""cl item 6: pilot harness. READY, NOT RUN against any paid provider. US$0.
Parts: prompt templates per form (build_prompt), spend guard (generate), automatic pre-checks (precheck), per-image QA record (QA_FIELDS), measurement (measure), cost model (cost_per_approved).
The only provider is 'stub', which copies/perturbs a local file. Any other provider raises SpendBlocked: there is no code path to a paid call in this file.
Usage: python3 -I scripts/pilot_harness.py selftest | cost [price] [qa_minutes] [qa_rate_per_hr] | measure results.csv"""
import csv, sys, math, collections, os, hashlib
from PIL import Image, ImageChops

FORMS = {  # form key -> (what it is, how it sits). Keys = cl-template-plan.md.
 'ear: drop on hook': ('a drop earring on a hook', 'worn on one ear, shown in profile, the drop hanging free'),
 'ear: post with drop': ('a post earring with a hanging drop', 'worn on one ear in profile, post fixed, drop hanging free'),
 'ear: stud': ('a stud earring', 'worn on the ear lobe in profile, flush to the ear'),
 'ear: hoop': ('a hoop earring', 'worn through the ear lobe in profile, hoop closed'),
 'neck: pendant on chain': ('a pendant on a chain', 'worn at the neckline, pendant resting centred below the collarbone, chain following the neck'),
 'neck: collar/statement': ('a collar or statement necklace', 'worn close at the base of the neck, lying flat'),
 'neck: station chain': ('a long station chain necklace', 'worn long, stations evenly spaced as in the reference, drape following gravity'),
 'hand: ring': ('a ring', 'worn on a finger of a relaxed hand, band fully visible'),
 'wrist: bracelet': ('a bracelet', 'worn on a wrist, clasp as in the reference'),
 'wrist: cuff/bangle': ('a cuff or bangle', 'worn on a wrist, opening and width as in the reference'),
 'wrist: watch': ('a watch', 'worn on a wrist, dial legible and unchanged'),
 'still: loose pendant/charm': ('a loose pendant or charm', 'laid or propped, not worn, bail and face visible')}
CONCEPTS = {  # filled from reference/cl-art-direction.md once David picks; the harness refuses to build a prompt without one.
 'A': dict(setting='pale stone or linen surface, at most one prop', crop='tight, piece fills 50-70% of frame', light='soft window daylight from one side', model='no person'),
 'B': dict(setting='neutral interior, linen and soft wall tones', crop='jaw-down or profile behind the ear, face outside the frame', light='warm natural side light, shallow depth of field', model='fully AI-generated person, face not shown'),
 'C': dict(setting='a table or window seat with a small everyday scene', crop='wide, piece 5-10% of frame, only hands or wrists visible', light='golden-hour or cafe light', model='hands only, no face')}
BASE = ("The attached reference photo is the product. Reproduce {desc} EXACTLY as shown: same shape, proportions, stones ({stone}), metal colour ({metal}), and fastening. "
        "Do not add, remove, resize, recolour or restyle any part of the piece. Placement: {sit}. Scene: {setting}. Crop: {crop}. Light: {light}. Model: {model}. "
        "Never show a full face. No text, logos or watermarks. Output {aspect}, long edge {px} px.")
def build_prompt(form, concept, stone, metal, aspect='4:5', px=1500):
    """Variables: form (data: classified form), concept (David's pick), stone and metal (HUMAN, read from the reference: no such field in the data), aspect, px."""
    if concept not in CONCEPTS: raise ValueError('art direction not chosen: concept must be one of ' + ','.join(CONCEPTS))
    d, s = FORMS[form]; return BASE.format(desc=d, sit=s, stone=stone, metal=metal, aspect=aspect, px=px, **CONCEPTS[concept])

class SpendBlocked(RuntimeError): pass
def generate(provider, ref_path, out_path, prompt):
    """Only 'stub' exists. Anything else is a paid call and is blocked until David lifts the limit AND a real provider is written."""
    if provider != 'stub': raise SpendBlocked(f'provider {provider!r} blocked: spend is US$0 until David chooses an art direction')
    im = Image.open(ref_path).convert('RGB'); w = max(im.size); canvas = Image.new('RGB', (w, int(w * 1.25)), (200, 190, 175))
    im.thumbnail((int(w * 0.8), int(w * 0.8))); canvas.paste(im, ((canvas.width - im.width) // 2, (canvas.height - im.height) // 2)); canvas.save(out_path); return out_path  # new 4:5 scene around the reference: stands in for a generated image

def precheck(ref_path, out_path, min_long=1000, aspect=0.8):
    """Automatic, cheap, per attempt. Returns list of failures. Does not replace a person."""
    f = []
    try: im = Image.open(out_path).convert('RGB')
    except Exception: return ['unreadable']
    if max(im.size) < min_long: f.append('too small')
    if abs(im.width / im.height - aspect) > 0.02: f.append('wrong aspect')
    ex = im.convert('L').getextrema()
    if ex[1] - ex[0] < 8: f.append('blank')
    ref = Image.open(ref_path).convert('RGB').resize(im.size)
    if ImageChops.difference(ref, im).getbbox() is None: f.append('identical to reference (nothing was generated)')
    return f

QA_FIELDS = ['sku', 'form', 'attempt', 'precheck_fail',
 'fid_shape', 'fid_stones_count', 'fid_metal_colour', 'fid_fastening', 'no_added_or_missing_parts',  # CRITICAL: product fidelity
 'no_full_face', 'anatomy_ok', 'scale_plausible', 'no_text_or_logo', 'no_artifacts',                 # CRITICAL
 'composition_matches_concept', 'light_matches_concept',                                           # MINOR
 'qa_seconds', 'pass', 'note']
CRITICAL = QA_FIELDS[4:14]
def verdict(row):
    """pass iff the precheck is clean and every CRITICAL item is 'y'. Minor items are recorded, not gating."""
    return 'y' if not row['precheck_fail'] and all(row[k] == 'y' for k in CRITICAL) else 'n'

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return ((c - h) / d, (c + h) / d)
def measure(rows, gen_price=0.0, qa_rate_per_hr=0.0):
    """rows: one per attempt. A slot = sku. Approved = a slot with a pass. Per form: slots, attempts, first-pass rate (Wilson), approved, abandoned, attempts per approved, QA minutes per approved, cost per approved."""
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows: by[r['form']][r['sku']].append(r)
    out = {}
    for form, slots in by.items():
        att = sum(len(v) for v in slots.values()); appr = sum(any(a['pass'] == 'y' for a in v) for v in slots.values())
        first = sum(sorted(v, key=lambda a: int(a['attempt']))[0]['pass'] == 'y' for v in slots.values()); qa = sum(float(a['qa_seconds'] or 0) for v in slots.values() for a in v) / 60
        cost = att * gen_price + qa / 60 * qa_rate_per_hr
        out[form] = dict(slots=len(slots), attempts=att, approved=appr, abandoned=len(slots) - appr, first_pass=first / len(slots), first_ci=wilson(first, len(slots)),
                         attempts_per_approved=att / appr if appr else None, qa_min_per_approved=qa / appr if appr else None, cost_per_approved=cost / appr if appr else None)
    return out
def cost_per_approved(p, k, price=1.0, qa_min=0.0, qa_rate_per_hr=0.0):
    """Closed form, independent attempts at pass rate p, up to k attempts per slot, one QA per attempt. Returns (approval prob per slot, attempts per approved, cost per approved).
    Assumes attempts are independent; hard pieces fail together, so measure it in the pilot rather than trust this for them."""
    if not 0 < p <= 1: raise ValueError('p in (0,1]')
    a = 1 - (1 - p) ** k; exp_att = (1 - (1 - p) ** k) / p; per_att = price + qa_min / 60 * qa_rate_per_hr
    return a, exp_att / a, exp_att * per_att / a

def selftest(d):
    os.makedirs(d, exist_ok=True); ref = os.path.join(d, 'ref.png')
    im = Image.new('RGB', (1200, 1000), (240, 238, 232)); px = im.load()
    for x in range(400, 800):
        for y in range(300, 700): px[x, y] = (150, 150, 160) if (x - 600) ** 2 + (y - 500) ** 2 < 150 ** 2 else px[x, y]
    im.save(ref)  # SYNTHETIC fixture standing in for a catalogue photo (none available here)
    pr = build_prompt('ear: stud', 'B', 'none', 'silver'); assert 'EXACTLY' in pr and 'Never show a full face' in pr
    try: build_prompt('ear: stud', 'Z', 'none', 'silver'); raise SystemExit('FAIL: no-concept prompt was built')
    except ValueError: pass
    try: generate('openai', ref, os.path.join(d, 'x.png'), pr); raise SystemExit('FAIL: paid provider not blocked')
    except SpendBlocked: pass
    out = generate('stub', ref, os.path.join(d, 'gen.png'), pr); assert precheck(ref, out) == [], precheck(ref, out)
    Image.new('RGB', (1000, 1250), (0, 0, 0)).save(os.path.join(d, 'blank.png')); assert 'blank' in precheck(ref, os.path.join(d, 'blank.png'))
    ref_same = os.path.join(d, 'same.png'); Image.open(ref).resize((1000, 1250)).save(ref_same); assert any('identical' in x for x in precheck(ref_same, ref_same))
    rows = []
    for sku, form, passes in [('S1', 'ear: stud', 'ny'), ('S2', 'ear: stud', 'y'), ('S3', 'ear: stud', 'nnn'), ('S4', 'hand: ring', 'y')]:
        for i, ch in enumerate(passes, 1):
            r = {k: 'y' for k in QA_FIELDS}; r.update(sku=sku, form=form, attempt=str(i), precheck_fail='', qa_seconds='120', note='')
            if ch == 'n': r['fid_stones_count'] = 'n'
            r['pass'] = verdict(r); assert r['pass'] == ch, (sku, i); rows.append(r)
    m = measure(rows, gen_price=1.0, qa_rate_per_hr=0.0)['ear: stud']; assert (m['slots'], m['attempts'], m['approved'], m['abandoned'], m['first_pass']) == (3, 6, 2, 1, 1 / 3), m
    assert abs(m['cost_per_approved'] - 3.0) < 1e-9; a, n, c = cost_per_approved(0.5, 3); assert abs(a - 0.875) < 1e-9 and abs(c - (1.75 / 0.875)) < 1e-9
    assert verdict({**rows[0], 'fid_shape': 'n', 'precheck_fail': ''}) == 'n' and verdict({**rows[1], 'precheck_fail': 'blank'}) == 'n'
    print('selftest ok: prompt guard, spend guard, 3 precheck failures fire, verdict gates on critical items, measure and cost model match hand arithmetic')
if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'selftest': selftest(sys.argv[2] if len(sys.argv) > 2 else '.scratch/harness_fixture')
    elif c == 'cost':
        price, qm, rate = (float(x) for x in (sys.argv[2:5] + ['1', '0', '0'][len(sys.argv[2:5]):]))
        print(f'price per generation={price}, QA minutes per attempt={qm}, QA rate per hour={rate}\nrows: pass rate p; columns: max attempts k. cell = cost per approved image (approval prob per slot)')
        print('p\\k ' + ''.join(f'{k:>16}' for k in (1, 2, 3, 5)))
        for p in (0.2, 0.3, 0.5, 0.7, 0.9): print(f'{p:<4}' + ''.join('{:>16}'.format('{:.2f} ({:.0%})'.format(cost_per_approved(p, k, price, qm, rate)[2], cost_per_approved(p, k)[0])) for k in (1, 2, 3, 5)))
    elif c == 'measure':
        for f, m in measure(list(csv.DictReader(open(sys.argv[2], encoding='utf8')))).items(): print(f, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in m.items()})
    else: print(__doc__)
