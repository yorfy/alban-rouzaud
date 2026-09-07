---
name: review-transcription
description: >
  Revue et correction d'une transcription de manuscrit (.txt).
  Utiliser quand l'utilisateur veut relire, corriger ou améliorer
  une transcription existante, ou détecter les erreurs de lecture.
metadata:
  author: transcrib
  version: "1.0"
  language: fr
compatibility: >
  Fonctionne sur tout fichier .txt produit par le skill transcribe-manuscript.
  Accès aux images sources recommandé pour la phase 3.
---

# Revue d'une transcription de manuscrit

Quatre phases. Entrée : un fichier `<X>.txt` issu d'une transcription. Sortie : un fichier `<X>_revue.txt` corrigé et un rapport `<X>_revue_rapport.md`.

## Phase 1 — Préparer

Collecter auprès de l'utilisateur :
- le fichier .txt à relire
- le dossier d'images sources (si disponible, pour vérification visuelle)
- le périmètre : tout le texte ou une section (ex. « journées 1 à 6 »)

Lire le texte ciblé. Identifier les personnages, lieux et noms propres récurrents. Construire un **dictionnaire contextuel** : pour chaque nom propre, compter ses occurrences. Ce dictionnaire sert en phase 2 à repérer les hapax suspects (nom apparaissant une seule fois alors qu'un nom proche apparaît souvent).

**Critère de fin** : le texte est chargé, le périmètre est délimité, le dictionnaire de noms propres est construit.

## Phase 2 — Détecter

Parcourir le texte et appliquer les trois niveaux de détection décrits dans `references/regles-revue.md` :

1. **Règles mécaniques** — typographie, guillemets, accents, casse, espaces.
2. **Dictionnaire contextuel** — noms propres incohérents, hapax suspects, mots inexistants.
3. **Analyse sémantique** — mots existants mais incohérents dans le contexte, phrases absurdes, confusions de lettres manuscrites.

Pour chaque anomalie trouvée, produire une entrée :
```
[TYPE] "texte original" → "correction proposée" (contexte : ...phrase...)
```

Types : `GUILLEMET`, `ESPACE_TYPO`, `ACCENT`, `CASSE`, `MOT_INEXISTANT`, `NOM_PROPRE`, `LECTURE_ERRONEE`, `PONCTUATION`, `PARAGRAPHE`, `SENS_DOUTEUX`.

Voir `references/erreurs-types.md` pour des exemples concrets issus de l'analyse du corpus ALBAN ROUZAUD 2.

**Critère de fin** : la liste complète des anomalies détectées est constituée, classée par type.

## Phase 3 — Corriger

Appliquer les corrections par niveau de confiance :

**Corrections automatiques** (confiance haute — appliquer sans demander) :
- Guillemets `"..."` → `« ... »` avec espaces insécables.
- Espaces typographiques françaises manquantes.
- Accents manquants sur des mots courants (`metres` → `mètres`).
- Casse évidente (minuscule après `.` `!` `?`).

**Corrections proposées** (confiance moyenne — signaler dans le rapport) :
- Mots inexistants avec une suggestion (ex. `démantons` → `démontons`).
- Noms propres hapax (ex. `Induï` apparaît 1 fois, `André` apparaît 47 fois).
- Mots coupés mal recollés (`n'au- vont` → `n'auront`).
- Paragraphes trop longs à découper (coupure proposée aux points de changement de scène ou de dialogue).

**Alertes** (confiance basse — signaler seulement) :
- Mots existants au sens douteux dans le contexte.
- Passages où la relecture visuelle de l'image source est recommandée.

Si les images sources sont disponibles, vérifier visuellement les corrections de confiance moyenne sur l'image de la page correspondante. OVERRIDE : un sub-agent `general-task-execution` par page à vérifier, avec l'image et le texte de la page. Maximum 14 sub-agents par vague.

Produire `<X>_revue.txt` avec toutes les corrections appliquées.

**Critère de fin** : `<X>_revue.txt` existe, toutes les corrections automatiques sont appliquées, les corrections proposées et alertes sont listées.

## Phase 4 — Rapport

Générer `<X>_revue_rapport.md` avec :

```markdown
# Rapport de revue — <TITRE>

## Résumé
- Périmètre : ...
- Corrections automatiques appliquées : N
- Corrections proposées : N
- Alertes : N

## Corrections automatiques appliquées
| # | Type | Avant | Après | Page |
|---|------|-------|-------|------|

## Corrections proposées (à valider)
| # | Type | Avant | Après proposé | Page | Confiance |
|---|------|-------|---------------|------|-----------|

## Alertes (relecture recommandée)
| # | Type | Passage | Page | Remarque |
|---|------|---------|------|----------|

## Dictionnaire des noms propres
| Nom | Occurrences | Variantes détectées |
|-----|-------------|---------------------|
```

**Critère de fin** : le rapport existe à côté du fichier corrigé.
