import fs from 'node:fs';
import assert from 'node:assert/strict';
const data=JSON.parse(fs.readFileSync('dist/catalog.json','utf8'));
assert(data.resources.length>5000,'Incomplete catalogue');
assert.equal(new Set(data.resources.map(r=>r.id)).size,data.resources.length,'Duplicate identifiers');
assert.equal(new Set(data.resources.map(r=>r.url.toLowerCase())).size,data.resources.length,'Duplicate source URLs');
const cats=new Set(data.categories.map(c=>c.id));
for(const r of data.resources){assert(r.title.length>2);assert(r.tags.length);assert(r.tags.every(t=>cats.has(t)));const u=new URL(r.url);assert.equal(u.protocol,'https:');assert(u.hostname==='dian.gov.co'||u.hostname.endsWith('.dian.gov.co'));assert(!r.title.includes('\uFFFD'),'Encoding error');}
assert.equal(data.coverage.resources,data.resources.length);
assert.equal(data.coverage.legal,data.resources.filter(r=>r.legal).length);
for(const id of ['arancel','norma1165','res46','origen','exportacion','importacion','servicios','contingencia','estadisticas','valoracion','anticipada','novedades'])assert(data.resources.some(r=>r.id===id),id);
const source=fs.readFileSync('dist/index.html','utf8');
for(const file of ['dist/product-search.js','dist/product-ui.js','dist/tariff-index.json'])assert(fs.existsSync(file),'Missing product asset '+file);
for(const match of source.matchAll(/(?:src|href)="([^"#:]+)"/g))if(!match[1].startsWith('http'))assert(fs.existsSync('dist/'+match[1]),'Missing asset '+match[1]);
console.log(`Verified ${data.resources.length} resources, ${data.coverage.legal} legal references, ${data.coverage.legalIndexes} indexes, unique IDs, official origins, category integrity and local assets.`);
