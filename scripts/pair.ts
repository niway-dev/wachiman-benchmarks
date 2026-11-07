/**
 * Pairs Wachiman's reviews with another reviewer's on the same pull requests, commit by commit.
 *
 * A pair is one commit that both tools finished reviewing. Only pairs feed a comparison. Everything
 * else (a tool that refused, skipped, never ran, or reviewed a different commit) is a special case,
 * listed apart with the reason, never mixed into the comparable set.
 *
 * Everything comes from the GitHub API through `gh`; no model runs here. The Wachiman engine
 * version comes from the workflow run that produced the review (`referenced_workflows`), because
 * the review footer does not carry it.
 *
 *   bun scripts/pair.ts --repo niway-dev/kaipu-record --prs 534-540 --other coderabbit --out <dir>
 *   bun scripts/pair.ts --fixtures scripts/fixtures/pair --other coderabbit --out <dir>   # offline
 */
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { ghJson, ghPaginate } from "./gh.ts";
import {
  hasWachimanSignature,
  parseCodeRabbit,
  parseCodeRabbitBody,
  parsePullfrog,
  parseWachimanHeader,
  parseWachimanReview,
  toCsv,
} from "./parse.ts";

export type Other = "coderabbit" | "pullfrog";
export type Tool = "wachiman" | Other;

export interface RawPr {
  pr: { number: number; title: string; html_url: string; head: { sha: string }; created_at: string };
  reviews: { id: number; user: { login: string }; body: string; commit_id: string; submitted_at: string; html_url: string }[];
  reviewComments: {
    id: number; user: { login: string }; body: string; path: string; line: number | null; original_line: number | null;
    commit_id: string; original_commit_id: string; created_at: string; html_url: string; in_reply_to_id?: number;
    pull_request_review_id: number;
  }[];
  issueComments: { id: number; user: { login: string }; body: string; created_at: string; html_url: string }[];
  /** Workflow runs by head sha, as the actions API lists them. */
  runs: Record<string, { id: number; name: string; conclusion: string | null; created_at: string; referenced_workflows?: { ref: string }[] }[]>;
}

/** One review a tool completed, refused or skipped at one commit. */
export interface ReviewRecord {
  pr: number;
  tool: Tool;
  commit: string;
  review_id: number;
  submitted_at: string;
  url: string;
  /** `completed`: findings can be compared. Anything else is a special case. */
  status: "completed" | "refused" | "skipped" | "partial";
  reason: string;
  scope: string;
  /** Wachiman only: engine version from the workflow run, model, effort and the posted cost. */
  version: string;
  model: string;
  effort: string;
  cost_usd: number | null;
  findings: number;
}

export interface FindingRecord {
  id: string;
  pr: number;
  tool: Tool;
  commit: string;
  review_id: number;
  comment_id: number | "";
  placement: "inline" | "body";
  path: string;
  line: number;
  severity: string;
  topic: string;
  confidence: string;
  native_severity: string;
  native_category: string;
  native_tags: string;
  title: string;
  url: string;
  /** `paired` when the commit was completed by both tools; else `special`. */
  comparison: "paired" | "special";
}

export interface SpecialCase {
  pr: number;
  commit: string;
  tool: Tool;
  status: ReviewRecord["status"] | "unpaired";
  /** Wachiman only: the engine version of that review, so a special case still says what ran. */
  version: string;
  reason: string;
  /** What would make it comparable. */
  action: string;
}

export interface PairRow {
  pr: number;
  commit: string;
  wachiman_review: number;
  wachiman_version: string;
  wachiman_model: string;
  wachiman_effort: string;
  wachiman_cost_usd: number | null;
  wachiman_findings: number;
  other_tool: Other;
  other_review: number;
  other_findings: number;
  /** Minutes from Wachiman's post to the other tool's; negative when the other tool posted first. */
  minutes_apart: number;
}

export const OTHER_LOGIN: Record<Other, string> = { coderabbit: "coderabbitai[bot]", pullfrog: "pullfrog[bot]" };
const isWachimanLogin = (login: string) => login === "github-actions[bot]";

