import json,re,sys
out=[]
for n in [l.split()[0] for l in open('cr_counts.tsv')]:
    for c in json.load(open(f'c/{n}.json')):
        if c['user']['login']!='coderabbitai[bot]' or c.get('in_reply_to_id') is not None: continue
        b=c['body']
        m=re.search(r'\*\*<picture>.*?alt=""></picture> ([^*]+)\*\*',b)
        sev=m.group(1).strip() if m else ''
        if not m:
            m2=re.search(r'_([^_]*(Potential issue|Nitpick|Minor|Major|Critical)[^_]*)_',b); sev=m2.group(1) if m2 else '?'
        h=re.search(r'\n\n\*\*([^\n]+?)\*\*\s*\n',b)
        hd=h.group(1) if h else ''
        fx=re.search(r'Addressed in commits? ([0-9a-f]{7,40})',b)
        out.append(dict(pr=int(n),id=c['id'],sev=sev,head=hd,path=c['path'],line=c['line'],oline=c['original_line'],cid=c['commit_id'],ocid=c['original_commit_id'],url=c['html_url'],fix=fx.group(1) if fx else '',pos=c['position']))
json.dump(out,open('findings.json','w'))
print(len(out))
