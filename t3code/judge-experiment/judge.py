#!/usr/bin/env python3
"""Hazard judge driver: one `claude -p` call per (review run, judge config).

Resumable: an output file that already exists is skipped. A failed call is
logged to <out>/failures.log, its raw output saved under <out>/failed/, and the
driver moves on. Calls run one at a time.

The call mirrors how the wachiman engine runs its reviewer
(src/providers/claude-code.ts on wachiman origin/main): `-p --model --effort
--max-budget-usd --restricted --strict-mcp-config --tools Read,Grep,Glob
--settings <engine settings> --add-dir <checkout> --allowedTools ...
--disallowedTools Bash,... --no-session-persistence --output-format json
--json-schema ...`, prompt on stdin, the process started in an empty scratch
directory (so the checkout's CLAUDE.md is not loaded), the isolated profile
forced through CLAUDE_CONFIG_DIR, and ANTHROPIC_API_KEY removed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORK = Path("/tmp/t3code-fork")
WORK = Path("/tmp/t3code-judge")
CLAUDE = Path.home() / ".local/bin/claude"
PROFILE_DIR = Path.home() / ".wachiman/claude-personal"
SETTINGS = HERE / "claude-code.settings.json"
TOOLS = "Read,Grep,Glob"
DISALLOWED = "Bash,Read(//proc/**),Grep(//proc/**),Glob(//proc/**)"
CALL_BUDGET_USD = 5.0
TOTAL_STOP_USD = float(os.environ.get("JUDGE_TOTAL_STOP_USD", "80"))
TIMEOUT_S = 40 * 60

CONFIGS = {
    "opus-high": ("claude-opus-5-5", "high"),
    "opus-medium": ("claude-opus-5-5", "medium"),
    "sonnet-high": ("claude-sonnet-5-5", "high"),
    "sonnet-medium": ("claude-sonnet-5-5", "medium"),
    "haiku-high": ("claude-haiku-5-5", "high"),
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["verdicts"],
    "properties": {
        "verdicts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["note_index", "verdict", "summary", "evidence"],
                "properties": {
                    "note_index": {"type": ["integer", "null"]},
                    "verdict": {"enum": ["breaks", "safe", "cannot_tell", "covered"]},
                    "summary": {"type": "string"},
                    "scenario": {"type": "string"},
                    "location": {"type": "string"},
                    "consequence": {"type": "string"},
                    "severity": {"enum": ["high", "medium", "low", "none"]},
                    "introduced_by_change": {"type": "boolean"},
                    "safe_line": {"type": "string"},
                    "missing": {"type": "string"},
                    "covered_by": {"type": ["integer", "null"]},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                },
            },
        }
    },
}


def git(*args: str, cwd: Path = FORK) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def ensure_checkout(sha: str) -> Path:
    path = WORK / f"wt-{sha[:12]}"
    if not (path / ".git").exists():
        WORK.mkdir(parents=True, exist_ok=True)
        git("worktree", "add", "--detach", str(path), sha)
    head = git("rev-parse", "HEAD", cwd=path).strip()
    if head != sha:
        raise RuntimeError(f"checkout {path} is at {head}, expected {sha}")
    return path


def ensure_diff(base: str, head: str) -> Path:
    d = WORK / "diffs"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{head[:12]}.diff"
    if not path.exists():
        path.write_text(git("diff", "--no-color", base, head))
    return path


def fmt_findings(findings: list[dict]) -> str:
    if not findings:
        return "(none)"
    out = []
    for i, f in enumerate(findings):
        out.append(
            f"[{i}] {f.get('path')}:{f.get('line')} ({f.get('severity')}) {f.get('title')}\n    {f.get('body', '').strip()}"
        )
    return "\n\n".join(out)


def fmt_contracts(contracts: list[dict]) -> str:
    if not contracts:
        return "(none)"
    return "\n\n".join(f"[{i}] {json.dumps(c, indent=2, ensure_ascii=False)}" for i, c in enumerate(contracts))


def build_prompt(template: str, run: dict, checkout: Path, diff_path: Path) -> str:
    change = run["change"]
    files = run.get("coverage", {}).get("expected", [])
    values = {
        "checkout": str(checkout),
        "head_sha": change["head"]["sha"],
        "base_sha": change["base"]["sha"],
        "title": change.get("title", ""),
        "changed_files": "\n".join(f"  - `{f}`" for f in files) or "  (see the diff)",
        "diff_path": str(diff_path),
        "findings": fmt_findings(run.get("findings", [])),
        "contracts": fmt_contracts(run.get("contracts", [])),
    }
    prompt = template
    for k, v in values.items():
        prompt = prompt.replace("{" + k + "}", v)
    return prompt


def total_spend() -> float:
    """Judge calls plus baseline reviews recorded under runs/, in API-price USD."""
    total = 0.0
    for p in (HERE / "runs").rglob("*.json"):
        if "failed" in p.parts:
            try:
                total += float(json.loads(p.read_text()).get("cost_usd") or 0)
            except Exception:
                pass
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if "cost_usd" in d:
            total += float(d["cost_usd"] or 0)
        elif "execution" in d:
            total += float(d["execution"].get("costUsdEstimate") or 0)
    return total


def run_one(input_path: Path, config: str, template: str, prompt_version: str, out_dir: Path) -> str:
    out = out_dir / f"{input_path.stem}__{config}.json"
    if out.exists():
        return "skip"
    spent = total_spend()
    if spent > TOTAL_STOP_USD:
        raise SystemExit(f"STOP: running total ${spent:.2f} exceeds ${TOTAL_STOP_USD}")
    model, effort = CONFIGS[config]
    run = json.loads(input_path.read_text())
    head, base = run["change"]["head"]["sha"], run["change"]["base"]["sha"]
    checkout = ensure_checkout(head)
    diff_path = ensure_diff(base, head)
    prompt = build_prompt(template, run, checkout, diff_path)
    args = [
        str(CLAUDE), "-p", "--model", model, "--effort", effort,
        "--max-budget-usd", str(CALL_BUDGET_USD),
        "--restricted", "--strict-mcp-config", "--tools", TOOLS,
        "--settings", str(SETTINGS),
        "--add-dir", str(checkout), "--add-dir", str(diff_path.parent),
        "--allowedTools", TOOLS, "--disallowedTools", DISALLOWED,
        "--no-session-persistence", "--output-format", "json",
        "--json-schema", json.dumps(SCHEMA),
    ]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CONFIG_DIR"] = str(PROFILE_DIR)
    scratch = tempfile.mkdtemp(prefix="hazard-judge-")
    started = time.time()
    try:
        proc = subprocess.run(args, input=prompt, cwd=scratch, env=env, capture_output=True, text=True, timeout=TIMEOUT_S)
        stdout, stderr, status = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        stdout, stderr, status = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout", -1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    wall_ms = int((time.time() - started) * 1000)
    record = {
        "format": "hazard-judge/1",
        "input": str(input_path.relative_to(HERE.parent.parent)),
        "config": config, "model": model, "effort": effort,
        "prompt_version": prompt_version,
        "prompt_sha256": hashlib.sha256(template.encode()).hexdigest(),
        "reviewed_commit": head, "base_commit": base,
        "wall_ms": wall_ms,
    }
    try:
        raw = json.loads(stdout)
    except Exception:
        raw = None
    if raw is not None:
        record.update({
            "cost_usd": raw.get("total_cost_usd"),
            "duration_ms": raw.get("duration_ms"),
            "num_turns": raw.get("num_turns"),
            "usage": raw.get("usage"),
            "is_error": raw.get("is_error"),
            "subtype": raw.get("subtype"),
            "model_usage": raw.get("modelUsage"),
        })
    so = raw.get("structured_output") if raw else None
    ok = raw is not None and not raw.get("is_error") and isinstance(so, dict) and "verdicts" in so
    if not ok:
        failed = out_dir / "failed"
        failed.mkdir(parents=True, exist_ok=True)
        record.update({"status": status, "stderr_tail": (stderr or "")[-3000:], "stdout_tail": (stdout or "")[-5000:]})
        (failed / f"{out.stem}.{int(started)}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
        with open(out_dir / "failures.log", "a") as log:
            log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {out.name} status={status} cost={record.get('cost_usd')} {(stderr or '')[-300:]!r}\n")
        return "fail"
    record["verdicts"] = so["verdicts"]
    record["result_text"] = raw.get("result")
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    cost = float(record.get("cost_usd") or 0)
    if cost > CALL_BUDGET_USD:
        raise SystemExit(f"STOP: call {out.name} cost ${cost:.2f} > ${CALL_BUDGET_USD}")
    return f"ok ${cost:.2f} {wall_ms/1000:.0f}s {len(so['verdicts'])} verdicts"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default=str(HERE / "judge-prompt.md"))
    ap.add_argument("--prompt-version", required=True)
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("inputs", nargs="+")
    a = ap.parse_args()
    template = Path(a.prompt).read_text()
    out_dir = Path(a.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    streak = 0
    for config in a.configs.split(","):
        for inp in a.inputs:
            p = Path(inp).resolve()
            try:
                status = run_one(p, config, template, a.prompt_version, out_dir)
            except SystemExit:
                raise
            except Exception as e:  # log and continue
                with open(out_dir / "failures.log", "a") as log:
                    log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {p.stem}__{config} exception {e!r}\n")
                status = f"fail {e!r}"
            print(f"{time.strftime('%H:%M:%S')} {p.stem} {config}: {status} | total ${total_spend():.2f}", flush=True)
            # A transient API block (seen: 403 from the API's edge) fails every call in seconds;
            # back off instead of burning through the queue, and give up after a long streak.
            streak = streak + 1 if status.startswith("fail") else 0
            if streak >= 8:
                raise SystemExit("STOP: 8 failures in a row")
            if streak:
                time.sleep(60 * streak)


if __name__ == "__main__":
    main()
