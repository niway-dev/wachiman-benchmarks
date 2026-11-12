"""Stored Opus / Haiku findings with their judge outcome, per PR. Counts and ids only; golden text is never read.

Opus rows for Keycloak 37634 and 36880 come from the corrected re-run (runs/2026-11-11-keycloak-range-fix).
Item fields: i (index in the review's findings list), path, line, sev, conf, topic, title, body, text,
golds (goldens this finding was the best match of), fp (judged a false positive).
"""
import csv, glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MARTIAN = os.environ.get('MARTIAN_DIR') or os.path.abspath(os.path.join(HERE, '..', '..', '..'))      # .../martian
WL = list(csv.DictReader(open(MARTIAN + '/worklist.tsv'), delimiter='\t'))
RUNS = {'opus': '2026-11-07-v1.9.0-opus-5-5', 'haiku': '2026-11-07-v1.9.0-haiku-5-5-high'}
FIX = '2026-11-11-keycloak-range-fix'
FIXED_URLS = {'https://github.com/keycloak/keycloak/pull/37634', 'https://github.com/keycloak/keycloak/pull/36880'}
HAIKU_FIX = os.path.join(HERE, '..', 'haiku-keycloak-rerun')            # filled by Experiment B
SEV = {'blocker': 0, 'fix': 1, 'consider': 2, 'info': 3}
CONF = {'high': 0, 'medium': 1, 'low': 2}


def _review(datadir, row):
    b = datadir + '/reviews/' + row['repo'] + '/'
    sfx = row['branch_suffix']
    fs = glob.glob(b + sfx + '.json') or glob.glob(b + sfx + '-flat.json') or glob.glob(b + sfx.replace('-flat', '') + '.json')
    return json.load(open(fs[0])) if fs else None


def _match(items, text):
    m = [it for it in items if it['text'] == text] or \
        [it for it in items if it['text'].startswith(text) or text.startswith(it['text'][:len(text)])]
    return m


def build(run, fix_dir=None):
    """fix_dir: a run directory (with data/) whose rows replace the stored ones for FIXED_URLS."""
    base = MARTIAN + '/runs/' + RUNS[run] + '/data'
    ev = json.load(open(base + '/evaluations/wachiman.json'))
    out = {}
    for row in WL:
        u = row['golden_url']
        d = base
        e = ev[u]['wachiman']
        if fix_dir and u in FIXED_URLS:
            d = fix_dir + '/data'
            e = json.load(open(d + '/evaluations/wachiman.json'))[u]['wachiman']
        rv = _review(d, row)
        items = []
        for i, f in enumerate(rv['findings']):
            items.append(dict(i=i, path=f['path'], line=int(f['line'] or 0), sev=f['severity'], conf=f['confidence'],
                              topic=f['topic'], title=f['title'], body=f['body'], text=f['title'] + '\n\n' + f['body'],
                              golds=[], fp=False))
        for g in e['true_positives']:
            m = _match(items, g['matched_candidate'])
            if len(m) != 1:
                print('map issue', u, len(m), run)
            if m:
                m[0]['golds'].append(dict(sev=g['severity'].lower(), cat=g['category']))
        fps = [x['candidate'] for x in e['false_positives']]
        for it in items:
            it['fp'] = (not it['golds']) and any(
                it['text'] == x or it['text'].startswith(x) or x.startswith(it['text'][:len(x)]) for x in fps)
        out[u] = dict(row=row, items=items, nfn=len(e['false_negatives']), ntp=len(e['true_positives']),
                      fn=[g['severity'].lower() for g in e['false_negatives']])
    return out


def opus():
    return build('opus', MARTIAN + '/runs/' + FIX)


def haiku_stored():
    return build('haiku')


def haiku_fixed():
    return build('haiku', os.path.abspath(HAIKU_FIX))


def pr_key(row):
    return row['repo'] + '-' + row['branch_suffix']


if __name__ == '__main__':
    P = opus()
    n = sum(len(p['items']) for p in P.values())
    tp = sum(len(it['golds']) for p in P.values() for it in p['items'])
    fp = sum(it['fp'] for p in P.values() for it in p['items'])
    lost = sum((not it['golds']) and (not it['fp']) for p in P.values() for it in p['items'])
    print('findings', n, 'goldens matched', tp, 'FP', fp, 'neither', lost)
