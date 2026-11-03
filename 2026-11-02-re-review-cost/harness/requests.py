# Per API request of a traced call: cache write, cache read, and the chars of the tool results that
# came back from the previous request (what that write mostly holds).
import json,sys
def load(path):
    ev=[json.loads(l) for l in open(path) if l.strip()]
    reqs=[];seen={};results={}
    for e in ev:
        if e.get('type')=='assistant':
            m=e['message']; mid=m['id']
            if mid not in seen:
                seen[mid]=len(reqs); reqs.append({'id':mid,'usage':m.get('usage',{}),'tools':[]})
            for b in m.get('content',[]):
                if b.get('type')=='tool_use': reqs[seen[mid]]['tools'].append(b)
        if e.get('type')=='user':
            for b in (e.get('message',{}).get('content') or []):
                if isinstance(b,dict) and b.get('type')=='tool_result':
                    c=b.get('content'); t=c if isinstance(c,str) else ''.join(x.get('text','') for x in (c or []) if isinstance(x,dict))
                    results[b['tool_use_id']]=len(t)
    return ev,reqs,results
for p in sys.argv[1:]:
    ev,reqs,res=load(p); print('==',p)
    prev=0
    for i,r in enumerate(reqs):
        u=r['usage']; print(f"req {i+1}: write={u.get('cache_creation_input_tokens')} read={u.get('cache_read_input_tokens')} prevResultChars={prev} tools={len(r['tools'])}")
        prev=sum(res.get(t['id'],0) for t in r['tools'])
