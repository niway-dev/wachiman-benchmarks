import json,glob,csv,collections
R='/Users/cristiansotomayor-m5-pro/Documents/Workspace/Personal/wachiman-benchmarks/.claude/worktrees/martian-v1-10/martian/'
WL=list(csv.DictReader(open(R+'worklist.tsv'),delimiter='\t'))
RUNS={'opus':'2026-11-07-v1.9.0-opus-5-5','haiku':'2026-11-07-v1.9.0-haiku-5-5-high','v110':'2026-11-10-v1.10.0-haiku-5-5-high-opus-verifier'}
SEV={'blocker':0,'fix':1,'consider':2,'info':3}; CONF={'high':0,'medium':1,'low':2}
def load(run):
    d=R+'runs/'+RUNS[run]+'/data/'
    ev=json.load(open(d+'evaluations/wachiman.json')); ca=json.load(open(d+'candidates-wachiman.json'))
    out={}
    for r in WL:
        b=d+'reviews/'+r['repo']+'/'
        fs=glob.glob(b+r['branch_suffix']+'.json')+glob.glob(b+r['branch_suffix']+'-flat.json')
        if not fs: out[r['golden_url']]=None; continue
        out[r['golden_url']]=json.load(open(fs[0]))
    return ev,ca,out
def build(run):
    ev,ca,rv=load(run)
    P={}
    for u in ev:
        e=ev[u]['wachiman']; cands=ca[u]['wachiman']; fs=rv[u]['findings']
        items=[]
        for i,f in enumerate(fs):
            t=f['title']+'\n\n'+f['body']
            items.append(dict(i=i,path=f['path'],line=int(f['line'] or 0),sev=f['severity'],conf=f['confidence'],topic=f['topic'],text=t,golds=[]))
        # map matched candidate text -> item
        for g in e['true_positives']:
            mc=g['matched_candidate']
            m=[it for it in items if it['text']==mc] or [it for it in items if it['text'].startswith(mc) or mc.startswith(it['text'][:len(mc)])]
            if len(m)!=1: print('map issue',u,len(m),run); 
            if m: m[0]['golds'].append(dict(sev=g['severity'].lower(),cat=g['category']))
        P[u]=dict(items=items,skipped=e.get('skipped'),nfn=len(e['false_negatives']),ntp=len(e['true_positives']),
          fn=[dict(sev=g['severity'].lower()) for g in e['false_negatives']],
          tpg=[g['severity'].lower() for g in e['true_positives']])
    return P
def build2(run):
    ev,ca,rv=load(run); P=build(run)
    for u in P:
        fps=[x['candidate'] for x in ev[u]['wachiman']['false_positives']]
        for it in P[u]['items']:
            it['fp']= (not it['golds']) and any(it['text']==x or it['text'].startswith(x) or x.startswith(it['text'][:len(x)]) for x in fps)
            it['lost']=(not it['golds']) and not it['fp']
    return P
def score(P,keep,hcset=None):
    tp=fp=n=0;hc=0
    for u,p in P.items():
        k=[it for it in p['items'] if keep(u,p,it)]
        n+=len(k)
        for it in k:
            tp+=len(it['golds']); fp+=it['fp']
            hc+=sum(1 for g in it['golds'] if g['sev'] in('high','critical'))
    r=tp/173; pr=tp/(tp+fp) if tp+fp else 0
    f1=2*pr*r/(pr+r) if pr+r else 0; f2=5*pr*r/(4*pr+r) if pr+r else 0
    return dict(n=n,tp=tp,fp=fp,R=100*r,P=100*pr,F1=100*f1,F2=100*f2,hc=hc)
def fmt(name,s): return '| %s | %d | %d | %d | %.1f | %.1f | %.1f | %.1f | %d |'%(name,s['n'],s['tp'],s['fp'],s['R'],s['P'],s['F1'],s['F2'],s['hc'])
