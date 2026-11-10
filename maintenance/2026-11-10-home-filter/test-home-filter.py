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
  call('Page.navigate',dict(url='https://plus-pro-max-ultra.github.io/remote-journal/?filtercheck=2216' if live else 'http://127.0.0.1:8765/'))
  for _ in range(200):
   if js('document.readyState==="complete" && document.querySelectorAll("#filters button").length>2'):break
   time.sleep(.05)
  js('localStorage.setItem("faraway-saved",JSON.stringify(["024-humidity","021-kilogram"]))')
  def check(name,action,expr,screenshot=False):
   js(action);time.sleep(.05)
   v=js('JSON.stringify([...document.querySelectorAll("#articleGrid .article-card")].filter(x=>getComputedStyle(x).display!=="none").map(x=>x.dataset.id))');ids=json.loads(v);expect=js(expr);assert sorted(ids)==sorted(expect),(width,name,ids,expect)
   r=dict(width=width,test=name,visible=ids,expected=expect,scroll=js('document.documentElement.scrollWidth'));results.append(r)
   if screenshot and width in [390,1440]:
    js('document.documentElement.style.scrollBehavior="auto";document.querySelector("#archiveTitle").scrollIntoView({behavior:"instant"});scrollBy(0,-20)');time.sleep(.1);cap=call('Page.captureScreenshot',dict(format='png'))['result']['data'];(out/f'{name}-{width}.png').write_bytes(base64.b64decode(cap))
  check('default','document.querySelector("#clearSearch").click()','[...document.querySelectorAll("#articleGrid .article-card:not(.extra)")].map(x=>x.dataset.id)')
  js('localStorage.setItem("faraway-saved",JSON.stringify(["010-daylight-saving-time"]))')
  call('Page.reload',dict(ignoreCache=True))
  for _ in range(200):
   if js('document.readyState==="complete" && document.querySelectorAll("#filters button").length>2'):break
   time.sleep(.05)
  check('010-after-reload','document.querySelector("#savedNav").click()','["010-daylight-saving-time"]',True)
  check('010-clear','document.querySelector("#clearSearch").click()','[...document.querySelectorAll("#articleGrid .article-card:not(.extra)")].map(x=>x.dataset.id)')
  js('localStorage.setItem("faraway-saved",JSON.stringify(["024-humidity","021-kilogram"]))')
  check('category','document.querySelector(\'#filters [data-filter="科學與日常"]\').click()','["024-humidity"]',True)
  check('history',"document.querySelector('#filters [data-filter=\"歷史與制度\"]').click()",'["018-seven-day-week","010-daylight-saving-time","003-imperial"]')
  check('category-return',"document.querySelector('#filters [data-filter=\"科學與日常\"]').click()",'["024-humidity"]')
  check('category-zero','document.querySelector("#searchInput").value="不存在題目xyz";document.querySelector("#searchInput").dispatchEvent(new Event("input"))','[]',True)
  assert js('getComputedStyle(document.querySelector("#emptyResult")).display!=="none"')
  check('search-old','document.querySelector("#clearSearch").click();document.querySelector("#searchInput").value="天花";document.querySelector("#searchInput").dispatchEvent(new Event("input"))','["008-smallpox"]',True)
  check('saved','document.querySelector("#savedNav").click()','["024-humidity","021-kilogram"]',True)
  check('saved-category','document.querySelector(\'#filters [data-filter="科學與日常"]\').click()','["024-humidity"]')
  check('saved-category-query-zero','document.querySelector("#searchInput").value="公斤";document.querySelector("#searchInput").dispatchEvent(new Event("input"))','[]')
  check('clear-restore','document.querySelector("#clearSearch").click()','[...document.querySelectorAll("#articleGrid .article-card:not(.extra)")].map(x=>x.dataset.id)')
  check('single010-reload','localStorage.setItem("faraway-saved",JSON.stringify(["010-daylight-saving-time"]));document.querySelector("#savedNav").click()','["010-daylight-saving-time"]',True)
  check('single010-leave','document.querySelector("#savedNav").click()','[...document.querySelectorAll("#articleGrid .article-card:not(.extra)")].map(x=>x.dataset.id)')
  check('empty-favorites','localStorage.setItem("faraway-saved","[]");document.querySelector("#savedNav").click()','[]')
  check('return-default','document.querySelector("#savedNav").click()','[...document.querySelectorAll("#articleGrid .article-card:not(.extra)")].map(x=>x.dataset.id)')
 print('PASS',len(results),'checks');(out/'checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 call('Browser.close');ws.close()
finally:
 try:os.killpg(p.pid,15)
 except:pass
 p.wait();server.shutdown();thread.join();server.server_close()
