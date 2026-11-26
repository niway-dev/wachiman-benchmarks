#!/usr/bin/env bun
/**
 * Writes `martian-runs.csv`: one row per run of Wachiman on Martian's benchmark, read from each
 * `martian/runs/<run>/metrics.json`. The run directory name carries the date, the Wachiman version,
 * the model, the effort and a repeat suffix (`-r2`); a directory that does not follow that shape
 * (a partial re-run such as `2026-11-11-keycloak-range-fix`) is kept with `full_run = false` and
 * empty version and model, so a chart by version leaves it out.
 *
 * Usage: bun scripts/martian-runs.ts --runs martian/runs --out dataset/martian-runs.csv
 */
import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { toCsv } from "./parse.ts";

export const MARTIAN_COLUMNS = [
  "run",
  "date",
  "version",
  "model",
  "effort",
  "repeat",
  "verifier",
  "full_run",
  "prs",
  "true_positives",
  "false_positives",
  "false_negatives",
  "precision",
  "recall",
  "f1",
  "hc_found",
  "hc_total",
  "hc_recall",
  "findings",
  "cost_usd",
  "cost_per_pr_median_usd",
  "cost_per_pr_p90_usd",
  "cost_per_hc_found_usd",
  "minutes_median",
  "minutes_max",
  "judge_cost_usd",
] as const;

export interface RunName {
  date: string;
  version: string;
  model: string;
  effort: string;
  repeat: number;
  verifier: string;
}

const MODELS: Record<string, string> = { haiku: "claude-haiku-5-5", sonnet: "claude-sonnet-5-5", opus: "claude-opus-5-5" };

/** Reads `2026-11-12-v1.9.0-sonnet-5-5-high-r2` or `...-haiku-5-5-high-opus-verifier`; null for any other shape. */
export function parseRunName(name: string): RunName | null {
  const m = /^(\d{4}-\d{2}-\d{2})-(v\d+\.\d+\.\d+(?:\+[\w.-]+)?)-(haiku|sonnet|opus)-5-5(?:-(low|medium|high|max))?(?:-(\w+)-verifier)?(?:-r(\d+))?$/.exec(name);
  if (!m) return null;
  return {
    date: m[1]!,
    version: m[2]!,
    model: MODELS[m[3]!]!,
    effort: m[4] ?? "",
    repeat: m[6] ? Number(m[6]) : 1,
    verifier: m[5] ? MODELS[m[5]] ?? m[5] : "",
  };
}

const round = (n: unknown, digits: number) => (typeof n === "number" && Number.isFinite(n) ? Number(n.toFixed(digits)) : "");

/** One CSV row from a run directory name and its parsed metrics.json. */
export function martianRow(name: string, metrics: any): Record<string, unknown> {
  const parsed = parseRunName(name);
  const all = metrics?.quality?.all ?? {};
  const cost = metrics?.product_cost ?? {};
  return {
    run: name,
    date: parsed?.date ?? name.slice(0, 10),
    version: parsed?.version ?? "",
    model: parsed?.model ?? "",
    effort: parsed?.effort ?? "",
    repeat: parsed?.repeat ?? "",
    verifier: parsed?.verifier ?? "",
    full_run: parsed !== null && all.prs === 50,
    prs: all.prs ?? "",
    true_positives: all.tp ?? "",
    false_positives: all.fp ?? "",
    false_negatives: all.fn ?? "",
    precision: round(all.precision, 4),
    recall: round(all.recall, 4),
    f1: round(all.f1, 4),
    hc_found: all.hc ?? "",
    hc_total: all.hc_total ?? "",
    hc_recall: typeof all.hc === "number" && all.hc_total ? round(all.hc / all.hc_total, 4) : "",
    findings: cost.findings ?? "",
    cost_usd: round(cost.total_usd, 4),
    cost_per_pr_median_usd: round(cost.per_pr_median_usd, 4),
    cost_per_pr_p90_usd: round(cost.per_pr_p90_usd, 4),
    cost_per_hc_found_usd: round(cost.per_hc_found_usd, 4),
    minutes_median: round(cost.minutes_median, 2),
    minutes_max: round(cost.minutes_max, 2),
    judge_cost_usd: round(metrics?.judge_cost?.usd, 2),
  };
}

export function martianRows(runsDir: string): Record<string, unknown>[] {
  return readdirSync(runsDir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && existsSync(join(runsDir, e.name, "metrics.json")))
    .map((e) => e.name)
    .sort()
    .map((name) => martianRow(name, JSON.parse(readFileSync(join(runsDir, name, "metrics.json"), "utf8"))));
}

if (import.meta.main) {
  const arg = (flag: string, fallback: string) => {
    const i = process.argv.indexOf(flag);
    return i > 0 && process.argv[i + 1] ? process.argv[i + 1]! : fallback;
  };
  const runs = arg("--runs", "martian/runs");
  const out = arg("--out", "dataset/martian-runs.csv");
  const rows = martianRows(runs);
  writeFileSync(out, toCsv(MARTIAN_COLUMNS, rows));
  console.log(`martian-runs: ${rows.length} runs (${rows.filter((r) => r.full_run).length} full) into ${out}`);
}
