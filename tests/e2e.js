/**
 * tests/e2e.js
 *
 * Tests E2E Puppeteer pour ECRITS_DE_GUERRE_v2.html.
 * Exécution : node tests/e2e.js
 *
 * Teste :
 *   - Navigation niveaux 0→1→2→3 pour chaque cahier
 *   - Retour arrière (bouton ←)
 *   - Clics répétés rapides (détection freeze)
 *   - Absence de surbrillance parasite
 *   - Boutons ◀/▶
 *   - Bouton settings ⚙
 */

'use strict';

const puppeteer = require('puppeteer-core');
const path      = require('path');
const fs        = require('fs');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const HTML   = 'file:///' + path.join(__dirname, '..', 'ECRITS_DE_GUERRE_v2.html').replace(/\\/g, '/');

// ─── Mini framework ──────────────────────────────────────────────────────────
let passed = 0;
let failed = 0;
const errors = [];

async function assert(condition, label) {
  if (condition) {
    console.log('  ✓', label);
    passed++;
  } else {
    console.error('  ✗', label);
    failed++;
    errors.push(label);
  }
}

async function suite(name, fn) {
  console.log('\n▶', name);
  await fn();
}

// ─── Helpers Puppeteer ───────────────────────────────────────────────────────

/** Attend que le panel-viewport contienne au moins un .panel-view */
async function waitForView(page, timeout = 3000) {
  try {
    await page.waitForSelector('#panel-viewport .panel-view', { timeout });
    return true;
  } catch {
    return false;
  }
}

/** Attend que _transitioning soit false (transition terminée) */
async function waitForTransitionEnd(page, timeout = 1000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const transitioning = await page.evaluate(() => {
      return typeof Panel !== 'undefined' && Panel._transitioning;
    });
    if (!transitioning) return true;
    await new Promise(r => setTimeout(r, 30));
  }
  return false; // timeout
}

/** Vérifie que le panneau répond (breadcrumb mis à jour) */
async function getPanelLevel(page) {
  return page.evaluate(() => {
    return typeof NAV !== 'undefined' ? NAV.state.level : -1;
  });
}

/** Clique sur un élément et attend la fin de transition */
async function clickAndWait(page, selector, timeout = 2000) {
  await page.click(selector);
  return waitForTransitionEnd(page, timeout);
}

/** Compte les .pv-item dans le viewport */
async function countItems(page) {
  return page.evaluate(() => {
    return document.querySelectorAll('#panel-viewport .pv-item').length;
  });
}

/** Vérifie l'absence de freeze : répond à evaluate en moins de 500ms */
async function isResponsive(page) {
  try {
    const start = Date.now();
    await page.evaluate(() => document.title);
    return Date.now() - start < 500;
  } catch {
    return false;
  }
}

/** Vérifie qu'il n'y a pas de .pv-item.active parasite au niveau 0 */
async function hasSpuriousActive(page) {
  return page.evaluate(() => {
    return document.querySelectorAll('#panel-viewport .pv-item.active').length > 0;
  });
}

// ─── Tests ───────────────────────────────────────────────────────────────────

