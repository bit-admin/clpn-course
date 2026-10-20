// 离线链接检查（无头 Chrome）：把课程文件夹当作 file:// 打开，检查每一页“运行完脚本后”的全部内部链接与资源。
//  - 不做任何服务器式的解析：目录不会自动补 index.html，没有“漂亮网址”，以 / 开头的绝对路径会指向磁盘根目录（= 错误）
//  - 目标必须是真实存在的文件；#锚点必须在目标页（运行脚本后）的 id / name 中存在
//  - 非 file:// 的资源请求（脚本、样式、图片、字体）一律拦截并记为错误；外部 <a> 链接只计数
// 用法：NODE_PATH=/workspace/tools/node_modules node src/test/check_offline.js [课程文件夹，默认为仓库根目录]
// 例：解压 downloads/clpn-course.zip 后，node src/test/check_offline.js /tmp/x/clpn-course
const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path'); const { fileURLToPath, pathToFileURL } = require('url');
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, '../..'));
const SKIP = new Set(['src', 'node_modules', 'dist', '.git', '.venv', '.wrangler']);
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.name.startsWith('.') || SKIP.has(e.name) ? [] :
  e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.html') ? [path.join(d, e.name)] : []);
(async () => {
  const pages = walk(ROOT).filter(f => path.relative(ROOT, f) !== '404.html').sort();
  const b = await puppeteer.launch({ executablePath: require('./chrome_path'), headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const ids = new Map(); const bad = []; let nRefs = 0, nExt = 0;
  const open = async (f, errs) => {
    const p = await b.newPage(); await p.setRequestInterception(true);
    p.on('request', r => { const u = r.url(); if (/^(file|data|blob):/.test(u) || u === 'about:blank') r.continue(); else { errs.push('external request blocked: ' + u); r.abort(); } });
    p.on('requestfailed', r => { if (r.url().startsWith('file:')) errs.push('resource failed: ' + r.url()); });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    await p.goto(pathToFileURL(f).href, { waitUntil: 'networkidle0', timeout: 60000 });
    await new Promise(r => setTimeout(r, 200));
    return p;
  };
  const idsOf = async f => {
    if (!ids.has(f)) { const e = []; const p = await open(f, e);
      ids.set(f, new Set(await p.evaluate(() => [...document.querySelectorAll('[id],a[name]')].map(x => x.id || x.getAttribute('name'))))); await p.close(); }
    return ids.get(f);
  };
  for (const f of pages) {
    const errs = []; const p = await open(f, errs);
    const refs = await p.evaluate(() => [
      ...[...document.querySelectorAll('a[href],area[href]')].map(a => ['a', a.getAttribute('href'), a.href]),
      ...[...document.querySelectorAll('link[href]')].map(a => ['link', a.getAttribute('href'), a.href]),
      ...[...document.querySelectorAll('[src]')].map(a => [a.tagName.toLowerCase(), a.getAttribute('src'), a.src])]);
    ids.set(f, new Set(await p.evaluate(() => [...document.querySelectorAll('[id],a[name]')].map(x => x.id || x.getAttribute('name')))));
    await p.close();
    const rel = path.relative(ROOT, f);
    for (const e of errs) bad.push([rel, '', e]);
    for (const [tag, raw, abs] of refs) {
      if (/^(javascript|mailto|data|blob):/.test(abs)) continue;
      nRefs++;
      if (!abs.startsWith('file:')) { if (tag === 'a') { nExt++; continue; } bad.push([rel, raw, 'external resource']); continue; }
      const u = new URL(abs); u.hash = ''; u.search = ''; const t = fileURLToPath(u.href);
      if (!t.startsWith(ROOT + path.sep) && t !== ROOT) { bad.push([rel, raw, 'points outside the course folder: ' + t]); continue; }
      if (!fs.existsSync(t)) { bad.push([rel, raw, 'missing file']); continue; }
      if (!fs.statSync(t).isFile()) { bad.push([rel, raw, 'is a directory (no index.html resolution offline)']); continue; }
      const frag = decodeURIComponent(new URL(abs).hash.slice(1));
      if (frag && t.endsWith('.html') && !(await idsOf(t)).has(frag)) bad.push([rel, raw, 'missing anchor #' + frag]);
    }
  }
  await b.close();
  console.log(`root: ${ROOT}\npages: ${pages.length}, internal refs checked: ${nRefs - nExt}, external <a> links (not followed): ${nExt}`);
  for (const x of bad) console.log('BROKEN', x[0], x[1], x[2]);
  console.log('broken:', bad.length);
  process.exit(bad.length ? 1 : 0);
})();
