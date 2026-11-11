import sys,itertools,re,json,hashlib;sys.path.insert(0,'/tmp/martian-cf')
from lib import *
H=build2('haiku'); V=build2('v110'); O=build2('opus')
_,_,rv110=load('v110')
# proposed H2 echo positions (415 entries incl. dropped)
PROP={u:[(e['path'],int(e['line'] or 0)) for e in (rv110[u]['verification']['entries'] if rv110[u] and rv110[u].get('verification') else [])] for u in V}
POST={u:[(i['path'],i['line']) for i in V[u]['items']] for u in V}
def pos(P): return {u:[(i['path'],i['line']) for i in p['items']] for u,p in P.items()}
HP=pos(H); OP=pos(O)
def echo(S,W):
    def f(u,p,i):
        return any(a==i['path'] and (W is None or abs(b-i['line'])<=W) for a,b in S[u])
    return f
def sc(P,fn):
    tp=fp=n=hc=0
    for u,p in P.items():
        for it in p['items']:
            if fn(u,p,it):
                n+=1;tp+=len(it['golds']);fp+=it['fp'];hc+=sum(g['sev'] in('high','critical') for g in it['golds'])
    r=tp/173;pr=tp/(tp+fp) if tp+fp else 0;f1=2*pr*r/(pr+r) if pr+r else 0
    return dict(n=n,tp=tp,fp=fp,R=100*r,P=100*pr,F1=100*f1,hc=hc)
def row(nm,P,fn,base):
    s=sc(P,fn);b=sc(P,lambda *a:True) if base is None else base
    gl=b['tp']-s['tp'];fr=b['fp']-s['fp']
    ratio='%.1f'%(fr/gl) if gl>0 else ('inf' if fr>0 else '-')
    return s,'| %s | %d | %d | %d | %.1f | %.1f | %.1f | %d | %d | %d | %s |'%(nm,s['n'],s['tp'],s['fp'],s['R'],s['P'],s['F1'],s['hc'],gl,fr,ratio)
HDR='| rule | kept | TP | FP | R | P | F1 | H+C/66 | goldens lost | FP removed | FP/golden |\n|---|---|---|---|---|---|---|---|---|---|---|'
lo=lambda i:i['sev'] in('consider','info')
bH=sc(H,lambda *a:True);print('H1 baseline',bH)
rows={}
def add(k,nm,P,fn,base):
    s,l=row(nm,P,fn,base);rows[k]=(s,l,fn,P);print(l)
print(HDR)
add('base','H1 baseline',H,lambda *a:True,bH)
for W,l in((5,'+-5'),(10,'+-10'),(None,'same file')):
    add('v1p'+l,'1 H1 echoed by H2(proposed) '+l,H,echo(PROP,W),bH)
for W,l in((10,'+-10'),):
    add('v1q'+l,'1 H1 echoed by H2(posted) '+l,H,echo(POST,W),bH)
bV=sc(V,lambda *a:True)
for W,l in((5,'+-5'),(10,'+-10'),(None,'same file')):
    add('m'+l,'1 mirror: H2 posted echoed by H1 %s (vs H2 base)'%l,V,echo(HP,W),bV)
add('hyb','2 hybrid: blocker/fix kept, cons/info need H2 +-10',H,lambda u,p,i:(not lo(i)) or echo(PROP,10)(u,p,i),bH)
# script rules
TESTP=re.compile(r'(^|/)(tests?|__tests__|__mocks__|e2e|playwright|fixtures?|spec)(/|$)|\.(test|spec|e2e)\.|_test\.|test_[^/]*$|/testing/|Test\.java$|Tests?\.java$|_spec\.rb$')
HEDGE=re.compile(r'\b(may|might|could|possibly|potentially|consider|it seems|appears?|unclear)\b',re.I)
bl=sorted(len(i['text']) for p in H.values() for i in p['items'])
q25,q50,q75=[bl[int(len(bl)*q)] for q in(.25,.5,.75)];print('body len quantiles',q25,q50,q75)
R={
'drop tests/docs topic @consider/info':lambda u,p,i:not(i['topic'] in('tests','docs') and lo(i)),
'drop conf low/medium':lambda u,p,i:i['conf']=='high',
'drop conf low':lambda u,p,i:i['conf']!='low',
'drop hedge words':lambda u,p,i:not HEDGE.search(i['text']),
'drop test-file paths':lambda u,p,i:not TESTP.search(i['path']),
'drop shortest quartile':lambda u,p,i:len(i['text'])>=q25,
'drop longest quartile':lambda u,p,i:len(i['text'])<=q75,
}
print('n test-path',sum(bool(TESTP.search(i['path'])) for p in H.values() for i in p['items']),'hedge',sum(bool(HEDGE.search(i['text'])) for p in H.values() for i in p['items']))
print('\nSCRIPT');print(HDR)
for k,fn in R.items(): add('s:'+k,'3 '+k,H,fn,bH)
names=list(R);best=None;allc=[]
for m in range(1,1<<len(names)):
    use=[names[j] for j in range(len(names)) if m>>j&1]
    fn=lambda u,p,i,use=use:all(R[k](u,p,i) for k in use)
    s=sc(H,fn);allc.append((s['F1'],use,s))
