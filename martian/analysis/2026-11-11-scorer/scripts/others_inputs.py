"""Inputs for "did other tools raise the same issue": others_inputs.py

For every audited Opus finding (Cal.com, Sentry) writes, per repository, the finding and the comments ten other
tools left on the same PR in Martian's published results (candidates.json, tool comments only, no golden text).
"""
import csv, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UP = os.path.expanduser('~/.cache/wachiman-martian/martian-upstream/offline/results/anthropic_claude-opus-4-5-20251101/candidates.json')
TOOLS = ['qodo-extended-v2', 'cubic-v2', 'augment', 'macroscope', 'greptile-v4-1', 'bugbot', 'devin', 'claude-code', 'coderabbit', 'copilot-v2']
C = json.load(open(UP))
url = {data.pr_key(p['row']): u for u, p in data.opus().items()}
F = {}
for f in glob.glob(os.path.join(ROOT, 'audit', 'inputs', '*.json')):
    d = json.load(open(f))
    for x in d['findings']: F[(d['pr'], str(x['id']))] = x
out = {'cal.com': {}, 'sentry': {}}
for r in csv.DictReader(open(os.path.join(ROOT, 'audit', 'audit.csv'))):
    rp = 'cal.com' if r['pr'].startswith('cal.com') else 'sentry'
    pr = out[rp].setdefault(r['pr'], {'ours': [], 'others': []})
    x = F[(r['pr'], r['id'])]
    pr['ours'].append({'id': int(r['id']), 'file': x['path'], 'line': x['line'], 'title': x['title'], 'body': x['body'][:500]})
for rp in out:
    for k, pr in out[rp].items():
        n = 0
        for t in TOOLS:
            for c in C[url[k]].get(t, []):
                n += 1; pr['others'].append({'n': n, 'tool': t, 'file': c.get('path'), 'line': c.get('line'), 'text': c['text'][:600]})
    json.dump(out[rp], open(os.path.join(ROOT, 'audit', 'others', 'input-%s.json' % rp), 'w'), indent=1)
    print(rp, len(out[rp]), 'PRs', sum(len(p['ours']) for p in out[rp].values()), 'ours', sum(len(p['others']) for p in out[rp].values()), 'others',
          os.path.getsize(os.path.join(ROOT, 'audit', 'others', 'input-%s.json' % rp)), 'bytes')
