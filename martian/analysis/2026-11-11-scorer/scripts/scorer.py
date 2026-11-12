#!/usr/bin/env python3
"""One scorer call per PR through `claude -p`, read-only tools, on the PR's head checkout.

usage: scorer.py <arm> <model> <repos|all|rest> [--limit N]
  arm    name of the output directory under outputs/ (e.g. haiku, opus)
  repos  comma list of worklist repos (cal.com,sentry,...), or `all`
Never reads golden text or judge results: only the findings of the stored Opus run (corrected Keycloak rows).
Env: needs ~/.wachiman/claude-personal signed in; ANTHROPIC_API_KEY must be unset.
"""
import json, os, subprocess, sys, threading, time, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPOS = os.path.expanduser('~/.cache/wachiman-martian/repos/')
PROFILE = os.path.expanduser('~/.wachiman/claude-personal')
SYSTEM = open(ROOT + '/prompts/scorer-system.md').read()
KINDS = ['bug', 'security', 'data-loss', 'concurrency', 'api-contract', 'test-gap', 'docs', 'style', 'speculative', 'pre-existing']
SCHEMA = {"type": "object", "required": ["findings"], "properties": {"findings": {"type": "array", "items": {
    "type": "object", "required": ["id", "score", "reason", "kind", "group"], "properties": {
        "id": {"type": "integer"}, "score": {"type": "integer", "minimum": 0, "maximum": 10},
        "reason": {"type": "string"}, "kind": {"type": "string", "enum": KINDS}, "group": {"type": "string"}}}}}}
DIFF_CAP = 200_000
GIT = threading.Lock()
STOP = threading.Event()


def user_prompt(row, items, diff):
    note = ''
    if len(diff) > DIFF_CAP:
        diff = diff[:DIFF_CAP]
        note = '\n[The diff was truncated here. Use Read, Grep and Glob for the rest of the changed files.]'
    fs = [dict(id=it['i'], path=it['path'], line=it['line'], severity=it['sev'], topic=it['topic'],
               title=it['title'], body=it['body']) for it in items]
    return ('Repository: %s\nThe checkout is the pull request head. Diff of the pull request (base..head):\n'
            '======\n%s%s\n======\n\nFindings to score (%d):\n======\n%s\n======\n'
            % (row['repo'], diff, note, len(fs), json.dumps(fs, indent=1, ensure_ascii=False)))


def parse(res, ids):
    so = res.get('structured_output')
    if so is None:
        t = (res.get('result') or '').strip()
        if t.startswith('```'):
            t = t.split('\n', 1)[1].rsplit('```', 1)[0]
        so = json.loads(t)
    fs = so['findings']
    got = [f['id'] for f in fs]
    assert sorted(got) == sorted(ids) and len(set(got)) == len(got), 'ids %s != %s' % (got, ids)
    for f in fs:
        assert isinstance(f['score'], int) and 0 <= f['score'] <= 10 and f['kind'] in KINDS and f['group'], f
    return fs


def run_one(arm, model, u, p):
    row = p['row']; key = data.pr_key(row)
    out = '%s/outputs/%s/%s.json' % (ROOT, arm, key)
    if os.path.exists(out) or STOP.is_set():
        return key, None
    items = p['items']
    if not items:
        json.dump(dict(key=key, findings=[], cost=0, seconds=0, empty=True), open(out, 'w')); return key, 0.0
    wt = '/tmp/scorer-wt/%s-%s' % (arm, key)
    with GIT:
        os.makedirs('/tmp/scorer-wt', exist_ok=True)
        subprocess.run(['git', '-C', REPOS + row['repo'], 'worktree', 'prune'], check=True)
        subprocess.run(['git', '-C', REPOS + row['repo'], 'worktree', 'add', '-q', '--detach', '-f', wt, row['head']], check=True)
    try:
        diff = subprocess.run(['git', '-C', wt, 'diff', '--no-color', '-U3', row['base'], row['head']],
                              capture_output=True, text=True, check=True).stdout
        prompt = user_prompt(row, items, diff)
        env = {k: v for k, v in os.environ.items() if k != 'ANTHROPIC_API_KEY'}
        env['CLAUDE_CONFIG_DIR'] = PROFILE
        cmd = ['claude', '-p', '--model', model, '--effort', 'high', '--system-prompt', SYSTEM,
               '--tools', 'Read,Grep,Glob', '--allowedTools', 'Read', 'Grep', 'Glob',
               '--setting-sources', '', '--strict-mcp-config', '--disable-slash-commands', '--no-session-persistence',
               '--max-budget-usd', '5', '--json-schema', json.dumps(SCHEMA), '--output-format', 'json']
        last = None
        for attempt in (1, 2):
            t0 = time.time()
            proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, env=env, cwd=wt, timeout=1500)
            secs = time.time() - t0
            try:
                res = json.loads(proc.stdout)
                open('%s/outputs/%s/%s.raw%d.json' % (ROOT, arm, key, attempt), 'w').write(proc.stdout)
                if res.get('is_error'):
                    raise RuntimeError('claude error: %s' % str(res.get('result'))[:300])
                fs = parse(res, [it['i'] for it in items])
                json.dump(dict(key=key, url=u, model=model, attempt=attempt, seconds=secs,
                               cost=res.get('total_cost_usd'), turns=res.get('num_turns'),
                               usage=res.get('usage'), findings=fs), open(out, 'w'), indent=1)
                return key, res.get('total_cost_usd')
            except Exception as e:
                last = '%s: %s | stderr %s' % (type(e).__name__, str(e)[:300], proc.stderr[-200:])
                print('FAIL', key, 'attempt', attempt, last, flush=True)
        STOP.set()
        raise RuntimeError('%s failed twice: %s' % (key, last))
    finally:
        with GIT:
            subprocess.run(['git', '-C', REPOS + row['repo'], 'worktree', 'remove', '--force', wt], capture_output=True)


def main():
    arm, model, sel = sys.argv[1:4]
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else 10**9
    os.makedirs('%s/outputs/%s' % (ROOT, arm), exist_ok=True)
    P = data.opus()
    keep = None if sel in ('all', 'rest') else sel.split(',')
    todo = [(u, p) for u, p in P.items() if keep is None or p['row']['repo'] in keep]
    todo = todo[:limit]
    tot = 0.0
    with cf.ThreadPoolExecutor(2) as ex:
        futs = [ex.submit(run_one, arm, model, u, p) for u, p in todo]
        for f in cf.as_completed(futs):
            key, cost = f.result()
            if cost is not None:
                tot += cost; print('done', key, 'cost %.2f' % cost, 'running total %.2f' % tot, flush=True)
    print('total', round(tot, 2))


main()