/** The engine version from the latest tagged Wachiman run started before the review; "" when none. */
export function versionFromRuns(runs: RawPr["runs"][string] | undefined, submittedAt: string): string {
  if (!runs) return "";
  const at = Date.parse(submittedAt);
  const tagged = (r: RawPr["runs"][string][number]) => r.referenced_workflows?.find((w) => /refs\/tags\/v\d/.test(w.ref))?.ref;
  const candidates = runs
    .filter((r) => tagged(r) && Date.parse(r.created_at) <= at + 60_000)
    .sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  return (candidates[0] ? tagged(candidates[0]) ?? "" : "").replace("refs/tags/", "");
}

export function wachimanReviews(raw: RawPr): { reviews: ReviewRecord[]; findings: FindingRecord[] } {
  const reviews: ReviewRecord[] = [];
  const findings: FindingRecord[] = [];
  for (const r of raw.reviews) {
    if (!isWachimanLogin(r.user.login) || !hasWachimanSignature(r.body)) continue;
    const parsed = parseWachimanReview(r.body);
    const refused = /\*\*Not reviewed: ([^*]+)\*\*/.exec(r.body);
    const version = versionFromRuns(raw.runs[r.commit_id], r.submitted_at);
    const base = {
      pr: raw.pr.number, tool: "wachiman" as const, commit: r.commit_id, review_id: r.id,
      submitted_at: r.submitted_at, url: r.html_url, version,
      model: parsed?.model_label ?? "", effort: parsed?.effort ?? "", cost_usd: parsed?.cost_usd ?? null,
    };
    if (refused) {
      reviews.push({ ...base, status: "refused", reason: (refused[1] as string).trim(), scope: "", findings: 0 });
      continue;
    }
    if (!parsed || !parsed.has_summary) continue; // a thread reply or a notice, not a review
    const inline = raw.reviewComments.filter((c) => c.user.login === r.user.login && !c.in_reply_to_id && c.pull_request_review_id === r.id);
    for (const c of inline) {
      const label = parseWachimanHeader(c.body);
      if (!label) continue;
      findings.push({
        id: `wachiman-${raw.pr.number}-${c.id}`, pr: raw.pr.number, tool: "wachiman", commit: r.commit_id, review_id: r.id,
        comment_id: c.id, placement: "inline", path: c.path, line: c.original_line ?? c.line ?? 0,
        severity: label.severity, topic: label.topic, confidence: label.confidence ?? "",
        native_severity: "", native_category: "", native_tags: "", title: label.title, url: c.html_url, comparison: "special",
      });
    }
    for (const [i, f] of parsed.body_findings.entries()) {
      findings.push({
        id: `wachiman-${raw.pr.number}-${r.id}-b${i}`, pr: raw.pr.number, tool: "wachiman", commit: r.commit_id, review_id: r.id,
        comment_id: "", placement: "body", path: f.path, line: f.line, severity: f.severity, topic: f.topic,
        confidence: f.confidence ?? "", native_severity: "", native_category: "", native_tags: "", title: f.title, url: r.html_url,
        comparison: "special",
      });
    }
    reviews.push({
      ...base, status: parsed.partial ? "partial" : "completed",
      reason: parsed.partial ? "partial review: some files were not reviewed" : "",
      scope: parsed.scope, findings: findings.filter((f) => f.review_id === r.id).length,
    });
  }
  return { reviews, findings };
}

