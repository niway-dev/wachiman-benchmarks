#!/usr/bin/env python3
"""Check every worklist.tsv row against the pull request it claims to review.

For each row, the diff base..head in the cached clone must match the original pull request
(golden_url) on GitHub: same title as the fork's PR #1, same file list,
same additions and deletions. Needs read-only `gh api` on public repositories.

usage: check_worklist.py [worklist.tsv] [cache-dir]
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
wl = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "worklist.tsv"
cache = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / ".cache/wachiman-martian"


def run(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, check=True).stdout


def gh(path, jq=None):
    return run("gh", "api", "--paginate", path, *(["--jq", jq] if jq else []))


bad = 0
rows = [l.rstrip("\n").split("\t") for l in wl.read_text().splitlines()[1:]]
for repo, url, suffix, base, head, fork in rows:
    owner_repo = url.split("github.com/")[1].split("/pull/")[0]
    num = url.rsplit("/", 1)[1]
    clone = cache / "repos" / repo
    problems = []
    # 1. local diff of the stored range
    names = set(run("git", "diff", "--name-only", base, head, cwd=clone).split())
    add = dele = 0
    for line in run("git", "diff", "--numstat", base, head, cwd=clone).splitlines():
        a, d, _ = line.split("\t", 2)
        if a != "-":
            add += int(a); dele += int(d)
    # 2. the original pull request
    pr = json.loads(gh(f"repos/{owner_repo}/pulls/{num}"))
    files = set(gh(f"repos/{owner_repo}/pulls/{num}/files?per_page=100", ".[].filename").split())
    if names != files:
        problems.append(f"files differ: stored range {len(names)}, original PR {len(files)}")
    if (add, dele) != (pr["additions"], pr["deletions"]):
        problems.append(f"lines differ: stored +{add}/-{dele}, original PR +{pr['additions']}/-{pr['deletions']}")
    # 3. the fork's PR #1 carries the benchmark's title
    ftitle = json.loads(gh(f"repos/code-review-benchmark/{fork}/pulls/1"))["title"]
    if ftitle.strip() != pr["title"].strip():
        problems.append(f"fork PR #1 is '{ftitle}', original is '{pr['title']}'")
    print(("BAD " if problems else "ok  ") + f"{repo} {num} {len(names)} files +{add}/-{dele}" + ("".join("\n     " + p for p in problems)))
    bad += bool(problems)
print(f"{len(rows)} rows, {bad} bad")
sys.exit(1 if bad else 0)
