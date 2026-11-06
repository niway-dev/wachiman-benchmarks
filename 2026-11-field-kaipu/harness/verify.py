"""Filter Haiku's findings for one PR, then ask each verifier model which ones to keep.

Usage: python3 -I verify.py <run-dir> <worktree> <base-sha> <model> [<model> ...]

Reads <run-dir>/haiku.json (a wachiman.review-result/1). Writes:
  candidates.json        the findings after the free filters, each with an id and the drop reason of the others
  verify-<label>.json    the verifier's verdict per candidate, plus its cost line from `claude -p`

The verifier gets every candidate in ONE call: the finding, the code around each cited line, and the
diff. It may read other files of the snapshot (Read, Glob, Grep; no Bash), with a turn cap.
"""

import json
import os
import re
import subprocess
import sys
import time

SNIPPET_LINES = 15
DIFF_CHARS = 60_000
MAX_TURNS = "15"
BUDGET_USD = "1.50"

SCHEMA = {
    "type": "object",
    "required": ["verdicts"],
    "properties": {
        "verdicts": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "keep", "severity", "reason"],
                "properties": {
                    "id": {"type": "string"},
                    "keep": {"type": "boolean"},
                    "severity": {"enum": ["blocker", "fix", "consider", "info"]},
                    "reason": {"type": "string"},
                },
            },
        }
    },
}

PROMPT = """You are the second reader of an automated code review of one pull request.
A cheaper model proposed the findings below. Decide, for each one, whether it should be posted.

Keep a finding only if all of these hold:
- the claim is true for the code at this commit;
- this pull request causes it, or makes an existing problem reachable or worse;
- a careful human reviewer would want it on the pull request.
Drop it if it is wrong, pre-existing and untouched by this change, a duplicate of another candidate,
or too minor to be worth a comment. When you keep one, give the severity it deserves.

The snapshot of the pull request head is the current directory. You may read other files to check a
claim, but do not search widely: most candidates can be decided from the code shown. Answer with
one verdict per candidate id, and a one or two sentence reason.

## The diff (base {base} to head)

```diff
{diff}
```

## Candidates
{candidates}
"""


def words(s):
    return set(re.findall(r"[a-z0-9_]+", s.lower()))


def similar(a, b):
    wa, wb = words(a), words(b)
    return bool(wa and wb) and len(wa & wb) / len(wa | wb) >= 0.5


def file_lines(worktree, path):
    try:
        with open(os.path.join(worktree, path), encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except OSError:
        return None


def filter_findings(findings, worktree):
    kept, dropped = [], []
    for f in findings:
        lines = file_lines(worktree, f["path"])
        if lines is None:
            dropped.append({**f, "dropReason": "cited file does not exist at the commit"})
            continue
        if f["line"] > len(lines):
            dropped.append({**f, "dropReason": f"cited line {f['line']} is past the end ({len(lines)} lines)"})
            continue
        dup = next(
            (k for k in kept if k["path"] == f["path"] and abs(k["line"] - f["line"]) <= 3 and similar(k["title"], f["title"])),
            None,
        )
        if dup:
            dropped.append({**f, "dropReason": f"duplicate of {dup['id']}"})
            continue
        kept.append({**f, "id": f"c{len(kept) + 1}"})
    return kept, dropped


def snippet(worktree, f):
    lines = file_lines(worktree, f["path"]) or []
    if f["line"] == 0:
        lo, hi = 1, min(len(lines), 2 * SNIPPET_LINES)
    else:
        lo, hi = max(1, f["line"] - SNIPPET_LINES), min(len(lines), f["line"] + SNIPPET_LINES)
    return "\n".join(f"{n:>5}  {lines[n - 1]}" for n in range(lo, hi + 1))


def render_candidates(worktree, cands):
    out = []
    for c in cands:
        out.append(
            f"\n### {c['id']} · {c['severity']} · {c['topic']} · `{c['path']}:{c['line']}`\n\n"
            f"**{c['title']}**\n\n{c['body']}\n\n```\n{snippet(worktree, c)}\n```\n"
        )
    return "".join(out)


def verify(model, prompt, worktree):
    args = [
        "claude", "-p",
        "--model", model,
        "--effort", "high",
        "--max-budget-usd", BUDGET_USD,
        "--max-turns", MAX_TURNS,
        "--strict-mcp-config",
        "--tools", "Read,Glob,Grep",
        "--allowedTools", "Read,Glob,Grep",
        "--disallowedTools", "Bash",
        "--no-session-persistence",
        "--output-format", "json",
        "--json-schema", json.dumps(SCHEMA),
    ]
    env = {**os.environ, "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"}
    env.pop("ANTHROPIC_API_KEY", None)
    t0 = time.time()
    p = subprocess.run(args, input=prompt, capture_output=True, text=True, cwd=worktree, env=env, timeout=1200)
    try:
        raw = json.loads(p.stdout)
    except json.JSONDecodeError:
        raw = {"is_error": True, "stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}
    usage = raw.get("usage") or {}
    return {
        "model": model,
        "isError": raw.get("is_error", True),
        "terminalReason": raw.get("subtype") or raw.get("terminal_reason"),
        "turns": raw.get("num_turns"),
        "durationMs": raw.get("duration_ms") or int((time.time() - t0) * 1000),
        "costUsd": raw.get("total_cost_usd"),
        "usage": {
            "input": usage.get("input_tokens", 0),
            "output": usage.get("output_tokens", 0),
            "cacheRead": usage.get("cache_read_input_tokens", 0),
            "cacheWrite": usage.get("cache_creation_input_tokens", 0),
        },
        "verdicts": (raw.get("structured_output") or {}).get("verdicts", []),
        **({"error": raw} if raw.get("is_error", True) else {}),
    }


def main():
    run_dir, worktree, base = sys.argv[1], sys.argv[2], sys.argv[3]
    models = sys.argv[4:]
    with open(os.path.join(run_dir, "haiku.json"), encoding="utf-8") as f:
        result = json.load(f)
    cands, dropped = filter_findings(result.get("findings", []), worktree)
    with open(os.path.join(run_dir, "candidates.json"), "w", encoding="utf-8") as f:
        json.dump({"candidates": cands, "dropped": dropped}, f, indent=2)
    print(f"filters: {len(cands)} candidate(s), {len(dropped)} dropped")
    if not cands:
        return
    diff = subprocess.run(["git", "diff", f"{base}...HEAD"], capture_output=True, text=True, cwd=worktree).stdout
    if len(diff) > DIFF_CHARS:
        diff = diff[:DIFF_CHARS] + f"\n… diff truncated at {DIFF_CHARS} characters; read the files for the rest\n"
    prompt = PROMPT.format(base=base[:12], diff=diff, candidates=render_candidates(worktree, cands))
    for model in models:
        label = model.removeprefix("claude-").split("-")[0]
        out = verify(model, prompt, worktree)
        with open(os.path.join(run_dir, f"verify-{label}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        kept = sum(1 for v in out["verdicts"] if v.get("keep"))
        print(f"verify {label}: kept {kept} of {len(cands)}, ${out['costUsd'] or 0:.2f}, {out['turns']} turns, error={out['isError']}")


if __name__ == "__main__":
    main()
