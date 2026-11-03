#!/usr/bin/env bun
/**
 * Re-review cost harness. Rebuilds one incremental re-review that Wachiman ran on a kaipu-record
 * pull request, and runs it through the engine's own `review()` (imported from --engine), so the
 * delta (`compare` + `rebaseDelta` + `ownChangeSince`), the batches, the open threads, the
 * call-site evidence and the prompt are the engine's, not a copy of them.
 *
 *   bun rereview.ts --engine <wachiman checkout> --clone <kaipu clone> --repo-dir <checkout at head>
 *     --pr <n> --head <sha> --at <ISO start time of the real re-review's job> --raw <field raw dir>
 *     --threads-now <graphql dump> --meta <pr meta json> --out <dir> [--base-tip <sha|main>] [--dry-run]
 *
 * `gh` is answered locally:
 *   - `pr view`, `pulls/<n>` (base.sha): from --meta and the clone.
 *   - `pulls/<n>/files`: `git diff <merge-base> <head>` in GitHub's patch format, with blob SHAs.
 *     The merge base is taken with the base branch as it was at --at (first parent of origin/main).
 *   - `compare/A...B`: `git diff merge-base(A,B) B`; status "ahead" when A is an ancestor of B.
 *   - `pulls/<n>/reviews` and `pulls/<n>/comments`: the field's raw JSON, cut at --at (strictly
 *     before), through the engine's own `--jq` program (run by `jq -r`).
 *   - GraphQL review threads: built from the raw comments cut at --at. A thread counts as open
 *     unless it is resolved today AND the real re-review did not reply to it (a resolved-today
 *     thread the real run replied to was open then).
 *   - contents API (repository instructions at the base): `git show` in the clone.
 *   - Any POST: refused (the run is a dry run for GitHub; the provider call is real).
 *
 * The provider is the engine's Claude Code adapter with production settings, run through a
 * generated wrapper that restores USER (keychain login), switches `--output-format json` to
 * `stream-json --verbose`, and keeps the whole stream as the trace. It prints only the final
 * `result` event, which has the fields `--output-format json` prints.
 */
import { spawnSync } from "node:child_process";
import { chmodSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const REPO = "niway-dev/kaipu-record";
const CLAUDE_BIN = process.env.CLAUDE_BIN ?? `${process.env.HOME}/.local/bin/claude`;

function parseArgs(argv: string[]) {
  const out: Record<string, string> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) continue;
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) out[a.slice(2)] = "1";
    else {
      out[a.slice(2)] = next;
      i++;
    }
  }
  return out;
}

const opts = parseArgs(process.argv.slice(2));
for (const k of ["engine", "clone", "repo-dir", "pr", "head", "at", "raw", "threads-now", "meta", "out"])
  if (!opts[k]) throw new Error(`--${k} is required`);
const clone = resolve(opts.clone);
const repoDir = resolve(opts["repo-dir"]);
const pr = Number(opts.pr);
const at = opts.at;
const out = resolve(opts.out);
mkdirSync(out, { recursive: true });

function git(args: string[], cwd = clone) {
  const r = spawnSync("git", ["-C", cwd, ...args], { encoding: "utf8", maxBuffer: 512 * 1024 * 1024 });
  if (r.status !== 0) throw new Error(`git ${args.join(" ")}: ${r.stderr}`);
  return r.stdout;
}
const head = git(["rev-parse", opts.head]).trim();
if (git(["rev-parse", "HEAD"], repoDir).trim() !== head) throw new Error(`--repo-dir is not at ${head}`);

/**
 * The base branch tip GitHub diffed the pull request against at --at: --base-tip when the pull
 * request was stacked on another branch then, else origin/main as it was at --at.
 */
const mainAt =
  opts["base-tip"] && opts["base-tip"] !== "main"
    ? git(["rev-parse", opts["base-tip"]]).trim()
    : git(["rev-list", "-1", "--first-parent", `--before=${at}`, "origin/main"]).trim();

