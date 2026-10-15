import json, re, shutil, datetime
from pathlib import Path
R = Path(__file__).resolve().parent
D = R / 'dist'
# flat mode: files named a__b__c.txt are placed at a/b/c.txt (phone upload me folders nahi bante)
for p in list(R.iterdir()):
    if p.is_file() and '__' in p.name:
        t = R.joinpath(*p.name.split('__'))
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(p), str(t))
vk = lambda s: tuple(int(x) for x in re.findall(r'\d+', s))
if D.exists():
    shutil.rmtree(D)
D.mkdir()
SW = """const C='%s';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['./','index.html','manifest.webmanifest']).catch(()=>{})))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=C).map(x=>caches.delete(x)))).then(()=>clients.claim()))});
self.addEventListener('fetch',e=>{if(e.request.method!='GET')return;e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(C).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request)))});
"""
REG = '<script>if("serviceWorker"in navigator){var had=!!navigator.serviceWorker.controller,done=0;navigator.serviceWorker.register("sw.js");navigator.serviceWorker.addEventListener("controllerchange",function(){if(had&&!done){done=1;location.reload()}})}</script>'
reg = []
for a in sorted((R / 'apps').iterdir()):
    mf = a / 'app.json'
    if not mf.exists():
        continue
    m = json.loads(mf.read_text(encoding='utf-8'))
    vdir = a / 'versions'
    vs = sorted([v for v in vdir.iterdir() if (v / 'index.html').exists()], key=lambda p: vk(p.name)) if vdir.exists() else []
    if not vs:
        continue
    L = vs[-1]
    ver = L.name
    out = D / a.name
    shutil.copytree(L, out, ignore=shutil.ignore_patterns('notes.txt'))
    for ic in ('icon-192.png', 'icon-512.png'):
        if (a / ic).exists():
            shutil.copy(str(a / ic), str(out / ic))
    h = (out / 'index.html').read_text(encoding='utf-8')
    head = '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="%s"><link rel="icon" href="icon-192.png"></head>' % m.get('theme', '#6c4cff')
    h = h.replace('</head>', head, 1).replace('</body>', REG + '</body>', 1)
    (out / 'index.html').write_text(h, encoding='utf-8')
    man = {'name': m['name'], 'short_name': m.get('short_name', m['name']), 'description': m.get('description', ''),
           'start_url': './', 'scope': './', 'display': 'standalone',
           'background_color': m.get('bg', '#ffffff'), 'theme_color': m.get('theme', '#6c4cff'),
           'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
                     {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}]}
    (out / 'manifest.webmanifest').write_text(json.dumps(man), encoding='utf-8')
    (out / 'sw.js').write_text(SW % (a.name + '-' + ver), encoding='utf-8')
    notes = (L / 'notes.txt').read_text(encoding='utf-8').strip() if (L / 'notes.txt').exists() else ''
    (out / 'version.json').write_text(json.dumps({'version': ver}), encoding='utf-8')
    reg.append({'id': a.name, 'name': m['name'], 'description': m.get('description', ''), 'version': ver,
                'notes': notes, 'updated': datetime.date.today().isoformat()})
    print('built', a.name, ver, '(%d versions in repo)' % len(vs))
(D / 'registry.json').write_text(json.dumps(reg), encoding='utf-8')
shutil.copy(str(R / 'hub' / 'index.html'), str(D / 'index.html'))
wk = R / 'well-known'
if wk.exists():
    shutil.copytree(wk, D / '.well-known')
