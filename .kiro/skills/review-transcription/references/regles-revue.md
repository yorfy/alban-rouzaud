# Règles de détection — Revue de transcription

Trois niveaux de détection, appliqués dans l'ordre. Chaque règle produit un type d'anomalie et un niveau de confiance (haute, moyenne, basse) qui détermine le traitement en phase 3.

---

## Niveau 1 — Règles mécaniques

Règles déterministes, applicables sans interprétation.

### GUILLEMET — Guillemets droits → français

Remplacer `"..."` par `« ... »` avec espaces insécables.

Logique de détection du sens :
- `"` précédé d'un espace, d'un début de ligne, ou d'un tiret de dialogue → guillemet ouvrant `« `
- `"` suivi d'un espace, d'une ponctuation de fin, ou d'une fin de ligne → guillemet fermant ` »`

Vérifier aussi :
- `«mot` sans espace après → ajouter espace insécable
- `mot»` sans espace avant → ajouter espace insécable
- Guillemets simples droits (`''`) utilisés comme fermants → remplacer par `»`

**Confiance : haute.**

### ESPACE_TYPO — Espaces typographiques françaises

En français, espace insécable **avant** : `!` `?` `;` `:` `»`
Espace insécable **après** : `«`

Détecter :
- Ponctuation haute collée au mot : `mot!` `mot?` `mot;` `mot:`
- Ponctuation haute avec espace sécable (acceptable mais normaliser en insécable)
- `«mot` ou `mot»` sans espace

Ne pas toucher aux tirets de dialogue (`—`) ni aux points (`.` `,`).

**Confiance : haute.**

### ACCENT — Accents manquants

Détecter les mots courants privés de leur accent :
- `a` au lieu de `à` (préposition vs verbe — vérifier le contexte grammatical)
- Mots courants : `metres`→`mètres`, `arreter`→`arrêter`, `becane`→`bécane`, `crepuscule`→`crépuscule`, `equipement`→`équipement`, `epoque`→`époque`, etc.

Méthode : vérifier si le mot sans accent n'existe pas dans un dictionnaire français, ou si la forme accentuée est la seule forme valide.

**Confiance : haute** quand le mot sans accent n'existe pas. **Moyenne** quand les deux formes existent (ex. `ou`/`où`, `a`/`à`).

### CASSE — Majuscules et minuscules

