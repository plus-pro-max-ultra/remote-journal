"""Rebuild only the archive month selector from actual article rows. No category fallback."""
from pathlib import Path
from bs4 import BeautifulSoup as B
import re,sys
p=Path(sys.argv[1]);z=B(p.read_text(),'html.parser');select=z.select_one('#archiveMonthSelect');assert select is not None
months=sorted({x['data-month'] for x in z.select('.topic-row[data-month]')},reverse=True)
assert all(re.fullmatch(r'\d{4}-\d{2}',x) for x in months)
select.clear()
for value,label in [('all','全部月份')]+[(m,f'{m[:4]} 年 {int(m[5:])} 月') for m in months]:
 op=z.new_tag('option',value=value);op.string=label;select.append(op)
p.write_text(str(z))
assert [x['value'] for x in B(p.read_text(),'html.parser').select('#archiveMonthSelect option')]==['all']+months
