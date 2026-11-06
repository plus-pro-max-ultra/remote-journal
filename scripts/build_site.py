#!/usr/bin/env python3
"""Validate and package the approved directly edited website. Do not regenerate it from legacy templates."""
from pathlib import Path
import shutil,json,re
ROOT=Path(__file__).resolve().parents[1]
def main():
    files=['404.html','about','archive','articles','assets','favicon-16.png','favicon-32.png','feed.xml','icon-180.png','icon-192.png','icon-512.png','index.html','manifest.webmanifest','preview','privacy','robots.txt','sitemap.xml','stories.js','sw.js','article-identifiers.json']
    mapping=json.loads((ROOT/'article-identifiers.json').read_text())['aliases']
    for old,new in mapping.items():
        assert (ROOT/'articles'/new/'index.html').is_file(),new
        assert (ROOT/'articles'/old/'index.html').is_file(),old
    stories_text=(ROOT/'stories.js').read_text()
    stories=json.loads(stories_text[stories_text.index('['):].strip().rstrip(';'))
    assert len(stories)==18
    assert len({story['id'] for story in stories})==18
    for story in stories:
        page=(ROOT/'articles'/story['id']/'index.html').read_text()
        assert 'reader-body' in page and 'class="sources"' in page,story['id']
        assert '品質控管' not in page,story['id']
        assert 'https://journal-for-far.learnman.workers.dev/articles/'+story['id']+'/' in page,story['id']
    for filename in ['feed.xml','sitemap.xml']:
        assert '017-antibiotic-course' in (ROOT/filename).read_text()
        assert '018-seven-day-week' in (ROOT/filename).read_text()
    out=ROOT/'dist'
    if out.exists():shutil.rmtree(out)
    out.mkdir()
    for name in files:
        p=ROOT/name
        if p.is_dir():shutil.copytree(p,out/name)
        else:shutil.copy2(p,out/name)
    (out/'.nojekyll').write_text('')
    print('Confirmed direct-edit website validated and packaged; issues001–018 readable.')
    return 0
if __name__=='__main__':raise SystemExit(main())
