"""Prepare audit inputs: audit_inputs.py <repo-substring> [opus|haiku|sonnet] [worktree-root]

For each PR of the matching repos with at least one Opus finding the judge matched to no golden, writes
audit/inputs/<key>.json and <key>.diff and checks out the PR head in a detached worktree. The json carries
no judge result: audit_ids only says which findings to check.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import data

want = sys.argv[1]
who = sys.argv[2] if len(sys.argv) > 2 else 'opus'
root = sys.argv[3] if len(sys.argv) > 3 else '/tmp/audit-wt'
repos = os.path.expanduser('~/.cache/wachiman-martian/repos/')
here = os.path.join(os.path.dirname(__file__), '..', 'audit', *([] if who == 'opus' else [who]), 'inputs')
os.makedirs(here, exist_ok=True); os.makedirs(root, exist_ok=True)
total = 0
for p in {'opus': data.opus, 'haiku': data.haiku_fixed, 'sonnet': data.sonnet}[who]().values():
    r = p['row']
    if want not in r['repo']: continue
    key = data.pr_key(r); wt = os.path.join(root, key)
    ids = [it['i'] for it in p['items'] if it['fp']]
    if not ids: print(key, 'no FP'); continue
    total += len(ids)
    if not os.path.isdir(wt):
        subprocess.run(['git', '-C', repos + r['repo'], 'worktree', 'add', '-q', '--detach', '-f', wt, r['head']], check=True)
    diff = subprocess.run(['git', '-C', wt, 'diff', '--no-color', '-U3', r['base'], r['head']], capture_output=True, text=True).stdout
    open(os.path.join(here, key + '.diff'), 'w').write(diff)
    json.dump(dict(pr=key, checkout=wt, audit_ids=ids, findings=[dict(id=it['i'], path=it['path'], line=it['line'],
              severity=it['sev'], topic=it['topic'], title=it['title'], body=it['body']) for it in p['items']]),
              open(os.path.join(here, key + '.json'), 'w'), indent=1)
    print(key, len(ids), 'of', len(p['items']), 'diff bytes', len(diff))
print('total', total)
