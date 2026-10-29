/* All 72 reference states at all 3 viewports. Never mutates canonical assets. */
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..');
const design = path.join(root, 'reference/design');
const artifacts = path.join(root, 'artifacts');
const capture = process.argv.includes('--capture');
fs.mkdirSync(artifacts, { recursive: true });

(async () => {
  const started = Date.now();
  const browser = await chromium.launch({ headless: true,
    ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {}) });
  const screens = JSON.parse(fs.readFileSync(path.join(design, 'screen-manifest.json')));
  const results = [];
  try {
    if (screens.length !== 72) throw new Error('The full reference requires exactly 72 states');
    for (const size of [[1920, 1080], [1366, 768], [1280, 720]]) {
      const page = await browser.newPage({ viewport: { width: size[0], height: size[1] } });
      page.setDefaultTimeout(10000);
      let errors = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('requestfailed', request => errors.push('Asset failed: ' + request.url()));
      for (const screen of screens) {
        errors = [];
        const url = pathToFileURL(path.join(design, 'index.html'));
        url.search = new URLSearchParams({ capture: '1', screen: screen.id }).toString();
        await page.goto(url.href);
        await page.evaluate(() => document.fonts.ready);
        await page.locator('body').click({ position: { x: 2, y: 2 } });
        const metrics = await page.evaluate(() => {
          const rect = element => {
            if (!element) return null;
            const r = element.getBoundingClientRect();
            return { x: r.x, y: r.y, right: r.right, bottom: r.bottom, width: r.width, height: r.height };
          };
          const body = document.querySelector('.dialog-body');
          const page = document.querySelector('.page');
          return { actualScreen: designReference.state.screen,
            windowOverflow: document.documentElement.scrollWidth > innerWidth + 1,
            dialog: rect(document.querySelector('.dialog')),
            footer: rect(document.querySelector('.dialog-footer')),
            checkout: rect(document.querySelector('.checkout')),
            dialogBodyOverflow: body ? body.scrollWidth > body.clientWidth + 1 : false,
            pageOverflow: page ? page.scrollWidth > page.clientWidth + 1 : false,
            fontsLoaded: document.fonts.check('14px Inter') && document.fonts.check('20px "Plus Jakarta Sans"') };
        });
        const outside = r => r && (r.x < -1 || r.y < -1 || r.right > size[0] + 1 || r.bottom > size[1] + 1);
        const issues = [...errors];
        if (metrics.actualScreen !== screen.id) issues.push('Wrong rendered state');
        if (!metrics.fontsLoaded) issues.push('Font load failed');
        if (metrics.windowOverflow || metrics.pageOverflow || metrics.dialogBodyOverflow) issues.push('Horizontal overflow');
        if (outside(metrics.footer) || outside(metrics.dialog)) issues.push('Dialog or footer outside viewport');
        if (outside(metrics.checkout)) issues.push('Checkout outside viewport');
        results.push({ screen: screen.id, size, issues, ...metrics });
        if (capture) {
          const dir = path.join(artifacts, 'screens', size.join('x'));
          fs.mkdirSync(dir, { recursive: true });
          await page.screenshot({ path: path.join(dir, `${String(screen.number).padStart(2, '0')}-${screen.id}.png`) });
        }
      }
      await page.close();
      console.log(`Measured ${screens.length} states at ${size.join('×')}`);
    }
  } finally {
    await browser.close();
  }
  const failures = results.filter(row => row.issues.length);
  const report = { scope: 'Relocated offline reference only; not the Windows app',
    state: failures.length || results.length !== 216 ? 'FAIL' : 'PASS',
    seconds: (Date.now() - started) / 1000, observations: results.length, failures, measurements: results };
  fs.writeFileSync(path.join(artifacts, 'reference-validation.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ state: report.state, observations: report.observations, seconds: report.seconds, failures }));
  if (report.state !== 'PASS') process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
