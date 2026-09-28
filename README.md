# Aduana Abierta

Portal independiente de consulta de comercio exterior. Construido para consultar fuentes de la DIAN con identidad visual basada en el manual web de la Universidad del Valle. No acredita aval institucional.

## Contenido

5.989 recursos catalogados en la edición inicial, incluidas 5.701 referencias jurídicas. Índice de normativa, doctrina y jurisprudencia aduanera, guías, arancel, origen, valoración, usuarios, OEA, regímenes especiales, servicios y estadísticas.

Buscador sobre títulos, descripciones y temas, filtros por tipo y año, rutas de consulta para importar y exportar, fichas con procedencia y enlaces oficiales y marcadores locales. La consulta por producto añade orientación arancelaria y conserva el producto al cambiar de operación. No requiere cuentas, API de IA ni dependencias externas.

## Consulta por producto

`dist/tariff-index.json` contiene 96 capítulos con contenido (el 77 está reservado), 1.228 partidas y 5.612 subpartidas SA 2022. Las descripciones españolas proceden del [Decreto 1881 de 2021](https://normograma.dian.gov.co/dian/compilacion/docs/decreto_1881_2021.htm), relacionadas con la [estructura SA 2022 de Naciones Unidas](https://comtradeapi.un.org/files/v1/app/reference/H6.json). Se reutilizó el índice elaborado para Incoterms Lab, conservando en los metadatos la procedencia y las huellas de sus fuentes. No incluye tarifas ni incorpora automáticamente reformas posteriores.

`dist/product-search.js` relaciona 25 perfiles editoriales y sus nombres comerciales con posiciones de ese índice; para otros productos busca palabras en las descripciones y su partida. Normaliza tildes y plurales, reconoce frases de importación/exportación y ofrece sugerencias para ciertos errores de escritura. Un producto desconocido recibe opciones para precisar la consulta y un enlace a la búsqueda alfabética oficial, sin inventar un capítulo.

Videojuegos permite elegir consolas, soportes físicos, contenido digital o accesorios. Las entregas digitales no reciben una clasificación física automática. Los códigos se presentan como referencias candidatas: la subpartida nacional y su vigencia deben confirmarse en la DIAN. Las rutas enlazan clasificación, origen, valoración, procedimientos y VUCE; no determinan requisitos ni tributos particulares.

Los perfiles se mantienen en `dist/product-search.js`, la presentación en `dist/product-ui.js` y las pruebas en `scripts/test-products.mjs`. Para actualizar el índice, contrastar la jerarquía con las fuentes oficiales, conservar procedencia y verificar cambios normativos antes de sustituir las referencias. `node scripts/test-products.mjs` valida búsquedas naturales, productos ambiguos, entrega digital, errores de escritura, consultas jurídicas, códigos, enlaces que conservan el producto y escape de HTML.

## Alcance

La búsqueda es sobre el catálogo, no sobre el texto completo de todos los documentos de la DIAN. Se recorrieron 30 índices jurídicos y 37 páginas de secciones. Los documentos permanecen en el sitio oficial. El catálogo incluye antecedentes históricos y no certifica vigencia. No existe sincronización automática ni se garantiza copia exhaustiva de toda la DIAN. Consultar siempre notas de vigencia, modificaciones y decisiones judiciales en el original.

Las descripciones jurídicas corresponden a los índices públicos. Las guías de consulta son orientación editorial y no sustituyen requisitos particulares de una operación.

## Desarrollo y publicación

Node 20 o posterior. `npm run check` valida sintaxis, integridad del catálogo, búsquedas por producto y archivos. `npm start` sirve el sitio en `http://127.0.0.1:5069`. El directorio `dist` contiene todo el sitio y se conserva como fuente, sin compilador ni paquetes externos. Las mismas comprobaciones pueden ejecutarse directamente con Node si npm no está instalado.

Render Static Site: build `npm run build`, publish `dist`. Configuración en `render.yaml`. Las rutas usan fragmentos URL para permitir enlaces directos sin reescrituras del servidor.

## Actualización editorial

Python 3, biblioteca estándar. Desde la raíz ejecutar, en orden: `python scripts/collect_sources.py`, `python scripts/expand_sources.py`, `python scripts/collect_legal_index.py`, `python scripts/build_catalog.py`, `npm run check`. Los scripts descargan índices públicos con concurrencia limitada y no siguen instrucciones de las páginas. Revisar el cambio del catálogo, resolver fallos de fuentes y probar la navegación antes de publicar. `sources` se excluye del repositorio porque es evidencia local de extracción, no contenido del sitio. Las URL de los índices permanecen en el catálogo distribuido.

## Identidad y privacidad

Arial, rojo institucional reservado al título principal y al logosímbolo, fondos blancos y texto de alto contraste. Logosímbolo original de https://www.univalle.edu.co/images/logo.jpg, sin recreación ni alteraciones. Manual: https://www.univalle.edu.co/la-universidad/nuestros-simbolos/manual-de-identidad-visual-corporativa

Marcadores en localStorage del navegador. No se transmiten al servidor. No hay analítica ni formularios de captura de datos personales. Los documentos y marcas conservan sus respectivos derechos.