interface PrFile {
  filename: string;
  additions: number;
  deletions: number;
  patch?: string;
  sha?: string;
}

/** `git diff from to` in the shape of GitHub's file lists, each patch from its first hunk header. */
function diffFiles(from: string, to: string): PrFile[] {
  const diff = git(["diff", "--no-color", "--no-ext-diff", "-M", "-U3", from, to]);
  const files: PrFile[] = [];
  for (const chunk of diff.split(/^diff --git /m).slice(1)) {
    const lines = chunk.split("\n");
    let filename: string | undefined;
    const renameTo = lines.find((l) => l.startsWith("rename to "));
    const plus = lines.find((l) => l.startsWith("+++ "));
    const minus = lines.find((l) => l.startsWith("--- "));
    if (renameTo) filename = renameTo.slice("rename to ".length);
    else if (plus && plus !== "+++ /dev/null") filename = plus.slice("+++ b/".length);
    else if (minus && minus !== "--- /dev/null") filename = minus.slice("--- a/".length);
    else filename = lines[0].match(/^a\/(.+) b\/(.+)$/)?.[2];
    if (!filename) continue;
    let sha: string | undefined;
    try {
      sha = git(["rev-parse", `${to}:${filename}`]).trim();
    } catch {
      sha = "0000000000000000000000000000000000000000";
    }
    const firstHunk = lines.findIndex((l) => l.startsWith("@@"));
    if (firstHunk < 0) {
      files.push({ filename, additions: 0, deletions: 0, sha });
      continue;
    }
    const body = lines.slice(firstHunk);
    while (body.length > 0 && body[body.length - 1] === "") body.pop();
    let additions = 0;
    let deletions = 0;
    for (const l of body) {
      if (l.startsWith("+")) additions++;
      else if (l.startsWith("-")) deletions++;
    }
    files.push({ filename, additions, deletions, patch: body.join("\n"), sha });
  }
  return files;
}

function jq(program: string, value: unknown) {
  const r = spawnSync("jq", ["-r", program], { input: JSON.stringify(value), encoding: "utf8", maxBuffer: 256 * 1024 * 1024 });
  if (r.status !== 0) throw new Error(`jq ${program}: ${r.stderr}`);
  return r.stdout;
}

const raw = (name: string) => JSON.parse(readFileSync(join(opts.raw, `pr-${pr}-${name}.json`), "utf8"));
const before = (t: string | null | undefined) => !!t && t < at;
const reviewsAt = raw("reviews").filter((r: { submitted_at: string }) => before(r.submitted_at));
const commentsAll = raw("comments") as {
  id: number;
  in_reply_to_id?: number;
  user: { login: string };
  author_association: string;
  body: string;
  path: string;
  line: number | null;
  original_line: number | null;
  created_at: string;
}[];
const commentsAt = commentsAll.filter((c) => before(c.created_at));
const meta = JSON.parse(readFileSync(opts.meta, "utf8"));
const now = JSON.parse(readFileSync(opts["threads-now"], "utf8")).data.repository.pullRequest.reviewThreads.nodes as {
  isResolved: boolean;
  comments: { nodes: { databaseId: number }[] };
}[];
const resolvedNow = new Set(now.filter((t) => t.isResolved).map((t) => t.comments.nodes[0]?.databaseId));
// The real re-review's replies: posted by the bot within 15 minutes after --at (the run's start).
const atMs = Date.parse(at);
const repliedAt = new Set(
  commentsAll
    .filter(
      (c) =>
        c.in_reply_to_id &&
        c.user.login === "github-actions[bot]" &&
        Date.parse(c.created_at) >= atMs &&
        Date.parse(c.created_at) <= atMs + 15 * 60_000,
    )
    .map((c) => c.in_reply_to_id),
);