Règles :
- Après `.` → la première lettre du mot suivant doit être une majuscule. **Confiance : haute.**
- En milieu de phrase, un nom commun ne prend pas de majuscule (ex. `Patelin` → `patelin` si ce n'est pas un nom propre). **Confiance : moyenne.**
- Début de paragraphe → majuscule. **Confiance : haute.**

**Exception dialogue** : après `!` ou `?` en milieu de réplique ou de phrase narrative, ne PAS forcer la majuscule. Dans ce type de récit oral, l'exclamation et l'interrogation ponctuent le débit sans forcément ouvrir une nouvelle phrase. Exemples à ne pas corriger :
- `Ah ! putain.` — l'exclamation fait partie de la même réplique.
- `Au galop ! faites place !` — suite de la même injonction.
- `Dis donc ! regarde cette moto !` — continuité de la réplique.
- `Ha ! qu'il fait.` — l'incise suit l'exclamation.
- `Ils sont malades ma parole ! trente hommes` — suite du même constat.

Critère de distinction : la majuscule après `!` ou `?` est justifiée seulement quand le mot suivant entame clairement un **nouveau paragraphe** ou une **nouvelle phrase indépendante** (changement de sujet, nouveau locuteur, transition narrative). En cas de doute, **conserver la minuscule de l'original**.

Attention : les noms propres (personnages, lieux) gardent leur majuscule. Croiser avec le dictionnaire contextuel (phase 1).

### PONCTUATION — Ponctuation incohérente

Détecter :
- Virgule là où un point est attendu (phrase complète suivie d'une majuscule après la virgule).
- Point d'exclamation/interrogation manquant ou en trop.
- Tirets de dialogue `—` remplacés par `…` ou inversement — signaler sans corriger automatiquement (choix stylistique).
- Point collé au guillemet fermant sans espace : `.»` → `. »`

**Confiance : moyenne.** Les choix de ponctuation dans un manuscrit ancien sont souvent délibérés.

### PARAGRAPHE — Paragraphes trop longs à découper

La transcription fusionne souvent en un seul paragraphe des passages qui, dans le manuscrit, constituent des blocs narratifs distincts. Le transcripteur suit les lignes de la page sans repérer les changements de sujet ou de rythme. Le résultat est un mur de texte difficile à lire et structurellement incorrect.

**Signaux de coupure** (un paragraphe mérite d'être scindé quand) :

1. **Tiret de dialogue en milieu de ligne** : un `—` précédé d'un espace et suivi d'une majuscule en plein milieu d'un paragraphe. Un tiret de dialogue ouvre toujours un nouveau paragraphe.

2. **Changement de scène ou de temps** : après une ponctuation de fin (`. ! ? …`), le mot suivant entame un nouveau sujet, un nouveau lieu, ou un saut temporel. Indices typiques :
   - Changement de sujet grammatical (passage de « nous » à une description impersonnelle, ou inversement).
   - Marqueurs temporels : « Maintenant », « Enfin », « Brusquement », « Le lendemain », « Au bout de », « Puis », « Ensuite ».
   - Marqueurs spatiaux : « Voici », « De l'autre côté », « Dans une maison », « Un carrefour ».
   - Passage du dialogue au récit ou inversement.

3. **Longueur excessive** : un paragraphe de prose narrative dépassant ~400 caractères ou ~5 phrases est suspect. Ce n'est pas un critère suffisant seul, mais il déclenche un examen des signaux 1 et 2.

**Seuils observés sur le corpus ALBAN ROUZAUD 2 :**
- Les paragraphes corrigés font rarement plus de 400 caractères.
- Les paragraphes de 500+ caractères contiennent presque toujours au moins un point de coupure naturel.
- Les paragraphes de 800+ caractères en contiennent systématiquement plusieurs.

**Confiance : moyenne.** Proposer les coupures mais ne pas les appliquer automatiquement. Le relecteur humain a le dernier mot sur le rythme du texte.

---

## Niveau 2 — Dictionnaire contextuel

Règles basées sur le dictionnaire de noms propres construit en phase 1.

### NOM_PROPRE — Noms propres incohérents

Construire la liste des noms propres (personnages, lieux, unités) et leurs occurrences. Signaler :

- **Hapax suspects** : un nom qui apparaît 1 seule fois alors qu'un nom graphiquement proche apparaît souvent. Exemples observés :
  - `Induï` (1 occ.) vs `André` (47 occ.) → probable erreur de lecture
  - `Riché` (1 occ.) vs `André` (47 occ.) → probable confusion
  - `Chapuze` (1 occ.) vs `Chapize` (4 occ.) → variante erronée
  - `Sarmont` (1 occ.) vs `Germont` (contexte géographique) → confusion S/G

- **Variantes orthographiques** : un même nom propre avec deux graphies. Signaler la moins fréquente.

Seuil : tout nom propre apparaissant ≤ 1 fois mérite examen.

**Confiance : moyenne.** Proposer la correction mais ne pas l'appliquer sans validation.

### MOT_INEXISTANT — Mots absents du dictionnaire

Vérifier chaque mot contre un dictionnaire français. Signaler les mots qui n'existent pas et ne sont pas des noms propres connus :
- `démantons` → `démontons` (confusion a/o)
- `cosue` → `cossue` (s manquant)
- `oralé` → `avalé` (confusion o/a, r/v)
- `foucher` → n'existe pas (correction contextuelle : `toucher` ou `joindre`)
- `ichot` → n'existe pas (correction : `idiot`, confusion ch/d)

Pour chaque mot inexistant, proposer le mot existant le plus proche par distance d'édition, en tenant compte des confusions manuscrites fréquentes (voir section confusions ci-dessous).

**Confiance : moyenne** quand un seul candidat proche existe. **Basse** quand plusieurs candidats sont possibles.

### Confusions manuscrites fréquentes

Paires de caractères souvent confondus dans les manuscrits français :
- `a` ↔ `o` (boucles similaires)
- `u` ↔ `n` (jambages inversés)
- `i` ↔ `l` ↔ `t` (hastes similaires)
- `e` ↔ `c` (boucle ouverte/fermée)
- `ch` ↔ `d` (en cursive)
- `m` ↔ `nn` ou `rn` (jambages)
- `r` ↔ `v` (sommet pointu vs arrondi)
- `S` ↔ `G` ↔ `L` (majuscules cursives)
- `f` ↔ `p` ↔ `j` (jambages descendants)
- `b` ↔ `h` ↔ `k` (hastes ascendantes)
- `s` ↔ `z` (terminaisons)
- `ss` ↔ `s` (doublement raté)

Utiliser ces paires pour générer des candidats de correction lorsqu'un mot est inexistant : substituer chaque paire et vérifier si le résultat existe.

---

## Niveau 3 — Analyse sémantique

Règles nécessitant une compréhension du contexte. Appliquées par le LLM.

### LECTURE_ERRONEE — Mot existant mais incorrect dans le contexte

Le mot existe en français mais produit un non-sens dans la phrase :
- `vallons. Verts, flaques d'eczémas` → `vallonnements verts plaqués d'eczémas` (phrase découpée de manière absurde)
- `ronronnement léger descend du ciel` → `ronflement` (les avions ne ronronnent pas légèrement)
- `bouteilles. Jouis d'en voir` → `bouteilles puis d'en vont` (Jouis ne fait pas sens ici)
- `Rouler !` → `Roulez !` (impératif attendu dans un contexte de dialogue)

Méthode : relire chaque phrase. Si le sens est incohérent, absurde, ou syntaxiquement cassé, envisager une erreur de lecture. Proposer une alternative en considérant les confusions manuscrites.

**Confiance : basse.** Signaler comme alerte. Si les images sources sont disponibles, vérifier visuellement.

### SENS_DOUTEUX — Passage obscur

Le texte est grammaticalement valide mais le sens reste bizarre dans le contexte du récit. Signaler pour relecture humaine sans proposer de correction.

Exemples :
- `9. c'est emballé dans un de ces bâtiments` → sens obscur (`9.C est installé` est une référence à une unité militaire)
- `du passé, reviennent` → fait sens littéralement mais `disparaissent` colle mieux au récit (les avions reprennent de la hauteur et s'en vont)

**Confiance : basse.** Alerte seulement.
