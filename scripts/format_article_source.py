"""Lossless source-only formatter for future Zine articles. Usage: script HTML..."""
from pathlib import Path
from bs4 import BeautifulSoup as B
import sys,re
pattern=r'(?<=>)(?=<(?:p(?:\s|>)|h[1-6](?:\s|>)|figure(?:\s|>)|/figure>|figcaption(?:\s|>)|/figcaption>|div(?:\s|>)|/div>|table(?:\s|>)|/table>|thead(?:\s|>)|tbody(?:\s|>)|tr(?:\s|>)|/tr>|ul(?:\s|>)|ol(?:\s|>)|li(?:\s|>)|blockquote(?:\s|>)|/blockquote>|section(?:\s|>)|/section>|details(?:\s|>)|/details>))'
def tree(s):
 d=B(s,'html.parser')
 for x in list(d.find_all(string=True)):
  if not x.strip():x.extract()
 return str(d)
for filename in sys.argv[1:]:
 p=Path(filename);s=p.read_text();a=s.index('<article');b=s.index('</article>',a);out=s[:a]+re.sub(pattern,'\n',s[a:b])+s[b:];assert out.replace('\n','')==s.replace('\n','');assert tree(out)==tree(s);p.write_text(out)
