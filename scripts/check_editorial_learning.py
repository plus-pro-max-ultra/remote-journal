from pathlib import Path
import sys,json,hashlib
r=Path(sys.argv[1]);d=json.loads((r/'editorial-learning-check.json').read_text())
for k in ['reviewed_at','compared_gh_commit','examples_version','checks','before_hashes','after_hashes']:assert d.get(k),k
assert d['full_text_reread'] and d['facts_and_limits_preserved'] and d['owner_text_untouched']
for c in d['checks']:
 for k in ['example','classification','location','decision','evidence']:assert c.get(k),k
for f,h in d['after_hashes'].items():assert hashlib.sha256((r/f).read_bytes()).hexdigest()==h, f+' changed after review'
assert not d['unresolved'], 'Unresolved items require separate review; not a passed learning check'
print('Editorial learning record complete and hashes current; this is not an automated language-quality verdict.')
