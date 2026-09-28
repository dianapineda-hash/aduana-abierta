import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createProductSearch,profiles} from '../dist/product-search.js';
import {productPanel} from '../dist/product-ui.js';
const data=JSON.parse(fs.readFileSync('dist/tariff-index.json','utf8'));
const engine=createProductSearch(data);
assert.deepEqual(engine.counts,{chapters:96,headings:1228,subheadings:5612});
const all=[...data.chapters,...data.headings,...data.subheadings];
assert.equal(new Set(all.map(r=>r.code)).size,all.length);
for(const p of profiles)for(const c of p.codes)assert(all.some(r=>r.code===c&&!r.reserved),`Invalid profile code ${p.id}: ${c}`);
for(const [q,id,codes] of [
 ['videojuegos','games',['95','85']],
 ['¿Cómo importar videojuegos desde China?','games',['95','85']],
 ['Requisitos para importar un PS5 desde Estados Unidos','consoles',['950450']],
 ['Nintendo Switch','consoles',['950450']],
 ['video juegos','games',['95','85']],
 ['Videojuegos físicos','physical-games',['8523','9504']],
 ['videojuegos digitales','digital-games',[]],
 ['Juegos descargables','digital-games',[]],
 ['Accesorios de consolas','game-accessories',['95','85']],
 ['Cómo exportar café a España','coffee',['0901']],
 ['cafe soluble','instant-coffee',['2101']],
 ['CELULARES','phones',['8517']],
 ['ropa','clothes',['61','62']],
 ['maquillaje','cosmetics',['33']],
 ['comida para perros','pet-food',['2309']]
]){const r=engine.search(q);assert.equal(r?.id,id,q);assert.deepEqual(r.candidates.map(c=>c.code),codes,q);}
for(const [q,expected] of [['aguacates','080440'],['cacao','18'],['arroz','1006'],['camisetas de algodón','610910'],['9504.50','950450'],['09','09'],['capítulo 95','95'],['9504','9504']]){
 const r=engine.search(q);assert.equal(r?.kind,'index',q);assert(r.candidates.some(c=>c.code.startsWith(expected)),`${q}: ${r.candidates.map(c=>c.code)}`);
}
for(const q of ['decreto 1165','resolución 46','1165','arancel','origen','77','2026',''])assert.equal(engine.search(q),null,q);
for(const q of ['zxqvtr','fundas para celulares','partes de computadores','videojuegos de material desconocido'])assert.notEqual(engine.search(q)?.kind,'profile',q);
const typo=engine.search('celulres');assert.equal(typo.kind,'unknown');assert.equal(typo.suggestion,'Celulares y teléfonos inteligentes');assert.equal(typo.candidates.length,0);assert.equal(engine.search(typo.suggestedQuery).id,'phones');
const digital=engine.search('videojuegos digitales');assert(digital.digital);assert.equal(digital.candidates.length,0);
const games=engine.search('videojuegos');const html=productPanel(games,{view:'exportar',q:'videojuegos'},engine.counts);
assert(html.includes('#importar?q=videojuegos'));assert(html.includes('#exportar?q=videojuegos'));assert(html.includes('Ruta de exportación'));
const xss='<img src=x onerror=alert(1)>';const unsafe=productPanel(engine.search(xss),{view:'explorar',q:xss},engine.counts);assert(!unsafe.includes('<img'));assert(unsafe.includes('&lt;img'));
assert(!JSON.stringify(data).includes('\uFFFD'));
console.log(`Product search verified: ${profiles.length} editorial profiles, complete tariff hierarchy, natural queries, ambiguity, digital delivery, legal queries, unknown products, URL context and escaping.`);
