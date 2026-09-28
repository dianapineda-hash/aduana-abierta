from collect_sources import ROOT, Links
import urllib.request, urllib.parse, json, concurrent.futures, re

BASE='https://www.dian.gov.co/aduanas/Paginas/Inicio.aspx'
extra=[
 ('Estadísticas de comercio exterior','https://www.dian.gov.co/dian/cifras/Paginas/EstadisticasComEx.aspx'),
 ('Bases estadísticas de importaciones y exportaciones','https://www.dian.gov.co/dian/cifras/Paginas/Bases-Estadisticas-de-Comercio-Exterior-Importaciones-y-Exportaciones.aspx'),
 ('Histórico de estadísticas','https://www.dian.gov.co/dian/cifras/Paginas/Historico-estadisticas-de-comercio-exterior.aspx'),
]
raw=json.loads((ROOT/'sources/aduanas.json').read_text(encoding='utf-8'))
raw=raw[26:86]+json.loads((ROOT/'sources/normativa.json').read_text(encoding='utf-8'))[26:39]
pages=[(a['title'],a['url']) for a in raw if urllib.parse.urlsplit(a['url']).hostname=='www.dian.gov.co' and a['url'].lower().endswith('.aspx')]
pages+=extra

def collect(pair):
 title,url=pair
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)
  data=r.read().decode('utf-8','replace')
  if 'DeltaPlaceHolderMain' in data: data=data.split('id="DeltaPlaceHolderMain"',1)[1]
  for marker in ['id="footer"','id="pie_pagina"','<!-- Footer']:
   data=data.split(marker)[0]
  p=Links();p.feed(data)
  records=[]
  for a in p.links:
   name=' '.join(a['title'].replace('\u200b','').split())
   dest=urllib.parse.urljoin(url,a['url'])
   host=urllib.parse.urlsplit(dest).hostname or ''
   if not (host=='dian.gov.co' or host.endswith('.dian.gov.co')):continue
   if len(name)<5 or any(w in name.lower() for w in ['política de','políticas de','notificaciones judiciales','mapa del sitio','denuncias','pqsr','puntos de contacto','puntos de atención']):continue
   if dest==url or dest.endswith('#') or '/Paginas/Privacidad' in dest:continue
   records.append({'title':name,'url':dest,'parentTitle':title,'parentUrl':url})
  return {'title':title,'url':url,'status':r.status,'links':records}
 except Exception as e:return {'title':title,'url':url,'error':str(e),'links':[]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(collect,list(dict.fromkeys(pages))))
(ROOT/'sources/expanded.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Pages:',len(results),'links:',sum(len(x['links']) for x in results),'errors:',[x['url'] for x in results if 'error' in x])
url='https://normograma.dian.gov.co/dian/compilacion/js/openClosePanelArbolOpcion_aux.js?v=2.0'
data=urllib.request.urlopen(url,timeout=30).read()
(ROOT/'sources/normograma-index-loader.js').write_bytes(data)
