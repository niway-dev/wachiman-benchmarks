import sys; sys.path.insert(0,'/tmp/martian-digest')
from load import *
U='/Users/cristiansotomayor-m5-pro/.cache/wachiman-martian/martian-upstream/offline/results/anthropic_claude-opus-4-5-20251101/evaluations.json'
st=json.load(open(U))
tools=collections.Counter(t for u in st for t in st[u]); print(len(tools),dict(tools))
G={k:golds(v) for k,v in runs.items()}
C={k:golds(v) for k,v in comp.items() if len(v)==50}
S={}
for u,tt in st.items():
    for t,r in tt.items():
        if r.get('skipped'): continue
        for g in r['true_positives']: S.setdefault(t,{})[(u,g['golden_comment'])]=True
keys=list(G['opus'])
miss=[k for k in keys if not G['opus'][k]['found']]
print('opus missed',len(miss),'HC missed',sum(1 for k in miss if G['opus'][k]['sev'].lower() in HC))
def tag(k): return G['opus'][k]
import itertools
rows=[]
for k in miss:
    rows.append(dict(k=k,sev=tag(k)['sev'],cat=tag(k)['cat'],repo=repo2(k[0]),h=G['haiku'][k]['found'],v=G['v110'][k]['found'],
      comp=[t for t in C if C[t][k]['found']], stored=sum(1 for t in S if (k in S[t])) ))
print('missed by repo',collections.Counter(r['repo'] for r in rows))
print('missed by sev',collections.Counter(r['sev'] for r in rows))
print('missed by cat',collections.Counter(r['cat'] for r in rows))
tot_by_repo=collections.Counter(repo2(k[0]) for k in keys); print('goldens by repo',tot_by_repo)
tot_by_sev=collections.Counter(G['opus'][k]['sev'] for k in keys); print(tot_by_sev)
tot_by_cat=collections.Counter(G['opus'][k]['cat'] for k in keys); print(tot_by_cat)
print('miss found by haiku',sum(r['h'] for r in rows),'by v110',sum(r['v'] for r in rows),'by haiku or v110',sum(r['h'] or r['v'] for r in rows))
for t in C: print(' missed-by-opus found by',t,sum(1 for r in rows if t in r['comp']))
print('by any of 3 competitors',sum(1 for r in rows if r['comp']),'; by any competitor or haiku/v110',sum(1 for r in rows if r['comp'] or r['h'] or r['v']))
print('found by none of anyone (3comp+haiku+v110)',sum(1 for r in rows if not (r['comp'] or r['h'] or r['v'])))
print('no stored tool found (22 tools Martian judge) and none of ours', sum(1 for r in rows if r['stored']==0 and not (r['h'] or r['v'])))
hcm=[r for r in rows if r['sev'].lower() in HC]
print('HC missed',len(hcm),'found by haiku',sum(r['h'] for r in hcm),'v110',sum(r['v'] for r in hcm),'comps',sum(1 for r in hcm if r['comp']),'any',sum(1 for r in hcm if r['comp'] or r['h'] or r['v']),'none',sum(1 for r in hcm if not (r['comp'] or r['h'] or r['v'])), 'stored 0:',sum(1 for r in hcm if r['stored']==0))
print('stored-found counts distribution for missed',collections.Counter(min(r['stored'],10)//2*2 for r in rows))
# Opus found goldens: how many tools find them (difficulty)
fnd=[k for k in keys if G['opus'][k]['found']]
print('avg #stored tools finding: opus-found',sum(sum(1 for t in S if k in S[t]) for k in fnd)/len(fnd),'missed',sum(r['stored'] for r in rows)/len(rows))
json.dump([dict(u=r['k'][0],g=r['k'][1],**{x:r[x] for x in('sev','cat','repo','h','v','comp','stored')}) for r in rows],open('/tmp/martian-digest/opus_misses.json','w'))
# Union
for a,b in [('opus','haiku'),('opus','v110'),('haiku','v110')]:
    A={k for k in keys if G[a][k]['found']};B={k for k in keys if G[b][k]['found']}
    hc=lambda s: sum(1 for k in s if G['opus'][k]['sev'].lower() in HC)
    print(a,b,'both',len(A&B),'only',a,len(A-B),'only',b,len(B-A),'union',len(A|B),'HC both',hc(A&B),'only a',hc(A-B),'only b',hc(B-A),'union',hc(A|B))
A={k for k in keys if G['opus'][k]['found']};B={k for k in keys if G['haiku'][k]['found']};V={k for k in keys if G['v110'][k]['found']}
print('3-way union',len(A|B|V),'HC',sum(1 for k in A|B|V if G['opus'][k]['sev'].lower() in HC),'in all three',len(A&B&V))
# union with competitors
for t in C:
    T={k for k in keys if C[t][k]['found']}
    print('opus U',t,len(A|T),'HC',sum(1 for k in A|T if G['opus'][k]['sev'].lower() in HC),' opus U haiku U',t,len(A|B|T))
allc=set().union(*[{k for k in keys if C[t][k]['found']} for t in C]); 
print('opus U all3 comps',len(A|allc),sum(1 for k in A|allc if G['opus'][k]['sev'].lower() in HC),'; all 6 sources',len(A|B|V|allc),sum(1 for k in A|B|V|allc if G['opus'][k]['sev'].lower() in HC))
print('goldens found by nobody (6 sources)',173-len(A|B|V|allc))
nobody=[k for k in keys if k not in (A|B|V|allc)]
print('nobody by sev',collections.Counter(G['opus'][k]['sev'] for k in nobody), 'and none of 22 stored', sum(1 for k in nobody if not any(k in S[t] for t in S)))
# union precision
def candset(name):
    return sum(r['total_candidates'] for r in runs[name].values())
print('union precision (goldens in union)/(sum findings): opus+haiku',len(A|B),'/',candset('opus')+candset('haiku'), len(A|B)/(candset('opus')+candset('haiku')))
print('   alt TP/(TP+FP) summed FPs', len(A|B)/(len(A|B)+174+314))
print('opus+haiku+v110', len(A|B|V)/(candset('opus')+candset('haiku')+candset('v110')))
