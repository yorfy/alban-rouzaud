# Exemples d'erreurs par type

Corpus de référence : ALBAN ROUZAUD 2 — « Journal non écrit d'un fantassin en repli stratégique », journées 1 à 6. 54 erreurs détectées par comparaison entre la transcription brute et la version relue.

---

## GUILLEMET (7 cas)

| Transcription | Correction | Contexte |
|---|---|---|
| `"fauché"` | `« fauché »` | la demeure d'un __ |
| `"souvenirs".` | `« souvenirs ».` | les poches s'emplissent de __ |
| `"voie Sacrée"` | `« voie Sacrée »` | nous marchons sur la __ |
| `"tombeau ouvert".` | `« tombeau ouvert ».` | une côte à __ |
| `"la plus belle armée du monde".` | `« la plus belle armée du monde ».` | couler dans le flot de __ |
| `«Il me faut` | `« Il me faut` | Coco rapplique. __ |
| `tunnel.»` | `tunnel. »` | faire sauter un __ |

Patron commun : les guillemets droits `"` sont systématiquement utilisés à la place des guillemets français. L'espace insécable est aussi absente autour des chevrons quand ils apparaissent.

---

## ESPACE_TYPO (3 cas)

| Transcription | Correction | Contexte |
|---|---|---|
| `Dieu! où` | `Dieu ! Où` | nom de __ allons-nous |
| `«Il` | `« Il` | voir GUILLEMET ci-dessus |
| `tunnel.»` | `tunnel. »` | voir GUILLEMET ci-dessus |

Souvent couplé à un problème de guillemets.

---

## ACCENT (3 cas)

| Transcription | Correction | Confusion |
|---|---|---|
| `becane` | `bécane` | e → é |
| `metres` | `mètres` | e → è |
| `arreter` | `arrêter` | e → ê |

Mots courants dont la forme sans accent n'existe pas — détection triviale par dictionnaire.

---

## CASSE (5 cas)

| Transcription | Correction | Règle |
|---|---|---|
| `Patelin.` | `patelin.` | nom commun en milieu de phrase |
| `Commençons` | `commençons` | continuation d'une phrase (pas de ponctuation forte avant) |
| `on` (après `!`) | `On` | majuscule après `!` |
| `tant` (après `!`) | `Tant` | majuscule après `!` |
| `on` (après `!`) | `On` | majuscule après `!` |

---

## PONCTUATION (9 cas)

| Transcription | Correction | Sous-type |
|---|---|---|
| `dire —` | `dire…` | tiret de dialogue → points de suspension (interruption) |
| `vélo —` | `vélo…` | idem |
| `boire !` | `boire.` | exclamation en trop |
| `fauché !` | `fauché.` | exclamation en trop |
| `ville. Devant` | `ville devant` | point en trop (phrase unique) |
| `nuit, des` | `nuit. Des` | virgule → point (nouvelle phrase) |
| `couvertures.` | `couvertures !` | point → exclamation |
| `fortune.` | `fortune !` | point → exclamation |
| `attend` | `attend,` | virgule manquante |

Les corrections de ponctuation sont les plus ambiguës : elles reflètent souvent un choix interprétatif du relecteur plus qu'une erreur de transcription.

---

## NOM_PROPRE (4 cas)

| Transcription | Correction | Occurrences TXT | Indice |
|---|---|---|---|
| `Induï` | `André` | 1 vs ~47 | hapax, forme graphiquement lointaine |
| `Riché` | `André` | 1 vs ~47 | hapax |
| `Chapuze` | `Chapize` | 1 vs ~4 | variante du même personnage |
| `Sarmont` | `Germont` | 1 vs 0 | confusion S/G en majuscule cursive |

Le signal le plus fiable est l'hapax : un nom propre qui n'apparaît qu'une seule fois est presque toujours une erreur de lecture.

---

## MOT_INEXISTANT (5 cas)

| Transcription | Correction | Confusion manuscrite |
|---|---|---|
| `démantons` | `démontons` | a ↔ o |
| `cosue` | `cossue` | s manquant (ss ↔ s) |
| `l'ichot` | `l'idiot` | ch ↔ d |
| `oralé` | `avalé` | o ↔ a, r ↔ v |
| `foucher` | `joindre` | mot entièrement mal lu |

