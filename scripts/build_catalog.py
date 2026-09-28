import json,re,html,hashlib,unicodedata
from pathlib import Path
from urllib.parse import urlsplit,urljoin
from datetime import datetime,timezone,timedelta
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'sources'/f'{name}.json').read_text(encoding='utf-8'))
def plain(s):return ' '.join(html.unescape(re.sub('<[^>]+>','',s)).replace('\u200b','').split()).replace(' – ','. ').replace(' - ','. ')
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))
categories=[('todos','Todos los temas'),('importacion','Importación'),('exportacion','Exportación'),('normativa','Normativa y doctrina'),('arancel','Arancel y clasificación'),('origen','Origen y acuerdos'),('valoracion','Valoración aduanera'),('transito','Tránsito y carga'),('zonas','Zonas y regímenes'),('operadores','Usuarios y OEA'),('servicios','Trámites y sistemas'),('estadisticas','Estadísticas')]
def tags_for(s):
 s=norm(s);tags=[]
 rules={'importacion':['importa','menaje','retorno','envios','viajero'],'exportacion':['exporta'],'arancel':['arancel','clasificacion','subpartida','armonizado'],'origen':['origen','acuerdo','preferenci'],'valoracion':['valoracion','valor en aduana','andina de valor'],'transito':['transito','carga','trazabilidad','transporte'],'zonas':['zona franca','regimen aduanero especial','puerto libre','leticia','maicao','tumaco'],'operadores':['oea','operador','agencia','usuario aduanero','economico autorizado'],'servicios':['informatico','syga','formulario','tramite','servicio','contingencia','muisca'],'estadisticas':['estadistic','cifras','tiempos de despacho','comex']}
 for k,vs in rules.items():
  if any(v in s for v in vs):tags.append(k)
 return tags
def kind(title,url):
 n=norm(title)
 if re.match(r'(resolucion|decreto|ley|circular|decision|memorando)',n):return 'Norma'
 if 'concepto' in n or 'oficio' in n or 'doctrina' in n:return 'Doctrina'
 if 'jurisprudencia' in n:return 'Jurisprudencia'
 if any(x in n for x in ['estadistic','cifras','tiempos de despacho','bases de datos','tablero']):return 'Estadística'
 if any(x in n for x in ['abece','abc','cartilla','guia','manual','paso a paso','infografia']):return 'Guía'
 if any(x in n for x in ['boletin','doctriflash','presentacion','judicial']):return 'Publicación'
 if any(x in n for x in ['consulta','servicio','solicitud','formulario','formato','ingreso','operaciones integradas','syga','arancel']):return 'Servicio'
 return 'Directorio'
rows={}
def add(title,url,description='',tags=None,type=None,sourceIndex='',group='',id=None,featured=0,legal=False):
 title=plain(title);url=url.split('#')[0];key=url.lower()
 if not title or not url.startswith('https://'):return
 if urlsplit(url).hostname not in ['www.dian.gov.co','normograma.dian.gov.co','muisca.dian.gov.co','importaciones.dian.gov.co']:return
 if key in rows:
  rows[key]['tags']=list(dict.fromkeys(rows[key]['tags']+(tags or tags_for(title+' '+group))))
  if legal:rows[key]['legal']=True;rows[key]['tags']=list(dict.fromkeys(rows[key]['tags']+['normativa']))
  return
 years=re.findall(r'\b(?:19|20)\d{2}\b',title)
 typ=type or kind(title,url)
 legal=legal or typ in ['Norma','Doctrina','Jurisprudencia']
 ts=tags or tags_for(title+' '+group)
 if legal and 'normativa' not in ts:ts.append('normativa')
 if not ts:ts=['normativa'] if legal else ['servicios']
 subtype=next((x for x in ['Resolución','Decreto','Ley','Circular','Decisión','Memorando'] if norm(title).startswith(norm(x))),typ)
 rows[key]={'id':id or 'r'+hashlib.sha1(url.encode()).hexdigest()[:12],'title':title,'url':url,'description':plain(description),'type':typ,'subtype':subtype,'tags':ts,'year':int(years[-1]) if years else None,'format':'PDF' if '.pdf' in url.lower() else ('Excel' if re.search(r'\.xlsx?$',url,re.I) else 'Web'),'sourceIndex':sourceIndex,'group':plain(group),'featured':featured,'legal':legal}

