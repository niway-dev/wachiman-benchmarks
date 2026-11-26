import { expect, test } from "bun:test";
import { knownBugs, normaliseSeverity, pickPrimary } from "./known-bugs.ts";

const md = (rows: string[]) =>
  ["## Expected issues", "", "| ID | Issue | Severity | W34 |", "|---|---|---|---|", ...rows, "", "## Additional", "", "| ID | Issue | Severity |", "|---|---|---|", "| A1 | x | Low |"].join("\n");

test("one row per E id, title trimmed, severity normalised, other tables ignored", () => {
  const rows = knownBugs(md(["| E1 |  No re-list  | medium | yes |", "| E2 | Pick `a\\|b` | LOW | no |", "| A9 | not expected | Low | no |"]), "d", "467");
  expect(rows).toEqual([
    { original_pr: "467", id: "E1", severity: "Medium", title: "No re-list", doc: "d" },
    { original_pr: "467", id: "E2", severity: "Low", title: "Pick `a|b`", doc: "d" },
  ]);
});

test("an Expected table without a Severity column gives no rows", () => {
  const m = ["## Expected issues", "", "| ID | Issue | W4 |", "|---|---|---|", "| E1 | A | yes |"].join("\n");
  expect(knownBugs(m, "d", "463")).toEqual([]);
});

test("severity words map to High/Medium/Low/Info", () => {
  expect(["high", "Medium", " low ", "INFO"].map(normaliseSeverity)).toEqual(["High", "Medium", "Low", "Info"]);
  expect(normaliseSeverity("Critical")).toBeNull();
});

test("the newest doc with rows is primary; a disagreement on an id's severity is a warning", () => {
  const old = knownBugs(md(["| E1 | A | High | yes |", "| E2 | B | Low | no |"]), "old", "465");
  const neu = knownBugs(md(["| E1 | A | Medium | yes |", "| E2 | B | Low | no |"]), "new", "465");
  const { rows, warnings } = pickPrimary([old, neu]);
  expect(rows.map((r) => [r.id, r.severity, r.doc])).toEqual([["E1", "Medium", "new"], ["E2", "Low", "new"]]);
  expect(warnings).toEqual(["PR 465 E1: old says High, new (primary) says Medium"]);
});
