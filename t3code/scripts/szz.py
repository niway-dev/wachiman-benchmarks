#!/usr/bin/env python3
"""SZZ for one t3code fix: which earlier PRs wrote the lines a fix removed or changed.

Usage: python3 -I szz.py <fix-commit> [paths...]

Blames, on the fix's first parent, every line the fix removed or changed (tests, docs, lockfiles
and snapshots skipped) and maps each blamed commit to the PR that merged it, using the `(#N)`
suffix of squash-merge subjects, else `gh api commits/<sha>/pulls`. Prints PR -> line count,
most lines first, plus per-file detail. Pure additions have no blamable lines; the output says so.

Repo: /tmp/t3code-mine/repo (blobless clone; blame fetches blobs on demand, so it can be slow).
"""
import collections, json, re, subprocess, sys

R = "/tmp/t3code-mine/repo"
SKIP = re.compile(r"(\.test\.|\.spec\.|/e2e/|__tests__|\.md$|\.mdx$|CHANGELOG|bun\.lock|pnpm-lock|\.snap$|fixture|/docs/)")


def g(*a):
    return subprocess.run(["git", "-C", R, *a], capture_output=True, text=True).stdout


def removed_ranges(fix, paths):
    d = g("diff", "-U0", "--no-renames", f"{fix}^1", fix, "--", *paths)
    out, f = collections.defaultdict(list), None
    for l in d.splitlines():
        if l.startswith("--- "):
            f = l[6:] if l.startswith("--- a/") else None
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@", l)
        if m and f:
            s, n = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
            if n:
                out[f].append((s, n))
    return out


_pr = {}


def pr_of(sha):
    if sha in _pr:
        return _pr[sha]
    subj = g("log", "-1", "--format=%s", sha).strip()
    m = re.search(r"\(#(\d+)\)\s*$", subj)
    if m:
        _pr[sha] = f"#{m.group(1)}"
    else:
        o = subprocess.run(["gh", "api", f"repos/pingdotgg/t3code/commits/{sha}/pulls", "--jq", ".[0].number"],
                           capture_output=True, text=True).stdout.strip()
        _pr[sha] = f"#{o}" if o else f"?{sha[:8]}"
    return _pr[sha]


def main(fix, paths):
    total, per_file = collections.Counter(), collections.defaultdict(collections.Counter)
    ranges = removed_ranges(fix, paths)
    for f, rs in ranges.items():
        if SKIP.search(f):
            continue
        for s, n in rs:
            o = g("blame", "-w", "--line-porcelain", f"-L{s},{s + n - 1}", f"{fix}^1", "--", f)
            for sha in (l.split()[0] for l in o.splitlines() if re.match(r"^[0-9a-f]{40} ", l)):
                p = pr_of(sha)
                total[p] += 1
                per_file[f][p] += 1
    if not ranges:
        changed = g("diff", "--name-only", f"{fix}^1", fix).split()
        print(f"no removed/changed lines in paths {paths or 'all'}. Files this commit changes: {changed[:15]}. "
              "If your paths are not in that list, re-run with repo-relative paths from it; otherwise it is a pure addition.")
        return
    if not total:
        print("no removed/changed source lines: pure addition, SZZ cannot point at an introducing PR")
        return
    print(json.dumps({"fix": fix, "introducing": total.most_common(),
                      "files": {f: c.most_common(5) for f, c in per_file.items()}}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
