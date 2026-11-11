import sys; sys.path.insert(0,'/tmp/martian-digest')
from load import *
def fb(p,r,b=1): return (1+b*b)*p*r/(b*b*p+r) if p+r else 0
allruns=dict(runs); 
for t in ['qodo-extended-v2','augment','claude-code']: allruns[t]=comp[t]
print('PER REPO  (R, P, TP, FP, cands/PR, nPRs)')
for t,e in allruns.items():
    line=[]
    for rp in ['cal.com','sentry','discourse','grafana','keycloak']:
        sub={u:r for u,r in e.items() if repo2(u)==rp}
        tp=sum(r['tp'] for r in sub.values());fp=sum(r['fp'] for r in sub.values());fn=sum(r['fn'] for r in sub.values());c=sum(r['total_candidates'] for r in sub.values())
        hc=sum(1 for r in sub.values() for g in r['true_positives'] if g['severity'].lower() in HC); 
        hct=hc+sum(1 for r in sub.values() for g in r['false_negatives'] if g['severity'].lower() in HC)
        p=tp/(tp+fp) if tp+fp else 0;r=tp/(tp+fn); line.append(f"{rp}: R{r:.0%} P{p:.0%} F{fb(p,r):.0%} HC{hc}/{hct} c/PR{c/len(sub):.1f}")
    print(f"{t:18s}",' | '.join(line))
print('PR counts',collections.Counter(repo2(u) for u in runs['opus']))
print('RECALL by sev / cat')
for t,e in allruns.items():
    g=golds(e)
    s=collections.defaultdict(lambda:[0,0]);c=collections.defaultdict(lambda:[0,0])
    for k,v in g.items():
        s[v['sev']][1]+=1; s[v['sev']][0]+=v['found']; c[v['cat']][1]+=1; c[v['cat']][0]+=v['found']
    print(f"{t:18s}",' '.join(f"{k}:{a}/{b}" for k,(a,b) in sorted(s.items())),'||',' '.join(f"{k}:{a}/{b}" for k,(a,b) in sorted(c.items(),key=lambda kv:-kv[1][1])))
# Per-PR: findings count vs precision quartiles for opus
print('PRs with 0 TP for opus', sum(1 for r in runs['opus'].values() if r['tp']==0), 'findings in those', sum(r['total_candidates'] for r in runs['opus'].values() if r['tp']==0))
# competitor findings-per-PR distribution
for t in ['qodo-extended-v2','augment','claude-code','opus']:
    e=allruns[t]; import statistics
    c=[r['total_candidates'] for r in e.values()]; print(t,'cands/PR median',statistics.median(c),'max',max(c),'PRs with 0 cands',sum(1 for x in c if x==0))
# multi golden matches per candidate
for t,e in allruns.items():
    m=collections.Counter()
    for r in e.values():
        cc=collections.Counter(g['matched_candidate'] for g in r['true_positives'])
        for v in cc.values(): m[v]+=1
    print(t,'candidates matching n goldens',dict(m),' non-FP cands',sum(r['total_candidates']-r['fp'] for r in e.values()),'cands',sum(r['total_candidates'] for r in e.values()))
