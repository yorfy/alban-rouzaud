// data_c4.js — Données Cahier 4 : Captivité, Récits et Réflexions (1940–1945)

var CAHIER_4_DATA = {
  PC: {
  1: '#3498db',   // bleu — lieux de captivité
  2: '#8e44ad'    // violet — lieux évoqués dans les textes
},
  PN: {
  1: 'Lieux de captivité',
  2: 'Lieux évoqués dans les récits'
},
  stops: [

  // ── Phase 1 : Lieux de captivité ─────────────────────────────────

  {
    id: 401, p: 1,
    n: "Bains-les-Bains — Camp de rassemblement",
    lat: 47.9974, lng: 6.2715,
    date: "Juin 1940",
    d: "Camp de rassemblement initial après la capture. « Cinquante à soixante mille parqués dans les prés qui bordent la coquette station thermale de Bains-les-Bains où la guerre a passé. » Alban y décrit la promiscuité, la faim et le spectacle de la foule en déroute.",
    q: "Un quart de lentilles par homme pour la journée et une boule de pain à sept à huit pour deux ou trois jours.",
    type: "retour"
  },

  {
    id: 402, p: 1,
    n: "Épinal — Camp de transit",
    lat: 48.1782, lng: 6.4518,
    date: "Juillet – Août 1940",
    d: "Camp de transit à Épinal. Alban y observe les premières scènes de captivité : le marché au pain (« cinq cents francs la boule »), la foire aux jeux clandestins (« Misez ! Faites vos jeux ! »), le chat qui faillit être mangé. C'est là qu'André attrape ses vingt-sept poux.",
    q: "André se gratte. — Tu en as attrapé ? — Oh ! non ! c'est le sang... — Deux jours après André, torse nu, prospecte les coutures de sa chemise. — Vingt-sept !",
    type: "retour"
  },

  {
    id: 403, p: 1,
    n: "Kaisersteinbrück — Stalag de transit (Autriche)",
    lat: 47.9965, lng: 16.7803,
    date: "Août 1940",
    d: "Stalag de transit à Kaisersteinbrück (Basse-Autriche), sur le chemin vers l'Allemagne. « Un vent aigrelet chasse d'un coin de pelouse les baigneurs de soleil. » La faim, les files d'attente pour la gamelle, les projections de projecteurs la nuit. C'est ici que commence la véritable captivité en territoire allemand.",
    q: "Des couteaux, des rasoirs, un tas d'autres affaires qui ont échappé à trois ou quatre fouilles successives montent à des chiffres astronomiques ou sont échangés contre un nombre dérisoire de biscuits.",
    type: "retour"
  },

  {
    id: 404, p: 1,
    n: "Güssing — Arbeitskommando (Burgenland, Autriche)",
    lat: 47.0529, lng: 16.3297,
    date: "Septembre – Octobre 1940",
    d: "Arbeitskommando à Güssing (Burgenland). Alban y note les petites scènes du quotidien : la cigarette de tabac de noyer ramassée sous les arbres, les feuilles de papier qu'on se dispute. « Là-bas, sous le noyer. Mais ne t'ébruite pas trop… » Un univers de débrouille et de solidarité précaire.",
    q: "Tabac... à la noix ! — En bourres-tu une ? — Il a une drôle de gueule, ton tabac ! — Goûte-le, tu m'en diras des nouvelles !",
    type: "kommando"
  },

  {
    id: 405, p: 1,
    n: "Steiermark — Kommandos agricoles (Styrie, Autriche)",
    lat: 47.237, lng: 15.687,
    date: "1940 – 1941",
    d: "Les Kommandos agricoles de Styrie, région des « Baouah » (paysans autrichiens). Alban décrit en détail la cohabitation avec les fermiers, le travail dans les fermes, les repas en commun, et la philosophie du bon prisonnier : « le Baouah aime le prisonnier français. » C'est depuis ces Kommandos que l'évasion du Cahier 3 a été préparée.",
    q: "Le Baouah n'en revient pas et congratule : « Gut arbeit ! Gut arbeit ! » — À la façon dont on dit : ça va ? le prisonnier réplique : Ja gueule.",
    type: "kommando"
  },

  {
    id: 406, p: 1,
    n: "Stalag XVIII D — Marburg an der Drau (Maribor)",
    lat: 46.5547, lng: 15.6467,
    date: "Nov. – Déc. 1941",
    d: "Le Stalag XVIII D à Marburg an der Drau (Maribor, Slovénie) est le lieu d'écriture de tout le Cahier 4. Alban y est de retour après sa recapture en Italie. Six textes portent la date de Marburg : du 25 nov. au 9 déc. 1941. C'est ici qu'il rédige ses réflexions sur la guerre, les Chleuhs, la captivité et la fête de Noël au stalag.",
    q: "Maintenant on est ici à en causer, bien entre nous, ou à en méditer, bien à part nous, dans les chambres-clapiers des stalags, enfumées, empestées, bruyantes.",
    type: "retour"
  },

  // ── Phase 2 : Lieux évoqués dans les récits ──────────────────────

  {
    id: 407, p: 2,
    n: "Lavelanet (Ariège) — Pays natal",
    lat: 42.9372, lng: 1.8478,
    date: "Évoqué dans les réflexions",
    d: "Lavelanet, en Ariège, est le berceau d'Alban Rouzaud, instituteur ariégeois. Non mentionné explicitement dans le Cahier 4 mais présent en filigrane dans toutes ses réflexions sur la paix, le retour et la vie ordinaire. La mention des « pentes enneigées » et des cahiers vierges dans le texte « Histoire de Pages » renvoie à son monde pyrénéen.",
    q: "Les feuilles blanches, je pourrais les comparer à un magnifique panorama de pentes enneigées devant lesquels je reste en contemplation.",
    type: "mention"
  },

  {
    id: 408, p: 2,
    n: "France (front de mai – juin 1940)",
    lat: 49.5, lng: 3.5,
    date: "Évoqué dans « Pages d'Histoire »",
    d: "Alban évoque longuement la débâcle de mai-juin 1940 : les Allemands qui enfoncent la Belgique, les régiments anéantis, l'absence des avions français, et la capitulation vécue comme inévitable. « C'était la fin des haricots. C'est nous qui étions dans la poche. Bel et bien. »",
    q: "On cherchait vainement dans le ciel les avions français ou anglais. Les derniers Tommies avaient quitté le Continent.",
    type: "mention"
  }
],
  cpa: [],
  staticRoutes: [],
  elevProfile: [],
  bounds: {
    cahier: [[1.8478, 42.9372], [16.7803, 49.5]],
    phases: {
      "1": [[6.2715, 46.5547], [16.7803, 48.1782]],
      "2": [[1.8478, 42.9372], [3.5, 49.5]]
    }
  },
  pins: {
    "1": { lat: 47.37,  lng: 11.52 },
    "2": { lat: 46.02,  lng: 2.67  }
  }
};
