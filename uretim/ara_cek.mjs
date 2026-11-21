// Ara Studio'yu headless Chrome ile açar, film JSON'u yükler, 1080x1920 MP4 dışa aktarır.
// Kullanım: node ara_cek.mjs film.json cikis.mp4   (Ara deposu dizininde, vite :4422'de çalışıyor olmalı)
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'node:fs';
const [film, out] = process.argv.slice(2);
const text = readFileSync(film, 'utf8');
const b = await chromium.launch({ channel: 'chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required', '--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1500, height: 1100 } });
const errs = [];
p.on('pageerror', e => errs.push(String(e)));
p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await p.addInitScript(() => { try { localStorage.setItem('ara.studio.tour.v1', '1'); } catch {} });
await p.goto('http://localhost:4422/studio/#demo');
await p.waitForFunction('window.studio?.ready', null, { timeout: 300000 });
await p.evaluate((t) => { const dt = new DataTransfer(); dt.items.add(new File([t], 'film.ara-studio.json', { type: 'application/json' }));
  const e = document.querySelector('#project-file'); e.files = dt.files; e.dispatchEvent(new Event('change')); }, text);
await p.waitForTimeout(3000);
await p.waitForFunction('window.studio?.ready', null, { timeout: 300000 });
const info = await p.evaluate(() => ({ actors: window.studio.project.actors.length, tpl: window.studio.project.template, aspect: window.studio.project.aspect }));
console.log('yüklendi', JSON.stringify(info));
const b64 = await p.evaluate(async () => {
  const proj = structuredClone(window.studio.project);
  const blob = await window.studio.exportMovie(window.studio.scene, proj, { width: 1080, height: 1920, signal: new AbortController().signal, progress: (x) => { if (Math.random() < .02) console.log('ilerleme', x); } });
  const bytes = new Uint8Array(await blob.arrayBuffer()); let s = '';
  for (let i = 0; i < bytes.length; i += 32768) s += String.fromCharCode(...bytes.subarray(i, i + 32768));
  return btoa(s);
});
writeFileSync(out, Buffer.from(b64, 'base64'));
console.log('yazıldı', out, Buffer.from(b64, 'base64').length, 'bayt');
if (errs.length) console.log('SAYFA HATALARI:', errs.slice(0, 5).join(' | '));
await b.close();