aduanas=load('aduanas')
def from_title(needle):return next(a['url'] for a in aduanas if needle.lower() in a['title'].lower())
featured=[
('arancel','Consulta del Arancel de Aduanas',from_title('Consulta del Arancel'),'Busca la nomenclatura, los gravámenes y la información asociada a una subpartida.',['arancel','importacion','exportacion'],'Servicio'),
('norma1165','Decreto 1165 de 2019','https://normograma.dian.gov.co/dian/compilacion/docs/decreto_1165_2019.htm','Régimen de Aduanas. Texto con anotaciones, modificaciones y concordancias en la compilación jurídica.',['normativa','importacion','exportacion'],'Norma'),
('res46','Resolución 46 de 2019','https://normograma.dian.gov.co/dian/compilacion/docs/resolucion_dian_0046_2019.htm','Reglamentación del Decreto 1165 de 2019. Consulta el texto y sus notas de vigencia.',['normativa','importacion','exportacion'],'Norma'),
('exportacion','Abecé de exportación',from_title('Abecé Exportación'),'Orientación de la DIAN para conocer los aspectos básicos de una operación de exportación.',['exportacion'],'Guía'),
('origen','Origen de las mercancías',from_title('Origen'),'Normativa, acuerdos comerciales, pruebas de origen y procedimientos para importadores y exportadores.',['origen','importacion','exportacion'],'Directorio'),
('importacion','Cartilla de importaciones',from_title('Cartilla de Importaciones'),'Consulta el instructivo oficial de la declaración de importación y sus casillas.',['importacion'],'Guía'),
('anticipada','Declaración anticipada de importación',from_title('Declaración Anticipada'),'Orientación, normativa y documentos oficiales sobre la declaración anticipada.',['importacion','servicios'],'Directorio'),
('valoracion','Valoración aduanera',from_title('Valoración Aduanera'),'Acceso a la sección técnica de la DIAN sobre el valor en aduana de las mercancías.',['valoracion','importacion'],'Directorio'),
('servicios','Servicios aduaneros en línea',from_title('Acceso a servicios'),'Ingreso de mercancías, exportación, tránsito, origen y otros servicios informáticos.',['servicios','importacion','exportacion','transito'],'Servicio'),
('oea','Operador Económico Autorizado',from_title('OEA'),'Información del programa OEA, solicitud de autorización y reconocimiento mutuo.',['operadores','importacion','exportacion'],'Directorio'),
('contingencia','Contingencias de los servicios aduaneros',from_title('Contingencia'),'Cartillas y procedimientos publicados por la DIAN para contingencias de los servicios electrónicos.',['servicios','importacion','exportacion'],'Directorio'),
('estadisticas','Estadísticas de comercio exterior','https://www.dian.gov.co/dian/cifras/Paginas/EstadisticasComEx.aspx','Tablero COMEX, bases de importaciones y exportaciones, tributos y directorios estadísticos.',['estadisticas','importacion','exportacion'],'Estadística'),
('normograma','Normograma aduanero','https://normograma.dian.gov.co/dian/compilacion/aduanero.html?q=ADUANERO','Explora el conjunto oficial de normativa, doctrina y jurisprudencia aduanera.',['normativa'],'Directorio'),
('normas','Normativa aduanera','https://normograma.dian.gov.co/dian/compilacion/a_1_normativa_aduanera.html?q=ADUANERO','Leyes, decretos, resoluciones, circulares y memorandos organizados por materia.',['normativa'],'Directorio'),
('doctrina','Doctrina aduanera','https://normograma.dian.gov.co/dian/compilacion/a_2_doctrina_aduanera.html?q=ADUANERO','Conceptos y oficios, con consulta por tipo de documento y período.',['normativa'],'Doctrina'),
('jurisprudencia','Jurisprudencia aduanera','https://normograma.dian.gov.co/dian/compilacion/a_3_jurisprudencia_aduanera.html?q=ADUANERO','Decisiones judiciales y jurisprudencia de unificación relacionadas con asuntos aduaneros.',['normativa'],'Jurisprudencia'),
('cambiario','Compilación del régimen cambiario','https://normograma.dian.gov.co/dian/compilacion/cambiario.html?q=CAMBIARIO','Consulta la compilación oficial en materia cambiaria.',['normativa','importacion','exportacion'],'Directorio'),
('novedades','Novedades y boletines jurídicos','https://normograma.dian.gov.co/dian/compilacion/novedades_boletines.html','Accede a las novedades publicadas por la DIAN y los boletines organizados por período.',['normativa'],'Publicación'),
]
for i,(id,title,url,desc,tags,typ) in enumerate(featured):add(title,url,desc,tags,typ,sourceIndex='https://www.dian.gov.co/aduanas/Paginas/Inicio.aspx' if 'normograma' not in url else 'https://normograma.dian.gov.co/dian/',id=id,featured=100-i)
for a in aduanas[26:86]:
 title=a['title']
 if title=='aquí':title='Abecé del régimen sancionatorio aduanero'
 title=title.replace('Despachoo','Despacho')
 add(title,a['url'],tags=tags_for(title),sourceIndex='https://www.dian.gov.co/aduanas/Paginas/Inicio.aspx')
