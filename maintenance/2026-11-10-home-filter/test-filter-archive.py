import subprocess,time,json,urllib.request,websocket,functools,http.server,threading,base64,os,sys
from pathlib import Path
live='--live' in sys.argv
out=Path('/downloads/home-filter-live' if live else '/downloads/home-filter-local');out.mkdir(exist_ok=True,parents=True)
server=http.server.ThreadingHTTPServer(('127.0.0.1',8765),functools.partial(http.server.SimpleHTTPRequestHandler,directory='/tmp/zine-gh-20261106'));thread=threading.Thread(target=server.serve_forever);thread.start()
p=subprocess.Popen(['google-chrome-stable','--headless','--no-sandbox','--disable-gpu','--remote-allow-origins=*','--remote-debugging-port=9229','--user-data-dir=/tmp/chromefilter2216'+str(live),'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
try:
 for _ in range(80):
  try:tabs=json.load(urllib.request.urlopen('http://127.0.0.1:9229/json'));break
  except:time.sleep(.1)
 ws=websocket.create_connection(next(x for x in tabs if x['type']=='page')['webSocketDebuggerUrl']);n=0
 def call(m,params={}):
  global n;n+=1;ws.send(json.dumps(dict(id=n,method=m,params=params)))
  while True:
   a=json.loads(ws.recv())
   if a.get('id')==n:return a
 def js(s):
  a=call('Runtime.evaluate',dict(expression=s,returnByValue=True))['result']
  if 'exceptionDetails' in a:raise RuntimeError(a)
  return a['result'].get('value')
 call('Network.enable');call('Network.setCacheDisabled',dict(cacheDisabled=True));call('Network.setBypassServiceWorker',dict(bypass=True));results=[]
 for width in [320,390,1440]:
  call('Emulation.setDeviceMetricsOverride',dict(width=width,height=1000,deviceScaleFactor=1,mobile=width<500))
  call('Page.navigate',dict(url='https://plus-pro-max-ultra.github.io/remote-journal/archive/?filtercheck=2220' if live else 'http://127.0.0.1:8765/archive/'))
  for _ in range(200):
   if js('document.readyState==="complete" && document.querySelectorAll(".topic-row[data-id]").length>20'):break
   time.sleep(.05)
  def ac(name,action,expected):
   js(action);time.sleep(.05)
   ids=json.loads(js('JSON.stringify([...document.querySelectorAll(".topic-row[data-id]")].filter(x=>getComputedStyle(x).display!=="none").map(x=>x.dataset.id))'));assert sorted(ids)==sorted(expected),(width,name,ids,expected)
   results.append(dict(width=width,test='archive-'+name,ids=ids))
  ac('default','document.querySelector("#archiveClear").click()',js('[...document.querySelectorAll(".topic-row[data-id]")].map(x=>x.dataset.id)'))
  ac('search','document.querySelector("#archiveSearchInput").value="天花";document.querySelector("#archiveSearchInput").dispatchEvent(new Event("input"))',['008-smallpox'])
  ac('query-category-zero','document.querySelector("#archiveFilters [data-afilter=科學與日常]").click()',[])
  ac('reset','document.querySelector("#archiveClear").click()',js('[...document.querySelectorAll(".topic-row[data-id]")].map(x=>x.dataset.id)'))
  ac('history','document.querySelector("#archiveFilters [data-afilter=歷史與制度]").click()',['018-seven-day-week','010-daylight-saving-time','003-imperial'])
 print('PASS',len(results),'checks');(out/'archive-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 call('Browser.close');ws.close()
finally:
 try:os.killpg(p.pid,15)
 except:pass
 p.wait();server.shutdown();thread.join();server.server_close()
