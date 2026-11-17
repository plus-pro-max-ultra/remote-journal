"""Record validation only. No publication, image quota or new approval rule."""
from pathlib import Path
import json,sys,subprocess
r=Path(sys.argv[1]);errors=[]
x=subprocess.run([sys.executable,str(Path(__file__).with_name('check_editorial_learning.py')),str(r)],check=False)
if x.returncode:errors.append('owner-edit learning record')
try:
 d=json.loads((r/'visual-assessment.json').read_text())
 assert d['status']=='complete', 'visual assessment is '+d['status']
 assert d['assessed_at'] and d['visual_role']
 inv=d['investigation'];assert inv['performed'] and inv['searches'], 'no actual investigation'
 for s in inv['searches']:
  assert s['query_or_source'] and s['checked_at'] and s['result_summary']
 for c in d['candidates']:
  assert c['url'].startswith('https://') and c['relevance'] and c['decision'] and c['reason']
  rights=c['rights'];assert rights['status'] in ['verified','unknown','restricted']
  if c['decision']=='selected':
   assert rights['status']=='verified' and rights['source_url'] and rights['license'] and rights['credit']
   assert c['caption'] and c['alt'] and c['layout']
 dec=d['decision'];assert dec['outcome'] in ['photos','original_visual','no_image'] and dec['rationale']
 if dec['outcome']=='photos':
  selected=[c['url'] for c in d['candidates'] if c['decision']=='selected']
  assert selected and set(selected)==set(dec['selected_candidate_urls'])
 if dec['outcome']!='no_image':assert d['verification']['pixels']=='inspected' and d['verification']['evidence']
 assert not d['unresolved'], 'unresolved visual items'
 print('Visual-assessment record complete; this does not judge visual quality or license interpretation.')
except (AssertionError,KeyError,FileNotFoundError) as e:errors.append('visual assessment: '+str(e))
if errors:
 print('NOT COMPLETE: '+'; '.join(errors));sys.exit(1)
print('Both records complete. This is not a publication authorization or an automated editorial-quality verdict.')