export function otherReviews(raw: RawPr, other: Other): { reviews: ReviewRecord[]; findings: FindingRecord[] } {
  const login = OTHER_LOGIN[other];
  const reviews: ReviewRecord[] = [];
  const findings: FindingRecord[] = [];
  const parse = other === "coderabbit" ? parseCodeRabbit : parsePullfrog;
  for (const r of raw.reviews.filter((x) => x.user.login === login)) {
    const inline = raw.reviewComments.filter((c) => c.user.login === login && !c.in_reply_to_id && c.pull_request_review_id === r.id);
    for (const c of inline) {
      const n = parse(c.body);
      findings.push({
        id: `${other}-${raw.pr.number}-${c.id}`, pr: raw.pr.number, tool: other, commit: r.commit_id, review_id: r.id,
        comment_id: c.id, placement: "inline", path: c.path, line: c.original_line ?? c.line ?? 0,
        severity: "", topic: "", confidence: "", native_severity: n.native_severity, native_category: n.native_category,
        native_tags: n.native_tags, title: n.title, url: c.html_url, comparison: "special",
      });
    }
    if (other === "coderabbit") {
      for (const [i, f] of parseCodeRabbitBody(r.body).entries()) {
        findings.push({
          id: `${other}-${raw.pr.number}-${r.id}-b${i}`, pr: raw.pr.number, tool: other, commit: r.commit_id, review_id: r.id,
          comment_id: "", placement: "body", path: f.path, line: f.line, severity: "", topic: "", confidence: "",
          native_severity: f.native_severity, native_category: f.native_category,
          native_tags: f.section + (f.native_tags ? ` · ${f.native_tags}` : ""), title: f.title, url: r.html_url, comparison: "special",
        });
      }
    }
    // One review per push, even with nothing to say: the tool looked and found nothing. That is a
    // completed review, and a legitimate pair.
    reviews.push({
      pr: raw.pr.number, tool: other, commit: r.commit_id, review_id: r.id, submitted_at: r.submitted_at, url: r.html_url,
      status: "completed", reason: "", scope: "", version: "", model: "", effort: "",
      cost_usd: pullfrogCost(other, r.body), findings: findings.filter((f) => f.review_id === r.id).length,
    });
  }
  // A skipped review is an issue comment, not a review, so it names no commit: it is recorded
  // against the PR head.
  for (const c of raw.issueComments.filter((x) => x.user.login === login)) {
    const skipped = /## Review skipped\s*\n[\s>]*([^\n]+)/.exec(c.body);
    if (skipped) {
      reviews.push({
        pr: raw.pr.number, tool: other, commit: raw.pr.head.sha, review_id: c.id, submitted_at: c.created_at, url: c.html_url,
        status: "skipped", reason: (skipped[1] as string).trim(), scope: "", version: "", model: "", effort: "", cost_usd: null, findings: 0,
      });
    }
  }
  return { reviews, findings };
}

/** Pullfrog prints what a review cost; CodeRabbit does not. The pattern is unverified against a real Pullfrog body. */
function pullfrogCost(other: Other, body: string): number | null {
  if (other !== "pullfrog") return null;
  const m = /\bcost\b[^$\n]*\$([\d.]+)/i.exec(body);
  return m ? Number(m[1]) : null;
}

export function pair(all: { reviews: ReviewRecord[]; findings: FindingRecord[] }[], other: Other): {
  pairs: PairRow[]; specials: SpecialCase[]; findings: FindingRecord[];
} {
  const pairs: PairRow[] = [];
  const specials: SpecialCase[] = [];
  const findings: FindingRecord[] = [];
  for (const { reviews, findings: fs } of all) {
    const pr = reviews[0]?.pr ?? fs[0]?.pr;
    if (pr === undefined) continue;
    const done = (tool: Tool) => reviews.filter((r) => r.tool === tool && r.status === "completed");
    const w = done("wachiman");
    const o = done(other);
    const paired = new Set<string>();
    for (const c of new Set(reviews.map((r) => r.commit))) {
      const wr = w.find((r) => r.commit === c);
      const or = o.find((r) => r.commit === c);
      if (!wr || !or) continue;
      paired.add(c);
      pairs.push({
        pr, commit: c, wachiman_review: wr.review_id, wachiman_version: wr.version, wachiman_model: wr.model,
        wachiman_effort: wr.effort, wachiman_cost_usd: wr.cost_usd, wachiman_findings: wr.findings,
        other_tool: other, other_review: or.review_id, other_findings: or.findings,
        minutes_apart: Math.round((Date.parse(or.submitted_at) - Date.parse(wr.submitted_at)) / 60_000),
      });
    }
    for (const r of reviews) {
      if (r.status !== "completed") {
        specials.push({ pr, commit: r.commit, tool: r.tool, status: r.status, version: r.version, reason: r.reason, action: actionFor(r.status, r.tool) });
      } else if (!paired.has(r.commit)) {
        const otherTool: Tool = r.tool === "wachiman" ? other : "wachiman";
        const otherTried = reviews.some((x) => x.tool === otherTool && x.commit === r.commit);
        specials.push({
          pr, commit: r.commit, tool: r.tool, status: "unpaired", version: r.version,
          reason: otherTried ? `${otherTool} did not complete at this commit` : `${otherTool} never reviewed this commit`,
          action: `rerun ${otherTool} at this commit (basis: rerun), or replay the commit`,
        });
      }
    }
    for (const f of fs) findings.push({ ...f, comparison: paired.has(f.commit) ? "paired" : "special" });
  }
  return { pairs, specials, findings };
}

