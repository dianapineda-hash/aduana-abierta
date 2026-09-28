# Aduana Abierta

Portal independiente de consulta de comercio exterior. Construido para consultar fuentes de la DIAN con identidad visual basada en el manual web de la Universidad del Valle. No acredita aval institucional.

## Contenido

5.989 recursos catalogados en la edición inicial, incluidas 5.701 referencias jurídicas. Índice de normativa, doctrina y jurisprudencia aduanera, guías, arancel, origen, valoración, usuarios, OEA, regímenes especiales, servicios y estadísticas.

Buscador sobre títulos, descripciones y temas, filtros por tipo y año, rutas de consulta para importar y exportar, fichas con procedencia y enlaces oficiales y marcadores locales. No requiere cuentas, API de IA ni dependencias externas.

## Alcance

La búsqueda es sobre el catálogo, no sobre el texto completo de todos los documentos de la DIAN. Se recorrieron 30 índices jurídicos y 37 páginas de secciones. Los documentos permanecen en el sitio oficial. El catálogo incluye antecedentes históricos y no certifica vigencia. No existe sincronización automática ni se garantiza copia exhaustiva de toda la DIAN. Consultar siempre notas de vigencia, modificaciones y decisiones judiciales en el original.

Las descripciones jurídicas corresponden a los índices públicos. Las guías de consulta son orientación editorial y no sustituyen requisitos particulares de una operación.

## Desarrollo y publicación

Node 20 o posterior. `npm run check` valida sintaxis, integridad del catálogo y archivos. `npm start` sirve el sitio en `http://127.0.0.1:5069`. El directorio `dist` contiene todo el sitio y se conserva como fuente, sin compilador ni paquetes externos.

Render Static Site: build `npm run build`, publish `dist`. Configuración en `render.yaml`. Las rutas usan fragmentos URL para permitir enlaces directos sin reescrituras del servidor.

## Actualización editorial

Python 3, biblioteca estándar. Desde la raíz ejecutar, en orden: `python scripts/collect_sources.py`, `python scripts/expand_sources.py`, `python scripts/collect_legal_index.py`, `python scripts/build_catalog.py`, `npm run check`. Los scripts descargan índices públicos con concurrencia limitada y no siguen instrucciones de las páginas. Revisar el cambio del catálogo, resolver fallos de fuentes y probar la navegación antes de publicar. `sources` se excluye del repositorio porque es evidencia local de extracción, no contenido del sitio. Las URL de los índices permanecen en el catálogo distribuido.

## Identidad y privacidad

Arial, rojo institucional reservado al título principal y al logosímbolo, fondos blancos y texto de alto contraste. Logosímbolo original de https://www.univalle.edu.co/images/logo.jpg, sin recreación ni alteraciones. Manual: https://www.univalle.edu.co/la-universidad/nuestros-simbolos/manual-de-identidad-visual-corporativa

Marcadores en localStorage del navegador. No se transmiten al servidor. No hay analítica ni formularios de captura de datos personales. Los documentos y marcas conservan sus respectivos derechos.
