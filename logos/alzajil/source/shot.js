const { chromium } = require('playwright');
(async () => {
  const [,, html, out, w, h, scale, transparent] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +(scale||1) });
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(200);
  await p.screenshot({ path: out, omitBackground: transparent === '1' });
  await b.close();
})();
