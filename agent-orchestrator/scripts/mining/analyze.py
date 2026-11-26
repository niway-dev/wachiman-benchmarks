import json,subprocess,re,collections
C=__import__('os').environ['AO_CLONE']
def g(*a,ok=False):
    r=subprocess.run(['git','-C',C]+list(a),capture_output=True,text=True)
    if ok: return r.returncode==0
    return r.stdout
prs={p['number']:p for p in json.load(open('prs.json'))}
F=json.load(open('findings.json'))
pool=[int(x) for x in open('pool.txt').read().split()]
def anc(a,b): return g('merge-base','--is-ancestor',a,b,ok=True)
def added(base,head,path):
    d=g('diff','-U0',base,head,'--',path)
    s=set()
    for m in re.finditer(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@',d,re.M):
        st=int(m.group(1)); ln=int(m.group(2)) if m.group(2) is not None else 1
        s.update(range(st,st+ln))
    return s
def mapline(head,x,path,L):
    # map line L in x to head; returns None if changed
    d=g('diff','-U0',head,x,'--',path)
    off=0
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',d,re.M):
        os_,oc,ns,nc=int(m.group(1)),m.group(2),int(m.group(3)),m.group(4)
        oc=1 if oc is None else int(oc); nc=1 if nc is None else int(nc)
        if L>=ns and L<ns+max(nc,0) and nc>0: return None
        if ns+nc<=L if nc>0 else ns< L: off+= oc-nc
    return L+off
res=[]
for n in pool:
    fs=[f for f in F if f['pr']==n]
    shas=set()
    for f in fs: shas.add(f['ocid'])
    for r in json.load(open(f'r/{n}.json')):
        if r['user']['login']=='coderabbitai[bot]': shas.add(r['commit_id'])
    shas=[s for s in shas if s]
    reach=[s for s in shas if g('cat-file','-e',s+'^{commit}',ok=True)]
    unreach=[s for s in shas if s not in reach]
    head=None
    for s in reach:
        if all(anc(s,t) for t in reach): head=s
    rec=dict(pr=n,unreach=unreach,head=head,nshas=len(shas))
    if not head or unreach and not head:
        res.append(rec); continue
    mc=(prs[n].get('mergeCommit') or {}).get('oid')
    basecand=None
    if mc and g('cat-file','-e',mc+'^{commit}',ok=True):
        basecand=g('rev-parse',mc+'^1').strip()
    if not basecand: basecand='refs/ao-upstream/main'
    base=g('merge-base',basecand,head).strip()
    rec['base']=base; rec['baseok']=anc(base,head)
    rec['stat']=g('diff','--shortstat',base,head).strip()
    prhead='refs/ao-pr/%d'%n
    rec['f']=[]
    for f in fs:
        x=f['ocid']; L=f['oline'] or f['line']
        if L is None: adm=None; hl=None; why='no line (file-level)'
        else:
            hl=L if x==head else mapline(head,x,f['path'],L)
            if hl is None: adm=False; why='line changed between head and reviewed commit'
            else:
                ad=added(base,head,f['path'])
                adm=hl in ad; why='added at head' if adm else 'line not in added lines (omission or context)'
        fx=f['fix']; fxfull=g('rev-parse','--verify','-q',fx+'^{commit}').strip() if fx else ''
        fxok= bool(fxfull) and anc(fxfull,prhead)
        rec['f'].append(dict(f,hl=hl,adm=adm,why=why,fixfull=fxfull,fxok=fxok))
    res.append(rec)
json.dump(res,open('analysis.json','w'),indent=1)
for r in res:
    if 'f' not in r: print(r['pr'],'NOHEAD',r['nshas'],r['unreach'][:2]); continue
    a=[f for f in r['f'] if f['fix'] and f['adm'] and f['fxok'] and not f['head'].startswith('Nit')]
    print(r['pr'],r['baseok'],r['stat'][:60],'unreach=%d'%len(r['unreach']),'adm_acc=%d'%len(a))
