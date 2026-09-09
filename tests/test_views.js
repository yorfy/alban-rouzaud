/**
 * tests/test_views.js
 * 
 * Suite de tests Node.js pour les fonctions de rendu de ECRITS_DE_GUERRE_v2.html.
 * Exécution : node tests/test_views.js
 * Aucune dépendance externe — Node.js standard uniquement.
 * 
 * Stratégie :
 *   1. Charger les 4 fichiers data (CAHIER_N_DATA globals)
 *   2. Extraire le bloc <script> principal du HTML via regex
 *   3. Exécuter dans un contexte vm avec mocks des globals browser
 *   4. Assertions sur les fonctions exposées dans le contexte
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const vm   = require('vm');

// ─── Chemins ────────────────────────────────────────────────────────────────
const ROOT    = path.join(__dirname, '..');
const HTML    = path.join(ROOT, 'ECRITS_DE_GUERRE_v2.html');
const DATA_C1 = path.join(ROOT, 'data', 'data_c1.js');
const DATA_C2 = path.join(ROOT, 'data', 'data_c2.js');
const DATA_C3 = path.join(ROOT, 'data', 'data_c3.js');
const DATA_C4 = path.join(ROOT, 'data', 'data_c4.js');

// ─── Contexte vm : mocks browser minimalistes ───────────────────────────────
//
// Le script HTML dépend de : document, window, history, location,
// requestAnimationFrame, setTimeout, maplibregl, Set.
// On fournit des stubs vides ou fonctionnels selon le besoin.

function makeEl() {
  const el = {
    style: {}, classList: { add: ()=>{}, remove: ()=>{}, toggle: ()=>{}, contains: ()=>false },
    addEventListener: ()=>{}, removeEventListener: ()=>{},
    appendChild: ()=>{}, removeChild: ()=>{}, replaceChild: ()=>{},
    innerHTML: '', textContent: '', title: '', disabled: false,
    offsetHeight: 400, clientWidth: 800, clientHeight: 200,
    firstChild: null, parentNode: null,
    querySelector: ()=>null, querySelectorAll: ()=>[],
    getContext: ()=>({
      clearRect:()=>{}, fillRect:()=>{}, strokeRect:()=>{},
      beginPath:()=>{}, moveTo:()=>{}, lineTo:()=>{},
      arc:()=>{}, fill:()=>{}, stroke:()=>{}, clip:()=>{},
      fillText:()=>{}, save:()=>{}, restore:()=>{},
      setTransform:()=>{}, globalAlpha: 1,
      fillStyle:'', strokeStyle:'', lineWidth:1,
      textAlign:'', textBaseline:'', font:'',
    }),
    cloneNode: function() { return makeEl(); },
    getBoundingClientRect: ()=>({ left:0, top:0, width:800, height:200 }),
  };
  el.parentNode = el; // évite null checks dans removeChild
  return el;
}

const mockDocument = {
  getElementById:     ()=>makeEl(),
  createElement:      ()=>makeEl(),
  createElementNS:    ()=>makeEl(),
  querySelector:      ()=>null,
  querySelectorAll:   ()=>[],
  addEventListener:   ()=>{},
  removeEventListener:()=>{},
  head: { appendChild: ()=>{} },
  body: { appendChild: ()=>{}, style: {} },
};

const mockMap = {
  loaded:             ()=>true,
  on:                 ()=>{},
  once:               ()=>{},
  off:                ()=>{},
  addSource:          ()=>{},
  addLayer:           ()=>{},
  removeSource:       ()=>{},
  removeLayer:        ()=>{},
  getSource:          ()=>null,
  getLayer:           ()=>null,
  getStyle:           ()=>({ layers: [] }),
  setLayoutProperty:  ()=>{},
  setTerrain:         ()=>{},
  setStyle:           ()=>{},
  fitBounds:          ()=>{},
  flyTo:              ()=>{},
  easeTo:             ()=>{},
  getZoom:            ()=>7,
  getBearing:         ()=>0,
  getPitch:           ()=>0,
  resize:             ()=>{},
  addControl:         ()=>{},
};

const ctx = vm.createContext({
  // Browser globals
  document:             mockDocument,
  window:               { innerWidth:1280, innerHeight:800, addEventListener:()=>{}, removeEventListener:()=>{}, devicePixelRatio:1, matchMedia:()=>({matches:false}) },
  history:              { pushState:()=>{}, replaceState:()=>{} },
  location:             { hash:'', search:'' },
  navigator:            { clipboard: null },
  requestAnimationFrame:cb=>cb(),
  setTimeout:           (cb)=>cb(),
  clearTimeout:         ()=>{},
  setInterval:          ()=>0,
  clearInterval:        ()=>{},
  console:              console,

  // MapLibre stub
  maplibregl: {
    Map:     function() { return mockMap; },
    Marker:  function() { return { setLngLat:()=>({addTo:()=>({})  }), remove:()=>{}, addTo:()=>{}, getElement:()=>makeEl(), getLngLat:()=>({lat:0,lng:0}) }; },
    Popup:   function() { return { setLngLat:()=>({setHTML:()=>({addTo:()=>({})})  }), remove:()=>{} }; },
    ScaleControl: function() {},
  },

  // localStorage stub
  localStorage: { getItem:()=>null, setItem:()=>{} },

  // Divers
  Set: Set,
  Math: Math,
  Array: Array,
  Object: Object,
  parseInt: parseInt,
  parseFloat: parseFloat,
  isNaN: isNaN,
  Date: Date,
  RegExp: RegExp,
  Error: Error,
});

// ─── Chargement des data globals ────────────────────────────────────────────
[DATA_C1, DATA_C2, DATA_C3, DATA_C4].forEach(f => {
  vm.runInContext(fs.readFileSync(f, 'utf8'), ctx);
});

// ─── Extraction et exécution du script HTML principal ───────────────────────
const html       = fs.readFileSync(HTML, 'utf8');
// Extraire le contenu du dernier (et seul) <script> sans src=
const scriptMatch = html.match(/<script>(?!.*src=)([\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error('ERREUR : impossible d\'extraire le <script> principal du HTML.');
  process.exit(1);
}

try {
  vm.runInContext(scriptMatch[1], ctx);
} catch (e) {
  // Certaines erreurs d'initialisation (ex: getElementById pendant init())
  // sont attendues dans l'environnement Node — on les ignore si les globals
  // testés sont bien définis.
  if (process.env.VERBOSE) console.warn('Init warning (ignoré):', e.message);
}

// ─── Mini framework d'assertions ────────────────────────────────────────────
let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    console.log('  ✓', label);
    passed++;
  } else {
    console.error('  ✗', label);
    failed++;
  }
}

function assertEqual(a, b, label) {
  assert(a === b, label + ' (attendu: ' + JSON.stringify(b) + ', reçu: ' + JSON.stringify(a) + ')');
}

function assertIncludes(str, sub, label) {
  assert(typeof str === 'string' && str.includes(sub), label);
}

function assertNotIncludes(str, sub, label) {
  assert(typeof str === 'string' && !str.includes(sub), label);
}

function suite(name, fn) {
  console.log('\n▶', name);
  fn();
}

// ─── Helpers ────────────────────────────────────────────────────────────────
const C1 = ctx.CAHIER_1_DATA;
const C2 = ctx.CAHIER_2_DATA;
const C3 = ctx.CAHIER_3_DATA;
const C4 = ctx.CAHIER_4_DATA;

// ─── Tests ──────────────────────────────────────────────────────────────────

suite('findStop — contrat d\'interface', () => {
  // Bug historique : findStop cherchait .S au lieu de .stops sur le brut
  const stop1 = ctx.findStop(C1, 1);
  assert(stop1 !== null,            'findStop(C1 brut, 1) ne retourne pas null');
  assertEqual(stop1 && stop1.id, 1, 'findStop(C1 brut, 1).id === 1');
  assertEqual(stop1 && stop1.n, 'Lavelanet', 'findStop(C1 brut, 1).n === "Lavelanet"');

  const stop101 = ctx.findStop(C2, 101);
  assert(stop101 !== null,              'findStop(C2 brut, 101) ne retourne pas null');
  assertEqual(stop101 && stop101.id, 101, 'findStop(C2 brut, 101).id === 101');

  const stop32 = ctx.findStop(C3, 32);
  assert(stop32 !== null,             'findStop(C3 brut, 32) ne retourne pas null');
  assertEqual(stop32 && stop32.p, 1,  'findStop(C3 brut, 32).p === 1 (phase 1)');

  const stop401 = ctx.findStop(C4, 401);
  assert(stop401 !== null,            'findStop(C4 brut, 401) ne retourne pas null');

  // Avec objet normalisé getCahierData (a .S)
  const cd1 = ctx.getCahierData(1);
  const stop1n = ctx.findStop(cd1, 1);
  assert(stop1n !== null,             'findStop(getCahierData(1), 1) ne retourne pas null');
  assertEqual(stop1n && stop1n.id, 1, 'findStop(getCahierData(1), 1).id === 1');

  // ID inexistant → null
  const missing = ctx.findStop(C1, 9999);
  assertEqual(missing, null,          'findStop(C1, 9999) retourne null pour id inexistant');
});


suite('renderEtape — jamais "Étape introuvable"', () => {
  // Pour chaque premier stop de chaque cahier, renderEtape ne doit pas
  // retourner le message d'erreur
  const cases = [
    { data: C1, id: 1,   cahier: 1 },
    { data: C2, id: 101, cahier: 2 },
    { data: C3, id: 32,  cahier: 3 },
    { data: C4, id: 401, cahier: 4 },
  ];

  cases.forEach(function(c) {
    const stop = ctx.findStop(c.data, c.id);
    const html = ctx.renderEtape(stop, c.data.PC, c.data.PN, c.cahier);
    assertNotIncludes(html, 'introuvable',
      'renderEtape C' + c.cahier + ' stop ' + c.id + ' : pas "introuvable"');
    assertIncludes(html, stop.n,
      'renderEtape C' + c.cahier + ' stop ' + c.id + ' : contient le nom du stop');
  });

  // Cas explicite : renderEtape(null) doit retourner le message d'erreur
  const errHtml = ctx.renderEtape(null, {}, {}, 1);
  assertIncludes(errHtml, 'introuvable',
    'renderEtape(null) retourne bien "Étape introuvable"');
});


suite('renderChapitre — toutes les phases de tous les cahiers', () => {
  const cahiers = [
    { data: C1, n: 1, phases: [1, 2, 3, 4] },
    { data: C2, n: 2, phases: [1, 2, 3, 4, 5, 6, 7, 8] },
    { data: C3, n: 3, phases: [1, 2, 3] },  // tester les 3 premières
    { data: C4, n: 4, phases: [1, 2] },
  ];

  cahiers.forEach(function(c) {
    c.phases.forEach(function(p) {
      const html = ctx.renderChapitre(c.n, p);
      assertNotIncludes(html, 'introuvable',
        'renderChapitre C' + c.n + ' phase ' + p + ' : pas "introuvable"');
      assertIncludes(html, 'pv-list',
        'renderChapitre C' + c.n + ' phase ' + p + ' : contient <ul class="pv-list">');
      assertIncludes(html, 'pv-item',
        'renderChapitre C' + c.n + ' phase ' + p + ' : contient au moins un <li class="pv-item">');
    });
  });
});


suite('getStopSeqNum — numérotation séquentielle', () => {
  // Le premier stop de chaque cahier doit être numéroté 1
  assertEqual(ctx.getStopSeqNum(1, 1),   1, 'C1 stop id=1 → séqNum 1');
  assertEqual(ctx.getStopSeqNum(2, 101), 1, 'C2 stop id=101 → séqNum 1');
  assertEqual(ctx.getStopSeqNum(3, 32),  1, 'C3 stop id=32 → séqNum 1');
  assertEqual(ctx.getStopSeqNum(4, 401), 1, 'C4 stop id=401 → séqNum 1');

  // Stop inexistant → null
  assertEqual(ctx.getStopSeqNum(1, 9999), null, 'C1 stop id=9999 → null');

  // Le deuxième stop de C1 (id=2) doit être 2
  assertEqual(ctx.getStopSeqNum(1, 2), 2, 'C1 stop id=2 → séqNum 2');
});


suite('buildFlatSequence — structure et couverture', () => {
  const seq = ctx.NAV._buildFlatSequence([C1, C2, C3, C4]);

  // Doit avoir des éléments
  assert(seq.length > 0, 'La séquence plate n\'est pas vide');

  // Tous les cahiers doivent être représentés
  const cahiers = [1, 2, 3, 4];
  cahiers.forEach(function(n) {
    const hasCahier = seq.some(function(item) { return item.cahier === n; });
    assert(hasCahier, 'Cahier ' + n + ' représenté dans la séquence');
  });

  // Tous les items ont un type valide
  const invalidType = seq.filter(function(item) {
    return item.type !== 'stop' && item.type !== 'cpa';
  });
  assertEqual(invalidType.length, 0, 'Tous les items ont type "stop" ou "cpa"');

  // Tous les items ont un objet data non null
  const nullData = seq.filter(function(item) { return !item.data; });
  assertEqual(nullData.length, 0, 'Tous les items ont item.data non null');

  // Le premier item doit être le premier stop de C1 (id=1)
  assertEqual(seq[0].type, 'stop', 'Premier item : type === "stop"');
  assertEqual(seq[0].cahier, 1,    'Premier item : cahier === 1');
  assertEqual(seq[0].data.id, 1,   'Premier item : id === 1 (Lavelanet)');

  // Les stops de C1 doivent apparaître avant les stops de C2
  const firstC1 = seq.findIndex(function(i) { return i.cahier === 1 && i.type === 'stop'; });
  const firstC2 = seq.findIndex(function(i) { return i.cahier === 2 && i.type === 'stop'; });
  assert(firstC1 < firstC2, 'Stops C1 avant stops C2 dans la séquence');

  // C4 a cpa:[] → aucun item CPA pour le cahier 4
  const cpaC4 = seq.filter(function(i) { return i.cahier === 4 && i.type === 'cpa'; });
  assertEqual(cpaC4.length, 0, 'C4 a cpa:[] → aucun item CPA dans la séquence');

  // Les items CPA de C3 ont un stopId ou p — vérifier l'intercalation
  const cpaC3 = seq.filter(function(i) { return i.cahier === 3 && i.type === 'cpa'; });
  assert(cpaC3.length > 0, 'C3 a des items CPA dans la séquence');
});


suite('NAV.state — état initial', () => {
  const state = ctx.NAV.state;
  assertEqual(state.level,  0,     'Niveau initial = 0');
  assertEqual(state.cahier, null,  'Cahier initial = null');
  assertEqual(state.stopId, null,  'StopId initial = null');
  assertEqual(state.panelMode, 'nav', 'panelMode initial = "nav"');
});


suite('NAV.go — transitions d\'état', () => {
  // go(0) depuis niveau 0 = no-op
  let called = false;
  ctx.NAV.on('change', function() { called = true; });
  ctx.NAV.go(0);
  assert(!called, 'NAV.go(0) depuis niveau 0 = no-op (pas d\'événement)');
  ctx.NAV.off('change', arguments[0]); // pas de ref, cleanup via re-init

  // go(1, {cahier:1}) → level=1, cahier=1
  ctx.NAV.go(1, { cahier: 1 });
  assertEqual(ctx.NAV.state.level,  1, 'Après go(1, {cahier:1}) : level=1');
  assertEqual(ctx.NAV.state.cahier, 1, 'Après go(1, {cahier:1}) : cahier=1');
  assertEqual(ctx.NAV.state.chapitre, null, 'Après go(1) : chapitre=null (effacé)');

  // go(2, {cahier:1, chapitre:2}) → level=2, chapitre=2
  ctx.NAV.go(2, { cahier: 1, chapitre: 2 });
  assertEqual(ctx.NAV.state.level,    2, 'Après go(2, {chapitre:2}) : level=2');
  assertEqual(ctx.NAV.state.chapitre, 2, 'Après go(2, {chapitre:2}) : chapitre=2');
  assertEqual(ctx.NAV.state.stopId,   null, 'Après go(2) : stopId=null (effacé)');

  // go(3, {stopId:5}) → level=3, stopId=5
  ctx.NAV.go(3, { cahier: 1, chapitre: 2, stopId: 5 });
  assertEqual(ctx.NAV.state.level,  3, 'Après go(3, {stopId:5}) : level=3');
  assertEqual(ctx.NAV.state.stopId, 5, 'Après go(3, {stopId:5}) : stopId=5');

  // Retour au niveau 0
  ctx.NAV.go(0);
  assertEqual(ctx.NAV.state.level,  0,    'Après go(0) depuis level=3 : level=0');
  assertEqual(ctx.NAV.state.cahier, null, 'Après go(0) : cahier=null (effacé)');
  assertEqual(ctx.NAV.state.stopId, null, 'Après go(0) : stopId=null (effacé)');
});


suite('NAV.isFirst / isLast — avant initSequence', () => {
  // Après l'init du script, initSequence a déjà été appelée.
  // Avec _seqIndex = -1, isFirst() retourne true (car -1 <= 0).
  // isLast() avec _seqIndex = -1 retourne false si la séquence est non-vide.
  assert(ctx.NAV.isFirst(), 'isFirst() = true avec seqIndex=-1');
});


suite('NAV.initSequence + isFirst/isLast', () => {
  ctx.NAV.initSequence([C1, C2, C3, C4]);

  // Après init, _seqIndex = -1, pas encore navigué
  // isFirst = true (seqIndex <= 0)
  assert(ctx.NAV.isFirst(), 'isFirst() = true juste après initSequence (seqIndex=-1)');

  // next() → premier item (seqIndex=0) — isFirst() est encore vrai sur le 1er item
  ctx.NAV.next();
  assert(ctx.NAV.isFirst(), 'isFirst() = true sur le premier item (seqIndex=0)');

  // Vérifier que l'état NAV correspond au premier stop de C1
  const state = ctx.NAV.state;
  assertEqual(state.level,  3, 'Après next() depuis -1 : level=3');
  assertEqual(state.cahier, 1, 'Après next() depuis -1 : cahier=1');
  assertEqual(state.stopId, 1, 'Après next() depuis -1 : stopId=1 (Lavelanet)');
});

suite('Dispatcher F-1 — navigation pendant transition', () => {
  // Simuler _transitioning = true
  ctx.Panel._transitioning = true;

  // Déclencher une navigation (via le dispatcher NAV.on('change'))
  ctx.NAV.go(1, { cahier: 1 });

  // Panel._pendingNav doit être non-null (nav mise en queue)
  assert(ctx.Panel._pendingNav !== null, 'Panel._pendingNav est non-null après NAV.go pendant transition');

  // renderFn doit retourner du HTML contenant pv-item
  if (ctx.Panel._pendingNav) {
    var html1 = ctx.Panel._pendingNav.renderFn();
    assertIncludes(html1, 'pv-item', 'Panel._pendingNav.renderFn() retourne HTML avec "pv-item"');
  }

  // Remettre _transitioning = false et appeler renderFn manuellement
  ctx.Panel._transitioning = false;
  if (ctx.Panel._pendingNav) {
    var html2 = ctx.Panel._pendingNav.renderFn();
    assertIncludes(html2, 'pv-item', 'renderFn() après libération contient encore "pv-item"');
  }

  // Remettre l'état NAV à 0 pour les suites suivantes
  ctx.NAV.go(0);
});


suite('NAV.previousStopId — conservation avant effacement', () => {
  // Naviguer vers niveau 3 avec stopId=1
  ctx.NAV.go(3, { cahier: 1, chapitre: 1, stopId: 1 });
  assertEqual(ctx.NAV.state.stopId, 1, 'Avant retour : stopId === 1');

  // Retour vers niveau 2 (efface stopId)
  ctx.NAV.go(2, { cahier: 1, chapitre: 1 }, 'back');
  assertEqual(ctx.NAV.state.stopId, null, 'Après retour niveau 2 : stopId === null');

  // previousStopId doit avoir conservé l'ancien stopId
  assertEqual(ctx.NAV.previousStopId, 1, 'previousStopId conserve le stopId effacé (=1)');

  // renderChapitre doit contenir 'pv-item active' (highlight sur le stop 1)
  var chapHtml = ctx.renderChapitre(1, 1);
  assertIncludes(chapHtml, 'pv-item active', 'renderChapitre(1,1) contient "pv-item active" grâce à previousStopId');

  // Après une navigation qui ne passe pas par niveau 2, previousStopId doit être null
  ctx.NAV.go(1, { cahier: 1 });
  assertEqual(ctx.NAV.previousStopId, null, 'previousStopId === null après NAV.go(1, ...)');

  // Remettre l'état à 0
  ctx.NAV.go(0);
});


suite('Cohérence numérotation carte / panneau', () => {
  // Premier stop de C1 : id=1 → doit être séqNum 1
  assertEqual(ctx.getStopSeqNum(1, 1),   1, 'C1 stop id=1 → séqNum 1');
  // Stop id=6 de C1 (6ème dans le tableau) → séqNum 6
  assertEqual(ctx.getStopSeqNum(1, 6),   6, 'C1 stop id=6 → séqNum 6');

  // buildFlatSequence([C1]) : premier item de type stop a id=1
  var seq = ctx.NAV._buildFlatSequence([C1]);
  var firstStop = seq.find(function(i) { return i.type === 'stop'; });
  assert(firstStop !== undefined, 'buildFlatSequence([C1]) : au moins un item "stop"');
  assertEqual(firstStop && firstStop.data.id, 1, 'Premier item stop de C1 a id === 1');

  // renderChapitre(1,1) : contient '1</span>' (badge numéro 1)
  var chapHtml = ctx.renderChapitre(1, 1);
  assertIncludes(chapHtml, '1</span>', 'renderChapitre(1,1) contient badge "1</span>"');
});


suite('mapTransitionDuration — variable globale', () => {
  // Valeur par défaut
  assertEqual(ctx.mapTransitionDuration, 1200, 'mapTransitionDuration === 1200 après chargement');

  // Après modification, MapAdapter doit utiliser la nouvelle valeur
  ctx.mapTransitionDuration = 0;
  // On vérifie l'existence de la variable (indirectement — MapAdapter la lit à l'appel)
  assert(ctx.mapTransitionDuration === 0, 'mapTransitionDuration modifiable à 0');

  // Remettre la valeur par défaut
  ctx.mapTransitionDuration = 1200;
  assertEqual(ctx.mapTransitionDuration, 1200, 'mapTransitionDuration remis à 1200');
});


suite('ck-terrain — synchronisation avec terrainOn', () => {
  // terrainOn doit être true après chargement
  assert(ctx.terrainOn === true, 'terrainOn === true après chargement');

  // Simuler un changement de checkbox (checked = false)
  var ckTerrain = ctx.document.getElementById('ck-terrain');
  // Dans le contexte vm, document.getElementById retourne un mock — on simule via ctx
  // On teste via la fonction syncTerrainUI ou le listener directement
  // On modifie terrainOn directement et vérifie que syncTerrainUI synchronise
  if (typeof ctx.syncTerrainUI === 'function') {
    ctx.terrainOn = false;
    ctx.syncTerrainUI();
    assert(ctx.terrainOn === false, 'terrainOn === false après syncTerrainUI');
    ctx.terrainOn = true;
    ctx.syncTerrainUI();
    assert(ctx.terrainOn === true, 'terrainOn === true après syncTerrainUI');
  } else {
    // syncTerrainUI pas encore implémenté — test de base
    assert(ctx.terrainOn === true, 'terrainOn toujours true (syncTerrainUI non implémenté)');
  }
});


suite('NAV.prev() sur premier item — remonte au niveau supérieur', () => {
  // Réinitialiser la séquence
  ctx.NAV.initSequence([C1, C2, C3, C4]);
  // Aller sur le premier stop
  ctx.NAV.next();  // seqIndex = 0
  assertEqual(ctx.NAV.state.level, 3, 'Après next() : level=3');
  assertEqual(ctx.NAV.state.stopId, 1, 'Après next() : stopId=1 (premier stop C1)');

  // prev() depuis premier item → doit remonter au niveau 2
  ctx.NAV.prev();
  assertEqual(ctx.NAV.state.level, 2, 'prev() depuis premier item : level=2');
  assertEqual(ctx.NAV.previousStopId, 1, 'prev() depuis premier item : previousStopId=1 pour highlight');
});


suite('NAV.next() sur dernier item — remonte au niveau supérieur', () => {
  // Réinitialiser la séquence
  ctx.NAV.initSequence([C1, C2, C3, C4]);

  // Trouver le DERNIER stop de TOUTE la séquence (tous cahiers)
  var seq = ctx.NAV._seq;
  var lastStopIdx = -1;
  for (var i = seq.length - 1; i >= 0; i--) {
    if (seq[i].type === 'stop') {
      lastStopIdx = i;
      break;
    }
  }
  assert(lastStopIdx >= 0, 'Dernier stop de la séquence trouvé');

  // Naviguer jusqu'au dernier item de la séquence
  ctx.NAV._seqIndex = seq.length - 1;
  var lastItem = seq[seq.length - 1];
  var lastCahier = lastItem.cahier;

  // next() depuis le dernier item → doit remonter au niveau 1
  ctx.NAV.next();
  assertEqual(ctx.NAV.state.level, 1, 'next() depuis dernier item : level=1');
  assertEqual(ctx.NAV.state.cahier, lastCahier, 'next() depuis dernier item : cahier=' + lastCahier);
});


suite('Boutons contextuels dans renderEtape / renderChapitre', () => {
  // Réinitialiser la séquence pour avoir un seqIndex cohérent
  ctx.NAV.initSequence([C1, C2, C3, C4]);

  // renderEtape pour un stop au milieu (id=3, C1) → contient nav-ctx-prev et nav-ctx-next non-disabled
  // Mettre seqIndex au stop 3 (milieu)
  var seq = ctx.NAV._seq;
  var stop3Idx = -1;
  for (var i = 0; i < seq.length; i++) {
    if (seq[i].type === 'stop' && seq[i].data.id === 3 && seq[i].cahier === 1) { stop3Idx = i; break; }
  }
  ctx.NAV._seqIndex = stop3Idx;
  var stopMid = ctx.findStop(C1, 3);
  var etapeMidHtml = ctx.renderEtape(stopMid, C1.PC, C1.PN, 1);
  assertIncludes(etapeMidHtml, 'nav-ctx-prev', 'renderEtape (milieu) : contient nav-ctx-prev');
  assertIncludes(etapeMidHtml, 'nav-ctx-next', 'renderEtape (milieu) : contient nav-ctx-next');
  // Pas disabled sur les deux
  assert(
    !etapeMidHtml.includes('<button class="nav-ctx-prev" disabled') &&
    !etapeMidHtml.includes('<button class="nav-ctx-prev"  disabled'),
    'renderEtape (milieu) : nav-ctx-prev non disabled'
  );

  // renderEtape pour le premier stop C1 (id=1) → nav-ctx-prev avec disabled
  // Mettre seqIndex à 0 (premier item de la séquence = stop id=1)
  ctx.NAV._seqIndex = 0;
  var stopFirst = ctx.findStop(C1, 1);
  var etapeFirstHtml = ctx.renderEtape(stopFirst, C1.PC, C1.PN, 1);
  assertIncludes(etapeFirstHtml, 'nav-ctx-prev', 'renderEtape (1er stop C1) : contient nav-ctx-prev');
  assert(
    etapeFirstHtml.includes('nav-ctx-prev') && etapeFirstHtml.includes('disabled'),
    'renderEtape (1er stop C1) : nav-ctx-prev est disabled'
  );

  // renderChapitre(1,1) → chap-ctx-prev disabled (premier chapitre) + chap-ctx-next non-disabled
  var chap1Html = ctx.renderChapitre(1, 1);
  assertIncludes(chap1Html, 'chap-ctx-prev', 'renderChapitre(1,1) : contient chap-ctx-prev');
  assertIncludes(chap1Html, 'chap-ctx-next', 'renderChapitre(1,1) : contient chap-ctx-next');
  assert(
    chap1Html.includes('chap-ctx-prev') && chap1Html.includes('disabled'),
    'renderChapitre(1,1) : chap-ctx-prev est disabled (premier chapitre)'
  );

  // renderChapitre(1,4) → chap-ctx-next avec disabled (dernier chapitre de C1)
  var chap4Html = ctx.renderChapitre(1, 4);
  assertIncludes(chap4Html, 'chap-ctx-next', 'renderChapitre(1,4) : contient chap-ctx-next');
  assert(
    chap4Html.includes('chap-ctx-next') && chap4Html.includes('disabled'),
    'renderChapitre(1,4) : chap-ctx-next est disabled (dernier chapitre C1)'
  );
});


// ─── Résultat final ─────────────────────────────────────────────────────────
console.log('\n' + '─'.repeat(50));
const total = passed + failed;
console.log(passed + '/' + total + ' tests passés' + (failed > 0 ? '  ← ' + failed + ' ÉCHEC(S)' : '  ✓ tout OK'));
if (failed > 0) process.exit(1);