async function runTests() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security',
           '--allow-file-access-from-files'],
  });

  try {
    const page = await browser.newPage();

    // Supprimer les erreurs console non critiques (MapLibre CDN en offline)
    page.on('pageerror', err => {
      if (process.env.VERBOSE) console.warn('  [pageerror]', err.message.slice(0, 80));
    });

    await page.goto(HTML, { waitUntil: 'domcontentloaded', timeout: 15000 });

    // Attendre que NAV et Panel soient définis
    await page.waitForFunction(() => typeof NAV !== 'undefined' && typeof Panel !== 'undefined', { timeout: 5000 });

    // ─── Suite 1 : Chargement initial ────────────────────────────────────────
    await suite('Chargement initial', async () => {
      const level = await getPanelLevel(page);
      await assert(level === 0, 'NAV.state.level === 0 après chargement');

      const hasView = await waitForView(page, 2000);
      await assert(hasView, 'panel-viewport contient une vue après chargement');

      const breadcrumb = await page.$eval('#panel-breadcrumb', el => el.textContent);
      await assert(breadcrumb.includes('Alban Rouzaud'), 'Breadcrumb contient "Alban Rouzaud" au niveau 0');

      const spurious = await hasSpuriousActive(page);
      await assert(!spurious, 'Pas de .pv-item.active parasite au niveau 0');
    });

    // ─── Suite 2 : Navigation Cahier 1 ───────────────────────────────────────
    await suite('Navigation Cahier 1 — niveaux 0→1→2→3', async () => {
      // Clic sur Cahier 1
      await page.evaluate(() => NAV.go(1, { cahier: 1 }));
      await waitForTransitionEnd(page);

      let level = await getPanelLevel(page);
      await assert(level === 1, 'Niveau 1 après navigation vers Cahier 1');
      await assert(await isResponsive(page), 'Page responsive après clic cahier 1');

      // Attendre que toutes les transitions (y compris pending) soient terminées
      // Le pending nav peut prendre 2×210ms = ~420ms en plus
      await new Promise(r => setTimeout(r, 500));
      await waitForTransitionEnd(page, 2000);
      await new Promise(r => setTimeout(r, 50));
      const items = await countItems(page);
      await assert(items > 0, 'Des chapitres sont listés au niveau 1 (C1)');

      // Clic sur premier chapitre
      await page.evaluate(() => NAV.go(2, { cahier: 1, chapitre: 1 }));
      await waitForTransitionEnd(page);
      level = await getPanelLevel(page);
      await assert(level === 2, 'Niveau 2 après clic sur chapitre 1');
      await assert(await isResponsive(page), 'Page responsive après navigation niveau 2');

      // Clic sur première étape
      await page.evaluate(() => NAV.go(3, { cahier: 1, chapitre: 1, stopId: 1 }));
      await waitForTransitionEnd(page);
      level = await getPanelLevel(page);
      await assert(level === 3, 'Niveau 3 après clic sur étape 1');
      await assert(await isResponsive(page), 'Page responsive après navigation niveau 3');

      // Vérifier le contenu de la vue-étape
      const viewText = await page.$eval('#panel-viewport', el => el.textContent);
      await assert(viewText.includes('Lavelanet'), 'Vue-étape contient "Lavelanet"');
      await assert(!viewText.includes('introuvable'), 'Vue-étape ne contient pas "introuvable"');
    });

    // ─── Suite 3 : Retour arrière ─────────────────────────────────────────────
    await suite('Retour arrière niveau 3→2→1→0', async () => {
      // Retour au niveau 2
      await page.evaluate(() => NAV.go(2, { cahier: 1, chapitre: 1 }, 'back'));
      await waitForTransitionEnd(page);
      let level = await getPanelLevel(page);
      await assert(level === 2, 'Retour niveau 2 OK');
      await assert(await isResponsive(page), 'Page responsive après retour niveau 2');

      // Attendre stabilisation du DOM après retour (scrollIntoView dans setTimeout 210ms)
      await new Promise(r => setTimeout(r, 300));
      const hasActive = await page.evaluate(() =>
        document.querySelectorAll('#panel-viewport .pv-item.active').length > 0
      );
      await assert(hasActive, 'Un item .active présent après retour (FR-1.4)');

      // Retour niveau 1
      await page.evaluate(() => NAV.go(1, { cahier: 1 }, 'back'));
      await waitForTransitionEnd(page);
      level = await getPanelLevel(page);
      await assert(level === 1, 'Retour niveau 1 OK');

      // Retour niveau 0
      await page.evaluate(() => NAV.go(0, null, 'back'));
      await waitForTransitionEnd(page);
      level = await getPanelLevel(page);
      await assert(level === 0, 'Retour niveau 0 OK');

      const spurious = await hasSpuriousActive(page);
      await assert(!spurious, 'Pas de .pv-item.active parasite après retour niveau 0');
    });

    // ─── Suite 4 : Clics répétés (détection freeze) ───────────────────────────
    await suite('Clics répétés rapides — détection freeze', async () => {
      // Naviguer rapidement 3 fois de suite sans attendre la transition
      await page.evaluate(() => {
        NAV.go(1, { cahier: 1 });
        NAV.go(2, { cahier: 1, chapitre: 1 });
        NAV.go(3, { cahier: 1, chapitre: 1, stopId: 1 });
      });

      // Attendre que la dernière transition + pending nav se finissent
      const ended = await waitForTransitionEnd(page, 3000);
      await assert(ended, 'Transitions concurrentes : _transitioning libéré en < 2s');
      await assert(await isResponsive(page), 'Page responsive après clics rapides');

      // Vérifier que le niveau final est 3 (la dernière go() a pris effet ou a été queued)
      const level = await getPanelLevel(page);
      await assert(level === 3, 'État final cohérent après clics rapides (level=3)');

      // Deuxième salve de clics rapides
      await page.evaluate(() => {
        NAV.go(2, { cahier: 1, chapitre: 2 }, 'back');
        NAV.go(1, { cahier: 1 }, 'back');
        NAV.go(2, { cahier: 1, chapitre: 3 });
      });
      await waitForTransitionEnd(page, 2000);
      await assert(await isResponsive(page), 'Page responsive après deuxième salve de clics');
    });

    // ─── Suite 5 : Navigation tous les cahiers ─────────────────────────────────
    await suite('Navigation cahiers 2, 3, 4', async () => {
      for (const c of [2, 3, 4]) {
        await page.evaluate((n) => NAV.go(0), c);
        await waitForTransitionEnd(page, 500);
        await page.evaluate((n) => NAV.go(1, { cahier: n }), c);
        await waitForTransitionEnd(page);

        const level = await getPanelLevel(page);
        await assert(level === 1, 'Niveau 1 après nav vers Cahier ' + c);
        await assert(await isResponsive(page), 'Page responsive Cahier ' + c);

        await new Promise(r => setTimeout(r, 50)); // stabilisation DOM
        const items = await countItems(page);
        await assert(items > 0, 'Des chapitres listés pour Cahier ' + c);

        // Clic sur premier chapitre du cahier
        const firstPhase = await page.evaluate((n) => {
          const cd = [null, CAHIER_1_DATA, CAHIER_2_DATA, CAHIER_3_DATA, CAHIER_4_DATA][n];
          const phases = Object.keys(cd.PN || {}).map(Number).sort((a,b)=>a-b);
          return phases[0];
        }, c);

        if (firstPhase) {
          await page.evaluate((n, p) => NAV.go(2, { cahier: n, chapitre: p }), c, firstPhase);
          await waitForTransitionEnd(page);
          const l2 = await getPanelLevel(page);
          await assert(l2 === 2, 'Niveau 2 OK Cahier ' + c + ' phase ' + firstPhase);

          // Premier stop du cahier
          const firstStop = await page.evaluate((n, p) => {
            const cd = [null, CAHIER_1_DATA, CAHIER_2_DATA, CAHIER_3_DATA, CAHIER_4_DATA][n];
            const stop = (cd.stops || []).find(s => s.p === p);
            return stop ? stop.id : null;
          }, c, firstPhase);

          if (firstStop) {
            await page.evaluate((n, p, s) => NAV.go(3, { cahier: n, chapitre: p, stopId: s }), c, firstPhase, firstStop);
            await waitForTransitionEnd(page);
            const l3 = await getPanelLevel(page);
            await assert(l3 === 3, 'Niveau 3 OK Cahier ' + c);

            const viewText = await page.$eval('#panel-viewport', el => el.textContent);
            await assert(!viewText.includes('introuvable'),
              'Vue-étape Cahier ' + c + ' stop ' + firstStop + ' : pas "introuvable"');
            await assert(await isResponsive(page), 'Page responsive après vue-étape Cahier ' + c);
          }
        }
      }
    });

    // ─── Suite 6 : Boutons ◀/▶ ───────────────────────────────────────────────
    await suite('Navigation ◀/▶ séquentielle', async () => {
      // Revenir au niveau 0 et init sequence
      await page.evaluate(() => { NAV.go(0); });
      await waitForTransitionEnd(page, 500);

      // ▶ x3
      for (let i = 0; i < 3; i++) {
        await page.evaluate(() => NAV.next());
        await waitForTransitionEnd(page, 1000);
      }
      await assert(await isResponsive(page), 'Page responsive après 3× next()');
      const level = await getPanelLevel(page);
      await assert(level === 3, 'Niveau 3 après 3× next()');

      // ◀ x2
      for (let i = 0; i < 2; i++) {
        await page.evaluate(() => NAV.prev());
        await waitForTransitionEnd(page, 1000);
      }
      await assert(await isResponsive(page), 'Page responsive après 2× prev()');
    });

    // ─── Suite 7 : Bouton settings ⚙ ─────────────────────────────────────────
    await suite('Bouton settings ⚙', async () => {
      const btnExists = await page.$('#settings-btn') !== null;
      await assert(btnExists, 'Le bouton #settings-btn existe');

      if (btnExists) {
        await page.click('#settings-btn');
        await new Promise(r => setTimeout(r, 100));
        const drawerOpen = await page.$eval('#settings-drawer', el => el.classList.contains('open'));
        await assert(drawerOpen, 'Drawer settings s\'ouvre au premier clic');

        // Deuxième clic sur le bouton settings (toggle)
        await page.click('#settings-btn');
        await new Promise(r => setTimeout(r, 100));
        const drawerClosed = await page.$eval('#settings-drawer', el => !el.classList.contains('open'));
        await assert(drawerClosed, 'Drawer settings se ferme au deuxième clic');

        await assert(await isResponsive(page), 'Page responsive après toggle settings');
      }
    });

  } finally {
    await browser.close();
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────
runTests().then(() => {
  console.log('\n' + '─'.repeat(50));
  const total = passed + failed;
  console.log(passed + '/' + total + ' tests E2E passés' +
    (failed > 0 ? '  ← ' + failed + ' ÉCHEC(S)\n  ' + errors.join('\n  ') : '  ✓ tout OK'));
  process.exit(failed > 0 ? 1 : 0);
}).catch(err => {
  console.error('\nErreur fatale E2E:', err.message);
  process.exit(1);
});