for a in load('normativa')[26:]:
 if any(w in norm(a['title']) for w in ['doctriflash','actualidad juridica','normas','agenda reglamentaria','judiciales']):add(a['title'],a['url'],tags=['normativa'],sourceIndex='https://www.dian.gov.co/normatividad/Paginas/Inicio.aspx')

for page in load('expanded'):
 if any(t in page['title'] for t in ['Convenios Tributarios','Intercambio Internacional','Convenios Interinstitucionales','Encuentros Aduana Empresa']):continue
 for a in page['links']:
  title=a['title']
  if title.startswith('http') or len(title)<7 or title in ['www.dian.gov.co','← Regresar','Publicaciones recientes','Esquema XSD']:continue
  if re.match(r'^\d+(\.\d+)*\.',title):title=re.sub(r'^\d+(\.\d+)*\.\s*','',title)
  add(title,a['url'],f"Recurso publicado en la sección {plain(page['title'])}.",tags=tags_for(title+' '+page['title']),sourceIndex=page['url'],group=page['title'])

indices=[]
for index in load('legal-index'):
 if index['url'].endswith('a_1_normativa_aduanera_parte_14.html'):continue
 path=ROOT/'sources'/index['url'].rsplit('/',1)[-1]
 if not path.exists():continue
 raw=path.read_text(encoding='utf-8');indices.append(index['url'])
 for item in re.findall(r'<li class="documento-arbol">(.*?)</li>',raw,re.S):
  u=re.search(r'href="([^"]+)"',item);t=re.search(r'<span class="id-documento">(.*?)</span>',item,re.S);d=re.search(r'<p>(.*?)</p>',item,re.S)
  if not u or not t:continue
  title=plain(t[1]);desc=plain(d[1]) if d else ''
  group=re.sub(r'^\d+(\.\d+)*\.\s*','',index['group'])
  tags=tags_for(title+' '+desc+' '+group)
  add(title,urljoin(index['url'],html.unescape(u[1])),desc,tags,index['type'],index['url'],group,legal=True)

result=list(rows.values());result.sort(key=lambda r:(-r['featured'],-(r['year'] or 0),r['title']))
stamp=datetime.now(timezone(timedelta(hours=-5))).strftime('%Y-%m-%d')
out={'updated':stamp,'categories':[{'id':i,'label':l} for i,l in categories],'resources':result,'coverage':{'resources':len(result),'legal':sum(r['legal'] for r in result),'legalIndexes':len(indices),'sectionPages':len(load('expanded')),'note':'Índice de referencias, títulos y descripciones. Incluye documentos históricos. No equivale a una copia integral de la DIAN ni a una certificación de vigencia.','indexUrls':indices}}
(ROOT/'dist/catalog.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({'resources':len(result),'legal':out['coverage']['legal'],'categories':{i:sum(i in r['tags'] for r in result) for i,l in categories[1:]},'bytes':(ROOT/'dist/catalog.json').stat().st_size},ensure_ascii=True))
