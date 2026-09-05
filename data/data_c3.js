// data_c3.js — Données Cahier 3 : L'Évasion (Sept.–Oct. 1941)

var CAHIER_3_DATA = {
  PC: {
    1: '#e94560',
    2: '#f5a623',
    3: '#2ecc71',
    4: '#3498db',
    5: '#9b59b6',
    6: '#e67e22',
    7: '#1abc9c',
    8: '#e74c3c',
    9: '#8e44ad'
},
  PN: {
    1: 'I \u2014 Le Chapeau \u00e0 Franz',
    2: 'II \u2014 \u00c0 ciel ouvert',
    3: 'III \u2014 Le Pont \u00e0 P\u00e9age',
    4: 'IV \u2014 Les Abreuvoirs',
    5: 'V \u2014 Les Bords de la Mur',
    6: 'VI \u2014 La Nuit tragique',
    7: 'VII \u2014 Tourisme',
    8: 'Evvira',
    9: '\u00c9pilogue'
},
  stops: [
    // Phase 1 — I. Le Chapeau à Franz
    {
        id: 32, p: 1,
        n: "Ferme Grabner",
        lat: 47.23845, lng: 15.69998,
        date: "20 sept. 1941 — dernier soir",
        d: "Dernier repas chez les Grabner. Le p\u00e8re Grabner, la pipe \u00e0 la main, est content de son prisonnier. Alban profite d\u2019un moment d\u2019inattention pour subtiliser le chapeau tyrolien de Franz sur l\u2019\u00e9tag\u00e8re \u00e0 vaisselle. \u00ab\u00a0Ouf\u00a0! je l\u2019ai\u00a0!\u00a0\u00bb Il embrasse le petit Ernst \u2014 \u00ab\u00a0Gute nacht, Ernsti\u00a0!\u00a0\u00bb \u2014 et d\u00e9vale le sentier \u00e0 travers pr\u00e9s vers le Kommando.",
        q: "Gute nacht, Ernsti !",
        type: "ferme"
    },
    // Phase 2 — II. À ciel ouvert
    {
        id: 1, p: 2,
        n: "Kommando de Hohenilz (Puch bei Weiz)",
        lat: 47.23764, lng: 15.68670,
        date: "20 sept. 1941 — vers 23h",
        d: "Baraquement collectif \u00e0 Hohenilz, commune de Puch bei Weiz. Andr\u00e9 et les copains pr\u00e9parent sacs, vivres, boussole et carte copi\u00e9e \u00e0 la main. La sentinelle se couche. Andr\u00e9 d\u00e9verrouille les portes, ils traversent la grange et sautent dans la nuit.",
        q: "Gute nacht ! Comme tous les soirs.",
        type: "kommando"
    },
    {
        id: 2, p: 2,
        n: "Weiz (travers\u00e9e nocturne, sortie nord-ouest)",
        lat: 47.2179, lng: 15.6284,
        date: "Nuit du 20 au 21 sept. — 1h du matin",
        d: "\u00c0 une heure du matin, les premi\u00e8res maisons de Weiz. Un civil les croise et se retourne. Au premier carrefour, \u00e0 droite ; 400\u00a0m plus loin, \u00e0 gauche vers le jardin public. Un couple d'amoureux. Plus loin de la jeunesse chante. Ils coupent \u00e0 travers pr\u00e9s, retrouvent la route qu'ils empruntaient matin et soir, foncent vers le \u00ab\u00a0village n\u00e8gre\u00a0\u00bb puis s'enfoncent dans la for\u00eat.",
        q: "Sortons du patelin !"
    },
    {
        id: 3, p: 2,
        n: "For\u00eat au nord-ouest de Weiz (pause)",
        lat: 47.2186, lng: 15.6135,
        date: "Nuit du 20 au 21 sept.",
        d: "Ils peuvent respirer. Chaussent leurs souliers, \u00e9changent leurs premi\u00e8res impressions. \u00ab\u00a0Tu as vu, le civil\u00a0? Il nous a dr\u00f4lement rep\u00e9r\u00e9s.\u00a0\u00bb Andr\u00e9 sort la boussole et cherche l'ouest.",
        q: "Et demain nous t\u00e2cherons de franchir la Mur !"
    },
    {
        id: 27, p: 2,
        n: "Pancarte \u00ab\u00a0Arbeits Kommando N\u00b0...\u00a0\u00bb",
        lat: 47.23365, lng: 15.56633,
        date: "Nuit du 20 au 21 sept.",
        d: "Ils joignent une route qui para\u00eet bien orient\u00e9e, mais \u00ab\u00a0apr\u00e8s quelques d\u00e9tours semble s'en aller carr\u00e9ment vers le nord\u00a0\u00bb. Andr\u00e9 \u00e9claire une pancarte : \u00ab\u00a0Arbeits Kommando N\u00b0\u2026 \u2192 \u00e0 200 m\u00e8tres.\u00a0\u00bb Ils quittent la route et suivent le lit sec d'un ruisseau dans le noir.",
        q: "Merde\u00a0!",
        type: "mention"
    },
    {
        id: 25, p: 2,
        n: "Bivouac nuit 1 (ravin bois\u00e9)",
        lat: 47.2329, lng: 15.5612,
        date: "Nuit du 20 au 21 sept.",
        d: "Recroquevill\u00e9s sous les couvertures, corps contre corps pour se r\u00e9chauffer, dans un antre de la for\u00eat embrouill\u00e9e, sur un l\u00e9ger replat. ~14\u00a0km depuis le Kommando.",
        q: "Et d'une \u00e9tape\u00a0! Je ne pense pas qu'on vienne nous d\u00e9couvrir ici.",
        type: "bivouac"
    },
    // Phase 3 — III. Le Pont à Péage
    {
        id: 4, p: 3,
        n: "Raabklamm (rivi\u00e8re & gu\u00e9s)",
        lat: 47.2448, lng: 15.5292,
        date: "21 sept. — matin",
        d: "Sur l'autre versant du bois, une longue gorge au fond de laquelle coule une petite rivi\u00e8re. \u00ab\u00a0La vall\u00e9e monte insensiblement vers l'ouest.\u00a0\u00bb Ils descendent, se d\u00e9chaussent, passent \u00e0 gu\u00e9 dans l'eau claire et froide qui leur monte \u00e0 mi-mollets. Deux civils arrivent sur l'autre rive : \u00ab\u00a0Heil Hitler\u00a0!\u00a0\u00bb Ils se font passer pour des Croates. Un groupe de jeunes campeurs gambade plus loin.",
        q: "Heil Hitler !",
        r: "Gu\u00e9s sur la Raab dans la Raabklamm"
    },
    {
        id: 5, p: 3,
        n: "Plateau pr\u00e8s de Semriach (bivouac nuit 2)",
        lat: 47.21671, lng: 15.44600,
        date: "Nuit du 21 au 22 sept.",
        d: "\u00ab\u00a0La nuit les rattrape dans les champs d'un plateau qui porte de loin en loin quelques fermes sur son dos caboss\u00e9.\u00a0\u00bb Fatigue, gosiers secs, pieds d'Andr\u00e9 entam\u00e9s. Recherche de pommiers. ~12\u00a0km depuis le bivouac pr\u00e9c\u00e9dent.",
        q: "R\u00e9veil dans la fra\u00eecheur matinale. Un coup d'\u0153il \u00e0 la boussole et \u00e0 la carte. \u2014 A\u00efe mes pieds\u00a0! \u2014 Et ces putains de sacs\u00a0! \u00c7a fait peur de les remettre. \u2014 Aujourd'hui il faut pourtant franchir la Mur.",
        type: "bivouac"
    },
    {
        id: 23, p: 3,
        n: "Cascade",
        lat: 47.20816, lng: 15.40010,
        date: "22 sept. — matin",
        d: "Dans une gorge \u00e9troite, ils s'arr\u00eatent sur des plates-formes b\u00e2ties pour les touristes et admirent le bouillonnement de la cascade dans le chaos des blocs rocheux. Des escaliers en bois longent les rochers, une cabane en bois pour l'organisation touristique. Ils \u00e9voquent les gorges pyr\u00e9n\u00e9ennes : la Pierre Lys, St Georges, Galamus.",
        q: "\u00c7a vaut le coup de s'\u00e9vader quand m\u00eame. Ne serait-ce que pour \u00e7a !",
        r: "Kesselfallklamm [?]"
    },
    {
        id: 28, p: 3,
        n: "Village travers\u00e9 [?\u00a0]",
        lat: 47.23120, lng: 15.37846,
        date: "22 sept.",
        d: "\u00ab\u00a0Ils ne peuvent \u00e9viter la travers\u00e9e d'un village. Des femmes leur indiquent la bonne route.\u00a0\u00bb",
        type: "mention"
    },
    {
        id: 29, p: 3,
        n: "Pentes abruptes (village \u00e9vit\u00e9)",
        lat: 47.24642, lng: 15.32951,
        date: "22 sept.",
        d: "Le sifflet d'une locomotive. La vall\u00e9e s'\u00e9largit pour se fondre dans la vall\u00e9e perpendiculaire. Ils d\u00e9cident de tourner le village par les bois, sur leur gauche. Mont\u00e9e \u00e0 pic dans les pentes bois\u00e9es. D'une trou\u00e9e ils observent la rivi\u00e8re et le village, mais le pont reste introuvable.",
        q: "O\u00f9 peut-il \u00eatre ce sacr\u00e9 pont\u00a0?",
        type: "mention"
    },
    {
        id: 6, p: 3,
        n: "Pont \u00e0 p\u00e9age sur la Mur \u2014 Frohnleiten",
        lat: 47.26884, lng: 15.32472,
        date: "22 sept. — apr\u00e8s-midi",
        d: "Un vieux bonhomme sort de sa baraque : \u00ab\u00a0Vier Pfennigo, bitte\u00a0!\u00a0\u00bb C'est un pont \u00e0 p\u00e9age, pas une sentinelle. Andr\u00e9 fouille nerveusement son sac. Le vieux demande s'ils sont Kroat\u00a0? \u00ab\u00a0Ja\u00a0!\u00a0\u00bb Il empoche dix pfennigs, veut rendre la monnaie. Ils filent. Sur le bord de la route, un prisonnier fran\u00e7ais travaille dans une scierie. Pont en bois, seul passage sur la Mur entre Bruck et Graz (document\u00e9 historiquement).",
        q: "Vier Pfennigo, bitte !",
        r: "Pont \u00e0 p\u00e9age de Frohnleiten (confirm\u00e9)"
    },
    {
        id: 26, p: 3,
        n: "Bivouac nuit 3 (apr\u00e8s le pont)",
        lat: 47.25831, lng: 15.29945,
        date: "Nuit du 22 au 23 sept.",
        d: "Les derni\u00e8res maisons pass\u00e9es, ils quittent la route pour le bois. Ils grimpent dans les feuilles s\u00e8ches, s'arr\u00eatent essouffl\u00e9s. Un bout de saucisson, un lit de feuilles mortes. ~24\u00a0km depuis le bivouac pr\u00e9c\u00e9dent.",
        q: "Nous avons la veine avec nous.",
        type: "bivouac"
    },
    // Phase 4 — IV. Les Abreuvoirs
    {
        id: 7, p: 4,
        n: "Montagnes entre Mur et M\u00fcrz",
        lat: 47.24166, lng: 15.15371,
        date: "~23-25 sept.",
        d: "\u00ab\u00a0Une belle vie, une vraie vie qui \u00e9prouve les muscles en lutte constante contre l'espace et la pesanteur.\u00a0\u00bb Marche \u00e0 la boussole plein ouest, plusieurs jours. Andr\u00e9 d\u00e9rive nord-ouest, Alban tire sud-ouest \u2014 \u00ab\u00a0en moyenne ils ne doivent gu\u00e8re s'\u00e9carter de la direction ouest\u00a0\u00bb. Trois jours de suite un abreuvoir creus\u00e9 dans un tronc les accueille \u00e0 l'\u00e9tape. ~17\u00a0km par jour.",
        q: "On n'en sortira jamais !"
    },
    {
        id: 30, p: 4,
        n: "Grange \u00e0 foin",
        lat: 47.2343, lng: 14.9202,
        date: "~25 sept.",
        d: "\u00ab\u00a0Ils escaladent une petite grange dans laquelle le foin sera doux \u00e0 leurs reins habitu\u00e9s au contact de la terre.\u00a0\u00bb Un palace peupl\u00e9 de beaux r\u00eaves de libert\u00e9. Vol de patates dans un champ voisin, le vieux n'y a vu que du feu. ~43\u00a0km en ~3\u00a0jours depuis le bivouac apr\u00e8s le pont.",
        q: "Un palace qu'ils vont peupler de beaux r\u00eaves de libert\u00e9\u2026"
    },
    // Phase 5 — V. Les Bords de la Mur
    {
        id: 31, p: 5,
        n: "Village au carrefour (d\u00e9tour nord)",
        lat: 47.22752, lng: 14.85871,
        date: "~26 sept. \u2014 matin",
        d: "Sortis de la grange une heure avant le jour, un village est atteint. Au carrefour, Andr\u00e9 tire vers le nord. La route vire dangereusement. \u00ab\u00a0C'\u00e9tait l'autre qui \u00e9tait la bonne.\u00a0\u00bb Ils regagnent le bon chemin \u00e0 travers les pr\u00e9s tremp\u00e9s de ros\u00e9e. Les locomotives sifflent dans le brouillard.",
        q: "La route vire dangereusement vers le nord. \u2014 C'\u00e9tait l'autre qui \u00e9tait la bonne.",
        type: "mention"
    },
    {
        id: 8, p: 5,
        n: "Bords de la Mur, vers Knittelfeld",
        lat: 47.2164, lng: 14.8483,
        date: "~26 sept.",
        d: "Dans le brouillard matinal, le bruit d'une grande rivi\u00e8re. \u00ab\u00a0La voil\u00e0\u2026 Merde\u00a0! \u00c7a ne peut \u00eatre que la Mur\u00a0!\u00a0\u00bb Un gros bourg sur l'autre rive \u2014 Knittelfeld\u00a0? Judenburg\u00a0? Feu de camp au bord de l'eau, th\u00e9 au lait, rasage. Ils d\u00e9cident de remonter la rivi\u00e8re vers l'ouest, direction Klagenfurt.",
        q: "La voil\u00e0... Merde ! \u00c7a ne peut \u00eatre que la Mur !",
        r: "Retrouvent la Mur apr\u00e8s avoir coup\u00e9 par les montagnes",
        type: "mention"
    },
    {
        id: 9, p: 5,
        n: "For\u00eat le long de la Mur",
        lat: 47.1781, lng: 14.7109,
        date: "~26 sept.",
        d: "Sentier sous les sapins, le long de la rivi\u00e8re. Ils jouissent de l'ombre et du murmure de l'eau. R\u00eaveries sur un cano\u00eb. \u00ab\u00a0L'Autriche est un magnifique pays\u00a0!\u00a0\u00bb Une enveloppe sur une bouse r\u00e9v\u00e8le le nom \u00ab\u00a0Juden\u2026\u00a0\u00bb \u2014 Judenburg\u00a0! Ils savent enfin o\u00f9 ils sont.",
        q: "L'Autriche est un magnifique pays !",
        r: "Sentier forestier le long de la Mur"
    },
    {
        id: 10, p: 5,
        n: "Judenburg (gare de marchandises)",
        lat: 47.17431, lng: 14.66452,
        date: "~26 sept. \u2014 soir",
        d: "Ils d\u00e9cident de tenter la gare de marchandises. Deux heures tapis le long de la cl\u00f4ture dans une petite fosse obscure. Des employ\u00e9s prom\u00e8nent leurs lampes entre les convois, des locomotives soufflent des fum\u00e9es rougeoyantes. Mais les trains ne s'arr\u00eatent pas.",
        q: "Y a pas moyen. On se d\u00e9bine ?",
        r: "Travers\u00e9e de Judenburg de nuit",
        type: "gare"
    },
    {
        id: 43, p: 5,
        n: "Grange apr\u00e8s Judenburg",
        lat: 47.17479, lng: 14.64926,
        date: "~26 sept. \u2014 nuit",
        d: "Apr\u00e8s l\u2019\u00e9chec \u00e0 la gare de marchandises, ils marchent de nuit, r\u00e9coltent des patates dans un champ, puis escaladent la fen\u00eatre d\u2019une grange et s\u2019allongent dans le foin. Le lendemain matin ils regagnent le bord de la rivi\u00e8re.",
        q: "Si on roupillait ici ?",
        type: "bivouac"
    },
    {
        id: 35, p: 5,
        n: "Tentative d\u2019escalade \u2014 raidillon (St. Georgen ob Judenburg)",
        lat: 47.19156, lng: 14.59773,
        date: "29 sept. \u2014 lundi soir",
        d: "Au cr\u00e9puscule, ils gagnent la voie ferr\u00e9e. \u00ab\u00a0Les longs trains de marchandises s\u2019essoufflent et ralentissent en montant un raidillon en lisi\u00e8re d\u2019une for\u00eat.\u00a0\u00bb Tentative d\u2019escalader un wagon \u2014 impossible. La gare suivante est Unzmarkt.",
        q: "Marchons. On essaiera \u00e0 la prochaine gare.",
        r: "Voie ferr\u00e9e Rudolfsbahn, raidillon vers St. Georgen ob Judenburg (714\u00a0m)",
        type: "mention"
    },
    {
        id: 34, p: 5,
        n: "Bord de la Mur \u2014 Dimanche de p\u00eacheurs",
        lat: 47.20762, lng: 14.54856,
        date: "27\u201329 sept. \u2014 sam. au lun.",
        d: "Apr\u00e8s l\u2019\u00e9chec \u00e0 la gare de Judenburg, ils avancent encore un peu le long de la Mur puis s\u2019installent sur la gr\u00e8ve. Repos du samedi et du dimanche (\u00ab\u00a0Dimanche au bord de l\u2019eau \u2014 Dimanche de p\u00eacheurs\u00a0\u00bb). Couture, stoppage de chaussettes, sandales pass\u00e9es au cirage. Le lundi soir, nouvelle tentative de train \u00e0 la voie ferr\u00e9e \u2014 impossible. D\u00e9cision de marcher jusqu\u2019\u00e0 la prochaine gare.",
        q: "Dimanche au bord de l\u2019eau \u2014 Dimanche de p\u00eacheurs.",
        r: "Bord de la Mur, entre Judenburg et Knittelfeld"
    },
    // Phase 6 — VI. La Nuit tragique
    {
        id: 11, p: 6,
        n: "Auto-strade \u2014 accident de v\u00e9lo (borne Klagenfurt 76\u00a0km)",
        lat: 47.10460, lng: 14.45578,
        date: "Nuit du 27 au 28 sept.",
        d: "Sur l'auto-strade Vienne-Klagenfurt. Bornes \u00ab\u00a0Klagenfurt 76\u00a0km\u2026 75\u2026 74\u2026\u00a0\u00bb Un cycliste sans lumi\u00e8re percute Andr\u00e9 de plein fouet. L'homme s'affale sur la route, le visage ensanglant\u00e9. Ils le rel\u00e8vent avec l'aide d'une femme puis s'enfuient \u00e0 travers champs. Point positionn\u00e9 \u00e0 ~18\u00a0km de Judenburg le long de la route, correspondant \u00e0 la borne \u00ab\u00a0Klagenfurt 76\u00a0km\u00a0\u00bb.",
        q: "Ah ! putain de Dieu ! Quelle tuile ! Quelle poisse !",
        r: "Auto-strade direction Klagenfurt (borne 76\u00a0km)"
    },
    {
        id: 12, p: 6,
        n: "Tunnel gard\u00e9 (sentinelle)",
        lat: 47.0109, lng: 14.4052,
        date: "Nuit du 27 au 28 sept.",
        d: "La route passe sous un pont ferroviaire dans une gorge \u00e9troite. Une sentinelle braque sa lampe sur Alban. \u00ab\u00a0Halt\u00a0!\u00a0\u00bb \u2014 \u00ab\u00a0Woher\u00a0?\u00a0\u00bb \u2014 \u00ab\u00a0Von Judenburg\u00a0!\u00a0\u00bb \u2014 \u00ab\u00a0Franzozen\u00a0?\u00a0\u00bb \u2014 \u00ab\u00a0Oh nein\u00a0!\u00a0\u00bb Il prom\u00e8ne sa lampe sur leurs corps puis : \u00ab\u00a0Gelt\u00a0!\u00a0\u00bb",
        q: "Gelt ! dit-il. \u2014 Danke sch\u00f6n !",
        r: "Route dans une gorge entre Judenburg et St. Veit"
    },
    // Phase 7 — VII. Tourisme
    {
        id: 13, p: 7,
        n: "St. Veit an der Glan",
        lat: 46.7681, lng: 14.3603,
        date: "~29-30 sept. — apr\u00e8s-midi",
        d: "Travers\u00e9e \u00e0 deux heures de l'apr\u00e8s-midi, parmi civils, soldats et gendarmes. Un soldat allemand s'approche pour demander du feu. Le sacr\u00e9 briquet d'Alban ne marchait pas, faute d'essence. Des prisonniers travaillent dans les champs comme des esclaves sous la surveillance d'un soldat.",
        q: "Et ce sacr\u00e9 briquet d'Alban qui ne marchait pas, faute d'essence !",
        r: "Travers\u00e9e de St. Veit \u00e0 pied"
    },
    {
        id: 14, p: 7,
        n: "Lac d'Ossiach",
        lat: 46.6700, lng: 13.9800,
        date: "~1er oct.",
        d: "Le plateau devient mar\u00e9cageux. Barbeaux dans un canal. Orage soudain, refuge dans une grange. Arc-en-ciel des sept couleurs. Le lac\u00a0: des maisons \u00e0 l'envers noy\u00e9es dans l'eau. Un vieillard qui garde une ch\u00e8vre les interroge : \u00ab\u00a0Wohin\u00a0?\u00a0\u00bb",
        q: "Wohin ? \u2014 Villach ! Auf Wiedersehen.",
        r: "Plateau puis bords du lac"
    },
    {
        id: 15, p: 7,
        n: "Villach (travers\u00e9e & pont sur la Drau)",
        lat: 46.60961, lng: 13.85230,
        date: "~2 oct.",
        d: "Le pont sur la Drau n'est pas gard\u00e9. La sentinelle de la caserne ne devine rien \u2014 c'est elle qui reste prisonni\u00e8re. Un adolescent ent\u00eat\u00e9 veut les prendre sur sa charrette tir\u00e9e par un b\u0153uf. \u00c0 la sortie, une pancarte\u00a0: \u00ab\u00a0Italien. Grenze 21\u00a0Km.\u00a0\u00bb",
        q: "Italien. Grenze 21 Km.",
        r: "Travers\u00e9e de Villach, pont sur la Drau"
    },
    // Phase 8 — Evvira
    {
        id: 16, p: 7,
        n: "Dernier bivouac en Autriche",
        lat: 46.54998, lng: 13.77312,
        date: "Nuit du 2 au 3 oct.",
        d: "\u00c0 la sortie de Villach, une pancarte les renseigne\u00a0: \u00ab\u00a0Italien. Grenze 21 Km.\u00a0\u00bb Ils traversent la ville, franchissent la Gail au pont d'Unterf\u00f6deraun, puis suivent la route de la vall\u00e9e de la Gail vers le sud-ouest (direction Arnoldstein) sur une dizaine de kilom\u00e8tres. Dernier feu de camp \u2014 pensent-ils \u2014 en territoire allemand\u00a0; ils se couchent \u00e0 m\u00eame le sol en lisi\u00e8re de for\u00eat.",
        q: "Italien. Grenze 21 Km.",
        type: "bivouac",
        r: "Route de la vall\u00e9e de la Gail, via le pont d'Unterf\u00f6deraun"
    },
    {
        id: 17, p: 8,
        n: "Fronti\u00e8re italo-autrichienne (cr\u00eate au sud de Th\u00f6rl-Maglern)",
        lat: 46.52221, lng: 13.70255,
        date: "3 oct. — 15h30",
        d: "Tranch\u00e9e dans la for\u00eat, une pancarte rong\u00e9e : \u00ab\u00a0Cassa\u00a0\u00bb. Une lettre en italien. \u00ab\u00a0Plus de doute\u00a0! On y est bien\u00a0!\u00a0\u00bb Ils s'embrassent. En patois occitan : \u00ab\u00a0\u00c9 aro euf f\u00e9 atension\u00a0!\u00a0\u00bb (Et maintenant il faut faire attention\u00a0!)",
        q: "Cassa ! Cassa ! \u00c7a veut dire certainement \u00ab chasse \u00bb en italien !",
        type: "frontiere"
    },
    {
        id: 33, p: 8,
        n: "Baraque en lisi\u00e8re (c\u00f4t\u00e9 italien)",
        lat: 46.51923, lng: 13.70240,
        date: "3 oct. — 15h30",
        d: "\u00c0 une vingtaine de m\u00e8tres, une maison appara\u00eet plant\u00e9e dans la clairi\u00e8re \u2014 \u00ab\u00a0une baraque roumani\u00e8re, s\u00fbrement\u00a0\u00bb. Un marteau cogne contre des planches, un homme chante sans les voir. Un grognement de chien. Prudemment, ils s'enfoncent dans le bois pour s'\u00e9loigner de ce danger qui chante et qui grogne.",
        q: "Il est trois heures et demie et un marteau cognant contre des planches cadence une chanson\u2026",
        type: "mention"
    },
    {
        id: 18, p: 8,
        n: "Versant italien (Alpes juliennes)",
        lat: 46.51204, lng: 13.62622,
        date: "3 oct. — soir (vendredi)",
        d: "Descente vers les vall\u00e9es. Montagnes d\u00e9chiquet\u00e9es, ar\u00eates coup\u00e9es \u00e0 la serpe. Ils \u00e9voquent les Dolomites. Mais l'Italie fourmille de soldats, carabiniers, gendarmes, police de la route. Ils suivent les routes de montagne, toute en terrain militaire. 35\u00a0km dans la nuit du samedi.",
        q: "Ne serait-ce que pour \u00e7a !",
        r: "Descente \u00e0 pied c\u00f4t\u00e9 italien"
    },
    // Phase 9 — Épilogue
    {
        id: 19, p: 9,
        n: "Arrestation par les carabiniers",
        lat: 46.44425, lng: 13.31431,
        date: "5 oct. — dimanche matin",
        d: "Dimanche matin, \u00e0 la sortie d'un village qu'on ne pouvait contourner \u00e0 cause de la montagne \u00e0 pic, deux sentinelles relev\u00e9es de la garde d'un tunnel leur demandent les papiers. Un vieux montait avec une corbeille de raisins \u2014 la plaine \u00e9tait toute proche.",
        q: "Et le dimanche matin il a fallu qu'un abruti !...",
        type: "capture"
    },
    {
        id: 20, p: 9,
        n: "Tarvisio (gare fronti\u00e8re)",
        lat: 46.5108, lng: 13.6039,
        date: "~6 oct.",
        d: "Poste de carabiniers. Fouille, interrogatoire, caserne, ceinture. Deux caf\u00e9s cr\u00e8me au buffet de la gare, moyennant cinq marks. Puis menottes entre deux carabiniers pour le train d'Udine.",
        q: "Elles font une dr\u00f4le d'impression, ces ferrailles qui t'emprisonnent les mains.",
        r: "Escorte par les carabiniers",
        type: "gare"
    },
    {
        id: 21, p: 9,
        n: "Udine (Prison Centrale)",
        lat: 46.0693, lng: 13.2357,
        date: "~6-7 oct.",
        d: "Panier \u00e0 salade, caserne, puis Prison Centrale \u2014 \u00ab\u00a0une esp\u00e8ce de forteresse sans fen\u00eatres\u00a0\u00bb. Un gardien ouvre une grille, referme. \u00ab\u00a0Ils nous ont fait crever de faim en Italie.\u00a0\u00bb Ils sont gentils, toujours le sourire, mais \u00ab\u00a0on ne vit pas que d'esp\u00e9rance\u00a0\u00bb.",
        q: "Ils nous ont fait crever de faim en Italie.",
        r: "Train sous escorte, menottes aux mains"
    },
    {
        id: 22, p: 9,
        n: "Stalag XVIII\u00a0D \u2014 Marburg (Maribor)",
        lat: 46.5547, lng: 15.6467,
        date: "21 oct. 1941 (\u00e9pilogue)",
        d: "Retour au Stalag XVIII\u00a0D, Marburg. 21 jours de cachot. Les copains passent des biscuits par le petit trou de la porte. \u00ab\u00a0Putain quelle fringale.\u00a0\u00bb",
        q: "Et d'o\u00f9 arrivez-vous ? \u2014 D'Italie. Vous avez des biscuits ?",
        type: "retour"
    }
],
  cpa: [
  { lat:47.21731, lng:15.62247, loc:'Weiz (Styrie)', cpa:[
    { img:'cartes_postales/weiz_hauptplatz_1898.jpg',       title:'Weiz — Place principale, ~1898',             desc:'Weiz, ville du district du Kommando de Hohenilz. Alban et André s\'évadent dans la nuit du 20 septembre.' },
    { img:'cartes_postales/weiz_cpa_autriche_hongrie.jpg',  title:'Weiz — Carte postale Empire austro-hongrois', desc:'Document de la poste impériale de Weiz.' },
    { img:'cartes_postales/weiz_sichelwerk_1898.jpg',       title:'Weiz — Scierie Mooshammer, ~1898',            desc:'Les prisonniers travaillaient dans des fermes et installations locales.' }
  ]},
  { lat:47.24914, lng:15.59556, loc:'Weiz — Weizklamm (Styrie)', cpa:[
    { img:'cartes_postales/akon_weiz_weizklamm.jpg', title:'Weiz — Ruine Sturmberg dans la Weizklamm', desc:'Le paysage boisé aux portes de Weiz — la gorge que traversent Alban et André dans la nuit du départ.' },
    { img:'cartes_postales/akon_weiz_1.jpg',         title:'Weiz — Ruine Sturmberg, forêt et rivière', desc:'C\'est de ce paysage qu\'ils s\'enfuient dans la nuit du 20 septembre 1941.' }
  ]},
  { lat:47.19880, lng:15.46776, loc:'Kesselfallklamm / Semriach (Styrie)', cpa:[
    { img:'cartes_postales/akon_schoeckl_1.jpg',    title:'Der Schöckl vom Rosenberg aus, ~1900',        desc:'Le vallon boisé du Schöckl, visible depuis leur itinéraire. Les Alpes styriennes dans toute leur splendeur.' },
    { img:'cartes_postales/akon_schoeckelhaus.jpg', title:'Schöcklhaus — Le refuge alpin',               desc:'Le sommet du Schöckl (1445 m) d\'où descend le Rötschbach.' }
  ]},
  { lat:47.20499, lng:15.39888, loc:'Kesselfallklamm — La cascade (Styrie)', cpa:[
    { img:'cartes_postales/kasselfalls_vintage.png', title:'Kesselfallklamm — La cascade et les passerelles', desc:'« Ça vaut le coup de s\'évader quand même. Ne serait-ce que pour ça ! » Alban et André s\'arrêtent sur les passerelles de la gorge pour admirer la cascade.' },
    { img:'cartes_postales/pierre_lys_trou_cure.jpg', title:'Gorges de la Pierre Lys — Le Trou du Curé (Aude)', desc:'« La Pierre Lys, St Georges, Galamus… de belles parties de camping… » Devant la cascade autrichienne, Alban et André évoquent les gorges pyrénéennes qu\'ils connaissent bien.' },
    { img:'cartes_postales/gorges_saint_georges_axat.jpg', title:'Gorges Saint-Georges — Axat (Aude)', desc:'Les gorges de Saint-Georges d\'Axat dans l\'Aude — l\'une des gorges pyrénéennes évoquées par les deux évadés devant la Kesselfallklamm.' }
  ]},
  { lat:47.269, lng:15.325, loc:'Frohnleiten — Pont sur la Mur (Styrie)', cpa:[
    { img:'cartes_postales/frohnleiten_lithographie_1830.jpg', title:'Frohnleiten — Lithographie J.F. Kaiser, 1830', desc:'« Vier Pfennigo, bitte ! » Un vieux gardien. Ils se font passer pour des Croates.' },
    { img:'cartes_postales/akon_frohnleiten_2.jpg',            title:'Frohnleiten — La Mur et le pont',             desc:'Vue panoramique avec la Mur et le pont bien visible.' },
    { img:'cartes_postales/akon_frohnleiten_3.jpg',            title:'Frohnleiten — Sommerfrische, les vergers',    desc:'Après le pont, un prisonnier français dans une scierie.' },
    { img:'cartes_postales/akon_frohnleiten_4.jpg',            title:'Frohnleiten — Le Stadtturm entre les sapins', desc:'Après le pont, les évadés bivouaquent dans les feuilles sèches.' }
  ]},
  { lat:47.320, lng:15.360, loc:'Mixnitz / Bärenschützklamm (Styrie)', cpa:[
    { img:'cartes_postales/akon_mixnitz_baerenschutz.jpg', title:'Mixnitz — Bärenschützschlucht et Hochlantsch', desc:'Contexte géographique du parcours sur la Mur.' },
    { img:'cartes_postales/akon_mixnitz_1.jpg',            title:'Mixnitz — Le village',                         desc:'La vallée de la Mur qu\'Alban et André remontent vers l\'ouest.' }
  ]},
  { lat:47.413, lng:15.287, loc:'Bruck an der Mur (Styrie)', cpa:[
    { img:'cartes_postales/bruck_mur_1910.png', title:'Bruck an der Mur — La Mürz et le Schlossberg, 1910', desc:'La confluence de la Mürz et la Mur. Phases 4–5.' }
  ]},
  { lat:47.6181, lng:15.1422, loc:'Hochschwab — Alpes de Styrie (Styrie)', cpa:[
    { img:'cartes_postales/Thomas_Leitner_-_Hochschwab_im_Winter_(1921).jpg', title:'Hochschwab im Winter — Thomas Leitner, 1921', desc:'« Une belle vie, une vraie vie qui éprouve les muscles en lutte constante contre l\'espace et la pesanteur. » Trois jours dans les montagnes entre Mur et Mürz.' }
  ]},
  { lat:47.19190, lng:14.43702, loc:'Unzmarkt / Vallée de la Mur (Styrie)', cpa:[
    { img:'cartes_postales/murtalbahn_mur_1900.jpg', title:'Murtalbahn — Train sur le pont de la Mur, ~1900', desc:'« Le petit train à voie étroite qui monte vers Murau en poussant des sifflements aigus. » La Murtalbahn part d\'Unzmarkt — c\'est là qu\'ils décident de tenter d\'escalader un wagon.' }
  ]},
  { lat:47.213, lng:14.827, loc:'Knittelfeld — Vallée de la Mur (Styrie)', cpa:[
    { img:'cartes_postales/akon_knittelfeld_1.jpg', title:'Knittelfeld — Vue depuis le Dremmelberg',    desc:'« Knittelfeld ? Judenbourg ? — Peu importe. Il n\'y a qu\'à suivre la Mur. »' },
    { img:'cartes_postales/akon_knittelfeld_2.jpg', title:'Knittelfeld — Roseggerstraße et les usines', desc:'« Un gros bourg sur l\'autre rive — Knittelfeld ? Judenbourg ? — Feu de camp au bord de l\'eau, thé au lait, rasage. Ils décident de remonter la rivière vers l\'ouest. »' }
  ]},
  { lat:47.169, lng:14.662, loc:'Judenburg (Styrie)', cpa:[
    { img:'cartes_postales/akon_judenburg_1.jpg', title:'Judenburg — Le Stadtturm depuis les sapins',      desc:'Identifiée via une pancarte déchirée : « Juden… »' },
    { img:'cartes_postales/akon_judenburg_2.jpg', title:'Judenburg — Vue panoramique, la Mur et les Alpes',desc:'Judenburg dans son écrin alpin. Puis la gare de marchandises.' }
  ]},
  { lat:46.768, lng:14.360, loc:'St. Veit an der Glan (Carinthie)', cpa:[
    { img:'cartes_postales/st_veit_kino_1900.jpg',      title:'St. Veit — Stadt-Kino-Theater, ~1900', desc:'Traversée à deux heures. « Et ce sacré briquet d\'Alban qui ne marchait pas ! »' },
    { img:'cartes_postales/st_veit_friesacher_tor.jpg', title:'St. Veit — Porte de Friesach',         desc:'Un soldat demande du feu. Le briquet est à sec.' },
    { img:'cartes_postales/hochosterwitz_1910.png',     title:'Burg Hochosterwitz — CPA ~1910',       desc:'Le paysage carinthien : routes militarisées, soldats partout.' }
  ]},
  { lat:46.68890, lng:13.99229, loc:'Lac d\'Ossiach (Carinthie)', cpa:[
    { img:'cartes_postales/ossiach_gierymski_1886.jpg', title:'Lac d\'Ossiach — Gierymski, 1886', desc:'« Le lac d\'Ossiach ! » — bord marécageux. « Wohin ? — Villach ! »' }
  ]},
  { lat:46.440, lng:13.310, loc:'Alpes juliennes — Arrestation (Italie)', cpa:[
    { img:'cartes_postales/Gabinio.Carabinieri_In_Servizio_Al_Confine_Alpino._Valli_Di_Lanzo,_Pian_Della_Mussa,_Due_Carabinieri_In_Pattuglia_2A79.jpg', title:'Deux carabiniers en patrouille à la frontière alpine, ~1902', desc:'Photo de Mario Gabinio (~1902). « À la sortie d\'un village qu\'on ne pouvait contourner à cause de la montagne à pic, deux sentinelles relevées de la garde d\'un tunnel leur demandent les papiers. »' }
  ]},
  { lat:46.53371, lng:13.64296, loc:'Pontafel / Pontebba — Frontière austro-italienne', cpa:[
    { img:'cartes_postales/Pontebba1900.JPG', title:'Pontafel/Pontebba — Vue du village, ~1900', desc:'Pontafel (côté autrichien) / Pontebba (côté italien), village frontalier du Kanaltal. C\'est sur la crête à l\'est, au sud de Thörl-Maglern, qu\'Alban et André franchissent la frontière le 3 octobre à 15h30.' },
    { img:'cartes_postales/Pontebba_(UD)_-_vecchia_stazione_ferroviaria_-_cartolina.jpg', title:'Gare de Pontebba — Ancienne station frontière, CPA', desc:'L\'ancienne gare de Pontebba, station frontière vers l\'Autriche jusqu\'à la Première Guerre mondiale. « Elles font une drôle d\'impression, ces ferrailles qui t\'emprisonnent les mains. » Alban et André seront escortés jusqu\'à Tarvisio puis Udine.' }
  ]},
  { lat:46.610, lng:13.852, loc:'Villach (Carinthie)', cpa:[
    { img:'cartes_postales/villach_1898.jpg',        title:'Villach — Vue de la ville, 1898',       desc:'« Le lendemain Villach est traversée sans encombre. »' },
    { img:'cartes_postales/villach_draubruecke.jpg', title:'Villach — Pont sur la Drau, ca. 1914',  desc:'« Le pont sur la Drau n\'est pas gardé. » Puis : Italien. Grenze 21 Km.' }
  ]}
],
  staticRoutes: [],
  elevProfile: []
};
