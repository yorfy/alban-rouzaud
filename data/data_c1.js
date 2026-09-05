// data_c1.js — Données Cahier 1 : La Guerre (Août 1939 – Juin 1940)

var CAHIER_1_DATA = {
  PC: {
    1: '#f5a623',   // ocre — avant la guerre (Ariège, virées)
    2: '#e94560',   // rouge — mobilisation (sept. 1939)
    3: '#3498db',   // bleu — drôle de guerre en Alsace
    4: '#e74c3c'    // rouge sombre — débâcle vers Verdun
  },
  PN: {
    1: 'Avant la guerre — Ariège',
    2: 'Mobilisation — Toulouse',
    3: 'Drôle de guerre — Alsace',
    4: 'La débâcle — vers Verdun'
  },
  stops: [
  {id:1,p:1,n:"Lavelanet",lat:42.9372,lng:1.8478,
   d:"Ville de l'auteur. Il y vit avec sa femme et sa fille. C'est dans l'escalier de son immeuble qu'il entend la mobilisation générale à la radio.",
   q:"Tu peux préparer ma valise, je pars mardi."},
  {id:2,p:1,n:"L'Alibert (maison natale, près de Fougax)",lat:42.8623,lng:1.9401,
   d:"La maison de ses parents dans la forêt de sapins de Bélesta. Sentier en lacets, colonnades de sapins, cèpes, lumière dans les futaies. Le père moissonne au Rec Blanc, la mère lie des gerbes au Soula.",
   q:"Ah ! les assassins ! dit la mère en lâchant la gerbe."},
  {id:3,p:1,n:"Vallée du Vicdessos",lat:42.77,lng:1.505,
   d:"Virée en torpedo avec trois amis. Prétexte : reconnaître les sentiers vers l'Espagne. Arrêt « jambon du pays » au bord du torrent. Rencontre avec une femme mémorable.",
   q:"L'auto dévidait sans effort la route qui chevauchait les collines, enjambait les rivières, trouait les bois.",
   r:"Route de la vallée du Vicdessos (D8)"},
  {id:4,p:1,n:"Cols vers l'Espagne",lat:42.60648,lng:1.46732,
   d:"But théorique de l'expédition, vite oublié. Le traité de Versailles, Dantzig, la liberté ? « Qu'est-ce que ça pouvait leur foutre ? »",
   q:"Mais ils avaient un état civil, un livret militaire et un fascicule de mobilisation."},
  {id:5,p:2,n:"Lavelanet (mobilisation)",lat:42.9372,lng:1.8478,
   date:"3 sept. 1939",
   d:"3 septembre 1939. Annonce à la radio. Départ le mardi. Visite à ses parents à La Libère. Le père, ancien fantassin de 14-18, s'assied sur une gerbe sans un mot.",
   q:"La mobilisation générale est décrétée."},
  {id:6,p:2,n:"Toulouse (rassemblement)",lat:43.6047,lng:1.4442,
   d:"Centre de rassemblement du « grand troupeau ». Trains, casernes, tramways. Costumes hétéroclites. La foule se teinte de kaki.",
   q:"Le plus dur n'est pas d'aller se faire casser la gueule ; c'est d'y aller avec des cons et des adjudants.",
   r:"Train depuis Lavelanet"},
  {id:7,p:3,n:"La Petite-Pierre (cantonnement)",lat:48.8564,lng:7.3192,
   d:"Secteur du 11e R.I. en Alsace. Cantonnement entre les montées en ligne. Pernod, poker, bridge. Le printemps alsacien « vient tout d'un coup, comme un miracle ».",
   q:"Il ne nous restait plus qu'à boire du pernod et jouer au poker.",
   r:"Train depuis Toulouse"},
  {id:8,p:3,n:"Ringendorf (repos)",lat:48.80,lng:7.4833,
   d:"Village alsacien. Le lieutenant y était « si pimpant dans son costume fantoche surmonté d'un képi flamboyant ». Relève de garde courtelinesque.",
   q:"Alors qu'il était si pimpant à Ringendorf…"},
  {id:9,p:3,n:"Avant-postes (face à Pirmasens)",lat:49.07,lng:7.55,
   d:"Colline boisée, tranchées, barbelés. No man's land. Cabanas bégaie, Daydé pose des collets à lièvre, G… raconte ses aventures espagnoles. Nuits de bombardement.",
   q:"Les faubourgs de Pirmasens se perdaient derrière l'horizon."},
  {id:10,p:3,n:"Pirmasens (positions allemandes)",lat:49.2014,lng:7.6056,
   d:"Ville allemande visible depuis les avant-postes. « Les ceux d'en face. » De courtes rafales rappellent leur présence.",
   q:"Tant qu'ils emmerderont les autres… qu'on pensait.",
   type:"mention"},
  {id:11,p:3,n:"Village de Sy (patrouille nocturne)",lat:49.04,lng:7.52,
   d:"Village abandonné. Patrouille de nuit. Cadavres, vaches estropiées. G… abat un soldat allemand au revolver. Riberot et Redon blessés. Le lieutenant tué.",
   q:"G… a tiré en criant : « C'en est un ! »"},
  {id:12,p:4,n:"Alsace (fin de la drôle de guerre)",lat:48.8564,lng:7.3192,
   date:"10 mai 1940",
   d:"10 mai 1940. « Les Allemands ont envahi la Hollande. » Les piqûres sont interrompues. Fin de neuf mois d'attente.",
   q:"Vous pouvez vous r'habiller. Les Allemands ont envahi la Hollande."},
  {id:13,p:4,n:"Verdun (position « en bretelle »)",lat:49.16,lng:5.3833,
   d:"Destination finale du cahier 1. Le régiment doit prendre position « en bretelle » pour « colmater la poche ». La suite dans le cahier 2.",
   q:"Ils devaient aboutir du côté de Verdun prendre une position dite « en bretelle ».",
   r:"Déplacement en train puis à pied",
   type:"capture"}
],
  cpa: [
  { lat:42.9372, lng:1.8478, loc:"Lavelanet (Ariège)", cpa:[
    { img:"cartes_postales/tarascon_vicdessos_sabart.jpg",
      title:"Tarascon-sur-Ariège — Sabart et la vallée du Vicdessos",
      desc:"La région ariégeoise d'Alban Rouzaud. La vallée du Vicdessos où il fait une dernière virée en torpedo avec ses amis avant la mobilisation." }
  ]},
  { lat:43.6047, lng:1.4442, loc:"Toulouse (Haute-Garonne)", cpa:[
    { img:"cartes_postales/toulouse_matabiau_cpa.jpg",
      title:"Toulouse — Gare Matabiau, CPA",
      desc:"La gare de Toulouse d'où Alban et ses camarades partent rejoindre leurs régiments en septembre 1939. « Le grand troupeau »." }
  ]},
  { lat:48.8564, lng:7.3192, loc:"La Petite-Pierre (Bas-Rhin)", cpa:[
    { img:"cartes_postales/pirmasens_1905.jpg",
      title:"Pirmasens (Allemagne) — CPA 1905",
      desc:"Pirmasens, la ville allemande visible depuis les avant-postes d'Alban Rouzaud. « Les ceux d'en face. » La drôle de guerre vue depuis la ligne Maginot." }
  ]},
  { lat:49.16, lng:5.3833, loc:"Verdun (Meuse)", cpa:[
    { img:"cartes_postales/verdun_bombardé_1918.jpg",
      title:"Verdun bombardé — CPA 1918",
      desc:"Verdun, destination finale du Cahier 1. Le régiment doit y prendre position « en bretelle » pour colmater la poche allemande de juin 1940." },
    { img:"cartes_postales/verdun_ruines_1914.jpg",
      title:"Verdun en ruines — CPA 1914",
      desc:"Les ruines de Verdun, symbole de 1914-1918. En juin 1940, l'histoire se répète tragiquement." }
  ]},
  { lat:48.178, lng:6.451, loc:"Épinal (Vosges)", cpa:[
    { img:"cartes_postales/bundesarchiv_prisonniers_francais_1940.jpg",
      title:"Prisonniers français — juin 1940 (Bundesarchiv)",
      desc:"Photo d'archives allemandes (Bundesarchiv) montrant des prisonniers français en juin 1940. Alban Rouzaud sera capturé à Épinal en juillet 1940." },
    { img:"cartes_postales/french_weeps_1940.jpg",
      title:"Soldat français pleurant l'armistice — juin 1940",
      desc:"« Une main qui ne fait pas l'aumône. Une main qui donne simplement. » La capture à Épinal." }
  ]}
],
  staticRoutes: [],
  elevProfile: []
};
