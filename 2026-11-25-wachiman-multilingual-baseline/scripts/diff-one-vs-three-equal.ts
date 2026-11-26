import { readdirSync, readFileSync, existsSync } from "node:fs"; import { join } from "node:path";
const DIFF = ["-c","diff.suppressBlankEmpty=false","diff","-M","--no-ext-diff","--no-textconv","--no-color","--no-relative","--src-prefix=a/","--dst-prefix=b/","--diff-algorithm=default","--indent-heuristic","-O/dev/null"];
const PATCH = ["--inter-hunk-context=1","-U3"];
const git = (d: string, a: string[]) => Bun.spawnSync(["git","-C",d,...a],{maxBuffer:1<<30}).stdout as Buffer;
let same=0, diff=0;
for (const id of readdirSync(process.argv[2] ?? "/tmp/classify-bench")) { const d=join(process.argv[2] ?? "/tmp/classify-bench",id); if(!existsSync(join(d,".base"))) continue;
  const b=readFileSync(join(d,".base"),"utf8").trim(), h=readFileSync(join(d,".head"),"utf8").trim();
  const raw=git(d,[...DIFF,"--raw","-z",b,h]), num=git(d,[...DIFF,"--numstat","-z",b,h]), pat=git(d,[...DIFF,...PATCH,b,h]);
  const one=git(d,[...DIFF,...PATCH,"--raw","--numstat","-z",b,h]);
  // In the combined output, the patch follows a NUL-terminated separator; compare the patch tail and the stat head.
  const i=one.indexOf("diff --git"); const head=one.subarray(0,i), tail=one.subarray(i);
  const patchSame = tail.equals(pat), headSame = head.equals(Buffer.concat([raw,num])) || head.subarray(0,raw.length).equals(raw);
  if (patchSame && headSame) same++; else { diff++; if (diff<3) console.log(id, "patchSame", patchSame, "headSame", headSame, head.length, raw.length+num.length); }
}
console.log("same", same, "different", diff);
