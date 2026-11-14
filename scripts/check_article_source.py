from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[1]
paths=[*root.glob("articles/0*/index.html"),*root.glob("review/*/index.html")]
bad=[]
for p in paths:
 s=p.read_text();a=s.index("<article");b=s.index("</article>",a)
 for no,line in enumerate(s[a:b].splitlines(),1):
  if re.search(r"</(?:p|h[1-6]|figure|blockquote)>[ \t]*<(?:p|h[1-6]|figure|blockquote)(?:\s|>)",line):bad.append(f"{p.relative_to(root)}:{no}")
if bad:raise SystemExit("Content blocks share lines: "+", ".join(bad))
print(f"Readable source verified: {len(paths)} article/review pages")
