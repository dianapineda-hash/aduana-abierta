import urllib.request, json, re, concurrent.futures
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.a=None
    def handle_starttag(self,t,a):
        if t=='a': self.a={'title':'','url':dict(a).get('href','')}
    def handle_data(self,d):
        if self.a is not None: self.a['title']+=d
    def handle_endtag(self,t):
        if t=='a' and self.a is not None: self.links.append(self.a); self.a=None

URLS = {
 'aduanas':'https://www.dian.gov.co/aduanas/Paginas/Inicio.aspx',
 'normograma':'https://normograma.dian.gov.co/dian/',
 'marca':'https://www.univalle.edu.co/la-universidad/nuestros-simbolos/manual-de-identidad-visual-corporativa',
 'normativa':'https://www.dian.gov.co/normatividad/Paginas/Inicio.aspx',
 'leyes':'https://normograma.dian.gov.co/dian/compilacion/a_1_normativa_aduanera.html?q=ADUANERO',
 'doctrina':'https://normograma.dian.gov.co/dian/compilacion/a_2_doctrina_aduanera.html?q=ADUANERO',
 'jurisprudencia':'https://normograma.dian.gov.co/dian/compilacion/a_3_jurisprudencia_aduanera.html?q=ADUANERO',
}
def get(name,url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    data=urllib.request.urlopen(req,timeout=40).read()
    (ROOT/'sources'/f'{name}.html').write_bytes(data)
    try: decoded=data.decode('utf-8')
    except UnicodeDecodeError: decoded=data.decode('cp1252')
    p=Links();p.feed(decoded)
    links=[{'title':' '.join(a['title'].split()),'url':urljoin(url,a['url'])} for a in p.links if a['title'].strip()]
    (ROOT/'sources'/f'{name}.json').write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name, len(links), 'enlaces')
    return links
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda p:get(*p), URLS.items()))
    data=urllib.request.urlopen('https://www.univalle.edu.co/images/logo.jpg',timeout=30).read()
    (ROOT/'dist/assets/univalle.jpg').write_bytes(data)
