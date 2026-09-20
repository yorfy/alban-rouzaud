---
name: fetch-gdrive-docx
description: "Récupère les cahiers DOCX d'Alban Rouzaud hébergés sur Google Drive (Google Docs partagés en lecture publique) et les place dans docs/, en écrasant les versions locales. Utiliser quand l'utilisateur veut télécharger, récupérer, resynchroniser ou mettre à jour les DOCX des cahiers depuis Google Drive."
metadata:
  author: transcrib
  version: "1.0"
  language: fr
compatibility: >
  Python 3.10+. Aucune dépendance externe (stdlib urllib). Les 4 Google Docs
  doivent rester partagés en lecture publique ("tous les utilisateurs disposant
  du lien"). Aucun credential ni OAuth requis.
---

# Récupération des cahiers DOCX depuis Google Drive

Les 4 cahiers sont hébergés comme **Google Docs partagés en lecture publique**. Chacun s'exporte en DOCX sans authentification via l'endpoint d'export Google (`/export?format=docx`). Le script `fetch_gdrive_docx.py` télécharge et écrit dans `docs/`, en **écrasant** les fichiers de même nom — les versions Drive font foi.

Le nom de fichier n'est **pas** codé en dur : il est lu dans l'en-tête `Content-Disposition` renvoyé par Google, donc si un titre change côté Drive le fichier local suit automatiquement.

## Table des cahiers

Les IDs des documents vivent dans le script (`CAHIERS`) et sont issus du `README.md` du repo :

| N° | Cahier | Nom de fichier attendu |
|----|--------|------------------------|
| 1 | La Guerre (1939-1940) | `ALBAN ROUZAUD_1_LA GUERRE.docx` |
| 2 | Journal non écrit d'un fantassin | `ALBAN ROUZAUD_2_JOURNAL NON ECRIT D'UN FANTASSIN EN REPLIS STRATEGIQUE.docx` |
| 3 | L'Évasion | `ALBAN ROUZAUD_3_L'EVASION.docx` |
| 4 | Captivité, récits et réflexions | `ALBAN ROUZAUD_4_CAPTIVITE, RECITS ET REFLEXIONS.docx` |

## Étape 1 — Lancer le téléchargement

Depuis la racine du repo (`C:\no_scan\code\transcrib`) :

```
python .kiro\skills\fetch-gdrive-docx\fetch_gdrive_docx.py
```

Options utiles :

- `--dry-run` — affiche les fichiers cibles sans rien écrire (vérifier l'accès public avant d'écraser).
- `3` — ne récupère qu'un seul cahier, par numéro (`1`..`4`).
- `--dest <dir>` — dossier de destination (défaut : `docs`).

## Étape 2 — Vérifier

- Le script affiche pour chaque cahier `créé` ou `écrasé` avec la taille en octets.
- Une réponse de moins de 1000 octets déclenche une erreur explicite (`doc privé ?`) : dans ce cas le document n'est plus partagé publiquement et il faut soit rétablir le partage, soit passer par l'API Google Drive (non couvert par ce skill).

## Guardrails

- Le skill **écrase** les DOCX locaux sans confirmation — c'est le comportement voulu. Si l'utilisateur veut une comparaison plutôt qu'un écrasement, utiliser `--dest` vers un dossier temporaire.
- Ne PAS committer les DOCX récupérés sans que l'utilisateur le demande : `docs/*.docx` peut être suivi par git dans ce repo, donc un téléchargement modifie l'arbre de travail. Présenter le `git status` et laisser l'utilisateur décider.
- Si un ID change ou un cahier est ajouté, mettre à jour la table `CAHIERS` du script **et** la table ci-dessus, en cohérence avec le `README.md`.
