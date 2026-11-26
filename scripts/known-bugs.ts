#!/usr/bin/env bun
/**
 * Writes `known-bugs.csv`: one row per known bug (an `E<n>` row of a replay doc's Expected issues
 * table) per original PR, read from the primary doc for that PR. The primary doc is the newest doc
 * in `REPLAY_DOCS` order whose Expected table has a Severity column. Older docs are compared with
 * it; a different severity for the same id is printed as a warning and the primary doc wins.
 *
 * Usage: bun scripts/known-bugs.ts --dataset dataset
 */
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { mdTables, REPLAY_DOCS, REPLAY_PRS } from "./labels.ts";
import { toCsv } from "./parse.ts";

export interface KnownBug {
  original_pr: string;
  id: string;
  severity: string;
  title: string;
  doc: string;
}

const SEVERITIES = ["High", "Medium", "Low", "Info"];

export function normaliseSeverity(raw: string): string | null {
  const s = raw.trim().toLowerCase();
  return SEVERITIES.find((x) => x.toLowerCase() === s) ?? null;
}

/** The E rows of a doc's Expected issues table; none when the table has no Severity column. */
export function knownBugs(md: string, doc: string, originalPr: string): KnownBug[] {
  const t = mdTables(md).find((x) => /^Expected/i.test(x.heading) && (x.header[0] ?? "").trim() === "ID");
  if (!t) return [];
  const sev = t.header.findIndex((c) => /^severity$/i.test(c.trim()));
  if (sev < 0) return [];
  const out: KnownBug[] = [];
  for (const row of t.rows) {
    const id = (row[0] ?? "").trim();
    if (!/^E\d+$/.test(id)) continue;
    const severity = normaliseSeverity(row[sev] ?? "");
    if (!severity) throw new Error(`${doc} PR ${originalPr} ${id}: unknown severity "${row[sev]}"`);
    out.push({ original_pr: originalPr, id, severity, title: (row[1] ?? "").trim(), doc });
  }
  return out;
}

/** `perDoc` is oldest first for one PR. The last doc with rows is primary. */
export function pickPrimary(perDoc: KnownBug[][]): { rows: KnownBug[]; warnings: string[] } {
  const docs = perDoc.filter((d) => d.length > 0);
  const primary = docs.at(-1);
  if (!primary) return { rows: [], warnings: [] };
  const warnings: string[] = [];
  for (const other of docs.slice(0, -1)) {
    for (const o of other) {
      const p = primary.find((x) => x.id === o.id);
      if (p && p.severity !== o.severity) {
        warnings.push(`PR ${o.original_pr} ${o.id}: ${o.doc} says ${o.severity}, ${p.doc} (primary) says ${p.severity}`);
      }
    }
  }
  return { rows: primary, warnings };
}

const COLUMNS = ["original_pr", "id", "severity", "title", "doc"] as const;

function main() {
  const argv = process.argv.slice(2);
  const i = argv.indexOf("--dataset");
  const dataset = i >= 0 ? argv[i + 1] : undefined;
  if (!dataset) throw new Error("usage: known-bugs.ts --dataset <dir>");
  const all: KnownBug[] = [];
  for (const pr of REPLAY_PRS) {
    const perDoc: KnownBug[][] = [];
    for (const d of REPLAY_DOCS) {
      const p = `${d.dir}/pr-${pr}.md`;
      perDoc.push(existsSync(p) ? knownBugs(readFileSync(p, "utf8"), d.name, pr) : []);
    }
    const { rows, warnings } = pickPrimary(perDoc);
    for (const w of warnings) console.warn(`warning: ${w}`);
    all.push(...rows);
  }
  writeFileSync(join(dataset, "known-bugs.csv"), toCsv(COLUMNS, all as unknown as Record<string, unknown>[]));
  const counts = REPLAY_PRS.map((pr) => `${pr}: ${all.filter((r) => r.original_pr === pr).length}`).join(", ");
  console.log(`known bugs ${all.length} (${counts})`);
}

if (import.meta.main) main();
