#!/usr/bin/env python3
"""Run one of Martian's pipeline steps with gentler concurrency, without editing Martian's files.

Martian's step2_5 and step3 send 20-30 judge calls at once, each with a 30 s client timeout. Through
the Claude Code CLI on one laptop that is heavy, and a queued call can time out. This wrapper changes
only throughput settings: the batch size (calls in flight) and the per-call timeout. Prompts, models,
dedup and scoring logic are Martian's, unchanged.

Run from Martian's `offline/` directory (it imports `code_review_benchmark`):
  python martian_step.py step3_judge_comments --batch 8 --call-timeout 120 -- --tool wachiman ...
"""
import argparse
import asyncio
import importlib
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["step2_5_dedup_candidates", "step3_judge_comments"])
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--call-timeout", type=int, default=120)
    argv = sys.argv[1:]
    own, rest = (argv[: argv.index("--")], argv[argv.index("--") + 1 :]) if "--" in argv else (argv, [])
    a = ap.parse_args(own)
    sys.path.insert(0, ".")
    m = importlib.import_module(f"code_review_benchmark.{a.step}")
    m.LLM_CALL_TIMEOUT = a.call_timeout
    # process_batch binds its batch size as a default argument at definition time.
    m.process_batch.__defaults__ = (a.batch,)
    sys.argv = [a.step, *rest]
    asyncio.run(m.main())


if __name__ == "__main__":
    main()
