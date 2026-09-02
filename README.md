# Transcription des manuscrits d'Alban Rouzaud

Transcription automatique de documents manuscrits (PDF ou images) via le skill Kiro `transcribe-manuscript`. Le modèle IA lit directement les images et produit un texte structuré en paragraphes.

## Manuscrits transcrits

| # | Document | Pages | PDF |
|---|----------|-------|-----|
| 1 | La Guerre (1939-1940) | 41 | [Télécharger](https://drive.google.com/file/d/1eEFtKvP_8kEG_qQVTPKMJxi6TKhQs4-I/view?usp=sharing) |
| 2 | Journal non écrit d'un fantassin en repli stratégique | 92 | [Télécharger](https://drive.google.com/file/d/1JKTnWPOrwgF-Oi9N0_5aGpOe_2UbRlX9/view?usp=sharing) |
| 3 | L'Évasion | 73 | [Télécharger](https://drive.google.com/file/d/1mRKi9u4zP9oXgVjFl_Fuj4GTTESVpxIA/view?usp=sharing) |
| 4 | Captivité, récits et réflexions | 82 | [Télécharger](https://drive.google.com/file/d/1ZW2hv8iLNkZE0e73iSyS1fN-bNBj3H_X/view?usp=sharing) |

Les fichiers PDF sont hébergés sur Google Drive (trop volumineux pour git).
Les transcriptions `.txt`, les rapports `.md`, les cartes `.html` et la config Kiro sont dans ce repo.

## Structure du workspace

```
ALBAN ROUZAUD_N_TITRE.txt            ← transcription finale assemblée
ALBAN ROUZAUD_N_TITRE/
├── pages/                           ← un .txt par page
├── ALBAN ROUZAUD_N_TITRE_rapport.md ← rapport de transcription
└── images/ / images_small/          ← pages scannées (exclues du repo)
ALBAN_ROUZAUD_N_CARTE.html           ← carte interactive du parcours
FRISE_CHRONOLOGIQUE.html             ← frise chronologique
ANALYSE_GLOBALE_TAMPONS_*.md         ← analyses transversales
```

## Prérequis

- **Kiro IDE** avec accès aux sub-agents
- **Python 3.10+** avec Pillow (`pip install Pillow`)
- **pymupdf** pour la conversion PDF → images (`pip install pymupdf`)

## Utilisation

Dans Kiro, invoquer le skill :

```
/transcribe-manuscript
```

Ou simplement demander : *"Transcris ce manuscrit"* — Kiro détecte le skill automatiquement.

Le skill demande la source (PDF ou dossier d'images), la langue et le contexte du document, puis exécute 6 phases automatiques : préparation, transcription parallèle, assemblage, validation de l'ordre, rapport et nettoyage.

## Skills disponibles

| Skill | Description |
|-------|-------------|
| `transcribe-manuscript` | Transcription d'un PDF scanné en texte structuré |
| `review-transcription` | Revue et correction d'une transcription existante |
| `format-manuscript` | Génération d'un DOCX mis en page depuis un `.txt` |
| `generate-map` | Carte HTML interactive du parcours décrit |
| `writing-for-agents` | Rédaction de skills, steering et docs agent-facing |