function threadsAt() {
  const roots = commentsAt.filter((c) => !c.in_reply_to_id);
  return roots.map((root) => ({
    isResolved: resolvedNow.has(root.id) && !repliedAt.has(root.id),
    path: root.path,
    line: root.line ?? root.original_line,
    comments: {
      nodes: [root, ...commentsAt.filter((c) => c.in_reply_to_id === root.id)].map((c) => ({
        databaseId: c.id,
        author: { login: c.user.login === "github-actions[bot]" ? "github-actions" : c.user.login },
        authorAssociation: c.author_association,
        body: c.body,
        createdAt: c.created_at,
      })),
    },
  }));
}

const calls: string[] = [];
const fakeGh = (E: { GhError: new (m: string, s: number | null, g: string) => Error }) => (args: string[], input?: string) => {
  calls.push(args.filter((a) => !a.startsWith("query=")).join(" ").slice(0, 200));
  const jqAt = args.indexOf("--jq");
  const program = jqAt >= 0 ? args[jqAt + 1] : null;
  const send = (value: unknown) => (program ? jq(program, value) : JSON.stringify(value));
  if (args[0] === "pr" && args[1] === "view")
    return JSON.stringify({ headRefOid: head, title: meta.title, body: meta.body ?? "", author: { login: meta.author.login } });
  if (args.includes("-X") || input !== undefined) throw new Error(`refused write: ${args.join(" ")}`);
  if (args[0] !== "api") throw new Error(`unexpected gh: ${args.join(" ")}`);
  if (args[1] === "graphql") {
    return JSON.stringify({ data: { repository: { pullRequest: { reviewThreads: { nodes: threadsAt() } } } } });
  }
  const path = args.find((a) => a.startsWith("repos/"))!;
  let m: RegExpMatchArray | null;
  if ((m = path.match(/^repos\/[^/]+\/[^/]+\/pulls\/\d+$/))) return send({ base: { sha: mainAt } });
  if (path.endsWith(`/pulls/${pr}/files`)) {
    const mb = git(["merge-base", mainAt, head]).trim();
    return send(diffFiles(mb, head));
  }
  if (path.endsWith(`/pulls/${pr}/reviews`)) return send(reviewsAt);
  if (path.endsWith(`/pulls/${pr}/comments`)) return send(commentsAt);
  if ((m = path.match(/\/compare\/([0-9a-f]+)\.\.\.([0-9a-f]+)$/))) {
    const [a, b] = [git(["rev-parse", m[1]]).trim(), git(["rev-parse", m[2]]).trim()];
    const mb = git(["merge-base", a, b]).trim();
    const status = a === b ? "identical" : mb === a ? "ahead" : mb === b ? "behind" : "diverged";
    return send({ status, files: diffFiles(mb, b) });
  }
  if ((m = path.match(/\/contents\/(.+)\?ref=([0-9a-f]+)$/))) {
    const r = spawnSync("git", ["-C", clone, "show", `${m[2]}:${m[1]}`], { encoding: "buffer" });
    if (r.status !== 0) throw new E.GhError("Not Found", 404, "Not Found");
    return JSON.stringify({ type: "file", encoding: "base64", content: Buffer.from(r.stdout).toString("base64") });
  }
  throw new Error(`unexpected gh api: ${args.join(" ")}`);
};

/** The wrapper `claude`: restores USER, records each call's argv, prompt and full stream. */
function writeWrapper() {
  const path = join(out, "claude-traced.sh");
  writeFileSync(
    path,
    `#!/bin/bash
export USER="\${USER:-$(id -un)}"
if [ "$1" = "--version" ]; then exec "${CLAUDE_BIN}" --version; fi
dir="${out}"
n=1; while [ -e "$dir/call-$n.jsonl" ]; do n=$((n+1)); done
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "--output-format" ] && [ "$a" = "json" ]; then args+=("stream-json" "--verbose"); else args+=("$a"); fi
  prev="$a"
done
printf '%s\\n' "\${args[@]}" | grep -v '^{' > "$dir/call-$n.args"
tee "$dir/call-$n.prompt.txt" | "${CLAUDE_BIN}" "\${args[@]}" > "$dir/call-$n.jsonl"
status=$?
grep '"type":"result"' "$dir/call-$n.jsonl" | tail -n 1
exit $status
`,
  );
  chmodSync(path, 0o755);
  return path;
}

