from pathlib import Path
import json,importlib.metadata,tiktoken
r=Path(__file__).resolve().parent;expected=json.loads((r/'token-demo.json').read_text());assert importlib.metadata.version('tiktoken')==expected['version'],'Use the recorded tiktoken version'
for row in expected['results']:
 for name,result in row['encodings'].items():
  e=tiktoken.get_encoding(name);ids=e.encode(row['text']);assert ids==result['ids'];assert len(ids)==result['count'];assert e.decode(ids)==row['text'];assert [e.decode_single_token_bytes(i).hex() for i in ids]==result['token_bytes_hex']
print('All four plain-text examples reproduce exactly in both recorded encodings. This is not an API usage count or language benchmark.')
