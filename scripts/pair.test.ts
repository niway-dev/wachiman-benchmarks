import { describe, expect, test } from "bun:test";
import { join } from "node:path";
import { expandPrs, pair, readFixture, run, versionFromRuns } from "./pair.ts";

const FIX = join(import.meta.dir, "fixtures", "pair");
const load = (n: number) => readFixture(join(FIX, `pr-${n}`));

describe("pairing by commit", () => {
  test("#535: one commit both tools completed is one pair, with version, model, effort and cost from Wachiman", () => {
    const { pairs, specials } = run([load(535)], "coderabbit");
    expect(pairs).toHaveLength(1);
    const p = pairs[0]!;
    expect(p.commit).toBe("1fb882cd7b110cb57ca84893802d50978e3ba26d");
    expect(p.wachiman_version).toBe("v1.7.0"); // the run referenced v1.7.0 although v1.8.0 was released that night
    expect(p.wachiman_model).toBe("Claude Opus 5.5");
    expect(p.wachiman_effort).toBe("high");
    expect(p.wachiman_cost_usd).toBe(0.51);
    expect(p.wachiman_findings).toBe(2); // one inline, one outside the diff
    expect(p.other_findings).toBe(1); // one comment that bundles two points; the judge splits it
    expect(p.minutes_apart).toBe(4);
    expect(specials).toHaveLength(0);
  });

  test("#534: Wachiman refused three times for no credit, so CodeRabbit's reviews are unpaired, and nothing is compared", () => {
    const { pairs, specials, findings } = run([load(534)], "coderabbit");
    expect(pairs).toHaveLength(0);
    expect(specials.filter((s) => s.tool === "wachiman" && s.status === "refused")).toHaveLength(3);
    expect(specials.find((s) => s.status === "refused")?.reason).toMatch(/no credit/);
    expect(specials.filter((s) => s.tool === "coderabbit" && s.status === "unpaired").length).toBeGreaterThan(0);
    expect(findings.every((f) => f.comparison === "special")).toBe(true);
    expect(findings.find((f) => f.tool === "coderabbit")?.native_severity).toBe("Major");
  });

  test("#540: CodeRabbit skipped on path filters and Wachiman was partial, so every row is special", () => {
    const { pairs, specials, findings } = run([load(540)], "coderabbit");
    expect(pairs).toHaveLength(0);
    expect(specials.find((s) => s.tool === "coderabbit")?.status).toBe("skipped");
    expect(specials.find((s) => s.tool === "coderabbit")?.reason).toMatch(/path filters/);
    expect(specials.filter((s) => s.tool === "wachiman").every((s) => s.status === "partial")).toBe(true);
    expect(findings.filter((f) => f.tool === "wachiman")).toHaveLength(15);
    expect(findings.every((f) => f.comparison === "special")).toBe(true);
  });

  test("a completed review by one tool on a commit the other never touched is unpaired, with the reason", () => {
    const w = { pr: 1, tool: "wachiman" as const, commit: "a", review_id: 1, submitted_at: "2026-11-06T00:00:00Z", url: "", status: "completed" as const, reason: "", scope: "", version: "v1.8.0", model: "m", effort: "high", cost_usd: 0.1, findings: 0 };
    const { pairs, specials } = pair([{ reviews: [w], findings: [] }], "coderabbit");
    expect(pairs).toHaveLength(0);
    expect(specials[0]).toMatchObject({ status: "unpaired", reason: "coderabbit never reviewed this commit" });
  });
});

describe("helpers", () => {
  test("the version is the latest tagged run started before the review", () => {
    const runs = [
      { id: 1, name: "Agent review", conclusion: "success", created_at: "2026-11-06T00:30:00Z", referenced_workflows: [{ ref: "refs/tags/v1.7.0" }] },
      { id: 2, name: "Agent review", conclusion: "success", created_at: "2026-11-06T03:00:00Z", referenced_workflows: [{ ref: "refs/tags/v1.8.0" }] },
      { id: 3, name: "PR checks", conclusion: "success", created_at: "2026-11-06T00:31:00Z", referenced_workflows: [] },
    ];
    expect(versionFromRuns(runs, "2026-11-06T00:36:00Z")).toBe("v1.7.0");
    expect(versionFromRuns(runs, "2026-11-06T03:05:00Z")).toBe("v1.8.0");
    expect(versionFromRuns(undefined, "2026-11-06T03:05:00Z")).toBe("");
  });

  test("--prs accepts ranges and lists", () => {
    expect(expandPrs("534-536,540")).toEqual([534, 535, 536, 540]);
    expect(() => expandPrs("x")).toThrow();
  });
});