const dir = resolve(opts.engine);
const engine = await import(join(dir, "src/engine.ts"));
const config = await import(join(dir, "src/config.ts"));
const provider = await import(join(dir, "src/providers/claude-code.ts"));

const logLines: string[] = [];
const log = (line: string) => {
  logLines.push(line);
  console.error(line);
};
// Production settings of the v1.4.0 field runs (kaipu-record's caller workflow), no trigger so the
// automatic ceiling does not apply (it only changes the review body's footer).
const env: Record<string, string> = {
  AGENT_REVIEW_BUDGET_USD: "3",
  AGENT_REVIEW_BATCH_BUDGET_USD: "0.75",
  AGENT_REVIEW_ANSWER_BUDGET_USD: "1",
  AGENT_REVIEW_BATCH_LINES: "1000",
  AGENT_REVIEW_BATCH_CHARS: "140000",
  AGENT_REVIEW_MODEL: "claude-opus-5-5",
  AGENT_REVIEW_EFFORT: "high",
  AGENT_REVIEW_MAX_TURNS: "40",
  AGENT_REVIEW_CALL_TIMEOUT_S: "900",
  AGENT_REVIEW_PROVIDER: "claude-code",
  AGENT_REVIEW_MENTION: "/wachi",
  AGENT_REVIEW_OPERATOR: "csdev19",
  AGENT_REVIEW_DRY_RUN: "1",
};
for (const [k, v] of Object.entries(process.env)) if (k.startsWith("AGENT_REVIEW_") && v !== undefined) env[k] = v;
const cfg = config.loadConfig(env, log);

const real = new provider.ClaudeCodeProvider({ model: cfg.model, requireApiKey: false, effort: cfg.effort, binary: writeWrapper() });
const dry = opts["dry-run"] === "1";
const prompts: string[] = [];
const results: unknown[] = [];
const wrapped = {
  name: "claude-code",
  preflight: () => real.preflight(),
  modelLabel: () => real.modelLabel(),
  leaksSecret: (t: string[]) => real.leaksSecret(t),
  run: (req: { prompt: string; maxBudgetUsd: number; maxTurns?: number }) => {
    prompts.push(req.prompt);
    writeFileSync(join(out, `prompt-${prompts.length}.txt`), req.prompt);
    if (dry) return { costUsd: 0, turns: 0, durationMs: 0, terminalReason: "error", isError: true, raw: { dry: true } };
    const r = real.run(req);
    results.push({ ...r, raw: undefined });
    writeFileSync(join(out, `result-${results.length}.json`), JSON.stringify(r, null, 2));
    return r;
  },
};
wrapped.preflight();

const deps = { gh: fakeGh(engine), provider: wrapped, config: cfg, repoDir, log, warn: (l: string) => log(`WARN ${l}`) };
let error: string | null = null;
try {
  engine.review(deps, REPO, pr, []);
} catch (e) {
  error = String(e);
  log(`review() threw: ${error}`);
}
writeFileSync(join(out, "engine-log.txt"), logLines.join("\n") + "\n");
writeFileSync(
  join(out, "info.json"),
  JSON.stringify(
    {
      pr,
      head,
      at,
      mainAt,
      engine: git(["rev-parse", "HEAD"], dir).trim(),
      experiment: Object.fromEntries(Object.entries(process.env).filter(([k]) => k.startsWith("WACHI_X_"))),
      calls: prompts.length,
      promptChars: prompts.map((p) => p.length),
      openThreads: threadsAt().filter((t) => !t.isResolved && t.comments.nodes[0].author.login === "github-actions").length,
      results: (results as { costUsd: number; turns: number; terminalReason: string }[]).map((r) => ({
        costUsd: r.costUsd,
        turns: r.turns,
        terminalReason: r.terminalReason,
      })),
      error,
      ghCalls: calls,
    },
    null,
    2,
  ),
);
