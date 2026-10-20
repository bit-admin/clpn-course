// Chrome / Chromium 的位置：先看环境变量 CHROME_PATH，再试常见安装位置（Linux、macOS、Windows），最后用 PATH 里的 google-chrome。
// 例：CHROME_PATH="/Applications/Chromium.app/Contents/MacOS/Chromium" node src/test/check_all.js
const fs = require('fs');
const CANDIDATES = [
  '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/snap/bin/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
];
module.exports = process.env.CHROME_PATH || CANDIDATES.find(p => fs.existsSync(p)) || 'google-chrome';
