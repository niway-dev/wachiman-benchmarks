import { expect, test } from "bun:test";
import { parseCsv } from "./indicators.ts";

test("parseCsv keeps quoted commas, doubled quotes and embedded newlines in one field", () => {
  const rows = parseCsv('id,title\n1,"a, b"\n2,"say ""hi"""\n3,"line\none"\n');
  expect(rows).toEqual([
    { id: "1", title: "a, b" },
    { id: "2", title: 'say "hi"' },
    { id: "3", title: "line\none" },
  ]);
});

test("parseCsv pads a short row with empty fields and skips blank lines", () => {
  expect(parseCsv("a,b,c\n1,2\n\n")).toEqual([{ a: "1", b: "2", c: "" }]);
});
