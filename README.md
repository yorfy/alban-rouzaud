# Transcription des manuscrits d'Alban Rouzaud

**Livrable public** : [https://yorfy.github.io/alban-rouzaud/ECRITS_DE_GUERRE.html](https://yorfy.github.io/alban-rouzaud/ECRITS_DE_GUERRE.html)

Transcription automatique de documents manuscrits (PDF ou images) via le skill Kiro `transcribe-manuscript`. Le modèle IA lit directement les images et produit un texte structuré en paragraphes.

## Manuscrits transcrits

| # | Document | Pages | DOCX |
|---|----------|-------|------|
| 1 | La Guerre (1939-1940) | 41 | [Ouvrir](https://docs.google.com/document/d/1cuSB04MSC8-Fyp5qBXDpXo0cc8VR9cs4/edit?usp=drive_link) |
| 2 | Journal non écrit d'un fantassin en repli stratégique | 92 | [Ouvrir](https://docs.google.com/document/d/1CJ_H8KuLxS6C2K5QgyMGPXW4mBOQLGyT/edit?usp=drive_link) |
| 3 | L'Évasion | 73 | [Ouvrir](https://docs.google.com/document/d/1LlsB4U3KwqlwQ5cNaj8wKaccrTnL7hu0/edit?usp=drive_link) |
| 4 | Captivité, récits et réflexions | 82 | [Ouvrir](https://docs.google.com/document/d/12HeGY9vhKJKc71NK3ajLXALOVU3sg5kk/edit?usp=drive_link) |

Les fichiers DOCX sont hébergés sur Google Drive.
Les transcriptions `.txt`, les rapports `.md`, les cartes `.html` et la config Kiro sont dans ce repo.

## Structure du repo

```
ECRITS_DE_GUERRE.html            ← livrable principal (carte interactive des 4 cahiers, 78 KB)
README.md
extract_data.py                  ← script de maintenance (extraction données HTML → JS)
│
├── data/                        ← données géographiques et textuelles par cahier
│   ├── data_c1.js               ← C1 : stops, CPA, routes GPS (La Guerre)
│   ├── data_c2.js               ← C2 : stops, routes GPS (Journal non écrit)
│   ├── data_c3.js               ← C3 : stops, CPA, routes GPS, profil altitude (L'Évasion)
│   └── data_c4.js               ← C4 : stops, CPA (Captivité)
│
├── cartes/                      ← cartes HTML secondaires et fichiers géo
│   ├── ALBAN_ROUZAUD_1_CARTE.html
│   ├── ALBAN ROUZAUD_2_CARTE_PARCOURS.html
│   ├── ALBAN ROUZAUD_3_CARTE_EVASION.html
│   ├── ALBAN_ROUZAUD_3_EVASION_MARKERS.html
│   ├── ALBAN_ROUZAUD_3_EVASION_MAPLIBRE.html
│   ├── ALBAN_ROUZAUD_3_EVASION_PARCOURS.kml
│   ├── ALBAN_ROUZAUD_CROQUIS_EVASION.svg
│   └── VELO_PARCOURS_EVASION.html
│
├── cartes_postales/             ← images + galerie HTML (cartes postales, photos d'archives)
│   ├── CARTES_POSTALES_ANCIENNES.html   ← galerie interactive
│   └── *.jpg / *.png / *.JPG
│
├── docs/                        ← documents et analyses
│   ├── ALBAN ROUZAUD_N_TITRE.txt      ← transcription finale assemblée
│   ├── ALBAN ROUZAUD_N_TITRE.docx     ← version mise en page
│   ├── ANALYSE_GLOBALE_TAMPONS_*.md
│   ├── ARBEITSKOMMANDOS_STALAG_XVIII_A.md
│   └── BIBLIOGRAPHIE_JEAN_BELLUS.md
│
├── transcriptions/              ← dossiers de travail par cahier (pages, rapports)
│   └── ALBAN ROUZAUD_N_TITRE/
│       ├── pages/               ← un .txt par page scannée
│       ├── *_rapport.md         ← rapport de transcription
│       └── images/              ← pages scannées (exclues du repo, ignorées par git)
│
└── cahiers/                     ← PDFs originaux (ignorés par git, hébergés sur Google Drive)
    ├── ALBAN ROUZAUD_1_LA GUERRE.pdf
    ├── ALBAN ROUZAUD_2_JOURNAL NON ECRIT (...).pdf
    ├── ALBAN ROUZAUD_3_L'EVASION.pdf
    └── ALBAN ROUZAUD_4_CAPTIVITE, RECITS ET REFLEXIONS.pdf
```

**ECRITS_DE_GUERRE.html** — Carte interactive des 4 cahiers de guerre d'Alban Rouzaud (MapLibre GL JS 4.7.1). Le HTML ne contient que la structure et le moteur JS (~78 KB) ; les données géographiques sont dans `data/`. Page de garde narrative, onglets par cahier, modèle accumulatif, profil altitude C3, cartes postales, contrôle d'exagération du relief (clic milieu + drag), pill ×1.0 sous la boussole.

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
| `docx-to-pdf` | Conversion de DOCX en PDF via l'API COM de Word (Windows) |
| `generate-map` | Carte HTML interactive du parcours décrit |
| `writing-for-agents` | Rédaction de skills, steering et docs agent-facing |
