#!/usr/bin/env python3
"""Experiment A analysis. Reads outputs/<arm>/*.json (scorer) and the stored judged findings. Counts and flags only.

usage: analyze.py [--haiku-echo stored|fixed]    writes tables.md, findings-<arm>.csv, summary.json next to the README
"""
import csv, json, math, os, statistics, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOTAL_GOLD = 173
BASE_GOLD = 104            # goldens kept by the proximity rule on the stored (uncorrected) data
ARMS = ['haiku', 'opus']
HALF_A = {'cal.com', 'sentry', 'sentry-greptile'}
echo_src = sys.argv[sys.argv.index('--haiku-echo') + 1] if '--haiku-echo' in sys.argv else 'fixed'


def echoed(items_h, it, w=10):
    return any(h['path'] == it['path'] and abs(h['line'] - it['line']) <= w for h in items_h)


def load(arm):
    P = data.opus()
    H = data.haiku_fixed() if echo_src == 'fixed' else data.haiku_stored()
    flat = []
    for u, p in P.items():
        key = data.pr_key(p['row'])
        f = '%s/outputs/%s/%s.json' % (ROOT, arm, key)
        sc = {x['id']: x for x in json.load(open(f))['findings']} if os.path.exists(f) else {}
        for it in p['items']:
            s = sc.get(it['i'])
            flat.append(dict(it, pr=key, half='A' if p['row']['repo'] in HALF_A else 'B',
                             score=s['score'] if s else None, reason=s['reason'] if s else '',
                             kind=s['kind'] if s else None, group=(key, s['group']) if s else None,
                             echo=echoed(H[u]['items'], it), ngold=len(it['golds']),
                             hc=sum(1 for g in it['golds'] if g['sev'] in ('high', 'critical'))))
    return flat


def m(sel):
    n = len(sel); tp = sum(x['ngold'] for x in sel); fp = sum(x['fp'] for x in sel)
    hc = sum(x['hc'] for x in sel); mf = sum(1 for x in sel if x['ngold'])
    r = tp / TOTAL_GOLD; p = tp / (tp + fp) if tp + fp else 0
    f1 = 2 * p * r / (p + r) if p + r else 0; f2 = 5 * p * r / (4 * p + r) if p + r else 0
    return dict(n=n, matched=mf, tp=tp, hc=hc, fp=fp, R=100 * r, P=100 * p, F1=100 * f1, F2=100 * f2)


def row(name, s):
    return '| %s | %d | %d | %d | %d | %d | %.1f | %.1f | %.1f | %.1f |' % (
        name, s['n'], s['matched'], s['tp'], s['hc'], s['fp'], s['R'], s['P'], s['F1'], s['F2'])


HDR = '| %s | Findings | Matched a golden | Goldens | H+C goldens | FP | R | P | F1 | F2 |\n|---|---|---|---|---|---|---|---|---|---|'
out = []
def w(s=''): out.append(s)


def topn_expected(flat, keyfn, N):
    """Expected FP and goldens in the top N when ties at the boundary are broken at random."""
    groups = collections.defaultdict(list)
    for x in flat: groups[keyfn(x)].append(x)
    fp = tp = 0.0; left = N
    for k in sorted(groups):
        g = groups[k]
        take = min(left, len(g)); frac = take / len(g)
        fp += frac * sum(x['fp'] for x in g); tp += frac * sum(x['ngold'] for x in g); left -= take
        if left <= 0: break
    return fp, tp


def auc(flat, keyfn):  # higher keyfn = more likely real; ties count half; positives = matched, negatives = FP
    pos = [keyfn(x) for x in flat if x['ngold']]; neg = [keyfn(x) for x in flat if x['fp']]
    s = sum((a > b) + 0.5 * (a == b) for a in pos for b in neg)
    return s / (len(pos) * len(neg))


def spearman(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = rk(a), rk(b); ma, mb = statistics.mean(ra), statistics.mean(rb)
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))


