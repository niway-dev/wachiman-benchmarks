exec(open('/tmp/martian-cf/a1.py').read().split("print('| rule")[0])
exec("def half(u):\n r=[w for w in WL if w['golden_url']==u][0]['repo']; return 'A' if r in('cal.com','sentry','sentry-greptile') else 'B'")
src=open('/tmp/martian-cf/a1.py').read()
exec(src[src.index('def hs'):src.index("print('half A")])
for nm,fn in [('echo10',echo(10)),('top6',capN(6)),('fitted cells',lambda u,p,i:(i['topic'],i['sev']) not in bd)]:
    a=hs(fn,'A');b=hs(fn,'B')
    print('| %s | A kept %d TP %d FP %d R %.1f P %.1f F1 %.1f | B kept %d TP %d FP %d R %.1f P %.1f F1 %.1f |'%((nm,)+a[:6]+b[:6]))
# 6
import collections
byf=collections.defaultdict(list)
for u,p in P.items():
    for i in p['items']: byf[u].append(i)
dup=0;fpn=0;dupfp_with_tp=0
for u,p in P.items():
    for i in p['items']:
        if not i['fp']: continue
        fpn+=1
        if any(j is not i and j['path']==i['path'] and abs(j['line']-i['line'])<=10 for j in p['items']): 
            dup+=1
            if any(j is not i and j['golds'] and j['path']==i['path'] and abs(j['line']-i['line'])<=10 for j in p['items']): dupfp_with_tp+=1
print('FP',fpn,'near another finding',dup,'near a TP finding',dupfp_with_tp)
print('lost',sum(i['lost'] for p in P.values() for i in p['items']),'multi',sum(len(i['golds'])>=2 for p in P.values() for i in p['items']))
# 7
fps=[sum(i['fp'] for i in p['items']) for p in P.values()]
def b(x): return '0' if x==0 else '1' if x==1 else '2' if x==2 else '3' if x==3 else '4-5' if x<=5 else '6-9' if x<=9 else '10+'
c=collections.Counter(b(x) for x in fps); print([(k,c[k]) for k in ['0','1','2','3','4-5','6-9','10+']])
s=sorted(fps,reverse=True); print('top10 share',sum(s[:10]),sum(s),sum(s[:10])/sum(s), s[:10])
rv=load('opus')[2]
r=rv[list(rv)[0]]; print(r['batches'][0],r['coverage'].keys())
