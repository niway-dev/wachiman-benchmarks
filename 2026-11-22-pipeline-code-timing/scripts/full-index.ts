// Experiment: build a FULL identifier index of a checkout (every word -> lines), save it, load it back.
// Answers: how long does indexing the whole repository take, how big is it, and is loading a saved one faster?
// Usage: bun full-index.ts <engine-src> <checkoutDir> <outFile> [--skip-vendored]
const [src, headDir, outFile] = process.argv.slice(2);
const skipVendored = process.argv.includes("--skip-vendored");
const ev = await import(`${src}/evidence.ts`);
const { readFileSync, writeFileSync, statSync } = await import("node:fs");
const { gzipSync, gunzipSync } = await import("node:zlib");
const t = () => performance.now();

const exts = ev.SOURCE_EXTENSIONS.map((e: string) => `*.${e}`);
const excl = ["node_modules/*", "*/node_modules/*", "dist/*", "*/dist/*", "build/*", "*/build/*", ".next/*", "*/.next/*", "vendor/*", "*/vendor/*", "*.min.js", "*.d.ts", ...(skipVendored ? [".repos/*"] : [])].map((p) => `:(exclude)${p}`);
let a = t();
const ls = Bun.spawnSync(["git", "ls-files", "-z", "--", ...exts, ...excl], { cwd: headDir });
const files = new TextDecoder().decode(ls.stdout).split("\0").filter(Boolean);
const listMs = t() - a;

// postings: word -> flat array of [fileIdx, line, fileIdx, line, ...], one entry per (file, line) like git grep -n.
a = t();
const postings = new Map<string, number[]>();
const TOKEN = /[A-Za-z_][A-Za-z0-9_]*/g;
let bytes = 0, readMs = 0;
for (let fi = 0; fi < files.length; fi++) {
  const r0 = t();
  let text: string;
  try { text = readFileSync(`${headDir}/${files[fi]}`, "utf8"); } catch { continue; }
  readMs += t() - r0;
  bytes += text.length;
  if (text.includes("\0")) continue;
  const lines = text.split("\n");
  for (let li = 0; li < lines.length; li++) {
    const seen = new Set<string>();
    for (const m of lines[li].matchAll(TOKEN)) {
      const w = m[0];
      if (w.length < 3 || w.length > 64 || seen.has(w)) continue;
      seen.add(w);
      let p = postings.get(w);
      if (!p) postings.set(w, (p = []));
      p.push(fi, li + 1);
    }
  }
}
const buildMs = t() - a;
let entries = 0;
for (const p of postings.values()) entries += p.length / 2;

a = t();
const blob = gzipSync(JSON.stringify({ files, postings: Object.fromEntries(postings) }));
writeFileSync(outFile, blob);
const saveMs = t() - a;
a = t();
const loaded = JSON.parse(gunzipSync(readFileSync(outFile)).toString());
const loadMs = t() - a;

console.log(JSON.stringify({
  dir: headDir.split("/").pop(), skipVendored, files: files.length, mb: +(bytes / 1e6).toFixed(1),
  distinctWords: postings.size, lineEntries: entries, savedMb: +(statSync(outFile).size / 1e6).toFixed(1),
  rssMb: Math.round(process.memoryUsage().rss / 1e6),
  ms: { listFiles: Math.round(listMs), readFiles: Math.round(readMs), buildTotal: Math.round(buildMs), saveGzipJson: Math.round(saveMs), loadGzipJson: Math.round(loadMs) },
  loadedWords: Object.keys(loaded.postings).length,
}));