allc.sort(key=lambda x:-x[0]);best=allc[0]
print('top combos',[(round(a,1),b,c['n']) for a,b,c in allc[:3]])
bfn=lambda u,p,i,use=best[1]:all(R[k](u,p,i) for k in use)
add('sbest','3 best combo (fitted): '+' + '.join(best[1]),H,bfn,bH)
# best single
bs=max(R,key=lambda k:sc(H,R[k])['F1']);print('best single',bs)
# item4
votes={'1 echo+-5':echo(PROP,5),'1 echo+-10':echo(PROP,10),'1 echo same file':echo(PROP,None),'2 hybrid':rows['hyb'][2]}
print('\nVOTE+SCRIPT');print(HDR)
c4=[]
for vk,vf in votes.items():
    for sk in [bs]+['best combo']:
        sf=bfn if sk=='best combo' else R[sk]
        fn=lambda u,p,i,vf=vf,sf=sf:vf(u,p,i) and sf(u,p,i)
        c4.append((sc(H,fn)['F1'],vk+' + '+sk,fn))
c4.sort(key=lambda x:-x[0])
for _,nm,fn in c4: add('4:'+nm,'4 '+nm,H,fn,bH)
# item5
print('\nOPUS REF');print(HDR)
add('5a','5 H1 echoed by O +-10',H,echo(OP,10),bH)
bO=sc(O,lambda *a:True)
add('5b','5 O echoed by H1 +-10 (vs O base)',O,echo(HP,10),bO)
# item6
def half(u):
    r=[w for w in WL if w['golden_url']==u][0]['repo'];return 'A' if r in('cal.com','sentry','sentry-greptile') else 'B'
def hs(P,fn,w):
    tp=fp=n=hc=0;ng=0
    for u,p in P.items():
        if half(u)!=w:continue
        ng+=p['ntp']+p['nfn']
        for i in p['items']:
            if fn(u,p,i):n+=1;tp+=len(i['golds']);fp+=i['fp']
    r=tp/ng;pr=tp/(tp+fp);return '%d/%d/%d R%.1f P%.1f F1 %.1f'%(n,tp,fp,100*r,100*pr,200*pr*r/(pr+r)),ng
cands=[(k,v) for k,v in rows.items() if k not in('base',) and not k.startswith('m') and not k.startswith('5') and k!='v1q+-10']
cands.sort(key=lambda kv:-kv[1][0]['F1'])
top=[];seenk=set()
for k,v in cands:
    key=(v[0]['n'],v[0]['tp'])
    if key in seenk:continue
    seenk.add(key);top.append((k,v))
    if len(top)==3:break
print('\nSPLIT (kept/TP/FP)');print('| rule | A | B |\n|---|---|---|')
a,na=hs(H,lambda *x:True,'A');b,nb=hs(H,lambda *x:True,'B');print('| baseline | %s | %s |'%(a,b),na,nb)
for k,v in top:
    print('| %s | %s | %s |'%(v[1].split('|')[1].strip(),hs(H,v[2],'A')[0],hs(H,v[2],'B')[0]))
# item7
def bucket(P,Q,nm,ref):
    f=echo(ref,10);n=tp=hc=fp=lost=0;gl=0
    for u,p in P.items():
        for i in p['items']:
            if not f(u,p,i):
                n+=1;tp+=len(i['golds']);fp+=i['fp'];lost+=i['lost'];gl+=bool(i['golds']);hc+=sum(g['sev'] in('high','critical') for g in i['golds'])
    print(nm,'not-echoed n',n,'goldens',tp,'findings w/golden',gl,'H+C',hc,'FP',fp,'unjudged-neither',lost)
print()
bucket(H,H,'H1 not echoed by H2(proposed)+-10',PROP);bucket(O,O,'O not echoed by H1 +-10',HP);bucket(H,H,'H1 not echoed by O +-10',OP)
# item8
def gset(run):
    ev,_,_=load(run);S={}
    for u in ev:
        for g in ev[u]['wachiman']['true_positives']:
            S[(u,hashlib.md5(g['golden_comment'].encode()).hexdigest())]=g['severity'].lower()
    return S
g1=gset('haiku');g2=gset('v110');g3=gset('opus')
hcf=lambda S:sum(v in('high','critical') for v in S.values())
for nm,A,B in(('H1,H2',g1,g2),('H1,O',g1,g3)):
    U=set(A)|set(B);I=set(A)&set(B)
    print(nm,'union',len(U),'H+C',sum(((A.get(k) or B.get(k)) in('high','critical')) for k in U),'| intersection',len(I),'H+C',sum(A[k] in('high','critical') for k in I))
nH=sum(len(p['items']) for p in H.values());nV=sum(len(p['items']) for p in V.values())
U=set(g1)|set(g2)
# precision if both posted: simple concat (no dedup) and dedup by +-5 same file
def dedup(W):
    k=0;fpc=0;tpc=0
    for u in H:
        items=[('H',i) for i in H[u]['items']]
        extra=[]
        for i in V[u]['items']:
            if not any(a==i['path'] and abs(b-i['line'])<=W for a,b in HP[u]): extra.append(i)
        k+=len(H[u]['items'])+len(extra);fpc+=sum(i['fp'] for i in H[u]['items'])+sum(i['fp'] for i in extra)
    return k,fpc
k,fpc=dedup(-1);print('concat both (no dedup): findings',nH+nV,'FP',sum(i['fp'] for p in H.values() for i in p['items'])+sum(i['fp'] for p in V.values() for i in p['items']))
for W in(5,10):
    k,fpc=dedup(W);print('H1 + H2 findings not echoed by H1 +-%d: n %d FP %d'%(W,k,fpc))
print('P with union',len(U),'/',(len(U)+ (sum(i['fp'] for p in H.values() for i in p['items'])+sum(i['fp'] for p in V.values() for i in p['items']))))
print('inter echo10 both directions: H1 echoed by H2 & ... see rows')
# metrics cost
for r in RUNS.values():
    m=json.load(open(R+'runs/'+r+'/metrics.json'))['product_cost'];print(r,m['total_usd'],m.get('verifier',{}).get('total_usd'))
