exec(open('/tmp/martian-cf/a1.py').read().split("print('| rule")[0])
import os
rv=load('opus')[2]
U=os.path.expanduser('~/.cache/wachiman-martian/martian-upstream/offline/results/anthropic_claude-opus-4-5-20251101/candidates.json')
cc=json.load(open(U))
print(len(cc))
for u in ['https://github.com/keycloak/keycloak/pull/37634','https://github.com/keycloak/keycloak/pull/36880']:
    ps=collections.Counter(c['path'] for t in cc[u] for c in cc[u][t] if c.get('path'))
    print(u,'tools',len(cc[u]),'comments with path',sum(ps.values()),dict(list(ps.items())[:8]),'reviewed',rv[u]['coverage']['reviewed'])
print('--- all PRs: reviewed vs competitor paths')
out=[]
for u,p in P.items():
    rev=set(rv[u]['coverage']['reviewed'])|set(rv[u]['coverage']['skipped'] if isinstance(rv[u]['coverage']['skipped'],list) else [])
    lines=sum(b['lines'] for b in rv[u]['batches'])
    ps=[c['path'] for t,l in cc.get(u,{}).items() for c in l if c.get('path')]
    ov=sum(1 for x in ps if x in rev or any(x.endswith(r) or r.endswith(x) for r in rev))
    out.append((u.split('github.com/')[1],lines,len(rev),len(ps),ov))
print('PRs with competitor paths',sum(1 for o in out if o[3]),'zero-overlap among those',[o for o in out if o[3] and o[4]==0])
print('no comps paths',[o[0] for o in out if not o[3]][:10])
print('small <=20 lines',[o for o in out if o[1]<=20])
