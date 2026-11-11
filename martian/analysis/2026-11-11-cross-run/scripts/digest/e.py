import sys; sys.path.insert(0,'/tmp/martian-digest')
from load import *
def fb(p,r,b=1): return (1+b*b)*p*r/(b*b*p+r) if p+r else 0
def build(k):
    F=findings_by_url(RL[k]); rows=[]
    ngold=sum(r['tp']+r['fn'] for r in runs[k].values())
    for u,r in runs[k].items():
        fps={x['candidate'] for x in r['false_positives']}
        best=collections.defaultdict(list)
        for g in r['true_positives']: best[g['matched_candidate']].append(g)
        for i,f in enumerate(F[u]['findings']):
            t=f"{f['title']}\n\n{f['body']}"
            rows.append(dict(u=u,repo=repo2(u),i=i,f=f,sev=f['severity'],conf=f['confidence'],topic=f['topic'],
                 fp=t in fps, gold=best.get(t,[]),text=t, len=len(f['body']),
                 tier=f.get('tier'),origin=f.get('origin'),vstat=(f.get('verification') or {}).get('status') if isinstance(f.get('verification'),dict) else None))
    return rows
def metrics(rows,keep=lambda x:True):
    K=[x for x in rows if keep(x)]
    tp=sum(len(x['gold']) for x in K); fp=sum(1 for x in K if x['fp'])
    hc=sum(1 for x in K for g in x['gold'] if g['severity'].lower() in HC)
    return tp,fp,hc,len(K)
def table(rows,key,title):
    c=collections.defaultdict(lambda:[0,0,0,0,0])
    for x in rows:
        v=c[key(x)]; v[0]+=1; v[1]+=x['fp']; v[2]+= (not x['fp']); v[3]+=len(x['gold']); v[4]+=sum(1 for g in x['gold'] if g['severity'].lower() in HC)
    print(title)
    for k,v in sorted(c.items(),key=lambda kv:-kv[1][0]): print(f"  {str(k):28s} n {v[0]:3d} FP {v[1]:3d} nonFP {v[2]:3d} goldens-bestmatch {v[3]:3d} HC {v[4]:2d}  candPrec {v[2]/v[0]:.0%}")
if __name__=='__main__':
    NG=173; HCT=66
    for k in ['opus','v110','haiku']:
        rows=build(k); print('=====',k,len(rows))
        print(collections.Counter(x['conf'] for x in rows), collections.Counter(x['sev'] for x in rows))
        table(rows,lambda x:x['sev'],'severity')
        table(rows,lambda x:x['conf'],'confidence')
        table(rows,lambda x:(x['sev'],x['conf']),'sev x conf')
        table(rows,lambda x:x['topic'],'topic')
        table(rows,lambda x:x['repo'],'repo')
        if k!='opus':
            table(rows,lambda x:x['tier'],'tier'); table(rows,lambda x:x['origin'],'origin'); table(rows,lambda x:x['vstat'],'verifier status')
        print('counterfactuals (lower bound recall)')
        S={'blocker':0,'fix':1,'consider':2,'info':3}
        defs={'all':lambda x:True,'sev>=consider (drop info)':lambda x:S[x['sev']]<=2,'sev>=fix':lambda x:S[x['sev']]<=1,'sev=blocker':lambda x:x['sev']=='blocker',
        'conf>=medium':lambda x:x['conf']!='low','conf=high':lambda x:x['conf']=='high',
        'sev>=fix & conf>=medium':lambda x:S[x['sev']]<=1 and x['conf']!='low','sev>=fix & conf=high':lambda x:S[x['sev']]<=1 and x['conf']=='high',
        'sev>=consider & conf=high':lambda x:S[x['sev']]<=2 and x['conf']=='high','topic=bug|security|perf':lambda x:x['topic'] in('bug','security','perf'),'topic not tests/cleanup/docs/question':lambda x:x['topic'] not in('tests','cleanup','docs','question','rules')}
        for n,fn in defs.items():
            tp,fp,hc,nk=metrics(rows,fn); p=tp/(tp+fp) if tp+fp else 0; r=tp/NG
            print(f"  {n:34s} kept {nk:3d}  TP {tp:3d} FP {fp:3d}  R {r:.1%} P {p:.1%} F1 {fb(p,r):.1%} HC {hc}/66")