Pour les quatre premiers, la table des confusions manuscrites (`regles-revue.md`) permet de générer le bon candidat. Le dernier cas (`foucher` → `joindre`) est hors de portée de la distance d'édition : seul le contexte permet de comprendre que « On recule pour __ le village » attend `joindre`.

---

## LECTURE_ERRONEE (8 cas)

Mots existants mais incorrects dans le contexte :

| Transcription | Correction | Indice de détection |
|---|---|---|
| `faiblit` | `pâlit` | les deux existent — seul le contexte tranche |
| `roues` | `gravier` | crissements de `roues` fait sens ; `gravier` est le mot du manuscrit |
| `bidon de Guern` | `breton Le Guern` | `bidon de` est syntaxiquement bizarre avant un nom propre |
| `vallons. Verts, flaques` | `vallonnements verts plaqués` | la phrase est cassée en fragments absurdes |
| `ronronnement` | `ronflement` | les deux existent, contexte d'avions de bombardement |
| `bouteilles. Jouis d'en voir` | `bouteilles puis d'en vont` | `Jouis d'en voir` est sémantiquement bizarre |
| `Rouler !` | `Roulez !` | contexte d'impératif (on parle au cocher) |
| `Nos sans capitaine` | `Un grand capitaine` | phrase agrammaticale |

Ces erreurs sont les plus difficiles à détecter automatiquement. Le signal le plus fiable : une phrase qui ne fait pas sens grammaticalement ou sémantiquement.

---

## PARAGRAPHE — Paragraphes trop longs découpés (5 cas, 12 coupures)

| TXT (1 paragraphe) | DOCX (découpé en) | Signal de coupure |
|---|---|---|
| 544 chars : « Juste au moment où la colonne… Repos de quelques heures… » | 2 paragraphes | `!` + changement de scène (combat → repos) |
| 373 chars : « Nous sortons d'une forêt… — Pour nous dire quoi ? » | 2 paragraphes | `…` + tiret de dialogue |
| 549 chars : « — Avec ça dit André… On repart encore un coup… » | 2 paragraphes | `.` + passage dialogue → récit |
| 759 chars : « — Ils pourraient au moins… Voici les avions… La section… On casse la croûte… » | 4 paragraphes | `?` `.` `!` + changements de scène successifs |
| 655 chars : « Mais où on ne se marre pas… Le Colon vient avec nous… » | 2 paragraphes | `.` + nouveau sujet (action → déplacement) |

Patterns observés dans les 12 points de coupure :
- 9 coupures après `.` suivi d'une majuscule (fin de phrase → nouveau paragraphe)
- 1 coupure après `!` suivi d'une majuscule
- 1 coupure après `?` suivi d'une majuscule
- 1 coupure après `…` suivi d'un tiret de dialogue `—`

Dans 100% des cas, la coupure se fait à une frontière de phrase existante (jamais en milieu de phrase). Le signal déclencheur est toujours un changement de sujet, de scène, ou de mode (dialogue ↔ récit).

---

## REFORMULATION (2 cas)

| Transcription | Correction | Nature |
|---|---|---|
| `du passé, reviennent.` | `disparaissent.` | relecture interprétative — le relecteur a relu le manuscrit |
| `9. c'est emballé` | `9.C est installé` | référence militaire mal déchiffrée |

Ces cas ne relèvent pas d'une règle : c'est le relecteur humain qui, en revoyant l'image, a lu autre chose. Le skill peut signaler le passage comme douteux mais la correction nécessite un accès à l'image source.

---

## Répartition statistique (sur 54 erreurs + 12 coupures de paragraphe)

| Type | Nb | % | Détection auto |
|---|---|---|---|
| PONCTUATION | 19 | 29% | partielle |
| MOT_DIFFERENT / LECTURE_ERRONEE | 13 | 20% | basse |
| PARAGRAPHE (coupures) | 12 | 18% | moyenne |
| ERREUR_LECTURE / MOT_INEXISTANT | 12 | 18% | moyenne |
| CASSE | 5 | 8% | haute |
| ACCENT | 3 | 5% | haute |
| REFORMULATION | 2 | 3% | nulle |

Estimation de couverture automatique : ~52% des erreurs corrigeables par les niveaux 1+2, ~75% détectables (corrigées ou signalées) avec le niveau 3. Les coupures de paragraphe sont détectables à ~90% mais nécessitent une validation humaine.
