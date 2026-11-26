// Reads ../raw/*.jsonl and prints the markdown tables of the README. Usage: bun summarize.ts
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
const raw = join(import.meta.dir, "../raw");
const rows = readdirSync(raw).filter((f) => f.endsWith(".jsonl")).flatMap((f) => readFileSync(join(raw, f), "utf8").trim().split("\n").map((l) => JSON.parse(l)));
const f1 = (n: number) => n.toFixed(n < 10 ? 2 : 1);
const cls = (r: any) => r.medianMs.filter + r.medianMs.split + r.medianMs.risk + r.medianMs.module + r.medianMs.plan;

console.log("### Per pull request (median of 5 runs, ms)\n");
console.log("| PR | changed files | reviewable | added lines | patch KB | batches | read | classify (filter+split+risk+module+plan) | symbols | total |");
console.log("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |");
for (const r of rows) console.log(`| ${r.id} | ${r.changedFiles} | ${r.reviewableFiles} | ${r.addedLinesAll} | ${(r.patchBytes / 1024).toFixed(0)} | ${r.batches} | ${f1(r.medianMs.read)} | ${f1(cls(r))} | ${f1(r.medianMs.symbols)} | ${f1(r.medianMs.total)} |`);

const stages = ["readDiff", "readContents", "filter", "split", "risk", "module", "plan", "addedLines", "extractCalled", "defined", "planEvidence", "total"];
const sum: Record<string, number> = {};
for (const s of stages) sum[s] = rows.reduce((n, r) => n + r.medianMs[s], 0);
const med = (xs: number[]) => { const s = [...xs].sort((a, b) => a - b); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
console.log("\n### Per stage, over all PRs (ms)\n");
console.log("| stage | sum of medians | median PR | max PR | share of total |");
console.log("| --- | ---: | ---: | ---: | ---: |");
for (const s of stages) console.log(`| ${s} | ${f1(sum[s])} | ${f1(med(rows.map((r) => r.medianMs[s])))} | ${f1(Math.max(...rows.map((r) => r.medianMs[s])))} | ${((100 * sum[s]) / sum.total).toFixed(1)}% |`);

const L: Record<string, { files: number; added: number; ex: number; def: number; names: number; defNames: number; reads: boolean; prs: number }> = {};
for (const r of rows) for (const [k, v] of Object.entries<any>(r.languages)) {
  const l = (L[k] ??= { files: 0, added: 0, ex: 0, def: 0, names: 0, defNames: 0, reads: v.engineReads, prs: 0 });
  l.files += v.files; l.added += v.added; l.ex += v.extractMs; l.def += v.definedMs; l.names += v.names; l.defNames += v.definedNames; l.prs++;
}
console.log("\n### Per language, over all PRs (reviewable files only)\n");
console.log("| language | read by the engine's extractor | PRs | files | added lines | extractCalledSymbols ms | definedSymbols ms | extracted names | defined names | ms per 1k added lines (extract) |");
console.log("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |");
const sorted = Object.entries(L).sort((a, b) => b[1].added - a[1].added);
const minor = sorted.filter(([, l]) => l.added < 500 && !l.reads);
const major = sorted.filter((e) => !minor.includes(e));
const line = (k: string, l: any, reads: string) => `| ${k} | ${reads} | ${l.prs} | ${l.files} | ${l.added} | ${f1(l.ex)} | ${f1(l.def)} | ${l.names} | ${l.defNames} | ${l.added ? f1((1000 * l.ex) / l.added) : "-"} |`;
for (const [k, l] of major) console.log(line(k, l, l.reads ? "yes" : "no (forced, for reference)"));
const agg = { prs: 0, files: 0, added: 0, ex: 0, def: 0, names: 0, defNames: 0 };
for (const [, l] of minor) for (const key of Object.keys(agg) as (keyof typeof agg)[]) agg[key] += (l as any)[key];
console.log(line(`${minor.length} minor types (under 500 added lines each; full list in raw/)`, agg, "no (forced, for reference)").replace(`| ${agg.prs} |`, "| - |"));