function actionFor(status: ReviewRecord["status"], tool: Tool): string {
  if (status === "refused") return tool === "wachiman" ? "rerun locally at this commit (basis: rerun), or replay the commit" : "rerun the tool at this commit";
  if (status === "skipped") return "replay the commit where the tool's filters admit it, or compare nothing";
  if (status === "partial") return "compare only the files it reviewed; list the rest";
  return "";
}

// ---------------------------------------------------------------------------------------------
// I/O

export async function fetchPr(repo: string, n: number): Promise<RawPr> {
  const pr = await ghJson<RawPr["pr"]>(`repos/${repo}/pulls/${n}`);
  const reviews = await ghPaginate<RawPr["reviews"][number]>(`repos/${repo}/pulls/${n}/reviews`);
  const comments = await ghPaginate<RawPr["reviewComments"][number]>(`repos/${repo}/pulls/${n}/comments`);
  const issue = await ghPaginate<RawPr["issueComments"][number]>(`repos/${repo}/issues/${n}/comments`);
  if (!pr.ok) throw new Error(`#${n}: ${pr.error}`);
  if (!reviews.ok) throw new Error(`#${n}: ${reviews.error}`);
  if (!comments.ok) throw new Error(`#${n}: ${comments.error}`);
  if (!issue.ok) throw new Error(`#${n}: ${issue.error}`);
  const raw: RawPr = { pr: pr.value, reviews: reviews.items, reviewComments: comments.items, issueComments: issue.items, runs: {} };
  for (const sha of new Set(raw.reviews.map((r) => r.commit_id))) {
    const runs = await ghJson<{ workflow_runs: RawPr["runs"][string] }>(`repos/${repo}/actions/runs?head_sha=${sha}&per_page=50`);
    raw.runs[sha] = runs.ok ? runs.value.workflow_runs : [];
  }
  return raw;
}

export function readFixture(dir: string): RawPr {
  const read = (f: string) => JSON.parse(readFileSync(join(dir, f), "utf8"));
  const runs: RawPr["runs"] = {};
  for (const f of readdirSync(dir)) {
    const m = /^runs-([0-9a-f]+)\.json$/.exec(f);
    if (m) runs[m[1] as string] = read(f).workflow_runs;
  }
  return { pr: read("pr.json"), reviews: read("reviews.json"), reviewComments: read("review-comments.json"), issueComments: read("issue-comments.json"), runs };
}

export const PAIR_COLUMNS = ["pr", "commit", "wachiman_review", "wachiman_version", "wachiman_model", "wachiman_effort", "wachiman_cost_usd", "wachiman_findings", "other_tool", "other_review", "other_findings", "minutes_apart"] as const;
export const SPECIAL_COLUMNS = ["pr", "commit", "tool", "status", "version", "reason", "action"] as const;
export const REVIEW_COLUMNS = ["pr", "tool", "commit", "review_id", "submitted_at", "status", "reason", "scope", "version", "model", "effort", "cost_usd", "findings", "url"] as const;
export const FINDING_COLUMNS = ["id", "pr", "tool", "commit", "comparison", "review_id", "comment_id", "placement", "path", "line", "severity", "topic", "confidence", "native_severity", "native_category", "native_tags", "title", "url"] as const;

