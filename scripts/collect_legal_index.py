from collect_sources import ROOT, Links
import urllib.request, json, re, concurrent.futures, html
from urllib.parse import urljoin

BASE='https://normograma.dian.gov.co/dian/compilacion/'
groups=[('a_1_normativa_aduanera','Norma','leyes'),('a_2_doctrina_aduanera','Doctrina','doctrina'),('a_3_jurisprudencia_aduanera','Jurisprudencia','jurisprudencia')]
jobs=[]
for stem,kind,file in groups:
 raw=(ROOT/'sources'/f'{file}.html').read_bytes()
 try:raw=raw.decode('utf-8')
 except UnicodeDecodeError:raw=raw.decode('cp1252')
 titles=re.findall(r'<div class="titulo-opcion-nueva">(.*?)</div>',raw,re.S)
 for i,title in enumerate(titles,1):
  if 'href=' in title:continue
  title=html.unescape(re.sub('<.*?>','',title)).strip()
  jobs.append((BASE+f'{stem}_parte_{i:02}.html',kind,title))

def fetch(job):
 url,kind,group=job
 try:
  data=urllib.request.urlopen(url,timeout=45).read()
  try:raw=data.decode('utf-8')
  except UnicodeDecodeError:raw=data.decode('cp1252')
  (ROOT/'sources'/url.rsplit('/',1)[-1]).write_text(raw,encoding='utf-8')
  p=Links();p.feed(raw)
  out=[]
  for a in p.links:
   dest=urljoin(url,a['url'])
   if '/docs/' in dest and a['title'].strip():out.append({'title':' '.join(a['title'].split()),'url':dest,'type':kind,'group':group,'sourceIndex':url})
  return {'url':url,'type':kind,'group':group,'links':out}
 except Exception as e:return {'url':url,'error':str(e),'links':[]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,jobs))
(ROOT/'sources/legal-index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Indexes:',len(results),'document references:',sum(len(r['links']) for r in results),'errors:',[r['url'] for r in results if 'error' in r])
