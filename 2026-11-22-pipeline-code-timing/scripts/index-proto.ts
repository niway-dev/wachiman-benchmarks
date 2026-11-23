// Prototype: one pass over the head that finds every symbol all batches want, vs one git grep per symbol per batch.
// Usage: bun index-proto.ts <engine-src> <repoDir(clone)> <commit> <checkoutDir> [--skip-vendored]
const [src, repoDir, commit, headDir] = process.argv.slice(2);
const skipVendored = process.argv.includes("--skip-vendored");
const { buildLocalInput } = await import(`${src}/connectors/local-git.ts`);
const eng = await import(`${src}/engine.ts`);
const ev = await import(`${src}/evidence.ts`);
const { loadConfig } = await import(`${src}/config.ts`);
const { readFileSync } = await import("node:fs");

const built = buildLocalInput({ repoDir, commit, paths: [], log: () => {}, warn: () => {} });
const input = built.input;
const config = loadConfig({}, () => {});
const kept = eng.filterFiles(input.files, [...eng.DEFAULT_EXCLUDE, ...config.exclude], input.scope).kept;
const batches = eng.planBatches(kept, { maxLines: config.batchLines, maxChars: config.batchChars }, input.pathRules);

const t = () => performance.now();
let a = t();
const plans = batches.map((b: any) => ev.planEvidence(b.files.map((f: any) => ({ filename: f.filename, addedLines: ev.addedLinesOf(f.patch) }))));
const planMs = t() - a;
const perBatch = plans.map((p: any) => p.symbols.map((s: any) => s.name));
const wanted = new Set<string>(perBatch.flat());
const searchesToday = perBatch.reduce((n: number, xs: string[]) => n + xs.length, 0);

// One pass: list source files, read each, tokenize, keep lines for wanted names.
a = t();
const exts = ev.SOURCE_EXTENSIONS.map((e: string) => `*.${e}`);
const excl = ["node_modules/*", "*/node_modules/*", "dist/*", "*/dist/*", "build/*", "*/build/*", ".next/*", "*/.next/*", "vendor/*", "*/vendor/*", "*.min.js", "*.d.ts", ...(skipVendored ? [".repos/*"] : [])].map((p) => `:(exclude)${p}`);
const ls = Bun.spawnSync(["git", "ls-files", "-z", "--", ...exts, ...excl], { cwd: headDir });
const files = new TextDecoder().decode(ls.stdout).split("\0").filter(Boolean);
const listMs = t() - a;
a = t();
const hits = new Map<string, number>();
const TOKEN = /[A-Za-z_][A-Za-z0-9_]*/g; // git grep -w word chars: [A-Za-z0-9_]
let bytes = 0;
for (const f of files) {
  let text: string;
  try { text = readFileSync(`${headDir}/${f}`, "utf8"); } catch { continue; }
  bytes += text.length;
  if (text.includes("\0")) continue; // -I: skip binary
  for (const m of text.matchAll(TOKEN)) if (wanted.has(m[0])) hits.set(m[0], (hits.get(m[0]) ?? 0) + 1);
}
const scanMs = t() - a;

// Differential check on 5 names: lines git grep finds vs lines containing the token.
const sample = [...wanted].slice(0, 5);
const diff = sample.map((name) => {
  const r = Bun.spawnSync(["git", "grep", "-c", "-I", "-w", "-F", "-e", name, "--", ...exts, ...excl], { cwd: headDir });
  const gitLines = new TextDecoder().decode(r.stdout).split("\n").filter(Boolean).reduce((n, l) => n + Number(l.split(":").pop()), 0);
  return { name, gitLines, tokenHits: hits.get(name) ?? 0 };
});
console.log(JSON.stringify({ commit: commit.slice(0, 10), skipVendored, batches: batches.length, searchesToday, uniqueNames: wanted.size, filesScanned: files.length, mbScanned: +(bytes / 1e6).toFixed(1), ms: { planAllBatches: Math.round(planMs), listFiles: Math.round(listMs), onePassScan: Math.round(scanMs) }, diff }));