export function summaryMarkdown(repo: string, other: Other, pairs: PairRow[], specials: SpecialCase[], findings: FindingRecord[], reviews: ReviewRecord[]): string {
  const money = (n: number | null) => (n === null ? "" : `$${n.toFixed(2)}`);
  const short = (s: string) => s.slice(0, 7);
  const on = (tool: Tool) => findings.filter((f) => f.comparison === "paired" && f.tool === tool).length;
  return [
    `# Pairs: Wachiman vs ${other} on ${repo}`, "",
    "Generated by `scripts/pair.ts`; do not edit. A pair is one commit both tools completed. Findings on paired commits are the comparable set; everything else is a special case.", "",
    `- Pull requests: ${new Set(reviews.map((r) => r.pr)).size}. Pairs: ${pairs.length}. Special cases: ${specials.length}.`,
    `- Comparable findings: Wachiman ${on("wachiman")}, ${other} ${on(other)}.`,
    `- Wachiman cost on pairs: ${money(pairs.reduce((s, p) => s + (p.wachiman_cost_usd ?? 0), 0))}. ${other} cost: ${other === "pullfrog" ? "from its posts where present" : "not published by the tool"}.`,
    `- Wachiman versions seen: ${[...new Set(reviews.filter((r) => r.tool === "wachiman" && r.version).map((r) => r.version))].join(", ") || "unknown"}.`, "",
    "## Pairs", "",
    `| PR | Commit | Wachiman version | Model · effort | Wachiman cost | Wachiman findings | ${other} findings | Minutes apart |`,
    "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ...pairs.map((p) => `| #${p.pr} | \`${short(p.commit)}\` | ${p.wachiman_version || "?"} | ${p.wachiman_model} · ${p.wachiman_effort} | ${money(p.wachiman_cost_usd)} | ${p.wachiman_findings} | ${p.other_findings} | ${p.minutes_apart} |`),
    "", "## Special cases (not compared)", "",
    "| PR | Commit | Tool | Status | Version | Reason | What would make it comparable |", "| --- | --- | --- | --- | --- | --- | --- |",
    ...specials.map((s) => `| #${s.pr} | \`${short(s.commit)}\` | ${s.tool} | ${s.status} | ${s.version} | ${s.reason} | ${s.action} |`),
    "",
  ].join("\n");
}

function parseArgs(argv: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i] as string;
    if (!a.startsWith("--")) continue;
    const next = argv[i + 1];
    out[a.slice(2)] = next !== undefined && !next.startsWith("--") ? (argv[++i] as string) : "true";
  }
  return out;
}

export function expandPrs(spec: string): number[] {
  const out: number[] = [];
  for (const part of spec.split(",")) {
    const m = /^(\d+)(?:-(\d+))?$/.exec(part.trim());
    if (!m) throw new Error(`bad --prs part: ${part}`);
    for (let n = Number(m[1]); n <= Number(m[2] ?? m[1]); n++) out.push(n);
  }
  return out;
}

export function run(raws: RawPr[], other: Other) {
  const per = raws.map((raw) => {
    const w = wachimanReviews(raw);
    const o = otherReviews(raw, other);
    return { reviews: [...w.reviews, ...o.reviews], findings: [...w.findings, ...o.findings] };
  });
  return { ...pair(per, other), reviews: per.flatMap((p) => p.reviews) };
}

if (import.meta.main) {
  const args = parseArgs(process.argv.slice(2));
  const other = (args.other ?? "coderabbit") as Other;
  if (!(other in OTHER_LOGIN)) throw new Error(`--other must be one of ${Object.keys(OTHER_LOGIN).join(", ")}`);
  const out = args.out ?? ".";
  let repo = args.repo ?? "";
  let raws: RawPr[];
  if (args.fixtures) {
    raws = readdirSync(args.fixtures).filter((d) => d.startsWith("pr-")).sort().map((d) => readFixture(join(args.fixtures as string, d)));
    repo ||= "fixtures";
  } else {
    if (!repo || !args.prs) throw new Error("need --repo owner/name and --prs a-b[,c]");
    raws = [];
    for (const n of expandPrs(args.prs)) {
      console.error(`fetching #${n}`);
      raws.push(await fetchPr(repo, n));
    }
  }
  const { pairs, specials, findings, reviews } = run(raws, other);
  mkdirSync(out, { recursive: true });
  const csv = (cols: readonly string[], rows: object[]) => toCsv(cols, rows as Record<string, unknown>[]);
  writeFileSync(join(out, "pairs.csv"), csv(PAIR_COLUMNS, pairs));
  writeFileSync(join(out, "special-cases.csv"), csv(SPECIAL_COLUMNS, specials));
  writeFileSync(join(out, "reviews.csv"), csv(REVIEW_COLUMNS, reviews));
  writeFileSync(join(out, "findings.csv"), csv(FINDING_COLUMNS, findings));
  writeFileSync(join(out, "pairs.md"), summaryMarkdown(repo, other, pairs, specials, findings, reviews));
  console.error(`${pairs.length} pairs, ${specials.length} special cases, ${findings.length} findings → ${out}`);
}
