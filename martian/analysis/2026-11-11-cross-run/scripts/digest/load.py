import json,glob,os,collections
R='/tmp/martian-digest/feat_martian-v1-10-0/martian/'
HC={'high','critical'}
def ev(path,tool): 
    d=json.load(open(path)); return {u:t[tool] for u,t in d.items() if tool in t}
runs={
 'opus':ev(R+'runs/2026-11-07-v1.9.0-opus-5-5/data/evaluations/wachiman.json','wachiman'),
 'haiku':ev(R+'runs/2026-11-07-v1.9.0-haiku-5-5-high/data/evaluations/wachiman.json','wachiman'),
 'v110':ev(R+'runs/2026-11-10-v1.10.0-haiku-5-5-high-opus-verifier/data/evaluations/wachiman.json','wachiman'),
}
# competitors
comp=collections.defaultdict(dict)
for f in glob.glob(R+'reference/evaluations/rejudge-*.json'):
    for u,t in json.load(open(f)).items():
        for k,v in t.items(): comp[k][u]=v
def golds(e):
    out={}
    for u,r in e.items():
        if r.get('skipped'): continue
        for g in r['true_positives']: out[(u,g['golden_comment'])]=dict(sev=g['severity'],cat=g['category'],found=True,cand=g['matched_candidate'],conf=g['confidence'])
        for g in r['false_negatives']: out[(u,g['golden_comment'])]=dict(sev=g['severity'],cat=g['category'],found=False)
    return out
def repo(u):
    if 'greptile' in u: return u.split('/')[-3]
    return u.split('/')[4] if 'github.com' in u else u

import csv
WL=[r for r in csv.DictReader(open(R+'worklist.tsv'),delimiter='\t')]
def findings_by_url(runlabel):
    out={}
    for r in WL:
        # find file
        base=R+'runs/'+runlabel+'/data/reviews/'+r['repo']+'/'
        cands=glob.glob(base+r['branch_suffix']+'.json')+glob.glob(base+r['branch_suffix']+'-flat.json')
        if not cands: print('missing',r['repo'],r['branch_suffix']); continue
        out[r['golden_url']]=json.load(open(cands[0]))
    return out
RL={'opus':'2026-11-07-v1.9.0-opus-5-5','haiku':'2026-11-07-v1.9.0-haiku-5-5-high','v110':'2026-11-10-v1.10.0-haiku-5-5-high-opus-verifier'}
def repo2(u):
    r=repo(u); return r.replace('-greptile','').replace('discourse-graphite','discourse')
