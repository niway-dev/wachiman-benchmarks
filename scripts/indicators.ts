/**
 * Computes every number quoted in a day's INDICATORS.md from the files `pair.ts` wrote and the
 * hand-written `verdicts.csv`. No model runs and nothing is estimated: each value is a count, a
 * sum or a median over those CSVs.
 *
 *   bun scripts/indicators.ts 2026-11-06-kaipu-day   # prints JSON; also writes <dir>/indicators.json
 */
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

type Row = Record<string, string>;

/** Minimal CSV reader: quoted fields, doubled quotes, embedded commas and newlines. */
export function parseCsv(text: string): Row[] {
  const rows: string[][] = [];
  let field = "";
  let row: string[] = [];
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i]!;
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') {
        field += '"';
        i++;
      } else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") {
      row.push(field);
      field = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      field = "";
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
    } else field += c;
  }
  if (field !== "" || row.length) {
    row.push(field);
    rows.push(row);
  }
  const [head, ...body] = rows;
  return body.map((r) => Object.fromEntries(head!.map((h, i) => [h, r[i] ?? ""])));
}

const sum = (xs: number[]): number => xs.reduce((a, b) => a + b, 0);
const round = (n: number, d = 2): number => Math.round(n * 10 ** d) / 10 ** d;
const median = (xs: number[]): number => {
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
const count = <T>(xs: T[], f: (x: T) => boolean): number => xs.filter(f).length;

export function indicators(dir: string): Record<string, unknown> {
  const read = (f: string): Row[] => parseCsv(readFileSync(join(dir, f), "utf8"));
  const reviews = read("pairs/reviews.csv");
  const pairs = read("pairs/pairs.csv");
  const special = read("pairs/special-cases.csv");
  const findings = read("pairs/findings.csv");
  const verdicts = read("verdicts.csv");

  // Coverage ---------------------------------------------------------------------------------
  const commits = new Set(reviews.map((r) => `${r.pr}:${r.commit}`));
  const completedBy = (tool: string): number =>
    new Set(reviews.filter((r) => r.tool === tool && r.status === "completed").map((r) => `${r.pr}:${r.commit}`)).size;
  const status = (tool: string, s: string): number => count(reviews, (r) => r.tool === tool && r.status === s);
  const specialCommits = new Set(special.map((r) => `${r.pr}:${r.commit}`));

  // Findings and verdicts --------------------------------------------------------------------
  const paired = findings.filter((f) => f.comparison === "paired");
  const byId = new Map(verdicts.map((v) => [v.id, v]));
  const toolOf = (id: string): string => findings.find((f) => f.id === id)!.tool;
  const perTool = (tool: string) => {
    const mine = paired.filter((f) => f.tool === tool);
    const v = mine.map((f) => byId.get(f.id)!);
    const n = (verdict: string): number => count(v, (x) => x.verdict === verdict);
    return {
      findings: mine.length,
      verified: n("verified"),
      ownerAccepted: n("owner-accepted"),
      unverified: n("unverified"),
      wrong: n("wrong"),
      confirmed: n("verified") + n("owner-accepted"),
    };
  };

  // A defect found by both tools appears as two rows joined by `matched_by`: count it once.
  const defects = (verdictNames: string[]): { rows: number; distinct: number; bothTools: number } => {
    const rows = verdicts.filter((v) => verdictNames.includes(v.verdict));
    const seen = new Set<string>();
    let distinct = 0;
    let bothTools = 0;
    for (const v of rows) {
      if (seen.has(v.id)) continue;
      seen.add(v.id);
      distinct++;
      if (v.matched_by && byId.has(v.matched_by) && verdictNames.includes(byId.get(v.matched_by)!.verdict)) {
        seen.add(v.matched_by);
        if (toolOf(v.matched_by) !== toolOf(v.id)) bothTools++;
      }
    }
    return { rows: rows.length, distinct, bothTools };
  };
  const found = (tool: string, verdictNames: string[]): number => {
    const rows = verdicts.filter((v) => verdictNames.includes(v.verdict));
    const ids = new Set<string>();
    for (const v of rows) {
      const group = [v.id, v.matched_by].filter(Boolean).sort().join("|");
      if (toolOf(v.id) === tool || (v.matched_by && toolOf(v.matched_by) === tool)) ids.add(group);
    }
    return ids.size;
  };
  const verifiedSet = ["verified"];
  const confirmedSet = ["verified", "owner-accepted"];

  const label = (l: string): { total: number; confirmed: number } => {
    const rows = paired.filter((f) => f.tool === "wachiman" && f.severity === l);
    return { total: rows.length, confirmed: count(rows, (f) => confirmedSet.includes(byId.get(f.id)!.verdict)) };
  };
  const tests = paired.filter((f) => f.tool === "wachiman" && f.topic === "tests");

  // Cost -------------------------------------------------------------------------------------
  const pairCost = pairs.map((p) => Number(p.wachiman_cost_usd));
  const wachimanReviews = reviews.filter((r) => r.tool === "wachiman");
  const allCost = sum(wachimanReviews.map((r) => Number(r.cost_usd || 0)));
  const partialCost = sum(wachimanReviews.filter((r) => r.status === "partial").map((r) => Number(r.cost_usd || 0)));
  const zeroCost = sum(pairs.filter((p) => Number(p.wachiman_findings) === 0).map((p) => Number(p.wachiman_cost_usd)));
  const apart = pairs.map((p) => Number(p.minutes_apart));
  const confirmedWachiman = perTool("wachiman").confirmed;
  const verifiedDefectsWachiman = found("wachiman", verifiedSet);

  return {
    coverage: {
      distinctCommitsSeen: commits.size,
      pairs: pairs.length,
      pairRatePct: round((pairs.length / commits.size) * 100, 1),
      wachimanCompleted: completedBy("wachiman"),
      wachimanCompletedPct: round((completedBy("wachiman") / commits.size) * 100, 1),
      wachimanPartial: status("wachiman", "partial"),
      wachimanRefused: status("wachiman", "refused"),
      coderabbitCompleted: completedBy("coderabbit"),
      coderabbitCompletedPct: round((completedBy("coderabbit") / commits.size) * 100, 1),
      coderabbitSkipped: status("coderabbit", "skipped"),
      specialCaseRows: special.length,
      specialCaseDistinctCommits: specialCommits.size,
      specialByStatus: Object.fromEntries(
        ["partial", "skipped", "unpaired", "refused"].map((s) => [s, count(special, (r) => r.status === s)]),
      ),
    },
    findings: {
      comparable: { wachiman: perTool("wachiman"), coderabbit: perTool("coderabbit") },
      wachimanFindingsOnNonComparableCommits: count(findings, (f) => f.tool === "wachiman" && f.comparison === "special"),
      distinctVerifiedDefects: defects(verifiedSet),
      distinctConfirmedDefects: defects(confirmedSet),
      verifiedDefectsFound: { wachiman: found("wachiman", verifiedSet), coderabbit: found("coderabbit", verifiedSet) },
      confirmedDefectsFound: { wachiman: found("wachiman", confirmedSet), coderabbit: found("coderabbit", confirmedSet) },
      wachimanOnlyVerified: verifiedDefectsFound(verdicts, toolOf, "wachiman"),
      coderabbitOnlyVerified: verifiedDefectsFound(verdicts, toolOf, "coderabbit"),
    },
    labelPrecision: { fix: label("fix"), consider: label("consider") },
    testNotes: {
      total: tests.length,
      ownerAccepted: count(tests, (f) => byId.get(f.id)!.verdict === "owner-accepted"),
      unverified: count(tests, (f) => byId.get(f.id)!.verdict === "unverified"),
      verified: count(tests, (f) => byId.get(f.id)!.verdict === "verified"),
    },
    cost: {
      wachimanOnPairsUsd: round(sum(pairCost)),
      perPairMeanUsd: round(sum(pairCost) / pairs.length, 3),
      perPairMedianUsd: round(median(pairCost), 3),
      largestPairUsd: Math.max(...pairCost),
      largestPairSharePct: round((Math.max(...pairCost) / sum(pairCost)) * 100, 1),
      perConfirmedFindingUsd: round(sum(pairCost) / confirmedWachiman),
      perVerifiedDefectUsd: round(sum(pairCost) / verifiedDefectsWachiman),
      wachimanAllReviewsUsd: round(allCost),
      outsidePairsUsd: round(allCost - sum(pairCost)),
      outsidePairsSharePct: round(((allCost - sum(pairCost)) / allCost) * 100, 1),
      partialReviewsUsd: round(partialCost),
      zeroFindingPairs: count(pairs, (p) => Number(p.wachiman_findings) === 0),
      zeroFindingPairsUsd: round(zeroCost),
    },
    minutesApart: {
      median: median(apart),
      mean: round(sum(apart) / apart.length),
      min: Math.min(...apart),
      max: Math.max(...apart),
      within5: count(apart, (m) => Math.abs(m) <= 5),
    },
  };
}

function verifiedDefectsFound(verdicts: Row[], toolOf: (id: string) => string, tool: string): number {
  return verdicts.filter((v) => v.verdict === "verified" && !v.matched_by && toolOf(v.id) === tool).length;
}

if (import.meta.main) {
  const dir = process.argv[2];
  if (!dir) throw new Error("usage: bun scripts/indicators.ts <day-folder>");
  const out = indicators(dir);
  writeFileSync(join(dir, "indicators.json"), JSON.stringify(out, null, 2) + "\n");
  console.log(JSON.stringify(out, null, 2));
}
