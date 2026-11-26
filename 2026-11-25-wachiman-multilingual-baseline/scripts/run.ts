// Times the code-only classification stages of the Wachiman engine over one case: no model, no
// evidence search (collectEvidence is never called). Prints one JSON line.
//
// Usage: bun run.ts --src <engine src dir> --repo <case checkout> --id <case id> [--runs 5]
// The checkout holds .base and .head (written by fetch.sh).
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";

const arg = (n: string) => {
  const i = process.argv.indexOf(`--${n}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
};
const srcDir = resolve(arg("src") ?? "");
const repoDir = resolve(arg("repo") ?? "");
const id = arg("id") ?? "";
const runs = Number(arg("runs") ?? 5);
if (!arg("src") || !arg("repo") || !id) {
  console.error("usage: bun run.ts --src <engine src dir> --repo <case checkout> --id <case id> [--runs N]");
  process.exit(2);
}
const base = readFileSync(join(repoDir, ".base"), "utf8").trim();
const head = readFileSync(join(repoDir, ".head"), "utf8").trim();

const eng: any = await import(join(srcDir, "engine.ts"));
const ev: any = await import(join(srcDir, "evidence.ts"));
const lg: any = await import(join(srcDir, "connectors/local-git.ts"));

// File extension -> language. Extensions the engine reads (SOURCE_EXTENSIONS) are marked per language at run time.
const LANG: Record<string, string> = {
  ts: "TypeScript", tsx: "TypeScript", mts: "TypeScript", cts: "TypeScript",
  js: "JavaScript", jsx: "JavaScript", mjs: "JavaScript", cjs: "JavaScript",
  go: "Go", py: "Python", rb: "Ruby", erb: "Ruby", rake: "Ruby", java: "Java", kt: "Kotlin", kts: "Kotlin",
  rs: "Rust", swift: "Swift", vue: "Vue", svelte: "Svelte", cs: "C#", php: "PHP", c: "C", h: "C", cc: "C++", cpp: "C++", hpp: "C++",
  scss: "CSS", css: "CSS", html: "HTML", ftl: "HTML",
  md: "Markdown", mdx: "Markdown", json: "JSON", yml: "YAML", yaml: "YAML", toml: "TOML", xml: "XML", sql: "SQL", sh: "Shell",
  proto: "Protobuf", properties: "Properties", txt: "Text", svg: "SVG", lock: "Lockfile",
};
const BASENAMES: Record<string, string> = { Dockerfile: "Docker", Makefile: "Make", Gemfile: "Ruby" };
const languageOf = (p: string) => {
  const name = p.split("/").pop() ?? p;
  if (BASENAMES[name]) return BASENAMES[name];
  const dot = name.lastIndexOf(".");
  return dot > 0 ? (LANG[name.slice(dot + 1).toLowerCase()] ?? `other(.${name.slice(dot + 1).toLowerCase()})`) : "other(no ext)";
};

const now = () => performance.now();
const median = (xs: number[]) => {
  const s = [...xs].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

/** Head contents of the changed files, written under a fresh headDir (the dir splitUnreviewable reads). */
function materialise(files: any[]): { dir: string; bytes: number } {
  const dir = mkdtempSync(join(tmpdir(), "classify-head-"));
  const withSha = files.filter((f) => f.sha);
  const proc = Bun.spawnSync(["git", "-C", repoDir, "cat-file", "--batch"], { stdin: Buffer.from(withSha.map((f) => f.sha).join("\n") + "\n"), maxBuffer: 1 << 30 });
  const out = Buffer.from(proc.stdout);
  let pos = 0;
  let bytes = 0;
  for (const f of withSha) {
    const nl = out.indexOf(10, pos);
    const [, type, size] = out.subarray(pos, nl).toString().split(" ");
    pos = nl + 1;
    if (type !== "blob") continue;
    const n = Number(size);
    const target = join(dir, f.filename);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, out.subarray(pos, pos + n));
    bytes += n;
    pos += n + 1;
  }
  return { dir, bytes };
}

type Lang = { files: number; added: number; extractMs: number; definedMs: number; names: number; definedNames: number; engineReads: boolean };

function once() {
  const t: Record<string, number> = {};
  let s = now();
  const files = lg.localFiles(repoDir, base, head);
  t.readDiff = now() - s;
  s = now();
  const headDir = materialise(files);
  t.readContents = now() - s;
  t.read = t.readDiff + t.readContents;

  s = now();
  const { kept, dropped } = eng.filterFiles(files, [...eng.DEFAULT_EXCLUDE], []);
  t.filter = now() - s;

  s = now();
  const { reviewable, unreviewable } = eng.splitUnreviewable(kept, headDir.dir);
  t.split = now() - s;

  s = now();
  for (const f of reviewable) eng.riskScore(f.filename);
  t.risk = now() - s;

  s = now();
  for (const f of reviewable) eng.moduleKey(f.filename);
  t.module = now() - s;

  s = now();
  const batches = eng.planBatches(reviewable, { maxLines: 1000, maxChars: 140000 });
  t.plan = now() - s;

  // Stage 7, per batch: the engine's three calls. Per-file calls are timed for the per-language split.
  const langs: Record<string, Lang> = {};
  const lang = (name: string, f: any) => (langs[name] ??= { files: 0, added: 0, extractMs: 0, definedMs: 0, names: 0, definedNames: 0, engineReads: ev.isSourceFile(f.filename) });
  for (const f of reviewable) {
    const l = lang(languageOf(f.filename), f);
    l.files++;
    l.added += f.additions;
  }
  t.addedLines = 0;
  t.extractCalled = 0;
  t.defined = 0;
  t.planEvidence = 0;
  let planned = 0;
  for (const b of batches) {
    s = now();
    const inputs = b.files.map((f: any) => ({ filename: f.filename, addedLines: ev.addedLinesOf(f.patch) }));
    t.addedLines += now() - s;
    for (const f of inputs) {
      const l = lang(languageOf(f.filename), f);
      s = now();
      const syms = ev.extractCalledSymbols(f.addedLines);
      const e1 = now() - s;
      s = now();
      const def = ev.definedSymbols(f.addedLines);
      const e2 = now() - s;
      l.extractMs += e1;
      l.definedMs += e2;
      l.names += syms.length;
      l.definedNames += def.size;
      if (ev.isSourceFile(f.filename)) {
        t.extractCalled += e1;
        t.defined += e2;
      }
    }
    s = now();
    const plan = ev.planEvidence(inputs);
    t.planEvidence += now() - s;
    planned += plan.symbols.length;
  }
  t.symbols = t.addedLines + t.extractCalled + t.defined + t.planEvidence;
  t.total = t.read + t.filter + t.split + t.risk + t.module + t.plan + t.symbols;

  rmSync(headDir.dir, { recursive: true, force: true });
  const shape = {
    changedFiles: files.length,
    addedLinesAll: files.reduce((n: number, f: any) => n + f.additions, 0),
    deletedLinesAll: files.reduce((n: number, f: any) => n + f.deletions, 0),
    keptFiles: kept.length,
    droppedFiles: dropped.length,
    unreviewableFiles: unreviewable.length,
    reviewableFiles: reviewable.length,
    reviewableAdded: reviewable.reduce((n: number, f: any) => n + f.additions, 0),
    patchBytes: reviewable.reduce((n: number, f: any) => n + (f.patch?.length ?? 0), 0),
    contentBytes: headDir.bytes,
    batches: batches.length,
    plannedSymbols: planned,
  };
  return { t, langs, shape };
}

once(); // warm-up: fetches the lazy blobs and warms the JIT; not counted
const samples = Array.from({ length: runs }, once);
const stages = Object.keys(samples[0].t);
const med = (key: string) => Math.round(median(samples.map((r) => r.t[key])) * 1000) / 1000;
const langOut: Record<string, any> = {};
for (const name of Object.keys(samples[0].langs)) {
  const l = samples[0].langs[name];
  const m = (k: keyof Lang) => Math.round(median(samples.map((r) => r.langs[name][k] as number)) * 1000) / 1000;
  langOut[name] = { files: l.files, added: l.added, engineReads: l.engineReads, extractMs: m("extractMs"), definedMs: m("definedMs"), names: l.names, definedNames: l.definedNames };
}
console.log(JSON.stringify({ id, base, head, runs, ...samples[0].shape, medianMs: Object.fromEntries(stages.map((k) => [k, med(k)])), runMs: samples.map((r) => Math.round(r.t.total * 1000) / 1000), languages: langOut }));