ALL = {a: load(a) for a in ARMS}
O = [x for x in ALL['opus']]
summary = dict(echo_source=echo_src)
base = ALL['opus']
base_all = m(base); prox = m([x for x in base if x['echo']])
w('## Baselines on the corrected Opus data (echo source: %s Haiku run)\n' % echo_src)
w(HDR % 'Rule'); w(row('all findings', base_all)); w(row('proximity: echoed by Haiku +-10', prox))
w(row('not echoed (second section)', m([x for x in base if not x['echo']])))
summary['baseline_all'] = base_all; summary['proximity'] = prox
w('\nKept-goldens mark used below: `>=104` as in the brief (stored data) and `>=%d` = this corrected proximity row.\n' % prox['tp'])

rules = {}   # arm -> {name: selection fn}
for arm in ARMS:
    flat = ALL[arm]
    assert all(x['score'] is not None for x in flat if True) or print('missing scores', arm, sum(x['score'] is None for x in flat))
    w('## Arm: %s scorer\n' % arm)
    w('### 1. Threshold on score (main section = score >= t)\n')
    w('| t | Main: findings | matched | goldens | H+C | FP | R | P | F1 | F2 | Second: findings | matched | goldens | H+C | FP | mark |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    sec = {}
    for t in range(1, 10):
        a = m([x for x in flat if x['score'] >= t]); b = m([x for x in flat if x['score'] < t]); sec[t] = a
        mark = ('>=104 ' if a['tp'] >= BASE_GOLD else '') + ('>=prox' if a['tp'] >= prox['tp'] else '')
        w('| %d | %d | %d | %d | %d | %d | %.1f | %.1f | %.1f | %.1f | %d | %d | %d | %d | %d | %s |' % (
            t, a['n'], a['matched'], a['tp'], a['hc'], a['fp'], a['R'], a['P'], a['F1'], a['F2'],
            b['n'], b['matched'], b['tp'], b['hc'], b['fp'], mark))
    summary[arm + '_thresholds'] = {t: sec[t] for t in sec}
    ok = [t for t in sec if sec[t]['tp'] >= BASE_GOLD]
    if ok:
        t = max(ok); w('\nHighest threshold keeping >= 104 goldens: t=%d, %d findings, %d FP (proximity: %d findings, %d FP, %d goldens).\n' % (
            t, sec[t]['n'], sec[t]['fp'], prox['n'], prox['fp'], prox['tp']))
        summary[arm + '_t104'] = dict(t=t, **sec[t])
    okp = [t for t in sec if sec[t]['tp'] >= prox['tp']]
    if okp:
        t = max(okp); w('Highest threshold keeping >= %d goldens (the corrected proximity row): t=%d, %d findings, %d FP.\n' % (prox['tp'], t, sec[t]['n'], sec[t]['fp']))
        summary[arm + '_tprox'] = dict(t=t, **sec[t])

    w('### 2. Ranking quality\n')
    w('Top N across the 50 PRs; ties at the boundary are broken at random, so FP and goldens are expected values. AUC = probability that a finding that matched a golden outranks a false positive (0.5 = chance).\n')
    w('| Ranking | AUC | Top 100: FP / goldens | Top 150: FP / goldens | Top 200: FP / goldens |\n|---|---|---|---|---|')
    rk = {'score (this arm)': lambda x: -x['score'], 'severity, then confidence (Wachiman labels)': lambda x: (data.SEV[x['sev']], data.CONF[x['conf']]),
          'echoed by Haiku (binary)': lambda x: 0 if x['echo'] else 1}
    rkr = {}
    for name, kf in rk.items():
        hi = (lambda kf: lambda x: -kf(x) if not isinstance(kf(x), tuple) else (-kf(x)[0], -kf(x)[1]))(kf)
        a = auc(flat, (lambda kf: lambda x: (-kf(x)[0], -kf(x)[1]) if isinstance(kf(x), tuple) else -kf(x))(kf))
        cells = []
        for N in (100, 150, 200):
            fp, tp = topn_expected(flat, kf, N); cells.append('%.1f / %.1f' % (fp, tp)); rkr[(name, N)] = (fp, tp)
        w('| %s | %.3f | %s |' % (name, a, ' | '.join(cells)))
        summary.setdefault(arm + '_rank', {})[name] = dict(auc=a, **{str(N): rkr[(name, N)] for N in (100, 150, 200)})
    w()

    w('### 3. Score combined with proximity\n')
    w(HDR % 'Rule')
    R_ = {}
    for t in range(1, 10):
        R_['score>=%d' % t] = (lambda t: lambda x: x['score'] >= t)(t)
        R_['score>=%d OR echo' % t] = (lambda t: lambda x: x['score'] >= t or x['echo'])(t)
        R_['score>=%d AND echo' % t] = (lambda t: lambda x: x['score'] >= t and x['echo'])(t)
    comb = {}
    for name, fn in R_.items():
        s = m([x for x in flat if fn(x)]); comb[name] = s
        if '>=' in name and ('OR' in name or 'AND' in name): w(row(name, s))
    rules[arm] = (R_, comb)
    summary[arm + '_combined'] = comb
    w()

    w('### 6. Kind tag vs outcome\n')
    w('| Kind | Findings | Matched a golden | FP | FP / findings | Mean score |\n|---|---|---|---|---|---|')
    kinds = collections.defaultdict(list)
    for x in flat: kinds[x['kind']].append(x)
    kt = {}
    for k, xs in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
        fp = sum(x['fp'] for x in xs); mt = sum(1 for x in xs if x['ngold'])
        kt[k] = dict(n=len(xs), matched=mt, fp=fp)
        w('| %s | %d | %d | %d | %.0f%% | %.1f |' % (k, len(xs), mt, fp, 100 * fp / len(xs), statistics.mean(x['score'] for x in xs)))
    summary[arm + '_kinds'] = kt
    w()

    w('### 5. Groups\n')
    G = collections.defaultdict(list)
    for x in flat: G[x['group']].append(x)
    sizes = collections.Counter(min(len(g), 5) for g in G.values())
    fp_with_matched = sum(x['fp'] for g in G.values() if any(y['ngold'] for y in g) for x in g)
    fp_total = sum(x['fp'] for x in flat)
    allfp = sum(1 for g in G.values() if not any(y['ngold'] for y in g) and all(y['fp'] for y in g))
    multi = [g for g in G.values() if sum(y['ngold'] for y in g) >= 2]
    multi_f = [g for g in G.values() if sum(1 for y in g if y['ngold']) >= 2]
    w('- Groups: %d for %d findings. Size 1: %d, 2: %d, 3: %d, 4: %d, 5 or more: %d.' % (
        len(G), len(flat), sizes[1], sizes[2], sizes[3], sizes[4], sizes[5]))
    w('- FP that share a group with a finding that matched a golden: %d of %d FP.' % (fp_with_matched, fp_total))
    w('- Groups made only of FP: %d. Posting each group as one comment would leave %d comments; at most %d FP findings disappear (upper bound: %d FP next to a match + %d FP findings folded inside all-FP groups).' % (
        allfp, len(G), fp_with_matched + (sum(len(g) for g in G.values() if not any(y['ngold'] for y in g) and all(y['fp'] for y in g)) - allfp),
        fp_with_matched, sum(len(g) for g in G.values() if not any(y['ngold'] for y in g) and all(y['fp'] for y in g)) - allfp))
    w('- Groups that contain 2 or more distinct goldens (over-merge risk): %d (%d contain 2 or more separate matched findings).' % (len(multi), len(multi_f)))
    summary[arm + '_groups'] = dict(groups=len(G), sizes=dict(sizes), fp_with_matched=fp_with_matched, fp=fp_total, allfp_groups=allfp, multi_golden=len(multi), multi_findings=len(multi_f))
    w()

    w('### 7. Cost and wall time\n')
    cs = []; ts = []
    for f in sorted(os.listdir('%s/outputs/%s' % (ROOT, arm))):
        if f.endswith('.json') and '.raw' not in f:
            d = json.load(open('%s/outputs/%s/%s' % (ROOT, arm, f)))
            if not d.get('empty'): cs.append(d['cost']); ts.append(d['seconds'])
    w('- %d scorer calls. Cost per PR: median $%.3f, mean $%.3f, max $%.2f, total $%.2f (subscription estimate from `total_cost_usd`).' % (len(cs), statistics.median(cs), statistics.mean(cs), max(cs), sum(cs)))
    w('- Wall time per PR: median %.0f s, mean %.0f s, max %.0f s, total %.0f min (two calls in flight).' % (statistics.median(ts), statistics.mean(ts), max(ts), sum(ts) / 60))
    w('- Review (Opus 5.5 high alone): median $0.48 per PR, $26.26 total with the corrected rows. Scorer as a share of the review: %.1f%%.\n' % (100 * sum(cs) / 26.26))
    summary[arm + '_cost'] = dict(n=len(cs), median=statistics.median(cs), mean=statistics.mean(cs), total=sum(cs), t_median=statistics.median(ts), t_total_min=sum(ts) / 60)

    with open('%s/findings-%s.csv' % (ROOT, arm), 'w', newline='') as fh:
        cw = csv.writer(fh); cw.writerow(['pr', 'id', 'path', 'line', 'severity', 'confidence', 'topic', 'score', 'kind', 'group', 'goldens', 'hc_goldens', 'fp', 'echo'])
        for x in flat: cw.writerow([x['pr'], x['i'], x['path'], x['line'], x['sev'], x['conf'], x['topic'], x['score'], x['kind'], x['group'][1], x['ngold'], x['hc'], int(x['fp']), int(x['echo'])])

# 4. split sample
w('## 4. Split sample (A = Cal.com + Sentry, 77 goldens; B = Grafana + Discourse + Keycloak, 96 goldens)\n')
def half_m(sel, h):
    s = m([x for x in sel if x['half'] == h]); return s
def half_row(name, flat, fn):
    out_ = []
    for h in 'AB':
        s = half_m([x for x in flat if fn(x)], h)
        gold = 77 if h == 'A' else 96
        r = s['tp'] / gold; p = s['tp'] / (s['tp'] + s['fp']) if s['tp'] + s['fp'] else 0; f1 = 2 * p * r / (p + r) if p + r else 0
        out_.append('%d / %d / %d | %.1f / %.1f / %.1f' % (s['n'], s['tp'], s['fp'], 100 * r, 100 * p, 100 * f1))
    return '| %s | %s |' % (name, ' | '.join(out_))
w('| Rule | A: kept / goldens / FP | A: R / P / F1 | B: kept / goldens / FP | B: R / P / F1 |\n|---|---|---|---|---|')
w(half_row('all findings', base, lambda x: True)); w(half_row('proximity: echoed +-10', base, lambda x: x['echo']))
for arm in ARMS:
    R_, comb = rules[arm]; flat = ALL[arm]
    ranked = sorted(comb.items(), key=lambda kv: -kv[1]['F1'])
    seen = set(); best = []
    for nm, s in ranked:
        if (s['n'], s['tp']) in seen: continue
        seen.add((s['n'], s['tp'])); best.append(nm)
        if len(best) == 2: break
    for nm in best: w(half_row('%s: %s (best by F1)' % (arm, nm), flat, R_[nm]))
    summary[arm + '_best2'] = best
w('\nHeld-out check: threshold chosen on A by F1, evaluated on B (and the reverse).\n')
w('| Arm | Family | t chosen on A | B result: kept / goldens / FP / F1 | t chosen on B | A result: kept / goldens / FP / F1 |\n|---|---|---|---|---|---|')
for arm in ARMS:
    R_, comb = rules[arm]; flat = ALL[arm]
    for fam, pat in (('score>=t', lambda t: 'score>=%d' % t), ('score>=t OR echo', lambda t: 'score>=%d OR echo' % t), ('score>=t AND echo', lambda t: 'score>=%d AND echo' % t)):
        def f1h(t, h):
            s = half_m([x for x in flat if R_[pat(t)](x)], h); g = 77 if h == 'A' else 96
            r = s['tp'] / g; p = s['tp'] / (s['tp'] + s['fp']) if s['tp'] + s['fp'] else 0
            return (2 * p * r / (p + r) if p + r else 0), s
        tA = max(range(1, 10), key=lambda t: f1h(t, 'A')[0]); tB = max(range(1, 10), key=lambda t: f1h(t, 'B')[0])
        fb, sb = f1h(tA, 'B'); fa, sa = f1h(tB, 'A')
        w('| %s | %s | %d | %d / %d / %d / %.1f | %d | %d / %d / %d / %.1f |' % (arm, fam, tA, sb['n'], sb['tp'], sb['fp'], 100 * fb, tB, sa['n'], sa['tp'], sa['fp'], 100 * fa))
w()


w('## False positives set aside per golden set aside (second section)\n')
w('Higher is better: how many false alarms leave the main section for each known bug that leaves with them. Whole-set baseline: %d FP over %d goldens.\n' % (base_all['fp'], base_all['tp']))
w('| Rule | Second section: FP | Goldens | H+C goldens | FP per golden |\n|---|---|---|---|---|')
nb = [x for x in base if not x['echo']]; sb = m(nb)
w('| proximity (not echoed) | %d | %d | %d | %.1f |' % (sb['fp'], sb['tp'], sb['hc'], sb['fp'] / max(sb['tp'], 1)))
for arm in ARMS:
    for t in range(3, 10):
        sb = m([x for x in ALL[arm] if x['score'] < t])
        w('| %s score < %d | %d | %d | %d | %.1f |' % (arm, t, sb['fp'], sb['tp'], sb['hc'], sb['fp'] / max(sb['tp'], 1)))
w()
w('## Agreement between the two scorers\n')
hs = {(x['pr'], x['i']): x['score'] for x in ALL['haiku']}; os_ = {(x['pr'], x['i']): x['score'] for x in ALL['opus']}
ks = sorted(hs)
a = [hs[k] for k in ks]; b = [os_[k] for k in ks]
w('- Spearman rho between Haiku and Opus scores over %d findings: %.2f. Same score: %.0f%%; within 1 point: %.0f%%.' % (
    len(ks), spearman(a, b), 100 * sum(x == y for x, y in zip(a, b)) / len(a), 100 * sum(abs(x - y) <= 1 for x, y in zip(a, b)) / len(a)))
w('- Mean score: Haiku %.2f, Opus %.2f.' % (statistics.mean(a), statistics.mean(b)))
dist = {arm: collections.Counter(x['score'] for x in ALL[arm]) for arm in ARMS}
w('\n| Score | ' + ' | '.join(str(i) for i in range(11)) + ' |\n|---|' + '---|' * 11)
for arm in ARMS: w('| %s findings | ' % arm + ' | '.join(str(dist[arm][i]) for i in range(11)) + ' |')
for arm in ARMS:
    w('| %s FP | ' % arm + ' | '.join(str(sum(x['fp'] for x in ALL[arm] if x['score'] == i)) for i in range(11)) + ' |')
    w('| %s goldens | ' % arm + ' | '.join(str(sum(x['ngold'] for x in ALL[arm] if x['score'] == i)) for i in range(11)) + ' |')
summary['spearman'] = spearman(a, b)
open(ROOT + '/tables.md', 'w').write('\n'.join(out) + '\n')
json.dump(summary, open(ROOT + '/summary.json', 'w'), indent=1, default=str)
print('\n'.join(out))
