# audit.py: writes raw/audit.tsv, one row per finding of every run, with the verdict reached by
# reading the code at the push's head (see README, "How the findings were checked").
# KEY maps (case, file:line) to the audited finding it matches; VERDICT gives the other findings.
import json, glob, os, csv
KEY = {("478-64db30b", "workspaces-context.tsx:167"): "F18", ("478-392778f", "workspaces-context.tsx:168"): "F20",
       ("478-392778f", "registry.ts:724"): "F21", ("478-392778f", "registry.ts:718"): "F21", ("483-0253fd7", "index.ts:755"): "F17",
       ("484-59f6d48", "reconcile-dialog.tsx:216"): "F2"}
# Not audited by the field audit; checked against the code for this study.
VERDICT = {
 ("478-64db30b", "registry.ts:684"): ("valid", "probe reads identity.json, awaits, then rewrites it; no lock covers the file write"),
 ("478-64db30b", "registry.ts:848"): ("invalid", "asks if a no-identity folder is intended; the code comment at the branch already says why"),
 ("478-64db30b", "registry.ts:836"): ("valid", "checkRelocate returns `different` where availability() would adopt the id"),
 ("478-64db30b", "registry.ts:629"): ("valid", "name-only offline edit sets pendingIdentity and drops pendingColorUpgrade; the cached color then overwrites the file"),
 ("478-64db30b", "registry.ts:821"): ("valid", "doc says only identity-carrying folders qualify; the pendingInit branch accepts one without"),
 ("478-392778f", "registry.ts:189"): ("valid", "`unchanged` is declared on the registry type; only relocate.ts:44 sets it"),
 ("479-413ee15", "2026-10-29-several-workspaces-design.md:1302"): ("valid", "relocate row lists only recording/export; a group move refuses it too"),
 ("479-413ee15", "relocate-copy.ts:36"): ("valid", "no test covers the `moving` branch"),
 ("479-413ee15", "workspace-dialog.test.tsx:328"): ("valid", "`moving` appears in no relocate dialog test"),
 ("479-413ee15", "workspace-dialog.test.tsx:321"): ("valid", "same as :328"),
 ("479-413ee15", "several-workspaces.md:26"): ("valid", "paragraph says refused only while a recording or export runs"),
 ("479-413ee15", "several-workspaces.md:9"): ("valid", "banner says nothing is implemented"),
 ("479-413ee15", "2026-10-29-several-workspaces-design.md:1307"): ("valid", "row ends 'a group of single moves' with no predicate"),
 ("479-413ee15", "2026-10-29-several-workspaces-design.md:1298"): ("valid", "switch returns the busy value (recording/exporting/moving) and also unknown/read-only, not 'busy'"),
 ("479-413ee15", "workspaces.ts:253"): ("valid", "refuse-all comment lists busy/stale/maintenance; refusalOfError can also give `io`"),
 ("482-ad0fa5c", "index.ts:608"): ("valid", "relocateFolder never calls workspaceSettings.refresh; afterCommit now rebroadcasts the old cache"),
 ("482-ad0fa5c", "index.ts:406"): ("valid", "same as :608"),
 ("482-ad0fa5c", "index.ts:427"): ("valid", "refresh() calls changed() before the commit when overrides differ; low impact, as the finding says"),
 ("483-0253fd7", "index.ts:756"): ("valid", "availabilityOf returns at :179 without clearing `unverified`"),
 ("483-0253fd7", "index.ts:762"): ("valid", "no test file references relocateFolder or the refresh"),
 ("484-59f6d48", "reconcile-dialog.tsx:216*"): ("valid", "any non-empty selection suppresses the toggle (code at :216)"),
 ("484-59f6d48", "reconcile.test.tsx:374"): ("valid", "mockRestore() runs after the assertions, not in a finally"),
 ("484-59f6d48", "reconcile.test.tsx:369"): ("valid", "same as :374"),
 ("484-59f6d48", "reconcile.test.tsx:368"): ("valid", "same as :374"),
}
rows = []
for d in sorted(glob.glob("raw/runs/*/*")):
    if not os.path.isdir(d): continue
    case, arm = d.split("/")[-2:]
    for r in sorted(glob.glob(d + "/result-*.json")):
        for f in (json.load(open(r)).get("structuredOutput") or {}).get("findings") or []:
            loc = f"{f['path'].split('/')[-1]}:{f['line']}"
            if case == "484-59f6d48" and loc == "reconcile-dialog.tsx:216" and "selection" in f["title"].lower():
                rows.append((case, arm, loc, f["title"], "", "valid: any non-empty selection suppresses the toggle (code at :216)")); continue
            if (case, loc) in KEY: rows.append((case, arm, loc, f["title"], KEY[(case, loc)], "key")); continue
            v = VERDICT.get((case, loc)) or VERDICT.get((case, loc + "*"))
            if case == "484-59f6d48" and loc == "reconcile-dialog.tsx:216":
                v = ("valid", "any non-empty selection suppresses the toggle") if "selection" in f["title"].lower() else None
            if v is None: v = ("UNCHECKED", "")
            rows.append((case, arm, loc, f["title"], "", v[0] + ": " + v[1]))
with open("raw/audit.tsv", "w") as out:
    out.write("case\tarm\tlocation\ttitle\taudited_id\tverdict\n")
    for r in rows: out.write("\t".join(r) + "\n")
print(len(rows), "findings;", sum(1 for r in rows if r[5].startswith("UNCHECKED")), "unchecked")
