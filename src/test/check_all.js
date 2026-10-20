// 全站检查（无头 Chrome，断网模式）：index.html、START_HERE.html、downloads/、R/README.html、data/data_dictionary.html、lessons/*.html、materials/*.html、R/output/*.html
//  - 拦截并拒绝一切非 file:// 请求（模拟断网），任何外部请求都算错误
//  - 收集 JS 异常、console.error/warning、加载失败的资源、坏图
//  - 检查 KaTeX：.katex-error 数量、页面上残留的未渲染 TeX 定界符
//  - “点一遍”所有交互组件与测验
// 用法：NODE_PATH=/workspace/tools/node_modules [CLPN_ROOT=课程文件夹] node src/test/check_all.js [文件...]
const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
const ROOT = process.env.CLPN_ROOT ? path.resolve(process.env.CLPN_ROOT) : path.resolve(__dirname, '../..');   // CLPN_ROOT=解压后的课程文件夹，可检查离线副本
let files = process.argv.slice(2);
const ls = (d, re) => fs.existsSync(path.join(ROOT, d)) ? fs.readdirSync(path.join(ROOT, d)).filter(f => re.test(f)).sort((a, b) => a.localeCompare(b, 'en', { numeric: true })).map(f => d + '/' + f) : [];
// 默认检查全站每一页（离线副本没有 downloads/，存在才查）
if (!files.length) files = ['index.html', 'START_HERE.html', 'downloads/index.html', 'R/README.html', 'data/data_dictionary.html']
  .filter(f => fs.existsSync(path.join(ROOT, f)))
  .concat(ls('lessons', /^L\d+-\d+\.html$/), ls('materials', /\.html$/), ls('R/output', /\.html$/));
(async () => {
  const b = await puppeteer.launch({ executablePath: require('./chrome_path'), headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
  let bad = 0; const summary = [];
  for (const f of files) {
    const p = await b.newPage(); await p.setViewport({ width: 1280, height: 900 }); const errs = [];
    await p.setRequestInterception(true);
    p.on('request', r => { const u = r.url(); if (u.startsWith('file://') || u.startsWith('data:') || u.startsWith('blob:') || u === 'about:blank') r.continue(); else { errs.push('external request blocked: ' + u); r.abort(); } });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    p.on('console', m => { if (['error', 'warning', 'warn'].includes(m.type())) errs.push('console.' + m.type() + ': ' + m.text()); });
    p.on('requestfailed', r => { if (!/^https?:/.test(r.url())) errs.push('requestfailed: ' + r.url() + ' ' + (r.failure() || {}).errorText); });
    p.on('response', r => { if (r.status() >= 400) errs.push('HTTP ' + r.status() + ' ' + r.url()); });
    await p.goto('file://' + path.join(ROOT, f), { waitUntil: 'networkidle0', timeout: 60000 });
    await p.evaluate(async () => { const im = [...document.images]; im.forEach(i => { i.loading = 'eager'; }); await Promise.all(im.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 8000); }))); });
    await new Promise(r => setTimeout(r, 400));
    const info = await p.evaluate(async () => {
      const S = ms => new Promise(r => setTimeout(r, ms));
      const raw = [...document.querySelectorAll('main p, main li, main td, main th, main dd, main h2, main h3, main h4, main .mathbox')]
        .filter(e => !e.closest('pre,code,script,.katex') && /\\\(|\\\[|\$\$/.test([...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(''))).map(e => e.textContent.slice(0, 60));
      const fontsOk = document.fonts ? [...document.fonts].filter(ff => ff.status === 'error').map(ff => ff.family) : [];
      let n = 0;
      for (const bt of document.querySelectorAll('.widget button')) { if (!/复制|Copy/i.test(bt.textContent)) { bt.click(); n++; await S(3); } }
      for (const s of document.querySelectorAll('.widget input[type=range]')) for (const v of [s.min, s.max, (+s.min + +s.max) / 2]) { s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); n++; }
      for (const c of document.querySelectorAll('.widget input[type=checkbox]')) { c.click(); c.click(); n++; }
      for (const s of document.querySelectorAll('.widget select')) for (const o of s.options) { s.value = o.value; s.dispatchEvent(new Event('change', { bubbles: true })); n++; }
      for (const q of document.querySelectorAll('.quiz')) { q.querySelectorAll('.opts button, button.opt').forEach(bt => { bt.click(); n++; }); const i = q.querySelector('input'); if (i) { i.value = '0'; const qb = q.querySelector('.qbtn'); if (qb) { qb.click(); qb.click(); } const rv = q.querySelector('.reveal'); if (rv) rv.click(); n++; } }
      document.querySelectorAll('details').forEach(d => d.open = true);
      const tb = document.getElementById('themeBtn'); if (tb) { tb.click(); await S(50); tb.click(); }
      const tc = document.getElementById('tocBtn'); if (tc) { tc.click(); tc.click(); }
      return { clicks: n, katex: document.querySelectorAll('.katex').length, katexErr: document.querySelectorAll('.katex-error').length, rawTex: raw,
        widgets: document.querySelectorAll('.widget').length, widgetWarn: document.querySelectorAll('.widget .warn').length,
        emptyWidgets: [...document.querySelectorAll('.widget')].filter(w => w.children.length < 1).map(w => w.dataset.widget),
        quizzes: document.querySelectorAll('.quiz').length, badImgs: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')),
        fontErr: fontsOk, katexLoaded: !!window.katex, tocLinks: document.querySelectorAll('.toc a').length };
    });
    await new Promise(r => setTimeout(r, 200));
    const issues = [...errs];
    if (info.katexErr) issues.push('katex-error x' + info.katexErr);
    if (info.rawTex.length) issues.push('unrendered TeX: ' + info.rawTex.join(' | '));
    if (info.badImgs.length) issues.push('broken images: ' + info.badImgs.join(', '));
    if (info.emptyWidgets.length) issues.push('empty widgets: ' + info.emptyWidgets.join(','));
    if (info.fontErr.length) issues.push('font load errors: ' + info.fontErr.join(','));
    if (info.katex && !info.katexLoaded) issues.push('KaTeX not loaded');
    const brief = `katex=${info.katex} widgets=${info.widgets} quizzes=${info.quizzes} clicks=${info.clicks} toc=${info.tocLinks}`;
    console.log((issues.length ? '✗ ' : '✓ ') + f + '  ' + brief); issues.forEach(e => console.log('    ' + e));
    if (issues.length) bad++; summary.push({ f, ...info, issues: issues.length });
    await p.close();
  }
  await b.close();
  fs.writeFileSync(path.join(__dirname, 'check_all_result.json'), JSON.stringify(summary, null, 1));
  console.log(`\n${files.length} pages checked, ${bad} with issues`); process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
