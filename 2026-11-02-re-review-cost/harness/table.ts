#!/usr/bin/env bun
/** Aggregates classify.ts output per arm: bun table.ts <runs dir> → markdown tables on stdout. */
import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { summarise } from "./classify";

const runs = process.argv[2];
const cases = readdirSync(runs).filter((d) => /^\d{3}-[0-9a-f]{7}$/.test(d)).sort();
const arms = ["base", "base2", "T", "F", "TFR"];
const classes = ["read-changed-full", "read-changed-part", "read-unchanged", "search", "read-threads", "read-pr", "read-evidence", "final-output", "no-tool"];
const ctxKeys = ["prompt", "output", "read-changed-full", "read-changed-part", "read-unchanged", "search", "read-threads", "read-pr"];
const r2 = (n: number) => n.toFixed(2);
const r3 = (n: number) => n.toFixed(3);
const all: Record<string, Record<string, ReturnType<typeof summarise>>> = {};
for (const a of arms) {
  all[a] = {};
  for (const c of cases) if (existsSync(join(runs, c, a, "call-1.jsonl"))) all[a][c] = summarise(join(runs, c, a));
}
console.log("### Cost and turns per case\n");
console.log(`| Case | ${arms.join(" | ")} |`);
console.log(`| --- | ${arms.map(() => "---").join(" | ")} |`);
for (const c of cases) {
  if (arms.every((a) => !all[a][c])) continue;
  const cells = arms.map((a) => {
    const s = all[a][c];
    if (!s) return "—";
    const p = s.perCall as { assistantMessages: number; findings: number; threadReplies: number }[];
    return `$${r2(s.totalCost)} · ${s.totalTurns}t · ${p.reduce((x, y) => x + y.assistantMessages, 0)}r · ${p.reduce((x, y) => x + y.findings, 0)}f · ${p.reduce((x, y) => x + y.threadReplies, 0)}tr`;
  });
  console.log(`| ${c} | ${cells.join(" | ")} |`);
}
const tot = (a: string) => Object.values(all[a]);
console.log(`| **Total** | ${arms.map((a) => {
  const s = tot(a);
  return `**$${r2(s.reduce((x, y) => x + y.totalCost, 0))}** · ${s.reduce((x, y) => x + y.totalTurns, 0)}t · ${s.reduce((x, y) => x + (y.perCall as { assistantMessages: number }[]).reduce((p, q) => p + q.assistantMessages, 0), 0)}r`;
}).join(" | ")} |`);
console.log("\n### Tool calls (= turns − 1) by class, summed over the cases\n");
console.log(`| Class | ${arms.join(" | ")} |`);
console.log(`| --- | ${arms.map(() => "---").join(" | ")} |`);
for (const k of classes) {
  console.log(`| ${k} | ${arms.map((a) => tot(a).reduce((x, y) => x + (y.byClass[k]?.calls ?? 0), 0)).join(" | ")} |`);
}
console.log("\n### Cost by what entered the context (USD, summed over the cases)\n");
console.log(`| Part | ${arms.join(" | ")} |`);
console.log(`| --- | ${arms.map(() => "---").join(" | ")} |`);
for (const k of ctxKeys) {
  console.log(`| ${k} | ${arms.map((a) => r3(tot(a).reduce((x, y) => x + ((y.contextCostUsd as Record<string, number>)[k] ?? 0), 0))).join(" | ")} |`);
}
console.log(`| reported total | ${arms.map((a) => r3(tot(a).reduce((x, y) => x + y.totalCost, 0))).join(" | ")} |`);
console.log("\n### Result chars by class (what each class put into context), summed\n");
console.log(`| Class | ${arms.join(" | ")} |`);
console.log(`| --- | ${arms.map(() => "---").join(" | ")} |`);
for (const k of classes.slice(0, 7)) {
  console.log(`| ${k} | ${arms.map((a) => tot(a).reduce((x, y) => x + (y.byClass[k]?.resultChars ?? 0), 0)).join(" | ")} |`);
}
