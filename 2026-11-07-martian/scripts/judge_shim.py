#!/usr/bin/env python3
"""OpenAI-compatible /v1/chat/completions endpoint backed by `claude -p`.

Martian's judge (step2_5 and step3) talks to an OpenAI-compatible gateway. This shim lets the
unmodified pipeline reach the same Anthropic model through the Claude Code CLI on a subscription:
point MARTIAN_BASE_URL at it and set MARTIAN_MODEL=anthropic/<model-id>.

What is forwarded: the system message (as --system-prompt) and the user message (on stdin), with
no tools, no settings, no session persistence. What is lost: `temperature` (the CLI has no such
option) and `response_format` (unused by the default pipeline). Every call is appended to a JSONL
log with its duration, model usage and reported cost, so the run can be audited.

Standard library only. Usage:
  CLAUDE_CONFIG_DIR=~/.wachiman/claude-personal python3 -I judge_shim.py --port 8787 --log calls.jsonl
"""
import argparse
import json
import os
import subprocess
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOCK = threading.Lock()


def run_claude(model: str, system: str, user: str, timeout: int) -> dict:
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    cmd = [
        "claude", "-p",
        "--model", model,
        "--system-prompt", system,
        "--tools", "",
        "--setting-sources", "",
        "--no-session-persistence",
        "--output-format", "json",
    ]
    start = time.time()
    proc = subprocess.run(cmd, input=user, capture_output=True, text=True, env=env, timeout=timeout)
    took = time.time() - start
    if proc.returncode != 0:
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr[-400:]}")
    out = json.loads(proc.stdout)
    if out.get("is_error"):
        raise RuntimeError(f"claude reported an error: {str(out.get('result'))[:400]}")
    return {"text": out.get("result", ""), "took": took, "usage": out.get("modelUsage"),
            "cost": out.get("total_cost_usd")}


class Handler(BaseHTTPRequestHandler):
    server_version = "judge-shim/1"

    def log_message(self, *args):  # quiet
        pass

    def do_POST(self):
        if not self.path.rstrip("/").endswith("/chat/completions"):
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        model = body["model"].split("/", 1)[-1]
        system = "\n\n".join(m["content"] for m in body["messages"] if m["role"] == "system")
        user = "\n\n".join(m["content"] for m in body["messages"] if m["role"] == "user")
        rec = {"id": str(uuid.uuid4()), "model": model, "at": time.time(),
               "temperature_requested": body.get("temperature"),
               "response_format_requested": "response_format" in body}
        try:
            with self.server.slots:
                res = run_claude(model, system, user, self.server.call_timeout)
        except Exception as exc:  # report as a 500 so the pipeline's own retry logic applies
            rec["error"] = str(exc)
            self._log(rec)
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": str(exc)}}).encode())
            return
        rec.update({"took_s": round(res["took"], 2), "usage": res["usage"], "cost_usd": res["cost"]})
        self._log(rec)
        payload = {
            "id": rec["id"], "object": "chat.completion", "created": int(time.time()), "model": body["model"],
            "choices": [{"index": 0, "message": {"role": "assistant", "content": res["text"]},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
        data = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _log(self, rec):
        with LOCK, open(self.server.log_path, "a") as f:
            f.write(json.dumps(rec) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--log", required=True)
    ap.add_argument("--concurrency", type=int, default=20)
    ap.add_argument("--call-timeout", type=int, default=120)
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    srv.slots = threading.BoundedSemaphore(a.concurrency)
    srv.log_path = a.log
    srv.call_timeout = a.call_timeout
    print(f"judge shim on 127.0.0.1:{a.port}, concurrency {a.concurrency}, log {a.log}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
