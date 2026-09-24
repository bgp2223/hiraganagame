const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto('file://' + __dirname + '/sheet.html');
  await p.pdf({ path: __dirname + '/立方体の切断_4図.pdf', preferCSSPageSize: true, printBackground: true });
  await p.screenshot({ path: __dirname + '/preview.png' });
  await b.close();
})();
