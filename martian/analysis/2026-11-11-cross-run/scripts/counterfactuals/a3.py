exec(open('/tmp/martian-cf/a1.py').read().split("print('| rule")[0])
import math
rv=load('opus')[2]
xs=[];ys=[];rows=[]
for u,p in P.items():
    r=rv[u]; lines=sum(b['lines'] for b in r['batches']); files=sum(b['files'] for b in r['batches'])
    n=len(p['items']); rows.append((u,lines,files,n,sum(i['fp'] for i in p['items']),len(r['coverage']['reviewed']),len(r['coverage']['expected'])))
def corr(a,b):
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
L=[r[1] for r in rows];N=[r[3] for r in rows];F=[r[4] for r in rows]
print('pearson findings~lines',corr(L,N),'FP~lines',corr(L,F))
def rk(a): s=sorted(range(len(a)),key=lambda i:a[i]); r=[0]*len(a)
for_=None
def rank(a):
    s=sorted(range(len(a)),key=lambda i:a[i]); r=[0]*len(a)
    for k,i in enumerate(s): r[i]=k
    return r
print('spearman',corr(rank(L),rank(N)))
for r in sorted(rows,key=lambda r:r[1])[:8]: print(r)
