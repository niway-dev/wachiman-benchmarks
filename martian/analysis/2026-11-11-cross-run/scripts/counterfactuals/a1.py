import sys,itertools,collections;sys.path.insert(0,'/tmp/martian-cf')
from lib import *
P=build2('opus'); H=build2('haiku')
def lo(u,p,i): return i['sev'] in('consider','info')
def rank(p): return sorted(p['items'],key=lambda i:(SEV[i['sev']],CONF[i['conf']],i['i']))
topn={}
def capN(N):
    ks={}
    for u,p in P.items(): ks[u]={id(i) for i in rank(p)[:N]}
    return lambda u,p,i:id(i) in ks[u]
def capK(K):
    ks={}
    for u,p in P.items():
        s=set(); c=0
        for i in rank(p):
            if SEV[i['sev']]<=1: s.add(id(i))
            elif c<K: s.add(id(i)); c+=1
        ks[u]=s
    return lambda u,p,i:id(i) in ks[u]
def echo(W):
    def f(u,p,i):
        for h in H[u]['items']:
            if h['path']==i['path'] and (W is None or abs(h['line']-i['line'])<=W): return True
        return False
    return f
rows=[]
def add(sec,name,fn): rows.append((sec,name,fn,score(P,fn)))
add(1,'baseline',lambda u,p,i:True)
add(1,'drop tests',lambda u,p,i:i['topic']!='tests')
add(1,'drop docs',lambda u,p,i:i['topic']!='docs')
add(1,'drop tests+docs',lambda u,p,i:i['topic'] not in('tests','docs'))
add(1,'drop tests+docs if consider/info',lambda u,p,i:not(i['topic'] in('tests','docs') and lo(u,p,i)))
add(1,'drop cleanup',lambda u,p,i:i['topic']!='cleanup')
add(1,'drop question',lambda u,p,i:i['topic']!='question')
cells=sorted({(i['topic'],i['sev']) for p in P.values() for i in p['items'] if i['sev'] in('consider','info')})
print(len(cells),cells)
best=None
for m in range(1<<len(cells)):
    d={cells[j] for j in range(len(cells)) if m>>j&1}
    s=score(P,lambda u,p,i:(i['topic'],i['sev']) not in d)
    if best is None or s['F1']>best[0]['F1']: best=(s,d)
bd=best[1]; print('bestF1 drops',sorted(bd))
add(1,'best-F1 cells (fitted)',lambda u,p,i:(i['topic'],i['sev']) not in bd)
for N in (3,4,5,6,8,10): add(2,'top %d/PR'%N,capN(N))
for K in (0,1,2,3,5): add(2,'fix+blocker, <=%d consider/PR'%K,capK(K))
for W,l in ((5,'+-5'),(10,'+-10'),(None,'same file')): add(3,'Haiku echo '+l,echo(W))
add(3,'hybrid: blocker/fix kept, consider/info need echo +-10',lambda u,p,i:(not lo(u,p,i)) or echo(10)(u,p,i))
# item 4 pairs
lib={
 'dropTD-lo':lambda u,p,i:not(i['topic'] in('tests','docs') and lo(u,p,i)),
 'dropTD':lambda u,p,i:i['topic'] not in('tests','docs'),
 'dropT':lambda u,p,i:i['topic']!='tests',
 'cons-echo10':lambda u,p,i:(not lo(u,p,i)) or echo(10)(u,p,i),
 'cons-echo5':lambda u,p,i:(not lo(u,p,i)) or echo(5)(u,p,i),
 'cons-echoFile':lambda u,p,i:(not lo(u,p,i)) or echo(None)(u,p,i),
 'echo10':echo(10),
 'dropCleanup':lambda u,p,i:i['topic']!='cleanup',
 'dropQ':lambda u,p,i:i['topic']!='question',
 'K1':capK(1),'K2':capK(2),'K3':capK(3),'N5':capN(5),'N6':capN(6),'N8':capN(8),
}
pairs=[]
for a,b in itertools.combinations(lib,2):
    fa,fb=lib[a],lib[b]; fn=(lambda fa,fb:lambda u,p,i:fa(u,p,i) and fb(u,p,i))(fa,fb)
    pairs.append((score(P,fn)['F1'],a+' + '+b,fn))
pairs.sort(key=lambda x:-x[0])
top=[];seen=set()
for f1,nm,fn in pairs:
    s=score(P,fn); key=(s['n'],s['tp'])
    if key in seen: continue
    seen.add(key); top.append((nm,fn)); 
    if len(top)==4: break
for nm,fn in top: add(4,nm,fn)
print('| rule | kept | TP | FP | R | P | F1 | F2 | H+C/66 |')
for sec,nm,fn,s in rows: print(sec,fmt(nm,s))
# item 5: top 3 rules by F1 among sections 1-4 excluding baseline
cand=[r for r in rows if r[1]!='baseline']
cand.sort(key=lambda r:-r[3]['F1']); t3=cand[:3]
def half(u): 
    r=[w for w in WL if w['golden_url']==u][0]['repo']; return 'A' if r in('cal.com','sentry','sentry-greptile') else 'B'
def hs(fn,which):
    sub={u:p for u,p in P.items() if half(u)==which}
    ng=sum(p['ntp']+p['nfn'] for p in sub.values())
    tp=fp=n=0
    for u,p in sub.items():
        for i in p['items']:
            if fn(u,p,i): n+=1; tp+=len(i['golds']); fp+=i['fp']
    r=tp/ng; pr=tp/(tp+fp) if tp+fp else 0; f1=2*pr*r/(pr+r) if pr+r else 0
    return n,tp,fp,100*r,100*pr,100*f1,ng
print('half A=Cal+Sentry, B=Grafana+Discourse+Keycloak')
for nm,fn in [('baseline',lambda u,p,i:True)]+[(r[1],r[2]) for r in t3]:
    a=hs(fn,'A');b=hs(fn,'B')
    print('| %s | A kept %d TP %d FP %d R %.1f P %.1f F1 %.1f (goldens %d) | B kept %d TP %d FP %d R %.1f P %.1f F1 %.1f (goldens %d) |'%((nm,)+a[:6]+(a[6],)+b[:6]+(b[6],)))
