import { expect, test } from "bun:test";
import { labelledRuns, parseReplayDoc, PRIMARY_DOC } from "./labels.ts";

test("a run that caught no expected issue is still a labelled run", () => {
  const md = [
    "## Expected issues",
    "",
    "| ID | Issue | W7 | W8 |",
    "|---|---|---|---|",
    "| E1 | A | yes | no |",
    "| E2 | B | partial | no |",
  ].join("\n");
  expect(labelledRuns(md, "doc", "463")).toEqual([
    { run_label: "W7", original_pr: "463", doc: "doc", expected_total: 2, expected_caught: ["E1"], expected_partial: ["E2"] },
    { run_label: "W8", original_pr: "463", doc: "doc", expected_total: 2, expected_caught: [], expected_partial: [] },
  ]);
});

test("two-digit run labels (W10…) are run columns", () => {
  const md = [
    "## Expected issues",
    "",
    "| ID | Issue | W9 | W10 |",
    "|---|---|---|---|",
    "| E1 | A | no | yes |",
  ].join("\n");
  expect(labelledRuns(md, "doc", "463").map((r) => [r.run_label, r.expected_caught])).toEqual([
    ["W9", []],
    ["W10", ["E1"]],
  ]);
});

test("the Sonnet baseline (W31-W33) and the 5-minute cache set (W34-W36) each have their own primary doc", () => {
  for (const l of ["W31", "W32", "W33"]) expect(PRIMARY_DOC[l]).toBe("2026-11-26-v1.21.0-sonnet-baseline");
  for (const l of ["W34", "W35", "W36"]) expect(PRIMARY_DOC[l]).toBe("2026-11-26-prompt-cache-5m");
});

test("the v1.22.0 Sonnet runs (W37-W39) have their own primary doc", () => {
  for (const x of ["W37", "W38", "W39"]) expect(PRIMARY_DOC[x]).toBe("2026-11-26-v1.22.0-sonnet");
});

test("the v1.22.0 doc's R1-R3 columns are W37-W39, and no other doc's R columns are", () => {
  const md = [
    "## Expected issues",
    "",
    "| ID | Issue | W31 | R1 | R2 | R3 |",
    "|---|---|---|---|---|---|",
    "| E1 | a | yes | yes | no | partial |",
    "| E2 | b | no | no | yes | no |",
  ].join("\n");
  const runs = labelledRuns(md, "2026-11-26-v1.22.0-sonnet", "463").map((r) => [r.run_label, r.expected_caught, r.expected_partial]);
  expect(runs).toEqual([["W31", ["E1"], []], ["W37", ["E1"], []], ["W38", ["E2"], []], ["W39", [], ["E1"]]]);
  expect(labelledRuns(md, "other-doc", "463").map((r) => r.run_label)).toEqual(["W31"]);
  const verdicts = parseReplayDoc(md, "2026-11-26-v1.22.0-sonnet", "463");
  expect([...(verdicts.find((v) => v.id === "E1")?.runs ?? [])].sort()).toEqual(["W31", "W37", "W39"]);
});
