// Headless test van een domein op de lokale site (stap 8). Gebruik: node lab/subsidies_sitetest.js [slug] [poort]
// Start zelf `python3 -m http.server <poort>` in site/. Controleert: domein laadt, teller = aantal in meta.json, geen JS-fouten.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const slug = process.argv[2] || 'subsidies', poort = process.argv[3] || '8765';
(async () => {
  const idx = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'site/data/domeinen/index.json')));
  const d = idx.find(x => x.slug === slug); if (!d) { console.log('FOUT: slug niet in index.json'); process.exit(1); }
  // de site laat uitspraken zonder relevant=true weg (index.html: fout=verr.filter(v=>!v.relevant)); verwacht dus alleen die
  const meta = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'site', d.pad, 'meta.json')));
  const verr = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'site', d.pad, 'verrijkt.json')));
  const nietRel = new Set(verr.filter(v => !v.relevant).map(v => v.ecli));
  const n = meta.filter(m => !nietRel.has(m.e)).length;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } }); const fout = [];
  p.on('pageerror', e => fout.push('pageerror: ' + e.message));
  // 404 op optionele bestanden (lijnen/eclireg/trends) en de uitlegvideo (niet in deze repo) is verwacht
  const VERWACHT = /\/(lijnen|eclireg|trends)\.json|\/video\//;
  // al op main ontbrekende tegelafbeeldingen van ANDERE domeinen: melden, niet als fout tellen
  const ANDER_BEELD = new RegExp('/assets/dom-(?!' + slug.replace(/[-]/g, '\\-') + '\\.)[a-z-]+\\.webp');
  const letop = [];
  p.on('response', r => { if (r.status() >= 400 && !VERWACHT.test(r.url())) (ANDER_BEELD.test(r.url()) ? letop : fout).push(`http ${r.status()}: ${r.url()}`); });
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) fout.push('console: ' + m.text()); });
  p.on('requestfailed', r => { if (!VERWACHT.test(r.url())) fout.push('request: ' + r.url()); });
  await p.goto(`http://localhost:${poort}/?domein=${slug}`, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  const tekst = await p.evaluate(() => document.body.innerText);
  const gekozen = await p.evaluate(() => (typeof DOM !== 'undefined' && DOM.slug) || null);
  const nMeta = await p.evaluate(() => (typeof S !== 'undefined' && S.meta) ? S.meta.length : -1);
  const raar = await p.evaluate(() => (typeof S !== 'undefined' && S.tax) ? Object.keys(S.tax).filter(k => k.startsWith('_')) : []);
  if (raar.length) fout.push('taxonomie bevat technische sleutels als onderwerp: ' + raar.join(', '));
  const fmt = x => x.toLocaleString('nl-NL');
  const teller = tekst.includes(String(n)) || tekst.includes(fmt(n)) || tekst.includes(String(meta.length)) || tekst.includes(fmt(meta.length));
  console.log(`domein ${gekozen} | meta geladen ${nMeta} / ${n} | teller op pagina ${teller ? 'ja' : 'nee'} | JS-fouten ${fout.length}`);
  fout.slice(0, 10).forEach(f => console.log('   FOUT', f));
  letop.forEach(f => console.log('   LET OP (bestaand, ander domein)', f));
  await b.close();
  const ok = gekozen === slug && nMeta === n && fout.length === 0;  // teller op pagina: informatief (startpagina toont soms geen totaal)
  console.log(ok ? 'SITETEST: OK' : 'SITETEST: FOUT'); process.exit(ok ? 0 : 1);
})();
