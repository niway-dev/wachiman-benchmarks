// Times Wachiman's code path over one commit, with a stub provider that answers instantly.
// Usage: bun bench.ts <engine-src-dir> <repoDir> <commit> [--concurrency-note]
const [srcDir, repoDir, commit] = process.argv.slice(2);
const { buildLocalInput, } = await import(`${srcDir}/connectors/local-git.ts`);
const { removeSnapshot } = await import(`${srcDir}/connectors/local-git.ts`).catch(() => ({ removeSnapshot: undefined }));
const eng = await import(`${srcDir}/engine.ts`);
const { loadConfig } = await import(`${srcDir}/config.ts`);

const t = () => performance.now();
const marks: { at: number; line: string }[] = [];
const T0 = t();
const log = (line: string) => marks.push({ at: t() - T0, line });

// 1. Input: git diff + snapshot of the head (local mode's equivalent of listFiles + checkout).
let a = t();
const built = buildLocalInput({ repoDir, commit, paths: [], log, warn: log });
const inputMs = t() - a;
const input = built.input;

const config = loadConfig({}, () => {});
const options = eng.reviewOptionsOf(config, 1e6, "default");

// 2. Pure planning steps, timed alone (reviewChange runs them again inside).
a = t();
const filtered = eng.filterFiles(input.files, [...eng.DEFAULT_EXCLUDE, ...options.exclude], input.scope);
const filterMs = t() - a;
a = t();
const split = eng.splitUnreviewable(filtered.kept, input.headDir);
const splitMs = t() - a;
a = t();
const batches = eng.planBatches(split.reviewable, { maxLines: options.batchLines, maxChars: options.batchChars }, input.pathRules);
const planMs = t() - a;

// 3. The whole core with a stub provider.
const calls: { start: number; end: number; promptChars: number; files: number }[] = [];
const provider = {
  name: "stub",
  preflight() {},
  modelLabel: () => "stub",
  leaksSecret: () => false,
  async run(req: { prompt: string }) {
    const start = t() - T0;
    const m = req.prompt.match(/This part holds exactly these files[^\n]*\n([\s\S]*?)\n\n/);
    const files = (m?.[1] ?? "").split("\n").map((l) => l.replace(/^- /, "").replace(/ \+\d+ −\d+.*$/, "")).filter(Boolean);
    calls.push({ start, end: t() - T0, promptChars: req.prompt.length, files: files.length });
    return {
      structuredOutput: { files_reviewed: files, files_skipped: [], findings: [], contracts: [], thread_replies: [], summary: "stub" },
      costUsd: 0, turns: 1, durationMs: 0, terminalReason: "success", isError: false,
    };
  },
};
a = t();
const result = await eng.reviewChange(input, options, { provider, log, warn: log });
const coreMs = t() - a;

const evid = marks.filter((m) => /evidence/i.test(m.line) && /ms/.test(m.line)).map((m) => Number(m.line.match(/(\d+)\s*ms/)?.[1] ?? 0));
const sum = (xs: number[]) => xs.reduce((x, y) => x + y, 0);
const out = {
  commit: commit.slice(0, 10),
  filesChanged: input.files.length,
  filesKept: filtered.kept.length,
  filesReviewable: split.reviewable.length,
  linesChanged: sum(split.reviewable.map((f: any) => f.additions + f.deletions)),
  diffChars: sum(split.reviewable.map((f: any) => (f.patch ?? "").length)),
  batches: batches.length,
  providerCalls: calls.length,
  promptCharsTotal: sum(calls.map((c) => c.promptChars)),
  ms: {
    input_gitDiffAndSnapshot: Math.round(inputMs),
    filter: +filterMs.toFixed(2),
    splitUnreviewable: +splitMs.toFixed(2),
    planBatches: +planMs.toFixed(2),
    reviewChange_total: Math.round(coreMs),
    evidence_sumOverBatches: sum(evid),
    evidence_maxBatch: Math.max(0, ...evid),
  },
  coverage: result.coverage ? { reviewed: result.coverage.reviewed?.length, expected: result.coverage.expected?.length } : undefined,
};
console.log(JSON.stringify(out));
if (process.env.BENCH_LOG) for (const m of marks) console.error(`${m.at.toFixed(1)}\t${m.line.slice(0, 160)}`);
try { (removeSnapshot ?? (() => {}))(built.snapshotDir); } catch {}
